#!/bin/bash
# Agentcy Data Sources Discovery
# Lists configured domains and connected marketing data sources.
#
# Usage: ./agentcy_sources.sh ["domain"]
#
# Environment: AGENTCY_API_KEY (required)
# External:    https://data.goagentcy.com/api/sources

set -euo pipefail

# --- Validate environment ---
if [ -z "${AGENTCY_API_KEY:-}" ]; then
  echo "Error: AGENTCY_API_KEY environment variable is not set." >&2
  echo "Get your API key at https://www.goagentcy.com" >&2
  exit 1
fi

DOMAIN="${1:-}"

# --- Build URL ---
if [ -n "$DOMAIN" ]; then
  ENCODED_DOMAIN=$(jq -rn --arg d "$DOMAIN" '$d | @uri')
  URL="https://data.goagentcy.com/api/sources?domain=${ENCODED_DOMAIN}"
else
  URL="https://data.goagentcy.com/api/sources"
fi

# --- Call Agentcy REST API ---
HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -H "Authorization: Bearer ${AGENTCY_API_KEY}" \
  "$URL")

HTTP_BODY=$(echo "$HTTP_RESPONSE" | sed '$d')
HTTP_STATUS=$(echo "$HTTP_RESPONSE" | tail -1)

# --- Handle errors ---
if [ "$HTTP_STATUS" -ge 400 ] 2>/dev/null; then
  ERROR_MSG=$(echo "$HTTP_BODY" | jq -r '.error // "Unknown error"' 2>/dev/null || echo "Request failed")
  echo "Error ($HTTP_STATUS): $ERROR_MSG" >&2
  exit 1
fi

# --- Format and display results ---
echo "$HTTP_BODY" | jq -r '
  if (.domains // [] | length) > 0 then
    (.domains[] | "Domain: \(.domain)\n  Connected: \(.services // [] | join(", "))\n")
  else
    "No domains configured.\n"
  end,

  if (.global_services // [] | length) > 0 then
    "Always available (no setup needed):",
    (.global_services[] | "  - \(.name)")
  else
    empty
  end
' 2>/dev/null
