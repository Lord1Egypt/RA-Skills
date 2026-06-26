#!/bin/bash
# Identify Facts Before Truncation - v2.1
# 使用 OpenClaw Agent 子代理提取结构化事实
# 解决问题：简单关键词匹配太粗糙，无法理解上下文
# v2.1: Added recursion guard to prevent infinite agent→truncation→agent loops

set -e

# Recursion guard: prevent nested agent calls from triggering truncation again
if [ "${CONTEXT_COMPRESSION_RUNNING:-false}" = "true" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⏭️ Skipping fact identification (already running)" >&2
    exit 0
fi
export CONTEXT_COMPRESSION_RUNNING=true

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/logs/truncation.log}"
TEMP_DIR="/tmp/openclaw-fact-identification"
FACTS_TIMEOUT="${FACTS_TIMEOUT:-60}"  # 子代理超时时间（秒）

mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$TEMP_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# 从 JSONL 行中提取文本内容（简化版）
get_text_from_jsonl() {
    local line=$1
    # 提取所有 content 字段，用 jq 如果可用
    if command -v jq &> /dev/null; then
        echo "$line" | jq -r '.content // .text // empty' 2>/dev/null || true
    else
        # 简单正则
        echo "$line" | grep -oP '(?<="content":")[^"]*' | head -1
    fi
}

# 检测是否有高价值内容（快速扫描）
has_high_value_content() {
    local content=$1
    
    # 高价值关键词列表
    local keywords=(
        "重要" "决定" "记住" "别忘了" "TODO" "待办"
        "偏好" "我喜欢" "我讨厌" "千万" "务必" "关键"
        "明天" "下周" "约会" "会议" "截止"
        "同事" "老板" "客户" "朋友"
    )
    
    for kw in "${keywords[@]}"; do
        if echo "$content" | grep -q "$kw"; then
            return 0
        fi
    done
    return 1
}

# 准备内容供 AI 分析
prepare_content_for_ai() {
    local content=$1
    local max_chars=8000  # 限制长度，避免太长
    
    # 提取文本并合并
    local text=""
    while IFS= read -r line; do
        [ -z "$line" ] && continue
        local identified=$(get_text_from_jsonl "$line")
        [ -n "$identified" ] && text+="$identified\n"
    done <<< "$content"
    
    # 截断
    echo -e "$text" | head -c $max_chars
}

# 调用 OpenClaw Agent 提取事实
call_agent_for_identification() {
    local content_file=$1
    local output_file=$2
    
    # 构建 agent 消息
    local prompt="你是一个事实提取专家。请分析以下对话内容，提取出所有重要事实。

要求：
1. 只提取真正重要、需要记住的信息
2. 格式为简洁的列表，每行一个事实
3. 分类：[偏好] [决策] [任务] [时间] [关系] [重要]
4. 忽略寒暄、客套话
5. 如果没有重要信息，输出：无重要事实

对话内容：
\`\`\`
$(cat "$content_file")
\`\`\`

请输出事实列表（不要其他解释）："

    # v8: Enhanced error handling with retry
    local MAX_RETRIES=2
    local retry_count=0
    local result
    
    log "🤖 Calling agent for fact identification..."
    
    while [ $retry_count -lt $MAX_RETRIES ]; do
        result=$(openclaw agent --agent main --message "$prompt" --timeout $FACTS_TIMEOUT 2>&1) && break
        ((retry_count++))
        log "⚠️ Agent call failed, retry $retry_count/$MAX_RETRIES"
        sleep 3
    done
    
    if [ $retry_count -eq $MAX_RETRIES ]; then
        log "❌ Agent call failed after $MAX_RETRIES retries"
        # v8: Save content to pending queue for later retry
        local pending_file="$TEMP_DIR/pending-facts-$(date +%s).txt"
        cp "$content_file" "$pending_file"
        log "📝 Content saved to pending queue: $pending_file"
        return 1
    fi
    
    # 提取结果
    echo "$result" > "$output_file"
    log "✅ Agent identification completed"
    return 0
}

# 将事实写入 MEMORY.md
write_facts_to_memory() {
    local facts=$1
    local session_name=$2
    
    # 跳过空内容或"无重要事实"
    if [ -z "$facts" ] || echo "$facts" | grep -q "^无重要事实"; then
        log "ℹ️ No significant facts to save"
        return 0
    fi
    
    local today=$(date '+%Y-%m-%d')
    
    # 确保章节存在
    if ! grep -q "## Truncated Facts - $today" "$MEMORY_FILE" 2>/dev/null; then
        echo "" >> "$MEMORY_FILE"
        echo "## Truncated Facts - $today" >> "$MEMORY_FILE"
        echo "> Facts identified from truncated sessions on $today" >> "$MEMORY_FILE"
        echo "" >> "$MEMORY_FILE"
    fi
    
    # 追加事实
    echo "### Session: $session_name" >> "$MEMORY_FILE"
    echo "\`\`\`" >> "$MEMORY_FILE"
    echo "$facts" >> "$MEMORY_FILE"
    echo "\`\`\`" >> "$MEMORY_FILE"
    echo "" >> "$MEMORY_FILE"
    
    log "📝 Facts saved to MEMORY.md"
}

# 主函数
identify_and_save_facts() {
    local content=$1
    local session_file=$2
    local session_name=$(basename "$session_file" .jsonl)
    
    log "=== Fact Identifyion v2 for $session_name ==="
    
    # 快速检查：是否有高价值内容
    if ! has_high_value_content "$content"; then
        log "ℹ️ No high-value content detected, skipping identification"
        return 0
    fi
    
    log "🔍 High-value content detected, preparing for AI analysis..."
    
    # 准备内容
    local content_file="$TEMP_DIR/content-$$-$RANDOM.txt"
    local output_file="$TEMP_DIR/facts-$$-$RANDOM.txt"
    
    prepare_content_for_ai "$content" > "$content_file"
    
    # 检查是否有足够内容
    local content_len=$(wc -c < "$content_file")
    if [ "$content_len" -lt 50 ]; then
        log "ℹ️ Content too short for meaningful identification"
        rm -f "$content_file" "$output_file"
        return 0
    fi
    
    # 调用 agent 提取
    if call_agent_for_identification "$content_file" "$output_file"; then
        local facts=$(cat "$output_file")
        write_facts_to_memory "$facts" "$session_name"
    fi
    
    # 清理
    rm -f "$content_file" "$output_file"
}

# 如果作为独立脚本运行
if [ -p /dev/stdin ]; then
    content=$(cat)
    session_file="${1:-unknown-session}"
    identify_and_save_facts "$content" "$session_file"
fi
