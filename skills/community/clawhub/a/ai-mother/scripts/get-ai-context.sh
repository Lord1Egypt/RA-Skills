#!/bin/bash
# Get full execution context for any AI agent process
# Supports: Claude Code, OpenCode, Codex
# Usage: ./get-ai-context.sh <PID>

PID=${1:-}
if [ -z "$PID" ]; then
    echo "Usage: $0 <PID>"
    exit 1
fi

if ! ps -p "$PID" > /dev/null 2>&1; then
    echo "Error: Process $PID not found"
    exit 1
fi

WORKDIR=$(pwdx "$PID" 2>/dev/null | cut -d: -f2 | xargs)
STATE=$(ps -o stat= -p "$PID" | head -c 1)
ELAPSED=$(ps -o etime= -p "$PID" | xargs)
CMD=$(ps -o cmd= -p "$PID")
TTY=$(ps -o tty= -p "$PID" | xargs)
AI_TYPE="unknown"

# Detect AI type
case "$CMD" in
    *claude*) AI_TYPE="claude" ;;
    *opencode*) AI_TYPE="opencode" ;;
    *codex*) AI_TYPE="codex" ;;
    *gemini*) AI_TYPE="gemini" ;;
    *pi\ *|*/pi) AI_TYPE="pi" ;;
esac

echo "=== AI Agent Context: PID $PID ==="
echo "Type:     $AI_TYPE"
echo "State:    $STATE | Runtime: $ELAPSED"
echo "Command:  $CMD"
echo "Workdir:  $WORKDIR"
echo "TTY:      $TTY"
echo ""

# ─── Last Output by AI type ───────────────────────────────────────────────────

echo "--- Last Output ---"

if [ "$AI_TYPE" = "claude" ]; then
    # Claude Code: reads ~/.claude/projects/<encoded-path>/*.jsonl
    SAFE_PATH=$(echo "$WORKDIR" | sed 's|/|-|g' | sed 's|^-||')
    SESSION_DIR="$HOME/.claude/projects/$SAFE_PATH"
    LATEST=""
    [ -d "$SESSION_DIR" ] && LATEST=$(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -1)

    # Fallback: search all projects for workdir reference, sort by modification time
    if [ -z "$LATEST" ]; then
        LATEST=$(find "$HOME/.claude/projects" -name "*.jsonl" -type f 2>/dev/null \
            | xargs grep -l "$WORKDIR" 2>/dev/null \
            | xargs ls -t 2>/dev/null \
            | head -1)
    fi

    if [ -n "$LATEST" ]; then
        echo "Session: $LATEST"
        tail -6 "$LATEST" 2>/dev/null | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        d = json.loads(line.strip())
        # Handle progress type (tool execution in flight)
        if d.get('type') == 'progress':
            msg = d.get('data', {}).get('message', {})
            for b in msg.get('content', []):
                if isinstance(b, dict) and b.get('type') == 'tool_use':
                    inp = b.get('input', {})
                    cmd = inp.get('command', inp.get('description', str(inp)[:100]))
                    print(f'[progress]: {b.get(\"name\")} - {cmd[:200]}')
            continue
        role = d.get('role','?')
        content = d.get('message', d).get('content', '')
        if isinstance(content, list):
            for b in content:
                if isinstance(b, dict):
                    if b.get('type') == 'text':
                        print(f'[{role}]: {b[\"text\"][:600]}')
                    elif b.get('type') == 'tool_use':
                        print(f'[{role}/tool]: {b.get(\"name\")} {str(b.get(\"input\",{}))[:200]}')
        elif isinstance(content, str) and content:
            print(f'[{role}]: {content[:600]}')
        err = d.get('error') or d.get('message', {}).get('error')
        if err:
            print(f'[ERROR]: {err}')
    except: pass
" 2>/dev/null
    else
        echo "(no session file found for $WORKDIR)"
    fi

elif [ "$AI_TYPE" = "opencode" ]; then
    # OpenCode: SQLite at ~/.local/share/opencode/opencode.db
    DB="$HOME/.local/share/opencode/opencode.db"
    if [ -f "$DB" ]; then
        echo "DB: $DB"
        # Get last 3 messages (user + assistant)
        sqlite3 "$DB" "
