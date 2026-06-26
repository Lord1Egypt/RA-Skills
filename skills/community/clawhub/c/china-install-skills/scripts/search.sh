#!/bin/bash
# ClawHub 搜索脚本（绕过 API 限流）
# 用法：./search.sh <搜索词> [数量]

set -e

QUERY="$1"
LIMIT="${2:-20}"

if [ -z "$QUERY" ]; then
  echo "❌ 用法：$0 <搜索词> [数量]"
  echo "示例：$0 weather 10"
  exit 1
fi

echo "🔍 正在搜索 ClawHub: ${QUERY}..."

# 编码查询词（空格转 + 号）
ENCODED_QUERY=$(echo "$QUERY" | sed 's/ /+/g')

# 使用 ClawHub 官方 API
API_URL="https://clawhub.com/api/v1/skills?q=${ENCODED_QUERY}"

# 获取 JSON 响应
RESPONSE=$(curl -sL "$API_URL" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")

# 解析 JSON 并提取技能信息
# 使用 awk/sed 替代 jq（更通用）
echo ""
echo "✅ 找到以下技能："
echo ""

# 提取技能信息（slug, displayName, summary, stars, downloads）
echo "$RESPONSE" | \
  sed 's/},{/}\n{/g' | \
  grep '"slug"' | \
  head -n "$LIMIT" | \
  while read -r line; do
    SLUG=$(echo "$line" | sed 's/.*"slug":"\([^"]*\)".*/\1/')
    NAME=$(echo "$line" | sed 's/.*"displayName":"\([^"]*\)".*/\1/')
    SUMMARY=$(echo "$line" | sed 's/.*"summary":"\([^"]*\)".*/\1/' | cut -c1-60)
    STARS=$(echo "$line" | sed 's/.*"stars":\([0-9]*\).*/\1/')
    DOWNLOADS=$(echo "$line" | sed 's/.*"downloads":\([0-9]*\).*/\1/')
    
    echo "📦 ${NAME} (${SLUG})"
    echo "   📝 ${SUMMARY}..."
    echo "   ⭐ ${STARS} · 📥 ${DOWNLOADS} 下载"
    echo ""
  done

echo "💡 提示：使用 './download.sh <技能名>' 下载，或 './install.sh <技能名> <目标目录>' 安装"
