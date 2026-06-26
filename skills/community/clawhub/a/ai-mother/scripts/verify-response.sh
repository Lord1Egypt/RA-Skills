#!/bin/bash
# Verify that AI received and responded to a message
# Supports: Claude Code, OpenCode, Codex, Aider
# Usage: ./verify-response.sh <PID> <expected_keyword> [timeout_seconds]
#
# Returns:
#   0 - AI responded with expected keyword
#   1 - Timeout or no response
#   2 - AI responded but without expected keyword (possible misunderstanding)

PID=$1
KEYWORD=$2
TIMEOUT=${3:-10}  # Default 10 seconds

if [ -z "$PID" ] || [ -z "$KEYWORD" ]; then
    echo "Usage: $0 <PID> <expected_keyword> [timeout_seconds]"
    exit 1
fi

if ! ps -p "$PID" > /dev/null 2>&1; then
    echo "Error: Process $PID not found"
    exit 1
fi

WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)
CMD=$(ps -o cmd= -p "$PID" | awk '{print $1}' | xargs basename)

echo "🔍 Verifying response from PID $PID ($CMD, expecting: '$KEYWORD', timeout: ${TIMEOUT}s)"

# ─── Get baseline timestamp ───────────────────────────────────────────────────
get_last_message_time() {
    case "$CMD" in
        claude)
            # Claude Code: ~/.claude/projects/<path>/<session-id>.jsonl
            LATEST=$(find "$HOME/.claude/projects" -type f -name "*.jsonl" -exec grep -l "\"$WORKDIR\"" {} \; 2>/dev/null | xargs ls -t 2>/dev/null | head -1)
            [ -n "$LATEST" ] && stat -c %Y "$LATEST" 2>/dev/null || echo "0"
            ;;
        opencode)
            # OpenCode: SQLite database
            DB="$HOME/.local/share/opencode/opencode.db"
            [ -f "$DB" ] && stat -c %Y "$DB" 2>/dev/null || echo "0"
            ;;
        codex)
            # Codex: ~/.codex/sessions/<uuid>/
            SESSION_DIR=$(lsof -p "$PID" 2>/dev/null | grep "\.codex/sessions" | awk '{print $NF}' | head -1 | xargs dirname 2>/dev/null)
            [ -n "$SESSION_DIR" ] && find "$SESSION_DIR" -type f -name "*.json" -o -name "*.log" 2>/dev/null | xargs ls -t 2>/dev/null | head -1 | xargs stat -c %Y 2>/dev/null || echo "0"
            ;;
        aider)
            # Aider: .aider.chat.history.md
            HISTORY="$WORKDIR/.aider.chat.history.md"
            [ -f "$HISTORY" ] && stat -c %Y "$HISTORY" 2>/dev/null || echo "0"
            ;;
        *)
            echo "0"
            ;;
    esac
}

BASELINE_TIME=$(get_last_message_time)
START_TIME=$(date +%s)

# ─── Poll for new response ────────────────────────────────────────────────────
while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    
    if [ $ELAPSED -ge $TIMEOUT ]; then
        echo "⏱️  Timeout: No response after ${TIMEOUT}s"
        exit 1
    fi
    
    CURRENT_MSG_TIME=$(get_last_message_time)
    
    # New message detected
    if [ "$CURRENT_MSG_TIME" -gt "$BASELINE_TIME" ]; then
        echo "✅ New response detected"
        
        # Extract last response based on AI type
        LAST_RESPONSE=""
        
        case "$CMD" in
            claude)
                LATEST=$(find "$HOME/.claude/projects" -type f -name "*.jsonl" -exec grep -l "\"$WORKDIR\"" {} \; 2>/dev/null | xargs ls -t 2>/dev/null | head -1)
                LAST_RESPONSE=$(tail -10 "$LATEST" 2>/dev/null | python3 -c "
import sys, json
responses = []
for line in sys.stdin:
    try:
        d = json.loads(line.strip())
        if d.get('type') == 'assistant':
            content = d.get('message', {}).get('content', '')
            if isinstance(content, list):
                for b in content:
                    if isinstance(b, dict) and b.get('type') == 'text':
                        responses.append(b['text'])
            elif isinstance(content, str):
                responses.append(content)
    except: pass
if responses:
    print(responses[-1])
" 2>/dev/null)
                ;;
                
            opencode)
                DB="$HOME/.local/share/opencode/opencode.db"
                LAST_RESPONSE=$(sqlite3 "$DB" "
                    SELECT m.data FROM message m
                    JOIN conversation c ON m.conversation_id = c.id
                    WHERE c.workdir = '$WORKDIR'
                    ORDER BY m.time_updated DESC LIMIT 1;
                " 2>/dev/null | python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    if d.get('role') == 'assistant':
        parts = d.get('parts', [])
        print(' '.join(p.get('text', '') for p in parts if isinstance(p, dict)))
except: pass
" 2>/dev/null)
                ;;
                
            codex)
                SESSION_DIR=$(lsof -p "$PID" 2>/dev/null | grep "\.codex/sessions" | awk '{print $NF}' | head -1 | xargs dirname 2>/dev/null)
                if [ -n "$SESSION_DIR" ]; then
                    LAST_RESPONSE=$(find "$SESSION_DIR" -name "*.json" -exec cat {} \; 2>/dev/null | jq -r '.messages[] | select(.role == "assistant") | .content' 2>/dev/null | tail -1)
                fi
                ;;
                
            aider)
                HISTORY="$WORKDIR/.aider.chat.history.md"
                # Extract last assistant response from markdown
                LAST_RESPONSE=$(tac "$HISTORY" 2>/dev/null | awk '/^####/ {if (found) exit; if (/Assistant/) found=1; next} found {print}' | tac)
                ;;
        esac
        
        # Check if response contains keyword
        if [ -n "$LAST_RESPONSE" ] && echo "$LAST_RESPONSE" | grep -qi "$KEYWORD"; then
            echo "✅ Response contains expected keyword: '$KEYWORD'"
            echo ""
            echo "--- Response Preview ---"
            echo "$LAST_RESPONSE" | head -c 300
            echo ""
            exit 0
        elif [ -n "$LAST_RESPONSE" ]; then
            echo "⚠️  Response received but doesn't contain '$KEYWORD'"
            echo ""
            echo "--- Response Preview ---"
            echo "$LAST_RESPONSE" | head -c 300
            echo ""
            exit 2
        else
            echo "⚠️  Response detected but couldn't extract content"
            exit 2
        fi
    fi
    
    sleep 1
done
