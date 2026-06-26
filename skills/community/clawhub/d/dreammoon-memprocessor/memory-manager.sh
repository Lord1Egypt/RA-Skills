#!/bin/bash
# DreamMoon Memory Processor 管理脚本

APP_DIR="/root/DreamMoon/config/dreammoon-memory-python"
LOG_FILE="/tmp/memory-processor.log"
PID_FILE="/tmp/memory-processor.pid"
PORT=9090

cd "$APP_DIR"

# 激活conda环境
export PATH="/root/miniconda3/bin:$PATH"
source /root/miniconda3/etc/profile.d/conda.sh
conda activate dreammoon

case "$1" in
    start)
        if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
            echo "⚠️ MemoryProcessor 已在运行 (PID: $(cat $PID_FILE))"
            exit 1
        fi
        
        echo "🚀 启动 DreamMoon Memory Processor..."
        nohup python3 start-simple.py > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        
        sleep 3
        
        if curl -s http://localhost:$PORT/health > /dev/null; then
            echo "✅ MemoryProcessor 启动成功！"
            echo "   地址: http://localhost:$PORT"
            echo "   文档: http://localhost:$PORT/docs"
            echo "   PID: $(cat $PID_FILE)"
        else
            echo "❌ 启动失败，查看日志: $LOG_FILE"
            exit 1
        fi
        ;;
        
    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                echo "🛑 停止 MemoryProcessor (PID: $PID)..."
                kill "$PID"
                rm -f "$PID_FILE"
                echo "✅ 已停止"
            else
                echo "⚠️ 进程不存在"
                rm -f "$PID_FILE"
            fi
        else
            echo "⚠️ 未找到PID文件"
        fi
        ;;
        
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
        
    status)
        echo "📊 DreamMoon Memory Processor 状态"
        echo "================================"
        echo ""
        
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                echo "✅ 服务运行中 (PID: $PID)"
            else
                echo "❌ 进程不存在但PID文件残留"
            fi
        else
            echo "❌ 服务未运行"
        fi
        
        echo ""
        echo "端口 $PORT:"
        if netstat -tlnp 2>/dev/null | grep -q ":$PORT"; then
            echo "  ✅ 监听中"
        else
            echo "  ❌ 未监听"
        fi
        
        echo ""
        echo "健康检查:"
        if curl -s http://localhost:$PORT/health > /dev/null; then
            curl -s http://localhost:$PORT/health | jq . 2>/dev/null || curl -s http://localhost:$PORT/health
        else
            echo "  ❌ 未响应"
        fi
        
        echo ""
        echo "统计信息:"
        if curl -s http://localhost:$PORT/api/v1/stats > /dev/null; then
            curl -s http://localhost:$PORT/api/v1/stats | jq . 2>/dev/null || curl -s http://localhost:$PORT/api/v1/stats
        fi
        
        echo ""
        echo "日志文件: $LOG_FILE"
        echo "最后10行:"
        tail -n 10 "$LOG_FILE" 2>/dev/null || echo "  无日志"
        ;;
        
    logs)
        tail -f "$LOG_FILE"
        ;;
        
    test)
        echo "🧪 测试 Memory Processor API..."
        echo ""
        
        echo "1. 健康检查:"
        curl -s http://localhost:$PORT/health | jq . 2>/dev/null || curl -s http://localhost:$PORT/health
        
        echo ""
        echo "2. 统计信息:"
        curl -s http://localhost:$PORT/api/v1/stats | jq . 2>/dev/null || curl -s http://localhost:$PORT/api/v1/stats
        
        echo ""
        echo "✅ 测试完成"
        ;;
        
    *)
        echo "DreamMoon Memory Processor 管理脚本"
        echo ""
        echo "用法: $0 {start|stop|restart|status|logs|test}"
        echo ""
        echo "命令:"
        echo "  start   - 启动服务"
        echo "  stop    - 停止服务"
        echo "  restart - 重启服务"
        echo "  status  - 查看状态"
        echo "  logs    - 查看实时日志"
        echo "  test    - 测试API"
        ;;
esac
