#!/bin/bash
# AI Mother - Full patrol scan of all AI agents
# Outputs a structured report and updates state file
# Usage: ./patrol.sh [--quiet] [--active-pids <pid1,pid2,...>]
#   --active-pids: only send notifications for these PIDs; others are checked silently

QUIET=${1:-""}
ACTIVE_PIDS_ARG=""
if [ "$1" = "--active-pids" ]; then
    QUIET=""
    ACTIVE_PIDS_ARG="$2"
elif [ "$2" = "--active-pids" ]; then
    ACTIVE_PIDS_ARG="$3"
fi
SKILL_DIR="$HOME/.openclaw/skills/ai-mother"

# File lock to prevent concurrent patrol runs
LOCK_FILE="$SKILL_DIR/.patrol.lock"
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
    [ "$QUIET" != "--quiet" ] && echo "⚠️  Patrol already running, skipping"
    exit 0
fi

# Cleanup temp files on exit
TEMP_FILES=()
cleanup() {
    for f in "${TEMP_FILES[@]}"; do rm -f "$f"; done
    flock -u 9
}
trap cleanup EXIT
STATE_FILE="$SKILL_DIR/ai-state.txt"
CONTEXT_SCRIPT="$SKILL_DIR/scripts/get-ai-context.sh"
UPDATE_STATE="$SKILL_DIR/scripts/update-state.sh"
CONV_DIR="$SKILL_DIR/conversations"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

ISSUES=()
COMPLETED=()
ACTIVE=()

[ "$QUIET" != "--quiet" ] && echo "=== AI Mother Patrol: $TIMESTAMP ==="
[ "$QUIET" != "--quiet" ] && echo ""

