#!/bin/bash
# Session Destroyer - script to delete the current Claude Code session

set -e

CLAUDE_DIR="$HOME/.claude"
BAK_DIR="$CLAUDE_DIR/.bak"
PROJECTS_DIR="$CLAUDE_DIR/projects"

# Create backup directory
mkdir -p "$BAK_DIR"

# Extract project folder name from current working directory
# Claude Code converts all non-alphanumeric characters to -
CURRENT_DIR="$(pwd)"
PROJECT_FOLDER=$(echo "$CURRENT_DIR" | sed 's/[^a-zA-Z0-9]/-/g')

# Find project session directory
SESSION_DIR="$PROJECTS_DIR/$PROJECT_FOLDER"

if [ ! -d "$SESSION_DIR" ]; then
    echo "Session directory not found: $SESSION_DIR"
    exit 1
fi

# Find the most recently modified session file
LATEST_SESSION=$(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -1)

if [ -z "$LATEST_SESSION" ]; then
    echo "No session files found."
    exit 1
fi

SESSION_ID=$(basename "$LATEST_SESSION" .jsonl)
BAK_FILENAME="${PROJECT_FOLDER}_${SESSION_ID}.jsonl"

echo "Deleting session..."
echo "  source: $LATEST_SESSION"
echo "  backup: $BAK_DIR/$BAK_FILENAME"

# Move session file to backup directory
mv "$LATEST_SESSION" "$BAK_DIR/$BAK_FILENAME"

echo "Session moved to backup directory."

# Detect VSCode/Cursor environment and restart Extension Host
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -n "$VSCODE_IPC_HOOK" ] || [ -n "$VSCODE_IPC_HOOK_CLI" ] || [ "$TERM_PROGRAM" = "vscode" ]; then
    echo "VSCode/Cursor environment detected. Restarting Extension Host..."
    bash "$SCRIPT_DIR/restart-extension-host.sh" || true
fi

echo "Done!"
