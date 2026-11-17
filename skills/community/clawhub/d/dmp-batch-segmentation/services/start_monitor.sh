#!/bin/bash
# DMP 任务监控服务启动脚本

MONITOR_DIR="/home/mlclaw/.dmp-monitor"
PID_FILE="$MONITOR_DIR/task_monitor.pid"
LOG_FILE="$MONITOR_DIR/service.log"

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "服务已在运行 (PID: $PID)"
        exit 0
    else
        echo "清理旧的 PID 文件"
        rm -f "$PID_FILE"
    fi
fi

# 启动服务
cd "$MONITOR_DIR"
nohup python3 task_monitor.py >> "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
echo "服务已启动 (PID: $!)"
