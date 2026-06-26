#!/bin/bash
# Security Manifest:
#   Environment: None required
#   Endpoints: api.evallayer.ai (HTTPS POST /demo/evaluate)
#   Files: None accessed
#
# Free demo evaluation — no API key needed. 3 per day per IP.
# Usage: bash demo.sh "topic" "deliverable content"

set -euo pipefail

TOPIC="${1:?Usage: demo.sh \"topic\" \"deliverable content\"}"
DELIVERABLE="${2:?Usage: demo.sh \"topic\" \"deliverable content\"}"

# Escape JSON special characters in inputs
TOPIC_ESCAPED=$(printf '%s' "$TOPIC" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()), end="")')
DELIVERABLE_ESCAPED=$(printf '%s' "$DELIVERABLE" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()), end="")')

curl -s -X POST "https://api.evallayer.ai/demo/evaluate" \
  -H "Content-Type: application/json" \
  -d "{
    \"task_type\": \"crypto_research\",
    \"topic\": ${TOPIC_ESCAPED},
    \"deliverable\": ${DELIVERABLE_ESCAPED}
  }"
