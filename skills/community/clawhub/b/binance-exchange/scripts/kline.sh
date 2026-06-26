#!/bin/bash
# Binance K-Line Data
# Usage: ./kline.sh <symbol> <interval> [limit]

PROXY="-x http://127.0.0.1:1082"
BASE_URL="https://api.binance.com/api/v3"

if [ $# -lt 2 ]; then
  echo "Usage: $0 <symbol> <interval> [limit]"
  echo "Example: $0 BTCUSDT 1h 100"
  echo "Intervals: 1m, 5m, 15m, 1h, 4h, 1d, 1w"
  exit 1
fi

SYMBOL=$1
INTERVAL=$2
LIMIT=${3:-100}

result=$(curl -s $PROXY "$BASE_URL/klines?symbol=$SYMBOL&interval=$INTERVAL&limit=$LIMIT")

echo "$result" | jq '.[] | {开盘:[1], 最高:[2], 最低:[3], 收盘:[4], 成交量:[5], 时间:[0]}' 2>/dev/null || echo "$result"
