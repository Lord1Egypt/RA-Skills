#!/bin/bash
# 市场概览

source "$(dirname "$0")/_common.sh"

MARKET="${1:-CN}"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --market) MARKET="$2"; shift 2 ;;
        -h|--help)
            echo "用法: overview.sh [--market CN|HK|US]"
            echo ""
            echo "参数:"
            echo "  --market   市场 (CN=A股, HK=港股, US=美股，默认 CN)"
            exit 0
            ;;
        *) shift ;;
    esac
done

# 获取市场概览
BASE_URL=$(get_config "baseUrl" "https://arena.wade.xylife.net/api")
RESPONSE=$(curl -s "${BASE_URL}/v1/market/overview?market=$MARKET")

SUCCESS=$(echo "$RESPONSE" | jq -r '.success // false')

if [ "$SUCCESS" != "true" ]; then
    echo "❌ 获取市场概览失败"
    exit 1
fi

DATA=$(echo "$RESPONSE" | jq '.data')

# 市场名称
case "$MARKET" in
    CN) echo "🇨🇳 A股市场概览"; echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" ;;
    HK) echo "🇭🇰 港股市场概览"; echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" ;;
    US) echo "🇺🇸 美股市场概览"; echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" ;;
esac

# 指数数据
echo ""
echo "📊 主要指数"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
printf "%-12s %12s %10s\n" "指数" "点位" "涨跌幅"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "$DATA" | jq -r '.indices | to_entries[] | [.key, .value.price, .value.changePct] | @tsv' | \
while IFS=$'\t' read -r name price change; do
    change_pct=$(echo "$change * 100" | bc 2>/dev/null || echo "0")
    printf "%-10s %12.2f %+10.2f%%\n" "$name" "$price" "$change_pct"
done

# 涨跌分布
echo ""
echo "📈 涨跌分布"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
UP_COUNT=$(echo "$DATA" | jq -r '.upCount // 0')
DOWN_COUNT=$(echo "$DATA" | jq -r '.downCount // 0')
FLAT_COUNT=$(echo "$DATA" | jq -r '.flatCount // 0')
TOTAL=$((UP_COUNT + DOWN_COUNT + FLAT_COUNT))

if [ "$TOTAL" -gt 0 ]; then
    UP_PCT=$(echo "scale=1; $UP_COUNT * 100 / $TOTAL" | bc)
    DOWN_PCT=$(echo "scale=1; $DOWN_COUNT * 100 / $TOTAL" | bc)
    
    echo "🔴 上涨: $UP_COUNT ($UP_PCT%)"
    echo "🟢 下跌: $DOWN_COUNT ($DOWN_PCT%)"
    echo "⚪ 平盘: $FLAT_COUNT"
    echo ""
    
    # 赚钱效应
    if [ "$UP_PCT" != "" ]; then
        if (( $(echo "$UP_PCT > 70" | bc -l) )); then
            echo "💰 赚钱效应: ${UP_PCT}% (强)"
        elif (( $(echo "$UP_PCT > 50" | bc -l) )); then
            echo "💰 赚钱效应: ${UP_PCT}% (中)"
        else
            echo "💰 赚钱效应: ${UP_PCT}% (弱)"
        fi
    fi
fi

echo ""
TIMESTAMP=$(echo "$DATA" | jq -r '.timestamp // "N/A"')
echo "更新时间: $TIMESTAMP"
