#!/bin/bash
# Orchestrix HANDOFF Detector - tmux Automation Hook (MCP Version)
# Triggers on Claude Code Stop event, detects HANDOFF and routes to target agent
#
# Design principles:
# - NO dependency on environment variables (robust)
# - Scans ALL tmux windows to find HANDOFF message
# - Uses hash-based deduplication to prevent re-processing
# - Background process handles cleanup and lock release
#
# Pro/Team Feature: This script is only available for Pro and Team subscribers.

set +e  # Don't exit on errors

# ============================================
# Configuration
# ============================================
# Try to get session from env, otherwise detect from tmux context
SESSION_NAME="${ORCHESTRIX_SESSION:-}"

# Agent mappings
get_agent_name() {
    case "$1" in
        0) echo "architect" ;;
        1) echo "sm" ;;
        2) echo "dev" ;;
        3) echo "qa" ;;
        *) echo "" ;;
    esac
}

get_window_num() {
    case "$1" in
        architect) echo "0" ;;
        sm) echo "1" ;;
        dev) echo "2" ;;
        qa) echo "3" ;;
        *) echo "" ;;
    esac
}

# MCP version: use /o {agent} format
get_agent_command() {
    case "$1" in
        architect) echo "/o architect" ;;
        sm) echo "/o sm" ;;
        dev) echo "/o dev" ;;
        qa) echo "/o qa" ;;
        *) echo "" ;;
    esac
}

# Infer target agent from command (for simplified format like "*develop-story 10.4")
get_target_from_command() {
    local cmd="$1"
    case "$cmd" in
        develop-story|apply-qa-fixes|quick-develop)
            echo "dev" ;;
        review|quick-verify|test-design|finalize-commit)
            echo "qa" ;;
        draft|revise-story|revise|apply-proposal|create-next-story)
            echo "sm" ;;
        review-escalation|resolve-change)
            echo "architect" ;;
        *)
            echo "" ;;
    esac
}

# ============================================
# Find Orchestrix Session (before any logging)
# ============================================

# Priority 1: Explicit env var
# Priority 2: Detect current tmux session (if inside tmux and it's an orchestrix session)
# Priority 3: Scan all tmux sessions for orchestrix prefix
if [[ -z "$SESSION_NAME" && -n "$TMUX" ]]; then
    CURRENT_SESSION=$(tmux display-message -p '#{session_name}' 2>/dev/null)
    if [[ "$CURRENT_SESSION" == orchestrix* ]]; then
        SESSION_NAME="$CURRENT_SESSION"
    fi
fi

if [[ -z "$SESSION_NAME" ]]; then
    SESSION_NAME=$(tmux list-sessions -F '#{session_name}' 2>/dev/null | grep -E '^orchestrix' | head -1)
fi

if [[ -z "$SESSION_NAME" ]]; then
    exit 0
fi

if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    exit 0
fi

# Session-specific log file (all logging starts AFTER session detection)
LOG_FILE="/tmp/${SESSION_NAME}-handoff.log"
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"; }

log "========== Hook triggered =========="
log "Session: $SESSION_NAME"

# ============================================
# Scan All Windows for HANDOFF
# ============================================
PROCESSED_FILE="/tmp/${SESSION_NAME}-processed.txt"
touch "$PROCESSED_FILE"

SOURCE_WIN=""
TARGET=""
CMD=""
HANDOFF_HASH=""

