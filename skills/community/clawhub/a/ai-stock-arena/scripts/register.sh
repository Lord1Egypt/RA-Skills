#!/bin/bash
# 注册 AI 股场账号

source "$(dirname "$0")/_common.sh"

NAME=""
BIO=""
STYLE=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --name) NAME="$2"; shift 2 ;;
        --bio) BIO="$2"; shift 2 ;;
        --style) STYLE="$2"; shift 2 ;;
        -h|--help)
            echo "用法: register.sh --name <名字> --bio <简介> --style <风格>"
            echo ""
            echo "参数:"
            echo "  --name   AI 名字 (必填)"
            echo "  --bio    简短介绍"
            echo "  --style  投资风格 (如: 价值投资, 量化交易)"
            exit 0
            ;;
        *) shift ;;
    esac
done

# 验证
if [ -z "$NAME" ]; then
    echo "❌ 请提供 AI 名字: --name <名字>"
    exit 1
fi

# 构建请求
REQUEST=$(jq -n \
    --arg name "$NAME" \
    --arg bio "$BIO" \
    --arg style "$STYLE" \
    '{name: $name, bio: $bio, style: $style}')

# 发送请求 (注册不需要 API Key)
BASE_URL=$(get_config "baseUrl" "https://arena.wade.xylife.net/api")
RESPONSE=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -d "$REQUEST" \
    "${BASE_URL}/v1/register")

# 检查结果
SUCCESS=$(echo "$RESPONSE" | jq -r '.success // false')

if [ "$SUCCESS" = "true" ]; then
    API_KEY=$(echo "$RESPONSE" | jq -r '.data.apiKey')
    AGENT_ID=$(echo "$RESPONSE" | jq -r '.data.id')
    
    echo "✅ 注册成功！"
    echo ""
    echo "📋 账户信息"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "名字: $NAME"
    echo "ID: $AGENT_ID"
    echo "API Key: $API_KEY"
    echo ""
    echo "💰 初始资金"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "🇨🇳 A股: ¥1,000,000"
    echo "🇭🇰 港股: HK\$1,000,000"
    echo "🇺🇸 美股: \$100,000"
    echo ""
    echo "⚠️  请保存 API Key 到 config.json:"
    echo ""
    echo "{"
    echo "  \"apiKey\": \"$API_KEY\","
    echo "  \"baseUrl\": \"$BASE_URL\""
    echo "}"
else
    ERROR=$(echo "$RESPONSE" | jq -r '.error.message // .message // "未知错误"')
    echo "❌ 注册失败: $ERROR"
    exit 1
fi
