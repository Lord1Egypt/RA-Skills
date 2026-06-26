#!/usr/bin/env bash
# Crypto Data Fetcher — one-shot fetch all data for analysis framework
# Usage: bash crypto-data.sh <BTC|TON|LINK|ETH|SOL|...>
set -euo pipefail

COIN="${1:-BTC}"
INST="${COIN}-USDT"
SWAP="${COIN}-USDT-SWAP"

echo "=== TICKER ==="
okx market ticker "$INST" --json 2>/dev/null

echo "=== CANDLES_15M ==="
okx market candles "$INST" --bar 15m --limit 96 --json 2>/dev/null

echo "=== CANDLES_4H ==="
okx market candles "$INST" --bar 4H --limit 42 --json 2>/dev/null

echo "=== CANDLES_1D ==="
okx market candles "$INST" --bar 1D --limit 14 --json 2>/dev/null

echo "=== RSI_1D ==="
okx market indicator rsi "$INST" --bar 1Dutc --limit 14 --json 2>/dev/null

echo "=== MACD_1D ==="
okx market indicator macd "$INST" --bar 1Dutc --limit 50 --json 2>/dev/null

echo "=== EMA ==="
okx market indicator ema "$INST" --bar 1Dutc --params 7,25,99 --limit 5 --json 2>/dev/null

echo "=== BB ==="
okx market indicator bb "$INST" --bar 1Dutc --limit 5 --json 2>/dev/null

echo "=== FUNDING ==="
okx market funding-rate "$SWAP" --json 2>/dev/null

echo "=== OI ==="
okx market open-interest --instType SWAP --instId "$SWAP" --json 2>/dev/null

echo "=== FEAR_GREED ==="
curl -s 'https://api.alternative.me/fng/?limit=1'