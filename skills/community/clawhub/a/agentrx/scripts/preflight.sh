#!/bin/bash
# AgentRx Preflight Check Script for OpenClaw agents
# Usage: ./preflight.sh <agent_id> <tool_name> <payload_json> <schema_json>
#
# Call this BEFORE executing any risky tool call.
# If proceed=false in the response, do NOT call the tool.
# Use suggested_correction to fix your payload first.

set -euo pipefail

AGENT_ID="${1:-}"
TOOL_NAME="${2:-}"
PAYLOAD="${3:-{}}"
SCHEMA="${4:-{}}"

if [[ -z "$AGENT_ID" || -z "$TOOL_NAME" ]]; then
  echo "Usage: $0 <agent_id> <tool_name> <payload_json> <schema_json>" >&2
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
  --argjson payload "$PAYLOAD" \
  --argjson schema  "$SCHEMA" \
  '{
    agent_id:         $agent_id,
    mcp_tool_name:    $tool_name,
    intended_payload: $payload,
    tool_schema:      $schema
  }')

RESPONSE=$(curl -s -w "\n%{http_code}" \
  -X POST "${AGENTRX_BASE_URL}/v1/preflight" \
  -H "X-API-Key: ${AGENTRX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [[ "$HTTP_CODE" != "200" ]]; then
  echo "AgentRx preflight error (HTTP $HTTP_CODE): $BODY" >&2
  exit 1
fi

echo "$BODY" | jq '.'

PROCEED=$(echo "$BODY" | jq -r '.proceed')
RISK=$(echo "$BODY" | jq -r '.risk_score')

echo "" >&2
echo "=== PREFLIGHT RESULT ===" >&2
echo "Risk score: $RISK" >&2
echo "Proceed: $PROCEED" >&2

if [[ "$PROCEED" == "false" ]]; then
  echo "WARNING: AgentRx says DO NOT proceed with this tool call." >&2
  echo "Check suggested_correction in the response above." >&2
  exit 2
fi

echo "Cleared to proceed." >&2
echo "========================" >&2
