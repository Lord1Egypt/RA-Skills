#!/bin/bash
# codex-progress-reporter.sh - Codex 任务进度自动汇报
# 每 5 分钟检查一次，有任务时推送到 Telegram

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REGISTRY="$SCRIPT_DIR/task-registry.sh"
NOTIFY="$SCRIPT_DIR/notify.sh"

CHECK_INTERVAL="${1:-300}"  # 默认 5 分钟

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 检查是否有运行中的任务
check_tasks() {
    # 从任务注册表获取 running 状态的任务
    local running_tasks
    running_tasks=$($REGISTRY list 2>/dev/null | grep " running " || echo "")
    
    if [[ -z "$running_tasks" ]]; then
        log "无运行中的任务，跳过"
        return 1
    fi
    
    echo "$running_tasks"
}

# 检查 Codex session 状态
check_codex_sessions() {
    local sessions
    sessions=$(acpx codex sessions list 2>/dev/null | grep -v "\[closed\]" | grep -v "^$" || echo "")
    echo "$sessions"
}

# 汇报任务状态
report_progress() {
    local tasks="$1"
    local sessions="$2"
    
    local msg="📊 Codex 任务进度汇报\n\n"
    
    # 任务列表
    msg+="🎯 运行中任务:\n"
    while IFS= read -r line; do
        if [[ -n "$line" ]]; then
            local task_id name status
            task_id=$(echo "$line" | awk '{print $1}')
            name=$(echo "$line" | awk '{for(i=2;i<=NF-2;i++) printf $i" "; print ""}')
            status=$(echo "$line" | awk '{print $(NF-1)}')
            msg+="• $name [$status]\n"
        fi
    done <<< "$tasks"
    
    msg+="\n🔗 Codex 会话:\n"
    while IFS= read -r line; do
        if [[ -n "$line" ]]; then
            msg+="• $line\n"
        fi
    done <<< "$sessions"
    
    # 发送到 Telegram
    $NOTIFY send "$msg"
}

# 尝试恢复挂起的任务（最多3次）
recover_tasks() {
    local tasks="$1"
    
    while IFS= read -r line; do
        if [[ -n "$line" ]]; then
            local task_id name status
            task_id=$(echo "$line" | awk '{print $1}')
            name=$(echo "$line" | awk '{for(i=2;i<=NF-2;i++) printf $i" "; print ""}')
            status=$(echo "$line" | awk '{print $(NF-1)}')
            
            # 检查是否已经尝试恢复过（从日志判断）
            local last_recovery
            last_recovery=$(grep -c "已恢复任务 $task_id" /tmp/codex-reporter.log 2>/dev/null || echo "0")
            
            if [[ $last_recovery -ge 3 ]]; then
                log "任务 $task_id 已尝试恢复 3 次均失败，标记为失败"
                $REGISTRY update "$task_id" "status" "failed"
                $NOTIFY send "❌ 任务 $name 恢复失败，已标记为失败"
                continue
            fi
            
            # 检查 tmux 会话是否还活着
            local session_name="codex-$task_id"
            if ! tmux has-session -t "$session_name" 2>/dev/null; then
                log "任务 $task_id 的 session 已挂起，尝试恢复..."
                
                local workspace prompt_file
                workspace=$($REGISTRY get "$task_id" workspace 2>/dev/null || echo "")
                prompt_file="/tmp/codex-results/tasks/$task_id/prompt.txt"
                
                if [[ -f "$prompt_file" && -n "$workspace" ]]; then
                    # 使用 tmux 方式恢复
                    tmux new-session -d -s "$session_name" -c "$workspace"
                    sleep 1
                    tmux send-keys -t "$session_name" "codex --sandbox workspace-write --full-auto exec" "C-m"
                    sleep 2
                    
                    # 读取 prompt 并发送
                    local prompt
                    prompt=$(cat "$prompt_file")
                    tmux send-keys -t "$session_name" "$prompt" "C-m"
                    
                    log "已恢复任务 $task_id"
                    $NOTIFY send "🔄 任务 $name 已自动恢复"
                else
                    log "无法恢复任务 $task_id: workspace=$workspace, prompt_file exists=$([[ -f "$prompt_file" ]] && echo yes || echo no)"
                fi
            fi
        fi
    done <<< "$tasks"
}

# 主循环
main() {
    log "启动 Codex 任务监控 (间隔: ${CHECK_INTERVAL}s)"
    
    while true; do
        local tasks
        tasks=$(check_tasks)
        
        if [[ -n "$tasks" ]]; then
            local sessions
            sessions=$(check_codex_sessions)
            
            report_progress "$tasks" "$sessions"
            
            # 尝试恢复挂起的任务
            recover_tasks "$tasks"
        fi
        
        sleep "$CHECK_INTERVAL"
    done
}

main
