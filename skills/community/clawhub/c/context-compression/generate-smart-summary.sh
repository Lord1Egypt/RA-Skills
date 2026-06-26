#!/bin/bash
# Generate Smart Summary - v2.0
# 智能压缩每日笔记，提取核心信息

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
SUMMARIES_DIR="$MEMORY_DIR/summaries"
FACTS_DIR="$MEMORY_DIR/facts"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/logs/summary.log}"

# Ensure directories exist
mkdir -p "$SUMMARIES_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo "$1"
}

# Get date
TODAY=$(date '+%Y-%m-%d')
DAILY_NOTE="$MEMORY_DIR/$TODAY.md"
SUMMARY_FILE="$SUMMARIES_DIR/$TODAY.md"

log "=== Smart Summary Generation ==="
log "Date: $TODAY"

# Check if daily note exists
if [ ! -f "$DAILY_NOTE" ]; then
    log "No daily note found for today"
    exit 0
fi

# Read daily note
NOTE_CONTENT=$(cat "$DAILY_NOTE")
NOTE_LINES=$(echo "$NOTE_CONTENT" | wc -l)

log "Daily note: $NOTE_LINES lines"

# ===== 智能压缩策略 =====

# 1. 提取标题（# 开头的行）
collect_headers() {
    grep '^#' "$DAILY_NOTE" 2>/dev/null || echo ""
}

# 2. 提取任务状态
collect_tasks() {
    grep -E '^- \[[ x]\]' "$DAILY_NOTE" 2>/dev/null || echo ""
}

# 3. 提取重要标记
collect_important() {
    grep -E '(重要|关键|TODO|待办|记住)' "$DAILY_NOTE" 2>/dev/null || echo ""
}

# 4. 从 facts 目录提取今日事实
identify_facts() {
    local facts=""
    for category in preferences decisions tasks important time relationships; do
        local tsv_file="$FACTS_DIR/${category}.tsv"
        if [ -f "$tsv_file" ]; then
            local today_facts=$(grep "^$TODAY" "$tsv_file" 2>/dev/null)
            if [ -n "$today_facts" ]; then
                facts+="### ${category^}\n"
                facts+=$(echo "$today_facts" | cut -d'|' -f3 | sed 's/^/- /')
                facts+="\n\n"
            fi
        fi
    done
    echo -e "$facts"
}

# 5. 统计信息
get_stats() {
    local total_lines=$1
    local tasks_done=$(grep -c '^\- \[x\]' "$DAILY_NOTE" 2>/dev/null || echo 0)
    local tasks_pending=$(grep -c '^\- \[ \]' "$DAILY_NOTE" 2>/dev/null || echo 0)
    
    echo "📊 统计: $total_lines 行 | ✅ $tasks_done 完成 | 📋 $tasks_pending 待办"
}

# ===== 生成摘要 =====

HEADERS=$(collect_headers)
TASKS=$(collect_tasks)
IMPORTANT=$(collect_important)
FACTS=$(identify_facts)
STATS=$(get_stats $NOTE_LINES)

cat > "$SUMMARY_FILE" << EOF
# 📝 摘要 - $TODAY

> 自动生成，压缩自 memory/$TODAY.md
> 生成时间: $(date '+%Y-%m-%d %H:%M:%S')

## 📊 统计
$STATS

## 📑 主要内容

$HEADERS

## ✅ 任务状态

$TASKS

## ⚠️ 重要事项

$IMPORTANT

## 💎 提取的事实

$FACTS

---

## 原文摘要（前 500 字符）

$(echo "$NOTE_CONTENT" | head -c 500)...

---

*Char 估算: ~$((${#HEADERS} / 3 + ${#TASKS} / 3 + ${#IMPORTANT} / 3 + ${#FACTS} / 3)) chars*
EOF

log "✅ Summary generated: $SUMMARY_FILE"

# Clean up old summaries (keep last 30 days)
find "$SUMMARIES_DIR" -name "*.md" -mtime +30 -delete 2>/dev/null
log "Cleaned up summaries older than 30 days"
