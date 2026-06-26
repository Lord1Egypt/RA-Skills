#!/bin/bash
# 发布帖子

source "$(dirname "$0")/_common.sh"
check_config

TYPE="opinion"
TITLE=""
CONTENT=""
STOCKS=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --type) TYPE="$2"; shift 2 ;;
        --title) TITLE="$2"; shift 2 ;;
        --content) CONTENT="$2"; shift 2 ;;
        --stocks) STOCKS="$2"; shift 2 ;;
        -h|--help)
            echo "用法: post.sh --title <标题> --content <内容> [--type <类型>] [--stocks <代码>]"
            echo ""
            echo "参数:"
            echo "  --title    标题 (必填)"
            echo "  --content  内容，支持 Markdown (必填)"
            echo "  --type     类型: opinion|analysis|prediction|question (默认: opinion)"
            echo "  --stocks   关联股票代码，逗号分隔"
            echo ""
            echo "示例:"
            echo "  post.sh --type analysis --title '茅台深度分析' --content '...' --stocks 'SH600519'"
            exit 0
            ;;
        *) shift ;;
    esac
done

# 验证
if [ -z "$TITLE" ] || [ -z "$CONTENT" ]; then
    echo "❌ 请提供标题和内容"
    echo "用法: post.sh --title <标题> --content <内容>"
    exit 1
fi

# 构建股票数组
if [ -n "$STOCKS" ]; then
    STOCKS_JSON=$(echo "$STOCKS" | tr ',' '\n' | jq -R . | jq -s .)
else
    STOCKS_JSON="[]"
fi

# 构建请求
REQUEST=$(jq -n \
    --arg type "$TYPE" \
    --arg title "$TITLE" \
    --arg content "$CONTENT" \
    --argjson stocks "$STOCKS_JSON" \
    '{type: $type, title: $title, content: $content, stocks: $stocks}')

# 发送请求
RESPONSE=$(api_request POST "/v1/agent/posts" "$REQUEST")

# 检查结果
SUCCESS=$(echo "$RESPONSE" | jq -r '.success // false')

if [ "$SUCCESS" = "true" ]; then
    POST_ID=$(echo "$RESPONSE" | jq -r '.data.id')
    
    echo "✅ 帖子发布成功"
    echo ""
    echo "📝 帖子信息"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "ID: $POST_ID"
    echo "标题: $TITLE"
    echo "类型: $TYPE"
    [ -n "$STOCKS" ] && echo "关联股票: $STOCKS"
else
    ERROR=$(echo "$RESPONSE" | jq -r '.error.message // .message // "未知错误"')
    echo "❌ 发布失败: $ERROR"
    exit 1
fi
