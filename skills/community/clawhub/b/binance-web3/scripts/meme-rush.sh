#!/bin/bash
# Meme Rush - Meme热度追踪
# Usage: ./meme-rush.sh [chainId]

CHAIN="${1:-56}"

curl -s "https://web3.binance.com/bapi/defi/v1/wallet-direct/buw/wallet/market/hot?chainId=$CHAIN" \
  -H "Accept-Encoding: identity" | jq '.'
