#!/usr/bin/env python3
from __future__ import annotations
import argparse
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(description='Generate an OpenClaw one-shot Feishu cron smoke test command.')
parser.add_argument('--open-id', required=True, help='Feishu open_id without the user: prefix')
parser.add_argument('--account', default='default', help='OpenClaw channel account id')
parser.add_argument('--minutes', type=int, default=2, help='How many minutes from now to schedule the smoke test')
parser.add_argument('--tz', default='Asia/Shanghai', help='Timezone for the cron add command')
parser.add_argument('--name', default='Feishu delivery smoke test', help='Cron job name')
args = parser.parse_args()

run_at = datetime.now() + timedelta(minutes=args.minutes)
iso_local = run_at.strftime('%Y-%m-%dT%H:%M:%S')
message = '在本轮只输出这一句话：主动消息链路测试：如果你看到这条，说明 Feishu cron 外发成功。'
cmd = f'''openclaw cron add \\
  --name "{args.name}" \\
  --at "{iso_local}" \\
  --tz "{args.tz}" \\
  --session isolated \\
  --message "{message}" \\
  --announce \\
  --channel feishu \\
  --account {args.account} \\
  --to "user:{args.open_id}" \\
  --delete-after-run'''
print(cmd)