# Clean up stale conversation state files
CLEANED=0
if [ -d "$CONV_DIR" ]; then
    for state_file in "$CONV_DIR"/*.state; do
        [ -f "$state_file" ] || continue
        PID=$(basename "$state_file" .state)
        if ! ps -p "$PID" > /dev/null 2>&1; then
            rm -f "$state_file" "${state_file%.state}.log" 2>/dev/null
            CLEANED=$((CLEANED + 1))
        fi
    done
fi
[ "$QUIET" != "--quiet" ] && [ "$CLEANED" -gt 0 ] && echo "🧹 Cleaned $CLEANED stale conversation file(s)"

# Clean up stale entries from ai-state.txt (dead PIDs or tmux wrappers)
if [ -f "$STATE_FILE" ]; then
    TEMP_STATE=$(mktemp)
    TEMP_FILES+=("$TEMP_STATE")
    while IFS='|' read -r pid ai_type rest; do
        # Skip if PID doesn't exist
        if ! ps -p "$pid" > /dev/null 2>&1; then
            continue
        fi
        # Skip if it's a tmux wrapper (not the actual AI)
        if [ "$ai_type" = "tmux" ]; then
            continue
        fi
        echo "$pid|$ai_type|$rest"
    done < "$STATE_FILE" > "$TEMP_STATE"
    mv "$TEMP_STATE" "$STATE_FILE"
fi

# Clean up notified completions for dead PIDs
NOTIFIED_FILE="$SKILL_DIR/.notified_completions"
if [ -f "$NOTIFIED_FILE" ]; then
    TEMP_NOTIFIED=$(mktemp)
    TEMP_FILES+=("$TEMP_NOTIFIED")
    while read -r pid; do
        if ps -p "$pid" > /dev/null 2>&1; then
            echo "$pid"
        fi
    done < "$NOTIFIED_FILE" > "$TEMP_NOTIFIED"
    mv "$TEMP_NOTIFIED" "$NOTIFIED_FILE"
fi

# Find all AI processes (exclude tmux wrapper processes)
AI_PROCS=$(ps aux | awk '
  /[[:space:]](claude|codex|opencode|gemini)[[:space:]]/ ||
  /[[:space:]](claude|codex|opencode|gemini)$/ {
    if ($0 !~ /grep/ && $0 !~ "ai-mother" && $0 !~ "get-ai-context" && $0 !~ /tmux.*claude/ && $0 !~ /tmux.*codex/ && $0 !~ /tmux.*opencode/ && $0 !~ /tmux.*gemini/ && $11 !~ /^tmux/) print $2
  }
')

if [ -z "$AI_PROCS" ]; then
    echo "No AI agents running."
    exit 0
fi

# Load active PIDs (high-frequency targets) if file exists
ACTIVE_PIDS_FILE="$SKILL_DIR/.active_pids"
ACTIVE_PIDS=""
if [ -f "$ACTIVE_PIDS_FILE" ]; then
    ACTIVE_PIDS=$(cat "$ACTIVE_PIDS_FILE")
fi

# Helper: check if a PID is in the active list (or if no active list = all PIDs qualify)
is_active_pid() {
    local pid="$1"
    [ -z "$ACTIVE_PIDS" ] && return 0  # No filter = all qualify
    echo "$ACTIVE_PIDS" | grep -qw "$pid"
}

for PID in $AI_PROCS; do
    ps -p "$PID" > /dev/null 2>&1 || continue

    WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)
    STATE=$(ps -o stat= -p "$PID" | head -c 1)
    ELAPSED=$(ps -o etime= -p "$PID" | xargs)
    CMD=$(ps -o cmd= -p "$PID" | awk '{print $1}' | xargs basename)
    CPU=$(ps -o pcpu= -p "$PID" | xargs)

    # Detect AI type
    AI_TYPE="$CMD"

    # Get last output from context script
    CONTEXT=$("$CONTEXT_SCRIPT" "$PID" 2>/dev/null)
    LAST_OUTPUT=$(echo "$CONTEXT" | sed -n '/^--- Last Output ---/,/^---/p' | grep -v "^---" | head -10)
    RECENT_FILES=$(echo "$CONTEXT" | sed -n '/^--- Recent File Changes/,/^---/p' | grep -v "^---" | head -5)

    # Check tmux pane for real-time waiting status (higher priority than session file)
    TMUX_CHECK=$("$SKILL_DIR/scripts/check-tmux-waiting.sh" "$PID" 2>/dev/null | head -1)

    # Determine status
    STATUS="active"
    NOTES=""
    
    # Only add to notification arrays if this PID is in the active list
    # (or if no active list filter is set — normal full patrol)
    SHOULD_NOTIFY=$(is_active_pid "$PID" && echo "true" || echo "false")

    # Priority 1: Check tmux pane (real-time status)
    if [ "$TMUX_CHECK" = "WAITING_INPUT" ]; then
        STATUS="waiting_input"
        NOTES="Waiting for user confirmation (detected in tmux)"
        # Always notify for permission prompts regardless of active list
        ISSUES+=("💬 PID $PID ($AI_TYPE) WAITING FOR INPUT — $WORKDIR")
        # Trigger auto-heal immediately to send permission notification with options
        "$SKILL_DIR/scripts/auto-heal.sh" "$PID" > /dev/null 2>&1 &

    elif [ "$STATE" = "T" ]; then
        STATUS="stopped"
        NOTES="Process suspended (Ctrl+Z)"
        [ "$SHOULD_NOTIFY" = "true" ] && ISSUES+=("⚠️  PID $PID ($AI_TYPE) STOPPED — $WORKDIR")

    elif echo "$LAST_OUTPUT" | grep -qi "429\|rate.limit\|rate_limit"; then
        STATUS="waiting_api"
        NOTES="Hit API rate limit (429)"
        [ "$SHOULD_NOTIFY" = "true" ] && ISSUES+=("🚫 PID $PID ($AI_TYPE) RATE LIMITED — $WORKDIR")

    elif echo "$LAST_OUTPUT" | grep -qi "permission denied\|EACCES\|not allowed"; then
        STATUS="error"
        NOTES="Permission denied error"
        [ "$SHOULD_NOTIFY" = "true" ] && ISSUES+=("❌ PID $PID ($AI_TYPE) PERMISSION ERROR — $WORKDIR")

    elif echo "$LAST_OUTPUT" | grep -qi "should i\|do you want\|shall i\|please confirm\|y/n\|yes/no"; then
        STATUS="waiting_input"
        NOTES="Waiting for confirmation"
        # Always notify for input-waiting regardless of active list
        ISSUES+=("💬 PID $PID ($AI_TYPE) WAITING FOR INPUT — $WORKDIR")

    elif echo "$LAST_OUTPUT" | grep -qi "all done\|completed\|finished\|task complete\|done\."; then
        STATUS="completed"
        NOTES="Task appears complete"
        [ "$SHOULD_NOTIFY" = "true" ] && COMPLETED+=("✅ PID $PID ($AI_TYPE) COMPLETED — $WORKDIR")
        
        # Check if we already notified about this completion
        NOTIFIED_FILE="$SKILL_DIR/.notified_completions"
        if ! grep -q "^$PID$" "$NOTIFIED_FILE" 2>/dev/null; then
            # Send completion notification
            NOTIFY_SCRIPT="$SKILL_DIR/scripts/notify-owner.sh"
            if [ -x "$NOTIFY_SCRIPT" ]; then
                "$NOTIFY_SCRIPT" "✅ AI Task Completed

AI: $AI_TYPE (PID $PID)
Project: ${WORKDIR/$HOME/~}
Runtime: $ELAPSED

The AI has finished its task. You may want to review the results." 2>/dev/null &
                
                # Mark as notified
                echo "$PID" >> "$NOTIFIED_FILE"
            fi
        fi

    elif [ -z "$RECENT_FILES" ] && [ "$CPU" = "0.0" ]; then
        STATUS="idle"
        NOTES="No recent file changes, CPU idle"
        ACTIVE+=("💤 PID $PID ($AI_TYPE) IDLE — $WORKDIR (runtime: $ELAPSED)")

    else
        STATUS="active"
        NOTES="Working normally"
        ACTIVE+=("✅ PID $PID ($AI_TYPE) ACTIVE — $WORKDIR (runtime: $ELAPSED)")
        
        # If AI became active again after completion, clear the notification flag
        # so we can notify again if it completes another task
        if grep -q "^$PID$" "$NOTIFIED_FILE" 2>/dev/null; then
            sed -i "/^$PID$/d" "$NOTIFIED_FILE" 2>/dev/null
        fi
    fi

    # Update state file
    TASK=$(grep "^$PID|" "$STATE_FILE" 2>/dev/null | cut -d'|' -f4)
    [ -z "$TASK" ] && TASK="unknown"
    "$UPDATE_STATE" "$PID" "$AI_TYPE" "$WORKDIR" "$TASK" "$STATUS" "$NOTES" 2>/dev/null

    # Print per-agent summary
    if [ "$QUIET" != "--quiet" ]; then
        echo "PID $PID | $AI_TYPE | $STATE | $ELAPSED | $WORKDIR"
        echo "  Status: $STATUS — $NOTES"
        if [ -n "$LAST_OUTPUT" ]; then
            echo "  Last: $(echo "$LAST_OUTPUT" | head -2 | tr '\n' ' ')"
        fi
        echo ""
    fi
done

# Detect duplicate workdirs (multiple AIs on same directory)
DUPLICATES=()
declare -A WORKDIR_PIDS
for PID in $AI_PROCS; do
    ps -p "$PID" > /dev/null 2>&1 || continue
    WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)
    if [ -n "${WORKDIR_PIDS[$WORKDIR]}" ]; then
        # Duplicate found
        EXISTING_PID="${WORKDIR_PIDS[$WORKDIR]}"
        AI_TYPE=$(ps -o cmd= -p "$PID" | awk '{print $1}' | xargs basename)
        DUPLICATES+=("⚠️  DUPLICATE: PID $EXISTING_PID and $PID both working on $WORKDIR")
    else
        WORKDIR_PIDS[$WORKDIR]="$PID"
    fi
done

# Print summary
if [ "$QUIET" != "--quiet" ]; then
    echo "=== Summary ==="
    [ ${#DUPLICATES[@]} -gt 0 ] && printf '%s\n' "${DUPLICATES[@]}"
    [ ${#ISSUES[@]} -gt 0 ] && printf '%s\n' "${ISSUES[@]}"
    [ ${#COMPLETED[@]} -gt 0 ] && printf '%s\n' "${COMPLETED[@]}"
    [ ${#ACTIVE[@]} -gt 0 ] && printf '%s\n' "${ACTIVE[@]}"
    
    # Suggest cleanup for duplicates
    if [ ${#DUPLICATES[@]} -gt 0 ]; then
        echo ""
        echo "💡 Multiple AIs on same directory detected!"
        echo "   Run: ~/.openclaw/skills/ai-mother/scripts/cleanup-duplicates.sh"
    fi
    echo ""
fi

# Adjust patrol frequency based on active conversations
"$SKILL_DIR/scripts/manage-patrol-frequency.sh" > /dev/null 2>&1 &

# Return issues for caller (without duplicating summary)
if [ ${#ISSUES[@]} -gt 0 ] || [ ${#COMPLETED[@]} -gt 0 ] || [ ${#DUPLICATES[@]} -gt 0 ]; then
    echo "NEEDS_ATTENTION=true"
fi
