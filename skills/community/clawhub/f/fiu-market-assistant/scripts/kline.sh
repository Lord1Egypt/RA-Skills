#!/bin/bash
# FIU MCP - K 线数据查询
# 获取日 K、周 K、分钟 K 等历史和实时 K 线

set -e

SYMBOL="${1:-}"
TYPE="${2:-0}"      # 0=日 K, 1=周 K, 2=月 K, 3=季 K, 4=年 K, 5=1 分，6=5 分，7=15 分，8=30 分，9=60 分
CANDLE_MODE="${3:-0}"  # 0=不复权，1=前复权，2=后复权
COUNT="${4:-100}"
TIME_MODE="${5:-0}"    # 0=实时，1=延时

if [ -z "$SYMBOL" ]; then
    echo "用法：kline.sh <股票代码> [K 线类型] [复权模式] [数量] [时间模式]"
    echo "K 线类型：0=日 K, 1=周 K, 2=月 K, 3=季 K, 4=年 K, 5=1 分，6=5 分，7=15 分，8=30 分，9=60 分"
    echo "复权模式：0=不复权，1=前复权，2=后复权"
    echo "示例：kline.sh 00700.HK 0 0 100 0"
    exit 1
fi

# 获取当前日期
DATE=$(date +%Y-%m-%d)
if [ "$TYPE" -ge 5 ]; then
    DATE=$(date +"%Y-%m-%d %H:%M:%S")
fi

TOKEN="${FIU_MCP_TOKEN:-}"
if [ -z "$TOKEN" ]; then
    echo "错误：请设置 FIU_MCP_TOKEN 环境变量"
    exit 1
fi

# 计算页码
PAGE_SIZE=100
PAGE_NUM=$(( (COUNT + PAGE_SIZE - 1) / PAGE_SIZE ))

RESPONSE=$(curl -s -X POST "https://ai.szfiu.com/stock_hk_sdk/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d "{
        \"jsonrpc\": \"2.0\",
        \"id\": 1,
        \"method\": \"tools/call\",
        \"params\": {
            \"name\": \"post_v3_chart_kline_list\",
            \"arguments\": {
                \"candleMode\": $CANDLE_MODE,
                \"timeMode\": $TIME_MODE,
                \"type\": $TYPE,
                \"date\": \"$DATE\",
                \"symbol\": \"$SYMBOL\",
                \"pageNum\": 1,
                \"pageSize\": $COUNT
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
