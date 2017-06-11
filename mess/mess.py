# -*- coding: utf-8 -*-
"""
Created on Fri May 20 22:00:32 2016

@author: willsaults
"""
import os
import sys
import time
import random
import csv
from collections import defaultdict

from tempfile import NamedTemporaryFile
import shutil

contacts_filename = "contacts.csv"
message_schedule_filename = "messageSchedule.csv"

def test():
    _message("jess")

def setup():

    # Create csv to manage message contacts
    isfile = os.path.isfile(contacts_filename)
    if not isfile:
        with open(contacts_filename, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['name','relation','phone','frequency-day-min','frequency-day-max','frequency-hour-min','frequency-hour-max'])
            writer.writerow(['test','other','5555555555','0','0','0','0'])

    # Create csv to manage the message schedule
    isfile = os.path.isfile(message_schedule_filename)
    if not isfile:
        with open(message_schedule_filename, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['name','message','firedate'])


def run():
    print("run")
    
    
def new_message(contactname):
    message = _generate_message(contactname)
    _update_schedule(contactname, message, None)





def _firedate(contactname):
    # This will use the frequency values for the contact to determine
    # an appropriate timestamp.
    timestamp = int(time.time())
    return timestamp
    
def _generate_message(contactname):
    messages = _messages(contactname)
    message = random.choice(messages)     
    message = _modify_message(message)
    return message
    
def _modify_message(message):
    
    # Lowercase string
    rnum = random.randrange(0, 3)
    if rnum == 0:
        message = message.lower()
    
    # Remove last character unless it's a question mark or an emoji.
    rnum = random.randrange(0, 2)
    if rnum == 0 and "?" not in message:
        message = message[:-1]
        
    return message


def _message(contactname):
    message = _generate_message(contactname)
    timestamp = _firedate(contactname)
    _update_schedule(contactname, message, timestamp)


def _messages(contactname):
    contacttype = None
    with open(contacts_filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            for field in row:
                if field == contactname:
                    contacttype = row[1]

    if contacttype != None:
        columns = defaultdict(list)

        with open("messages.csv", 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                for (k,v) in row.items(): # go over each column name and value
                    columns[k].append(v) # append the value into the appropriate list

        return columns[contacttype]


def _update_schedule(contactname, message, timestamp):

    updatedline = None

    with open(message_schedule_filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for (k,v) in row.items():
                if k == 'name' and v == contactname:
                    updatedline = reader.line_num


    if updatedline != None:
        # update the row
        tempfile = NamedTemporaryFile(delete=False)

        with open(message_schedule_filename, 'rb') as csvFile, tempfile:
            reader = csv.reader(csvFile, delimiter=',')
            writer = csv.writer(tempfile, delimiter=',')

            for row in reader:
                if reader.line_num == updatedline:
                    row[1] = message
                    if timestamp != None:
                        row[2] = timestamp
                    
                writer.writerow(row)

        shutil.move(tempfile.name, message_schedule_filename)
    else:
        # apppend
        with open(message_schedule_filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow([contactname,message,timestamp])

