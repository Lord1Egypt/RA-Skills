#!/bin/bash
# Security Manifest:
#   Environment: AGENTIZZY_API_KEY
#   Endpoints: api.agentizzy.com (HTTPS POST /api/v1/agents)
#   Files: None accessed
#
# Provisions a new AI phone agent for a business.
# Usage: bash setup.sh "Business Name" [vertical] [phone] [website_url]

set -euo pipefail

NAME="${1:?Usage: setup.sh \"Business Name\" [vertical] [phone] [website_url]}"
VERTICAL="${2:-}"
PHONE="${3:-}"
WEBSITE="${4:-}"

if [ -z "${AGENTIZZY_API_KEY:-}" ]; then
  echo '{"error": "AGENTIZZY_API_KEY environment variable is not set. Contact team@agentizzy.com for API access."}'
  exit 1
fi

# Escape name for JSON
NAME_ESCAPED=$(printf '%s' "$NAME" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()), end="")')

# Build JSON body
BODY="{\"name\": ${NAME_ESCAPED}"
[ -n "$VERTICAL" ] && BODY="${BODY}, \"vertical\": \"${VERTICAL}\""
[ -n "$PHONE" ] && BODY="${BODY}, \"phone\": \"${PHONE}\""
[ -n "$WEBSITE" ] && BODY="${BODY}, \"website\": \"${WEBSITE}\""
BODY="${BODY}}"

curl -s -X POST "https://api.agentizzy.com/api/v1/agents" \
  -H "Authorization: Bearer ${AGENTIZZY_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$BODY"
