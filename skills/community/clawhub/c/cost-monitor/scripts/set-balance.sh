#!/bin/bash
# set-balance: 修改余额文件
# Usage: set-balance deepseek <rmb>
#        set-balance mimo <consumed> / <total>
# 直接从后台复制粘贴，如: set-balance mimo 3,933,069,360 / 11,000,000,000
set -euo pipefail
BALANCE_FILE="$HOME/.openclaw/skills/cost-monitor/balance.json"

case "${1:-}" in
  deepseek)
    python3 -c "
import json
with open('$BALANCE_FILE') as f: d = json.load(f)
d['deepseek']['balance_rmb'] = float('$2'.replace(',',''))
d['_last_processed'] = ''
with open('$BALANCE_FILE', 'w') as f: json.dump(d, f, indent=2, ensure_ascii=False)
print(f'DeepSeek balance set to ¥{float(\"$2\"):.2f}')
"
    ;;
  mimo)
    consumed="${2//,/}"  # strip commas
    total="${4//,/}"     # strip commas
    remaining=$((total - consumed))
    pct=$(python3 -c "print(f'{$remaining / $total * 100:.1f}')")
    python3 -c "
import json
with open('$BALANCE_FILE') as f: d = json.load(f)
d['mimo']['total_credits'] = $total
d['mimo']['consumed_credits'] = $consumed
d['_last_processed'] = ''
with open('$BALANCE_FILE', 'w') as f: json.dump(d, f, indent=2, ensure_ascii=False)
print(f'MIMO: consumed={$consumed} / {$total}, remaining={$remaining} ({$remaining*100/$total:.1f}%)')
"
    ;;
  *)
    echo "Usage: set-balance deepseek <rmb>"
    echo "       set-balance mimo <consumed> / <total>"
    echo ""
    echo "Example: set-balance mimo 3,933,069,360 / 11,000,000,000"
    exit 1
    ;;
esac
