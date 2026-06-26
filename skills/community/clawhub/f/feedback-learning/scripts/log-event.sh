#!/bin/bash
# log-event.sh — append a learning event to events.jsonl
# Usage: log-event.sh <agent> <type> <source> <context> <signal> [hint]
# Types: error, correction, positive, pattern, requery
# Sources: exec_fail, user_nlp, user_emoji, requery, auto

EVENTS_FILE="$HOME/.openclaw/shared/learning/events.jsonl"

AGENT="${1:?agent required}"
TYPE="${2:?type required}"    # error|correction|positive|pattern|requery
SOURCE="${3:?source required}" # exec_fail|user_nlp|user_emoji|requery|auto
CONTEXT="${4:?context required}"
SIGNAL="${5:?signal required}"
HINT="${6:-}"

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Escape JSON strings
json_escape() {
  python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$1"
}

AGENT_J=$(json_escape "$AGENT")
TYPE_J=$(json_escape "$TYPE")
SOURCE_J=$(json_escape "$SOURCE")
CONTEXT_J=$(json_escape "$CONTEXT")
SIGNAL_J=$(json_escape "$SIGNAL")
HINT_J=$(json_escape "$HINT")

echo "{\"ts\":\"$TS\",\"agent\":$AGENT_J,\"type\":$TYPE_J,\"source\":$SOURCE_J,\"context\":$CONTEXT_J,\"signal\":$SIGNAL_J,\"hint\":$HINT_J,\"heat\":1}" >> "$EVENTS_FILE"
