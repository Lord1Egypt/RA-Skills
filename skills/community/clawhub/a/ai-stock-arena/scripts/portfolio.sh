#!/bin/bash
# 查看投资组合

source "$(dirname "$0")/_common.sh"
check_config

MARKET=""
ALL=false
FORMAT="summary"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --market) MARKET="$2"; shift 2 ;;
        --all) ALL=true; shift ;;
        --format) FORMAT="$2"; shift 2 ;;
        -h|--help)
            echo "用法: portfolio.sh [--market CN|HK|US] [--all] [--format summary|positions]"
            echo ""
            echo "参数:"
            echo "  --market   市场 (CN=A股, HK=港股, US=美股)"
            echo "  --all      显示所有市场"
            echo "  --format   输出格式 (summary=概览, positions=持仓)"
            exit 0
            ;;
        *) shift ;;
    esac
done

# 默认显示A股
[ -z "$MARKET" ] && [ "$ALL" = false ] && MARKET="CN"

show_portfolio() {
    local market="$1"
    local response=$(api_request GET "/v1/agent/portfolio?market=$market")
    local success=$(echo "$response" | jq -r '.success // false')
    
    if [ "$success" != "true" ]; then
        echo "❌ 获取 $market 组合失败"
        return 1
    fi
    
    local data=$(echo "$response" | jq '.data')
    local total=$(echo "$data" | jq -r '.totalAssets // 0')
    local cash=$(echo "$data" | jq -r '.cash // 0')
    local return_pct=$(echo "$data" | jq -r '.totalReturn // 0')
    local currency=$(echo "$data" | jq -r '.currency // "CNY"')
    
    # 市场名称和 emoji
    local market_name=""
    local emoji=""
    case "$market" in
        CN) market_name="A股"; emoji="🇨🇳" ;;
        HK) market_name="港股"; emoji="🇭🇰" ;;
        US) market_name="美股"; emoji="🇺🇸" ;;
    esac
    
    echo ""
    echo "$emoji $market_name 账户"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "总资产: $(format_money $total $currency)"
    echo "现金: $(format_money $cash $currency)"
    echo "收益率: $(format_percent $return_pct)"
    
    # 持仓详情
    if [ "$FORMAT" = "positions" ]; then
        local positions=$(echo "$data" | jq -r '.positions // []')
        local count=$(echo "$positions" | jq 'length')
        
        if [ "$count" -gt 0 ]; then
            echo ""
            echo "📋 持仓明细"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            printf "%-12s %8s %10s %10s %10s\n" "股票" "数量" "成本" "现价" "盈亏"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            
            echo "$positions" | jq -r '.[] | [.stockName, .shares, .avgCost, .currentPrice, .unrealizedPnlPct] | @tsv' | \
            while IFS=$'\t' read -r name shares cost price pnl_pct; do
                printf "%-10s %8s %10.2f %10.2f %10s\n" "$name" "$shares" "$cost" "$price" "$(format_percent $pnl_pct)"
            done
        else
            echo ""
            echo "📋 暂无持仓"
        fi
    fi
}

echo "📊 投资组合"

if [ "$ALL" = true ]; then
    show_portfolio "CN"
    show_portfolio "HK"
    show_portfolio "US"
else
    show_portfolio "$MARKET"
fi
