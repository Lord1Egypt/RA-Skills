#!/bin/bash
# 一键安装脚本：搜索 + 下载 + 安装
# 用法：./quick-install.sh <搜索词> <目标目录>

set -e

QUERY="$1"
TARGET="$2"

if [ -z "$QUERY" ] || [ -z "$TARGET" ]; then
  echo "❌ 用法：$0 <搜索词> <目标目录>"
  echo "示例：$0 weather /Users/xubangbang/.openclaw/workspace/agents/MAIN/skills"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "⚡ 一键安装：${QUERY}"
echo "  目标：${TARGET}"
echo ""

# 步骤 1: 搜索
echo "🔍 步骤 1/3: 搜索技能..."
SEARCH_RESULT=$(curl -sL "https://wry-manatee-359.convex.site/api/v1/skills?q=$(echo $QUERY | sed 's/ /+/g')" | \
  sed 's/},{/}\n{/g' | \
  grep -i "$QUERY" | \
  head -1)

if [ -z "$SEARCH_RESULT" ]; then
  echo "❌ 未找到匹配的技能"
  exit 1
fi

# 提取技能名
SLUG=$(echo "$SEARCH_RESULT" | sed 's/.*"slug":"\([^"]*\)".*/\1/')
NAME=$(echo "$SEARCH_RESULT" | sed 's/.*"displayName":"\([^"]*\)".*/\1/')

echo "  → 找到最佳匹配：${NAME} (${SLUG})"
echo ""

# 步骤 2: 下载
echo "📥 步骤 2/3: 下载中..."
"${SCRIPT_DIR}/download.sh" "$SLUG"
echo ""

# 步骤 3: 安装
echo "📦 步骤 3/3: 安装中..."
"${SCRIPT_DIR}/install.sh" "$SLUG" "$TARGET" --force
echo ""

echo "✅ 完成！${SLUG} 已安装到 ${TARGET}"
