#!/bin/bash
# Orchestrix tmux Multi-Agent Session Starter (MCP Version)
# Purpose: Create 4 separate windows, each running a Claude Code agent
# Supports multi-repo: Each repo gets its own tmux session based on repository_id
#
# Pro/Team Feature: This script is only available for Pro and Team subscribers.

set -e

# Dynamically get project root directory (where .orchestrix-core is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORK_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Working directory: $WORK_DIR"

# ============================================
# Dynamic Session Naming (Multi-Repo Support)
# ============================================

# Try to read repository_id from core-config.yaml
CONFIG_FILE="$WORK_DIR/.orchestrix-core/core-config.yaml"
REPO_ID=""

if [ -f "$CONFIG_FILE" ]; then
    # Extract repository_id using grep and sed (POSIX compatible)
    REPO_ID=$(grep -E "^\s*repository_id:" "$CONFIG_FILE" 2>/dev/null | head -1 | sed "s/.*repository_id:[[:space:]]*['\"]*//" | sed "s/['\"].*//")

    # Clean up: remove quotes and whitespace
    REPO_ID=$(echo "$REPO_ID" | tr -d "'" | tr -d '"' | tr -d ' ')
fi

# Fallback: use directory name if repository_id is empty
if [ -z "$REPO_ID" ]; then
    REPO_ID=$(basename "$WORK_DIR")
    echo "Warning: No repository_id in config, using directory name: $REPO_ID"
fi

# Sanitize REPO_ID for tmux session name (alphanumeric, dash, underscore only)
REPO_ID=$(echo "$REPO_ID" | tr -cd 'a-zA-Z0-9_-')

# Sanitized REPO_ID must not be empty
if [ -z "$REPO_ID" ]; then
    REPO_ID="default"
    echo "⚠️  REPO_ID is empty after sanitization, using fallback: $REPO_ID"
fi

# Generate dynamic session name and log file
SESSION_NAME="orchestrix-${REPO_ID}"
# IMPORTANT: Must match handoff-detector.sh pattern: /tmp/${SESSION_NAME}-handoff.log
LOG_FILE="/tmp/${SESSION_NAME}-handoff.log"

echo "🏷️  Repository ID: $REPO_ID"
echo "📺 tmux Session: $SESSION_NAME"
echo "📝 Log file: $LOG_FILE"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
echo "❌ Error: tmux is not installed"
    echo "Please run: brew install tmux"
    exit 1
fi

# Check if cc command is available
if ! command -v cc &> /dev/null; then
    echo "❌ Error: cc command not available"
    echo "Please ensure Claude Code alias is configured: alias cc='claude'"
    exit 1
fi

# If session already exists, kill it first
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "⚠️  Session '$SESSION_NAME' already exists, closing..."
    tmux kill-session -t "$SESSION_NAME"
fi

# Create new session with first window (Architect)
echo "🚀 Creating tmux session: $SESSION_NAME"
tmux new-session -d -s "$SESSION_NAME" -n "Arch" -c "$WORK_DIR"

# ============================================
# Inject handoff-detector hook into target project
# ============================================
# CRITICAL: The tmux agents run Claude Code in WORK_DIR, so their Stop hooks
# come from WORK_DIR/.claude/settings*.json, NOT from the orchestrix-mcp-server project.
# We must inject the handoff-detector hook into the target project's settings.local.json
# so that agent Stop events trigger local handoff detection.
SETTINGS_LOCAL="$WORK_DIR/.claude/settings.local.json"
HANDOFF_HOOK_CMD="bash -c 'cd \"\$(git rev-parse --show-toplevel)\" && .orchestrix-core/scripts/handoff-detector.sh'"

# Ensure .claude directory exists
mkdir -p "$WORK_DIR/.claude"

