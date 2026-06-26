#!/bin/sh
# check-status.sh — Check the status of an EvalPal evaluation run.
# Usage: bash scripts/check-status.sh --run-id <RUN_ID>
#
# Environment:
#   EVALPAL_API_KEY  (required) — API key for authentication
#   EVALPAL_API_URL  (optional) — Base URL (default: https://evalpal.dev)

set -e

# ---------------------------------------------------------------------------
# Defaults & argument parsing
# ---------------------------------------------------------------------------
API_URL="${EVALPAL_API_URL:-https://evalpal.dev}"
RUN_ID=""

while [ $# -gt 0 ]; do
  case "$1" in
    --run-id)  RUN_ID="$2";  shift 2 ;;
    --help|-h)
      echo "Usage: bash check-status.sh --run-id <ID>"
      echo ""
      echo "Environment:"
      echo "  EVALPAL_API_KEY   API key (required)"
      echo "  EVALPAL_API_URL   Base URL (default: https://evalpal.dev)"
      exit 0
      ;;
    *)  echo "Error: Unknown argument: $1"; exit 1 ;;
  esac
done

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
if [ -z "$EVALPAL_API_KEY" ]; then
  echo "Error: EVALPAL_API_KEY is not set"
  exit 1
fi

if [ -z "$RUN_ID" ]; then
  echo "Error: --run-id is required"
  exit 1
fi

for tool in curl jq; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Error: '$tool' is required but not installed"
    exit 1
  fi
done

# ---------------------------------------------------------------------------
# Fetch run status
# ---------------------------------------------------------------------------
RESPONSE=$(curl -s -w "\n%{http_code}" -X GET \
  -H "Authorization: Bearer $EVALPAL_API_KEY" \
  -H "Content-Type: application/json" \
  "${API_URL}/api/v1/runs/${RUN_ID}" 2>/dev/null) || {
  echo "Error: Could not reach EvalPal API" >&2
  exit 1
}

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

case "$HTTP_CODE" in
  2[0-9][0-9]) ;;
  401) echo "Error: Authentication failed (401)" >&2; exit 1 ;;
  404) echo "Error: Run not found (404)" >&2; exit 1 ;;
  429)
    RETRY=$(echo "$BODY" | jq -r '.retryAfter // "60"' 2>/dev/null || echo "60")
    echo "Error: Rate limited — retry after ${RETRY}s (429)" >&2
    exit 1
    ;;
  *)  echo "Error: API returned HTTP $HTTP_CODE" >&2; exit 1 ;;
esac

# ---------------------------------------------------------------------------
# Format output
# ---------------------------------------------------------------------------
STATUS=$(echo "$BODY" | jq -r '.status // "unknown"')
TOTAL=$(echo "$BODY" | jq -r '.totalTests // "-"')
PASSED=$(echo "$BODY" | jq -r '.passedTests // "-"')
FAILED=$(echo "$BODY" | jq -r '.failedTests // "-"')
CREATED=$(echo "$BODY" | jq -r '.createdAt // "-"')

echo "📊 Run Status: $RUN_ID"
echo "Status: $STATUS"
echo "Started: $CREATED"

if [ "$STATUS" = "completed" ] || [ "$STATUS" = "failed" ]; then
  echo "Total: $TOTAL · Passed: $PASSED · Failed: $FAILED"
fi
