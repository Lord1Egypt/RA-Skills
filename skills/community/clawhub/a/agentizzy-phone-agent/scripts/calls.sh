#!/bin/bash
# Security Manifest:
#   Environment: AGENTIZZY_API_KEY
#   Endpoints: api.agentizzy.com (HTTPS GET /api/v1/agents/:id/calls)
#   Files: None accessed
#
# Retrieves call history with AI summaries and sentiment.
# Usage: bash calls.sh "facility_id" [limit] [since]

set -euo pipefail

FACILITY_ID="${1:?Usage: calls.sh \"facility_id\" [limit] [since]}"
LIMIT="${2:-20}"
SINCE="${3:-}"

if [ -z "${AGENTIZZY_API_KEY:-}" ]; then
  echo '{"error": "AGENTIZZY_API_KEY environment variable is not set. Contact team@agentizzy.com for API access."}'
  exit 1
fi

URL="https://api.agentizzy.com/api/v1/agents/${FACILITY_ID}/calls?limit=${LIMIT}"
[ -n "$SINCE" ] && URL="${URL}&since=${SINCE}"

curl -s "$URL" \
  -H "Authorization: Bearer ${AGENTIZZY_API_KEY}"
