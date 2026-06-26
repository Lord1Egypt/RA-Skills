#!/bin/bash
# Send a task to an interactive session with one-time completion monitoring
# Usage: send-task.sh --session <name> --task <prompt> [--callback <type>]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

SESSION=""
TASK=""
CALLBACK="${CC_CALLBACK:-openclaw}"
SESSION_KEY=""
TIMEOUT=600  # 10 minutes

while [[ $# -gt 0 ]]; do
    case $1 in
        --session)
            SESSION="$2"
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
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [[ -z "$SESSION" ]]; then
    echo "Error: --session is required"
    exit 1
fi

if [[ -z "$TASK" ]]; then
    echo "Error: --task is required"
    exit 1
fi

if [[ -z "$SESSION_KEY" ]]; then
    echo "Error: --session-key is required"
    exit 1
fi

# Add cc- prefix if not present
[[ "$SESSION" != cc-* ]] && SESSION="cc-${SESSION}"

# Check if session exists
if ! tmux -L cc has-session -t "$SESSION" 2>/dev/null; then
    echo "Error: Session $SESSION does not exist"
    echo "Start it first with: bash modes/interactive.sh --project <path> --label <name>"
    exit 1
fi

# Reset session timeout by updating SESSION_START in state file
SESSION_STATE_FILE="/tmp/cc-session-${SESSION#cc-}.state"
if [[ -f "$SESSION_STATE_FILE" ]]; then
    echo "SESSION_START=$(date +%s)" > "$SESSION_STATE_FILE"
    echo "SESSION_LABEL=\"${SESSION#cc-}\"" >> "$SESSION_STATE_FILE"
    echo "SESSION_NAME=\"$SESSION\"" >> "$SESSION_STATE_FILE"
fi

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}ℹ${NC} $*"
}

log_success() {
    echo -e "${GREEN}✅${NC} $*"
}

# Generate unique task ID using timestamp
TASK_ID=$(date +%Y%m%d_%H%M%S_%N)
TASK_MARKER="=== START ${TASK_ID} ==="

# Prepend unique task marker
TASK_WITH_MARKER="$TASK_MARKER

$TASK

⚠️ 注意协议要求输出：CC_CALLBACK_DONE"

# Send task via temp file + tmux load-buffer to handle multi-line safely
TMPFILE=$(mktemp /tmp/cc-task-XXXXXX.txt)
printf '%s' "$TASK_WITH_MARKER" > "$TMPFILE"
tmux -L cc load-buffer "$TMPFILE"
tmux -L cc paste-buffer -t "$SESSION"
rm -f "$TMPFILE"
sleep 0.2
tmux -L cc send-keys -t "$SESSION" Enter

log_success "Task sent to $SESSION"
log_info "Session timeout reset to 3 hours from now"
log_info "Monitoring for completion in background (timeout: ${TIMEOUT}s, task_id: $TASK_ID)..."

# Run monitoring in background
(
    # Start one-time monitoring for this task
    START_TIME=$(date +%s)
    START_DETECTED=false  # Track if we've seen the START marker

    while true; do
        CURRENT_TIME=$(date +%s)
        ELAPSED=$((CURRENT_TIME - START_TIME))

        if [[ $ELAPSED -ge $TIMEOUT ]]; then
            log_info "⏰ Task timeout after ${TIMEOUT}s"
            exit 1
        fi

        # Check if session still exists
        if ! tmux -L cc has-session -t "$SESSION" 2>/dev/null; then
            log_info "ℹ️  Session ended"
            exit 0
        fi

        # Capture output and check for patterns
        OUTPUT=$(tmux -L cc capture-pane -p -S -50 -t "$SESSION" 2>/dev/null || echo "")

        # Check for user close commands first
        if grep -qiE "结束此次会话|关闭会话|exit session|quit session|close session" <<< "$OUTPUT"; then
            # User requested to close session
            tmux -L cc kill-session -t "$SESSION" 2>/dev/null || true
            log_info "🔚 Session closed by user request"
            exit 0
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
                exit 0
            fi
        fi

        sleep 3
    done
) &

TASK_MONITOR_PID=$!

log_success "Interactive task started in background. Callback will notify on completion."
exit 0
