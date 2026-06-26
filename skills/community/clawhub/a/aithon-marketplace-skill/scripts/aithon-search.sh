#!/usr/bin/env bash
# Quick search the Aithon catalog
# Usage: aithon-search.sh <query> [category] [limit]
# Examples:
#   aithon-search.sh "fiber Dallas"
#   aithon-search.sh "500mbps" business-internet 5

set -euo pipefail

QUERY="${1:?Usage: aithon-search.sh <query> [category] [limit]}"
CATEGORY="${2:-}"
LIMIT="${3:-10}"

BASE="https://aithon.tech/api/v1/catalog/search"
URL="${BASE}?q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('${QUERY}'))")&limit=${LIMIT}"

if [ -n "$CATEGORY" ]; then
  URL="${URL}&category=${CATEGORY}"
fi

curl -s "$URL" | python3 -m json.tool 2>/dev/null || curl -s "$URL"
