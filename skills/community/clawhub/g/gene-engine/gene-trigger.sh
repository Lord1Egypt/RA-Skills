#!/bin/bash
# Gene Trigger Recorder - 记录Gene触发结果
# 用法：bash gene-trigger.sh <gene_key> <success|fail> <outcome描述>
# 示例：bash gene-trigger.sh gene24 success "三层验证通过，执行了决策"
# 示例：bash gene-trigger.sh gene26 fail "学到但72h内没有行为改变"

set -euo pipefail

GENE_FILE="$HOME/.openclaw/workspace/memory/gene-state.json"
NOW_ISO=$(TZ=Asia/Shanghai date +"%Y-%m-%dT%H:%M:%S+08:00")

if [ $# -lt 3 ]; then
  echo "用法: bash gene-trigger.sh <gene_key> <success|fail> <outcome描述>"
  echo ""
  echo "可用gene_key:"
  echo "  gene17  - 心跳采样"
  echo "  gene20  - 主动分层 (internalized)"
  echo "  gene23  - 公众号发布检查"
  echo "  gene24  - 三层验证法"
  echo "  gene25  - 激活条件检查"
  echo "  gene26  - 学以致用自检"
  exit 1
fi

GENE_KEY="_$1"
RESULT="$2"
OUTCOME="$3"

# 验证gene_key存在
if ! python3 -c "import json; d=json.load(open('$GENE_FILE')); assert '$GENE_KEY' in d" 2>/dev/null; then
  echo "❌ Gene '$1' 不存在"
  exit 1
fi

echo "=== Gene Trigger Recorder ==="
echo "Gene: $1"
echo "结果: $RESULT"
echo "描述: $OUTCOME"
echo "时间: $NOW_ISO"
echo ""

# 更新JSON
python3 -c "
import json, sys

with open('$GENE_FILE', 'r') as f:
    data = json.load(f)

gene = data['$GENE_KEY']
now = '$NOW_ISO'

# 更新基础字段
gene['lastTriggered'] = now
gene['triggeredCount'] = gene.get('triggeredCount', 0) + 1

if gene.get('daysSinceLastTrigger') is None:
    gene['daysSinceLastTrigger'] = 0

if '$RESULT' == 'success':
    gene['lastResult'] = {'success': True, 'outcome': '''$OUTCOME'''}
    gene['consecutiveFailures'] = 0
    gene['status'] = 'verified'
    gene['lastVerified'] = now
    # wakeUpRate: 每次成功都算改变判断
    gene['activationCount'] = gene.get('activationCount', 0) + 1
else:
    gene['lastResult'] = {'success': False, 'error': 'trigger_failed', 'reason': '''$OUTCOME'''}
    gene['consecutiveFailures'] = gene.get('consecutiveFailures', 0) + 1
    gene['totalFailures'] = gene.get('totalFailures', 0) + 1
    gene['lastFailure'] = now
    # 连续失败3次 → cooldown
    if gene['consecutiveFailures'] >= 3:
        gene['status'] = 'cooldown'
    # 总失败10次 → disabled
    if gene['totalFailures'] >= 10:
        gene['status'] = 'disabled'

# 重新计算wakeUpRate
tc = gene.get('triggeredCount', 0)
ac = gene.get('activationCount', 0)
if tc > 0:
    gene['wakeUpRate'] = round(ac / tc, 2)

# 更新时间戳
data['_updated'] = now

with open('$GENE_FILE', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('✅ 已更新')
print(f'  triggeredCount: {gene[\"triggeredCount\"]}')
print(f'  consecutiveFailures: {gene[\"consecutiveFailures\"]}')
print(f'  totalFailures: {gene[\"totalFailures\"]}')
print(f'  status: {gene[\"status\"]}')
print(f'  wakeUpRate: {gene.get(\"wakeUpRate\", \"N/A\")}')
"
