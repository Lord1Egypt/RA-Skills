#!/bin/bash
# renal-check.sh - 上下文过滤检测
# 检测上下文状态，判断是否需要过滤

WORKSPACE="/root/.openclaw/workspace"
TOKEN_ESTIMATOR="$WORKSPACE/skills/apollo-dream/scripts/token-estimator.py"
STATE_FILE="$WORKSPACE/.renal/filter-state.json"
DREAM_TASK="$WORKSPACE/.dream/task-state.json"
DREAM_TOPIC="$WORKSPACE/.dream/topic-state.json"
mkdir -p "$(dirname "$STATE_FILE")"

# 估算当前会话token（基于今日memory文件）
estimate_session_tokens() {
    local today=$(date +%Y-%m-%d)
    local memory_file="$WORKSPACE/memory/$today.md"
    
    if [ -f "$memory_file" ]; then
        local chars=$(wc -c < "$memory_file")
        # 粗略估算：中文约2字符=1token
        echo $((chars / 2))
    else
        echo 0
    fi
}

# 统计重复确认
count_confirmations() {
    local today=$(date +%Y-%m-%d)
    local memory_file="$WORKSPACE/memory/$today.md"
    
    if [ -f "$memory_file" ]; then
        local count=$(grep -cE "好的|收到|OK|好的好的|明白了" "$memory_file" 2>/dev/null)
        [ -z "$count" ] && count=0
        echo $count
    else
        echo 0
    fi
}

# 获取进行中任务数
get_active_tasks() {
    if [ -f "$DREAM_TASK" ]; then
        grep -o '"status":"active"' "$DREAM_TASK" 2>/dev/null | wc -l || echo 0
    else
        echo 0
    fi
}

# 获取活跃话题数
get_active_topics() {
    if [ -f "$DREAM_TOPIC" ]; then
        grep -o '"status":"active"' "$DREAM_TOPIC" 2>/dev/null | wc -l || echo 0
    else
        echo 0
    fi
}

# 估算信息密度（简化版：基于字符重复率）
estimate_density() {
    local today=$(date +%Y-%m-%d)
    local memory_file="$WORKSPACE/memory/$today.md"
    
    if [ -f "$memory_file" ] && [ -s "$memory_file" ]; then
        local chars=$(wc -c < "$memory_file")
        local unique=$(sort -u "$memory_file" 2>/dev/null | wc -c)
        if [ $chars -gt 0 ]; then
            local density=$((unique * 100 / chars))
            echo $density
        else
            echo 0
        fi
    else
        echo 100  # 新会话密度100%
    fi
}

# 判断是否需要过滤
should_filter() {
    local tokens=$1
    local density=$2
    local confirmations=$3
    
    local warnings=0
    [ $tokens -gt 50000 ] && ((warnings++))
    [ $density -lt 50 ] && ((warnings++))
    [ $confirmations -gt 5 ] && ((warnings++))
    
    echo $warnings
}

# 获取状态emoji
get_status_emoji() {
    local warnings=$1
    if [ $warnings -eq 0 ]; then
        echo "🟢"
    elif [ $warnings -eq 1 ]; then
        echo "🟡"
    else
        echo "🔴"
    fi
}

# 主函数
main() {
    local tokens=$(estimate_session_tokens)
    local density=$(estimate_density)
    local confirmations=$(count_confirmations)
    local active_tasks=$(get_active_tasks)
    local active_topics=$(get_active_topics)
    local warnings=$(should_filter $tokens $density $confirmations)
    local status_emoji=$(get_status_emoji $warnings)
    if [ $warnings -ge 2 ]; then
        local needs_filter="true"
    else
        local needs_filter="false"
    fi
    
    # 估算节省空间
    local wasted=0
    if [ $confirmations -gt 0 ]; then
        wasted=$((confirmations * 10))  # 每个确认约浪费10token
    fi
    if [ $density -lt 70 ]; then
        wasted=$((wasted + (70 - density)))
    fi
    
    # 输出报告
    echo "🫘 [apollo-renal] 上下文净化报告"
    echo ""
    echo "当前状态："
    echo "  - Token估算：$tokens"
    echo "  - 有效信息密度：${density}%"
    echo "  - 重复确认：${confirmations}次"
    echo "  - 进行中任务：${active_tasks}个"
    echo "  - 活跃话题：${active_topics}个"
    echo ""
    
    if [ $warnings -eq 0 ]; then
        echo "$status_emoji 上下文状态正常"
        echo ""
        echo "推荐任务：继续当前工作"
    elif [ $warnings -eq 1 ]; then
        echo "$status_emoji 上下文略长，可以考虑整理"
        echo ""
        echo "推荐任务：apollo-renal快速过滤 或 继续当前工作"
    else
        echo "$status_emoji 上下文需深度整理"
        echo ""
        echo "推荐任务：apollo-renal过滤 → apollo-dream巩固"
    fi
    
    # 保存状态
    cat > "$STATE_FILE" << EOF
{
    "tokens": $tokens,
    "density": $density,
    "confirmations": $confirmations,
    "active_tasks": $active_tasks,
    "active_topics": $active_topics,
    "warnings": $warnings,
    "needs_filter": $needs_filter,
    "status": "$status_emoji",
    "checked_at": "$(date -Iseconds)"
}
EOF
}

main
