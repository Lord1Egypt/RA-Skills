#!/bin/bash
# Agentcy Web Research
# Performs web research and competitive intelligence via the Agentcy REST API.
# Returns synthesized findings with sources.
#
# Usage: ./agentcy_research.sh "question" ["domain"]
#
# Environment: AGENTCY_API_KEY (required)
# External:    https://data.goagentcy.com/api/research

set -euo pipefail

# --- Validate environment ---
if [ -z "${AGENTCY_API_KEY:-}" ]; then
  echo "Error: AGENTCY_API_KEY environment variable is not set." >&2
  echo "Get your API key at https://www.goagentcy.com" >&2
  exit 1
fi

# --- Validate arguments ---
if [ $# -lt 1 ]; then
  echo "Usage: ./agentcy_research.sh \"question\" [\"domain\"]" >&2
  exit 1
fi

REQUEST="$1"
DOMAIN="${2:-}"

# --- Build JSON payload with jq (safe from injection) ---
if [ -n "$DOMAIN" ]; then
  PAYLOAD=$(jq -n \
    --arg req "$REQUEST" \
    --arg dom "$DOMAIN" \
    '{request: $req, domain: $dom}')
else
  PAYLOAD=$(jq -n \
    --arg req "$REQUEST" \
    '{request: $req}')
fi

# --- Call Agentcy REST API ---
HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "https://data.goagentcy.com/api/research" \
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

# --- Extract and display the synthesized research ---
CONTENT=$(echo "$HTTP_BODY" | jq -r '.content // empty' 2>/dev/null)

if [ -z "$CONTENT" ]; then
  echo "No content returned from Agentcy." >&2
  exit 1
fi

echo "$CONTENT"
