#!/usr/bin/env python3
"""Check for CHANEL messages via Redis Pub/Sub"""

import sys
import json
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cfm_messenger import CFMMessenger

def main():
    try:
        with CFMMessenger('hermes') as m:
            msgs = m.get_messages(limit=10)
            chanel_msgs = [msg for msg in msgs if msg.get('from') == 'chanel']
            if chanel_msgs:
                print('CHANEL_MESSAGES_FOUND')
                for msg in chanel_msgs:
                    print(json.dumps(msg, ensure_ascii=False))
            else:
                print('NO_CHANEL_MESSAGES')
    except Exception as e:
        print(f'ERROR: {e}')

if __name__ == '__main__':
    main()
