#!/bin/bash
# Session End Hook - v2.0
# 会话结束时强制保存关键信息 + 检查未保存内容

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
FACTS_DIR="$WORKSPACE/memory/facts"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/logs/session-hook.log}"
ALERT_FILE="$WORKSPACE/.session-alert"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

TODAY=$(date '+%Y-%m-%d')

log "=== Session End Hook v2.0 ==="

# 1. 统计今日事实提取
FACTS_COUNT=0
for category in preferences decisions tasks important time relationships; do
    tsv="$FACTS_DIR/${category}.tsv"
    if [ -f "$tsv" ]; then
        count=$(grep -c "^$TODAY" "$tsv" 2>/dev/null || echo 0)
        FACTS_COUNT=$((FACTS_COUNT + count))
    fi
done

log "📊 Total facts identified today: $FACTS_COUNT"

# 2. 检查 MEMORY.md 是否有今日更新
MEMORY_UPDATED=false
if grep -q "$TODAY" "$MEMORY_FILE" 2>/dev/null; then
    MEMORY_UPDATED=true
    log "✅ MEMORY.md contains today's updates"
else
    log "⚠️ MEMORY.md missing today's updates"
fi

# 3. 检查 daily note 是否存在且有内容
DAILY_NOTE="$WORKSPACE/memory/$TODAY.md"
DAILY_UPDATED=false
if [ -f "$DAILY_NOTE" ]; then
    lines=$(wc -l < "$DAILY_NOTE" 2>/dev/null || echo 0)
    if [ "$lines" -gt 10 ]; then
        DAILY_UPDATED=true
        log "✅ Daily note has content ($lines lines)"
    else
        log "⚠️ Daily note exists but minimal content ($lines lines)"
    fi
else
    log "⚠️ Daily note not found: $DAILY_NOTE"
fi

# 4. 🆕 检查会话文件中的潜在重要内容
check_unsaved_content() {
    local session_dir="$HOME/.openclaw/agents/main/sessions"
    local potential_count=0
    local keywords=("重要" "决定" "记住" "TODO" "待办" "偏好" "喜欢" "讨厌")
    
    # 找到最近修改的会话文件
    local recent_session=$(find "$session_dir" -name "*.jsonl" -mmin -30 -type f 2>/dev/null | head -1)
    
    if [ -n "$recent_session" ]; then
        for keyword in "${keywords[@]}"; do
            count=$(grep -c "$keyword" "$recent_session" 2>/dev/null || echo 0)
            if [ "$count" -gt 0 ]; then
                potential_count=$((potential_count + count))
            fi
        done
    fi
    
    echo $potential_count
}

UNSAVED_POTENTIAL=$(check_unsaved_content)
log "🔍 Potential unsaved important content: $UNSAVED_POTENTIAL occurrences"

# 5. 🆕 生成警告文件（如果需要）
if [ "$MEMORY_UPDATED" = false ] || [ "$DAILY_UPDATED" = false ] || [ "$UNSAVED_POTENTIAL" -gt 5 ]; then
    cat > "$ALERT_FILE" << EOF
# ⚠️ Session Memory Alert - $TODAY

## Status
- MEMORY.md updated: $MEMORY_UPDATED
- Daily note updated: $DAILY_UPDATED
- Potential unsaved content: $UNSAVED_POTENTIAL occurrences

## Action Required
请在下次会话开始时：
1. 检查 MEMORY.md 是否需要更新
2. 检查 memory/$TODAY.md 是否记录了重要内容
3. 回顾上次会话是否有遗漏的重要信息

## Recent Session Files
$(find "$HOME/.openclaw/agents/main/sessions" -name "*.jsonl" -mmin -60 -type f 2>/dev/null | head -3)

---
Generated at: $(date '+%Y-%m-%d %H:%M:%S')
EOF
    log "⚠️ Alert file generated: $ALERT_FILE"
fi

# 6. 触发 summary 生成（如果今天还没有）
SUMMARY_FILE="$WORKSPACE/memory/summaries/$TODAY.md"
if [ ! -f "$SUMMARY_FILE" ]; then
    log "Generating today's summary..."
    "$WORKSPACE/skills/context-compression/generate-smart-summary.sh" 2>/dev/null
fi

log "✅ Session end hook completed"

# 7. 🆕 输出摘要（供 AI 读取）
echo "📊 Session End Summary:"
echo "  - Facts identified today: $FACTS_COUNT"
echo "  - MEMORY.md updated: $MEMORY_UPDATED"
echo "  - Daily note updated: $DAILY_UPDATED"
echo "  - Potential unsaved content: $UNSAVED_POTENTIAL"
echo "  - Summary generated: $([ -f "$SUMMARY_FILE" ] && echo 'Yes' || echo 'No')"

# 8. 🆕 如果有警告，输出警告标记
if [ -f "$ALERT_FILE" ]; then
    echo ""
    echo "⚠️ MEMORY ALERT: Check $ALERT_FILE for details"
fi
