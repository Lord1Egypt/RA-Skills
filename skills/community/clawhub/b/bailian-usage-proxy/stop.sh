#!/bin/bash
# 停止服务脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/proxy.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "停止服务 (PID: $PID)..."
        kill "$PID"
        sleep 2
        
        # 强制停止
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "强制停止..."
            kill -9 "$PID" 2>/dev/null
        fi
        
        rm -f "$PID_FILE"
        echo "✅ 服务已停止"
    else
        echo "服务未运行"
        rm -f "$PID_FILE"
    fi
else
    echo "未找到 PID 文件，服务可能未运行"
    
    # 尝试查找并停止
    PID=$(pgrep -f "app.main" | head -1)
    if [ -n "$PID" ]; then
        echo "找到进程 $PID，正在停止..."
        kill "$PID" 2>/dev/null
        sleep 1
        kill -9 "$PID" 2>/dev/null
        echo "✅ 服务已停止"
    fi
fi
