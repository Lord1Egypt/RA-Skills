#!/bin/bash
# Agentcy Marketing Data Query
# Queries marketing data for a specific client domain via the Agentcy REST API.
# Returns synthesized insights, not raw data.
#
# Usage: ./agentcy_query.sh "question" "domain" [start_date] [end_date] [source_hints]
#
# Environment: AGENTCY_API_KEY (required)
# External:    https://data.goagentcy.com/api/query

set -euo pipefail

# --- Validate environment ---
if [ -z "${AGENTCY_API_KEY:-}" ]; then
  echo "Error: AGENTCY_API_KEY environment variable is not set." >&2
  echo "Get your API key at https://www.goagentcy.com" >&2
  exit 1
fi

# --- Validate arguments ---
if [ $# -lt 2 ]; then
  echo "Usage: ./agentcy_query.sh \"question\" \"domain\" [start_date] [end_date] [source_hints]" >&2
  exit 1
fi

REQUEST="$1"
DOMAIN="$2"
START_DATE="${3:-30daysAgo}"
END_DATE="${4:-yesterday}"
SOURCE_HINTS="${5:-}"

# --- Build JSON payload with jq (safe from injection) ---
if [ -n "$SOURCE_HINTS" ]; then
  HINTS_JSON=$(echo "$SOURCE_HINTS" | jq -R 'split(",")')
  PAYLOAD=$(jq -n \
    --arg req "$REQUEST" \
    --arg dom "$DOMAIN" \
    --arg sd "$START_DATE" \
    --arg ed "$END_DATE" \
    --argjson hints "$HINTS_JSON" \
    '{request: $req, domain: $dom, start_date: $sd, end_date: $ed, source_hints: $hints}')
else
  PAYLOAD=$(jq -n \
    --arg req "$REQUEST" \
    --arg dom "$DOMAIN" \
    --arg sd "$START_DATE" \
    --arg ed "$END_DATE" \
    '{request: $req, domain: $dom, start_date: $sd, end_date: $ed}')
fi

# --- Call Agentcy REST API ---
HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "https://data.goagentcy.com/api/query" \
  -H "Authorization: Bearer ${AGENTCY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

HTTP_BODY=$(echo "$HTTP_RESPONSE" | sed '$d')
HTTP_STATUS=$(echo "$HTTP_RESPONSE" | tail -1)

# --- Handle errors ---
if [ "$HTTP_STATUS" -ge 400 ] 2>/dev/null; then
  ERROR_MSG=$(echo "$HTTP_BODY" | jq -r '.error // "Unknown error"' 2>/dev/null || echo "Request failed")
  ERROR_CODE=$(echo "$HTTP_BODY" | jq -r '.code // "unknown"' 2>/dev/null || echo "unknown")
  echo "Error ($HTTP_STATUS): $ERROR_MSG (code: $ERROR_CODE)" >&2
  exit 1
fi

# --- Extract and display the synthesized insight ---
CONTENT=$(echo "$HTTP_BODY" | jq -r '.content // empty' 2>/dev/null)
SERVICES=$(echo "$HTTP_BODY" | jq -r '.services // [] | join(", ")' 2>/dev/null)

if [ -z "$CONTENT" ]; then
  echo "No content returned from Agentcy." >&2
  exit 1
fi

echo "$CONTENT"

if [ -n "$SERVICES" ]; then
  echo ""
  echo "[Sources: $SERVICES]"
fi
