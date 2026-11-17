#!/bin/bash
# DMP 任务监控服务停止脚本

MONITOR_DIR="/home/mlclaw/.dmp-monitor"
PID_FILE="$MONITOR_DIR/task_monitor.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        kill "$PID"
        echo "服务已停止 (PID: $PID)"
    else
        echo "服务未在运行"
    fi
    rm -f "$PID_FILE"
else
    echo "PID 文件不存在"
    # 尝试杀死所有相关进程
    pkill -f "task_monitor.py" 2>/dev/null
    echo "已尝试停止所有相关进程"
fi
