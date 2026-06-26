#!/bin/bash
# Get current session ID/path for different AI clients
# Usage: ./get-session-info.sh <PID>

PID=$1
if [ -z "$PID" ]; then
    echo "Usage: $0 <PID>"
    exit 1
fi

CMD=$(ps -o cmd= -p "$PID" 2>/dev/null | awk '{print $1}' | xargs basename)
WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)

echo "=== Session Info for PID $PID ==="
echo "AI Type: $CMD"
echo "Workdir: $WORKDIR"
echo ""

case "$CMD" in
    claude)
        # Claude Code: ~/.claude/projects/<encoded-path>/<session-id>.jsonl
        # Path encoding: /home/user/project → -home-user-project
        SAFE_PATH=$(echo "$WORKDIR" | sed 's|^/||' | sed 's|/|-|g')
        SESSION_DIR="$HOME/.claude/projects/$SAFE_PATH"
        
        if [ ! -d "$SESSION_DIR" ]; then
            # Fallback: search by workdir in session files
            LATEST_SESSION=$(find "$HOME/.claude/projects" -type f -name "*.jsonl" -exec grep -l "\"$WORKDIR\"" {} \; 2>/dev/null | xargs ls -t 2>/dev/null | head -1)
        else
            LATEST_SESSION=$(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -1)
        fi
        
        if [ -n "$LATEST_SESSION" ]; then
            SESSION_ID=$(basename "$LATEST_SESSION" .jsonl)
            echo "Session file: $LATEST_SESSION"
            echo "Session ID: $SESSION_ID"
            echo "Last modified: $(stat -c %y "$LATEST_SESSION" 2>/dev/null)"
        else
            echo "No session files found"
        fi
        ;;
        
    opencode)
        # OpenCode: SQLite database at ~/.local/share/opencode/opencode.db
        DB="$HOME/.local/share/opencode/opencode.db"
        if [ -f "$DB" ]; then
            echo "Database: $DB"
            # Get active conversation ID
            CONV_ID=$(sqlite3 "$DB" "
                SELECT c.id, c.title 
                FROM conversation c 
                WHERE c.workdir = '$WORKDIR' 
                ORDER BY c.time_updated DESC 
                LIMIT 1;" 2>/dev/null)
            if [ -n "$CONV_ID" ]; then
                echo "Conversation: $CONV_ID"
            else
                echo "No active conversation found for $WORKDIR"
            fi
        else
            echo "Database not found: $DB"
        fi
        ;;
        
    codex)
        # Codex: ~/.codex/sessions/<session-uuid>/
        # Find by checking open files or recent sessions
        SESSION_DIR=$(lsof -p "$PID" 2>/dev/null | grep "\.codex/sessions" | awk '{print $NF}' | head -1 | xargs dirname 2>/dev/null)
        
        if [ -z "$SESSION_DIR" ]; then
            # Fallback: find most recent session in workdir
            SESSION_DIR=$(find "$HOME/.codex/sessions" -name "cwd" -exec grep -l "^$WORKDIR$" {} \; 2>/dev/null | head -1 | xargs dirname 2>/dev/null)
        fi
        
        if [ -n "$SESSION_DIR" ]; then
            SESSION_ID=$(basename "$SESSION_DIR")
            echo "Session dir: $SESSION_DIR"
            echo "Session ID: $SESSION_ID"
            echo "Last modified: $(stat -c %y "$SESSION_DIR" 2>/dev/null)"
        else
            echo "Session directory not found"
        fi
        ;;
        
    gemini)
        # Gemini CLI: typically doesn't persist sessions to disk
        # Check if it has a config file
        CONFIG="$HOME/.config/gemini/config.json"
        if [ -f "$CONFIG" ]; then
            echo "Config: $CONFIG"
            echo "Note: Gemini CLI typically doesn't persist session history"
        else
            echo "No persistent session (Gemini CLI is stateless by default)"
        fi
        ;;
        
    aider)
        # Aider: .aider.chat.history.md in project root
        HISTORY_FILE="$WORKDIR/.aider.chat.history.md"
        if [ -f "$HISTORY_FILE" ]; then
            echo "History file: $HISTORY_FILE"
            echo "Last modified: $(stat -c %y "$HISTORY_FILE" 2>/dev/null)"
        else
            echo "No history file found (may be using --no-auto-commits)"
        fi
        ;;
        
    *)
        echo "Unknown AI type: $CMD"
        echo "Cannot determine session info"
        exit 1
        ;;
esac