for win in 0 1 2 3; do
    OUTPUT=$(tmux capture-pane -t "$SESSION_NAME:$win" -p -S - 2>/dev/null)
    [[ -z "$OUTPUT" ]] && continue

    # Pattern 1: Standard HANDOFF format (🎯 HANDOFF TO agent: *command args)
    LINE=$(echo "$OUTPUT" | grep -E '🎯.*HANDOFF.*TO' | tail -1)
    if [[ -n "$LINE" ]]; then
        # Calculate hash to avoid re-processing
        HASH=$(echo "$LINE" | md5 2>/dev/null || echo "$LINE" | md5sum 2>/dev/null | cut -d' ' -f1)

        # Skip if already processed
        if grep -q "$HASH" "$PROCESSED_FILE" 2>/dev/null; then
            continue
        fi

        # Parse HANDOFF message
        if [[ "$LINE" =~ HANDOFF[[:space:]]+TO[[:space:]]+([a-zA-Z0-9_-]+):[[:space:]]*\*?([a-z0-9-]+)([[:space:]]+([0-9]+\.[0-9]+))? ]]; then
            SOURCE_WIN=$win
            TARGET=$(echo "${BASH_REMATCH[1]}" | tr '[:upper:]' '[:lower:]')
            CMD="*${BASH_REMATCH[2]}${BASH_REMATCH[4]:+ ${BASH_REMATCH[4]}}"
            HANDOFF_HASH=$HASH
            log "Found HANDOFF in window $win: $LINE"
            break
        fi
    fi

    # Pattern 2: Simplified format - more flexible detection
    # Handles: "*develop-story 10.4", "*draft", "* review 10.4", etc.
    if [[ -z "$TARGET" ]]; then
        # Search last 30 lines for command patterns (more tolerant)
        LAST_LINES=$(echo "$OUTPUT" | tail -30)

        # Try multiple patterns in order of specificity
        # Pattern 2a: *command story_id (e.g., "*develop-story 10.4")
        SIMPLE_LINE=$(echo "$LAST_LINES" | grep -E '\*[a-z]+-?[a-z-]*\s+[0-9]+\.[0-9]+' | tail -1)

        if [[ -z "$SIMPLE_LINE" ]]; then
            # Pattern 2b: *command without story_id (e.g., "*draft")
            SIMPLE_LINE=$(echo "$LAST_LINES" | grep -E '^\s*\*[a-z]+-?[a-z-]*\s*$' | tail -1)
        fi

        if [[ -n "$SIMPLE_LINE" ]]; then
            # Extract command and optional story_id
            # Handle: "*develop-story 10.4", "* review 10.4", "*draft"
            if [[ "$SIMPLE_LINE" =~ \*[[:space:]]*([a-z][a-z-]*)[[:space:]]*([0-9]+\.[0-9]+)? ]]; then
                simple_cmd="${BASH_REMATCH[1]}"
                story_id="${BASH_REMATCH[2]}"
                inferred_target=$(get_target_from_command "$simple_cmd")

                if [[ -n "$inferred_target" ]]; then
                    # Calculate hash
                    HASH=$(echo "$SIMPLE_LINE" | md5 2>/dev/null || echo "$SIMPLE_LINE" | md5sum 2>/dev/null | cut -d' ' -f1)

                    # Skip if already processed
                    if grep -q "$HASH" "$PROCESSED_FILE" 2>/dev/null; then
                        continue
                    fi

                    SOURCE_WIN=$win
                    TARGET=$inferred_target
                    if [[ -n "$story_id" ]]; then
                        CMD="*${simple_cmd} ${story_id}"
                    else
                        CMD="*${simple_cmd}"
                    fi
                    HANDOFF_HASH=$HASH
                    log "[SIMPLE] Found in window $win: '$SIMPLE_LINE' -> $TARGET: $CMD"
                    break
                fi
            fi
        fi
    fi
done