# Check if settings.local.json already has handoff-detector configured
if [ -f "$SETTINGS_LOCAL" ]; then
    if grep -q "handoff-detector" "$SETTINGS_LOCAL" 2>/dev/null; then
        echo "✅ Handoff hook already configured in $SETTINGS_LOCAL"
    else
        echo "⚠️  settings.local.json exists but missing handoff hook, injecting..."
        # Use jq to merge if available, otherwise create new
        if command -v jq &>/dev/null; then
            EXISTING=$(cat "$SETTINGS_LOCAL")
            echo "$EXISTING" | jq --arg cmd "$HANDOFF_HOOK_CMD" \
                '.hooks.Stop = (.hooks.Stop // []) + [{"hooks": [{"type": "command", "command": $cmd}]}]' \
                > "$SETTINGS_LOCAL.tmp" && mv "$SETTINGS_LOCAL.tmp" "$SETTINGS_LOCAL"
            echo "✅ Handoff hook injected into existing settings.local.json"
        else
            echo "⚠️  jq not found, cannot safely merge. Please add handoff hook manually."
        fi
    fi
else
    # Create new settings.local.json with handoff hook
    cat > "$SETTINGS_LOCAL" << SETTINGS_EOF
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$HANDOFF_HOOK_CMD"
          }
        ]
      }
    ]
  }
}
SETTINGS_EOF
    echo "✅ Created $SETTINGS_LOCAL with handoff hook"
fi

# ============================================
# Ensure handoff-detector.sh exists in target project
# ============================================
HANDOFF_SCRIPT="$WORK_DIR/.orchestrix-core/scripts/handoff-detector.sh"
if [ ! -f "$HANDOFF_SCRIPT" ]; then
    SCRIPT_DIR_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -f "$SCRIPT_DIR_SRC/handoff-detector.sh" ]; then
        mkdir -p "$(dirname "$HANDOFF_SCRIPT")"
        cp "$SCRIPT_DIR_SRC/handoff-detector.sh" "$HANDOFF_SCRIPT"
        chmod +x "$HANDOFF_SCRIPT"
        echo "✅ Copied handoff-detector.sh to target project"
    else
        echo "⚠️  handoff-detector.sh not found in setup directory"
    fi
fi

# ============================================
# Create tmux automation marker
# ============================================
# This file signals to agents that they're running in tmux automation mode
# Agents check for this file to decide whether to register pending-handoff fallback
RUNTIME_DIR="$WORK_DIR/.orchestrix-core/runtime"
TMUX_MARKER="$RUNTIME_DIR/tmux-automation-active"

mkdir -p "$RUNTIME_DIR"
echo "{\"session\": \"$SESSION_NAME\", \"started_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > "$TMUX_MARKER"
echo "📌 tmux automation marker: $TMUX_MARKER"

# Cleanup marker file on script exit (detach, kill, Ctrl+C)
cleanup() {
    rm -f "$TMUX_MARKER"
    echo "🧹 Cleaned up tmux automation marker"
}
trap cleanup EXIT INT TERM

# Configure status bar for better display
tmux set-option -t "$SESSION_NAME" status-left-length 20
tmux set-option -t "$SESSION_NAME" status-right-length 60
tmux set-option -t "$SESSION_NAME" window-status-format "#I:#W"
tmux set-option -t "$SESSION_NAME" window-status-current-format "#I:#W*"

# Set environment variables for Architect window
# ORCHESTRIX_SESSION and ORCHESTRIX_LOG are used by handoff-detector.sh
tmux send-keys -t "$SESSION_NAME:0" "export AGENT_ID=architect" C-m
tmux send-keys -t "$SESSION_NAME:0" "export ORCHESTRIX_SESSION=$SESSION_NAME" C-m
tmux send-keys -t "$SESSION_NAME:0" "export ORCHESTRIX_LOG=$LOG_FILE" C-m
tmux send-keys -t "$SESSION_NAME:0" "clear" C-m
tmux send-keys -t "$SESSION_NAME:0" "echo '╔════════════════════════════════════════╗'" C-m
tmux send-keys -t "$SESSION_NAME:0" "echo '║  🏛️  Architect Agent (Window 0)      ║'" C-m
tmux send-keys -t "$SESSION_NAME:0" "echo '╚════════════════════════════════════════╝'" C-m
tmux send-keys -t "$SESSION_NAME:0" "echo ''" C-m

