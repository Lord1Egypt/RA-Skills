#!/usr/bin/env python3
import argparse, json, time, uuid
from pathlib import Path

QUEUE_DIR = Path('/root/.openclaw/workspace-dev/skills/feishu-card-sender/tmp/callback-queue')


def main():
    p = argparse.ArgumentParser(description='enqueue card callback job')
    p.add_argument('--payload', required=True)
    p.add_argument('--message-id', required=True)
    p.add_argument('--user-id', required=True)
    p.add_argument('--account-id', default='1')
    p.add_argument('--channel', default='feishu')
    args = p.parse_args()

    payload = json.loads(args.payload)
    job = {
        'payload': payload,
        'message_id': args.message_id,
        'user_id': args.user_id,
        'account_id': args.account_id,
        'channel': args.channel,
        'enqueued_at': time.time(),
    }
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    name = f"{int(time.time()*1000)}-{uuid.uuid4().hex}.json"
    f = QUEUE_DIR / name
    f.write_text(json.dumps(job, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({'ok': True, 'job': str(f)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
