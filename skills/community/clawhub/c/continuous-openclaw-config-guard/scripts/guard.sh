#!/bin/bash
# OpenClaw 配置回滚守护脚本
# 功能：备份、监控、重启、回滚

# ============ 环境与路径 ============
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=${XDG_RUNTIME_DIR}/bus"

CONFIG_FILE="${CONFIG_FILE:-$HOME/.openclaw/openclaw.json}"
BACKUP_DIR="${BACKUP_DIR:-$HOME/.openclaw/workspace/skills/continuous-openclaw-config-guard/backups}"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/workspace/skills/continuous-openclaw-config-guard/guard.log}"
PID_FILE="${PID_FILE:-$HOME/.openclaw/workspace/skills/continuous-openclaw-config-guard/guard.pid}"
SESSION_FILE="${SESSION_FILE:-$HOME/.openclaw/agents/huoxiaoxing/sessions/sessions.json}"
OPENCLAW_BIN="${OPENCLAW_BIN:-$HOME/.npm-global/bin/openclaw}"

# 默认策略
WAIT_TIME="${WAIT_TIME:-300}"
CHECK_INTERVAL="${CHECK_INTERVAL:-10}"

# ============ 工具函数 ============

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

get_mtime() {
    stat -c %Y "$1" 2>/dev/null || stat -f %m "$1" 2>/dev/null || echo 0
}

get_latest_backup() {
    ls -t "$BACKUP_DIR"/openclaw.json.[0-9]* 2>/dev/null | grep -v "\.note$" | head -1
}

create_backup() {
    local note="${1:-}"
    local backup_name="openclaw.json.$(date +%Y%m%d%H%M%S)"
    cp "$CONFIG_FILE" "$BACKUP_DIR/$backup_name"
    if [ -n "$note" ]; then
        echo "$note" > "$BACKUP_DIR/$backup_name.note"
        log "创建备份: $backup_name (备注: $note)"
    else
        log "创建备份: $backup_name"
    fi
    echo "$BACKUP_DIR/$backup_name"
}

restart_gateway() {
    log "开始重启网关..."
    "$OPENCLAW_BIN" gateway restart >> "$LOG_FILE" 2>&1
    sleep 5
    local status_output
    status_output=$("$OPENCLAW_BIN" gateway status 2>&1)
    if echo "$status_output" | grep -q "Runtime: running"; then
        log "网关重启成功，当前状态：Running"
        return 0
    else
        log "警告：网关重启失败或状态异常！"
        log "状态详情: $status_output"
        return 1
    fi
}

rollback_and_restart() {
    local backup_file="$1"
    log "=========================================="
    log "执行回滚流程..."
    log "目标备份: $(basename "$backup_file")"
    
    # 记录事故现场
    local failed_record="$BACKUP_DIR/openclaw.json.failed.$(date +%Y%m%d%H%M%S)"
    cp "$CONFIG_FILE" "$failed_record"
    log "已保存失败配置至: $(basename "$failed_record")"
    
    cp "$backup_file" "$CONFIG_FILE"
    restart_gateway
    log "回滚操作完成"
    log "=========================================="
}

show_help() {
    cat << EOF
用法: $(basename "$0") [选项]

选项:
  -s, --start           启动守护进程
  -w, --wait <秒>       设置验证等待时间 (默认: 300)
  -c, --check <秒>      设置监控检查间隔 (默认: 10)
  -r, --rollback        立即回滚到最新的稳定备份
  -l, --list            列出所有备份及其备注
  -k, --kill            停止正在运行的守护进程
  -h, --help            显示此帮助信息
EOF
}

# ============ 参数处理 ============

mkdir -p "$BACKUP_DIR"
touch "$LOG_FILE"

START_DAEMON=false
ROLLBACK_NOW=false
KILL_DAEMON=false

# 使用 while 循环处理完整参数
while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--start) START_DAEMON=true; shift ;;
        -w|--wait) WAIT_TIME="$2"; shift 2 ;;
        -c|--check) CHECK_INTERVAL="$2"; shift 2 ;;
        -r|--rollback) ROLLBACK_NOW=true; shift ;;
        -k|--kill) KILL_DAEMON=true; shift ;;
        -l|--list) 
            log "用户查询备份列表"
            ls -lt "$BACKUP_DIR" | grep "openclaw.json."
            exit 0 ;;
        -h|--help) show_help; exit 0 ;;
        *) echo "错误: 未知参数 $1"; show_help; exit 1 ;;
    esac
done

# --- 停止逻辑 ---
if [ "$KILL_DAEMON" = true ]; then
    log "停止守护进程..."
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        kill "$PID" 2>/dev/null && log "守护进程已停止 (PID: $PID)"
        rm -f "$PID_FILE"
    else
        pkill -f "guard.sh -s" 2>/dev/null && log "守护进程已停止"
    fi
    exit 0
fi

# --- 立即回滚逻辑 ---
if [ "$ROLLBACK_NOW" = true ]; then
    LATEST=$(get_latest_backup)
    if [ -z "$LATEST" ]; then
        echo "错误: 未找到任何备份文件"
        exit 1
    fi
    rollback_and_restart "$LATEST"
    exit 0
fi

# 如果没输入启动参数，显示帮助
if [ "$START_DAEMON" = false ]; then
    show_help
    exit 0
fi

# ============ 守护进程主循环 ============

# 写入 PID
echo $$ > "$PID_FILE"

