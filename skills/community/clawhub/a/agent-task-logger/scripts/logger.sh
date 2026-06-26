#!/bin/bash
# Agent Task Logger - 任务日志工具脚本
# 自动检测 Agent 工作空间位置

# 自动检测工作空间（优先级从高到低）
# 1. WORKSPACE 环境变量
# 2. OPENCLAW_WORKSPACE 环境变量
# 3. 当前目录的父目录（如果在 skills 目录中）
# 4. ~/.openclaw/workspace
# 5. .openclaw/workspace
detect_workspace() {
    if [ -n "$WORKSPACE" ]; then
        echo "$WORKSPACE"
    elif [ -n "$OPENCLAW_WORKSPACE" ]; then
        echo "$OPENCLAW_WORKSPACE"
    elif [ -f "$(dirname "$0")/../.openclaw/workspace" ]; then
        echo "$(cd "$(dirname "$0")/.." && pwd)"
    elif [ -d "$HOME/.openclaw/workspace" ]; then
        echo "$HOME/.openclaw/workspace"
    elif [ -d "./.openclaw/workspace" ]; then
        echo "$(pwd)/.openclaw/workspace"
    else
        # 默认当前目录
        echo "$(pwd)"
    fi
}

WORKSPACE=$(detect_workspace)
LOG_DIR="${WORKSPACE}/logs"
LOG_FILE="${LOG_FILE:-agent-task.log}"
LOG_PATH="${LOG_DIR}/${LOG_FILE}"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

# 获取当前时间（格式：04-3 月 -2026 17:38:00.000）
get_timestamp() {
    date +"%d-%-m 月 -%Y %H:%M:%S.000"
}

# 写入日志
log() {
    local level="$1"
    local thread="$2"
    local class="$3"
    local message="$4"
    echo "$(get_timestamp) ${level} [${thread}] ${class} ${message}" >> "$LOG_PATH"
}

# 初始化日志系统（自动检测工作空间）
init() {
    local workspace="$1"
    
    # 如果没有指定工作空间，使用自动检测的
    if [ -z "$workspace" ]; then
        workspace="$WORKSPACE"
    fi
    
    LOG_DIR="${workspace}/logs"
    LOG_PATH="${LOG_DIR}/${LOG_FILE}"
    mkdir -p "$LOG_DIR"
    
    log "INFO" "main" "org.apache.catalina.startup.VersionLoggerListener.log" "Agent 任务日志系统已初始化"
    log "INFO" "main" "org.apache.catalina.startup.VersionLoggerListener.log" "工作空间：${workspace} (自动检测)"
    log "INFO" "main" "org.apache.catalina.startup.VersionLoggerListener.log" "日志文件：${LOG_PATH}"
    log "INFO" "main" "org.apache.catalina.startup.VersionLoggerListener.log" "============================================================"
    echo "✅ 日志系统已初始化"
    echo "   工作空间：${workspace}"
    echo "   日志文件：${LOG_PATH}"
}

# 记录任务开始
task_start() {
    local task_id="$1"
    local task_name="$2"
    local estimated="$3"
    log "INFO" "${task_id}" "com.openclaw.agent.TaskExecutor.execute" "任务：${task_name}"
    [ -n "$estimated" ] && log "INFO" "${task_id}" "com.openclaw.agent.TaskExecutor.execute" "预估时间：${estimated}"
}

# 记录执行命令
task_command() {
    local task_id="$1"
    local command="$2"
    log "INFO" "${task_id}" "com.openclaw.agent.TaskExecutor.execute" "执行命令：${command}"
}

# 记录任务状态
task_status() {
    local task_id="$1"
    local status="$2"
    local actual_time="$3"
    log "INFO" "${task_id}" "com.openclaw.agent.TaskExecutor.execute" "状态：${status}"
    [ -n "$actual_time" ] && log "INFO" "${task_id}" "com.openclaw.agent.TaskExecutor.execute" "实际时间：${actual_time}"
    log "INFO" "${task_id}" "com.openclaw.agent.TaskExecutor.execute" "结果：${status}"
}

# 记录错误
task_error() {
    local task_id="$1"
    local error="$2"
    log "ERROR" "${task_id}" "com.openclaw.agent.TaskExecutor.execute" "错误：${error}"
}

# 显示工作空间信息
show_info() {
    echo "Agent Task Logger - 信息"
    echo ""
    echo "当前工作空间：${WORKSPACE}"
    echo "日志目录：${LOG_DIR}"
    echo "日志文件：${LOG_PATH}"
    echo ""
    if [ -f "$LOG_PATH" ]; then
        echo "日志文件大小：$(ls -lh "$LOG_PATH" | awk '{print $5}')"
        echo "最后更新：$(ls -l "$LOG_PATH" | awk '{print $6, $7, $8}')"
    else
        echo "日志文件：不存在（首次运行将自动创建）"
    fi
}

# 显示帮助
show_help() {
    echo "Agent Task Logger - 任务日志工具"
    echo ""
    echo "用法：$0 <action> [options]"
    echo ""
    echo "Actions:"
    echo "  init [workspace]              初始化日志系统（自动检测工作空间）"
    echo "  start <task-id> <name> [time] 记录任务开始"
    echo "  command <task-id> <cmd>       记录执行命令"
    echo "  status <task-id> <status> [time] 记录任务状态"
    echo "  error <task-id> <error>       记录错误信息"
    echo "  info                          显示工作空间和日志信息"
    echo "  tail                          实时查看日志"
    echo "  help                          显示帮助"
    echo ""
    echo "环境变量:"
    echo "  WORKSPACE            指定工作空间路径"
    echo "  OPENCLAW_WORKSPACE   指定 OpenClaw 工作空间路径"
    echo "  LOG_FILE             指定日志文件名（默认：agent-task.log）"
    echo ""
    echo "工作空间检测顺序:"
    echo "  1. WORKSPACE 环境变量"
    echo "  2. OPENCLAW_WORKSPACE 环境变量"
    echo "  3. 脚本所在目录的父目录"
    echo "  4. ~/.openclaw/workspace"
    echo "  5. 当前目录"
    echo ""
    echo "示例:"
    echo "  # 自动检测工作空间（推荐）"
    echo "  $0 init"
    echo ""
    echo "  # 手动指定工作空间"
    echo "  $0 init /path/to/workspace"
    echo ""
    echo "  # 使用环境变量"
    echo "  export WORKSPACE=/path/to/workspace"
    echo "  $0 init"
    echo ""
    echo "  # 记录任务"
    echo "  $0 start task-001 '停止 Tomcat 8' 5s"
    echo "  $0 command task-001 './shutdown.sh'"
    echo "  $0 status task-001 成功 3.5s"
    echo ""
    echo "  # 查看日志"
    echo "  $0 tail"
    echo "  $0 info"
}

# 主程序
case "$1" in
    init)
        init "$2"
        ;;
    start)
        task_start "$2" "$3" "$4"
        ;;
    command)
        task_command "$2" "$3"
        ;;
    status)
        task_status "$2" "$3" "$4"
        ;;
    error)
        task_error "$2" "$3"
        ;;
    info)
        show_info
        ;;
    tail)
        tail -f "$LOG_PATH"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "错误：未知操作 '$1'"
        echo "使用 '$0 help' 查看帮助"
        exit 1
        ;;
esac
