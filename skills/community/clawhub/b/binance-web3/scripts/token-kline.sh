#!/bin/bash
# Token K-Line - Get candlestick data

ADDRESS="${1:-0x55d398326f99059ff775485246999027b3197955}"
PLATFORM="${2:-bsc}"
INTERVAL="${3:-1h}"
LIMIT="${4:-100}"

curl -s "https://dquery.sintral.io/u-kline/v1/k-line/candles?address=${ADDRESS}&platform=${PLATFORM}&interval=${INTERVAL}&limit=${LIMIT}" \
  -H "Accept-Encoding: identity" | jq '.'
