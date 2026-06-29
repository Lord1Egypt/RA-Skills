#!/usr/bin/env bash
# log-session.sh — Log a session run with full state for cross-session resume
# Usage: bash scripts/log-session.sh <project> <task> <model> <status> [notes] [agent] [duration] [qa_done] [checked]
#
# Writes:
#   session_log.md          — Quick reference table (append)
#   sessions/YYYY-MM-DD-HHMM-<project-slug>-<task-slug>.md  — Full session state
#   projects/<project>/sessions.json — Project-specific session tracking
#
# Data is stored in $ORCHESTRATOR_DATA_DIR (default: ../../orchestrator-data/ from skill root)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${ORCHESTRATOR_DATA_DIR:-$(dirname "$(dirname "$SKILL_DIR")")/orchestrator-data}"
SESSION_LOG="$DATA_DIR/session_log.md"
SESSIONS_DIR="$DATA_DIR/sessions"
PROJECTS_DIR="$DATA_DIR/projects"

PROJECT="${1:-}"
TASK="${2:-}"
MODEL="${3:-}"
STATUS="${4:-}"
NOTES="${5:-}"
AGENT="${6:-shell}"
DURATION="${7:-}"
QA_DONE="${8:-false}"
CHECKED="${9:-false}"

# Initialize optional context variables
CONTEXT=""
CONTEXT_FILE=""

# Parse optional flags
shift 9 2>/dev/null || true
while [ $# -gt 0 ]; do
    case "$1" in
        --context) CONTEXT="$2"; shift 2 ;;
        --context-file) CONTEXT_FILE="$2"; shift 2 ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

if [ -z "$PROJECT" ] || [ -z "$TASK" ]; then
    echo "Usage: bash scripts/log-session.sh <project> <task> <model> <status> [notes] [agent] [duration] [qa_done] [checked]"
    echo ""
    echo "Arguments:"
    echo "  project   - Project name (for slug)"
    echo "  task      - Task description"
    echo "  model     - Model used (e.g., deepseek-v4-flash)"
    echo "  status    - complete|partial|failed|blocked"
    echo "  notes     - Optional notes"
    echo "  agent     - Agent type: subagent|cursor|acp|shell (default: shell)"
    echo "  duration  - Duration in minutes (optional)"
    echo "  qa_done   - true|false (optional)"
    echo "  checked   - true|false (optional)"
    echo ""
    echo "Examples:"
    echo "  bash scripts/log-session.sh myproject \"Fix bug #123\" deepseek-v4-flash complete \"Fixed in PR #45\""
    echo "  bash scripts/log-session.sh myproject \"Code review\" big-pickle partial \"Waiting on feedback\" subagent"
    exit 1
fi

mkdir -p "$DATA_DIR" "$SESSIONS_DIR" "$PROJECTS_DIR/$PROJECT"

TIMESTAMP=$(date -Iseconds)
DATE_STAMP=$(date '+%Y-%m-%d')
TIME_STAMP=$(date '+%H%M')

# Build filesystem-safe slugs (no spaces, no special chars)
slugify() { echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//'; }
PROJECT_SLUG=$(slugify "$PROJECT")
TASK_SLUG=$(slugify "$TASK")
SESSION_FILE="$SESSIONS_DIR/$DATE_STAMP-$TIME_STAMP-$PROJECT_SLUG-$TASK_SLUG.md"

# Escape pipe characters for markdown table safety
TABLE_TASK=$(echo "$TASK" | sed 's/|/\\|/g')
TABLE_NOTES=$(echo "$NOTES" | sed 's/|/\\|/g')

EMOJI=""
case "$STATUS" in
    complete) EMOJI="✅" ;;  failed) EMOJI="❌" ;;  partial) EMOJI="⚠️" ;;  blocked) EMOJI="🚫" ;;
    *) EMOJI="❓" ;;
esac

# --- Quick reference (session_log.md) ---
if [ ! -f "$SESSION_LOG" ]; then
    cat > "$SESSION_LOG" << 'EOF'
# Session Log
*Auto-generated session tracking for all orchestrated work*

| Date | Project | Task | Model | Agent | Status | Duration | QA | Checked | Notes |
|------|---------|------|-------|-------|--------|----------|----|---------|-------|
EOF
fi
echo "| $TIMESTAMP | $PROJECT | $TABLE_TASK | $MODEL | $AGENT | $EMOJI $STATUS | ${DURATION}m | $QA_DONE | $CHECKED | $TABLE_NOTES |" >> "$SESSION_LOG"

# --- Project-specific sessions.json ---
mkdir -p "$PROJECTS_DIR/$PROJECT"
if [ ! -f "$PROJECTS_DIR/$PROJECT/sessions.json" ]; then
    echo '{"sessions": []}' > "$PROJECTS_DIR/$PROJECT/sessions.json"
fi

# Add session entry to project sessions.json
python3 -c "
import json
import sys
with open('$PROJECTS_DIR/$PROJECT/sessions.json', 'r') as f:
    data = json.load(f)
data['sessions'].append({
    'timestamp': '$TIMESTAMP',
    'task': '$TASK',
    'model': '$MODEL',
    'agent': '$AGENT',
    'status': '$STATUS',
    'duration_minutes': '$DURATION' if '$DURATION' else None,
    'qa_done': '$QA_DONE' == 'true',
    'checked': '$CHECKED' == 'true',
    'notes': '$NOTES'
})
with open('$PROJECTS_DIR/$PROJECT/sessions.json', 'w') as f:
    json.dump(data, f, indent=2)
"

# --- Detailed session state ---
{
    echo "# Session: $PROJECT / $TASK"
    echo ""
    echo "- **Date:** $TIMESTAMP"
    echo "- **Model:** $MODEL"
    echo "- **Agent:** $AGENT"
    echo "- **Status:** $EMOJI $STATUS"
    echo "- **QA Done:** $QA_DONE"
    echo "- **Checked:** $CHECKED"
    if [ -n "$DURATION" ]; then echo "- **Duration:** ${DURATION}m"; fi
    echo "- **Session file:** $SESSION_FILE"
    echo ""
    echo "## Task"
    echo "$TASK"
    echo ""
    echo "## Notes"
    echo "$NOTES"
    echo ""

    if [ -n "$CONTEXT_FILE" ] && [ -f "$CONTEXT_FILE" ]; then
        echo "## Context"
        echo ""
        cat "$CONTEXT_FILE"
        echo ""
    elif [ -n "$CONTEXT" ]; then
        echo "## Context"
        echo ""
        echo "$CONTEXT"
        echo ""
    fi
} > "$SESSION_FILE"

echo "✅ Session logged: $PROJECT / $TASK [$STATUS]"
echo "   Agent: $AGENT | QA: $QA_DONE | Checked: $CHECKED"
echo "   State: $SESSION_FILE"
echo "   Project data: $PROJECTS_DIR/$PROJECT/sessions.json"