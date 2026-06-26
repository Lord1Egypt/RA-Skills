#!/bin/bash
# Cron 全量修复脚本
# 批量将所有投递类 cron 修复为标准配置
# 用法: bash skills/cron-delivery-fix/scripts/fix-all.sh
#
# 修复规则：
# 1. 所有 announce 模式的任务 → 确保完整投递参数 + isolated session
# 2. 所有 session=main 且 payload.kind=agentTurn 的任务 → 改为 isolated
# 3. 修复后自动运行 diagnose.sh 验证

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

STD_CHANNEL="openclaw-weixin"
STD_TO="YOUR_WECHAT_USER_ID@im.wechat"
STD_ACCOUNT="54f3a3da9e82-im-bot"

echo "🔧 Cron 全量修复"
echo "================"
echo ""

# 获取需要修复的任务列表
FIX_NEEDED=$(openclaw cron list --json 2>/dev/null | python3 -c "
import json, sys

data = json.loads(sys.stdin.read().split('{', 1)[1].rsplit('}', 1)[0] + '}')
# 重新解析
text = sys.stdin.read()
" 2>/dev/null || true)

# 用 Python 完成整个修复流程
openclaw cron list --json 2>/dev/null | python3 -c "
import json, sys, subprocess

text = sys.stdin.read()
start = text.index('{')
data = json.loads(text[start:])
jobs = data.get('jobs', data) if isinstance(data, dict) else data

std_channel = '$STD_CHANNEL'
std_to = '$STD_TO'
std_account = '$STD_ACCOUNT'

# 需要修复为 announce 的任务（有投递需求的）
announce_tasks = []
# 需要修复 session 的任务
session_fix_tasks = []

for job in jobs:
    job_id = job['id']
    name = job.get('name', '?')
    session = job.get('sessionTarget', 'isolated')
    payload_kind = job.get('payload', {}).get('kind', 'agentTurn')
    delivery = job.get('delivery', {})
    mode = delivery.get('mode', '')
    to = delivery.get('to', '')
    account = delivery.get('accountId', '')
    channel = delivery.get('channel', '')

    # 检测需要修复的情况
    needs_fix = False

    # 问题1: main + agentTurn
    if session == 'main' and payload_kind == 'agentTurn':
        needs_fix = True
        print(f'⚠️  {name}: main+agentTurn冲突，需要改为isolated')

    # 问题2: announce 缺少参数
    if mode == 'announce' and (not to or not account or not channel):
        needs_fix = True
        missing = []
        if not channel: missing.append('channel')
        if not to: missing.append('to')
        if not account: missing.append('accountId')
        print(f'⚠️  {name}: announce缺少{','.join(missing)}')

    # 问题3: announce 参数不匹配标准值
    if mode == 'announce' and (channel != std_channel or to != std_to or account != std_account):
        needs_fix = True
        print(f'⚠️  {name}: 投递参数与标准不匹配')

    if needs_fix:
        # 判断应该用 announce 还是 silent
        # 如果之前是 announce 或者没有 mode，默认修复为 announce
        target_mode = mode if mode in ('announce', 'none') else 'announce'
        announce_tasks.append((job_id, name, target_mode))

if not announce_tasks:
    print('✅ 所有任务配置正常，无需修复')
    sys.exit(0)

print(f'\n共需修复 {len(announce_tasks)} 个任务\n')

for job_id, name, target_mode in announce_tasks:
    if target_mode == 'announce':
        cmd = ['openclaw', 'cron', 'edit', job_id,
               '--session', 'isolated',
               '--announce',
               '--channel', std_channel,
               '--to', std_to,
               '--account', std_account]
    else:
        cmd = ['openclaw', 'cron', 'edit', job_id,
               '--session', 'isolated',
               '--no-deliver']

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        out = result.stdout
        try:
            s = out.index('{')
            d = json.loads(out[s:])
            sess = d.get('sessionTarget', '?')
            m = d.get('delivery', {}).get('mode', '?')
            t = d.get('delivery', {}).get('to', '')
            if m == 'announce' and t == std_to:
                print(f'✅ {name}: session={sess} mode={m}')
            elif m == 'none':
                print(f'✅ {name}: session={sess} mode={m}')
            else:
                print(f'⚠️  {name}: 修复后参数异常，请手动检查')
        except:
            print(f'⚠️  {name}: 修复命令执行但输出解析失败')
    else:
        print(f'❌ {name}: 修复失败 - {result.stderr.strip()[:100]}')
" 2>&1

echo ""
echo "================"
echo "修复完成，运行诊断验证..."
echo ""

# 自动运行诊断
bash "$SCRIPT_DIR/diagnose.sh"
