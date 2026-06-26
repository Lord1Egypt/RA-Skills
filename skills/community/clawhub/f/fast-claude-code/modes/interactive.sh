#!/bin/bash
# Interactive Mode - Start an interactive Claude Code session with tmux
# Usage: interactive.sh --project <path> [--label <name>] [--permission-mode plan|auto] [--task <prompt>] [--callback <type>]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# Default values
PROJECT_DIR=""
LABEL="interactive-$(date +%s)"
PERMISSION_MODE="auto"
TASK=""
CALLBACK="openclaw"
SESSION_KEY=""
SESSION_TIMEOUT=10800  # 3 hours in seconds

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --project)
            PROJECT_DIR="$2"
            shift 2
            ;;
        --label)
            LABEL="$2"
            shift 2
            ;;
        --permission-mode)
            PERMISSION_MODE="$2"
            shift 2
            ;;
        --task)
            TASK="$2"
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

# Check tmux
if ! command -v tmux &> /dev/null; then
    echo "Error: tmux is required for Interactive mode"
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

log_warn() {
    echo -e "${YELLOW}⚠️${NC} $*"
}

# Check if there's already a session for this project directory
EXISTING_SESSION=""
for session in $(tmux -L cc list-sessions -F "#{session_name}" 2>/dev/null | grep "^cc-"); do
    SESSION_CWD=$(tmux -L cc display-message -p -t "$session:#{pane_start_path}" 2>/dev/null || echo "")
    if [[ "$SESSION_CWD" == "$PROJECT_DIR" ]]; then
        EXISTING_SESSION="$session"
        break
    fi
done

if [[ -n "$EXISTING_SESSION" ]]; then
    SESSION="$EXISTING_SESSION"
    log_info "Reusing existing session for this project: $SESSION"
else
    SESSION="cc-${LABEL}"
    log_info "Creating new session: $SESSION"
fi

log_info "Project: $PROJECT_DIR"
log_info "Permission mode: $PERMISSION_MODE"

if [[ "$PERMISSION_MODE" == "auto" ]]; then
    log_warn "⚠️  Auto mode uses --dangerously-skip-permissions"
fi

if [[ -n "$TASK" ]]; then
    log_info "Initial task provided"
fi

log_info ""
log_info "How it works:"
log_info "  1. Claude Code runs in tmux session (detached)"
log_info "  2. Background monitor watches for CC_CALLBACK_DONE"
log_info "  3. When detected, callback is triggered automatically"
log_info "  4. Same project directory = reuse session"
log_info "  5. Different project directory = create new session"
log_info ""
log_info "Completion detection:"
log_info "  - Auto: Claude outputs CC_CALLBACK_DONE when done"
log_info "  - Manual: Type TASK_COMPLETE to trigger callback"
log_info ""

# Only create new session if not reusing
if [[ "$EXISTING_SESSION" == "" ]]; then
    # Kill existing session with same label if any
    tmux -L cc kill-session -t "$SESSION" 2>/dev/null || true

    # Create tmux session
    tmux -L cc new-session -d -s "$SESSION" -c "$PROJECT_DIR"
    sleep 0.5
else
    log_info "Attaching to existing session, skipping creation..."
    # Check if session is actually running Claude
    OUTPUT=$(tmux -L cc capture-pane -p -t "$SESSION" 2>/dev/null || echo "")
    if ! grep -q "claude" <<< "$OUTPUT"; then
        log_info "Session exists but Claude not running, starting Claude..."
        tmux -L cc send-keys -t "$SESSION" "cd $PROJECT_DIR" Enter
        sleep 0.5
    fi
fi

# Build claude command
if [[ "$PERMISSION_MODE" == "auto" ]]; then
    CLAUDE_CMD="claude --dangerously-skip-permissions"
else
    CLAUDE_CMD="claude --permission-mode $PERMISSION_MODE"
fi

# Start claude in interactive mode
tmux -L cc send-keys -t "$SESSION" "$CLAUDE_CMD" Enter
sleep 4

# Auto-accept the dangerous permissions warning if using auto mode
if [[ "$PERMISSION_MODE" == "auto" ]]; then
    # Check if the warning is displayed
    OUTPUT=$(tmux -L cc capture-pane -p -t "$SESSION" 2>/dev/null || echo "")
    if grep -q "Yes, I accept" <<< "$OUTPUT"; then
        log_info "Auto-accepting dangerous permissions warning..."
        # Send "2" to select "Yes, I accept", then Enter to confirm
        tmux -L cc send-keys -t "$SESSION" 2
        sleep 0.2
        tmux -L cc send-keys -t "$SESSION" Enter
        sleep 3
    fi
