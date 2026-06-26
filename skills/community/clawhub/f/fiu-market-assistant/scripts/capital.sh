#!/bin/bash
# FIU MCP - 资金流向查询
# 获取个股资金流入流出及大单、中单、小单分布

set -e

SYMBOL="${1:-}"

if [ -z "$SYMBOL" ]; then
    echo "用法：capital.sh <股票代码>"
    echo "示例：capital.sh 00700.HK"
    exit 1
fi

TOKEN="${FIU_MCP_TOKEN:-}"
if [ -z "$TOKEN" ]; then
    echo "错误：请设置 FIU_MCP_TOKEN 环境变量"
    exit 1
fi

RESPONSE=$(curl -s -X POST "https://ai.szfiu.com/stock_hk_sdk/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d "{
        \"jsonrpc\": \"2.0\",
        \"id\": 1,
        \"method\": \"tools/call\",
        \"params\": {
            \"name\": \"post_v3_capital_flow\",
            \"arguments\": {
                \"symbol\": \"$SYMBOL\"
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
