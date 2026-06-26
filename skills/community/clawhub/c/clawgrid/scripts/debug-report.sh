#!/usr/bin/env bash
set -euo pipefail
#
# Submit a debug report for a completed task.
# Called by poll.sh after task submission (success or failure).
#
# Usage: debug-report.sh <task_id> [task_debug_flag] [executor]
#
# Both conditions must be true for the report to be submitted:
#   1. Agent config: "debug_report": true  (default: true)
#   2. Task-level:   agent_context.debug_report == true  (passed as $2)
#
# $3 = executor type: prefetch | hybrid | mock | llm (injected into report)

SKILL_DIR="$HOME/.openclaw/workspace/skills/clawgrid-connector"
source "$SKILL_DIR/scripts/_clawgrid_env.sh"
DEBUGGER="$SKILL_DIR/scripts/local_debugger.py"

if [ $# -lt 1 ]; then
  echo "[DEBUG-REPORT] Usage: debug-report.sh <task_id> [task_debug_flag]" >&2
  exit 1
fi

TASK_ID="$1"
TASK_DEBUG_FLAG="${2:-False}"
EXECUTOR_TYPE="${3:-}"

if [ ! -f "$CONFIG" ]; then
  echo "[DEBUG-REPORT] Config not found, skipping." >&2
  exit 0
fi

if [ ! -f "$DEBUGGER" ]; then
  echo "[DEBUG-REPORT] local_debugger.py not found, skipping." >&2
  exit 0
fi

# Check 1: Agent-level config toggle
AGENT_DEBUG=$(python3 -c "import json; print(json.load(open('$CONFIG')).get('debug_report', True))" 2>/dev/null || echo "True")
if [ "$AGENT_DEBUG" = "False" ] || [ "$AGENT_DEBUG" = "false" ]; then
  exit 0
fi

# Check 2: Task-level flag (from claim response agent_context.debug_report)
if [ "$TASK_DEBUG_FLAG" = "False" ] || [ "$TASK_DEBUG_FLAG" = "false" ]; then
  exit 0
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_key'])")
API_BASE=$(python3 -c "import json; print(json.load(open('$CONFIG'))['api_base'])")

REPORT=$(python3 "$DEBUGGER" "$TASK_ID" 2>/dev/null || true)

if [ -z "$REPORT" ]; then
  echo "[DEBUG-REPORT] No report generated for task $TASK_ID" >&2
  exit 0
fi

if [ -n "$EXECUTOR_TYPE" ]; then
  REPORT=$(echo "$REPORT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
data['executor'] = '$EXECUTOR_TYPE'
print(json.dumps(data))
" 2>/dev/null || echo "$REPORT")
fi

RESP=$(curl -s -w "\n%{http_code}" -X POST "$API_BASE/api/lobster/tasks/$TASK_ID/debug-report" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "$REPORT" \
  --max-time 15)

CODE=$(echo "$RESP" | tail -1)

if [ "$CODE" -ge 200 ] && [ "$CODE" -lt 300 ]; then
  echo "[DEBUG-REPORT] Submitted for task $TASK_ID" >&2
else
  echo "[DEBUG-REPORT] Failed (HTTP $CODE) for task $TASK_ID" >&2
fi