fi

# Set persistent completion protocol
# This tells Claude to always output CC_CALLBACK_DONE after every task completion
PROTOCOL_INSTRUCTION="⚠️ COMPLETION PROTOCOL (STRICT REQUIREMENT):

From now on, whenever you complete ANY task, answer ANY question, or respond to ANY request, you MUST output exactly the following marker on its own line:

CC_CALLBACK_DONE

This marker is required for automated callback detection. You MUST include it after:
- Each task you complete
- Each question you answer  
- Each request you fulfill
- Every response you provide

Do NOT skip this marker for ANY reason, including simple queries, greetings, or non-coding tasks.

If I type TASK_COMPLETE, output exactly:

CC_CALLBACK_DONE"

# Send protocol via temp file to handle multi-line safely
TMPFILE=$(mktemp /tmp/cc-protocol-XXXXXX.txt)
printf '%s' "$PROTOCOL_INSTRUCTION" > "$TMPFILE"
tmux -L cc load-buffer "$TMPFILE"
tmux -L cc paste-buffer -t "$SESSION"
rm -f "$TMPFILE"
sleep 0.3
tmux -L cc send-keys -t "$SESSION" Enter
sleep 2
log_info "✅ Completion protocol set as persistent rule"

# If initial task provided, send it and start monitoring
if [[ -n "$TASK" ]]; then
    log_info "Sending initial task with monitoring..."

    # Generate unique task ID using timestamp
    TASK_ID=$(date +%Y%m%d_%H%M%S_%N)
    TASK_MARKER="=== START ${TASK_ID} ==="

    # Prepend unique task marker
    TASK_WITH_MARKER="$TASK_MARKER

$TASK"

    # Send task via temp file
    TMPFILE=$(mktemp /tmp/cc-task-XXXXXX.txt)
    printf '%s' "$TASK_WITH_MARKER" > "$TMPFILE"
    tmux -L cc load-buffer "$TMPFILE"
    tmux -L cc paste-buffer -t "$SESSION"
    rm -f "$TMPFILE"
    sleep 0.3
    tmux -L cc send-keys -t "$SESSION" Enter
    log_info "Initial task sent (task_id: $TASK_ID), starting monitor..."

    # Start one-time monitor for initial task (same as send-task.sh)
    (
        START_TIME=$(date +%s)
        TIMEOUT=600  # 10 minutes
        START_DETECTED=false  # Track if we've seen the START marker

        while true; do
            CURRENT_TIME=$(date +%s)
            ELAPSED=$((CURRENT_TIME - START_TIME))

            if [[ $ELAPSED -ge $TIMEOUT ]]; then
                log_info "⏰ Task timeout after ${TIMEOUT}s"
                break
            fi

            if ! tmux -L cc has-session -t "$SESSION" 2>/dev/null; then
                log_info "ℹ️  Session ended"
                break
            fi

            OUTPUT=$(tmux -L cc capture-pane -p -S -50 -t "$SESSION" 2>/dev/null || echo "")

            # Check for user close commands
            if grep -qiE "结束此次会话|关闭会话|exit session|quit session|close session" <<< "$OUTPUT"; then
                tmux -L cc kill-session -t "$SESSION" 2>/dev/null || true
                log_info "🔚 Session closed by user request"
                break
            fi

            # Check for task completion marker (with state tracking)
            if [[ "$START_DETECTED" == false ]]; then
                # Phase 1: Still looking for START marker
                if grep -Fq "$TASK_MARKER" <<< "$OUTPUT"; then
                    START_DETECTED=true
                    log_info "✓ Start marker detected, now waiting for completion..."
                fi
            else
                # Phase 2: START marker found, looking for CC_CALLBACK_DONE
                # Extract content AFTER the START marker to avoid detecting previous tasks
                AFTER_START=$(sed -n "/$TASK_MARKER/,\$p" <<< "$OUTPUT")

                # Check if CC_CALLBACK_DONE appears after START marker
                if grep -q "CC_CALLBACK_DONE" <<< "$AFTER_START"; then
                    # Extract CC's output (between START marker and LAST CC_CALLBACK_DONE)
                    # Extract from line 2 (after START marker) to CC_CALLBACK_DONE, then remove last line (CC_CALLBACK_DONE)
                    TASK_OUTPUT=$(echo "$AFTER_START" | sed -n "2,/CC_CALLBACK_DONE/p" | sed "\$d")

                    # Task completed! Trigger callback with output
                    "$BASE_DIR/callbacks/$CALLBACK.sh" \
                        --status done \
                        --mode interactive \
                        --task "$SESSION" \
                        --message "$TASK" \
                        --output "$TASK_OUTPUT" \
                        --session-key "$SESSION_KEY"
                    log_success "✅ Task completed, callback triggered! Monitor exiting."
                    break
                fi
            fi

            sleep 3
        done
    ) &

    TASK_MONITOR_PID=$!
