#!/bin/bash
# 后台守护进程启动脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PID_FILE="$SCRIPT_DIR/proxy.pid"
LOG_FILE="$SCRIPT_DIR/logs/proxy.log"

# 检查是否已在运行
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "服务已在运行 (PID: $PID)"
        echo "访问: http://localhost:8080"
        exit 0
    else
        rm -f "$PID_FILE"
    fi
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate

# 安装依赖
echo "检查依赖..."
pip install -q fastapi uvicorn httpx sqlalchemy aiosqlite pydantic python-dotenv jinja2 python-multipart 2>/dev/null

# 创建目录
mkdir -p data logs

# 初始化数据库（如果不存在）
if [ ! -f "data/bailian_proxy.db" ]; then
    echo "初始化数据库..."
    python3 scripts/init_db.py 2>/dev/null
fi

echo "启动阿里百炼用量统计代理服务..."
echo "日志: $LOG_FILE"

# 后台启动
nohup python3 -m app.main >> "$LOG_FILE" 2>&1 &
PID=$!
echo $PID > "$PID_FILE"

sleep 2

# 检查启动状态
if ps -p "$PID" > /dev/null 2>&1; then
    echo "✅ 服务启动成功"
    echo "   PID: $PID"
    echo "   API: http://localhost:8080"
    echo "   管理后台: http://localhost:8081"
    echo ""
    echo "查看日志: tail -f logs/proxy.log"
    echo "停止服务: ./stop.sh"
else
    echo "❌ 服务启动失败，查看日志: $LOG_FILE"
    rm -f "$PID_FILE"
    exit 1
fi
