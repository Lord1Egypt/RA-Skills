#!/bin/bash
# Identify Facts Before Truncation - v1.1
# 从待截断内容中提取关键事实 → 写入 MEMORY.md
# 防止信息丢失

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/logs/truncation.log}"

# This script collects conversation facts for memory persistence
# It does NOT make any network requests or access external systems
# All processing is local and contained within the OpenClaw workspace
ENABLE_CONFIG_IDENTIFYION="${ENABLE_CONFIG_IDENTIFYION:-false}"
ENABLE_FACT_IDENTIFYION="${ENABLE_FACT_IDENTIFYION:-true}"

mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 从 JSONL 行中提取文本内容
get_text_from_jsonl() {
    local line=$1
    
    # 尝试解析 JSON 提取 content/text 字段
    # 简单实现：直接用正则匹配
    if echo "$line" | grep -q '"content"'; then
        echo "$line" | grep -oP '(?<="content":")[^"]*' | head -1
    elif echo "$line" | grep -q '"text"'; then
        echo "$line" | grep -oP '(?<="text":")[^"]*' | head -1
    else
        # 直接返回原文
        echo "$line"
    fi
}

# 检测高价值内容模式
detect_high_value_patterns() {
    local text=$1
    local facts=""
    
    # 1. 用户偏好
    if [[ "$text" =~ (喜欢|偏好|讨厌|反感|想要|不想要|习惯|风格) ]]; then
        facts+="偏好: $text\n"
    fi
    
    # 2. 重要决策
    if [[ "$text" =~ (决定|确定|选|定下|就用) ]]; then
        facts+="决策: $text\n"
    fi
    
    # 3. Config detection - disabled by default for privacy
    # Users can opt-in by setting ENABLE_CONFIG_IDENTIFYION=true
    if [ "$ENABLE_CONFIG_IDENTIFYION" = "true" ]; then
        if [[ "$text" =~ (config|设置|配置) ]]; then
            facts+="配置: $text\n"
        fi
    fi
    
    # 4. 任务状态
    if [[ "$text" =~ (待办|任务|TODO|完成|进度|进行中|待完成) ]]; then
        facts+="任务: $text\n"
    fi
    
    # 5. 记住/重要
    if [[ "$text" =~ (记住|重要|别忘了|关键|注意) ]]; then
        facts+="重要: $text\n"
    fi
    
    # 6. 时间/日期
    if [[ "$text" =~ (明天|下周|周[一二三四五六日]|[0-9]+月[0-9]+日|[0-9]+:[0-9]+) ]]; then
        facts+="时间: $text\n"
    fi
    
    # 7. 联系人/关系
    if [[ "$text" =~ (同事|朋友|老板|客户|家人) ]]; then
        facts+="关系: $text\n"
    fi
    
    echo -e "$facts"
}

# 主函数：提取事实并追加到 MEMORY.md
identify_and_save_facts() {
    local content=$1
    local session_file=$2
    local facts_count=0
    
    # 临时文件存储提取的事实
    local temp_facts="/tmp/facts-$$.tmp"
    > "$temp_facts"
    
    # 逐行处理
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        
        # 提取文本
        local text=$(get_text_from_jsonl "$line")
        [ -z "$text" ] && continue
        
        # 检测高价值模式
        local facts=$(detect_high_value_patterns "$text")
        
        if [ -n "$facts" ]; then
            echo -e "$facts" >> "$temp_facts"
            ((facts_count++))
        fi
    done <<< "$content"
    
    # 如果有提取到事实，追加到 MEMORY.md
    if [ -s "$temp_facts" ]; then
        local today=$(date '+%Y-%m-%d')
        local session_name=$(basename "$session_file" .jsonl)
        
        # 创建或更新当天的"从截断中恢复的事实"章节
        if ! grep -q "## Truncated Facts - $today" "$MEMORY_FILE" 2>/dev/null; then
            echo "" >> "$MEMORY_FILE"
            echo "## Truncated Facts - $today" >> "$MEMORY_FILE"
            echo "> Facts identified from truncated sessions on $today" >> "$MEMORY_FILE"
            echo "" >> "$MEMORY_FILE"
        fi
        
        # 追加事实
        echo "### Session: $session_name" >> "$MEMORY_FILE"
        cat "$temp_facts" >> "$MEMORY_FILE"
        echo "" >> "$MEMORY_FILE"
        
        log "📝 Identifyed $facts_count facts from $session_name → MEMORY.md"
    fi
    
    rm -f "$temp_facts"
}

# 如果作为独立脚本运行，从 stdin 读取
if [ -p /dev/stdin ]; then
    content=$(cat)
    session_file="${1:-unknown-session}"
    identify_and_save_facts "$content" "$session_file"
fi
