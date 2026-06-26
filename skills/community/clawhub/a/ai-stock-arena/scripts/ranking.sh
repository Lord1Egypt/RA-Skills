#!/bin/bash
# 查看收益排行榜

source "$(dirname "$0")/_common.sh"
check_config

MARKET="CN"
LIMIT=10

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --market) MARKET="$2"; shift 2 ;;
        --limit) LIMIT="$2"; shift 2 ;;
        -h|--help)
            echo "用法: ranking.sh [--market CN|HK|US] [--limit 10]"
            echo ""
            echo "参数:"
            echo "  --market   市场 (CN=A股, HK=港股, US=美股，默认 CN)"
            echo "  --limit    显示数量 (默认 10)"
            exit 0
            ;;
        *) shift ;;
    esac
done

# 获取自己的排名信息
RESPONSE=$(api_request GET "/v1/agent/portfolios")
SUCCESS=$(echo "$RESPONSE" | jq -r '.success // false')

if [ "$SUCCESS" != "true" ]; then
    echo "❌ 获取排名信息失败"
    exit 1
fi

# 找到对应市场的数据
PORTFOLIO=$(echo "$RESPONSE" | jq --arg market "$MARKET" '.data[] | select(.market == $market)')

if [ -z "$PORTFOLIO" ] || [ "$PORTFOLIO" = "null" ]; then
    echo "❌ 未找到 $MARKET 市场的账户"
    exit 1
fi

# 市场名称
case "$MARKET" in
    CN) MARKET_NAME="A股"; EMOJI="🇨🇳"; CURRENCY="CNY" ;;
    HK) MARKET_NAME="港股"; EMOJI="🇭🇰"; CURRENCY="HKD" ;;
    US) MARKET_NAME="美股"; EMOJI="🇺🇸"; CURRENCY="USD" ;;
esac

echo "$EMOJI $MARKET_NAME 收益排行榜"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 自己的信息
MY_RANK=$(echo "$PORTFOLIO" | jq -r '.rankReturn // "N/A"')
MY_RETURN=$(echo "$PORTFOLIO" | jq -r '.totalReturn // 0')
MY_RETURN_PCT=$(echo "$MY_RETURN * 100" | bc 2>/dev/null || echo "0")
TOTAL_VALUE=$(echo "$PORTFOLIO" | jq -r '.totalValue // 0')

echo "📍 我的排名"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "排名: 第 ${MY_RANK} 名"
printf "累计收益: %+.2f%%\n" "$MY_RETURN_PCT"
echo "总资产: $(format_money $TOTAL_VALUE $CURRENCY)"
echo ""

# 提示
echo "💡 Tips"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "查看完整排行榜: https://arena.wade.xylife.net/rankings?market=$MARKET"
echo ""
echo "注: 排行榜数据来自 portfolios API 的 rankReturn 字段"
