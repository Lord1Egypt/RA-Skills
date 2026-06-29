#!/usr/bin/env bash
# resume-session.sh — Resume work from a previous session state file
# Usage: bash scripts/resume-session.sh <session-id>
#   <session-id> can be:
#     - Full filename: "2026-06-08-1134-genor-orchestrator-publish.md"
#     - Partial match: "publish" or "genor-orchestrator"
#     - "last" — most recent session
#     - "list" — show available sessions
#
# Outputs a structured resume brief that an LLM can use to continue work.
# Data is stored in $ORCHESTRATOR_DATA_DIR (default: ../../orchestrator-data/ from skill root)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${ORCHESTRATOR_DATA_DIR:-$(dirname "$(dirname "$SKILL_DIR")")/orchestrator-data}"
SESSIONS_DIR="$DATA_DIR/sessions"
SESSION_LOG="$DATA_DIR/session_log.md"

QUERY="${1:-}"

if [ -z "$QUERY" ] || [ "$QUERY" = "list" ]; then
    echo "━━━ Available Sessions ━━━"
    echo ""
    if [ -d "$SESSIONS_DIR" ] && [ "$(ls -A "$SESSIONS_DIR" 2>/dev/null)" ]; then
        ls -1t "$SESSIONS_DIR"/*.md 2>/dev/null | while read -r f; do
            name=$(basename "$f" .md)
            title=$(head -1 "$f" 2>/dev/null | sed 's/^# Session: //')
            echo "  $name"
            echo "    → $title"
        done
    else
        echo "  No session state files found."
    fi
    echo ""
    echo "Quick reference: $SESSION_LOG"
    echo ""
    echo "Usage: bash scripts/resume-session.sh <id>"
    echo "  <id> = filename, partial match, or 'last'"
    exit 0
fi

mkdir -p "$SESSIONS_DIR"

# Find the session file
SESSION_FILE=""

if [ "$QUERY" = "last" ]; then
    # Most recent session
    SESSION_FILE=$(ls -1t "$SESSIONS_DIR"/*.md 2>/dev/null | head -1 || true)
elif [ -f "$SESSIONS_DIR/$QUERY" ]; then
    SESSION_FILE="$SESSIONS_DIR/$QUERY"
elif [ -f "$SESSIONS_DIR/$QUERY.md" ]; then
    SESSION_FILE="$SESSIONS_DIR/$QUERY.md"
else
    # Partial match — find most recent match
    SESSION_FILE=$(ls -1t "$SESSIONS_DIR"/*.md 2>/dev/null | grep -i "$QUERY" | head -1 || true)
fi

if [ -z "$SESSION_FILE" ] || [ ! -f "$SESSION_FILE" ]; then
    echo "❌ No session found matching: $QUERY"
    echo "   Run 'bash scripts/resume-session.sh list' to see available sessions."
    exit 1
fi

SESSION_NAME=$(basename "$SESSION_FILE" .md)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  RESUME: $SESSION_NAME"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Output the full session state
cat "$SESSION_FILE"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  RESUME BRIEF END"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 To continue this work, the LLM should:"
echo "   1. Read the context above"
echo "   2. Check current state of referenced files"
echo "   3. Continue from the next steps"
echo ""
echo "Session file: $SESSION_FILE"