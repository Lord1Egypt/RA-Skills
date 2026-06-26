#!/bin/bash
# log-event.sh v2 — append a learning event to events.jsonl
# Configurable via $FEEDBACK_LEARNING_DIR (default: ~/.openclaw/shared/learning)
# Deduplicates via content hash to prevent duplicate entries.
#
# Usage: log-event.sh <agent> <type> <source> <context> <signal> [hint]
# Types:   error | correction | positive | requery
# Sources: exec_fail | user_nlp | user_emoji | requery | auto

DIR="${FEEDBACK_LEARNING_DIR:-$HOME/.openclaw/shared/learning}"
EVENTS_FILE="$DIR/events.jsonl"

AGENT="${1:?agent required}"
TYPE="${2:?type required}"
SOURCE="${3:?source required}"
CONTEXT="${4:?context required}"
SIGNAL="${5:?signal required}"
HINT="${6:-}"

# Ensure directory exists
mkdir -p "$DIR"

TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# JSON-safe escaping via Python
json_escape() {
  python3 -c "import json,sys; print(json.dumps(sys.argv[1]))" "$1"
}

AGENT_J=$(json_escape "$AGENT")
TYPE_J=$(json_escape "$TYPE")
SOURCE_J=$(json_escape "$SOURCE")
CONTEXT_J=$(json_escape "$CONTEXT")
SIGNAL_J=$(json_escape "$SIGNAL")
HINT_J=$(json_escape "$HINT")

# Content hash for deduplication (type+source+signal+hint, excluding timestamp)
HASH=$(python3 -c "
import hashlib, sys
content = '|'.join(sys.argv[1:])
print(hashlib.sha256(content.encode()).hexdigest()[:8])
" "$TYPE" "$SOURCE" "$SIGNAL" "$HINT")

# Check for recent duplicate (same hash in last 1h)
if [ -f "$EVENTS_FILE" ] && [ -s "$EVENTS_FILE" ]; then
  CUTOFF=$(date -u -v-1H +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d '1 hour ago' +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || echo "")
  if [ -n "$CUTOFF" ]; then
    DUPE=$(python3 -c "
import json, sys
events_file, hash_id, cutoff = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    with open(events_file) as f:
        for line in f:
            try:
                ev = json.loads(line.strip())
                if ev.get('id') == hash_id and ev.get('ts', '') >= cutoff:
                    print('1')
                    break
            except: pass
except: pass
" "$EVENTS_FILE" "$HASH" "$CUTOFF")
    if [ "$DUPE" = "1" ]; then
      echo "[log-event] Duplicate skipped (hash=$HASH)" >&2
      exit 0
    fi
  fi
fi

LINE="{\"ts\":\"$TS\",\"id\":\"$HASH\",\"agent\":$AGENT_J,\"type\":$TYPE_J,\"source\":$SOURCE_J,\"context\":$CONTEXT_J,\"signal\":$SIGNAL_J,\"hint\":$HINT_J,\"heat\":1}"
echo "$LINE" >> "$EVENTS_FILE"
