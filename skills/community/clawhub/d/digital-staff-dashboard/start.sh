#!/bin/bash
# Agent Dashboard v2 - Startup Script
# 自动安装依赖并启动服务器

set -e  # 遇到错误立即退出

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  Agent Dashboard v2.0"
echo "========================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${BLUE}🐍 Python version: $PYTHON_VERSION${NC}"

# 检查 pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 not found. Please install pip${NC}"
    exit 1
fi

# 检查 requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ requirements.txt not found!${NC}"
    exit 1
fi

# 安装/更新依赖
echo -e "${YELLOW}📦 Checking and installing dependencies...${NC}"

# 尝试安装依赖
INSTALL_CMD="pip3 install -q -r requirements.txt"

# 检测是否需要 --break-system-packages (Python 3.11+)
if pip3 install --help 2>/dev/null | grep -q "break-system-packages"; then
    INSTALL_CMD="pip3 install -q -r requirements.txt --break-system-packages"
fi

# 执行安装
if $INSTALL_CMD 2>&1 | grep -q "Successfully installed\|Requirement already satisfied"; then
    echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
else
    # 静默安装，检查是否成功
    $INSTALL_CMD > /tmp/pip_install.log 2>&1
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Dependencies are up to date${NC}"
    else
        echo -e "${YELLOW}⚠️  Some dependencies may need manual installation${NC}"
        echo "Check /tmp/pip_install.log for details"
    fi
fi

# 创建必要的目录
echo -e "${BLUE}📁 Creating necessary directories...${NC}"
mkdir -p data/avatars
mkdir -p data/logs
echo -e "${GREEN}✅ Directories ready${NC}"

# 检查端口是否被占用
PORT="${DASHBOARD_PORT:-5177}"
if lsof -i :$PORT > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Port $PORT is already in use. Trying to find an available port...${NC}"
    # 尝试找到可用端口
    for try_port in 5178 5179 5180 5181 5182; do
        if ! lsof -i :$try_port > /dev/null 2>&1; then
            PORT=$try_port
            echo -e "${GREEN}✅ Found available port: $PORT${NC}"
            break
        fi
    done
fi

echo ""
echo "🚀 Starting Agent Dashboard..."
echo -e "${BLUE}🌐 Dashboard will be available at: http://localhost:$PORT${NC}"
echo ""

# 设置环境变量
export DASHBOARD_PORT=$PORT

# 启动服务器
python3 dashboard_server.py