# Create window 1 - SM
tmux new-window -t "$SESSION_NAME:1" -n "SM" -c "$WORK_DIR"
tmux send-keys -t "$SESSION_NAME:1" "export AGENT_ID=sm" C-m
tmux send-keys -t "$SESSION_NAME:1" "export ORCHESTRIX_SESSION=$SESSION_NAME" C-m
tmux send-keys -t "$SESSION_NAME:1" "export ORCHESTRIX_LOG=$LOG_FILE" C-m
tmux send-keys -t "$SESSION_NAME:1" "clear" C-m
tmux send-keys -t "$SESSION_NAME:1" "echo '╔════════════════════════════════════════╗'" C-m
tmux send-keys -t "$SESSION_NAME:1" "echo '║  📋 SM Agent (Window 1)               ║'" C-m
tmux send-keys -t "$SESSION_NAME:1" "echo '╚════════════════════════════════════════╝'" C-m
tmux send-keys -t "$SESSION_NAME:1" "echo ''" C-m

# Create window 2 - Dev
tmux new-window -t "$SESSION_NAME:2" -n "Dev" -c "$WORK_DIR"
tmux send-keys -t "$SESSION_NAME:2" "export AGENT_ID=dev" C-m
tmux send-keys -t "$SESSION_NAME:2" "export ORCHESTRIX_SESSION=$SESSION_NAME" C-m
tmux send-keys -t "$SESSION_NAME:2" "export ORCHESTRIX_LOG=$LOG_FILE" C-m
tmux send-keys -t "$SESSION_NAME:2" "clear" C-m
tmux send-keys -t "$SESSION_NAME:2" "echo '╔════════════════════════════════════════╗'" C-m
tmux send-keys -t "$SESSION_NAME:2" "echo '║  💻 Dev Agent (Window 2)              ║'" C-m
tmux send-keys -t "$SESSION_NAME:2" "echo '╚════════════════════════════════════════╝'" C-m
tmux send-keys -t "$SESSION_NAME:2" "echo ''" C-m

# Create window 3 - QA
tmux new-window -t "$SESSION_NAME:3" -n "QA" -c "$WORK_DIR"
tmux send-keys -t "$SESSION_NAME:3" "export AGENT_ID=qa" C-m
tmux send-keys -t "$SESSION_NAME:3" "export ORCHESTRIX_SESSION=$SESSION_NAME" C-m
tmux send-keys -t "$SESSION_NAME:3" "export ORCHESTRIX_LOG=$LOG_FILE" C-m
tmux send-keys -t "$SESSION_NAME:3" "clear" C-m
tmux send-keys -t "$SESSION_NAME:3" "echo '╔════════════════════════════════════════╗'" C-m
tmux send-keys -t "$SESSION_NAME:3" "echo '║  🧪 QA Agent (Window 3)               ║'" C-m
tmux send-keys -t "$SESSION_NAME:3" "echo '╚════════════════════════════════════════╝'" C-m
tmux send-keys -t "$SESSION_NAME:3" "echo ''" C-m

# ============================================
# Configuration
# ============================================

# Wait time for Claude Code to start (seconds)
CC_STARTUP_WAIT=12

# Wait time between command text and Enter key (seconds)
COMMAND_ENTER_DELAY=1

# Wait time between activating agents (seconds)
AGENT_ACTIVATION_DELAY=2

# Wait time for agents to fully load before starting workflow (seconds)
AGENT_LOAD_WAIT=15

# Auto-start workflow command (sent to SM window)
AUTO_START_COMMAND="1"

# Agent activation commands (MCP version uses /o command)
declare -a AGENT_COMMANDS=(
    "/o architect"   # Window 0 - Architect
    "/o sm"          # Window 1 - SM
    "/o dev"         # Window 2 - Dev
    "/o qa"          # Window 3 - QA
)

declare -a AGENT_NAMES=(
    "Architect"
    "SM"
    "Dev"
    "QA"
)

# ============================================
# Function: Send command with delay before Enter
# Usage: send_command_with_delay <window> <command>
# ============================================
send_command_with_delay() {
    local window="$1"
    local command="$2"

    # Send command text first
    tmux send-keys -t "$SESSION_NAME:$window" "$command"

    # Wait before sending Enter (prevents race condition)
    sleep "$COMMAND_ENTER_DELAY"

    # Send Enter key
    tmux send-keys -t "$SESSION_NAME:$window" "Enter"
}

