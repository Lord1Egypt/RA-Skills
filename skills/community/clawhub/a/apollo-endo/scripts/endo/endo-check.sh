#!/bin/bash
# endo-check.sh - 内分泌全局参数检测
# 监控和调节全局参数，维持系统平衡

STATE_FILE="/root/.openclaw/workspace/.endo/state.json"
mkdir -p "$(dirname "$STATE_FILE")"

# 全局参数配置
CONFIG_FILE="$HOME/.openclaw/openclaw.json"

# 获取当前token使用率（估算）
get_token_usage() {
    local memory_file="/root/.openclaw/workspace/memory/$(date +%Y-%m-%d).md"
    if [ -f "$memory_file" ]; then
        local chars=$(wc -c < "$memory_file")
        local estimated=$((chars * 2))  # 粗略估算
        echo $estimated
    else
        echo 0
    fi
}

# 获取活跃任务数
get_active_tasks() {
    local task_file="/root/.openclaw/workspace/.dream/task-state.json"
    if [ -f "$task_file" ]; then
        local count=$(grep -c '"status":"active"' "$task_file" 2>/dev/null)
        [ -z "$count" ] && count=0
        echo $count
    else
        echo 0
    fi
}

# 获取对话轮数
get_turn_count() {
    local memory_file="/root/.openclaw/workspace/memory/$(date +%Y-%m-%d).md"
    if [ -f "$memory_file" ]; then
        grep -c "^## " "$memory_file" 2>/dev/null || echo 0
    else
        echo 0
    fi
}

# 计算系统负载
calc_load() {
    local tokens=$1
    local tasks=$2
    local turns=$3
    
    local load=0
    [ $tokens -gt 50000 ] && ((load++))
    [ $tasks -gt 5 ] && ((load++))
    [ $turns -gt 20 ] && ((load++))
    
    echo $load
}

# 获取参数调节建议
get_adjustment() {
    local load=$1
    local tokens=$2
    
    if [ $load -ge 3 ]; then
        echo "降低处理速度|减少并行任务|触发整理"
    elif [ $load -eq 2 ]; then
        echo "保持当前节奏|监控token使用"
    elif [ $tokens -gt 80000 ]; then
        echo "建议整理上下文|防止token溢出"
    else
        echo "参数正常|维持当前状态"
    fi
}

# 获取负载emoji
get_load_emoji() {
    local load=$1
    if [ $load -eq 0 ]; then
        echo "🟢"
    elif [ $load -le 2 ]; then
        echo "🟡"
    else
        echo "🔴"
    fi
}

# 主函数
main() {
    local tokens=$(get_token_usage)
    local tasks=$(get_active_tasks)
    local turns=$(get_turn_count)
    local load=$(calc_load $tokens $tasks $turns)
    local adjustment=$(get_adjustment $load $tokens)
    local emoji=$(get_load_emoji $load)
    
    echo "⚙️ [apollo-endo] 内分泌参数报告"
    echo ""
    echo "全局状态："
    echo "  - Token估算：$tokens"
    echo "  - 活跃任务：$tasks个"
    echo "  - 对话轮数：$turns轮"
    echo ""
    echo "系统负载：$emoji $load/3"
    echo ""
    echo "参数调节：$adjustment"
    
    # 保存状态
    cat > "$STATE_FILE" << EOF
{
    "tokens": $tokens,
    "active_tasks": $tasks,
    "turn_count": $turns,
    "load": $load,
    "adjustment": "$adjustment",
    "checked_at": "$(date -Iseconds)"
}
EOF
}

main
