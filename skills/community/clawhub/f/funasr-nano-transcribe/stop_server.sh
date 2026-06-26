#!/bin/bash
# 停止 Fun-ASR-Nano-2512 FastAPI 服务

PID_FILE="/tmp/funasr_api.pid"

echo "🛑 正在停止 Fun-ASR-Nano-2512 服务..."

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        kill "$PID" 2>/dev/null
        sleep 2
        
        # 检查是否还在运行
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "⚠️ 服务未响应，强制停止..."
            kill -9 "$PID" 2>/dev/null
        fi
        
        rm -f "$PID_FILE"
        echo "✅ 服务已停止"
    else
        echo "⚠️ 服务未运行"
        rm -f "$PID_FILE"
    fi
else
    # 尝试通过端口查找进程
    PID=$(lsof -t -i:11890 2>/dev/null)
    if [ -n "$PID" ]; then
        kill "$PID" 2>/dev/null
        echo "✅ 服务已停止 (PID: $PID)"
    else
        echo "⚠️ 服务未运行"
    fi
fi
