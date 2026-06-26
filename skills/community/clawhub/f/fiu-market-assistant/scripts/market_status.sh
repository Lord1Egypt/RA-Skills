#!/bin/bash
# FIU MCP - 市场状态查询
# 查询各市场开盘/休市状态

set -e

MARKET="${1:-ALL}"  # ALL/HK/US/CN

TOKEN="${FIU_MCP_TOKEN:-}"
if [ -z "$TOKEN" ]; then
    echo "错误：请设置 FIU_MCP_TOKEN 环境变量"
    exit 1
fi

curl -s -X POST "https://ai.szfiu.com/toolkit/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
        \"tool\": \"market_status\",
        \"params\": {
            \"market\": \"$MARKET\"
        }
    }" | jq .
