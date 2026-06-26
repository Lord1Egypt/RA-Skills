#!/bin/bash
# mesh-poll.sh — Poll Supabase for messages addressed to this agent
#
# Usage: mesh-poll.sh [--since ISO_TIMESTAMP]
#
# Required env vars:
#   MESH_SUPABASE_URL — Supabase REST API URL
#   MESH_SUPABASE_KEY — Supabase anon key
#   MESH_AGENT_ID     — This agent's ID
#
# Output: Message details (JSON + summary), or "No new mesh messages."
# The --since flag filters to messages after a given timestamp.
# Without --since, returns messages from the last 30 minutes.
#
# This script is read-only: it performs a single GET request.
# No PATCH, no UPDATE, no state mutation.

set -euo pipefail

SUPABASE_URL="${MESH_SUPABASE_URL:-}"
SUPABASE_KEY="${MESH_SUPABASE_KEY:-}"
MY_AGENT="${MESH_AGENT_ID:-}"

if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ] || [ -z "$MY_AGENT" ]; then
  echo "ERROR: MESH_SUPABASE_URL, MESH_SUPABASE_KEY, and MESH_AGENT_ID must be set."
  echo "Configure via: skills.entries.agent-mesh.env in openclaw.json"
  exit 1
fi

# Parse --since flag, default to 30 minutes ago
SINCE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --since) SINCE="$2"; shift 2 ;;
    *) shift ;;
  esac
done

if [ -z "$SINCE" ]; then
  # Default: last 30 minutes (portable across GNU and BusyBox date)
  SINCE=$(node -e "console.log(new Date(Date.now() - 30*60*1000).toISOString())")
fi

# Fetch messages addressed to this agent since the given timestamp
MESSAGES=$(curl -s \
  "${SUPABASE_URL}/agent_messages?to_agent=eq.${MY_AGENT}&created_at=gt.${SINCE}&order=created_at.asc" \
  -H "apikey: ${SUPABASE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_KEY}")

# Parse and display
node -e "
const msgs = JSON.parse(process.argv[1] || '[]');
if (!Array.isArray(msgs) || msgs.length === 0) {
  console.log('No new mesh messages.');
  process.exit(0);
}
console.log('Found ' + msgs.length + ' message(s):');
msgs.forEach(m => {
  const thread = m.thread_id ? ' [thread:' + m.thread_id + ']' : '';
  console.log('  From: ' + m.from_agent + ' | Priority: ' + (m.priority || 'normal') + thread);
  console.log('  Message: ' + m.message);
  console.log('  Time: ' + m.created_at + ' | ID: ' + m.id);
  console.log('');
});
// Output last timestamp for next --since call
const last = msgs[msgs.length - 1].created_at;
console.log('LAST_TIMESTAMP=' + last);
" "$MESSAGES"
