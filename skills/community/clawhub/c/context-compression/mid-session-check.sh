#!/bin/bash
# Mid-Session Check - v1.0
# 会话过程中定期检查是否有未保存的重要内容

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
FACTS_DIR="$WORKSPACE/memory/facts"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/logs/session-hook.log}"

TODAY=$(date '+%Y-%m-%d')
TODAY_NOTE="$WORKSPACE/memory/$TODAY.md"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 检查当前会话中的重要关键词
check_session_keywords() {
    local session_file="$1"
    local keywords=(
        "重要"
        "决定"
        "记住"
        "别忘了"
        "TODO"
        "待办"
        "偏好"
        "我喜欢"
        "我讨厌"
        "千万"
        "务必"
    )
    
    local found_keywords=""
    
    for kw in "${keywords[@]}"; do
        if grep -q "$kw" "$session_file" 2>/dev/null; then
            found_keywords="$found_keywords $kw"
        fi
    done
    
    echo "$found_keywords"
}

# 检查 daily note 是否最近更新过
check_daily_note_freshness() {
    if [ ! -f "$TODAY_NOTE" ]; then
        echo "NOT_FOUND"
        return
    fi
    
    local note_mtime=$(stat -c%Y "$TODAY_NOTE" 2>/dev/null || stat -f%m "$TODAY_NOTE" 2>/dev/null)
    local now=$(date +%s)
    local age_minutes=$(( (now - note_mtime) / 60 ))
    
    if [ $age_minutes -lt 5 ]; then
        echo "FRESH"
    elif [ $age_minutes -lt 30 ]; then
        echo "RECENT"
    else
        echo "STALE"
    fi
}

# 主逻辑
main() {
    log "=== Mid-Session Check ==="
    
    local session_dir="$HOME/.openclaw/agents/main/sessions"
    local current_session=$(ls -t "$session_dir"/*.jsonl 2>/dev/null | head -1)
    
    if [ -z "$current_session" ]; then
        log "No session file found"
        echo "NO_SESSION"
        return
    fi
    
    # 检查关键词
    local keywords_found=$(check_session_keywords "$current_session")
    
    # 检查 daily note 新鲜度
    local note_status=$(check_daily_note_freshness)
    
    # 输出 JSON 格式的结果（方便 AI 解析）
    cat << EOF
{
  "session_file": "$(basename "$current_session")",
  "keywords_found": "$keywords_found",
  "daily_note_status": "$note_status",
  "recommendation": "$([ -n "$keywords_found" ] && echo "SAVE_NOW" || echo "OK")"
}
EOF
    
    # 如果发现关键词且 daily note 不是新鲜的，记录警告
    if [ -n "$keywords_found" ] && [ "$note_status" = "STALE" ]; then
        log "⚠️ Important keywords detected but daily note is stale"
        log "   Keywords: $keywords_found"
    fi
}

main
