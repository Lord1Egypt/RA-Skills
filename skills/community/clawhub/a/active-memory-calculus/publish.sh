#!/bin/bash
# Active Memory for Calculus Teaching - 发布脚本
# 用于一键发布到 ClawHub

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Skill 信息
SKILL_NAME="Active Memory for Calculus Teaching"
SKILL_SLUG="active-memory-calculus"
VERSION="1.0.0"
CHANGELOG="Initial release: Active Memory and Dreaming System for calculus education"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Publishing ${SKILL_NAME}${NC}"
echo -e "${BLUE}  Version: ${VERSION}${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查 clawhub CLI
echo -e "${YELLOW}[1/6] Checking ClawHub CLI...${NC}"
if ! command -v clawhub &> /dev/null; then
    echo -e "${RED}Error: clawhub CLI not found${NC}"
    echo "Please install: npm install -g @clawhub/cli"
    exit 1
fi
echo -e "${GREEN}✓ ClawHub CLI found${NC}"

# 检查登录状态
echo -e "${YELLOW}[2/6] Checking authentication...${NC}"
if ! clawhub whoami &> /dev/null; then
    echo -e "${RED}Error: Not logged in to ClawHub${NC}"
    echo "Please run: clawhub login"
    exit 1
fi
USER=$(clawhub whoami)
echo -e "${GREEN}✓ Logged in as: ${USER}${NC}"

# 检查文件结构
echo -e "${YELLOW}[3/6] Checking skill structure...${NC}"
REQUIRED_FILES=("SKILL.md" "hermes.config.yaml" "_meta.json")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}Error: Required file $file not found${NC}"
        exit 1
    fi
done
echo -e "${GREEN}✓ All required files present${NC}"

# 本地测试
echo -e "${YELLOW}[4/6] Running local tests...${NC}"
if ! clawhub test . &> /dev/null; then
    echo -e "${RED}Error: Local test failed${NC}"
    echo "Please check SKILL.md format"
    exit 1
fi
echo -e "${GREEN}✓ Local tests passed${NC}"

# 检查远程状态
echo -e "${YELLOW}[5/6] Checking remote status...${NC}"
if clawhub inspect ${SKILL_SLUG} &> /dev/null; then
    echo -e "${YELLOW}⚠ Skill already exists, will update${NC}"
    EXISTING_VERSION=$(clawhub inspect ${SKILL_SLUG} --json | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
    echo -e "   Existing version: ${EXISTING_VERSION}"
    echo -e "   New version: ${VERSION}"
else
    echo -e "${GREEN}✓ New skill will be created${NC}"
fi

# 发布确认
echo ""
echo -e "${YELLOW}[6/6] Ready to publish${NC}"
echo "  Slug: ${SKILL_SLUG}"
echo "  Name: ${SKILL_NAME}"
echo "  Version: ${VERSION}"
echo "  Changelog: ${CHANGELOG}"
echo ""
read -p "Continue with publish? (y/N): " confirm
if [[ ! $confirm =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Publish cancelled${NC}"
    exit 0
fi

# 执行发布
echo ""
echo -e "${BLUE}Publishing to ClawHub...${NC}"
clawhub publish . \
  --slug ${SKILL_SLUG} \
  --name "${SKILL_NAME}" \
  --version ${VERSION} \
  --changelog "${CHANGELOG}"

# 验证发布
echo ""
echo -e "${YELLOW}Verifying publish...${NC}"
sleep 5  # 等待服务器处理

if clawhub inspect ${SKILL_SLUG} &> /dev/null; then
    echo -e "${GREEN}✓ Publish successful!${NC}"
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  Skill Published Successfully${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "  URL: https://clawhub.ai/skills/${SKILL_SLUG}"
    echo "  Author: https://clawhub.ai/${USER}"
    echo ""
    echo "  Install command:"
    echo "    clawhub install ${SKILL_SLUG}"
    echo ""
    echo "  Or:"
    echo "    openclaw skills add ${SKILL_SLUG}"
    echo ""
else
    echo -e "${YELLOW}⚠ Verification pending, please check manually:${NC}"
    echo "  https://clawhub.ai/skills/${SKILL_SLUG}"
fi
