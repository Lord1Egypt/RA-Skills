#!/bin/bash
# fiu-market-assistant - Main dispatch script
# Handles: setup, test, discover, quote, kline, search, trade, positions, cash, orders, capflow

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Config
CONFIG_FILE="$HOME/.fiu-market/config"
MCP_FILE="$HOME/.mcp.json"

# Load token
load_token() {
    if [ -f "$CONFIG_FILE" ]; then
        source "$CONFIG_FILE"
    fi
    if [ -z "$FIU_MCP_TOKEN" ]; then
        echo -e "${RED}错误: 请先配置 FIU_MCP_TOKEN${NC}"
        echo "运行: /fiu-market-assistant setup <token>"
        exit 1
    fi
}

# Show status
cmd_status() {
    load_token
    echo "📊 FIU Market Assistant 状态"
    echo "============================"
    echo ""

    # Check token
    if [ -n "$FIU_MCP_TOKEN" ]; then
        MASKED="${FIU_MCP_TOKEN:0:15}..."
        echo "✅ Token: $MASKED"
    else
        echo "❌ Token: 未配置"
    fi

    echo ""
    echo "📡 MCP 服务:"
    echo "   - stockHkF10  (港股F10)"
    echo "   - stockUsF10  (美股F10)"
    echo "   - stockCnF10  (A股F10)"
    echo "   - stockHkSdk  (港股SDK)"
    echo "   - stockUsSdk  (美股SDK)"
    echo "   - stockCnSdk  (A股SDK)"
    echo "   - szfiuToolkit (代码检索)"

    echo ""
    echo "📝 可用命令:"
    echo "   setup <token>    - 快速配置"
    echo "   test             - 测试连接"
    echo "   discover <市场>  - 发现可用工具"
    echo "   quote <代码>     - 查询行情"
    echo "   kline <代码>     - 查询K线"
    echo "   search <关键词>  - 搜索股票"
    echo "   trade <操作> <代码> <数量> [价格] - 交易"
    echo "   positions        - 查询持仓"
    echo "   cash             - 查询资金"
    echo "   orders           - 查询订单"
    echo "   capflow <代码>   - 资金流向"
}

# Quick setup
cmd_setup() {
    TOKEN="$1"
    if [ -z "$TOKEN" ]; then
        echo "用法: setup <FIU_MCP_TOKEN>"
        echo "获取Token: https://ai.szfiu.com/auth/login"
        exit 1
    fi

    # Warn about ~/.mcp.json
    if [ -f "$MCP_FILE" ]; then
        echo -e "${YELLOW}⚠️  警告: ~/.mcp.json 已存在，将被覆盖!${NC}"
        echo "现有配置将备份为 ~/.mcp.json.bak"
        cp "$MCP_FILE" "$MCP_FILE.bak"
    fi

    # Save config with secure permissions
    mkdir -p "$HOME/.fiu-market"
    echo "export FIU_MCP_TOKEN=\"$TOKEN\"" > "$CONFIG_FILE"
    chmod 600 "$CONFIG_FILE"  # Secure: only owner can read

    # Create MCP config - warn users to merge if they have existing config
    cat > "$MCP_FILE" << MCPEOF
{
  "mcpServers": {
    "stockHkF10": {"transport":"streamable_http","url":"https://ai.szfiu.com/stock_hk_f10/","headers":{"Authorization":"Bearer $TOKEN"}},
    "stockUsF10": {"transport":"streamable_http","url":"https://ai.szfiu.com/stock_us_f10/","headers":{"Authorization":"Bearer $TOKEN"}},
    "stockCnF10": {"transport":"streamable_http","url":"https://ai.szfiu.com/stock_cn_f10/","headers":{"Authorization":"Bearer $TOKEN"}},
    "stockHkSdk": {"transport":"streamable_http","url":"https://ai.szfiu.com/stock_hk_sdk/","headers":{"Authorization":"Bearer $TOKEN"}},
    "stockUsSdk": {"transport":"streamable_http","url":"https://ai.szfiu.com/stock_us_sdk/","headers":{"Authorization":"Bearer $TOKEN"}},
    "stockCnSdk": {"transport":"streamable_http","url":"https://ai.szfiu.com/stock_cn_sdk/","headers":{"Authorization":"Bearer $TOKEN"}},
    "szfiuToolkit": {"transport":"streamable_http","url":"https://ai.szfiu.com/toolkit/"}
  }
}
MCPEOF

    echo -e "${GREEN}✅ 配置完成!${NC}"
    echo "Token 已保存，MCP 配置已创建到 ~/.mcp.json"
    echo ""
    if [ -f "$MCP_FILE.bak" ]; then
        echo "💾 备份文件: ~/.mcp.json.bak"
    fi
    echo "请重启 Claude Code / OpenClaw"
}

