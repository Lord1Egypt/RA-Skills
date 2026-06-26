#!/bin/bash

# Double Search Skill 一键安装和配置脚本

set -e

echo "=========================================="
echo "Double Search Skill 安装脚本"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 获取脚本目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "📍 当前目录: $SCRIPT_DIR"
echo ""

# 1. 检查Python版本
echo "📦 检查Python版本..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误: Python3未安装${NC}"
    echo "请先安装Python 3.8或更高版本"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✅ Python版本: $PYTHON_VERSION${NC}"
echo ""

# 2. 检查Python依赖
echo "📋 检查Python依赖..."

if python3 -c "import aiohttp" 2>/dev/null; then
    echo -e "${GREEN}✅ aiohttp 已安装${NC}"
else
    echo -e "${YELLOW}⚠️  aiohttp 未安装，正在安装...${NC}"
    pip3 install aiohttp python-dotenv --quiet
    echo -e "${GREEN}✅ aiohttp 安装完成${NC}"
fi

if python3 -c "import dotenv" 2>/dev/null; then
    echo -e "${GREEN}✅ python-dotenv 已安装${NC}"
else
    echo -e "${YELLOW}⚠️  python-dotenv 未安装，正在安装...${NC}"
    pip3 install python-dotenv --quiet
    echo -e "${GREEN}✅ python-dotenv 安装完成${NC}"
fi

echo ""

# 3. 检查API Keys
echo "🔑 检查API Keys配置..."

TAVILY_KEY="${TAVILY_API_KEY:-}"
KIMI_KEY="${KIMI_API_KEY:-}"

if [ -n "$TAVILY_KEY" ]; then
    echo -e "${GREEN}✅ TAVILY_API_KEY 已设置${NC}"
    echo "   Key前缀: ${TAVILY_KEY:0:10}..."
else
    echo -e "${RED}❌ TAVILY_API_KEY 未设置${NC}"
    echo "   请设置TAVILY_API_KEY环境变量或创建.env文件"
fi

if [ -n "$KIMI_KEY" ]; then
    echo -e "${GREEN}✅ KIMI_API_KEY 已设置${NC}"
    echo "   Key前缀: ${KIMI_KEY:0:10}..."
else
    echo -e "${YELLOW}⚠️  KIMI_API_KEY 未设置（可选）${NC}"
    echo "   只使用Tavily搜索"
fi

echo ""

# 4. 创建.env文件（如果不存在）
if [ ! -f "$SCRIPT_DIR/.env" ]; then
    echo "📝 创建.env配置文件..."
    cat > "$SCRIPT_DIR/.env" << EOF
# Double Search Skill 配置文件
# 请在此处填入您的API Keys

# Tavily Search API Key (必需)
# 获取地址: https://app.tavily.com/
TAVILY_API_KEY=

# Kimi Search API Key (可选)
# 获取地址: https://api.moonshot.cn/
KIMI_API_KEY=
EOF
    echo -e "${GREEN}✅ .env文件创建成功${NC}"
    echo -e "${YELLOW}⚠️  请编辑.env文件，填入您的API Keys${NC}"
else
    echo -e "${GREEN}✅ .env文件已存在${NC}"
fi

echo ""

# 5. 测试搜索功能
echo "🧪 测试搜索功能..."
echo ""

python3 "$SCRIPT_DIR/__init__.py"

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo -e "${GREEN}✅ 安装和测试完成！${NC}"
    echo "=========================================="
    echo ""
    echo "💡 使用方法:"
    echo ""
    echo "1. 在Python代码中导入:"
    echo "   from double_search import DoubleSearcher"
    echo ""
    echo "2. 创建搜索器实例:"
    echo "   searcher = DoubleSearcher()"
    echo ""
    echo "3. 执行搜索:"
    echo "   results = await searcher.search('您的搜索查询')"
    echo ""
    echo "📖 详细文档: SKILL.md"
    echo ""
else
    echo ""
    echo "=========================================="
    echo -e "${RED}❌ 测试失败${NC}"
    echo "=========================================="
    echo ""
    echo "💡 解决方案:"
    echo ""
    echo "1. 检查API Keys是否正确设置"
    echo "2. 检查Python依赖是否安装成功"
    echo "3. 查看错误信息并修复"
    echo ""
    exit 1
fi

echo ""
echo "✨ Double Search Skill 已就绪！"
echo ""
