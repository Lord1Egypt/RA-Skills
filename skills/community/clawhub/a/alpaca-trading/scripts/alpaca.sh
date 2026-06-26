#!/usr/bin/env bash
# alpaca.sh — Thin curl wrapper for Alpaca REST API
# Usage: alpaca <METHOD> <PATH> [JSON_BODY]
# Examples:
#   alpaca GET /v2/account
#   alpaca POST /v2/orders '{"symbol":"AAPL","qty":"10","side":"buy","type":"market","time_in_force":"day"}'
#   alpaca DELETE /v2/orders/ORDER_ID
#   ALPACA_DATA=1 alpaca GET '/v2/stocks/AAPL/quotes/latest'
set -euo pipefail

# --- Auth check ---
if [[ -z "${APCA_API_KEY_ID:-}" || -z "${APCA_API_SECRET_KEY:-}" ]]; then
  echo "Error: APCA_API_KEY_ID and APCA_API_SECRET_KEY must be set" >&2
  exit 1
fi

METHOD="${1:?Usage: alpaca METHOD PATH [BODY]}"
ENDPOINT="${2:?Usage: alpaca METHOD PATH [BODY]}"
BODY="${3:-}"

# --- Base URL resolution ---
# ALPACA_DATA=1 → market data API; otherwise trading API
if [[ "${ALPACA_DATA:-}" == "1" ]]; then
  BASE_URL="${APCA_DATA_API_BASE_URL:-https://data.alpaca.markets}"
else
  BASE_URL="${APCA_API_BASE_URL:-https://paper-api.alpaca.markets}"
fi

URL="${BASE_URL}${ENDPOINT}"

# --- Build curl args ---
CURL_ARGS=(
  -s -w '\n%{http_code}'
  -X "$METHOD"
  -H "APCA-API-KEY-ID: ${APCA_API_KEY_ID}"
  -H "APCA-API-SECRET-KEY: ${APCA_API_SECRET_KEY}"
  -H "Accept: application/json"
)

if [[ -n "$BODY" ]]; then
  CURL_ARGS+=(-H "Content-Type: application/json" -d "$BODY")
fi

# --- Execute ---
RESPONSE=$(curl "${CURL_ARGS[@]}" "$URL")

# Split body and status code
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY_TEXT=$(echo "$RESPONSE" | sed '$d')

# --- Format output ---
if command -v jq &>/dev/null; then
  FORMATTED=$(echo "$BODY_TEXT" | jq . 2>/dev/null || echo "$BODY_TEXT")
else
  FORMATTED=$(echo "$BODY_TEXT" | python3 -m json.tool 2>/dev/null || echo "$BODY_TEXT")
fi

# --- Error handling ---
if [[ "$HTTP_CODE" -ge 400 ]]; then
  echo "HTTP $HTTP_CODE" >&2
  echo "$FORMATTED" >&2
  exit 1
fi

echo "$FORMATTED"
