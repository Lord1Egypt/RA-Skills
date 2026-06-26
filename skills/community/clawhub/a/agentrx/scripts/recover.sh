#!/bin/bash
# AgentRx Recovery Script for OpenClaw agents
# Usage: ./recover.sh <agent_id> <tool_name> <error_message> <error_code> [latency_ms]
#
# Uses jq --arg to safely construct JSON — handles quotes, special chars,
# and newlines in error messages without breaking the JSON structure.

set -euo pipefail

AGENT_ID="${1:-}"
TOOL_NAME="${2:-}"
ERROR_MSG="${3:-}"
ERROR_CODE="${4:-0}"
LATENCY_MS="${5:-0}"

if [[ -z "$AGENT_ID" || -z "$TOOL_NAME" ]]; then
  echo "Usage: $0 <agent_id> <tool_name> <error_message> <error_code> [latency_ms]" >&2
  exit 1
fi

if [[ -z "${AGENTRX_API_KEY:-}" ]]; then
  echo "Error: AGENTRX_API_KEY environment variable is not set." >&2
  exit 1
fi

if [[ -z "${AGENTRX_BASE_URL:-}" ]]; then
  echo "Error: AGENTRX_BASE_URL environment variable is not set." >&2
  exit 1
fi

PAYLOAD=$(jq -n \
  --arg agent_id    "$AGENT_ID" \
  --arg tool_name   "$TOOL_NAME" \
  --arg error_msg   "$ERROR_MSG" \
  --arg error_code  "$ERROR_CODE" \
  --arg latency_ms  "$LATENCY_MS" \
  '{
    agent_id:      $agent_id,
    tool_name:     $tool_name,
    error_message: $error_msg,
    error_code:    ($error_code | tonumber),
    latency_ms:    ($latency_ms | tonumber)
  }')

RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST "${AGENTRX_BASE_URL}/v1/openclaw/recover" \
  -H "X-API-Key: ${AGENTRX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [[ "$HTTP_CODE" != "200" && "$HTTP_CODE" != "503" ]]; then
  echo "AgentRx error (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi

echo "$BODY" | jq '.'

INSTRUCTION=$(echo "$BODY" | jq -r '.openclaw_instruction // empty')
CONFIDENCE=$(echo "$BODY" | jq -r '.confidence_score // empty')

if [[ -n "$INSTRUCTION" ]]; then
  echo "" >&2
  echo "=== OPENCLAW INSTRUCTION ===" >&2
  echo "$INSTRUCTION" >&2
  if [[ -n "$CONFIDENCE" ]]; then
    echo "Confidence Score: $CONFIDENCE" >&2
  fi
  echo "============================" >&2
fi
