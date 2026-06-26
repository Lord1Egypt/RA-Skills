#!/bin/bash
#
# Frugal Orchestrator - Delegation Completion Handler
# Records completion metrics and updates token savings
#
# Usage: delegate_complete.sh <session_id> <actual_tokens_used>
#

set -uo pipefail

PROJECT_DIR="/a0/usr/projects/frugal_orchestrator"
LOGDIR="$PROJECT_DIR/logs"
TOKENS_FILE="$LOGDIR/tokens.json"

SESSION_ID="${1:-}"
ACTUAL_TOKENS="${2:-0}"
STATUS="${3:-completed}"

if [[ -z "$SESSION_ID" ]]; then
 echo '{"error": "Usage: delegate_complete.sh <session_id> <actual_tokens_used> [status]"}' >&2
 exit 1
fi

# Update tokens.json using Python for proper JSON manipulation
cd "$PROJECT_DIR"
python3 -- "$PROJECT_DIR/scripts/delegate_complete.py" "$@" "$STATUS"

exit $?
