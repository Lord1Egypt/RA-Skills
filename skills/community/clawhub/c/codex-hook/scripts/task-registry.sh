#!/bin/bash
# task-registry.sh - 任务注册表管理
# 管理 active-tasks.json，实现任务的创建、查询、更新、删除

set -euo pipefail

REGISTRY_DIR="${CODEX_TASK_DIR:-/tmp/codex-tasks}"
REGISTRY_FILE="${REGISTRY_DIR}/active-tasks.json"

# 初始化注册表
init_registry() {
    mkdir -p "$REGISTRY_DIR"
    if [[ ! -f "$REGISTRY_FILE" ]]; then
        echo '{"tasks": [], "version": "1.0"}' > "$REGISTRY_FILE"
    fi
}

# 读取注册表
read_registry() {
    init_registry
    cat "$REGISTRY_FILE"
}

# 写入注册表
write_registry() {
    local content="$1"
    echo "$content" > "$REGISTRY_FILE"
}

# 获取任务列表
list_tasks() {
    init_registry
    local status="${1:-}"
    local format="${2:-table}"  # table, json
    
    if [[ "$format" == "json" ]]; then
        read_registry
        return
    fi
    
    # 表格输出
    echo ""
    echo "📋 任务列表"
    echo "================================================================"
    printf "%-12s %-20s %-10s %-12s %s\n" "ID" "名称" "状态" "进度" "时间"
    echo "----------------------------------------------------------------"
    
    # 使用 jq 转换为 JSON 数组
    local tasks_json
    tasks_json=$(read_registry | jq '.tasks' 2>/dev/null || echo "[]")
    
    local task_count
    task_count=$(echo "$tasks_json" | jq 'length')
    
    if [[ "$task_count" -eq 0 ]]; then
        echo "暂无任务"
        return
    fi
    
    local i=0
    while [[ $i -lt $task_count ]]; do
        local task
        task=$(echo "$tasks_json" | jq -c ".[$i]")
        
        local id name status progress started_at
        id=$(echo "$task" | jq -r '.id')
        name=$(echo "$task" | jq -r '.name // "unnamed"' | cut -c1-18)
        status=$(echo "$task" | jq -r '.status')
        progress=$(echo "$task" | jq -r '.progress // 0')
        started_at=$(echo "$task" | jq -r '.started_at // 0')
        
        # 状态emoji
        local status_emoji
        case "$status" in
            pending) status_emoji="⏳" ;;
            running) status_emoji="🔄" ;;
            done) status_emoji="✅" ;;
            failed) status_emoji="❌" ;;
            *) status_emoji="❓" ;;
        esac
        
        # 进度条
        local progress_bar
        progress_bar=$(printf "%s %d%%" "$status_emoji" "$progress")
        
        printf "%-12s %-20s %-10s %-12s %s\n" "$id" "$name" "$status" "$progress_bar" "$(date -j -f %s "$started_at" '+%H:%M' 2>/dev/null || echo '-')"
        ((i++))
    done
    
    echo "================================================================"
}

# 获取任务详情
get_task() {
    local task_id="$1"
    if [[ -z "$task_id" ]]; then
        echo "null"
        return
    fi
    init_registry
    read_registry | jq ".tasks[] | select(.id == \"$task_id\")" 2>/dev/null || echo "null"
}

# 创建任务
create_task() {
    local name="$1"
    local description="${2:-}"
    local parent_id="${3:-}"
    local workspace="${4:-$HOME/projects}"
    
    init_registry
    
    local task_id
    task_id="task-$(date +%Y%m%d)-$(head -c 4 /dev/urandom | xxd -p)"
    
    local now
    now=$(date +%s)
    
    local new_task
    new_task=$(cat <<EOF
{
    "id": "$task_id",
    "name": "$name",
    "description": "$description",
    "parent_id": "$parent_id",
    "status": "pending",
    "progress": 0,
    "workspace": "$workspace",
    "branch": "",
    "tmux_session": "",
    "started_at": $now,
    "completed_at": null,
    "pr": null,
    "checks": {},
    "logs": [],
    "children": []
}
EOF
)
    
    # 添加到注册表
    local registry
    registry=$(read_registry)
    local updated
    updated=$(echo "$registry" | jq ".tasks += [$new_task]")
    write_registry "$updated"
    
    echo "$task_id"
}

# 更新任务状态
update_task() {
    local task_id="$1"
    local field="$2"
    local value="${3:-}"
    
    if [[ -z "$task_id" || -z "$field" ]]; then
        echo "Error: Missing required arguments" >&2
        return 1
    fi
    
    init_registry
    
    local registry updated
    registry=$(read_registry)
    
    # 检查任务是否存在
    local exists
    exists=$(echo "$registry" | jq ".tasks[] | select(.id == \"$task_id\") | length" 2>/dev/null || echo "")
    if [[ -z "$exists" ]]; then
        echo "Error: Task $task_id not found" >&2
        return 1
    fi
    
    # 判断 value 是数字还是字符串
    local updater
    if [[ "$value" =~ ^[0-9]+$ ]]; then
        # 数字类型
        updater=$(echo "$registry" | jq --arg id "$task_id" --arg field "$field" --argjson value "$value" \
            '.tasks |= map(if .id == $id then .[$field] = $value else . end)')
    else
        # 字符串类型
        updater=$(echo "$registry" | jq --arg id "$task_id" --arg field "$field" --arg value "$value" \
            '.tasks |= map(if .id == $id then .[$field] = $value else . end)')
    fi
    
    write_registry "$updater"
    echo "Updated $task_id $field = $value"
}

