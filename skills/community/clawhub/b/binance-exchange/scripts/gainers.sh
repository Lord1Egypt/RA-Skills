#!/bin/bash
# Binance Top Gainers (24h)

PROXY="-x http://127.0.0.1:1082"
BASE_URL="https://api.binance.com/api/v3"

SYMBOLS="BTCUSDT ETHUSDT BNBUSDT SOLUSDT XRPUSDT DOGEUSDT ADAUSDT AVAXUSDT LINKUSDT DOTUSDT MATICUSDT LTCUSDT UNIUSDT ATOMUSDT ETCUSDT FILUSDT XLMUSDT APTUSDT ARBUSDT OPUSDT NEARUSDT INJUSDT SUIUSDT TIAUSDT PEPEUSDT WIFUSDT BONKUSDT SHIBUSDT FETUSDT RNDRUSDT GRTUSDT STXUSDT"

echo "=== Binance 24h 涨幅榜 ==="
echo ""

for sym in $SYMBOLS; do
  result=$(curl -s $PROXY "$BASE_URL/klines?symbol=$sym&interval=1d&limit=2" 2>/dev/null)
  open=$(echo "$result" | jq -r '.[0][1]' 2>/dev/null)
  close=$(echo "$result" | jq -r '.[1][4]' 2>/dev/null)
  
  if [ "$open" != "null" ] && [ "$close" != "null" ] && [ -n "$open" ]; then
    change=$(echo "scale=2; ($close - $open) / $open * 100" | bc 2>/dev/null)
    echo "$change|$sym"
  fi
done | sort -t'|' -k1 -rn | head -20 | while read line; do
  change=$(echo "$line" | cut -d'|' -f1)
  sym=$(echo "$line" | cut -d'|' -f2)
  printf "%-12s %+6s%%\n" "$sym" "$change"
done
