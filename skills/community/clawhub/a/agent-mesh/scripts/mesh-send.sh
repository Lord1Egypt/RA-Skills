#!/bin/bash
# mesh-send.sh — Send a message to another agent (or broadcast to all) via Supabase
#
# Usage: mesh-send.sh <to_agent> <message> [priority] [thread_id]
#
# Required env vars:
#   MESH_SUPABASE_URL — Supabase REST API URL
#   MESH_SUPABASE_KEY — Supabase anon key
#   MESH_AGENT_ID     — This agent's ID
#
# Special to_agent values:
#   "broadcast" — fans out one message per agent (excluding sender)
#
# Priority: low, normal (default), high, urgent
# Thread ID: optional, groups related messages into a conversation

set -euo pipefail

SUPABASE_URL="${MESH_SUPABASE_URL:-}"
SUPABASE_KEY="${MESH_SUPABASE_KEY:-}"
MY_AGENT="${MESH_AGENT_ID:-}"

TO_AGENT="${1:-}"
MESSAGE="${2:-}"
PRIORITY="${3:-normal}"
THREAD_ID="${4:-}"

if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ] || [ -z "$MY_AGENT" ]; then
  echo "ERROR: MESH_SUPABASE_URL, MESH_SUPABASE_KEY, and MESH_AGENT_ID must be set."
  echo "Configure via: skills.entries.agent-mesh.env in openclaw.json"
  exit 1
fi

if [ -z "$TO_AGENT" ] || [ -z "$MESSAGE" ]; then
  echo "Usage: mesh-send.sh <to_agent> <message> [priority] [thread_id]"
  echo "  to_agent: agent_id or 'broadcast'"
  echo "  priority: low | normal | high | urgent"
  echo "  thread_id: optional conversation thread"
  exit 1
fi

# Broadcast: fan out individual messages to each known agent
if [ "$TO_AGENT" = "broadcast" ]; then
  # Discover all agents that have sent or received messages (excluding self)
  ROSTER=$(curl -s "${SUPABASE_URL}/agent_messages?select=from_agent,to_agent&limit=200" \
    -H "apikey: ${SUPABASE_KEY}" \
    -H "Authorization: Bearer ${SUPABASE_KEY}")

  AGENTS=$(node -e "
const msgs = JSON.parse(process.argv[1] || '[]');
const agents = new Set();
msgs.forEach(m => { agents.add(m.from_agent); if (m.to_agent !== 'broadcast') agents.add(m.to_agent); });
agents.delete(process.argv[2]);
agents.delete('broadcast');
console.log([...agents].join('\n'));
" "$ROSTER" "$MY_AGENT")

  if [ -z "$AGENTS" ]; then
    echo "No other agents found on the mesh to broadcast to."
    exit 0
  fi

  SENT=0
  while IFS= read -r AGENT; do
    [ -z "$AGENT" ] && continue
    PAYLOAD=$(node -e "
console.log(JSON.stringify({
  from_agent: process.argv[1],
  to_agent: process.argv[2],
  message: process.argv[3],
  priority: process.argv[4],
  metadata: { broadcast: true }
}));
" "$MY_AGENT" "$AGENT" "$MESSAGE" "$PRIORITY" "$THREAD_ID")

    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${SUPABASE_URL}/agent_messages" \
      -H "apikey: ${SUPABASE_KEY}" \
      -H "Authorization: Bearer ${SUPABASE_KEY}" \
      -H "Content-Type: application/json" \
      -H "Prefer: return=minimal" \
      -d "$PAYLOAD")

    if [ "$HTTP_CODE" = "201" ]; then
      SENT=$((SENT + 1))
    else
      echo "WARN: Failed to send to ${AGENT} (HTTP ${HTTP_CODE})"
    fi
  done <<< "$AGENTS"

  echo "Broadcast sent to ${SENT} agent(s): ${MESSAGE:0:80}"
  exit 0
fi

# Direct message to a single agent
PAYLOAD=$(node -e "
console.log(JSON.stringify({
  from_agent: process.argv[1],
  to_agent: process.argv[2],
  message: process.argv[3],
  priority: process.argv[4],
  metadata: {}
}));
" "$MY_AGENT" "$TO_AGENT" "$MESSAGE" "$PRIORITY" "$THREAD_ID")

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${SUPABASE_URL}/agent_messages" \
  -H "apikey: ${SUPABASE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_KEY}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=minimal" \
  -d "$PAYLOAD")

if [ "$HTTP_CODE" = "201" ]; then
  echo "Sent to ${TO_AGENT} (${PRIORITY}): ${MESSAGE:0:80}"
else
  echo "ERROR: Supabase returned HTTP ${HTTP_CODE}"
  exit 1
fi
