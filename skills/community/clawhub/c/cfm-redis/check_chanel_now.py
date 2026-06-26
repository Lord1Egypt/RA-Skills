#!/usr/bin/env python3
"""Check for messages TO chanel FROM hermes via Redis Pub/Sub"""
import redis
import json
import sys
import time

def main():
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
    except Exception as e:
        print(f"REDIS_ERROR: {e}")
        return

    # Check stored messages for chanel (messages sent to chanel)
    messages = r.lrange("cfm:chanel:messages", 0, 20)
    chanel_msgs = []
    for msg_str in messages:
        try:
            msg = json.loads(msg_str)
            chanel_msgs.append(msg)
        except:
            pass
    
    # Filter for messages FROM hermes
    hermes_msgs = [m for m in chanel_msgs if m.get('from') == 'hermes']
    
    if hermes_msgs:
        print("HERMES_MESSAGES_FOUND")
        for m in hermes_msgs:
            print(json.dumps(m, ensure_ascii=False))
    else:
        # Also try real-time Pub/Sub with short timeout
        pubsub = r.pubsub()
        pubsub.subscribe("cfm:chanel:inbox")
        
        # Consume any subscription confirmation
        msg = pubsub.get_message(timeout=1)
        
        # Wait briefly for real-time messages
        found = False
        start = time.time()
        while time.time() - start < 3:
            msg = pubsub.get_message(timeout=1)
            if msg and msg.get("type") == "message":
                data = json.loads(msg["data"])
                if data.get("from") == "hermes":
                    print("HERMES_MESSAGES_FOUND")
                    print(json.dumps(data, ensure_ascii=False))
                    found = True
                    break
        
        pubsub.unsubscribe()
        pubsub.close()
        
        if not found:
            print("NO_HERMES_MESSAGES")
    
    r.close()

if __name__ == '__main__':
    main()
