#!/bin/bash
# 博查搜索脚本
# 用法: ./search.sh "搜索关键词" [结果数量]

QUERY="${1:-}"
COUNT="${2:-5}"

if [[ -z "$QUERY" ]]; then
    echo "Usage: ./search.sh \"搜索关键词\" [结果数量]"
    exit 1
fi

# 读取 API Key
CONFIG_FILE="$HOME/.openclaw/skills-config/bocha-search.json"

if [[ -f "$CONFIG_FILE" ]]; then
    API_KEY=$(jq -r '.apiKey' "$CONFIG_FILE" 2>/dev/null)
else
    # 尝试环境变量
    API_KEY="${BOCHA_API_KEY:-}"
fi

if [[ -z "$API_KEY" ]] || [[ "$API_KEY" == "null" ]]; then
    echo "❌ 未配置 API Key"
    echo ""
    echo "请先配置:"
    echo "  1. 访问 https://open.bocha.cn 获取 API Key"
    echo "  2. 运行: ~/.openclaw/skills/bocha-search/scripts/setup.sh <你的APIKey>"
    exit 1
fi

# 执行搜索
RESPONSE=$(curl -s "https://api.bocha.cn/v1/web-search" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
        \"query\": \"$QUERY\",
        \"summary\": true,
        \"freshness\": \"noLimit\",
        \"count\": $COUNT
    }")

# 检查错误
if echo "$RESPONSE" | jq -e '.code' >/dev/null 2>&1; then
    ERROR_CODE=$(echo "$RESPONSE" | jq -r '.code')
    ERROR_MSG=$(echo "$RESPONSE" | jq -r '.message // "未知错误"')
    echo "❌ 错误 ($ERROR_CODE): $ERROR_MSG"
    exit 1
fi

# 格式化输出
echo "$RESPONSE" | jq -r '
.data.webPages.value[] |
"📌 " + .name + "\n🔗 " + .url + "\n📝 " + (.summary // .snippet) + "\n"
'
