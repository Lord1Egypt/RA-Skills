#!/bin/bash

set -e

echo "=========================================="
echo "  AI资讯网站生成器 - 一键启动脚本"
echo "=========================================="
echo ""

PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

echo "项目目录: $PROJECT_DIR"
echo ""

# 检查 Docker
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    echo "✅ 检测到 Docker 和 Docker Compose"
    echo ""
    read -p "是否使用 Docker 模式启动? (y/n): " use_docker
    
    if [ "$use_docker" = "y" ]; then
        echo ""
        echo "🚀 启动 Docker 容器..."
        cd "$PROJECT_DIR"
        docker-compose up -d --build
        echo ""
        echo "✅ Docker 容器启动成功！"
        echo ""
        echo "访问地址："
        echo "  前端: http://localhost:3000"
        echo "  后端: http://localhost:8000"
        echo "  API文档: http://localhost:8000/docs"
        echo ""
        echo "查看日志: docker-compose logs -f"
        echo "停止服务: docker-compose down"
        exit 0
    fi
else
    echo "⚠️  未检测到 Docker，将使用本地模式启动"
fi

echo ""
echo "🚀 本地模式启动..."
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    exit 1
fi

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js"
    exit 1
fi

echo "✅ 环境检查通过"
echo ""

# 创建虚拟环境（后端）
cd "$PROJECT_DIR/backend"
if [ ! -d "venv" ]; then
    echo "创建 Python 虚拟环境..."
    python3 -m venv venv
fi

echo "激活虚拟环境并安装依赖..."
source venv/bin/activate
pip install -q -r requirements.txt

# 启动后端（后台）
echo "启动后端服务 (端口 8000)..."
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "后端 PID: $BACKEND_PID"

# 启动前端
cd "$PROJECT_DIR/frontend"
if [ ! -d "node_modules" ]; then
    echo "安装前端依赖..."
    npm install
fi

echo "启动前端服务 (端口 3000)..."
npm run dev &
FRONTEND_PID=$!

# 保存 PID 到文件
echo "$BACKEND_PID" > "$PROJECT_DIR/backend.pid"
echo "$FRONTEND_PID" > "$PROJECT_DIR/frontend.pid"

echo ""
echo "=========================================="
echo "  ✅ 所有服务启动成功！"
echo "=========================================="
echo ""
echo "访问地址："
echo "  前端: http://localhost:3000"
echo "  后端: http://localhost:8000"
echo "  API文档: http://localhost:8000/docs"
echo ""
echo "停止服务:"
echo "  cd $PROJECT_DIR && kill \$(cat backend.pid) \$(cat frontend.pid)"
echo ""
echo "查看日志:"
echo "  后端: tail -f $PROJECT_DIR/backend/backend.log"
