#!/bin/bash
# Detect communication method for an AI process
# Usage: ./detect-comm-method.sh <PID>

PID=$1
if [ -z "$PID" ]; then
    echo "Usage: $0 <PID>"
    exit 1
fi

if ! ps -p "$PID" > /dev/null 2>&1; then
    echo "ERROR: Process $PID not found"
    exit 1
fi

CMD=$(ps -o cmd= -p "$PID" | awk '{print $1}' | xargs basename)

# Check if process is in a tmux session
TMUX_SESSION=""
if command -v tmux >/dev/null 2>&1; then
    # Method 1: Check if PID is in any tmux pane
    TMUX_SESSION=$(tmux list-panes -a -F "#{pane_pid} #{session_name}" 2>/dev/null | grep "^$PID " | awk '{print $2}')
    
    # Method 2: Check parent process chain for tmux
    if [ -z "$TMUX_SESSION" ]; then
        PPID_CHAIN=$(pstree -p $PID | grep -o "tmux([0-9]*)" | head -1 | grep -o "[0-9]*")
        if [ -n "$PPID_CHAIN" ]; then
            TMUX_SESSION=$(tmux list-sessions -F "#{session_name} #{pane_pid}" 2>/dev/null | grep "$PID" | awk '{print $1}')
        fi
    fi
fi

# Determine communication method
if [ -n "$TMUX_SESSION" ]; then
    METHOD="tmux"
    echo "PID: $PID"
    echo "AI Type: $CMD"
    echo "Communication: tmux"
    echo "Tmux Session: $TMUX_SESSION"
    echo "Command: tmux send-keys -t $TMUX_SESSION \"message\" Enter"
else
    # Check if it's a TUI or pipe-friendly
    case "$CMD" in
        claude|opencode)
            METHOD="notify_only"
            echo "PID: $PID"
            echo "AI Type: $CMD"
            echo "Communication: notify_only (TUI without tmux)"
            echo "Note: Cannot send messages automatically. Manual intervention required."
            ;;
        codex|aider)
            METHOD="stdin"
            echo "PID: $PID"
            echo "AI Type: $CMD"
            echo "Communication: stdin"
            echo "Command: printf 'message\\n' > /proc/$PID/fd/0"
            ;;
        *)
            METHOD="unknown"
            echo "PID: $PID"
            echo "AI Type: $CMD"
            echo "Communication: unknown"
            ;;
    esac
fi

# Output machine-readable format
echo ""
echo "# Machine-readable output:"
echo "COMM_METHOD=$METHOD"
echo "TMUX_SESSION=$TMUX_SESSION"
echo "AI_TYPE=$CMD"