# No HANDOFF found - try fallback from pending-handoff file
if [[ -z "$TARGET" || -z "$CMD" ]]; then
    log "No HANDOFF in terminal output, checking fallback file..."

    # ============================================
    # Fallback: Check pending-handoff.json
    # ============================================
    # Find project root (look for .orchestrix-core directory)
    FALLBACK_FILE=""
    for win in 0 1 2 3; do
        # Get the pane's current directory
        PANE_DIR=$(tmux display-message -t "$SESSION_NAME:$win" -p '#{pane_current_path}' 2>/dev/null)
        if [[ -n "$PANE_DIR" && -f "$PANE_DIR/.orchestrix-core/runtime/pending-handoff.json" ]]; then
            FALLBACK_FILE="$PANE_DIR/.orchestrix-core/runtime/pending-handoff.json"
            SOURCE_WIN=$win
            break
        fi
    done

    if [[ -z "$FALLBACK_FILE" ]]; then
        log "No pending-handoff.json found"
        exit 0
    fi

    log "Found fallback file: $FALLBACK_FILE"

    # Read and parse the JSON file
    if command -v jq &>/dev/null; then
        # Use jq if available
        STATUS=$(jq -r '.status // "unknown"' "$FALLBACK_FILE" 2>/dev/null)
        if [[ "$STATUS" != "pending" ]]; then
            log "Fallback file status is '$STATUS', not 'pending'. Skipping."
            exit 0
        fi

        TARGET=$(jq -r '.target_agent // ""' "$FALLBACK_FILE" 2>/dev/null)
        CMD=$(jq -r '.command // ""' "$FALLBACK_FILE" 2>/dev/null)
        STORY_ID=$(jq -r '.story_id // ""' "$FALLBACK_FILE" 2>/dev/null)
        SOURCE_AGENT=$(jq -r '.source_agent // ""' "$FALLBACK_FILE" 2>/dev/null)
    else
        # Fallback to grep/sed parsing
        STATUS=$(grep -o '"status"[[:space:]]*:[[:space:]]*"[^"]*"' "$FALLBACK_FILE" | sed 's/.*"\([^"]*\)"$/\1/')
        if [[ "$STATUS" != "pending" ]]; then
            log "Fallback file status is '$STATUS', not 'pending'. Skipping."
            exit 0
        fi

        TARGET=$(grep -o '"target_agent"[[:space:]]*:[[:space:]]*"[^"]*"' "$FALLBACK_FILE" | sed 's/.*"\([^"]*\)"$/\1/')
        CMD=$(grep -o '"command"[[:space:]]*:[[:space:]]*"[^"]*"' "$FALLBACK_FILE" | sed 's/.*"\([^"]*\)"$/\1/')
        STORY_ID=$(grep -o '"story_id"[[:space:]]*:[[:space:]]*"[^"]*"' "$FALLBACK_FILE" | sed 's/.*"\([^"]*\)"$/\1/')
        SOURCE_AGENT=$(grep -o '"source_agent"[[:space:]]*:[[:space:]]*"[^"]*"' "$FALLBACK_FILE" | sed 's/.*"\([^"]*\)"$/\1/')
    fi

    if [[ -z "$TARGET" || -z "$CMD" ]]; then
        log "Invalid fallback file content"
        exit 0
    fi

    # Create a hash to prevent re-processing
    # Include STORY_ID to differentiate handoffs for different stories with same command
    HANDOFF_HASH=$(echo "fallback-$SOURCE_AGENT-$TARGET-$CMD-$STORY_ID" | md5 2>/dev/null || echo "fallback-$SOURCE_AGENT-$TARGET-$CMD-$STORY_ID" | md5sum 2>/dev/null | cut -d' ' -f1)

    # Skip if already processed
    if grep -q "$HANDOFF_HASH" "$PROCESSED_FILE" 2>/dev/null; then
        log "Fallback handoff already processed"
        exit 0
    fi

    # Get SOURCE_WIN from SOURCE_AGENT (override the window where file was found)
    SOURCE_WIN=$(get_window_num "$SOURCE_AGENT")

    log "[FALLBACK] Recovered handoff from file: $SOURCE_AGENT (win $SOURCE_WIN) -> $TARGET: $CMD"

    # Mark the fallback file as completed
    if command -v jq &>/dev/null; then
        jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '.status = "completed_by_fallback" | .completed_at = $ts' "$FALLBACK_FILE" > "$FALLBACK_FILE.tmp.$$" 2>/dev/null && mv "$FALLBACK_FILE.tmp.$$" "$FALLBACK_FILE"
    else
        sed -i.bak 's/"status"[[:space:]]*:[[:space:]]*"pending"/"status": "completed_by_fallback"/' "$FALLBACK_FILE" 2>/dev/null
        rm -f "$FALLBACK_FILE.bak" 2>/dev/null
    fi
fi

# Mark as processed
echo "$HANDOFF_HASH" >> "$PROCESSED_FILE"

# Keep processed file small (last 100 entries)
# Use PID in tmp filename to avoid race with concurrent hook instances or background processes
tail -100 "$PROCESSED_FILE" > "$PROCESSED_FILE.tmp.$$" 2>/dev/null && mv "$PROCESSED_FILE.tmp.$$" "$PROCESSED_FILE"

