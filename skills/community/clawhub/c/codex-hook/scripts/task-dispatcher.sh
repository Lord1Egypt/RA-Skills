#!/bin/bash
# task-dispatcher.sh - 任务调度器
# 支持并行执行、tmux 隔离、git worktree、中途干预

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REGISTRY="$SCRIPT_DIR/task-registry.sh"
SPLITTER="$SCRIPT_DIR/task-splitter.sh"

CODEX_DIR="${CODEX_DIR:-$HOME/.codex-agent}"
MAX_PARALLEL="${MAX_PARALLEL:-3}"
RESULT_DIR="${CODEX_RESULT_DIR:-/tmp/codex-results}"
WORKTREE_DIR="${WORKTREE_DIR:-$HOME/codex-worktrees}"
REPO_DIR="${REPO_DIR:-$HOME/projects}"
MAIN_BRANCH="${MAIN_BRANCH:-main}"

# 初始化调度器
init_dispatcher() {
    mkdir -p "$RESULT_DIR/tasks"
    mkdir -p "$WORKTREE_DIR"
    $REGISTRY init
    echo "调度器初始化完成"
}

# 创建 git worktree
create_worktree() {
    local task_id="$1"
    local branch_name="codex-$task_id"
    local worktree_path="$WORKTREE_DIR/$task_id"
    
    # 检查是否是 git 仓库
    if ! cd "$REPO_DIR" && ! git rev-parse --git-dir &>/dev/null; then
        echo "Error: $REPO_DIR 不是 git 仓库" >&2
        return 1
    fi
    
    cd "$REPO_DIR"
    
    # 检查 worktree 是否已存在
    if [[ -d "$worktree_path" ]]; then
        echo "Worktree 已存在，删除旧的" >&2
        git worktree remove --force "$worktree_path" 2>/dev/null || true
        git branch -D "$branch_name" 2>/dev/null || true
    fi
    
    # 创建新 worktree（只返回路径）
    if git worktree add "$worktree_path" -b "$branch_name" "$MAIN_BRANCH" &>/dev/null; then
        # 只输出路径（用于变量赋值）
        echo "$worktree_path"
        return 0
    else
        echo "❌ Worktree 创建失败: $branch_name" >&2
        return 1
    fi
}

# 清理 worktree
cleanup_worktree() {
    local task_id="$1"
    local worktree_path="$WORKTREE_DIR/$task_id"
    
    if [[ -d "$worktree_path" ]]; then
        cd "$REPO_DIR"
        git worktree remove --force "$worktree_path" 2>/dev/null || true
        git branch -D "codex-$task_id" 2>/dev/null || true
        echo "🧹 清理 worktree: $task_id"
    fi
}

# 派发单个任务到 tmux + worktree
dispatch_task() {
    local task_id="$1"
    local prompt="$2"
    local workspace="${3:-$REPO_DIR}"
    local agent="${4:-codex}"
    
    echo "📤 派发任务: $task_id"
    
    # 获取任务信息
    local task_info
    task_info=$($REGISTRY get "$task_id")
    
    if [[ -z "$task_info" || "$task_info" == "null" ]]; then
        echo "Error: Task $task_id not found"
        return 1
    fi
    
    # 创建 worktree（如果使用 worktree 模式）
    local worktree_path=""
    if [[ "${USE_WORKTREE:-true}" == "true" ]]; then
        worktree_path=$(create_worktree "$task_id")
        if [[ -z "$worktree_path" ]]; then
            echo "Worktree 创建失败，回退到共享目录"
            worktree_path="$workspace"
        else
            echo "✅ Worktree 创建成功: $worktree_path"
        fi
    else
        worktree_path="$workspace"
    fi
    
    # 生成 tmux 会话名
    local tmux_session="codex-$task_id"
    
    # 更新任务状态
    $REGISTRY update "$task_id" "status" "running"
    $REGISTRY update "$task_id" "tmux_session" "$tmux_session"
    $REGISTRY update "$task_id" "branch" "codex-$task_id"
    $REGISTRY update "$task_id" "workspace" "$worktree_path"
    $REGISTRY log "$task_id" "开始执行任务 (worktree: $worktree_path)" "info"
    
    # 创建任务目录
    local task_dir="$RESULT_DIR/tasks/$task_id"
    mkdir -p "$task_dir"
    
    # 写入任务提示词
    echo "$prompt" > "$task_dir/prompt.txt"
    
    # 检查 tmux 是否可用
    if ! command -v tmux &>/dev/null; then
        echo "⚠️ tmux 不可用，使用后台执行"
        # 后台执行
        (
            execute_task "$task_id" "$prompt" "$worktree_path" "$agent" 2>&1 | tee "$task_dir/output.log"
        ) &
        return 0
    fi
    
    # 创建 tmux 会话
    if tmux has-session -t "$tmux_session" 2>/dev/null; then
        echo "会话已存在，终止旧的"
        tmux kill-session -t "$tmux_session"
    fi
    
    # 创建新会话（使用 worktree 目录）
    tmux new-session -d -s "$tmux_session" -c "$worktree_path"
    
    # 发送执行命令
    local prompt_text
    prompt_text=$(cat "$task_dir/prompt.txt")
    local cmd="cd '$worktree_path' && codex --sandbox workspace-write --full-auto exec \"$prompt_text\""
    
    tmux send-keys -t "$tmux_session" "$cmd" Enter
    
    echo "✅ 任务已派发，会话: $tmux_session, 目录: $worktree_path"
    echo "   监控: tmux attach -t $tmux_session"
    echo "   日志: tail -f $task_dir/output.log"
    
    return 0
}

