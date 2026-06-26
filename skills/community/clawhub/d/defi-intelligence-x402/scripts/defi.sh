#!/usr/bin/env bash
# deep-research gateway caller — handles x402 payment flow via curl
# Usage:
#   research.sh GET  /api/v1/research/papers/search '{"query":"restaking"}'
#   research.sh POST /api/v1/search/web '{"query":"ethereum restaking 2026"}'

set -euo pipefail

METHOD="${1:?Usage: research.sh METHOD ENDPOINT [JSON_BODY]}"
ENDPOINT="${2:?Usage: research.sh METHOD ENDPOINT [JSON_BODY]}"
BODY="${3:-{}}"

GATEWAY="${RESEARCH_GATEWAY_URL:-https://gateway.spraay.app}"
URL="${GATEWAY}${ENDPOINT}"

# Build curl args based on method
if [[ "${METHOD^^}" == "GET" ]]; then
  # Convert JSON body to query params for GET requests
  QUERY_STRING=$(echo "$BODY" | python3 -c "
import sys, json, urllib.parse
try:
    d = json.load(sys.stdin)
    print(urllib.parse.urlencode(d))
except:
    print('')
" 2>/dev/null || echo "")
  if [[ -n "$QUERY_STRING" ]]; then
    URL="${URL}?${QUERY_STRING}"
  fi
  CURL_ARGS=(-s -X GET)
else
  CURL_ARGS=(-s -X POST -H "Content-Type: application/json" -d "$BODY")
fi

# Add auth header if API key is set
if [[ -n "${RESEARCH_API_KEY:-}" ]]; then
  CURL_ARGS+=(-H "Authorization: Bearer ${RESEARCH_API_KEY}")
fi

# Make the request
RESPONSE=$(curl "${CURL_ARGS[@]}" -w "\n%{http_code}" "$URL" 2>/dev/null)
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
RESP_BODY=$(echo "$RESPONSE" | sed '$d')

if [[ "$HTTP_CODE" == "200" ]]; then
  echo "$RESP_BODY"
elif [[ "$HTTP_CODE" == "402" ]]; then
  echo "PAYMENT REQUIRED — This endpoint costs USDC via x402." >&2
  echo "Set RESEARCH_API_KEY for subscription access or use the Python CLI with a funded wallet." >&2
  echo "$RESP_BODY"
else
  echo "HTTP $HTTP_CODE from $URL" >&2
  echo "$RESP_BODY"
  exit 1
fi
