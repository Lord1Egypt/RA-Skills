#!/bin/bash
# search.sh - 搜索B站视频

KEYWORD="${1:-}"
LIMIT="${2:-10}"

if [ -z "$KEYWORD" ]; then
    echo "用法: ./search.sh <关键词> [结果数量]"
    echo "示例: ./search.sh 'Python教程' 20"
    exit 1
fi

echo "🔍 搜索B站视频: $KEYWORD (前 $LIMIT 个结果)"
echo ""

# 使用 yt-dlp 搜索
yt-dlp "ytsearch${LIMIT}:${KEYWORD} site:bilibili.com" \
    --print "%(title)s | %(uploader)s | %(view_count)s views | %(id)s | %(webpage_url)s" \
    --quiet 2>/dev/null || echo "搜索失败，请检查网络连接"
