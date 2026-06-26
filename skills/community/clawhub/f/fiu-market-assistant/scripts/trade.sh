#!/bin/bash
# FIU MCP - 交易下单
# 证券/期货下单（默认模拟环境）
# Uses jq for safe JSON construction to prevent injection

set -e

ACTION="${1:-}"  # buy/sell
SYMBOL="${2:-}"
QTY="${3:-}"
PRICE="${4:-}"
ENV="${5:-SIMULATE}"  # SIMULATE/REAL

if [ -z "$ACTION" ] || [ -z "$SYMBOL" ] || [ -z "$QTY" ]; then
    echo "用法：trade.sh <buy|sell> <股票代码> <数量> [价格] [环境 SIMULATE|REAL]"
    echo "示例：trade.sh buy 00700.HK 100 350.5 SIMULATE"
    exit 1
fi

# Validate inputs to prevent injection
if [[ ! "$ACTION" =~ ^(buy|sell)$ ]]; then
    echo "错误: action 必须是 buy 或 sell"
    exit 1
fi

if [[ ! "$QTY" =~ ^[0-9]+$ ]]; then
    echo "错误: qty 必须是数字"
    exit 1
fi

if [ -n "$PRICE" ] && [[ ! "$PRICE" =~ ^[0-9]+\.?[0-9]*$ ]]; then
    echo "错误: price 必须是数字"
    exit 1
fi

if [[ ! "$ENV" =~ ^(SIMULATE|REAL)$ ]]; then
    echo "错误: environment 必须是 SIMULATE 或 REAL"
    exit 1
fi

# 实盘交易需要二次确认
if [ "$ENV" = "REAL" ]; then
    echo "⚠️  警告：您正在使用 REAL 实盘环境！"
    read -p "确认继续？(yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo "已取消"
        exit 0
    fi
fi

TOKEN="${FIU_MCP_TOKEN:-}"
if [ -z "$TOKEN" ]; then
    echo "错误：请设置 FIU_MCP_TOKEN 环境变量"
    exit 1
fi

# Build order type
ORDER_TYPE="NORMAL"
if [ -z "$PRICE" ]; then
    ORDER_TYPE="MARKET"
    PRICE="0"
fi

# Use jq to safely construct JSON payload
JSON_payload=$(jq -n \
    --arg tool "place_order" \
    --arg symbol "$SYMBOL" \
    --arg action "$ACTION" \
    --argjson qty "$QTY" \
    --argjson price "$PRICE" \
    --arg order_type "$ORDER_TYPE" \
    --arg environment "$ENV" \
    '{
        tool: $tool,
        params: {
            symbol: $symbol,
            action: $action,
            qty: $qty,
            price: $price,
            order_type: $order_type,
            environment: $environment
        }
    }')

curl -s -X POST "https://ai.szfiu.com/stock_hk_sdk/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "$JSON_payload" | jq .