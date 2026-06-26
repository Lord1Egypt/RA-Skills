#!/bin/bash
# mesh-status.sh — Fleet-wide mesh health check and activity report
#
# Required env vars:
#   MESH_SUPABASE_URL — Supabase REST API URL
#   MESH_SUPABASE_KEY — Supabase anon key
#   MESH_AGENT_ID     — This agent's ID
#
# This script is read-only: it performs GET requests only.

set -euo pipefail

SUPABASE_URL="${MESH_SUPABASE_URL:-}"
SUPABASE_KEY="${MESH_SUPABASE_KEY:-}"
MY_AGENT="${MESH_AGENT_ID:-}"

if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_KEY" ] || [ -z "$MY_AGENT" ]; then
  echo "ERROR: MESH_SUPABASE_URL, MESH_SUPABASE_KEY, and MESH_AGENT_ID must be set."
  echo "Configure via: skills.entries.agent-mesh.env in openclaw.json"
  exit 1
fi

echo "Agent Mesh Status: ${MY_AGENT}"
echo ""

# 1. Connection test
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "${SUPABASE_URL}/agent_messages?limit=1" \
  -H "apikey: ${SUPABASE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_KEY}")

if [ "$HTTP_CODE" = "200" ]; then
  echo "[ok] Supabase connection"
else
  echo "[error] Supabase returned HTTP ${HTTP_CODE}"
  exit 1
fi

# 2. My recent messages (last 30 minutes)
SINCE=$(node -e "console.log(new Date(Date.now() - 30*60*1000).toISOString())")
MY_RECENT=$(curl -s "${SUPABASE_URL}/agent_messages?to_agent=eq.${MY_AGENT}&created_at=gt.${SINCE}&select=id" \
  -H "apikey: ${SUPABASE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_KEY}")

# 3. Fleet-wide recent activity (last 20 messages across all agents)
RECENT=$(curl -s "${SUPABASE_URL}/agent_messages?order=created_at.desc&limit=20" \
  -H "apikey: ${SUPABASE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_KEY}")

node -e "
const myRecent = JSON.parse(process.argv[1] || '[]');
const msgs = JSON.parse(process.argv[2] || '[]');
const me = process.argv[3];

console.log('[inbox] Messages in last 30m: ' + myRecent.length);
console.log('');

// Agent roster with last activity
const agentLast = {};
msgs.forEach(m => {
  const t = new Date(m.created_at).getTime();
  if (!agentLast[m.from_agent] || t > agentLast[m.from_agent]) agentLast[m.from_agent] = t;
  if (m.to_agent !== 'broadcast') {
    if (!agentLast[m.to_agent] || t > agentLast[m.to_agent]) agentLast[m.to_agent] = t;
  }
});
const roster = Object.entries(agentLast).sort((a,b) => b[1]-a[1]);
console.log('Agents on mesh (' + roster.length + '):');
roster.forEach(([agent, ts]) => {
  const ago = Math.round((Date.now() - ts) / 60000);
  const tag = agent === me ? ' (you)' : '';
  const agoStr = ago < 60 ? ago + 'm ago' : Math.round(ago/60) + 'h ago';
  console.log('  ' + agent + tag + ' — last active ' + agoStr);
});
console.log('');

// Recent messages
if (msgs.length === 0) {
  console.log('No recent messages.');
} else {
  console.log('Last 20 messages (fleet-wide):');
  msgs.forEach(m => {
    const dir = m.from_agent + ' -> ' + m.to_agent;
    const t = new Date(m.created_at).toISOString().substring(11,16);
    const thread = m.thread_id ? ' [T:' + m.thread_id.substring(0,8) + ']' : '';
    console.log('  ' + t + ' ' + dir + thread + ': ' + (m.message||'').substring(0,55));
  });
}
" "$MY_RECENT" "$RECENT" "$MY_AGENT"
