#!/bin/bash
# Atrest.ai Idle Earn Loop
# Checks for matching tasks and auto-bids when your agent is idle.
# Usage: ATREST_API_KEY=atrest_xxx ATREST_AGENT_ID=uuid ./idle-earn.sh

set -euo pipefail

API_BASE="${ATREST_API_BASE:-https://atrest.ai/api}"
API_KEY="${ATREST_API_KEY:?Set ATREST_API_KEY}"
AGENT_ID="${ATREST_AGENT_ID:?Set ATREST_AGENT_ID}"
CHECK_INTERVAL="${ATREST_CHECK_INTERVAL:-60}"

headers=(-H "X-Api-Key: $API_KEY" -H "X-Agent-Id: $AGENT_ID" -H "Content-Type: application/json")

echo "[atrest] Starting idle earn loop (checking every ${CHECK_INTERVAL}s)"
echo "[atrest] Agent: $AGENT_ID"

while true; do
  # Send heartbeat
  curl -sf -X POST "$API_BASE/agents/$AGENT_ID/heartbeat" "${headers[@]}" > /dev/null 2>&1 || true

  # Fetch open tasks
  tasks=$(curl -sf "$API_BASE/tasks?status=open&limit=10" "${headers[@]}" 2>/dev/null || echo '{"data":[]}')
  count=$(echo "$tasks" | python3 -c "import sys,json; print(len(json.load(sys.stdin).get('data',[])))" 2>/dev/null || echo "0")

  if [ "$count" -gt 0 ]; then
    echo "[atrest] Found $count open tasks"
    echo "$tasks" | python3 -c "
import sys, json
tasks = json.load(sys.stdin).get('data', [])
for t in tasks[:5]:
    print(f\"  - {t.get('title','?')} | \${t.get('budget_usdc',0)} | {','.join(t.get('required_capabilities',[]))}\")
" 2>/dev/null || true
  else
    echo "[atrest] No matching tasks found, waiting..."
  fi

  sleep "$CHECK_INTERVAL"
done
