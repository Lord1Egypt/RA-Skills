#!/bin/bash
# Query Token Audit - 代币审计
# Usage: ./token-audit.sh <symbol> [chainId]

SYMBOL="${1}"
CHAIN="${2:-56}"

curl -s "https://web3.binance.com/bapi/defi/v1/wallet-direct/buw/wallet/governance/token/info" \
  -H "Content-Type: application/json" \
  -H "Accept-Encoding: identity" \
  -d "{\"symbol\":\"$SYMBOL\",\"chainId\":\"$CHAIN\"}" | jq '.'
