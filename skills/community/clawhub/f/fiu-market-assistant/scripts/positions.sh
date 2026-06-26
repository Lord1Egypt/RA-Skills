#!/bin/bash
# FIU MCP - 持仓查询
# 查询账户持仓

set -e

ENV="${1:-SIMULATE}"

TOKEN="${FIU_MCP_TOKEN:-}"
if [ -z "$TOKEN" ]; then
    echo "错误：请设置 FIU_MCP_TOKEN 环境变量"
    exit 1
fi

curl -s -X POST "https://ai.szfiu.com/stock_hk_sdk/" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
        \"tool\": \"positions\",
        \"params\": {
            \"environment\": \"$ENV\"
        }
    }" | jq .
