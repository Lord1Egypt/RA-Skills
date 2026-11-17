#!/bin/bash
# DMP 任务监控服务检查脚本
# 如果服务未运行，则自动启动

MONITOR_DIR="/home/mlclaw/.dmp-monitor"
PID_FILE="$MONITOR_DIR/task_monitor.pid"
LOG_FILE="$MONITOR_DIR/service.log"

# 检查是否已在运行
RUNNING=false
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        RUNNING=true
    fi
fi

if [ "$RUNNING" = false ]; then
    # 服务未运行，启动它
    cd "$MONITOR_DIR"
    nohup python3 task_monitor.py >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 服务已自动启动 (PID: $!)" >> "$LOG_FILE"
fi
