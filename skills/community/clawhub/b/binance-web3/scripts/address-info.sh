#!/bin/bash
# Query Address Info - 地址持仓洞察
# Usage: ./address-info.sh <address> [chainId]

ADDRESS="${1}"
CHAIN="${2:-56}"

curl -s "https://web3.binance.com/bapi/defi/v1/wallet-direct/buw/wallet/token/balance" \
  -H "Content-Type: application/json" \
  -H "Accept-Encoding: identity" \
  -d "{\"address\":\"$ADDRESS\",\"chainId\":\"$CHAIN\"}" | jq '.'
