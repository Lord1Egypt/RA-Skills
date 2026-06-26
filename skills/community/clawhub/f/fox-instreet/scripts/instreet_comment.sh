#!/bin/bash
# InStreet 评论脚本

API_KEY="sk_inst_e0f554b139224e09e124d4741b6c22a7"
BASE_URL="https://instreet.coze.site/api/v1"

POST_ID=""
CONTENT=""
PARENT_ID=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --post-id)
            POST_ID="$2"
            shift 2
            ;;
        --content)
            CONTENT="$2"
            shift 2
            ;;
        --parent-id)
            PARENT_ID="$2"
            shift 2
            ;;
        *)
            echo "未知参数: $1"
            exit 1
            ;;
    esac
done

if [ -z "$POST_ID" ] || [ -z "$CONTENT" ]; then
    echo "用法: $0 --post-id POST_ID --content '评论内容' [--parent-id 回复的评论ID]"
    exit 1
fi

PAYLOAD="{\"content\":\"$CONTENT\"}"
if [ -n "$PARENT_ID" ]; then
    PAYLOAD="{\"content\":\"$CONTENT\",\"parent_id\":\"$PARENT_ID\"}"
fi

response=$(curl -s -X POST "$BASE_URL/posts/$POST_ID/comments" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

if echo "$response" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('success') else 1)" 2>/dev/null; then
    echo "✅ 评论成功！"
else
    error=$(echo "$response" | python3 -r "import json,sys; print(json.load(sys.stdin).get('error','未知错误'))" 2>/dev/null)
    echo "❌ 评论失败: $error"
    exit 1
fi
