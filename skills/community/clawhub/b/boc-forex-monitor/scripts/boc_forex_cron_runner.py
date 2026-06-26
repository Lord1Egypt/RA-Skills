#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path.cwd()
STATE_DIR = ROOT / '.openclaw-state'
STATE_DIR.mkdir(parents=True, exist_ok=True)
NOTIFY_STATE_PATH = STATE_DIR / 'boc-forex-alert-notify-state.json'
CHECK_SCRIPT = SCRIPT_DIR / 'boc_forex_check.py'


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None


def save_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def fmt(x):
    s = f"{float(x):.4f}"
    return s.rstrip('0').rstrip('.')


def ordered_currencies(data):
    monitoring = data.get('monitoring') or []
    seen = [item.get('currency') for item in monitoring if item.get('currency')]
    for key in (data.get('picked') or {}).keys():
        if key not in seen:
            seen.append(key)
    return seen


def build_body(data):
    picked = data.get('picked') or {}
    pub_date = None
    pub_time = None
    for key in ordered_currencies(data):
        row = picked.get(key)
        if row and (row.get('pubDate') or row.get('pubTime')):
            pub_date = row.get('pubDate')
            pub_time = row.get('pubTime')
            break
    first = '更新时间：' + ' '.join([x for x in [pub_date, pub_time] if x]) if (pub_date or pub_time) else '更新时间：未知'
    lines = [first]
    deltas = data.get('deltas') or {}
    for key in ordered_currencies(data):
        row = picked.get(key)
        if not row:
            continue
        value = row.get('value')
        column = row.get('column')
        if key in deltas:
            delta = float(deltas[key])
            baseline = float(value) - delta
            lines.append(f"{row.get('name', key)}（{column}）：{fmt(value)}（基线：{fmt(baseline)}，差值：{fmt(delta)}）")
        else:
            lines.append(f"{row.get('name', key)}（{column}）：{fmt(value)}")
    return '\n'.join(lines)


def run_check():
    proc = subprocess.run([sys.executable, str(CHECK_SCRIPT)], cwd=str(ROOT), capture_output=True, text=True)
    if proc.returncode not in (0, 10):
        err = (proc.stderr or proc.stdout or '').strip()
        print('❌ 汇率检查执行失败')
        if err:
            print(err)
        return proc.returncode, None
    raw = (proc.stdout or '').strip()
    if not raw:
        print('❌ 汇率检查执行失败')
        print('empty stdout')
        return proc.returncode, None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print('❌ 汇率检查执行失败')
        print(raw)
        return proc.returncode, None
    if 'status' not in data:
        print('❌ 汇率检查执行失败')
        print(raw)
        return proc.returncode, None
    return proc.returncode, data


def send_openclaw_message(channel: str, target: str, message: str, account_id: str | None = None):
    cmd = ['openclaw', 'message', 'send', '--channel', channel, '--target', target, '--message', message]
    if account_id:
        cmd.extend(['--account', account_id])
    return subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--notify-channel', default=os.getenv('BOC_FOREX_NOTIFY_CHANNEL'))
    parser.add_argument('--notify-target', default=os.getenv('BOC_FOREX_NOTIFY_TARGET'))
    parser.add_argument('--notify-account-id', default=os.getenv('BOC_FOREX_NOTIFY_ACCOUNT_ID'))
    parser.add_argument('--no-notify', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    _, data = run_check()
    if data is None:
        return 2

    status = data.get('status')
    body = build_body(data)

    if status == 'skipped':
        print(f"⏭️ 汇率检查跳过 | {data.get('message') or data.get('reason') or 'unknown'}")
        return 0

    if status in ('baseline-updated', 'ok'):
        print('✅ 汇率检查完成')
        print(body)
        return 0

    if status == 'trigger':
        notify_state = load_json(NOTIFY_STATE_PATH) or {}
        trigger_ts = data.get('timestamp')
        trigger_summary = data.get('triggerSummary') or data.get('summary') or '汇率触发提醒'
        if notify_state.get('lastNotifiedTriggerTimestamp') == trigger_ts:
            print('⚠️ 已触发阈值，但通知已发送过')
            print(body)
            print(f'触发摘要：{trigger_summary}')
            return 0

        if args.no_notify or not args.notify_channel or not args.notify_target:
            print('⚠️ 已触发阈值，但未配置外部通知')
            print(body)
            print(f'触发摘要：{trigger_summary}')
            return 0

        proc = send_openclaw_message(args.notify_channel, args.notify_target, trigger_summary, args.notify_account_id)
        if proc.returncode == 0:
            save_json(NOTIFY_STATE_PATH, {
                'lastNotifiedTriggerTimestamp': trigger_ts,
                'lastNotifiedTriggerSummary': trigger_summary,
                'updatedAt': datetime.now(timezone.utc).isoformat(),
                'channel': args.notify_channel,
                'target': args.notify_target,
                'accountId': args.notify_account_id,
                'note': 'sent via openclaw message send',
            })
            print('🔔 已触发阈值并发送提醒')
            print(body)
            print(f'触发摘要：{trigger_summary}')
            return 0

        err = (proc.stderr or proc.stdout or '').strip()
        print('⚠️ 已触发阈值，但消息发送失败')
        print(body)
        print(f'触发摘要：{trigger_summary}')
        if err:
            print(f'发送错误：{err}')
        return 1

    print('❌ 汇率检查执行失败')
    print(json.dumps(data, ensure_ascii=False))
    return 2


if __name__ == '__main__':
    raise SystemExit(main())
