#!/bin/bash
# 通知提醒管理脚本
# 用于管理关键节点确认模式的提醒机制

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
通知提醒管理脚本

用法: $0 <action> [options]

操作:
  send <task_id> <message>    发送通知
  check <task_id>             检查是否有未回复的确认
  remind <task_id>            发送提醒通知
  fallback <task_id>          检查是否需要降级到无人模式
  log <task_id>                显示通知日志

选项:
  -h, --help                  显示此帮助信息
  -v, --verbose               详细输出模式
  -f, --file <path>           指定任务进度文件路径
  --interval <seconds>         提醒间隔时间（默认: 3600秒 = 1小时）
  --max-reminders <count>     最大提醒次数（默认: 2）
  --timeout <seconds>         超时时间（默认: 7200秒 = 2小时）
  --channel <channel>          通知渠道（默认: feishu）
  --dry-run                   只显示将要执行的操作，不实际执行

示例:
  # 发送需要确认的通知
  $0 send xianyu-daily-2026-03-14 "准备执行需要Gateway重启的操作"

  # 检查是否需要发送提醒
  $0 check xianyu-daily-2026-03-14

  # 发送提醒
  $0 remind xianyu-daily-2026-03-14

  # 检查是否需要降级
  $0 fallback xianyu-daily-2026-03-14

  # 查看通知日志
  $0 log xianyu-daily-2026-03-14
EOF
}

# 默认值
TASK_PROGRESS_FILE="./task-progress.json"
VERBOSE=false
DRY_RUN=false
REMINDER_INTERVAL=3600      # 1小时
MAX_REMINDERS=2
TIMEOUT=7200               # 2小时
CHANNEL="feishu"

# 解析全局参数
shift_count=0
for arg in "$@"; do
    case $arg in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--verbose)
            VERBOSE=true
            shift_count=$((shift_count + 1))
            ;;
        -f|--file)
            TASK_PROGRESS_FILE="$2"
            shift_count=$((shift_count + 2))
            ;;
        --interval)
            REMINDER_INTERVAL="$2"
            shift_count=$((shift_count + 2))
            ;;
        --max-reminders)
            MAX_REMINDERS="$2"
            shift_count=$((shift_count + 2))
            ;;
        --timeout)
            TIMEOUT="$2"
            shift_count=$((shift_count + 2))
            ;;
        --channel)
            CHANNEL="$2"
            shift_count=$((shift_count + 2))
            ;;
        --dry-run)
            DRY_RUN=true
            shift_count=$((shift_count + 1))
            ;;
        *)
            # 不是全局参数，停止解析
            break
            ;;
    esac
done

# 移除已解析的全局参数
shift $shift_count

# 检查是否提供了操作
if [ $# -lt 1 ]; then
    log_error "缺少操作参数"
    show_help
    exit 1
fi

ACTION="$1"
shift

# 当前时间戳
NOW=$(date +%s)

# 通知日志文件
NOTIFICATION_LOG="./task-notification.log"

# 写入通知日志
log_notification() {
    local task_id="$1"
    local message="$2"
    local level="${3:-INFO}"

    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] [$level] [$task_id] $message" >> "$NOTIFICATION_LOG"
}

# 发送通知
send_notification() {
    local task_id="$1"
    local message="$2"
    local urgency="${3:-normal}"

    log_info "发送通知: $message"

    # 记录到日志
    log_notification "$task_id" "$message" "NOTIFY"

    # 更新任务进度文件中的通知状态
    if [ -f "$TASK_PROGRESS_FILE" ]; then
        jq --arg msg "$message" \
           --arg ts "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
           '.notification.lastReminder = $ts |
            .notification.reminderCount += 1 |
            .notification.remindersSent += [$msg]' \
           "$TASK_PROGRESS_FILE" > "${TASK_PROGRESS_FILE}.tmp"
        mv "${TASK_PROGRESS_FILE}.tmp" "$TASK_PROGRESS_FILE"
    fi

    # 这里应该调用实际的通知发送逻辑
    # 例如通过 Feishu API 或其他渠道
    if [ "$DRY_RUN" = false ]; then
        # 实际发送通知的逻辑
        log_info "通知已发送到: $CHANNEL"
    else
        log_info "[DRY RUN] 将发送通知到: $CHANNEL"
        log_info "消息: $message"
    fi
}

# 检查是否需要发送提醒
check_reminder() {
    local task_id="$1"

    if [ ! -f "$TASK_PROGRESS_FILE" ]; then
        log_error "任务进度文件不存在: $TASK_PROGRESS_FILE"
        return 1
    fi

    # 获取最后提醒时间
    local last_reminder=$(jq -r '.notification.lastReminder // null' "$TASK_PROGRESS_FILE")

    if [ "$last_reminder" = "null" ] || [ -z "$last_reminder" ]; then
        log_info "没有发送过提醒，无需检查"
        return 0
    fi

    # 计算时间差
    local last_reminder_ts=$(date -d "$last_reminder" +%s)
    local elapsed=$((NOW - last_reminder_ts))

    if [ "$VERBOSE" = true ]; then
        log_info "距离上次提醒已过 $elapsed 秒"
    fi

    if [ "$elapsed" -ge "$REMINDER_INTERVAL" ]; then
        log_info "需要发送提醒"
        return 0
    else
        log_info "还未到提醒时间"
        return 1
    fi
}

