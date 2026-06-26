#!/bin/bash
# FIU MCP - 证券代码检索
# 检索证券代码服务

set -e

KEYWORD="${1:-}"

if [ -z "$KEYWORD" ]; then
    echo "用法：search.sh <关键词>"
    echo "示例：search.sh 腾讯"
    echo "       search.sh AAPL"
    exit 1
fi

TOKEN="${FIU_MCP_TOKEN:-}"
if [ -z "$TOKEN" ]; then
    echo "错误：请设置 FIU_MCP_TOKEN 环境变量"
    exit 1
fi

# 使用港股码表查询
RESPONSE=$(curl -s -X POST "https://ai.szfiu.com/stock_hk_sdk/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d "{
        \"jsonrpc\": \"2.0\",
        \"id\": 1,
        \"method\": \"tools/call\",
        \"params\": {
            \"name\": \"post_v3_stock_list\",
            \"arguments\": {
                \"keyword\": \"$KEYWORD\",
                \"market\": \"MAIN\",
                \"type\": \"EQTY\",
                \"typeMode\": 1
            }
        }
    }")

DATA=$(echo "$RESPONSE" | grep "^data:" | sed 's/^data: //')
TEXT=$(echo "$DATA" | jq -r '.result.content[0].text' 2>/dev/null)

if [ -n "$TEXT" ]; then
    echo "$TEXT" | jq .
else
    echo "$DATA" | jq .
fi