# 执行任务（无 tmux）
execute_task() {
    local task_id="$1"
    local prompt="$2"
    local workspace="${3:-$REPO_DIR}"
    local agent="${4:-codex}"
    
    cd "$workspace"
    
    # 记录开始
    $REGISTRY progress "$task_id" 10 "running"
    
    # 执行 codex
    if command -v codex &>/dev/null; then
        codex --sandbox workspace-write --full-auto exec "$prompt"
    elif [[ -x "$CODEX_DIR/run-agent.sh" ]]; then
        "$CODEX_DIR/run-agent.sh" "$agent" "$prompt"
    else
        echo "Error: 未找到 Codex 执行方式"
        $REGISTRY progress "$task_id" 0 "failed"
        return 1
    fi
    
    # 标记完成
    $REGISTRY complete "$task_id"
    $REGISTRY progress "$task_id" 100 "done"
}

# 并行派发多个任务
dispatch_parallel() {
    local task_ids=("$@")
    local pids=()
    
    echo "🚀 并行派发 ${#task_ids[@]} 个任务"
    echo "================================================================"
    
    # 限制并发数
    local running=0
    local max_running=$MAX_PARALLEL
    
    for task_id in "${task_ids[@]}"; do
        # 等待直到有槽位
        while [[ $running -ge $max_running ]]; do
            sleep 2
            running=$(get_running_count)
        done
        
        # 派发任务
        local task_info
        task_info=$($REGISTRY get "$task_id")
        
        local prompt
        prompt=$($REGISTRY get "$task_id" | jq -r '.description')
        
        dispatch_task "$task_id" "$prompt" &
        pids+=($!)
        
        ((running++))
    done
    
    # 等待所有任务完成
    for pid in "${pids[@]}"; do
        wait "$pid" 2>/dev/null || true
    done
    
    echo "================================================================"
    echo "✅ 所有任务派发完成"
}

# 获取运行中的任务数
get_running_count() {
    $REGISTRY json | jq '[.tasks[] | select(.status == "running")] | length' 2>/dev/null || echo "0"
}

# 监控任务
monitor_tasks() {
    echo "📊 任务监控 (每10秒刷新, Ctrl+C 退出)"
    echo "================================================================"
    
    while true; do
        clear
        echo "📊 任务监控 - $(date '+%H:%M:%S')"
        echo "================================================================"
        
        $REGISTRY list
        
        # 检查是否有完成的任务
        local done_count
        done_count=$($REGISTRY json | jq '[.tasks[] | select(.status == "done")] | length')
        
        if [[ $done_count -gt 0 ]]; then
            echo ""
            echo "🎉 有 $done_count 个任务已完成"
        fi
        
        sleep 10
    done
}

# 干预任务
intervene() {
    local task_id="$1"
    local message="$2"
    
    echo "📝 干预任务: $task_id"
    echo "消息: $message"
    
    # 获取 tmux 会话
    local tmux_session
    tmux_session=$($REGISTRY get "$task_id" | jq -r '.tmux_session')
    
    if [[ -z "$tmux_session" || "$tmux_session" == "null" ]]; then
        echo "⚠️ 任务未在 tmux 中运行"
        return 1
    fi
    
    # 检查 tmux 会话是否存在
    if ! tmux has-session -t "$tmux_session" 2>/dev/null; then
        echo "⚠️ tmux 会话不存在"
        return 1
    fi
    
    # 发送消息
    tmux send-keys -t "$tmux_session" "$message" Enter
    
    # 记录干预
    $REGISTRY log "$task_id" "人工干预: $message" "warning"
    
    echo "✅ 消息已发送"
}

