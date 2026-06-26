#!/bin/bash
# mesh-agents.sh — Discover all agents on the mesh
#
# Lists every agent that has sent or received a message, with last activity time.
# Use this to find agent IDs before sending messages.
#
# Required env vars:
#   MESH_SUPABASE_URL — Supabase REST API URL
#   MESH_SUPABASE_KEY — Supabase anon key
#   MESH_AGENT_ID     — This agent's ID

set -euo pipefail

SUPABASE_URL="${MESH_SUPABASE_URL:-}"
SUPABASE_KEY="${MESH_SUPABASE_KEY:-}"
MY_AGENT="${MESH_AGENT_ID:-}"

if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ] || [ -z "$MY_AGENT" ]; then
  echo "ERROR: MESH_SUPABASE_URL, MESH_SUPABASE_KEY, and MESH_AGENT_ID must be set."
  echo "Configure via: skills.entries.agent-mesh.env in openclaw.json"
  exit 1
fi

# Fetch recent messages to extract agent roster
MSGS=$(curl -s "${SUPABASE_URL}/agent_messages?select=from_agent,to_agent,created_at&order=created_at.desc&limit=500" \
  -H "apikey: ${SUPABASE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_KEY}")

node -e "
const msgs = JSON.parse(process.argv[1] || '[]');
const me = process.argv[2];
const agentLast = {};
const agentMsgCount = {};

msgs.forEach(m => {
  [m.from_agent, m.to_agent].forEach(a => {
    if (a === 'broadcast') return;
    const t = new Date(m.created_at).getTime();
    if (!agentLast[a] || t > agentLast[a]) agentLast[a] = t;
    agentMsgCount[a] = (agentMsgCount[a] || 0) + 1;
  });
});

const roster = Object.keys(agentLast).sort();
console.log('Agents on mesh: ' + roster.length);
console.log('');
roster.forEach(a => {
  const ago = Math.round((Date.now() - agentLast[a]) / 60000);
  const agoStr = ago < 60 ? ago + ' min ago' : Math.round(ago/60) + ' hours ago';
  const tag = a === me ? ' (you)' : '';
  console.log('  ' + a + tag + ' — last active ' + agoStr + ' — ' + agentMsgCount[a] + ' messages');
});
" "$MSGS" "$MY_AGENT"
