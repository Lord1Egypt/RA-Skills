#!/bin/bash
# ClawHub 技能搜索脚本
# 用法: ./search.sh <query> [--limit N]

set -e

QUERY="$1"
LIMIT="${3:-10}"

if [ -z "$QUERY" ]; then
  echo "❌ 错误：缺少搜索关键词"
  echo ""
  echo "用法: $0 <query> [--limit N]"
  echo ""
  echo "示例："
  echo "  $0 feishu"
  echo "  $0 pdf --limit 20"
  exit 1
fi

echo "🔍 搜索技能: $QUERY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ "$2" = "--limit" ] && [ -n "$LIMIT" ]; then
  clawhub search "$QUERY" --limit "$LIMIT"
else
  clawhub search "$QUERY" --limit 10
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 搜索完成"
echo ""
echo "💡 提示：使用 inspect.sh 查看技能详细信息"
echo "   bash /root/.openclaw/workspace/skills/clawhub-manager/scripts/inspect.sh <skill-slug>"
