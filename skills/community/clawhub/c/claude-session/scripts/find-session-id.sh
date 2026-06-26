#!/usr/bin/env bash
# find-session-id.sh - Find current session ID by searching for a unique marker
#
# Usage:
#   find-session-id.sh                  # Generate a unique marker and print it
#   find-session-id.sh <marker>         # Search for marker in session files
#   find-session-id.sh <marker> <dir>   # Search with explicit project directory
#
# When called without arguments, generates and prints a unique marker.
# The caller should echo this marker (so it gets recorded in JSONL),
# then call this script again with the marker to find the session ID.

set -euo pipefail

CLAUDE_PROJECTS_DIR="$HOME/.claude/projects"

# Convert CWD to Claude Code project name
# Matches @claude-sessions/core pathToFolderName:
#   absolutePath.replace(/[^a-zA-Z0-9]/g, '-')
cwd_to_project_name() {
    local cwd="$1"
    cwd="${cwd%/}"
    # Replace all non-alphanumeric characters with '-'
    echo "$cwd" | sed 's/[^a-zA-Z0-9]/-/g'
}

MARKER="${1:-}"
if [[ -z "$MARKER" ]]; then
    # No marker provided — generate one and output it.
    # The caller must run the script again with this marker after it appears in JSONL.
    echo "SESSION_MARKER_$(date +%s)_$$"
    exit 0
fi

# Determine project directory
if [[ -n "${2:-}" ]]; then
    PROJECT_DIR="$2"
else
    PROJECT_NAME=$(cwd_to_project_name "$(pwd)")
    PROJECT_DIR="$CLAUDE_PROJECTS_DIR/$PROJECT_NAME"
fi

if [[ ! -d "$PROJECT_DIR" ]] && [[ -z "${2:-}" ]]; then
    # Fallback: walk up parent directories until a matching project is found
    SEARCH_DIR="$(pwd)"
    while [[ "$SEARCH_DIR" != "/" ]]; do
        SEARCH_DIR=$(dirname "$SEARCH_DIR")
        CANDIDATE="$CLAUDE_PROJECTS_DIR/$(cwd_to_project_name "$SEARCH_DIR")"
        if [[ -d "$CANDIDATE" ]]; then
            PROJECT_DIR="$CANDIDATE"
            break
        fi
    done
fi

if [[ ! -d "$PROJECT_DIR" ]]; then
    echo "ERROR: Project directory not found: $PROJECT_DIR" >&2
    if [[ -z "${2:-}" ]]; then
        echo "Searched from CWD upward to /" >&2
    fi
    exit 1
fi

# Search for the marker in session files (exclude sync-conflict files)
RESULT=$(grep -rl "$MARKER" "$PROJECT_DIR"/*.jsonl 2>/dev/null | grep -v 'sync-conflict' | head -1 || true)

if [[ -z "$RESULT" ]]; then
    echo "ERROR: No session file found containing marker: $MARKER" >&2
    exit 1
fi

# Extract session ID (UUID) from filename
SESSION_ID=$(basename "$RESULT" .jsonl)
echo "$SESSION_ID"
