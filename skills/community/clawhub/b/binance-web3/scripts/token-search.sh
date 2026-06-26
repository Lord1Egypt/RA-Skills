#!/bin/bash
# Token Search - Search tokens by keyword, chain

KEYWORD="${1:-BTC}"
CHAINIDS="${2:-56}"

curl -s "https://web3.binance.com/bapi/defi/v5/public/wallet-direct/buw/wallet/market/token/search?keyword=${KEYWORD}&chainIds=${CHAINIDS}&orderBy=volume24h" \
  -H "Accept-Encoding: identity" | jq '.'
