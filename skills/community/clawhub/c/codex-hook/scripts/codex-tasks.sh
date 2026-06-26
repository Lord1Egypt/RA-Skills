#!/bin/bash
# codex-tasks.sh - Codex 任务执行入口
# 由 OpenClaw 调用，负责执行、监控、干预、PR、自动合并

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 子脚本
REGISTRY="$SCRIPT_DIR/task-registry.sh"
DISPATCHER="$SCRIPT_DIR/task-dispatcher.sh"
AUTO_MERGE="$SCRIPT_DIR/auto-merge.sh"
MONITOR="$SCRIPT_DIR/task-monitor.sh"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_msg() { echo -e "${1}${2}${NC}"; }

# ========== 核心功能 ==========

# 初始化
init() {
    print_msg "$BLUE" "🚀 初始化..."
    $REGISTRY init
    print_msg "$GREEN" "✅ 完成"
}

# 接收任务并执行
execute() {
    local parent_task="$1"      # 父任务ID
    local subtasks_json="$2"    # 子任务JSON数组
    local workspace="${3:-$HOME/projects}"
    
    print_msg "$BLUE" "📥 接收任务: $parent_task"
    echo ""
    
    # 解析子任务
    local task_count
    task_count=$(echo "$subtasks_json" | jq 'length')
    
    print_msg "$YELLOW" "📦 共 $task_count 个子任务"
    echo ""
    
    # 创建子任务到注册表
    local task_ids=()
    local i=0
    while [[ $i -lt $task_count ]]; do
        local name desc
        name=$(echo "$subtasks_json" | jq -r ".[$i].name")
        desc=$(echo "$subtasks_json" | jq -r ".[$i].description // \"$name\"")
        
        local task_id
        task_id=$($REGISTRY create "[$((i+1))/$task_count] $name" "$desc" "$parent_task")
        $REGISTRY add-child "$parent_task" "$task_id"
        
        task_ids+=("$task_id")
        print_msg "$GREEN" "  ✅ [$((i+1))/$task_count] $name → $task_id"
        
        ((i++))
    done
    
    echo ""
    print_msg "$YELLOW" "📤 开始派发任务..."
    
    # 并行派发所有任务
    for task_id in "${task_ids[@]}"; do
        local task_info
        task_info=$($REGISTRY get "$task_id")
        local prompt
        prompt=$($REGISTRY get "$task_id" | jq -r '.description')
        
        $DISPATCHER dispatch "$task_id" "$prompt" "$workspace" &
    done
    
    print_msg "$GREEN" "✅ 已派发 ${#task_ids[@]} 个任务"
    echo ""
    echo "📌 任务ID: $parent_task"
    echo "📌 查看进度: codex-tasks status $parent_task"
    echo "📌 干预任务: codex-tasks intervene <task_id> '<message>'"
}

# 添加子任务（OpenClaw 逐个添加）
add_subtask() {
    local parent_id="$1"
    local name="$2"
    local description="${3:-}"
    
    local task_id
    task_id=$($REGISTRY create "$name" "$description" "$parent_id")
    $REGISTRY add-child "$parent_id" "$task_id"
    
    echo "$task_id"
}

# 开始执行（所有子任务已添加完毕）
start_execution() {
    local parent_id="$1"
    local workspace="${2:-$HOME/projects}"
    
    print_msg "$YELLOW" "🔄 开始执行..."
    
    # 获取所有子任务
    local children
    children=$($REGISTRY get "$parent_id" | jq -r '.children[]' 2>/dev/null || echo "")
    
    if [[ -z "$children" ]]; then
        print_msg "$RED" "❌ 无子任务"
        return 1
    fi
    
    local task_ids=()
    while IFS= read -r child_id; do
        [[ -z "$child_id" ]] && continue
        task_ids+=("$child_id")
    done <<< "$children"
    
    # 并行派发
    for task_id in "${task_ids[@]}"; do
        local prompt
        prompt=$($REGISTRY get "$task_id" | jq -r '.description')
        $DISPATCHER dispatch "$task_id" "$prompt" "$workspace" &
    done
    
    print_msg "$GREEN" "✅ 已派发 ${#task_ids[@]} 个任务"
    echo "$parent_id"
}

# ========== 监控功能 ==========

# 查看状态
status() {
    local task_id="${1:-}"
    
    if [[ -z "$task_id" ]]; then
        $REGISTRY list
    else
        $DISPATCHER status "$task_id"
    fi
}

# 监控面板
monitor() {
    $DISPATCHER monitor
}

