#!/bin/bash
# Single Mode - Run a single Claude Code task with callback
# Usage: single.sh --task <prompt> --project <path> [--permission-mode plan|auto] [--callback <type>]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# Default values
TASK=""
PROJECT_DIR=""
PERMISSION_MODE="auto"
CALLBACK="openclaw"
SESSION_KEY=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --task)
            TASK="$2"
            shift 2
            ;;
        --project)
            PROJECT_DIR="$2"
            shift 2
            ;;
        --permission-mode)
            PERMISSION_MODE="$2"
            shift 2
            ;;
        --callback)
            CALLBACK="$2"
            shift 2
            ;;
        --session-key)
            SESSION_KEY="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Validate required arguments
if [[ -z "$TASK" ]]; then
    echo "Error: --task is required"
    exit 1
fi

if [[ -z "$PROJECT_DIR" ]]; then
    echo "Error: --project is required"
    exit 1
fi

if [[ -z "$SESSION_KEY" ]]; then
    echo "Error: --session-key is required"
    exit 1
fi

# Validate permission mode
if [[ "$PERMISSION_MODE" != "plan" && "$PERMISSION_MODE" != "auto" ]]; then
    echo "Error: --permission-mode must be 'plan' or 'auto'"
    exit 1
fi

# Expand ~ to home directory
PROJECT_DIR="${PROJECT_DIR/#\~/$HOME}"

if [[ ! -d "$PROJECT_DIR" ]]; then
    echo "Error: Project directory does not exist: $PROJECT_DIR"
    exit 1
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}ℹ${NC} $*"
}

log_success() {
    echo -e "${GREEN}✅${NC} $*"
}

log_error() {
    echo -e "${RED}❌${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}⚠️${NC} $*"
}

# Build task with completion protocol
# We ask Claude to output a marker when done, then we detect it and trigger callback
TASK_WITH_CALLBACK="$TASK

⚠️ COMPLETION PROTOCOL (MUST FOLLOW):
After you complete the requested task, you MUST output exactly the following marker on its own line:

CC_CALLBACK_DONE

This marker is required for automated callback detection. Do not skip it for any reason, including simple queries or non-coding tasks."

log_info "Starting Single mode..."
log_info "Project: $PROJECT_DIR"
log_info "Permission mode: $PERMISSION_MODE"

if [[ "$PERMISSION_MODE" == "auto" ]]; then
    log_warn "⚠️  Auto mode uses --dangerously-skip-permissions"
    log_warn "   Claude Code will run all tools without confirmation"
    log_warn "   Only use in trusted environments with version-controlled code"
fi

# Run Claude Code in non-interactive mode
cd "$PROJECT_DIR"

# Clean up team hooks that may interfere with single mode
# 1. Delete on-stop.sh file
# 2. Clean up settings.json entries that reference on-stop.sh
HOOKS_DIR="$PROJECT_DIR/.claude/hooks"
SETTINGS_FILE="$PROJECT_DIR/.claude/settings.json"

# Remove on-stop.sh hook file
rm -f "$HOOKS_DIR/on-stop.sh"
log_info "Removed team hook file (on-stop.sh)"

# Clean up settings.json - remove any hook entries that reference on-stop.sh
if [ -f "$SETTINGS_FILE" ]; then
    if command -v jq &> /dev/null; then
        # Check if on-stop.sh reference exists
        if jq -e '.. | objects | select(.command? == ".claude/hooks/on-stop.sh")' "$SETTINGS_FILE" > /dev/null 2>&1; then
            # Clean up Stop hooks array by filtering out on-stop.sh references
            if jq '.hooks.Stop |= (map(.hooks |= map(select(.command != ".claude/hooks/on-stop.sh"))))' "$SETTINGS_FILE" > "$SETTINGS_FILE.tmp"; then
                mv "$SETTINGS_FILE.tmp" "$SETTINGS_FILE"
                log_success "Removed on-stop.sh references from settings.json"
            else
                log_warn "Failed to update settings.json, keeping original"
                rm -f "$SETTINGS_FILE.tmp"
            fi
        else
            log_info "No on-stop.sh references found in settings.json"
        fi
    else
        log_warn "jq not available, skipping settings.json cleanup"
    fi
fi

log_info "Running Claude Code..."

# Map permission modes to Claude Code values
# Note: We use --dangerously-skip-permissions directly for auto mode to avoid confirmation prompt
case "$PERMISSION_MODE" in
    plan)
        CLAUDE_CMD="claude -p --permission-mode plan"
        ;;
    auto)
        CLAUDE_CMD="claude -p --dangerously-skip-permissions"
        ;;
    *)
        echo "Error: --permission-mode must be 'plan' or 'auto'"
        exit 1
        ;;
esac

# Run in background mode (default)
log_info "Running in background mode..."

# Create a wrapper script that runs Claude and monitors for completion
(
    OUTPUT=$($CLAUDE_CMD "$TASK_WITH_CALLBACK" 2>&1) || EXIT_CODE=$?
    
    if grep -q "CC_CALLBACK_DONE" <<< "$OUTPUT"; then
        TASK_OUTPUT=$(echo "$OUTPUT" | sed -n '1,/CC_CALLBACK_DONE/p' | sed '$d')
        "$BASE_DIR/callbacks/$CALLBACK.sh" \
            --status done \
            --mode single \
            --task "a single task" \
            --message "$TASK" \
            --output "$TASK_OUTPUT" \
            --session-key "$SESSION_KEY"
    else
        "$BASE_DIR/callbacks/$CALLBACK.sh" \
            --status error \
            --mode single \
            --task "a single task" \
            --message "$TASK" \
            --output "CC_CALLBACK_DONE marker not found. Original output:\n${OUTPUT}" \
            --session-key "$SESSION_KEY"
    fi
) &

BACKGROUND_PID=$!
echo "Background process started (PID: $BACKGROUND_PID)"
log_success "Task started in background. Callback will notify on completion."
exit 0
