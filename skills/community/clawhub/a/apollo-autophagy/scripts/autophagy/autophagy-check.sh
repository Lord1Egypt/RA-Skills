#!/bin/bash
# autophagy-check.sh - 自噬清理检测
# 检查需要清理的内容，提出清理建议

WORKSPACE="/root/.openclaw/workspace"
AUTOPHAGY_STATE="/root/.openclaw/workspace/.autophagy/state.json"
mkdir -p "$(dirname "$AUTOPHAGY_STATE")"

# 检查临时文件
check_temp_files() {
    local temp_dirs="/tmp/openclaw /tmp/.dream /tmp/.heartbeat"
    local total_size=0
    local file_count=0
    
    for dir in $temp_dirs; do
        if [ -d "$dir" ]; then
            local size=$(du -sb "$dir" 2>/dev/null | cut -f1)
            local count=$(find "$dir" -type f 2>/dev/null | wc -l)
            total_size=$((total_size + size))
            file_count=$((file_count + count))
        fi
    done
    
    echo "$file_count|$total_size"
}

# 检查旧日志
check_old_logs() {
    local log_dir="$WORKSPACE/logs"
    local old_count=0
    
    if [ -d "$log_dir" ]; then
        # 找出7天前的日志
        find "$log_dir" -name "*.log" -mtime +7 2>/dev/null | wc -l
    else
        echo 0
    fi
}

# 检查memory文件大小
check_memory_size() {
    local total=0
    if [ -d "$WORKSPACE/memory" ]; then
        total=$(du -sb "$WORKSPACE/memory" 2>/dev/null | cut -f1)
    fi
    echo $total
}

# 检查workflow状态文件
check_workflow_files() {
    local wf_dir="$WORKSPACE/.workflow"
    local stale=0
    
    if [ -d "$wf_dir" ]; then
        # 找出3天前的gate文件
        find "$wf_dir/gate" -name "*.json" -mtime +3 2>/dev/null | wc -l
    else
        echo 0
    fi
}

# 检查trash
check_trash() {
    local trash_dir="$WORKSPACE/.trash"
    if [ -d "$trash_dir" ]; then
        find "$trash_dir" -type f 2>/dev/null | wc -l
    else
        echo 0
    fi
}

# 判断是否需要自噬
should_autophagy() {
    local temp_count=$1
    local memory_size=$2
    local old_logs=$3
    local trash=$4
    
    local score=0
    [ $temp_count -gt 10 ] && ((score++))
    [ $memory_size -gt 10485760 ] && ((score++))  # >10MB
    [ $old_logs -gt 0 ] && ((score++))
    [ $trash -gt 5 ] && ((score++))
    
    echo $score
}

# 获取清理建议
get_cleanup_suggestion() {
    local temp_count=$1
    local memory_size=$2
    local old_logs=$3
    local trash=$4
    
    local suggestions=()
    
    [ $temp_count -gt 10 ] && suggestions+=("清理临时文件($temp_count个)")
    [ $memory_size -gt 10485760 ] && suggestions+=("压缩memory文件")
    [ $old_logs -gt 0 ] && suggestions+=("删除旧日志($old_logs个)")
    [ $trash -gt 5 ] && suggestions+=("清空回收站($trash个)")
    
    if [ ${#suggestions[@]} -eq 0 ]; then
        echo "无需清理"
    else
        IFS='|' && echo "${suggestions[*]}"
    fi
}

# 格式化大小
format_size() {
    local bytes=$1
    if [ $bytes -lt 1024 ]; then
        echo "${bytes}B"
    elif [ $bytes -lt 1048576 ]; then
        echo "$((bytes/1024))KB"
    elif [ $bytes -lt 1073741824 ]; then
        echo "$((bytes/1048576))MB"
    else
        echo "$((bytes/1073741824))GB"
    fi
}

# 主函数
main() {
    local temp_info=$(check_temp_files)
    local temp_count=$(echo "$temp_info" | cut -d'|' -f1)
    local temp_size=$(echo "$temp_info" | cut -d'|' -f2)
    local memory_size=$(check_memory_size)
    local old_logs=$(check_old_logs)
    local trash=$(check_trash)
    local score=$(should_autophagy $temp_count $memory_size $old_logs $trash)
    local suggestions=$(get_cleanup_suggestion $temp_count $memory_size $old_logs $trash)
    
    echo "🔄 [apollo-autophagy] 自噬清理报告"
    echo ""
    echo "当前状态："
    echo "  - 临时文件：${temp_count}个 ($(format_size $temp_size))"
    echo "  - Memory目录：$(format_size $memory_size)"
    echo "  - 旧日志(>7天)：${old_logs}个"
    echo "  - 回收站：${trash}个"
    echo ""
    
    if [ $score -eq 0 ]; then
        echo "🟢 系统状态正常"
        echo "无需自噬清理"
    elif [ $score -le 2 ]; then
        echo "🟡 建议轻量清理"
        echo "清理建议：$suggestions"
    else
        echo "🔴 需要深度清理"
        echo "清理建议：$suggestions"
    fi
    
    # 保存状态
    cat > "$AUTOPHAGY_STATE" << EOF
{
    "temp_count": $temp_count,
    "temp_size": $temp_size,
    "memory_size": $memory_size,
    "old_logs": $old_logs,
    "trash": $trash,
    "score": $score,
    "needs_cleanup": $([ $score -ge 2 ] && echo "true" || echo "false"),
    "suggestions": "$suggestions",
    "checked_at": "$(date -Iseconds)"
}
EOF
}

main
