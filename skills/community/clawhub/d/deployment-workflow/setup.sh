#!/bin/bash
# Agent工作流一键部署脚本（非root版）
# 使用: bash setup.sh

set -e

echo "========================================="
echo "  Agent工作流部署脚本"
echo "========================================="

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 获取用户目录
USER_HOME=$HOME
WORKSPACE_DIR="$USER_HOME/openclaw-workspace"

echo -e "${YELLOW}[1/6] 检查系统依赖...${NC}"

# 检查Node.js
if ! command -v node &> /dev/null; then
  echo -e "${RED}Node.js 未安装，请先安装 Node.js v18+${NC}"
  exit 1
fi

# 检查Python
if ! command -v python3 &> /dev/null; then
  echo -e "${RED}Python3 未安装，请先安装 Python 3.10+${NC}"
  exit 1
fi

echo -e "${GREEN}✓ 系统依赖检查通过${NC}"

echo -e "${YELLOW}[2/6] 安装OpenClaw...${NC}"
npm install -g openclaw

echo -e "${GREEN}✓ OpenClaw安装完成${NC}"

echo -e "${YELLOW}[3/6] 安装Python依赖...${NC}"
pip3 install --user playwright requests

echo -e "${GREEN}✓ Python依赖安装完成${NC}"

echo -e "${YELLOW}[4/6] 安装Playwright浏览器...${NC}"
playwright install chromium

echo -e "${GREEN}✓ Playwright安装完成${NC}"

echo -e "${YELLOW}[5/6] 初始化目录结构...${NC}"
mkdir -p "$WORKSPACE_DIR/memory"
mkdir -p "$WORKSPACE_DIR/scripts"
mkdir -p "$WORKSPACE_DIR/config"

echo -e "${GREEN}✓ 目录初始化完成${NC}"

echo -e "${YELLOW}[6/6] 配置Telegram Bot...${NC}"
echo -e "${YELLOW}请输入Telegram Bot Token:${NC}"
read -r BOT_TOKEN

if [ -n "$BOT_TOKEN" ]; then
  openclaw configure --section telegram --token "$BOT_TOKEN"
  echo -e "${GREEN}✓ Bot配置完成${NC}"
else
  echo -e "${YELLOW}跳过Bot配置${NC}"
fi

echo ""
echo "========================================="
echo -e "${GREEN}  部署完成！${NC}"
echo "========================================="
echo ""
echo "工作目录: $WORKSPACE_DIR"
echo ""
echo "后续步骤："
echo "1. 配置Telegram Bot并加入群组"
echo "2. 配置Playwright CDP连接"
echo "3. 添加定时任务"
echo "4. 验证部署"
echo ""