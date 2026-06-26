#!/usr/bin/env python3
"""Check for messages TO chanel FROM hermes via Redis"""

import sys
import json
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cfm_messenger import CFMMessenger

def main():
    try:
        with CFMMessenger('chanel') as m:
            msgs = m.get_messages(limit=10)
            hermes_msgs = [msg for msg in msgs if msg.get('from') == 'hermes']
            if hermes_msgs:
                print('HERMES_MESSAGES_FOUND')
                for msg in hermes_msgs:
                    print(json.dumps(msg, ensure_ascii=False))
            else:
                print('NO_HERMES_MESSAGES')
    except Exception as e:
        print(f'ERROR: {e}')

if __name__ == '__main__':
    main()
