#!/bin/bash
# Token Dynamic Data - Get real-time price, volume, holders

CHAINID="${1:-56}"
CONTRACT="${2:-0x55d398326f99059ff775485246999027b3197955}" # USDT

curl -s "https://web3.binance.com/bapi/defi/v4/public/wallet-direct/buw/wallet/market/token/dynamic/info?chainId=${CHAINID}&contractAddress=${CONTRACT}" \
  -H "Accept-Encoding: identity" | jq '.'
