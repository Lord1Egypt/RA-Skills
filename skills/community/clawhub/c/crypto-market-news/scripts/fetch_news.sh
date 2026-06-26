#!/bin/bash
# fetch_news.sh - Fetch crypto news from public RSS feeds
# Usage: bash fetch_news.sh [keyword] [hours]
# Example: bash fetch_news.sh "bitcoin" 24

KEYWORD="${1:-}"
HOURS="${2:-24}"
CUTOFF=$(date -v -${HOURS}H +%s 2>/dev/null || date -d "-${HOURS} hours" +%s 2>/dev/null)

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

RSS_FEEDS=(
  "https://feeds.feedburner.com/CoinDesk"
  "https://cointelegraph.com/rss"
  "https://decrypt.co/feed"
  "https://cryptoslate.com/feed/"
)

FEED_NAMES=("CoinDesk" "CoinTelegraph" "Decrypt" "CryptoSlate")

echo "=== Crypto Market News (last ${HOURS}h) ==="
[ -n "$KEYWORD" ] && echo "=== Filter: $KEYWORD ==="
echo ""

for i in "${!RSS_FEEDS[@]}"; do
  FEED="${RSS_FEEDS[$i]}"
  NAME="${FEED_NAMES[$i]}"
  echo "--- $NAME ---"

  RAW=$(curl -sL --max-time 10 "$FEED" 2>/dev/null)
  if [ -z "$RAW" ]; then
    echo "(fetch failed)"
    echo ""
    continue
  fi

  echo "$RAW" | python3 "$SCRIPT_DIR/parse_rss.py" "$KEYWORD" "$CUTOFF"
  echo ""
done
