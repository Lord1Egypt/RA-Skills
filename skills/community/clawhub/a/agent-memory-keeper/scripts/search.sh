#!/bin/bash
# 记忆搜索 — 搜索所有memory文件
# 用法: bash search.sh "关键词"

query="$*"
if [ -z "$query" ]; then
    echo "用法: search.sh 关键词"
    echo "示例: search.sh 定价策略"
    exit 1
fi

echo "🔍 搜索记忆: $query"
echo "================================"

found=0

# 搜索 MEMORY.md
if [ -f "MEMORY.md" ]; then
    matches=$(grep -in "$query" MEMORY.md)
    if [ -n "$matches" ]; then
        echo ""
        echo "📌 MEMORY.md 中找到:"
        echo "$matches" | head -10
        found=$((found+1))
    fi
fi

# 搜索 memory/ 目录
if [ -d "memory" ]; then
    files=$(grep -ril "$query" memory/ 2>/dev/null)
    if [ -n "$files" ]; then
        echo ""
        echo "📂 memory/ 中找到:"
        echo "$files" | while read f; do
            echo "   📄 $f"
        done
        found=$((found+1))
    fi
fi

# 搜索 knowledge/ 目录
if [ -d "memory/knowledge" ]; then
    files=$(grep -ril "$query" memory/knowledge/ 2>/dev/null)
    if [ -n "$files" ]; then
        echo ""
        echo "🧠 knowledge/ 中找到:"
        echo "$files" | while read f; do
            echo "   📄 $f"
        done
        found=$((found+1))
    fi
fi

if [ $found -eq 0 ]; then
    echo ""
    echo "😅 没找到关于「$query」的记忆"
    echo "   建议: 1. 换个关键词试试 2. 或者现在把相关信息记下来"
else
    echo ""
    echo "✅ 找到 $found 个来源"
fi
