#!/bin/bash
# FIU MCP Router - 通用 MCP 接口调用工具
# 根据参数调用任意 FIU MCP Server API

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 用法说明
usage() {
    cat << EOF
FIU MCP Router - 通用 MCP 接口调用工具

用法:
  $0 <市场> <tool_name> [参数...]
  $0 --list-tools <市场>       # 列出该市场所有可用工具

市场选项:
  hk_f10   - 港股 F10 数据
  us_f10   - 美股 F10 数据
  cn_f10   - A 股 F10 数据
  hk_sdk   - 港股 SDK 数据
  us_sdk   - 美股 SDK 数据
  cn_sdk   - A 股 SDK 数据
  toolkit  - 代码检索服务

参数格式: key=value
  例如: symbol=00700.HK fields=snapshot,quote

示例:
  $0 hk_sdk post_v3_stock_quote fields=snapshot
  $0 hk_sdk post_v3_chart_kline_list symbol=00700.HK type=0
  $0 hk_f10 financials symbol=00700.HK
  $0 toolkit search keyword=腾讯
  $0 --list-tools cn_sdk
EOF
    exit 1
}

# MCP Server 端点映射
declare -A ENDPOINTS=(
    ["hk_f10"]="https://ai.szfiu.com/stock_hk_f10/"
    ["us_f10"]="https://ai.szfiu.com/stock_us_f10/"
    ["cn_f10"]="https://ai.szfiu.com/stock_cn_f10/"
    ["hk_sdk"]="https://ai.szfiu.com/stock_hk_sdk/"
    ["us_sdk"]="https://ai.szfiu.com/stock_us_sdk/"
    ["cn_sdk"]="https://ai.szfiu.com/stock_cn_sdk/"
    ["toolkit"]="https://ai.szfiu.com/toolkit/"
)

# 检查参数
if [ $# -lt 2 ]; then
    usage
fi

MARKET="$1"
TOOL_NAME="$2"

# 支持 --list-tools 列出所有可用工具
if [ "$MARKET" == "--list-tools" ] || [ "$MARKET" == "-l" ]; then
    MARKET="$TOOL_NAME"
    ENDPOINT="${ENDPOINTS[$MARKET]:-}"
    if [ -z "$ENDPOINT" ]; then
        echo "错误: 未知市场 '$MARKET'"
        usage
    fi
    TOKEN="${FIU_MCP_TOKEN:-}"
    if [ "$MARKET" != "toolkit" ] && [ -z "$TOKEN" ]; then
        echo "错误: 请设置 FIU_MCP_TOKEN 环境变量"
        exit 1
    fi
    RESPONSE=$(curl -s -X POST "$ENDPOINT" \
        $([ "$MARKET" != "toolkit" ] && echo "-H \"Authorization: Bearer $TOKEN\"") \
        -H "Content-Type: application/json" \
        -H "Accept: application/json, text/event-stream" \
        -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}')
    DATA=$(echo "$RESPONSE" | grep "^data:" | sed 's/^data: //')
    echo "$DATA" | jq '.result.tools[] | {name: .name, description: .description}' 2>/dev/null || echo "$DATA"
    exit 0
fi

shift 2

# 解析参数
ARGS_JSON="{}"
while [ $# -gt 0 ]; do
    KEY=$(echo "$1" | cut -d= -f1)
    VALUE=$(echo "$1" | cut -d= -f2-)
    # 尝试解析 JSON 数组格式 [a,b,c]
    if [[ "$VALUE" == \[*\] ]]; then
        ARGS_JSON=$(echo "$ARGS_JSON" | jq --arg k "$KEY" --argjson v "$VALUE" '. + {($k): $v}')
    else
        ARGS_JSON=$(echo "$ARGS_JSON" | jq --arg k "$KEY" --arg v "$VALUE" '. + {($k): $v}')
    fi
    shift
done

# 验证市场
if [ -z "${ENDPOINTS[$MARKET]}" ]; then
    echo -e "${RED}错误: 未知市场 '$MARKET'${NC}"
    usage
fi

ENDPOINT="${ENDPOINTS[$MARKET]}"

# 获取 Token (toolkit 不需要认证)
TOKEN="${FIU_MCP_TOKEN:-}"
if [ "$MARKET" != "toolkit" ] && [ -z "$TOKEN" ]; then
    echo -e "${RED}错误: 请设置 FIU_MCP_TOKEN 环境变量${NC}"
    exit 1
fi

# 构建请求
if [ "$MARKET" == "toolkit" ]; then
    # toolkit 不需要 Authorization header
    REQUEST_JSON=$(jq -n \
        --jsonrpc "2.0" \
        --id 1 \
        --method "tools/call" \
        --name "$TOOL_NAME" \
        --arguments "$ARGS_JSON" \
        '{
            "jsonrpc": .jsonrpc,
            "id": .id,
            "method": .method,
            "params": {
                "name": .name,
                "arguments": .arguments
            }
        }')
else
    REQUEST_JSON=$(jq -n \
        --jsonrpc "2.0" \
        --id 1 \
        --method "tools/call" \
        --name "$TOOL_NAME" \
        --arguments "$ARGS_JSON" \
        '{
            "jsonrpc": .jsonrpc,
            "id": .id,
            "method": .method,
            "params": {
                "name": .name,
                "arguments": .arguments
            }
        }')
fi

# 调用 API
if [ "$MARKET" == "toolkit" ]; then
    RESPONSE=$(curl -s -X POST "$ENDPOINT" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json, text/event-stream" \
        -d "$REQUEST_JSON")
else
    RESPONSE=$(curl -s -X POST "$ENDPOINT" \
        -H "Authorization: Bearer $TOKEN" \
        -H "Content-Type: application/json" \
        -H "Accept: application/json, text/event-stream" \
        -d "$REQUEST_JSON")
fi

# 解析响应
if echo "$RESPONSE" | grep -q "^data:"; then
    # SSE 响应格式
    DATA=$(echo "$RESPONSE" | grep "^data:" | sed 's/^data: //')
    TEXT=$(echo "$DATA" | jq -r '.result.content[0].text' 2>/dev/null)

    if [ -n "$TEXT" ] && [ "$TEXT" != "null" ]; then
        echo "$TEXT" | jq . 2>/dev/null || echo "$TEXT"
    else
        echo "$DATA" | jq . 2>/dev/null || echo "$DATA"
    fi
else
    # 普通 JSON 响应
    echo "$RESPONSE" | jq .
fi