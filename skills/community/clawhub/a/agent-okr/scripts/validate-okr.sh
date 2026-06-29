#!/bin/bash
# validate-okr.sh — 校验所有 Agent OKR 文件
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WS_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
OKR_DIR="$WS_DIR/docs/agent-okr"

if [ ! -d "$OKR_DIR" ]; then
  echo "❌ OKR 目录不存在: $OKR_DIR"
  exit 1
fi

ERRORS=0
VALID=0

echo "🔍 校验 Agent OKR..."
echo "   目录: $OKR_DIR"
echo ""

for f in "$OKR_DIR"/*.yaml "$OKR_DIR"/*.yml; do
  [ -f "$f" ] || continue
  fname=$(basename "$f")
  
  ISSUES=$(python3 -c "
import yaml, sys

with open('$f') as fh:
    try:
        d = yaml.safe_load(fh)
    except yaml.YAMLError as e:
        print(f'ERRORS:YAML解析失败: {e}')
        sys.exit(0)

errors = []

# Required fields
for field in ['agent', 'period', 'status', 'objective', 'mainline', 'key_results']:
    if field not in d:
        errors.append(f'缺少必填字段: {field}')

# Validate key_results
krs = d.get('key_results', [])
if not isinstance(krs, list) or len(krs) == 0:
    errors.append('key_results 必须是非空数组')
else:
    for i, kr in enumerate(krs):
        if not isinstance(kr, dict):
            errors.append(f'KR[{i}] 不是字典')
            continue
        for kf in ['id', 'description', 'target', 'current']:
            if kf not in kr:
                errors.append(f'KR[{i}] 缺少字段: {kf}')

# Validate period format
period = str(d.get('period', ''))
import re
if not re.match(r'^\d{4}-\d{2}$', period):
    errors.append(f'period 格式错误: {period} (应为 YYYY-MM)')

# Validate status
valid_status = ['active', 'completed', 'archived']
if d.get('status') not in valid_status:
    errors.append(f'status 非法: {d.get(\"status\")}')

if errors:
    print('ERRORS:' + '; '.join(errors))
" 2>&1)

  if [ -n "$ISSUES" ]; then
    echo "❌ $fname: $(echo "$ISSUES" | sed 's/^ERRORS://')"
    ERRORS=$((ERRORS + 1))
  else
    echo "✅ $fname"
    VALID=$((VALID + 1))
  fi
done

echo ""
echo "📊 结果: ✅${VALID}个有效 ❌${ERRORS}个错误"
[ "$ERRORS" -gt 0 ] && exit 1
