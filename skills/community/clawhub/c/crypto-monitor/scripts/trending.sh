#!/bin/bash
# Discover trending tokens via CoinGecko
set -euo pipefail

API_BASE="https://api.coingecko.com/api/v3"

usage() {
    cat << EOF
Usage: trending.sh [options]

Options:
  -l, --limit N    Number of results (default: 10)
  -h, --help       Show this help
EOF
}

LIMIT=10
while [[ $# -gt 0 ]]; do
    case "$1" in
        -l|--limit) LIMIT="$2"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) shift ;;
    esac
done

echo "=== 🔥 Trending Tokens (24h) ==="

data=$(curl -sf --connect-timeout 10 "${API_BASE}/search/trending" 2>/dev/null) || {
    echo "❌ Failed to fetch trending data"
    exit 1
}

echo "$data" | jq -r --argjson limit "$LIMIT" '
    .coins[:$limit][] | 
    "🔥 #\(.market_cap_rank // "?") \(.name) (\(.symbol | ascii_upcase)) | MCap: \(.market_cap // "N/A") | Score: \(.score // "N/A")"
' 2>/dev/null

echo ""
echo "💡 Data from CoinGecko Trending Search"
