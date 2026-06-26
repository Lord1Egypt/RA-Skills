#!/bin/bash
# 执行模式选择脚本
# 用于在任务开始前选择执行模式（无人模式或关键节点确认模式）

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示帮助信息
show_help() {
    cat << EOF
执行模式选择脚本

用法: $0 [选项]

选项:
  -h, --help              显示此帮助信息
  -f, --file <path>        指定任务进度文件路径 (默认: ./task-progress.json)
  -m, --mode <mode>        直接指定模式 (unattended/confirmation)
  --no-interaction        非交互模式，使用默认配置
  --night-mode            启用夜间模式
  --night-start <time>    夜间模式开始时间 (默认: 22:00)
  --night-end <time>      夜间模式结束时间 (默认: 08:00)

示例:
  # 交互式选择模式
  $0

  # 直接使用无人模式
  $0 -m unattended

  # 启用夜间模式
  $0 --night-mode --night-start 22:00 --night-end 08:00

  # 非交互模式，使用默认配置
  $0 --no-interaction
EOF
}

# 默认值
TASK_PROGRESS_FILE="./task-progress.json"
INTERACTIVE=true
NIGHT_MODE=false
NIGHT_START="22:00"
NIGHT_END="08:00"

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -f|--file)
            TASK_PROGRESS_FILE="$2"
            shift 2
            ;;
        -m|--mode)
            EXECUTION_MODE="$2"
            shift 2
            ;;
        --no-interaction)
            INTERACTIVE=false
            shift
            ;;
        --night-mode)
            NIGHT_MODE=true
            shift
            ;;
        --night-start)
            NIGHT_START="$2"
            shift 2
            ;;
        --night-end)
            NIGHT_END="$2"
            shift 2
            ;;
        *)
            log_error "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 检查任务进度文件是否存在
if [ ! -f "$TASK_PROGRESS_FILE" ]; then
    log_error "任务进度文件不存在: $TASK_PROGRESS_FILE"
    exit 1
fi

# 显示任务信息
echo ""
echo "=========================================="
echo "      执行模式选择"
echo "=========================================="
echo ""
echo "任务信息:"
jq -r '"  任务名称: \(.taskName)\n  任务 ID: \(.taskId)\n  总阶段数: \(.totalPhases)"' "$TASK_PROGRESS_FILE"
echo ""

# 如果交互模式
if [ "$INTERACTIVE" = true ]; then
    echo "请选择执行模式:"
    echo ""
    echo "1) 🌙 夜间无人模式"
    echo "   - 提前收集所有必要信息"
    echo "   - 在用户休息期间自助决策完成任务"
    echo "   - 适合：夜间批量任务、长时间运行的任务"
    echo ""
    echo "2) 🔑 关键节点确认模式"
    echo "   - 关键操作需要用户确认"
    echo "   - 超时后自动降级到无人模式"
    echo "   - 适合：需要人工干预的重要任务"
    echo ""
    read -p "请输入选项 (1/2) [默认: 2]: " mode_choice

    case "$mode_choice" in
        1)
            EXECUTION_MODE="unattended"
            log_info "已选择: 夜间无人模式"
            ;;
        2|"")
            EXECUTION_MODE="confirmation"
            log_info "已选择: 关键节点确认模式"
            ;;
        *)
            log_error "无效的选项"
            exit 1
            ;;
    esac
else
    # 非交互模式，使用默认模式
    EXECUTION_MODE="${EXECUTION_MODE:-confirmation}"
    log_info "非交互模式，使用默认执行模式: $EXECUTION_MODE"
fi

# 收集用户偏好
echo ""
echo "=========================================="
echo "      用户偏好设置"
echo "=========================================="
echo ""

# 无人模式的预配置信息收集
if [ "$EXECUTION_MODE" = "unattended" ] || [ "$NIGHT_MODE" = true ]; then
    log_info "无人模式需要提前收集必要信息..."
    echo ""

    # 创建临时配置文件
    PREF_FILE="$(dirname "$TASK_PROGRESS_FILE")/.user-preferences.json"

    cat > "$PREF_FILE" << EOF
{
  "confirmations": {
    "gatewayRestart": {
      "allowed": false,
      "alternative": "使用缓存或降级方案"
    },
    "fileOperations": {
      "allowed": true,
      "safePaths": [
        "/root/.openclaw/workspace",
        "/root/.openclaw/workspace/xianyu-automation"
      ]
    },
    "apiCalls": {
      "allowed": true,
      "rateLimit": 100
    },
    "criticalOperations": {
      "allowed": false,
      "autoFallback": true
    }
  },
  "fallbackStrategies": {
    "critical": "skip_or_fallback",
    "nonCritical": "auto_proceed"
  },
  "notification": {
    "enabled": true,
    "onlyOnCritical": true
  }
}
EOF

    log_info "已创建用户偏好文件: $PREF_FILE"

    # 如果是交互模式，询问是否需要修改
    if [ "$INTERACTIVE" = true ]; then
        read -p "是否需要修改默认配置? (y/N) [默认: N]: " modify_pref
        if [[ "$modify_pref" =~ ^[Yy]$ ]]; then
            ${EDITOR:-nano} "$PREF_FILE"
        fi
    fi
fi

# 更新任务进度文件
log_info "更新任务进度文件..."

# 使用 jq 更新执行模式和用户偏好
if [ -f "$PREF_FILE" ]; then
    # 如果有偏好文件，读取并合并
    jq --arg mode "$EXECUTION_MODE" \
       --argjson night_mode "$NIGHT_MODE" \
       --arg night_start "$NIGHT_START" \
       --arg night_end "$NIGHT_END" \
       '.executionMode = $mode |
        .userPreferences.nightModeEnabled = $night_mode |
        .userPreferences.nightModeStart = $night_start |
        .userPreferences.nightModeEnd = $night_end |
        .userPreferences.preferredAction = (if $mode == "unattended" then "auto" else "ask-critical" end) |
        .userPreferences.autoFallbackToUnattended = (if $mode == "unattended" then false else true end)' \
       "$TASK_PROGRESS_FILE" > "${TASK_PROGRESS_FILE}.tmp"
else
    # 没有偏好文件，只更新基本配置
    jq --arg mode "$EXECUTION_MODE" \
       --argjson night_mode "$NIGHT_MODE" \
       --arg night_start "$NIGHT_START" \
       --arg night_end "$NIGHT_END" \
       '.executionMode = $mode |
        .userPreferences.nightModeEnabled = $night_mode |
        .userPreferences.nightModeStart = $night_start |
        .userPreferences.nightModeEnd = $night_end |
        .userPreferences.preferredAction = (if $mode == "unattended" then "auto" else "ask-critical" end) |
        .userPreferences.autoFallbackToUnattended = (if $mode == "unattended" then false else true end)' \
       "$TASK_PROGRESS_FILE" > "${TASK_PROGRESS_FILE}.tmp"
fi

# 替换原文件
mv "${TASK_PROGRESS_FILE}.tmp" "$TASK_PROGRESS_FILE"

log_info "✅ 任务配置已更新"
echo ""
echo "=========================================="
echo "      配置摘要"
echo "=========================================="
echo ""
jq -r '"执行模式: \(.executionMode)\n夜间模式: \(.userPreferences.nightModeEnabled)\n夜间时段: \(.userPreferences.nightModeStart) - \(.userPreferences.nightModeEnd)\n默认操作: \(.userPreferences.preferredAction)\n自动降级: \(.userPreferences.autoFallbackToUnattended)"' "$TASK_PROGRESS_FILE"
echo ""
echo "=========================================="
echo ""

log_info "任务已准备就绪，可以开始执行！"
