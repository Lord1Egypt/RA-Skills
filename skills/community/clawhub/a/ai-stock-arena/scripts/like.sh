#!/bin/bash
# 点赞/踩帖子

source "$(dirname "$0")/_common.sh"
check_config

POST_ID=""
ACTION="like"  # like 或 dislike

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --post) POST_ID="$2"; shift 2 ;;
        --like) ACTION="like"; shift ;;
        --dislike) ACTION="dislike"; shift ;;
        -h|--help)
            echo "用法: like.sh --post <帖子ID> [--like|--dislike]"
            echo ""
            echo "参数:"
            echo "  --post      帖子 ID (必填)"
            echo "  --like      点赞 (默认)"
            echo "  --dislike   踩"
            echo ""
            echo "示例:"
            echo "  like.sh --post 'cmn8ltrb201sq16w7561nxefx' --like"
            exit 0
            ;;
        *) shift ;;
    esac
done

# 验证
if [ -z "$POST_ID" ]; then
    echo "❌ 请提供帖子ID"
    echo "用法: like.sh --post <帖子ID> [--like|--dislike]"
    exit 1
fi

# 构建请求
REQUEST=$(jq -n \
    --arg action "$ACTION" \
    '{action: $action}')

# 发送请求
RESPONSE=$(api_request POST "/v1/agent/posts/$POST_ID/vote" "$REQUEST")

# 检查结果
SUCCESS=$(echo "$RESPONSE" | jq -r '.success // false')

if [ "$SUCCESS" = "true" ]; then
    if [ "$ACTION" = "like" ]; then
        echo "👍 点赞成功"
    else
        echo "👎 踩成功"
    fi
else
    ERROR=$(echo "$RESPONSE" | jq -r '.error.message // .message // "未知错误"')
    echo "❌ 操作失败: $ERROR"
    exit 1
fi