SELECT m.id, m.data FROM message m
ORDER BY m.time_updated DESC LIMIT 6;" 2>/dev/null | while IFS='|' read -r mid mdata; do
            ROLE=$(echo "$mdata" | python3 -c "import sys,json; d=json.loads(sys.stdin.read()); print(d.get('role','?'))" 2>/dev/null)
            # Get text parts for this message
            PARTS=$(sqlite3 "$DB" "SELECT data FROM part WHERE message_id='$mid' ORDER BY time_created;" 2>/dev/null)
            TEXT=$(echo "$PARTS" | python3 -c "
import sys, json
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    try:
        d = json.loads(line)
        if d.get('type') == 'text':
            t = d.get('text','').strip()
            if t: print(t[:500])
        elif d.get('type') == 'tool-invocation':
            name = d.get('toolInvocation',{}).get('toolName','?')
            state = d.get('toolInvocation',{}).get('state','?')
            print(f'[tool:{name} state:{state}]')
        elif d.get('type') == 'error':
            print(f'[ERROR]: {d.get(\"error\",d)[:300]}')
    except: pass
" 2>/dev/null)
            [ -n "$TEXT" ] && echo "[$ROLE]: $TEXT" && echo "---"
        done
    else
        echo "(opencode.db not found)"
    fi

elif [ "$AI_TYPE" = "codex" ]; then
    # Codex: ~/.codex/sessions/
    SESSION_DIR="$HOME/.codex/sessions"
    if [ -d "$SESSION_DIR" ]; then
        LATEST=$(ls -t "$SESSION_DIR"/*.json 2>/dev/null | head -1)
        if [ -n "$LATEST" ]; then
            echo "Session: $LATEST"
            python3 -c "
import json, sys
with open('$LATEST') as f:
    data = json.load(f)
msgs = data if isinstance(data, list) else data.get('messages', [])
for m in msgs[-4:]:
    role = m.get('role','?')
    content = m.get('content','')
    if isinstance(content, list):
        for b in content:
            if isinstance(b,dict) and b.get('type')=='text':
                print(f'[{role}]: {b[\"text\"][:500]}')
    elif isinstance(content, str):
        print(f'[{role}]: {content[:500]}')
" 2>/dev/null
        else
            echo "(no codex session files)"
        fi
    else
        echo "(~/.codex/sessions not found)"
    fi

else
    echo "(unsupported AI type: $AI_TYPE — cannot read session)"
fi

echo ""

# ─── Recent file changes ──────────────────────────────────────────────────────
echo "--- Recent File Changes (last 2h) ---"
find "$WORKDIR" -type f -mmin -120 \
    ! -path "*/.git/*" ! -path "*/node_modules/*" ! -path "*/__pycache__/*" \
    ! -path "*/.claude/*" \
    2>/dev/null | xargs ls -lt 2>/dev/null | head -15
echo ""

# ─── Git status ───────────────────────────────────────────────────────────────
echo "--- Git Status ---"
git -C "$WORKDIR" status --short 2>/dev/null | head -20 || echo "(not a git repo)"
git -C "$WORKDIR" log --oneline -3 2>/dev/null
echo ""

# ─── Open files ───────────────────────────────────────────────────────────────
echo "--- Open Files (active work) ---"
lsof -p "$PID" 2>/dev/null | awk 'NR>1 {print $NF}' | \
    grep -v "^/proc\|^/usr\|^/lib\|^/dev\|node_modules\|\.so\|/sys\|/run\|^$\|(ESTABLISHED\|(CONNECTED\|eventfd\|eventpoll\|inotify\|io_uring\|directory" | \
    sort -u | head -15
echo ""

# ─── Error logs ───────────────────────────────────────────────────────────────
echo "--- Recent Logs ---"
find "$WORKDIR" -name "*.log" -mmin -120 2>/dev/null | while read -r f; do
    echo "[$(basename $f)]"
    tail -8 "$f" 2>/dev/null
    echo ""
done

echo "=== End of Context ==="
