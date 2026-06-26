#!/bin/bash
# Security Manifest:
#   Environment: None required
#   Endpoints: api.agentizzy.com (HTTPS POST /api/v1/register)
#   Files: None accessed
#
# Registers a new free-tier API key. No authentication required.
# Usage: bash register.sh "Agent Name" [agent_id]

set -euo pipefail

NAME="${1:?Usage: register.sh \"Agent Name\" [agent_id]}"
AGENT_ID="${2:-}"

# Escape name for JSON
NAME_ESCAPED=$(printf '%s' "$NAME" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()), end="")')

BODY="{\"name\": ${NAME_ESCAPED}"
[ -n "$AGENT_ID" ] && BODY="${BODY}, \"agent_id\": \"${AGENT_ID}\""
BODY="${BODY}}"

curl -s -X POST "https://api.agentizzy.com/api/v1/register" \
  -H "Content-Type: application/json" \
  -d "$BODY"