# Test connectivity
cmd_test() {
    load_token

    echo "🧪 测试各市场连接..."
    echo ""

    # Test toolkit (no auth needed)
    echo "1. 测试 szfiuToolkit..."
    RESP=$(curl -s -X POST "https://ai.szfiu.com/toolkit/" \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}')
    if echo "$RESP" | grep -q "tools"; then
        echo "   ✅ szfiuToolkit OK"
    else
        echo "   ❌ szfiuToolkit 失败"
    fi

    # Test HK SDK
    echo "2. 测试 stockHkSdk..."
    RESP=$(curl -s -X POST "https://ai.szfiu.com/stock_hk_sdk/" \
        -H "Authorization: Bearer $FIU_MCP_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}')
    if echo "$RESP" | grep -q "tools"; then
        echo "   ✅ stockHkSdk OK"
    else
        echo "   ❌ stockHkSdk 失败"
    fi

    # Test CN SDK
    echo "3. 测试 stockCnSdk..."
    RESP=$(curl -s -X POST "https://ai.szfiu.com/stock_cn_sdk/" \
        -H "Authorization: Bearer $FIU_MCP_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}')
    if echo "$RESP" | grep -q "tools"; then
        echo "   ✅ stockCnSdk OK"
    else
        echo "   ❌ stockCnSdk 失败"
    fi
}

# Discover tools
cmd_discover() {
    load_token
    MARKET="$1"

    if [ -z "$MARKET" ]; then
        echo "用法: discover <market>"
        echo "市场: hk_sdk, us_sdk, cn_sdk, hk_f10, us_f10, cn_f10, toolkit"
        exit 1
    fi

    declare -A ENDPOINTS=(
        ["hk_f10"]="https://ai.szfiu.com/stock_hk_f10/"
        ["us_f10"]="https://ai.szfiu.com/stock_us_f10/"
        ["cn_f10"]="https://ai.szfiu.com/stock_cn_f10/"
        ["hk_sdk"]="https://ai.szfiu.com/stock_hk_sdk/"
        ["us_sdk"]="https://ai.szfiu.com/stock_us_sdk/"
        ["cn_sdk"]="https://ai.szfiu.com/stock_cn_sdk/"
        ["toolkit"]="https://ai.szfiu.com/toolkit/"
    )

    ENDPOINT="${ENDPOINTS[$MARKET]}"
    if [ -z "$ENDPOINT" ]; then
        echo "错误: 未知市场 $MARKET"
        exit 1
    fi

    echo "🔍 发现 $MARKET 可用工具..."
    echo ""

    if [ "$MARKET" == "toolkit" ]; then
        RESP=$(curl -s -X POST "$ENDPOINT" \
            -H "Content-Type: application/json" \
            -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}')
    else
        RESP=$(curl -s -X POST "$ENDPOINT" \
            -H "Authorization: Bearer $FIU_MCP_TOKEN" \
            -H "Content-Type: application/json" \
            -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}')
    fi

    echo "$RESP" | grep -o '"name":"[^"]*"' | sed 's/"name":"//;s/"//' | while read -r tool; do
        echo "  - $tool"
    done
}

# Quote
cmd_quote() {
    load_token
    SYMBOL="$1"

    if [ -z "$SYMBOL" ]; then
        echo "用法: quote <股票代码>"
        echo "示例: quote 00700"
        exit 1
    fi

    # Add suffix if needed
    if [[ ! "$SYMBOL" =~ \. ]] && [ ${#SYMBOL} -eq 5 ]; then
        SYMBOL="${SYMBOL}.HK"
    elif [[ ! "$SYMBOL" =~ \. ]] && [ ${#SYMBOL} -eq 6 ]; then
        SYMBOL="${SYMBOL}.SZ"
    fi

    echo "📊 查询 $SYMBOL 行情..."

    RESP=$(curl -s -X POST "https://ai.szfiu.com/stock_hk_sdk/" \
        -H "Authorization: Bearer $FIU_MCP_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{
            \"jsonrpc\": \"2.0\",
            \"id\": 1,
            \"method\": \"tools/call\",
            \"params\": {
                \"name\": \"post_v3_stock_quote\",
                \"arguments\": {\"fields\": [\"snapshot\"], \"symbols\": [\"$SYMBOL\"]}
            }
        }")

    DATA=$(echo "$RESP" | grep "^data:" | sed 's/^data: //')
    TEXT=$(echo "$DATA" | jq -r '.result.content[0].text' 2>/dev/null)

    if [ -n "$TEXT" ] && [ "$TEXT" != "null" ]; then
        echo "$TEXT" | jq .
    else
        echo "$DATA" | jq .
    fi
}

# Search
cmd_search() {
    load_token
    KEYWORD="$1"

    if [ -z "$KEYWORD" ]; then
        echo "用法: search <关键词>"
        echo "示例: search 腾讯"
        exit 1
    fi

    echo "🔍 搜索 $KEYWORD ..."

    RESP=$(curl -s -X POST "https://ai.szfiu.com/toolkit/" \
        -H "Content-Type: application/json" \
        -d "{
            \"jsonrpc\": \"2.0\",
            \"id\": 1,
            \"method\": \"tools/call\",
            \"params\": {
                \"name\": \"search\",
                \"arguments\": {\"key\": \"$KEYWORD\"}
            }
        }")

    DATA=$(echo "$RESP" | grep "^data:" | sed 's/^data: //')
    TEXT=$(echo "$DATA" | jq -r '.result.content[0].text' 2>/dev/null)

    if [ -n "$TEXT" ] && [ "$TEXT" != "null" ]; then
        echo "$TEXT" | jq .
    else
        echo "$DATA" | jq .
    fi
}

# Dispatch
CMD="$1"
shift

case "$CMD" in
    setup)    cmd_setup "$@" ;;
    test)     cmd_test ;;
    discover) cmd_discover "$@" ;;
    quote)    cmd_quote "$@" ;;
    search)   cmd_search "$@" ;;
    status)   cmd_status ;;
    *)
        echo "用法: $0 <command> [args]"
        echo ""
        echo "命令:"
        echo "  setup <token>    - 快速配置"
        echo "  test             - 测试连接"
        echo "  discover <市场>  - 发现可用工具"
        echo "  quote <代码>     - 查询行情"
        echo "  search <关键词>  - 搜索股票"
        echo "  status           - 显示状态"
        ;;
esac