# ============================================
# Start Claude Code in all windows
# ============================================

echo "🤖 Starting Claude Code in all windows..."

# Window 0 - Architect
tmux send-keys -t "$SESSION_NAME:0" "cc" C-m

# Window 1 - SM
tmux send-keys -t "$SESSION_NAME:1" "cc" C-m

# Window 2 - Dev
tmux send-keys -t "$SESSION_NAME:2" "cc" C-m

# Window 3 - QA
tmux send-keys -t "$SESSION_NAME:3" "cc" C-m

# ============================================
# Wait for Claude Code to fully initialize
# ============================================

echo ""
echo "⏳ Waiting ${CC_STARTUP_WAIT}s for Claude Code to start..."
echo ""

# Countdown + auto-accept trust dialogs in all windows.
# Claude Code shows "Do you trust" when entering a new project directory.
# We detect it and send Enter to accept. Checked every 2 seconds.
TRUST_HANDLED=""
for i in $(seq "$CC_STARTUP_WAIT" -1 1); do
    printf "\r   %2d seconds remaining..." "$i"
    sleep 1

    # Check every 2 seconds for trust dialog in any window
    if [ $((i % 2)) -eq 0 ] && [ -z "$TRUST_HANDLED" ]; then
        for w in 0 1 2 3; do
            PANE=$(tmux capture-pane -t "$SESSION_NAME:$w" -p -S -10 2>/dev/null || true)
            if echo "$PANE" | grep -qi "trust this folder\|safety check"; then
                tmux send-keys -t "$SESSION_NAME:$w" Enter
                echo ""
                echo "   🔓 Auto-accepted trust dialog in window $w"
            fi
        done
        # Check if any window has ❯ (past trust dialog)
        PANE0=$(tmux capture-pane -t "$SESSION_NAME:0" -p -S -5 2>/dev/null || true)
        if echo "$PANE0" | grep -q "❯"; then
            TRUST_HANDLED="yes"
        fi
    fi
done
printf "\r   ✓ Claude Code should be ready now!      \n"
echo ""

# ============================================
# Auto-activate agents in each window
# ============================================

echo "🚀 Auto-activating agents..."
echo ""

for window in 0 1 2 3; do
    agent_name="${AGENT_NAMES[$window]}"
    agent_cmd="${AGENT_COMMANDS[$window]}"

    echo "   [Window $window] Activating $agent_name..."
    send_command_with_delay "$window" "$agent_cmd"

    # Wait before activating next agent (avoid overwhelming the system)
    if [ "$window" -lt 3 ]; then
        sleep "$AGENT_ACTIVATION_DELAY"
    fi
done

echo ""
echo "✅ All agents activated!"

# ============================================
# Wait for agents to fully load
# ============================================

echo ""
echo "⏳ Waiting ${AGENT_LOAD_WAIT}s for agents to load..."
echo ""

for i in $(seq "$AGENT_LOAD_WAIT" -1 1); do
    printf "\r   %2d seconds remaining..." "$i"
    sleep 1
done
printf "\r   ✓ Agents should be ready now!           \n"

# ============================================
# Auto-start workflow in SM window
# ============================================

echo ""
echo "🎬 Starting workflow in SM window..."
send_command_with_delay "1" "$AUTO_START_COMMAND"

# Select SM window (window 1) as starting point
tmux select-window -t "$SESSION_NAME:1"

# Display startup completion message
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ Orchestrix automation started!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "📋 Window Layout:"
echo "  Window 0: 🏛️  Architect"
echo "  Window 1: 📋 SM (current window) ← workflow started"
echo "  Window 2: 💻 Dev"
echo "  Window 3: 🧪 QA"
echo ""
echo "⌨️  tmux navigation:"
echo "  Ctrl+b → 0/1/2/3   Jump to window"
echo "  Ctrl+b → n/p       Next/Previous window"
echo "  Ctrl+b → d         Detach (runs in background)"
echo "  Ctrl+b → [         Scroll mode (q to exit)"
echo ""
echo "📝 Monitor: tail -f $LOG_FILE"
echo "📝 Reconnect: tmux attach -t $SESSION_NAME"
echo ""

# Attach to session
tmux attach-session -t "$SESSION_NAME"