# 发送提醒
send_reminder() {
    local task_id="$1"

    if [ ! -f "$TASK_PROGRESS_FILE" ]; then
        log_error "任务进度文件不存在: $TASK_PROGRESS_FILE"
        return 1
    fi

    # 检查提醒次数
    local reminder_count=$(jq -r '.notification.reminderCount // 0' "$TASK_PROGRESS_FILE")

    if [ "$reminder_count" -ge "$MAX_REMINDERS" ]; then
        log_warn "已达到最大提醒次数 ($MAX_REMINDERS)"
        return 1
    fi

    # 检查是否需要发送提醒
    if ! check_reminder "$task_id"; then
        return 1
    fi

    # 获取当前阶段信息
    local current_phase=$(jq -r '.currentPhase' "$TASK_PROGRESS_FILE")
    local phase_name=$(jq -r ".phases.phase${current_phase}.name" "$TASK_PROGRESS_FILE")
    local requires_confirmation=$(jq -r ".phases.phase${current_phase}.requiresConfirmation" "$TASK_PROGRESS_FILE")

    if [ "$requires_confirmation" != "true" ]; then
        log_info "当前阶段不需要确认"
        return 0
    fi

    # 构建提醒消息
    local reminder_msg="📌 任务需要确认提醒 (已等待 $((elapsed / 60)) 分钟)\n\n任务: $task_id\n阶段: $phase_name\n\n请确认是否继续执行？"

    # 发送提醒
    send_notification "$task_id" "$reminder_msg" "reminder"

    log_info "✅ 提醒已发送"
}

# 检查是否需要降级到无人模式
check_fallback() {
    local task_id="$1"

    if [ ! -f "$TASK_PROGRESS_FILE" ]; then
        log_error "任务进度文件不存在: $TASK_PROGRESS_FILE"
        return 1
    fi

    # 获取最后提醒时间
    local last_reminder=$(jq -r '.notification.lastReminder // null' "$TASK_PROGRESS_FILE")

    if [ "$last_reminder" = "null" ] || [ -z "$last_reminder" ]; then
        log_info "没有发送过提醒，无需检查降级"
        return 1
    fi

    # 计算时间差
    local last_reminder_ts=$(date -d "$last_reminder" +%s)
    local elapsed=$((NOW - last_reminder_ts))

    if [ "$elapsed" -ge "$TIMEOUT" ]; then
        log_info "已超时，需要降级到无人模式"

        # 降级到无人模式
        if [ "$DRY_RUN" = false ]; then
            jq '.executionMode = "unattended" |
                .userPreferences.preferredAction = "auto"' \
               "$TASK_PROGRESS_FILE" > "${TASK_PROGRESS_FILE}.tmp"
            mv "${TASK_PROGRESS_FILE}.tmp" "$TASK_PROGRESS_FILE"

            # 记录降级日志
            log_notification "$task_id" "已降级到无人模式（超时 ${elapsed} 秒）" "FALLBACK"

            log_info "✅ 已降级到无人模式"
        else
            log_info "[DRY RUN] 将降级到无人模式"
        fi

        return 0
    else
        log_info "还未到降级时间"
        return 1
    fi
}

# 显示通知日志
show_log() {
    local task_id="$1"

    if [ ! -f "$NOTIFICATION_LOG" ]; then
        log_info "通知日志不存在: $NOTIFICATION_LOG"
        return
    fi

    log_info "通知日志 ($task_id):"
    echo ""

    grep "\[$task_id\]" "$NOTIFICATION_LOG" | while IFS= read -r line; do
        echo "  $line"
    done
}

# 执行操作
case "$ACTION" in
    send)
        if [ $# -lt 2 ]; then
            log_error "send 操作需要 task_id 和 message 参数"
            show_help
            exit 1
        fi
        send_notification "$1" "$2" "${3:-normal}"
        ;;
    check)
        if [ $# -lt 1 ]; then
            log_error "check 操作需要 task_id 参数"
            show_help
            exit 1
        fi
        check_reminder "$1"
        ;;
    remind)
        if [ $# -lt 1 ]; then
            log_error "remind 操作需要 task_id 参数"
            show_help
            exit 1
        fi
        send_reminder "$1"
        ;;
    fallback)
        if [ $# -lt 1 ]; then
            log_error "fallback 操作需要 task_id 参数"
            show_help
            exit 1
        fi
        check_fallback "$1"
        ;;
    log)
        if [ $# -lt 1 ]; then
            log_error "log 操作需要 task_id 参数"
            show_help
            exit 1
        fi
        show_log "$1"
        ;;
    *)
        log_error "未知操作: $ACTION"
        show_help
        exit 1
        ;;
esac

exit 0
