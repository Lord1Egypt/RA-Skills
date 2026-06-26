#!/bin/bash
# AI Daily - 查看日报
# Usage: ./view.sh <date|today>

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$BASE_DIR/output"

if [ -z "$1" ]; then
    echo "Usage: $0 <date|today>"
    echo "  today     - 查看今日日报"
    echo "  YYYY-MM-DD - 查看指定日期日报"
    exit 1
fi

if [ "$1" = "today" ]; then
    DATE=$(date +%Y-%m-%d)
else
    DATE="$1"
fi

FILENAME="AI-Daily-${DATE}.md"
FILEPATH="$OUTPUT_DIR/$FILENAME"

if [ ! -f "$FILEPATH" ]; then
    echo "❌ 未找到日报文件：$FILEPATH"
    echo ""
    echo "可用文件:"
    ls -la "$OUTPUT_DIR"/*.md 2>/dev/null || echo "  (无)"
    exit 1
fi

echo "📰 AI 日报 | $DATE"
echo "================================"
echo ""
cat "$FILEPATH"
