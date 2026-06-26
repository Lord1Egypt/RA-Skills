#!/bin/bash
# Update AI state tracking file
# Usage: ./update-state.sh <PID> <AI_TYPE> <WORKDIR> <TASK> <STATUS> <NOTES>

STATE_FILE="$HOME/.openclaw/skills/ai-mother/ai-state.txt"
TIMESTAMP=$(date +%s)

PID=$1
AI_TYPE=$2
WORKDIR=$3
TASK=$4
STATUS=$5
NOTES=$6

if [ -z "$PID" ] || [ -z "$STATUS" ]; then
    echo "Usage: $0 <PID> <AI_TYPE> <WORKDIR> <TASK> <STATUS> <NOTES>"
    exit 1
fi

# Create state file if not exists
[ ! -f "$STATE_FILE" ] && touch "$STATE_FILE"

# Remove old entry for this PID
grep -v "^$PID|" "$STATE_FILE" > "$STATE_FILE.tmp" 2>/dev/null || true
mv "$STATE_FILE.tmp" "$STATE_FILE"

# Add new entry
echo "$PID|$AI_TYPE|$WORKDIR|$TASK|$STATUS|$TIMESTAMP|$NOTES" >> "$STATE_FILE"

# Clean up dead processes (older than 24h)
CUTOFF=$((TIMESTAMP - 86400))
awk -F'|' -v cutoff="$CUTOFF" '$6 > cutoff' "$STATE_FILE" > "$STATE_FILE.tmp"
mv "$STATE_FILE.tmp" "$STATE_FILE"

# Also write to SQLite database for analytics
DB_SCRIPT="$HOME/.openclaw/skills/ai-mother/scripts/db.py"
if [ -f "$DB_SCRIPT" ]; then
    python3 - <<EOF 2>/dev/null
import sys
sys.path.insert(0, '$HOME/.openclaw/skills/ai-mother/scripts')
from db import init_db, update_agent
init_db()
update_agent($PID, '$AI_TYPE', '$WORKDIR', '$TASK', '$STATUS', '$NOTES')
EOF
fi
