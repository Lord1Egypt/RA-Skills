#!/bin/bash
# Session Start Hook - v1.0
# 会话开始时自动检查并加载上下文

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
FACTS_DIR="$WORKSPACE/memory/facts"
SUMMARIES_DIR="$WORKSPACE/memory/summaries"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/logs/session-hook.log}"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

TODAY=$(date '+%Y-%m-%d')
YESTERDAY=$(date -d "yesterday" '+%Y-%m-%d' 2>/dev/null || date -v-1d '+%Y-%m-%d' 2>/dev/null)

log "=== Session Start Hook ==="

# 1. 检查 MEMORY.md 存在
if [ ! -f "$MEMORY_FILE" ]; then
    log "⚠️ MEMORY.md not found, creating..."
    cat > "$MEMORY_FILE" << 'EOF'
# MEMORY.md - Long-Term Memory

> Your curated memories. Distill from daily notes. Remove when outdated.

---

## About User

[User info will be populated automatically]

---

*Last updated: $(date '+%Y-%m-%d')*
EOF
fi

# 2. 检查 today's daily note
TODAY_NOTE="$WORKSPACE/memory/$TODAY.md"
if [ ! -f "$TODAY_NOTE" ]; then
    log "Creating today's daily note: $TODAY_NOTE"
    cat > "$TODAY_NOTE" << EOF
# $TODAY Daily Notes

## Session Start
- Time: $(date '+%H:%M')
- Status: Ready

---

EOF
fi

# 3. 检查 facts 目录
if [ ! -d "$FACTS_DIR" ]; then
    log "Creating facts directory structure"
    mkdir -p "$FACTS_DIR"
    for category in preferences decisions tasks important time relationships; do
        touch "$FACTS_DIR/${category}.log"
        touch "$FACTS_DIR/${category}.tsv"
    done
fi

# 4. 加载关键事实到环境变量（可选，供 agent 读取）
export RECENT_PREFERENCES=$(tail -5 "$FACTS_DIR/preferences.log" 2>/dev/null || echo "")
export RECENT_DECISIONS=$(tail -5 "$FACTS_DIR/decisions.log" 2>/dev/null || echo "")
export RECENT_TASKS=$(tail -5 "$FACTS_DIR/tasks.log" 2>/dev/null || echo "")

# 5. 输出上下文摘要
echo "📋 Session Context Summary:"
echo "  - MEMORY.md: $(wc -l < "$MEMORY_FILE" 2>/dev/null || echo 0) lines"
echo "  - Daily note: $TODAY_NOTE"
echo "  - Recent facts: $(ls "$FACTS_DIR"/*.tsv 2>/dev/null | wc -l) categories"
echo "  - Summaries: $(ls "$SUMMARIES_DIR"/*.md 2>/dev/null | wc -l) files"

log "✅ Session context ready"
