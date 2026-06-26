#!/bin/bash
# 获取热门股票

source "$(dirname "$0")/_common.sh"

MARKET="CN"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --market) MARKET="$2"; shift 2 ;;
        -h|--help)
            echo "用法: hot.sh [--market CN|HK|US]"
            echo ""
            echo "参数:"
            echo "  --market  市场 (CN=A股, HK=港股, US=美股，默认 CN)"
            exit 0
            ;;
        *) shift ;;
    esac
done

# 获取热门股票 (不需要认证)
BASE_URL=$(get_config "baseUrl" "https://arena.wade.xylife.net/api")
RESPONSE=$(curl -s "${BASE_URL}/v1/market/hot?market=$MARKET")

SUCCESS=$(echo "$RESPONSE" | jq -r '.success // false')

if [ "$SUCCESS" != "true" ]; then
    ERROR=$(echo "$RESPONSE" | jq -r '.error.message // "获取失败"')
    echo "❌ $ERROR"
    exit 1
fi

# 市场名称
MARKET_NAME=""
case "$MARKET" in
    CN) MARKET_NAME="A股" ;;
    HK) MARKET_NAME="港股" ;;
    US) MARKET_NAME="美股" ;;
esac

echo "🔥 $MARKET_NAME 热门股票"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "%-12s %12s %12s %12s\n" "股票" "现价" "涨跌幅" "成交额"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "$RESPONSE" | jq -r '.data[:10] | .[] | [.name, .price, .changePct, .amount] | @tsv' | \
while IFS=$'\t' read -r name price pct amount; do
    pct_str=$(printf "%+.2f%%" $(echo "${pct:-0} * 100" | bc 2>/dev/null || echo "0"))
    # 格式化成交额 (使用 bc 处理浮点数)
    amount_num=$(printf "%.0f" "${amount:-0}" 2>/dev/null || echo "0")
    if [ "$amount_num" -gt 100000000 ] 2>/dev/null; then
        amount_str=$(printf "%.1f亿" $(echo "$amount / 100000000" | bc -l 2>/dev/null || echo "0"))
    else
        amount_str=$(printf "%.0f万" $(echo "$amount / 10000" | bc 2>/dev/null || echo "0"))
    fi
    printf "%-10s %12.2f %12s %12s\n" "$name" "${price:-0}" "$pct_str" "$amount_str"
done
