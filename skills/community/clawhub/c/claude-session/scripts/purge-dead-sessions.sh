#!/bin/bash
# Purge Dead Sessions - permanently delete empty/hook-only sessions with no assistant responses
#
# Usage:
#   purge-dead-sessions.sh <project_name>          # Print targets (dry-run)
#   purge-dead-sessions.sh <project_name> --delete  # Actually delete
#
# Criteria: 10 lines or fewer AND no "type":"assistant"

set -e

CLAUDE_DIR="$HOME/.claude"
PROJECTS_DIR="$CLAUDE_DIR/projects"

PROJECT_NAME="${1:?Usage: purge-dead-sessions.sh <project_name> [--delete]}"
DELETE_FLAG="$2"

if [[ "$PROJECT_NAME" == *".."* || "$PROJECT_NAME" == *"/"* ]]; then
    echo "ERROR: invalid project name (must not contain '..' or '/')" >&2
    exit 1
fi

SESSION_DIR="$PROJECTS_DIR/$PROJECT_NAME"

if [ ! -d "$SESSION_DIR" ]; then
    echo "ERROR: project directory not found: $SESSION_DIR" >&2
    exit 1
fi

count=0
deleted=0

for f in "$SESSION_DIR"/*.jsonl; do
    [ -f "$f" ] || continue
    lines=$(wc -l < "$f")
    if [ "$lines" -le 10 ]; then
        has_assistant=$(grep -cE '"type"\s*:\s*"assistant"' "$f" 2>/dev/null || true)
        if [ "$has_assistant" -eq 0 ]; then
            session_id=$(basename "$f" .jsonl)
            count=$((count + 1))
            if [ "$DELETE_FLAG" = "--delete" ]; then
                rm "$f"
                echo "deleted: $session_id  ($lines lines)"
                deleted=$((deleted + 1))
            else
                echo "dead: $session_id  ($lines lines)"
            fi
        fi
    fi
done

if [ "$DELETE_FLAG" = "--delete" ]; then
    echo "---"
    echo "Deleted: ${deleted} sessions"
else
    echo "---"
    echo "Found: ${count} dead sessions (add --delete to remove)"
fi
