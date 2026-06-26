#!/bin/bash

# Claude Code Usage Checker - Optimized
# Fast check of Claude Code quota via tmux

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SESSION_NAME="cu-$$"
SCRATCH_DIR=$(mktemp -d)

cleanup() {
    tmux kill-session -t "$SESSION_NAME" 2>/dev/null || true
    rm -rf "$SCRATCH_DIR"
}
trap cleanup EXIT

# Pre-flight checks
for cmd in tmux claude git; do
    if ! command -v "$cmd" &>/dev/null; then
        echo "❌ Required command not found: $cmd"
        exit 1
    fi
done

# Init git repo
cd "$SCRATCH_DIR"
git init -q

# Create tmux session
tmux new-session -d -s "$SESSION_NAME"

# Launch Claude Code
tmux send-keys -t "$SESSION_NAME" "cd $SCRATCH_DIR && claude" Enter

# Wait for trust prompt or ready (max 10s)
READY=false
for i in {1..20}; do
    sleep 0.5
    PANES=$(tmux capture-pane -t "$SESSION_NAME" -p 2>/dev/null || true)
    if echo "$PANES" | grep -q "trust this folder"; then
        tmux send-keys -t "$SESSION_NAME" "1"
        sleep 0.2
        tmux send-keys -t "$SESSION_NAME" Enter
        READY=true
        break
    fi
    if echo "$PANES" | grep -q "Welcome back"; then
        READY=true
        break
    fi
    if echo "$PANES" | grep -q "Please log in\|auth"; then
        echo "❌ Claude Code authentication expired. Run 'claude' manually to re-authenticate."
        exit 1
    fi
done

if [ "$READY" = false ]; then
    echo "❌ Claude Code failed to start within 10 seconds."
    exit 1
fi

# Wait for Claude to be ready
sleep 1.5

# Send /usage command
tmux send-keys -t "$SESSION_NAME" "/usage"
sleep 0.3
tmux send-keys -t "$SESSION_NAME" Enter

# Wait for usage screen
sleep 1.5

# Capture and parse output
OUTPUT=$(tmux capture-pane -t "$SESSION_NAME" -p)

# Display results
echo "=== Claude Code Usage ==="
echo "$OUTPUT" | grep -E "Opus.*Claude (Pro|Max)" | head -1 | sed 's/│//g; s/^[[:space:]]*/Plan: /; s/[[:space:]]*$//'
echo "$OUTPUT" | grep "% used" | sed 's/^[[:space:]]*/Usage: /'
echo "$OUTPUT" | grep "Resets" | sed 's/^[[:space:]]*/Reset: /'
