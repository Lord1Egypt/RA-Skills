#!/bin/bash
#
# Cognitive Brain 一键安装脚本
# 用法: curl -fsSL https://.../install.sh | bash
# 或者: ./install.sh
#

set -e

SKILL_DIR="${HOME}/.openclaw/workspace/skills/cognitive-brain"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}🧠 Cognitive Brain 安装程序${NC}"
echo "=================================================="
echo ""

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ Node.js 未安装${NC}"
    echo "   请先安装 Node.js: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo -e "${RED}❌ Node.js 版本过低 (需要 >= 18)${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Node.js $(node -v)${NC}"

# 方式1: 使用 clawhub
if command -v clawhub &> /dev/null; then
    echo ""
    echo -e "${BLUE}使用 ClawHub 安装...${NC}"
    clawhub install cognitive-brain
else
    # 方式2: 手动克隆
    echo ""
    echo -e "${YELLOW}未找到 clawhub，使用手动安装...${NC}"
    
    mkdir -p "${HOME}/.openclaw/workspace/skills"
    
    if [ -d "$SKILL_DIR" ]; then
        echo -e "${YELLOW}⚠️  cognitive-brain 已存在，更新...${NC}"
        cd "$SKILL_DIR"
        git pull 2>/dev/null || true
    else
        echo "克隆仓库..."
        git clone https://github.com/your-repo/cognitive-brain.git "$SKILL_DIR" 2>/dev/null || {
            echo -e "${RED}无法克隆仓库，请手动下载${NC}"
            exit 1
        }
    fi
fi

cd "$SKILL_DIR"

# 安装 npm 依赖（会触发 postinstall）
echo ""
echo -e "${BLUE}安装依赖并初始化...${NC}"
npm install --include=dev 2>&1 | tail -20

# 检查安装结果
echo ""
if [ -f "config.json" ] && [ -d "node_modules" ]; then
    echo "=================================================="
    echo ""
    echo -e "${GREEN}✨ Cognitive Brain 安装完成！${NC}"
    echo ""
    echo "使用方法:"
    echo "  npm run health     # 健康检查"
    echo "  npm run encode     # 编码记忆"
    echo "  npm run recall     # 检索记忆"
    echo ""
else
    echo -e "${YELLOW}⚠️  安装可能未完成，请检查错误信息${NC}"
    echo "可以尝试运行: npm run setup"
fi
