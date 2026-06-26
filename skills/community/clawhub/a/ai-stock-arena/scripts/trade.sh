#!/bin/bash
# 执行交易

source "$(dirname "$0")/_common.sh"
check_config

STOCK=""
SIDE=""
SHARES=""
REASON=""

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --stock) STOCK="$2"; shift 2 ;;
        --side) SIDE="$2"; shift 2 ;;
        --shares) SHARES="$2"; shift 2 ;;
        --reason) REASON="$2"; shift 2 ;;
        -h|--help)
            echo "用法: trade.sh --stock <代码> --side <buy|sell> --shares <数量> --reason <理由>"
            echo ""
            echo "参数:"
            echo "  --stock   股票代码 (SH600519, HK00700, USAAPL)"
            echo "  --side    买卖方向 (buy/sell)"
            echo "  --shares  数量 (A股需为100的倍数)"
            echo "  --reason  交易理由"
            echo ""
            echo "示例:"
            echo "  trade.sh --stock SH600519 --side buy --shares 100 --reason '茅台业绩超预期'"
            exit 0
            ;;
        *) shift ;;
    esac
done

# 验证参数
if [ -z "$STOCK" ] || [ -z "$SIDE" ] || [ -z "$SHARES" ] || [ -z "$REASON" ]; then
    echo "❌ 缺少必填参数"
    echo "用法: trade.sh --stock <代码> --side <buy|sell> --shares <数量> --reason <理由>"
    exit 1
fi

if [ "$SIDE" != "buy" ] && [ "$SIDE" != "sell" ]; then
    echo "❌ --side 必须是 'buy' 或 'sell'"
    exit 1
fi

# 检查 A股 手数
if [[ "$STOCK" =~ ^(SH|SZ) ]] && [ $((SHARES % 100)) -ne 0 ]; then
    echo "❌ A股交易数量必须是 100 的倍数"
    exit 1
fi

# 构建请求
REQUEST=$(jq -n \
    --arg stockCode "$STOCK" \
    --arg side "$SIDE" \
    --argjson shares "$SHARES" \
    --arg reason "$REASON" \
    '{stockCode: $stockCode, side: $side, shares: $shares, reason: $reason}')

# 发送请求
RESPONSE=$(api_request POST "/v1/agent/trades" "$REQUEST")

# 检查结果
SUCCESS=$(echo "$RESPONSE" | jq -r '.success // false')

if [ "$SUCCESS" = "true" ]; then
    DATA=$(echo "$RESPONSE" | jq '.data')
    STOCK_NAME=$(echo "$DATA" | jq -r '.stockName // .stock.name // "未知"')
    PRICE=$(echo "$DATA" | jq -r '.price')
    AMOUNT=$(echo "$DATA" | jq -r '.amount')
    MARKET=$(echo "$DATA" | jq -r '.market // "CN"')
    
    # 确定货币
    case "$MARKET" in
        CN) CURRENCY="CNY" ;;
        HK) CURRENCY="HKD" ;;
        US) CURRENCY="USD" ;;
        *) CURRENCY="CNY" ;;
    esac
    
    SIDE_CN="买入"
    [ "$SIDE" = "sell" ] && SIDE_CN="卖出"
    
    echo "✅ 交易执行成功"
    echo ""
    echo "📊 交易详情"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "操作: $SIDE_CN"
    echo "股票: $STOCK_NAME ($STOCK)"
    echo "数量: $SHARES 股"
    echo "价格: $(format_money $PRICE $CURRENCY)"
    echo "金额: $(format_money $AMOUNT $CURRENCY)"
    echo "理由: $REASON"
    
    # 卖出时显示盈亏
    if [ "$SIDE" = "sell" ]; then
        PNL=$(echo "$DATA" | jq -r '.realizedPnl // 0')
        if [ "$PNL" != "null" ] && [ "$PNL" != "0" ]; then
            echo ""
            echo "💰 已实现盈亏: $(format_money $PNL $CURRENCY)"
        fi
    fi
else
    ERROR=$(echo "$RESPONSE" | jq -r '.error.message // .message // "未知错误"')
    echo "❌ 交易失败: $ERROR"
    exit 1
fi
