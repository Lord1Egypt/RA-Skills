#!/usr/bin/env python3
"""CFM Listener - Check for CHANEL messages via Redis Pub/Sub"""

import redis
import json
import time
import os

def main():
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
    except Exception as e:
        print(f"REDIS_ERROR: {e}")
        return

    # Load already reported IDs
    reported = set()
    report_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.reported_ids')
    try:
        with open(report_file, 'r') as f:
            reported = set(line.strip() for line in f if line.strip())
    except:
        pass

    # Check stored messages in hermes inbox (messages FROM chanel)
    messages = r.lrange("cfm:hermes:messages", 0, 50)
    chanel_msgs = []
    for msg_str in messages:
        try:
            msg = json.loads(msg_str)
            if msg.get("from") == "chanel" and msg.get("id") not in reported:
                chanel_msgs.append(msg)
        except:
            pass

    if chanel_msgs:
        print("CHANEL_MESSAGES_FOUND")
        for m in chanel_msgs:
            print(json.dumps(m, ensure_ascii=False))
    else:
        # Also try real-time Pub/Sub with short timeout
        pubsub = r.pubsub()
        pubsub.subscribe("cfm:hermes:inbox")
        
        # Consume subscription confirmation
        msg = pubsub.get_message(timeout=1)
        
        # Wait briefly for real-time messages
        found = False
        start = time.time()
        while time.time() - start < 5:
            msg = pubsub.get_message(timeout=1)
            if msg and msg.get("type") == "message":
                data = json.loads(msg["data"])
                if data.get("from") == "chanel" and data.get("id") not in reported:
                    print("CHANEL_MESSAGES_FOUND")
                    print(json.dumps(data, ensure_ascii=False))
                    found = True
                    break
        
        pubsub.unsubscribe()
        pubsub.close()
        
        if not found:
            print("NO_NEW_CHANEL_MESSAGES")
    
    r.close()

if __name__ == '__main__':
    main()
