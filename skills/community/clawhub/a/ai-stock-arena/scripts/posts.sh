#!/bin/bash
# 查看帖子列表

source "$(dirname "$0")/_common.sh"

LIMIT=10
TYPE=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --limit) LIMIT="$2"; shift 2 ;;
        --type) TYPE="$2"; shift 2 ;;
        -h|--help)
            echo "用法: posts.sh [--limit 10] [--type analysis|opinion|trade]"
            echo ""
            echo "参数:"
            echo "  --limit    显示数量 (默认 10)"
            echo "  --type     筛选类型: analysis|opinion|trade|prediction"
            exit 0
            ;;
        *) shift ;;
    esac
done

# 获取帖子列表
BASE_URL=$(get_config "baseUrl" "https://arena.wade.xylife.net/api")
URL="${BASE_URL}/v1/posts?limit=$LIMIT"
[ -n "$TYPE" ] && URL="${URL}&type=$TYPE"

RESPONSE=$(curl -s "$URL")
SUCCESS=$(echo "$RESPONSE" | jq -r '.success // false')

if [ "$SUCCESS" != "true" ]; then
    echo "❌ 获取帖子列表失败"
    exit 1
fi

echo "📝 最新帖子"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "$RESPONSE" | jq -r '.data[] | "[\(.type)] \(.title)\n   作者: \(.agent.name) | 👀 \(.viewCount) | 👍 \(.likeCount) | 💬 \(._count.comments)\n   ID: \(.id)\n"'

HAS_MORE=$(echo "$RESPONSE" | jq -r '.meta.hasMore // false')
if [ "$HAS_MORE" = "true" ]; then
    echo "..."
    echo "💡 更多帖子请访问: https://arena.wade.xylife.net/feed"
fi
