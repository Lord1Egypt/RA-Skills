#!/bin/bash
# 检查文档是否已存在（根据标题去重）

set -e

ARTICLE_URL="$1"
SPACE_ID="${2:-7527734827164909572}"
PARENT_NODE="${3:-NqZvwBqMTiTEtkkMsRoc76rznce}"

if [ -z "$ARTICLE_URL" ]; then
  echo "Usage: $0 <article_url> [space_id] [parent_node]"
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COOKIE_FILE="$SCRIPT_DIR/../config/twitter-cookies.txt"

# 1. 提取文章标题（只提取标题，不提取完整内容）
echo "正在提取文章标题..." >&2
TITLE=$(node "$SCRIPT_DIR/html-to-markdown-final.js" "$ARTICLE_URL" "$(cat "$COOKIE_FILE")" 2>/dev/null | jq -r '.title')

if [ -z "$TITLE" ] || [ "$TITLE" = "null" ]; then
  echo "❌ 无法提取文章标题" >&2
  exit 1
fi

echo "文章标题：$TITLE" >&2

# 2. 在知识库中搜索同名文档
echo "正在检查是否已存在..." >&2
EXISTING_NODE=$(feishu_wiki nodes --space-id "$SPACE_ID" --parent-node "$PARENT_NODE" 2>/dev/null | \
  jq -r --arg title "$TITLE" '.nodes[]? | select(.title == $title) | .node_token' | head -1)

# 3. 返回结果
if [ -n "$EXISTING_NODE" ]; then
  echo "EXISTS:$EXISTING_NODE:$TITLE"
  exit 0
else
  echo "NOT_EXISTS:$TITLE"
  exit 0
fi
