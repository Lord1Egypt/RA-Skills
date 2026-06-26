#!/bin/bash
# openclaw skills 搜索美化脚本
# 用法: skills search <关键词>

KEYWORD="$1"

if [ -z "$KEYWORD" ]; then
    echo "用法: skills search <关键词>"
    echo "示例: skills search daily-report-catchup"
    exit 1
fi

echo ""
echo "🔍 搜索: $KEYWORD"
echo "=========================================="
echo ""

openclaw skills search "$KEYWORD" 2>&1 | grep -v "^🦞" | grep -v "^$" | while read line; do
    if echo "$line" | grep -q "found [0-9]"; then
        echo "📦 $line"
    elif echo "$line" | grep -q "^  - "; then
        echo "$line" | sed 's/^  - /\n  /'
    else
        echo "$line"
    fi
done

echo ""
echo "=========================================="
echo "💡 提示: 使用 \"精确关键词\" 可获得更准确的结果"
echo "   示例: skills search \"daily report catchup\""
echo ""
