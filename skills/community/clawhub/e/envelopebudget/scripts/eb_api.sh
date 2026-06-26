#!/usr/bin/env bash
# EnvelopeBudget API helper
# Usage: eb_api.sh <METHOD> <path> [json_body]
# Env: ENVELOPE_BUDGET_API_KEY (required)
#
# Examples:
#   eb_api.sh GET /api/budgets
#   eb_api.sh GET "/api/transactions/BUDGET_ID?limit=10"
#   eb_api.sh POST /api/transactions/BUDGET_ID '{"account_id":"...","payee":"Grocery","amount":-5000,"date":"2026-03-06"}'

set -euo pipefail

BASE_URL="https://envelopebudget.com"
METHOD="${1:?Usage: eb_api.sh METHOD path [body]}"
PATH_ARG="${2:?Usage: eb_api.sh METHOD path [body]}"
BODY="${3:-}"

if [ -z "${ENVELOPE_BUDGET_API_KEY:-}" ]; then
  echo "Error: ENVELOPE_BUDGET_API_KEY not set" >&2
  exit 1
fi

CURL_ARGS=(
  -s -w "\n%{http_code}"
  -X "$METHOD"
  -H "X-API-Key: ${ENVELOPE_BUDGET_API_KEY}"
  -H "Content-Type: application/json"
)

if [ -n "$BODY" ]; then
  CURL_ARGS+=(-d "$BODY")
fi

RESPONSE=$(curl "${CURL_ARGS[@]}" "${BASE_URL}${PATH_ARG}")

# Split response body and status code
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY_OUT=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -ge 400 ] 2>/dev/null; then
  echo "HTTP $HTTP_CODE Error:" >&2
  echo "$BODY_OUT" | python3 -m json.tool 2>/dev/null || echo "$BODY_OUT" >&2
  exit 1
fi

echo "$BODY_OUT" | python3 -m json.tool 2>/dev/null || echo "$BODY_OUT"