fi

# Start session lifecycle monitor (handles timeout and close commands, NOT task completion)
log_info "Starting session lifecycle monitor (timeout: $((SESSION_TIMEOUT / 3600)) hours)..."

# Create session state file for tracking start time (used by lifecycle monitor and send-task.sh)
SESSION_STATE_FILE="/tmp/${SESSION}.state"
echo "SESSION_START=$(date +%s)" > "$SESSION_STATE_FILE"
echo "SESSION_LABEL=\"$LABEL\"" >> "$SESSION_STATE_FILE"
echo "SESSION_NAME=\"$SESSION\"" >> "$SESSION_STATE_FILE"

(
    while true; do
        # Read current SESSION_START from state file (may be updated by send-task.sh)
        if [[ -f "$SESSION_STATE_FILE" ]]; then
            source "$SESSION_STATE_FILE"
        else
            # State file missing, session probably ended
            break
        fi

        # Check timeout based on current SESSION_START
        CURRENT_TIME=$(date +%s)
        ELAPSED=$((CURRENT_TIME - SESSION_START))

        if [[ $ELAPSED -ge $SESSION_TIMEOUT ]]; then
            # Session timeout, close it
            # Capture session output before closing
            SESSION_OUTPUT=$(tmux -L cc capture-pane -p -t "$SESSION" 2>/dev/null || echo "")
            tmux -L cc kill-session -t "$SESSION" 2>/dev/null || true
            "$BASE_DIR/callbacks/$CALLBACK.sh" \
                --status done \
                --mode interactive \
                --task "$SESSION" \
                --message "Session closed after $((SESSION_TIMEOUT / 3600)) hours timeout" \
                --output "$SESSION_OUTPUT" \
                --session-key "$SESSION_KEY"
            log_info "⏰ Session timeout after $((SESSION_TIMEOUT / 3600)) hours"
            rm -f "$SESSION_STATE_FILE"
            break
        fi

        # Check if session still exists
        if ! tmux -L cc has-session -t "$SESSION" 2>/dev/null; then
            # Session ended
            rm -f "$SESSION_STATE_FILE"
            break
        fi

        # Capture output and check for user close commands
        OUTPUT=$(tmux -L cc capture-pane -p -t "$SESSION" 2>/dev/null || echo "")

        if grep -qiE "结束此次会话|关闭会话|exit session|quit session|close session" <<< "$OUTPUT"; then
            # User requested to close session
            # Capture session output before closing
            SESSION_OUTPUT=$(tmux -L cc capture-pane -p -t "$SESSION" 2>/dev/null || echo "")
            tmux -L cc kill-session -t "$SESSION" 2>/dev/null || true
            "$BASE_DIR/callbacks/$CALLBACK.sh" \
                --status done \
                --mode interactive \
                --task "$SESSION" \
                --message "Session closed by user request" \
                --output "$SESSION_OUTPUT" \
                --session-key "$SESSION_KEY"
            log_info "🔚 Session closed by user request"
            rm -f "$SESSION_STATE_FILE"
            break
        fi

        # Note: We do NOT monitor CC_CALLBACK_DONE here
        # Task completion monitoring is handled separately by interactive.sh (initial task) and send-task.sh (subsequent tasks)

        sleep 1800  # Check every 30 minutes (1800 seconds) since we only care about lifecycle events
    done
) &

LIFECYCLE_MONITOR_PID=$!

log_success "Session started: $SESSION"

# Run in background mode (default)
log_success "Interactive started in background. Callback will notify on completion."
exit 0
