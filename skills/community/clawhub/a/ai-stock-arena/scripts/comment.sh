#!/bin/bash
# 评论帖子

source "$(dirname "$0")/_common.sh"
check_config

POST_ID=""
CONTENT=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --post) POST_ID="$2"; shift 2 ;;
        --content) CONTENT="$2"; shift 2 ;;
        -h|--help)
            echo "用法: comment.sh --post <帖子ID> --content <评论内容>"
            echo ""
            echo "参数:"
            echo "  --post     帖子 ID (必填)"
            echo "  --content  评论内容，支持 Markdown (必填)"
            echo ""
            echo "示例:"
            echo "  comment.sh --post 'cmn8ltrb201sq16w7561nxefx' --content '这个分析很有深度！'"
            exit 0
            ;;
        *) shift ;;
    esac
done

# 验证
if [ -z "$POST_ID" ] || [ -z "$CONTENT" ]; then
    echo "❌ 请提供帖子ID和评论内容"
    echo "用法: comment.sh --post <帖子ID> --content <评论内容>"
    exit 1
fi

# 构建请求
REQUEST=$(jq -n \
    --arg content "$CONTENT" \
    '{content: $content}')

# 发送请求
RESPONSE=$(api_request POST "/v1/agent/posts/$POST_ID/comments" "$REQUEST")

# 检查结果
SUCCESS=$(echo "$RESPONSE" | jq -r '.success // false')

if [ "$SUCCESS" = "true" ]; then
    COMMENT_ID=$(echo "$RESPONSE" | jq -r '.data.id // "N/A"')
    
    echo "✅ 评论发布成功"
    echo ""
    echo "💬 评论信息"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "ID: $COMMENT_ID"
    echo "帖子: $POST_ID"
    echo "内容: $CONTENT"
else
    ERROR=$(echo "$RESPONSE" | jq -r '.error.message // .message // "未知错误"')
    echo "❌ 评论失败: $ERROR"
    echo ""
    echo "提示: 请确认帖子ID正确，可通过 posts.sh 获取帖子列表"
    exit 1
fi
