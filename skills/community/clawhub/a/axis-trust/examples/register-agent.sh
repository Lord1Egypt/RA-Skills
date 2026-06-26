#!/usr/bin/env bash
# register-agent.sh — Register a new agent with the AXIS trust infrastructure
# Usage: ./register-agent.sh <session_cookie> <agent_name> <agent_class>
# Example: ./register-agent.sh "session=abc123" "My Research Agent" "research"
#
# Agent classes: enterprise, personal, research, service, autonomous
# Requires authentication (session cookie from https://axistrust.io).

set -euo pipefail

SESSION_COOKIE="${1:?Usage: $0 <session_cookie> <agent_name> <agent_class>}"
AGENT_NAME="${2:?Provide agent name}"
AGENT_CLASS="${3:?Provide agent class: enterprise|personal|research|service|autonomous}"
BASE_URL="https://www.axistrust.io/api/trpc"

echo "Registering agent: $AGENT_NAME (class: $AGENT_CLASS)"
echo ""

RESPONSE=$(curl -sf -X POST "$BASE_URL/agents.register" \
  -H "Content-Type: application/json" \
  -H "Cookie: $SESSION_COOKIE" \
  -d "{\"json\":{\"name\":\"$AGENT_NAME\",\"agentClass\":\"$AGENT_CLASS\"}}")

echo "$RESPONSE" | python3 -c "
import json, sys

data = json.load(sys.stdin)
agent = data['result']['data']['json']

print('=== Agent Registered ===')
print(f'Numeric ID:  {agent[\"id\"]}   <-- SAVE THIS — required for score/event calls')
print(f'AUID:        {agent[\"auid\"]}')
print(f'Name:        {agent[\"name\"]}')
print(f'Class:       {agent[\"agentClass\"]}')
print(f'Registered:  {agent.get(\"createdAt\", \"Unknown\")}')
print()
print('Next steps:')
print('  - Use the numeric ID (not AUID) for trust.getScore, trust.addEvent, credit.getScore')
print('  - Share the AUID string with other agents for public trust lookups')
"
