#!/usr/bin/env python3
"""Check for messages FROM chanel via Redis"""
import redis
import json
import time

def main():
    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
    except Exception as e:
        print(f"REDIS_ERROR: {e}")
        return

    # Check stored messages where chanel is the sender
    # Messages from chanel would be stored in various keys
    # Check all message stores for messages FROM chanel
    all_keys = r.keys("cfm:*:messages")
    
    chanel_sent_msgs = []
    seen_ids = set()
    
    for key in all_keys:
        messages = r.lrange(key, 0, 50)
        for msg_str in messages:
            try:
                msg = json.loads(msg_str)
                if msg.get('from') == 'chanel' and msg.get('id') not in seen_ids:
                    chanel_sent_msgs.append(msg)
                    seen_ids.add(msg.get('id'))
            except:
                pass
    
    # Also check real-time Pub/Sub (Hermes inbox for messages from chanel)
    pubsub = r.pubsub()
    pubsub.subscribe("cfm:hermes:inbox")
    pubsub.get_message(timeout=0.5)  # consume subscription confirmation
    
    start = time.time()
    while time.time() - start < 3:
        msg = pubsub.get_message(timeout=1)
        if msg and msg.get("type") == "message":
            data = json.loads(msg["data"])
            if data.get("from") == "chanel":
                chanel_sent_msgs.append(data)
    
    pubsub.unsubscribe()
    pubsub.close()
    r.close()
    
    if chanel_sent_msgs:
        print("CHANEL_MESSAGES_FOUND")
        for m in chanel_sent_msgs:
            print(json.dumps(m, ensure_ascii=False))
    else:
        print("NO_CHANEL_MESSAGES")

if __name__ == '__main__':
    main()