# 停止任务
stop_task() {
    local task_id="$1"
    
    echo "🛑 停止任务: $task_id"
    
    # 获取 tmux 会话
    local tmux_session
    tmux_session=$($REGISTRY get "$task_id" | jq -r '.tmux_session')
    
    if [[ -n "$tmux_session" && "$tmux_session" != "null" ]]; then
        if tmux has-session -t "$tmux_session" 2>/dev/null; then
            tmux kill-session -t "$tmux_session"
            echo "✅ tmux 会话已终止"
        fi
    fi
    
    # 清理 worktree
    cleanup_worktree "$task_id"
    
    # 更新状态
    $REGISTRY update "$task_id" "status" "stopped"
    $REGISTRY log "$task_id" "任务被停止" "error"
    
    echo "任务已停止"
}

# 检查任务状态
check_status() {
    local task_id="$1"
    
    local task_info
    task_info=$($REGISTRY get "$task_id")
    
    if [[ -z "$task_info" || "$task_info" == "null" ]]; then
        echo "任务不存在"
        return 1
    fi
    
    local status tmux_session progress branch workspace
    status=$(echo "$task_info" | jq -r '.status')
    tmux_session=$(echo "$task_info" | jq -r '.tmux_session')
    progress=$(echo "$task_info" | jq -r '.progress')
    branch=$(echo "$task_info" | jq -r '.branch')
    workspace=$(echo "$task_info" | jq -r '.workspace')
    
    echo "📋 任务: $task_id"
    echo "状态: $status"
    echo "进度: $progress%"
    echo "tmux: $tmux_session"
    echo "分支: $branch"
    echo "目录: $workspace"
    
    # 检查 tmux
    if [[ -n "$tmux_session" && "$tmux_session" != "null" ]]; then
        if tmux has-session -t "$tmux_session" 2>/dev/null; then
            echo "tmux 会话: ✅ 运行中"
        else
            echo "tmux 会话: ❌ 已结束"
        fi
    fi
}

# 创建 PR
create_pr() {
    local task_id="$1"
    local title="${2:-}"
    local description="${3:-}"
    
    local task_info
    task_info=$($REGISTRY get "$task_id")
    
    local branch
    branch=$(echo "$task_info" | jq -r '.branch')
    
    if [[ -z "$branch" || "$branch" == "null" ]]; then
        echo "任务无分支信息"
        return 1
    fi
    
    cd "$REPO_DIR"
    
    # 推送分支
    git push -u origin "$branch" 2>&1 || true
    
    # 创建 PR
    local pr_info
    pr_info=$(gh pr create --title "$title" --body "$description" --base "$MAIN_BRANCH" 2>&1)
    
    if echo "$pr_info" | grep -qE "^https?://"; then
        echo "✅ PR 创建成功: $pr_info"
        echo "$pr_info" | grep -oE '[0-9]+$'
    else
        echo "❌ PR 创建失败: $pr_info"
        return 1
    fi
}

# 帮助
show_help() {
    cat <<EOF
task-dispatcher.sh - 任务调度器 (支持 Worktree)

用法: task-dispatcher.sh <command> [options]

环境变量:
  USE_WORKTREE       是否使用 worktree (默认 true)
  WORKTREE_DIR       worktree 目录 (默认 ~/codex-worktrees)
  REPO_DIR           主仓库目录 (默认 ~/projects)
  MAIN_BRANCH       主分支名 (默认 main)

命令:
  init                   初始化调度器
  
  dispatch <task_id> <prompt> [workspace] [agent]
    派发单个任务 (使用 worktree)
  
  parallel <task_ids...>
    并行派发多个任务
  
  monitor                监控任务状态
  
  intervene <task_id> <message>
    干预任务（发送消息到 tmux）
  
  stop <task_id>         停止任务
  
  status <task_id>       查看任务状态
  
  create-pr <task_id> <title> <desc>
    为任务创建 PR

示例:
  USE_WORKTREE=true task-dispatcher.sh dispatch task-xxx "实现登录功能"
  task-dispatcher.sh status task-xxx
  task-dispatcher.sh create-pr task-xxx "feat: 添加登录功能"
EOF
}

# 主命令
main() {
    local command="${1:-}"
    shift || true
    
    case "$command" in
        init)
            init_dispatcher
            ;;
        dispatch)
            dispatch_task "$@"
            ;;
        parallel)
            shift
            dispatch_parallel "$@"
            ;;
        monitor|watch)
            monitor_tasks
            ;;
        intervene|send)
            intervene "$@"
            ;;
        stop|kill)
            stop_task "$@"
            ;;
        status)
            check_status "$@"
            ;;
        create-pr|pr)
            create_pr "$@"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            show_help
            ;;
    esac
}

main "$@"