log "=========================================="
log "OpenClaw 守护进程正式启动 (PID: $$)"
log "监控文件: $CONFIG_FILE"
log "配置参数: 等待 ${WAIT_TIME}s, 间隔 ${CHECK_INTERVAL}s"
log "=========================================="

# 初始准备
LATEST_STABLE=$(get_latest_backup)
if [ -z "$LATEST_STABLE" ]; then
    log "未发现历史记录，创建初始基准备份..."
    LATEST_STABLE=$(create_backup "Initial Baseline")
fi

LAST_CONFIG_MTIME=$(get_mtime "$CONFIG_FILE")
LAST_SESSION_MTIME=$(get_mtime "$SESSION_FILE")

MONITORING=false
MONITOR_START_TIME=0
LAST_LOGGED_MINUTE=0

while true; do
    sleep "$CHECK_INTERVAL"
    
    CUR_CONFIG_MTIME=$(get_mtime "$CONFIG_FILE")
    CUR_SESSION_MTIME=$(get_mtime "$SESSION_FILE")
    NOW=$(date +%s)

    # 1. 检测修改 (步骤3 -> 步骤4)
    if [ "$MONITORING" = false ] && [ "$CUR_CONFIG_MTIME" -ne "$LAST_CONFIG_MTIME" ]; then
        log "检测到 openclaw.json 修改"
        "$OPENCLAW_BIN" message send -t "!HwJBqEutNMXtWGuTAa:matrix.local" -m "OpenClaw配置被修改" --account huoxiaoxing >> "$LOG_FILE" 2>&1
        
        if restart_gateway; then
            # 重启成功 -> 进入验证阶段 (步骤5)
            log "网关重启成功，开启消息验证计时..."
            "$OPENCLAW_BIN" message send -t "!HwJBqEutNMXtWGuTAa:matrix.local" -m "OpenClaw配置被修改 -> 网关重启成功 -> 开始进行消息验证" --account huoxiaoxing >> "$LOG_FILE" 2>&1
            MONITORING=true
            MONITOR_START_TIME=$NOW
            LAST_LOGGED_MINUTE=0
            LAST_SESSION_MTIME=$(get_mtime "$SESSION_FILE") # 记录当前会话状态点
        else
            # 重启失败 -> 立即回滚 (步骤6)
            log "网关重启失败，立即回滚至稳定版本"
            "$OPENCLAW_BIN" message send -t "!HwJBqEutNMXtWGuTAa:matrix.local" -m "OpenClaw配置被修改 -> 网关重启失败 -> 回滚至稳定版本，回归正常监控" --account huoxiaoxing >> "$LOG_FILE" 2>&1
            rollback_and_restart "$LATEST_STABLE"
            # 刷新时间戳，防止因回滚文件操作导致再次触发
            CUR_CONFIG_MTIME=$(get_mtime "$CONFIG_FILE")
        fi
    fi

    # 2. 验证阶段逻辑处理
    if [ "$MONITORING" = true ]; then
        ELAPSED=$((NOW - MONITOR_START_TIME))
        
        # A. 收到新消息 -> 验证成功
        if [ "$CUR_SESSION_MTIME" -gt "$LAST_SESSION_MTIME" ]; then
            log "检测到新消息活动！新配置已通过验证"
            LATEST_STABLE=$(create_backup "Verified Stable Config")
            MONITORING=false
            log "验证期结束，回归正常监控状态"
            "$OPENCLAW_BIN" message send -t "!HwJBqEutNMXtWGuTAa:matrix.local" -m "OpenClaw配置被修改 -> 网关重启成功 -> 开始进行消息验证 -> 消息验证通过 -> 新配置已备份，回归正常监控" --account huoxiaoxing >> "$LOG_FILE" 2>&1
        
        # B. 超时 -> 验证失败
        elif [ "$ELAPSED" -ge "$WAIT_TIME" ]; then
            log "超时未检测到消息 (${WAIT_TIME}s)，判定为故障配置"
            "$OPENCLAW_BIN" message send -t "!HwJBqEutNMXtWGuTAa:matrix.local" -m "OpenClaw配置被修改 -> 网关重启成功 -> 开始进行消息验证 -> 超时未检测到消息 (${WAIT_TIME}s)，判定为故障配置 -> 回滚至稳定版本，回归正常监控" --account huoxiaoxing >> "$LOG_FILE" 2>&1
            rollback_and_restart "$LATEST_STABLE"
            MONITORING=false
            CUR_CONFIG_MTIME=$(get_mtime "$CONFIG_FILE")
        
        # C. 进度日志
        else
            CUR_MINUTE=$((ELAPSED / 60))
            if [ "$CUR_MINUTE" -gt "$LAST_LOGGED_MINUTE" ]; then
                REMAINING=$((WAIT_TIME - ELAPSED))
                log "验证监控中: 已耗时 ${ELAPSED}s，剩余 ${REMAINING}s..."
                "$OPENCLAW_BIN" message send -t "!HwJBqEutNMXtWGuTAa:matrix.local" -m "OpenClaw配置被修改 -> 网关重启成功 -> 开始进行消息验证 -> 验证监控中: 已耗时 ${ELAPSED}s，剩余 ${REMAINING}s..." --account huoxiaoxing >> "$LOG_FILE" 2>&1
                LAST_LOGGED_MINUTE=$CUR_MINUTE
            fi
        fi
    fi

    LAST_CONFIG_MTIME=$CUR_CONFIG_MTIME
done