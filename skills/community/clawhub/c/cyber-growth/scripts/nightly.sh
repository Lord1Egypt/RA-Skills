#!/bin/bash
# Cyber Growth - 每日结算
# 每天 24:00 自动运行，批量处理当日事件
# 用法: nightly.sh [--date YYYY-MM-DD]

set -uo pipefail

GROW_SH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/grow.sh"
LOG_DIR="${CYBER_GROWTH_LOG:-$HOME/.openclaw/memory/cyber-growth-events}"

# 日期（默认昨天，因为通常在凌晨运行）
DATE="${1:-$(date -v-1d +"%Y-%m-%d" 2>/dev/null || date -d "yesterday" +"%Y-%m-%d")}"
LOG_FILE="$LOG_DIR/$DATE.jsonl"

if [ ! -f "$LOG_FILE" ]; then
    echo "No events for $DATE" >&2
    exit 0
fi

# 统计
total_xp=0
count=0
domains=""
while IFS= read -r line; do
    xp=$(echo "$line" | python3 -c "import json,sys; print(json.load(sys.stdin).get('xp',0))" 2>/dev/null || echo 0)
    domain=$(echo "$line" | python3 -c "import json,sys; print(json.load(sys.stdin).get('domain',''))" 2>/dev/null || echo "")
    desc=$(echo "$line" | python3 -c "import json,sys; print(json.load(sys.stdin).get('desc',''))" 2>/dev/null || echo "")
    type=$(echo "$line" | python3 -c "import json,sys; print(json.load(sys.stdin).get('type','mission-cleared'))" 2>/dev/null || echo "mission-cleared")

    # 调用 grow.sh 记录
    bash "$GROW_SH" record "$desc" --domain "$domain" --xp "$xp" --type "$type" 2>&1 | grep -E "(TRANSMISSION|UPGRADED|BREAKTHROUGH)" || true

    total_xp=$((total_xp + xp))
    count=$((count + 1))
done < "$LOG_FILE"

# 归档日志
ARCHIVE_DIR="$LOG_DIR/archive"
mkdir -p "$ARCHIVE_DIR"
mv "$LOG_FILE" "$ARCHIVE_DIR/"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 DAILY SETTLEMENT: $DATE"
echo "   Transmissions: $count"
echo "   Total XP: +$total_xp"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