# 更新任务进度
update_progress() {
    local task_id="$1"
    local progress="$2"
    local status="${3:-}"
    
    update_task "$task_id" "progress" "$progress"
    
    if [[ -n "$status" ]]; then
        update_task "$task_id" "status" "$status"
    fi
}

# 标记任务完成
complete_task() {
    local task_id="$1"
    local pr="${2:-}"
    
    local now
    now=$(date +%s)
    
    init_registry
    
    local registry updated
    registry=$(read_registry)
    
    updated=$(echo "$registry" | jq \
        --arg id "$task_id" \
        --argjson completed_at "$now" \
        --arg pr "$pr" \
        '.tasks |= map(if .id == $id then .status = "done" | .progress = 100 | .completed_at = $completed_at | .pr = $pr else . end)')
    
    write_registry "$updated"
    echo "Task $task_id completed"
}

# 删除任务
delete_task() {
    local task_id="$1"
    
    init_registry
    
    local registry updated
    registry=$(read_registry)
    updated=$(echo "$registry" | jq --arg id "$task_id" '.tasks |= map(select(.id != $id))')
    write_registry "$updated"
    echo "Task $task_id deleted"
}

# 添加子任务
add_child() {
    local parent_id="$1"
    local child_id="$2"
    
    init_registry
    
    local registry updated
    registry=$(read_registry)
    
    # 给父任务添加子任务ID
    updated=$(echo "$registry" | jq \
        --arg parent "$parent_id" \
        --arg child "$child_id" \
        '.tasks |= map(if .id == $parent then .children += [$child] else . end)')
    
    write_registry "$updated"
}

# 添加日志
add_log() {
    local task_id="$1"
    local message="$2"
    local level="${3:-info}"
    
    local now
    now=$(date +%s)
    
    init_registry
    
    local registry updated
    registry=$(read_registry)
    
    local log_entry
    log_entry=$(cat <<EOF
{"timestamp": $now, "level": "$level", "message": "$message"}
EOF
)
    
    updated=$(echo "$registry" | jq \
        --arg id "$task_id" \
        --argjson log "$log_entry" \
        '.tasks |= map(if .id == $id then .logs += [$log] else . end)')
    
    write_registry "$updated"
}

# 清理已完成任务（保留最近N个）
cleanup() {
    local keep="${1:-10}"
    
    init_registry
    
    local registry updated
    registry=$(read_registry)
    
    # 按完成时间排序，保留最近的
    updated=$(echo "$registry" | jq \
        --argjson keep "$keep" \
        '.tasks |= (map(select(.status == "done")) | .[-$keep:] + map(select(.status != "done")))')
    
    write_registry "$updated"
    echo "Cleaned up completed tasks (kept latest $keep)"
}

# 导出任务（用于调试）
export_task() {
    local task_id="$1"
    local output_dir="${2:-/tmp/codex-tasks/exports}"
    
    mkdir -p "$output_dir"
    
    local task
    task=$(get_task "$task_id")
    
    if [[ -z "$task" || "$task" == "null" ]]; then
        echo "Task $task_id not found" >&2
        return 1
    fi
    
    local output_file="${output_dir}/${task_id}.json"
    echo "$task" > "$output_file"
    echo "Exported to $output_file"
}

# 主命令处理
main() {
    local command="${1:-}"
    shift || true
    
    case "$command" in
        init)
            init_registry
            echo "Registry initialized at $REGISTRY_FILE"
            ;;
        list)
            list_tasks "$@"
            ;;
        get)
            get_task "$1"
            ;;
        create)
            create_task "$1" "${2:-}" "${3:-}" "${4:-}"
            ;;
        update)
            update_task "$1" "$2" "$3"
            ;;
        progress)
            update_progress "$1" "$2" "$3"
            ;;
        complete)
            complete_task "$1" "${2:-}"
            ;;
        delete)
            delete_task "$1"
            ;;
        add-child)
            add_child "$1" "$2"
            ;;
        log)
            add_log "$1" "$2" "$3"
            ;;
        cleanup)
            cleanup "$1"
            ;;
        export)
            export_task "$1" "$2"
            ;;
        json)
            read_registry
            ;;
        "")
            list_tasks
            ;;
        *)
            echo "Usage: $0 <command> [args...]"
            echo ""
            echo "Commands:"
            echo "  init                   初始化注册表"
            echo "  list [status]          列出任务"
            echo "  get <task_id>          获取任务详情"
            echo "  create <name> [desc]   创建任务"
            echo "  update <id> <field> <val>  更新任务字段"
            echo "  progress <id> <prog>   更新进度"
            echo "  complete <id> [pr]      标记完成"
            echo "  delete <id>            删除任务"
            echo "  add-child <parent> <child>  添加子任务"
            echo "  log <id> <msg>        添加日志"
            echo "  cleanup [N]            清理已完成任务"
            echo "  export <id> [dir]     导出任务"
            echo "  json                  输出JSON格式"
            ;;
    esac
}

main "$@"
