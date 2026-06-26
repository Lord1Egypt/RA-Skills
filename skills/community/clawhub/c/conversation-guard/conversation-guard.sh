#!/bin/bash
# DreamMoon-Conversation-Guard
# A self-contained conversation backup system for OpenClaw
# 
# 一个自成体系的OpenClaw对话备份系统
#
# Usage:
#   source conversation-guard.sh
#   record_interaction "User message" "Assistant response" [importance] [tags]
#
# Author: zfanmy \ 梦月儿 (DreamMoon) 🌙
# Version: 1.0.0
# License: MIT

set -e

# Configuration
GUARDIAN_VERSION="1.0.0"
GUARDIAN_DIR="${GUARDIAN_DIR:-$HOME/.openclaw/workspace/memory/.guardian}"
MEMORY_DIR="${MEMORY_DIR:-$HOME/.openclaw/workspace/memory}"

# Get today's date
TODAY=$(date +%Y-%m-%d)
TODAY_FILE="${MEMORY_DIR}/${TODAY}.md"
BACKUP_FILE="${GUARDIAN_DIR}/.backup_${TODAY}.jsonl"

# Initialize guardian
guardian_init() {
    # Create directories
    mkdir -p "$GUARDIAN_DIR"
    mkdir -p "$MEMORY_DIR"
    
    # Initialize today's markdown file if not exists
    if [ ! -f "$TODAY_FILE" ]; then
        printf "%s\n" "# 📋 ${TODAY} 对话记录 | Conversation Log" "" "> 🛡️ Protected by DreamMoon-Conversation-Guard v${GUARDIAN_VERSION}" "> 🌙 Our conversations, never lost | 我们的对话，永不丢失" "" "---" "" > "$TODAY_FILE"
    fi
    
    # Check for session reset
    local session_marker="${GUARDIAN_DIR}/.current_session"
    if [ -f "$session_marker" ]; then
        local last_session=$(cat "$session_marker")
        local current_time=$(date +%s)
        local time_diff=$((current_time - last_session))
        
        # If gap > 5 minutes, likely a new session
        if [ $time_diff -gt 300 ]; then
            {
                echo ""
                echo "<!-- ⚠️ New session detected | 检测到新会话 - $(date '+%Y-%m-%d %H:%M:%S') -->"
                echo ""
            } >> "$TODAY_FILE"
        fi
    fi
    
    # Update session marker
    date +%s > "$session_marker"
}

# Record a single interaction
record_interaction() {
    local user_msg="$1"
    local assistant_msg="$2"
    local importance="${3:-5}"
    local tags="${4:-normal}"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Ensure directories exist
    if [ -n "$GUARDIAN_DIR" ] && [ -n "$MEMORY_DIR" ]; then
        mkdir -p "$GUARDIAN_DIR"
        mkdir -p "$MEMORY_DIR"
    fi
    
    # Escape for JSON
    local user_json=$(echo "$user_msg" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' 2>/dev/null || echo "\"$user_msg\"")
    local assistant_json=$(echo "$assistant_msg" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))' 2>/dev/null || echo "\"$assistant_msg\"")
    
    # Write to JSONL backup
    echo "{\"t\":\"$timestamp\",\"r\":\"user\",\"c\":$user_json,\"i\":$importance,\"g\":\"$tags\"}" >> "$BACKUP_FILE"
    echo "{\"t\":\"$timestamp\",\"r\":\"assistant\",\"c\":$assistant_json,\"i\":$importance,\"g\":\"$tags\"}" >> "$BACKUP_FILE"
    
    # Write to Markdown (human-readable)
    {
        echo "**👤 USER** ($timestamp)"
        echo ""
        echo "$user_msg"
        echo ""
        echo "**🌙 ASSISTANT** ($timestamp)"
        echo ""
        echo "$assistant_msg"
        echo ""
        
        # Add emotional marker for high importance
        if [ "$importance" -ge 8 ]; then
            echo "<!-- 💝 High importance [$importance] | 高重要性: $tags -->"
            echo ""
        fi
        
        echo "---"
        echo ""
    } >> "$TODAY_FILE"
    
    # Emergency log for critical conversations
    if [ "$importance" -ge 9 ]; then
        echo "$(date '+%Y%m%d_%H%M%S') [IMPORTANCE:$importance] [$tags]" >> "${GUARDIAN_DIR}/.emergency_log.txt"
    fi
}

# Mark a message as emotionally significant
mark_emotional() {
    local note="$1"
    local intensity="${2:-7}"
    local tags="${3:-significant}"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "<!-- 💝 EMOTIONAL [$timestamp] intensity=$intensity tags=$tags: $note -->" >> "$TODAY_FILE"
}

# Create emergency backup
emergency_backup() {
    local timestamp=$(date '+%Y%m%d_%H%M%S')
    local backup_path="${GUARDIAN_DIR}/.emergency_backup_${timestamp}.md"
    
    if [ -f "$TODAY_FILE" ]; then
        cp "$TODAY_FILE" "$backup_path"
        echo "✅ Emergency backup created: $backup_path"
    else
        echo "⚠️ No conversation file to backup"
    fi
}

# Recover from JSONL backup
recover_from_backup() {
    if [ -f "$BACKUP_FILE" ]; then
        echo "🔄 Found backup file: $BACKUP_FILE"
        echo "Recent entries:"
        tail -10 "$BACKUP_FILE"
    else
        echo "⚠️ No backup file found"
    fi
}

# Detect session reset
guardian_detect_reset() {
    local session_marker="${GUARDIAN_DIR}/.current_session"
    if [ -f "$session_marker" ]; then
        local last_session=$(cat "$session_marker")
        local current_time=$(date +%s)
        local time_diff=$((current_time - last_session))
        
        if [ $time_diff -gt 300 ]; then
            return 0  # Reset detected
        fi
    fi
    return 1  # No reset
}

# Recover context after reset
guardian_recover_context() {
    if [ -f "$BACKUP_FILE" ]; then
        local last_user=$(tail -2 "$BACKUP_FILE" | head -1)
        local last_assistant=$(tail -1 "$BACKUP_FILE")
        
        # Extract content (simplified)
        echo "🔄 Last conversation context recovered from backup"
        echo "User: $(echo "$last_user" | grep -o '"c":[^,]*' | head -1)"
    fi
}

# Show status
guardian_status() {
    echo "🌙 DreamMoon-Conversation-Guard v${GUARDIAN_VERSION}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Memory dir: $MEMORY_DIR"
    echo "Guardian dir: $GUARDIAN_DIR"
    echo "Today's file: $TODAY_FILE"
    echo "Backup file: $BACKUP_FILE"
    
    if [ -f "$TODAY_FILE" ]; then
        local lines=$(wc -l < "$TODAY_FILE")
        echo "Today's conversations: ~$(( (lines - 10) / 5 )) entries"
    fi
    
    if [ -f "$BACKUP_FILE" ]; then
        local entries=$(wc -l < "$BACKUP_FILE")
        echo "Backup entries: $entries"
    fi
    
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Auto-init on source
guardian_init

# Export functions
export -f record_interaction
export -f mark_emotional
export -f emergency_backup
export -f recover_from_backup
export -f guardian_detect_reset
export -f guardian_recover_context
export -f guardian_status
