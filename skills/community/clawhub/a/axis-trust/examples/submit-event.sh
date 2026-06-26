#!/usr/bin/env bash
# submit-event.sh — Submit a behavioral event for an agent after an interaction
# Usage: ./submit-event.sh <session_cookie> <agent_id> <event_type> <score_impact> <description>
# Example: ./submit-event.sh "session=abc123" 42 "task_completed" 10 "Completed data analysis accurately"
#
# agent_id: numeric integer (from agents.register or agents.list response)
# event_type: task_completed | task_failed | security_pass | security_fail |
#             compliance_pass | compliance_fail | user_feedback_positive |
#             user_feedback_negative | peer_feedback_positive | peer_feedback_negative |
#             incident_reported | incident_resolved | adversarial_detected
# score_impact: integer from -100 to +100
# Requires authentication (session cookie from https://axistrust.io).

set -euo pipefail

SESSION_COOKIE="${1:?Usage: $0 <session_cookie> <agent_id> <event_type> <score_impact> <description>}"
AGENT_ID="${2:?Provide numeric agent ID}"
EVENT_TYPE="${3:?Provide event type}"
SCORE_IMPACT="${4:?Provide score impact (-100 to +100)}"
DESCRIPTION="${5:?Provide description}"
BASE_URL="https://www.axistrust.io/api/trpc"

echo "Submitting event for agent ID $AGENT_ID: $EVENT_TYPE (impact: $SCORE_IMPACT)"
echo ""

RESPONSE=$(curl -sf -X POST "$BASE_URL/trust.addEvent" \
  -H "Content-Type: application/json" \
  -H "Cookie: $SESSION_COOKIE" \
  -d "{\"json\":{\"agentId\":$AGENT_ID,\"eventType\":\"$EVENT_TYPE\",\"category\":\"submitted_via_skill\",\"scoreImpact\":$SCORE_IMPACT,\"description\":\"$DESCRIPTION\"}}")

echo "$RESPONSE" | python3 -c "
import json, sys

data = json.load(sys.stdin)
result = data['result']['data']['json']

print('=== Event Submitted ===')
print(f'Event ID:    {result.get(\"id\", \"Unknown\")}')
print(f'Agent ID:    {result.get(\"agentId\", \"Unknown\")}')
print(f'Event Type:  {result.get(\"eventType\", \"Unknown\")}')
print(f'Impact:      {result.get(\"scoreImpact\", \"Unknown\")}')
print(f'Status:      {result.get(\"status\", \"Unknown\")}')
print()
print('The event has been recorded in the AXIS audit trail.')
print('Score updates are computed asynchronously.')
"
