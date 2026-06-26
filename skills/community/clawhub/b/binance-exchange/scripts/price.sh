#!/bin/bash
# Binance Price Query
# Usage: ./price.sh [symbol1] [symbol2] ...

PROXY="-x http://127.0.0.1:1082"
BASE_URL="https://api.binance.com/api/v3"

if [ $# -eq 0 ]; then
  echo "Usage: $0 <symbol> [symbol2] ..."
  echo "Example: $0 BTCUSDT ETHUSDT"
  exit 1
fi

# Get all prices
result=$(curl -s $PROXY "$BASE_URL/ticker/price")

for symbol in "$@"; do
  price=$(echo "$result" | jq -r ".[] | select(.symbol == \"$symbol\") | .price")
  if [ "$price" != "null" ]; then
    echo "$symbol: $price"
  else
    echo "$symbol: Not found"
  fi
done
