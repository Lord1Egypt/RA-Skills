#!/bin/bash
# Security Manifest:
#   Environment: EVALLAYER_API_KEY
#   Endpoints: api.evallayer.ai (HTTPS POST /evaluate)
#   Files: None accessed
#
# Submits a deliverable to EvalLayer for quality evaluation.
# Usage: bash evaluate.sh "topic" "deliverable content"

set -euo pipefail

TOPIC="${1:?Usage: evaluate.sh \"topic\" \"deliverable content\"}"
DELIVERABLE="${2:?Usage: evaluate.sh \"topic\" \"deliverable content\"}"

if [ -z "${EVALLAYER_API_KEY:-}" ]; then
  echo '{"error": "EVALLAYER_API_KEY environment variable is not set. Register at: curl -X POST https://api.evallayer.ai/register -H \"Content-Type: application/json\" -d {\"agent_id\": \"your-id\"}"}'
  exit 1
fi

# Escape JSON special characters in inputs
TOPIC_ESCAPED=$(printf '%s' "$TOPIC" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()), end="")')
DELIVERABLE_ESCAPED=$(printf '%s' "$DELIVERABLE" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()), end="")')

curl -s -X POST "https://api.evallayer.ai/evaluate" \
  -H "Authorization: Bearer ${EVALLAYER_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"task_type\": \"crypto_research\",
    \"topic\": ${TOPIC_ESCAPED},
    \"deliverable\": ${DELIVERABLE_ESCAPED}
  }"
