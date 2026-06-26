#!/bin/bash
# Cron 恢复脚本 — 将任务恢复为标准的 announce 配置
# 用于 AI 手动改坏配置后的紧急恢复
# 用法: bash skills/cron-delivery-fix/scripts/restore.sh <job-id>
#
# 强制将任务恢复为：
#   sessionTarget: isolated
#   delivery.mode: announce
#   delivery.channel: openclaw-weixin
#   delivery.to: YOUR_WECHAT_USER_ID@im.wechat
#   delivery.accountId: 54f3a3da9e82-im-bot

set -euo pipefail

if [ $# -lt 1 ]; then
    echo "用法: $0 <job-id>"
    exit 1
fi

JOB_ID="$1"

STD_CHANNEL="openclaw-weixin"
STD_TO="YOUR_WECHAT_USER_ID@im.wechat"
STD_ACCOUNT="54f3a3da9e82-im-bot"

echo "🔄 恢复 $JOB_ID 为标准 announce 配置..."

# 先获取当前配置
echo "--- 当前配置 ---"
openclaw cron list --json 2>/dev/null | python3 -c "
import json, sys
text = sys.stdin.read()
start = text.index('{')
data = json.loads(text[start:])
for job in data.get('jobs', data):
    if job['id'].startswith('$JOB_ID') or job['id'] == '$JOB_ID':
        print(f'  name: {job.get(\"name\")}')
        print(f'  session: {job.get(\"sessionTarget\")}')
        print(f'  kind: {job.get(\"payload\",{}).get(\"kind\")}')
        d = job.get('delivery', {})
        print(f'  mode: {d.get(\"mode\")}')
        print(f'  channel: {d.get(\"channel\")}')
        print(f'  to: {d.get(\"to\")}')
        print(f'  accountId: {d.get(\"accountId\")}')
        break
"

# 执行恢复
echo ""
echo "--- 执行恢复 ---"
RESULT=$(openclaw cron edit "$JOB_ID" \
    --session isolated \
    --announce \
    --channel "$STD_CHANNEL" \
    --to "$STD_TO" \
    --account "$STD_ACCOUNT" 2>&1)

echo "$RESULT" | python3 -c "
import json, sys
text = sys.stdin.read()
try:
    start = text.index('{')
    d = json.loads(text[start:])
    sess = d.get('sessionTarget', '?')
    mode = d.get('delivery', {}).get('mode', '?')
    to = d.get('delivery', {}).get('to', '?')
    acct = d.get('delivery', {}).get('accountId', '?')
    kind = d.get('payload', {}).get('kind', '?')
    
    ok = True
    if sess != 'isolated':
        print(f'❌ session={sess} (应为isolated)'); ok = False
    if mode != 'announce':
        print(f'❌ mode={mode} (应为announce)'); ok = False
    if not to:
        print(f'❌ to 为空'); ok = False
    if not acct:
        print(f'❌ accountId 为空'); ok = False
    
    if ok:
        print(f'✅ 恢复成功: session={sess} kind={kind} mode={mode}')
    else:
        print('⚠️ 恢复后仍有问题，请检查')
except Exception as e:
    print(f'❌ 解析失败: {e}')
"

echo ""
echo "恢复完成。建议运行 diagnose.sh 确认所有任务状态。"
