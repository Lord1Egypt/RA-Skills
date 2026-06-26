#!/bin/bash
# Cron 投递诊断脚本
# 检查所有 cron 任务的投递配置是否合法
# 用法: bash skills/cron-delivery-fix/scripts/diagnose.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 标准投递参数（微信）
STD_CHANNEL="openclaw-weixin"
STD_TO="YOUR_WECHAT_USER_ID@im.wechat"
STD_ACCOUNT="54f3a3da9e82-im-bot"

echo "🔍 Cron 投递诊断"
echo "================"
echo ""

# 获取 cron 列表 JSON
JSON=$(openclaw cron list --json 2>/dev/null | sed -n '/^{/,$p')
if [ -z "$JSON" ]; then
    echo "❌ 无法获取 cron 列表"
    exit 1
fi

ISSUE_COUNT=0
TOTAL_COUNT=0

echo "$JSON" | python3 -c "
import json, sys

data = json.loads(sys.stdin.read())
jobs = data.get('jobs', data) if isinstance(data, dict) else data

std_channel = '$STD_CHANNEL'
std_to = '$STD_TO'
std_account = '$STD_ACCOUNT'

issues_found = 0
total = 0

for job in jobs:
    total += 1
    name = job.get('name', '?')
    job_id = job.get('id', '?')
    session = job.get('sessionTarget', '?')
    payload_kind = job.get('payload', {}).get('kind', '?')
    delivery = job.get('delivery', {})
    mode = delivery.get('mode', '')
    channel = delivery.get('channel', '')
    to = delivery.get('to', '')
    account = delivery.get('accountId', '')
    state = job.get('state', {})
    last_status = state.get('lastRunStatus', '-')
    last_deliv = state.get('lastDeliveryStatus', '-')

    errors = []

    # 规则1: main + agentTurn = 非法
    if session == 'main' and payload_kind == 'agentTurn':
        errors.append('main+agentTurn冲突(Gateway会拒绝)')

    # 规则2: announce 模式必须有三件套
    if mode == 'announce':
        if not channel:
            errors.append('announce模式缺少channel')
        if not to:
            errors.append('announce模式缺少to')
        if not account:
            errors.append('announce模式缺少accountId')
        if channel != std_channel:
            errors.append(f'channel应为{std_channel},实际为{channel}')
        if to != std_to:
            errors.append(f'to不匹配')
        if account != std_account:
            errors.append(f'accountId不匹配')

    # 规则3: isolated + announce 但上次投递失败
    if mode == 'announce' and session == 'isolated' and last_deliv == 'not-delivered' and last_status == 'ok':
        errors.append('上次执行成功但投递失败(可能是contextToken问题)')

    # 规则4: isolated + none 但 payload 里没有 message tool 发送指令
    if mode == 'none' and session == 'isolated':
        msg = job.get('payload', {}).get('message', '')
        if 'message tool' not in msg and 'message\"' not in msg and 'action: \"send\"' not in msg:
            # 某些任务确实不需要发消息（如记忆整理）
            pass  # 不算错误，但标记提醒

    if errors:
        issues_found += 1
        print(f'⚠️  [{job_id[:8]}] {name}')
        for e in errors:
            print(f'    → {e}')
        print(f'    当前: session={session} kind={payload_kind} mode={mode}')
        print(f'    上次: run={last_status} deliv={last_deliv}')
        print()
    else:
        mode_display = mode if mode else '(无)'
        print(f'✅  {name:40s} | {session:9s} | {mode_display:10s} | last:{last_status:4s}/{last_deliv}')

print()
print(f'总计: {total} 个任务, {issues_found} 个问题')
" 2>&1

echo ""
echo "================"
echo "诊断完成"