# Get source agent name (only if not already set by fallback)
if [[ -z "$SOURCE_AGENT" ]]; then
    SOURCE_AGENT=$(get_agent_name "$SOURCE_WIN")
fi
TARGET_WIN=$(get_window_num "$TARGET")

# Validate
if [[ -z "$TARGET_WIN" ]]; then
    log "ERROR: Unknown target agent '$TARGET'"
    exit 0
fi

if [[ "$TARGET_WIN" == "$SOURCE_WIN" ]]; then
    log "ERROR: Source and target are same window"
    exit 0
fi

log "HANDOFF: $SOURCE_AGENT (win $SOURCE_WIN) -> $TARGET (win $TARGET_WIN)"
log "Command: $CMD"

# ============================================
# Atomic Lock
# ============================================
LOCK="/tmp/${SESSION_NAME}-${SOURCE_WIN}.lock"
LOCK_TIMEOUT=60

if ! mkdir "$LOCK" 2>/dev/null; then
    if [[ -f "$LOCK/ts" ]]; then
        ts=$(cat "$LOCK/ts" 2>/dev/null || echo 0)
        now=$(date +%s)
        age=$((now - ts))
        if [[ $age -lt $LOCK_TIMEOUT ]]; then
            log "SKIP: Window $SOURCE_WIN locked (${age}s ago)"
            exit 0
        fi
        log "Stale lock (${age}s), cleaning"
    fi
    rm -rf "$LOCK" 2>/dev/null
    mkdir "$LOCK" 2>/dev/null || { log "SKIP: lock race"; exit 0; }
fi
date +%s > "$LOCK/ts"

# ============================================
# Send to Target
# ============================================
log "Sending '$CMD' to $TARGET (window $TARGET_WIN)..."

if tmux send-keys -t "$SESSION_NAME:$TARGET_WIN" "$CMD" 2>/dev/null; then
    sleep 0.5
    tmux send-keys -t "$SESSION_NAME:$TARGET_WIN" Enter
    log "SUCCESS: Command sent to $TARGET"
else
    log "ERROR: Failed to send command"
    rm -rf "$LOCK"
    exit 0
fi

# ============================================
# Background: Clear & Reload Source Agent
# ============================================
RELOAD_CMD=$(get_agent_command "$SOURCE_AGENT")

(
    log "[BG] Starting cleanup for $SOURCE_AGENT (window $SOURCE_WIN)"
    sleep 2

    # Clear
    tmux send-keys -t "$SESSION_NAME:$SOURCE_WIN" "/clear" 2>/dev/null
    sleep 0.5
    tmux send-keys -t "$SESSION_NAME:$SOURCE_WIN" Enter
    log "[BG] /clear sent to $SOURCE_AGENT"

    sleep 5

    # Reload
    if [[ -n "$RELOAD_CMD" ]]; then
        tmux send-keys -t "$SESSION_NAME:$SOURCE_WIN" "$RELOAD_CMD" 2>/dev/null
        sleep 0.5
        tmux send-keys -t "$SESSION_NAME:$SOURCE_WIN" Enter
        log "[BG] Reload sent: $RELOAD_CMD"
        sleep 15
    fi

    # Remove hash from processed file to allow future same-message HANDOFF
    # This fixes the issue where repeated identical messages (e.g., "*draft") are skipped
    if [[ -n "$HANDOFF_HASH" && -f "$PROCESSED_FILE" ]]; then
        grep -v "^${HANDOFF_HASH}$" "$PROCESSED_FILE" > "$PROCESSED_FILE.tmp.$$" 2>/dev/null && mv -f "$PROCESSED_FILE.tmp.$$" "$PROCESSED_FILE"
        log "[BG] Hash removed from processed file: $HANDOFF_HASH"
    fi

    # Release lock
    rm -rf "$LOCK"
    log "[BG] Cleanup complete, lock released"
) >> "$LOG_FILE" 2>&1 &

log "Background process started (PID $!)"
log "========== Hook complete =========="
exit 0
