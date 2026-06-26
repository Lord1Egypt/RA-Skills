#!/bin/bash
#
# Frugal Orchestrator - Delegation Router v0.5.0
# Routes tasks to appropriate subordinates with token tracking
#
# Usage: delegate.sh <profile> "task description"
# Output: JSON for Agent Zero call_subordinate execution
#

set -uo pipefail

PROJECT_DIR="/a0/usr/projects/frugal_orchestrator"
LOGDIR="$PROJECT_DIR/logs"

PROFILE="${1:-}"
TASK="${2:-}"
CONTEXT="${3:-}"

if [[ -z "$PROFILE" || -z "$TASK" ]]; then
 echo '{"error": "Usage: delegate.sh <profile> \"task\" [context]"}' >&2
 exit 1
fi

mkdir -p "$LOGDIR"
TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S)
SESSION_ID="$(date +%Y%m%d_%H%M%S)_$$"
TOKENS_FILE="$LOGDIR/tokens.json"

# Estimate initial burn (15 tokens per word + 500 system overhead)
TASK_WORDS=$(echo "$TASK" | wc -w)
ESTIMATED_BURN=$((TASK_WORDS * 15 + 500))

# Record delegation start using Python for valid JSON
python3 << EOF
import json
from pathlib import Path
from datetime import datetime

log_file = Path("$TOKENS_FILE")
entry = {
    "timestamp": "$TIMESTAMP",
    "session_id": "$SESSION_ID",
    "profile": "$PROFILE",
    "task_snippet": "$(echo "$TASK" | head -c 100 | sed 's/"/\\"/g')...",
    "estimated_burn": $ESTIMATED_BURN,
    "status": "started",
    "tokens_before": 0,
    "tokens_after": 0,
    "tokens_saved": 0,
    "percent_savings": 0
}

entries = json.loads(log_file.read_text()) if log_file.exists() else []
entries.append(entry)
log_file.write_text(json.dumps(entries, indent=2))
EOF

# Build message with context if provided
if [[ -n "$CONTEXT" && -f "$CONTEXT" ]]; then
 FULL_TASK="$TASK\\n\\nContext:\\n$(cat "$CONTEXT")"
else
 FULL_TASK="$TASK"
fi

# Output JSON for Agent Zero call_subordinate
cat << JSON_EOF
{
 "delegation": {
   "session_id": "$SESSION_ID",
   "profile": "$PROFILE",
   "estimated_burn": $ESTIMATED_BURN,
   "start_time": "$TIMESTAMP"
 },
 "agent_call": {
   "tool": "call_subordinate",
   "params": {
     "profile": "$PROFILE",
     "message": "$FULL_TASK",
     "reset": "true"
   }
 },
 "completion_instructions": "After subordinate completes, run: delegate_complete.sh '$SESSION_ID' <actual_tokens>",
 "token_tracker_info": "Session recorded in tokens.json with ID: $SESSION_ID"
}
JSON_EOF

# Update metrics files
cd "$PROJECT_DIR"
python3 << EOF
import json
from pathlib import Path
from datetime import datetime

metrics_json = Path("$PROJECT_DIR/metrics.json")
metrics_toon = Path("$PROJECT_DIR/metrics.toon")

stats = {"total_delegations": 0, "successful_delegations": 0, "failed_delegations": 0, "script_fallbacks": 0}
if metrics_json.exists():
    try:
        data = json.loads(metrics_json.read_text())
        stats.update(data.get("project_stats", {}))
    except: pass

stats["total_delegations"] += 1

now = datetime.now().isoformat() + "Z"
metrics_json.write_text(json.dumps({"project_stats": stats, "version": "0.5.0", "last_updated": now}, indent=2))

toon = f"""project_stats:
 total_delegations:{stats['total_delegations']}
 successful_delegations:{stats['successful_delegations']}
 failed_delegations:{stats['failed_delegations']}
 script_fallbacks:{stats['script_fallbacks']}
version: 0.5.0
last_updated: {now}"""
metrics_toon.write_text(toon)
print(f"Metrics updated: {stats['total_delegations']} total delegations")
EOF

exit 0
