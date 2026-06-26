#!/bin/bash
# FIU MCP - 市场快照查询
# 获取股票最新报价、涨跌幅、成交量等

set -e

SYMBOL="${1:-}"
MARKET="${2:-HK}"
TIME_MODE="${3:-0}"  # 0=实时，1=延时

if [ -z "$SYMBOL" ]; then
    echo "用法：quote.sh <股票代码> [市场 HK|US|CN] [时间模式 0|1]"
    echo "示例：quote.sh 00700.HK HK 0"
    exit 1
fi

# 根据市场选择端点和方法名
case "$MARKET" in
    HK)
        ENDPOINT="https://ai.szfiu.com/stock_hk_sdk/"
        METHOD="post_v3_stock_quote"
        ;;
    US)
        ENDPOINT="https://ai.szfiu.com/stock_us_sdk/"
        METHOD="post_v1_stock_quote"
        ;;
    CN)
        ENDPOINT="https://ai.szfiu.com/stock_cn_sdk/"
        METHOD="post_v1_stock_quote"
        ;;
    *)
        echo "错误：市场参数必须是 HK、US 或 CN"
        exit 1
        ;;
esac

# 获取 Token
TOKEN="${FIU_MCP_TOKEN:-}"
if [ -z "$TOKEN" ]; then
    echo "错误：请设置 FIU_MCP_TOKEN 环境变量"
    exit 1
fi

# 调用 API (JSON-RPC 2.0 格式)
# 美股和 A 股需要 sessionId 参数，港股不需要
case "$MARKET" in
    US|CN)
        RESPONSE=$(curl -s -X POST "$ENDPOINT" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -H "Accept: application/json, text/event-stream" \
            -d "{
                \"jsonrpc\": \"2.0\",
                \"id\": 1,
                \"method\": \"tools/call\",
                \"params\": {
                    \"name\": \"$METHOD\",
                    \"arguments\": {
                        \"fields\": [\"snapshot\"],
                        \"symbols\": [\"$SYMBOL\"],
                        \"timeMode\": $TIME_MODE,
                        \"sessionId\": \"1\"
                    }
                }
            }")
        ;;
    HK)
        RESPONSE=$(curl -s -X POST "$ENDPOINT" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -H "Accept: application/json, text/event-stream" \
            -d "{
                \"jsonrpc\": \"2.0\",
                \"id\": 1,
                \"method\": \"tools/call\",
                \"params\": {
                    \"name\": \"$METHOD\",
                    \"arguments\": {
                        \"fields\": [\"snapshot\"],
                        \"symbols\": [\"$SYMBOL\"],
                        \"timeMode\": $TIME_MODE
                    }
                }
            }")
        ;;
esac

# 解析 SSE 响应
DATA=$(echo "$RESPONSE" | grep "^data:" | sed 's/^data: //')
TEXT=$(echo "$DATA" | jq -r '.result.content[0].text' 2>/dev/null)

if [ -n "$TEXT" ]; then
    echo "$TEXT" | jq .
else
    echo "$DATA" | jq .
fi