# 干预任务
intervene() {
    local task_id="$1"
    local message="$2"
    
    if [[ -z "$task_id" || -z "$message" ]]; then
        print_msg "$RED" "用法: codex-tasks intervene <task_id> '<message>'"
        return 1
    fi
    
    $DISPATCHER intervene "$task_id" "$message"
}

# 停止任务
stop() {
    local task_id="$1"
    $DISPATCHER stop "$task_id"
}

# 查看日志
logs() {
    local task_id="$1"
    
    if [[ -z "$task_id" ]]; then
        print_msg "$RED" "用法: codex-tasks logs <task_id>"
        return 1
    fi
    
    $REGISTRY get "$task_id" | jq -r '.logs[] | "\(.timestamp | strftime("%H:%M:%S")) [\(.level)] \(.message)"'
}

# ========== 完成后处理 ==========

# 自动合并
auto_merge() {
    local task_id="$1"
    local repo="${2:-.}"
    
    if [[ -z "$task_id" ]]; then
        print_msg "$RED" "用法: codex-tasks auto-merge <task_id> [repo]"
        return 1
    fi
    
    $AUTO_MERGE run-flow "$task_id" "$repo"
}

# 汇报完成
report() {
    local task_id="$1"
    local channel="${2:-telegram}"
    
    if [[ -z "$task_id" ]]; then
        print_msg "$RED" "用法: codex-tasks report <task_id> [channel]"
        return 1
    fi
    
    $AUTO_MERGE report "$task_id" "$channel"
}

# 清理
cleanup() {
    $REGISTRY cleanup "${1:-10}"
}

# 监控
monitor_start() {
    local interval="${1:-600}"
    $MONITOR start "$interval"
}

monitor_check() {
    $MONITOR check
}

# ========== 帮助 ==========

help() {
    cat <<EOF
╔═══════════════════════════════════════════════════════════════╗
║                    Codex Tasks v2.0                          ║
║              任务执行与自动化工作流                           ║
╚═══════════════════════════════════════════════════════════════╝

用法: codex-tasks <command> [options]

📥 接收任务 (OpenClaw 调用):
  execute <parent_id> <subtasks_json> [workspace]
    接收子任务列表并开始执行
  
  add-subtask <parent_id> <name> [description]
    添加单个子任务
  
  start <parent_id> [workspace]
    开始执行所有子任务

📊 监控:
  status [task_id]       查看状态
  monitor                实时监控
  logs <task_id>        查看日志
  check                  单次检查任务状态

🔧 干预:
  intervene <task_id> <message>
    干预任务（发送消息到 tmux）
  
  stop <task_id>        停止任务

✅ 完成后:
  auto-merge <task_id> [repo]  自动合并 PR
  report <task_id> [channel]  汇报任务完成

🧹 清理:
  cleanup [N]           清理已完成任务

📖 示例:
  # OpenClaw 拆解后调用
  codex-tasks execute parent-123 '[{"name":"API开发","description":"..."},{"name":"前端","description":"..."}]'
  
  # 或者逐个添加
  codex-tasks add-subtask parent-123 "API开发" "实现用户API"
  codex-tasks add-subtask parent-123 "前端" "实现登录页"
  codex-tasks start parent-123
  
  # 监控干预
  codex-tasks status
  codex-tasks intervene task-xxx "停下，先做X"

EOF
}

# 主命令
main() {
    local command="${1:-}"
    shift || true
    
    # 自动初始化
    if [[ "$command" != "init" && "$command" != "help" && -n "$command" ]]; then
        if [[ ! -f "/tmp/codex-tasks/active-tasks.json" ]]; then
            init
        fi
    fi
    
    case "$command" in
        init|i) init ;;
        
        # 任务接收与执行
        execute|run)
            execute "$@"
            ;;
        add-subtask|add)
            add_subtask "$@"
            ;;
        start|start-execution)
            start_execution "$@"
            ;;
        
        # 监控
        status|list|ls) status "$@" ;;
        monitor|watch) monitor ;;
        check) monitor_check ;;
        monitor-start) monitor_start "$@" ;;
        logs) logs "$@" ;;
        
        # 干预
        intervene|send) intervene "$@" ;;
        stop|kill) stop "$@" ;;
        
        # 完成后
        auto-merge|merge) auto_merge "$@" ;;
        report) report "$@" ;;
        
        # 清理
        cleanup|clean) cleanup "$@" ;;
        
        help|--help|-h|"") help ;;
        *) print_msg "$RED" "未知命令: $command"; help ;;
    esac
}

main "$@"
