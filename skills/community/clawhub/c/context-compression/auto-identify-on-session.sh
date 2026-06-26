#!/bin/bash
# Auto Identify on Session Change - v1.0
# 监听 session 文件变化，自动提取并写入 memory

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
FACTS_DIR="$WORKSPACE/memory/facts"
SESSION_DIR="$HOME/.openclaw/agents/main/sessions"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/logs/auto-identify.log}"

mkdir -p "$FACTS_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

TODAY=$(date '+%Y-%m-%d')
DAILY_NOTE="$WORKSPACE/memory/$TODAY.md"

# 提取最新会话中的关键内容
collect_latest_content() {
    local session_file=$(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -1)
    [ -z "$session_file" ] && return
    
    # 获取最后 50 行（最近内容）
    local recent_content=$(tail -50 "$session_file" 2>/dev/null)
    
    # 提取用户消息（role: user）
    local user_messages=$(echo "$recent_content" | grep -o '"role":"user"[^}]*"content":"[^"]*"' | \
        sed 's/.*"content":"\([^"]*\)".*/\1/g' | head -10)
    
    echo "$user_messages"
}

# 检测重要模式并生成 memory 条目
detect_and_format() {
    local text=$1
    local entries=""
    
    # 偏好
    if echo "$text" | grep -qE "(我喜欢|我偏好|我讨厌|我反感)"; then
        entries+="[PREFERENCE] $text\n"
    fi
    
    # 决定
    if echo "$text" | grep -qE "(决定了|确定是|选定|就选|定下了)"; then
        entries+="[DECISION] $text\n"
    fi
    
    # 重要提醒
    if echo "$text" | grep -qE "(重要|记住|别忘了|务必|千万)"; then
        entries+="[IMPORTANT] $text\n"
    fi
    
    # TODO/任务
    if echo "$text" | grep -qE "(TODO|待办|要完成|需要做)"; then
        entries+="[TASK] $text\n"
    fi
    
    echo -e "$entries"
}

# 写入 daily note
write_to_daily_note() {
    local content=$1
    [ -z "$content" ] && return
    
    local timestamp=$(date '+%H:%M')
    
    # 确保 daily note 存在
    [ ! -f "$DAILY_NOTE" ] && echo "# $TODAY Daily Notes" > "$DAILY_NOTE"
    
    # 追加内容
    echo "" >> "$DAILY_NOTE"
    echo "## [$timestamp] Auto-collected" >> "$DAILY_NOTE"
    echo -e "$content" >> "$DAILY_NOTE"
    
    log "📝 Written to daily note: $(echo -e "$content" | wc -l) lines"
}

# 主逻辑
main() {
    log "=== Auto Identify Check ==="
    
    local latest=$(collect_latest_content)
    [ -z "$latest" ] && log "No content to identify" && return
    
    local entries=$(detect_and_format "$latest")
    
    if [ -n "$entries" ]; then
        write_to_daily_note "$entries"
        echo "Identifyed: $entries"
    else
        log "No important patterns detected"
    fi
}

main
