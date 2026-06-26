#!/bin/bash
# PostToolUse hook: auto-log exec failures to feedback learning
# Usage: Add to hooks.PostToolUse for Bash matcher
# Reads $TOOL_EXIT_CODE and $TOOL_STDERR from hook environment

DIR="${FEEDBACK_LEARNING_DIR:-$HOME/.openclaw/shared/learning}"
AGENT="${AGENT_ID:-unknown}"

# Only trigger on non-zero exit codes
if [ "${TOOL_EXIT_CODE:-0}" = "0" ]; then
    exit 0
fi

STDERR="${TOOL_STDERR:-unknown error}"
# Truncate stderr to 200 chars
STDERR="${STDERR:0:200}"

CONTEXT="${TOOL_COMMAND:-exec command}"

# Log the error event
bash "$DIR/log-event.sh" "$AGENT" "error" "exec_fail" "$CONTEXT" "$STDERR" "Auto-captured exec failure"
