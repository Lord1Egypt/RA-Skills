#!/bin/bash
#
# Monitor Daemon - 监控守护进程
# 定期执行所有活跃监控项

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="$(cd "$SCRIPT_DIR/../.." && pwd)"
MONITORS_DIR="$HOME/.cuecue/users/$CHAT_ID/monitors"
LOG_DIR="$HOME/.cuecue/logs"

mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_DIR/monitor-daemon.log"
}

# 执行单个监控
execute_monitor() {
    local monitor_file="$1"
    local monitor_id
    monitor_id=$(basename "$monitor_file" .json)
    
    log "🔔 执行监控: $monitor_id"
    
    # 调用 monitor-engine.sh
    if [ -f "$SCRIPT_DIR/executor/monitor-engine.sh" ]; then
        "$SCRIPT_DIR/executor/monitor-engine.sh" "$monitor_id" "$monitor_file"
    else
        log "⚠️ monitor-engine.sh 不存在"
    fi
}

# 主执行逻辑
main() {
    log "🚀 监控守护进程启动"
    
    if [ ! -d "$MONITORS_DIR" ]; then
        log "📭 暂无监控项目录"
        exit 0
    fi
    
    local count=0
    for monitor_file in "$MONITORS_DIR"/*.json; do
        if [ -f "$monitor_file" ]; then
            local status
            status=$(jq -r '.status // "active"' "$monitor_file" 2>/dev/null)
            
            if [ "$status" = "active" ]; then
                execute_monitor "$monitor_file"
                count=$((count + 1))
            fi
        fi
    done
    
    log "✅ 完成执行 $count 个监控项"
}

# 执行
main "$@"
