#!/bin/bash
# Cron 单任务修复脚本
# 将指定任务修复为合法的投递配置
# 用法: bash skills/cron-delivery-fix/scripts/fix-single.sh <job-id> [--announce|--silent]
#
# --announce: 修复为投递模式（isolated + announce + 完整投递参数）
# --silent:   修复为静默模式（isolated + none）

set -euo pipefail

STD_CHANNEL="openclaw-weixin"
STD_TO="YOUR_WECHAT_USER_ID@im.wechat"
STD_ACCOUNT="54f3a3da9e82-im-bot"

usage() {
    echo "用法: $0 <job-id> [--announce|--silent]"
    echo ""
    echo "  --announce  修复为投递模式（isolated + announce + 完整参数）"
    echo "  --silent    修复为静默模式（isolated + none，agent自行用message tool发送）"
    exit 1
}

if [ $# -lt 2 ]; then usage; fi

JOB_ID="$1"
MODE="$2"

case "$MODE" in
    --announce)
        echo "🔧 修复 $JOB_ID → announce 模式"
        # 先恢复为 isolated（如果被错误改为 main）
        RESULT=$(openclaw cron edit "$JOB_ID" \
            --session isolated \
            --announce \
            --channel "$STD_CHANNEL" \
            --to "$STD_TO" \
            --account "$STD_ACCOUNT" 2>&1)
        ;;
    --silent)
        echo "🔧 修复 $JOB_ID → silent 模式"
        RESULT=$(openclaw cron edit "$JOB_ID" \
            --session isolated \
            --no-deliver 2>&1)
        ;;
    *)
        usage
        ;;
esac

# 验证修复结果
VERIFY=$(echo "$RESULT" | python3 -c "
import json, sys
text = sys.stdin.read()
try:
    start = text.index('{')
    d = json.loads(text[start:])
    session = d.get('sessionTarget', '?')
    mode = d.get('delivery', {}).get('mode', '?')
    to = d.get('delivery', {}).get('to', '?')
    acct = d.get('delivery', {}).get('accountId', '?')
    kind = d.get('payload', {}).get('kind', '?')
    
    errors = []
    if session == 'main' and kind == 'agentTurn':
        errors.append('FATAL: main+agentTurn冲突')
    if mode == 'announce' and (not to or not acct):
        errors.append('FATAL: announce模式缺少投递参数')
    
    if errors:
        print('❌ 修复失败: ' + '; '.join(errors))
        sys.exit(1)
    else:
        print(f'✅ session={session} kind={kind} mode={mode}')
except Exception as e:
    print(f'⚠️ 无法解析输出: {e}')
    sys.exit(1)
" 2>&1)

echo "$VERIFY"
