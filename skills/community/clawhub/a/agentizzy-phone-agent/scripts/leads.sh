#!/bin/bash
# Security Manifest:
#   Environment: AGENTIZZY_API_KEY
#   Endpoints: api.agentizzy.com (HTTPS GET /api/v1/agents/:id/leads)
#   Files: None accessed
#
# Retrieves leads captured from phone calls.
# Usage: bash leads.sh "facility_id" [limit]

set -euo pipefail

FACILITY_ID="${1:?Usage: leads.sh \"facility_id\" [limit]}"
LIMIT="${2:-50}"

if [ -z "${AGENTIZZY_API_KEY:-}" ]; then
  echo '{"error": "AGENTIZZY_API_KEY environment variable is not set. Contact team@agentizzy.com for API access."}'
  exit 1
fi

curl -s "https://api.agentizzy.com/api/v1/agents/${FACILITY_ID}/leads?limit=${LIMIT}" \
  -H "Authorization: Bearer ${AGENTIZZY_API_KEY}"
