#!/bin/bash
# Smart Money Trading Signals

CHAINID="${1:-56}"

curl -s "https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money" \
  -H "Content-Type: application/json" \
  -H "Accept-Encoding: identity" \
  -d "{\"smartSignalType\":\"\",\"page\":1,\"pageSize\":20,\"chainId\":\"${CHAINID}\"}" | jq '.'
