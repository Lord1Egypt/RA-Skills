#!/bin/bash
# Binance 24h Change (via K-lines)
# Usage: ./change.sh [symbol]

PROXY="-x http://127.0.0.1:1082"
BASE_URL="https://api.binance.com/api/v3"

if [ $# -eq 0 ]; then
  echo "Usage: $0 <symbol>"
  echo "Example: $0 BTCUSDT"
  exit 1
fi

SYMBOL=$1
result=$(curl -s $PROXY "$BASE_URL/klines?symbol=$SYMBOL&interval=1d&limit=2")

open=$(echo "$result" | jq -r '.[0][1]')
close=$(echo "$result" | jq -r '.[1][4]')

if [ "$open" != "null" ] && [ "$close" != "null" ]; then
  change=$(echo "scale=4; ($close - $open) / $open * 100" | bc)
  echo "$SYMBOL: 开盘=$open 收=$close 变化=$change%"
else
  echo "$SYMBOL: 数据获取失败"
fi
