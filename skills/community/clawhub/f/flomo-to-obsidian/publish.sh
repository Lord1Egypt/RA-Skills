#!/bin/bash
# 发布到 ClawHub 的快捷脚本

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}发布 flomo-to-obsidian 到 ClawHub${NC}"
echo -e "${GREEN}==========================================${NC}"
echo ""

# 检查是否已登录
echo -e "${YELLOW}检查登录状态...${NC}"
if ! clawhub whoami &>/dev/null; then
    echo -e "${RED}❌ 未登录 ClawHub${NC}"
    echo ""
    echo -e "${YELLOW}请先登录：${NC}"
    echo "  clawhub login"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ 已登录${NC}"
echo ""

# 显示当前配置
echo -e "${YELLOW}📦 发布信息：${NC}"
echo "  Slug: flomo-to-obsidian"
echo "  Name: Flomo to Obsidian Sync Tool"
echo "  Version: 2.0.0"
echo "  Tags: latest"
echo ""

# 确认
read -p "确认发布？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${RED}取消发布${NC}"
    exit 0
fi

echo ""
echo -e "${YELLOW}🚀 开始发布...${NC}"
echo ""

# 执行发布
clawhub publish . \
  --slug flomo-to-obsidian \
  --name "Flomo to Obsidian Sync Tool" \
  --version 2.0.0 \
  --changelog "v2.0: Added safe mode with browser session login (no password storage), improved security, fixed HTML file detection, tested with 514 notes successfully. Features: automatic sync, incremental updates, attachment support, dual-link support, comprehensive documentation (7 detailed guides), two sync modes (safe mode for personal use, password mode for automation)." \
  --tags latest

# 检查结果
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}==========================================${NC}"
    echo -e "${GREEN}✅ 发布成功！${NC}"
    echo -e "${GREEN}==========================================${NC}"
    echo ""
    echo -e "${YELLOW}用户可以通过以下方式安装：${NC}"
    echo "  clawhub install flomo-to-obsidian"
    echo ""
    echo -e "${YELLOW}或在 OpenClaw 中直接说：${NC}"
    echo '  "帮我同步 flomo 到 Obsidian"'
    echo ""
    echo -e "${YELLOW}查看 skill：${NC}"
    echo "  https://clawhub.ai/skills/flomo-to-obsidian"
    echo ""
else
    echo ""
    echo -e "${RED}❌ 发布失败${NC}"
    echo "请检查错误信息并重试"
    exit 1
fi
