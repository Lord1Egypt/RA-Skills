#!/bin/bash
# 查看服务状态

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$SCRIPT_DIR/proxy.pid"
LOG_FILE="$SCRIPT_DIR/logs/proxy.log"

echo "========================================"
echo "阿里百炼用量统计代理 - 服务状态"
echo "========================================"
echo ""

# 检查 PID 文件
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "✅ 服务运行中"
        echo "   PID: $PID"
        echo "   启动时间: $(ps -o lstart= -p "$PID")"
        echo "   CPU: $(ps -o %cpu= -p "$PID")%"
        echo "   内存: $(ps -o rss= -p "$PID" | awk '{print int($1/1024)"MB"}')"
        echo ""
        echo "📊 访问地址:"
        echo "   API: http://localhost:8080"
        echo "   管理后台: http://localhost:8081"
        echo ""
        echo "📁 日志文件: $LOG_FILE"
        
        # 显示最近日志
        if [ -f "$LOG_FILE" ]; then
            echo ""
            echo "📝 最近5条日志:"
            tail -5 "$LOG_FILE" 2>/dev/null | sed 's/^/   /'
        fi
    else
        echo "❌ 服务未运行（PID文件存在但进程不存在）"
        rm -f "$PID_FILE"
    fi
else
    echo "❌ 服务未运行（无PID文件）"
    
    # 尝试查找进程
    PID=$(pgrep -f "app.main" | head -1)
    if [ -n "$PID" ]; then
        echo "⚠️  发现孤儿进程: $PID"
        echo "   建议执行: ./stop.sh 后重新启动"
    fi
fi

echo ""
echo "========================================"
echo "常用命令:"
echo "  启动: ./start_daemon.sh"
echo "  停止: ./stop.sh"
echo "  查看日志: tail -f logs/proxy.log"
echo "========================================"
