#!/bin/bash
# 查询行情

source "$(dirname "$0")/_common.sh"

CODES=""
DETAIL=false

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --codes) CODES="$2"; shift 2 ;;
        --detail) DETAIL=true; shift ;;
        -h|--help)
            echo "用法: quotes.sh --codes <股票代码> [--detail]"
            echo ""
            echo "参数:"
            echo "  --codes   股票代码，逗号分隔 (SH600519,HK00700,USAAPL)"
            echo "  --detail  显示详细信息"
            exit 0
            ;;
        *) shift ;;
    esac
done

if [ -z "$CODES" ]; then
    echo "❌ 请提供股票代码: --codes <代码>"
    exit 1
fi

# 获取行情 (不需要认证)
BASE_URL=$(get_config "baseUrl" "https://arena.wade.xylife.net/api")
RESPONSE=$(curl -s "${BASE_URL}/v1/market/quotes?codes=$CODES")

SUCCESS=$(echo "$RESPONSE" | jq -r '.success // false')

if [ "$SUCCESS" != "true" ]; then
    ERROR=$(echo "$RESPONSE" | jq -r '.error.message // "获取行情失败"')
    echo "❌ $ERROR"
    exit 1
fi

echo "📈 实时行情"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

DATA=$(echo "$RESPONSE" | jq '.data')

if [ "$DETAIL" = true ]; then
    echo "$DATA" | jq -r '.[] | "
\(.name) (\(.code))
━━━━━━━━━━━━━━━━━━━━━━━━
现价: \(.price)  涨跌幅: \(if .changePct >= 0 then "+" else "" end)\(.changePct | . * 100 | . * 100 | round / 100)%
今开: \(.open // "-")   昨收: \(.preClose // "-")
最高: \(.high // "-")   最低: \(.low // "-")
成交量: \(.volume // "-")
"'
else
    printf "%-12s %12s %12s %12s\n" "股票" "现价" "涨跌" "涨跌幅"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    echo "$DATA" | jq -r '.[] | [.name, .price, .change, .changePct] | @tsv' | \
    while IFS=$'\t' read -r name price change pct; do
        pct_str=$(printf "%+.2f%%" $(echo "$pct * 100" | bc 2>/dev/null || echo "0"))
        change_str=$(printf "%+.2f" ${change:-0})
        printf "%-10s %12.2f %12s %12s\n" "$name" "${price:-0}" "$change_str" "$pct_str"
    done
fi
