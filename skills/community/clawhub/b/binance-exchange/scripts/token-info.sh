#!/bin/bash
# Token Info - Query token details, market data, and prices
# Uses Binance official API (no proxy needed)

set -e

SYMBOL="${1:-BTCUSDT}"
PROXY="${HTTP_PROXY:-}"

usage() {
    echo "Usage: $0 <symbol> [options]"
    echo ""
    echo "Arguments:"
    echo "  symbol         Trading pair (e.g., BTCUSDT, ETHUSDT, BNBUSDT)"
    echo ""
    echo "Examples:"
    echo "  $0 BTCUSDT"
    echo "  $0 ETHUSDT"
    echo "  $0 BNBUSDT"
    echo ""
    echo "24h Stats:"
    echo "  $0 BTCUSDT stats"
    exit 1
}

if [ -z "$SYMBOL" ]; then
    usage
fi

# Check if requesting stats
if [ "$2" = "stats" ] || [ "$2" = "-s" ]; then
    echo "=== $SYMBOL 24h Statistics ==="
    curl -s "https://api.binance.com/api/v3/ticker/24hr?symbol=${SYMBOL}" | jq '{
        symbol: .symbol,
        price: .lastPrice,
        change24h: .priceChange,
        changePercent: .priceChangePercent,
        high24h: .highPrice,
        low24h: .lowPrice,
        volume: .volume,
        quoteVolume: .quoteVolume,
        weightedAvg: .weightedAvgPrice
    }'
    exit 0
fi

# Default: get basic price info
echo "=== $SYMBOL Price Info ==="
curl -s "https://api.binance.com/api/v3/ticker/price?symbol=${SYMBOL}" | jq '.'
