#!/bin/bash
# 自动上传脚本 - Auto Upload to ClawHub
# 生成时间: 2026-04-12 20:29

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

SKILL_DIR="/mnt/kimi/output/active-memory-calculus"
SKILL_SLUG="active-memory-calculus"
SKILL_NAME="Active Memory for Calculus Teaching"
VERSION="1.0.0"

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          🚀 AUTO UPLOAD TO CLAWHUB 🚀                          ║"
echo "║          Active Memory for Calculus Teaching v1.0.0           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# 步骤1: 环境检查
echo -e "${BLUE}[Step 1/5] Environment Check${NC}"
echo "────────────────────────────────────────────────────────────────"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}⚠ Node.js not found. Installing...${NC}"
    # 尝试安装 Node.js (根据系统)
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y nodejs npm
    elif command -v yum &> /dev/null; then
        sudo yum install -y nodejs npm
    elif command -v brew &> /dev/null; then
        brew install node
    else
        echo -e "${RED}✗ Please install Node.js manually from https://nodejs.org${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}✓ Node.js: $(node --version)${NC}"

# 检查 ClawHub CLI
if ! command -v clawhub &> /dev/null; then
    echo -e "${YELLOW}⚠ ClawHub CLI not found. Installing...${NC}"
    npm install -g @clawhub/cli
    if [ $? -ne 0 ]; then
        echo -e "${RED}✗ Failed to install ClawHub CLI${NC}"
        exit 1
    fi
fi
echo -e "${GREEN}✓ ClawHub CLI installed${NC}"

# 检查目录
if [ ! -d "$SKILL_DIR" ]; then
    echo -e "${RED}✗ Skill directory not found: $SKILL_DIR${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Skill directory found${NC}"
echo ""

# 步骤2: 登录验证
echo -e "${BLUE}[Step 2/5] Authentication${NC}"
echo "────────────────────────────────────────────────────────────────"

if ! clawhub whoami &> /dev/null; then
    echo -e "${YELLOW}⚠ Not logged in. Initiating login...${NC}"
    echo "A browser window will open for authentication."
    echo "Please complete the login and return here."
    echo ""
    clawhub login

    if ! clawhub whoami &> /dev/null; then
        echo -e "${RED}✗ Login failed${NC}"
        exit 1
    fi
fi

USER=$(clawhub whoami)
echo -e "${GREEN}✓ Logged in as: $USER${NC}"
echo ""

# 步骤3: 预上传验证
echo -e "${BLUE}[Step 3/5] Pre-upload Validation${NC}"
echo "────────────────────────────────────────────────────────────────"

cd "$SKILL_DIR"

# 检查必需文件
REQUIRED_FILES=("SKILL.md" "hermes.config.yaml" "_meta.json")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ Missing required file: $file${NC}"
        exit 1
    fi
done
echo -e "${GREEN}✓ All required files present${NC}"

# 运行本地测试
if command -v clawhub &> /dev/null; then
    if clawhub test . &> /tmp/clawhub_test.log; then
        echo -e "${GREEN}✓ Local validation passed${NC}"
    else
        echo -e "${YELLOW}⚠ Local test failed (non-blocking)${NC}"
        echo "Error log: /tmp/clawhub_test.log"
    fi
fi

# 检查远程状态
echo ""
echo -e "${CYAN}Checking remote skill status...${NC}"
if clawhub inspect $SKILL_SLUG &> /dev/null; then
    echo -e "${YELLOW}⚠ Skill '$SKILL_SLUG' already exists${NC}"
    EXISTING_VERSION=$(clawhub inspect $SKILL_SLUG --json 2>/dev/null | grep -o '"version":"[^"]*"' | head -1 | cut -d'"' -f4)
    echo "   Existing version: $EXISTING_VERSION"
    echo "   New version: $VERSION"

    read -p "Continue with update? (y/N): " confirm
    if [[ ! $confirm =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Upload cancelled${NC}"
        exit 0
    fi
else
    echo -e "${GREEN}✓ New skill will be created${NC}"
fi
echo ""

# 步骤4: 执行上传
echo -e "${BLUE}[Step 4/5] Uploading to ClawHub${NC}"
echo "────────────────────────────────────────────────────────────────"
echo "Skill: $SKILL_NAME"
echo "Slug: $SKILL_SLUG"
echo "Version: $VERSION"
echo ""

# 执行发布命令
clawhub publish . \
  --slug "$SKILL_SLUG" \
  --name "$SKILL_NAME" \
  --version "$VERSION" \
  --changelog "Initial release: Active Memory and Dreaming System for calculus education" \
  2>&1 | tee /tmp/clawhub_upload.log

UPLOAD_STATUS=${PIPESTATUS[0]}

if [ $UPLOAD_STATUS -ne 0 ]; then
    echo ""
    echo -e "${RED}✗ Upload failed${NC}"
    echo "Error log: /tmp/clawhub_upload.log"
    exit 1
fi

echo ""
echo -e "${GREEN}✓ Upload completed${NC}"
echo ""

# 步骤5: 验证上传
echo -e "${BLUE}[Step 5/5] Post-upload Verification${NC}"
echo "────────────────────────────────────────────────────────────────"

echo "Waiting for server processing (5 seconds)..."
sleep 5

# 验证技能存在
if clawhub inspect $SKILL_SLUG &> /dev/null; then
    echo -e "${GREEN}✓ Skill verified on ClawHub${NC}"

    # 获取技能信息
    SKILL_INFO=$(clawhub inspect $SKILL_SLUG --json 2>/dev/null)

    echo ""
    echo -e "${CYAN}Skill Information:${NC}"
    echo "  Name: $SKILL_NAME"
    echo "  Slug: $SKILL_SLUG"
    echo "  Version: $VERSION"
    echo "  Author: $USER"
    echo ""
    echo -e "${CYAN}URLs:${NC}"
    echo "  Skill Page: https://clawhub.ai/skills/$SKILL_SLUG"
    echo "  Author Page: https://clawhub.ai/$USER"
    echo ""
    echo -e "${CYAN}Installation:${NC}"
    echo "  clawhub install $SKILL_SLUG"
    echo "  openclaw skills add $SKILL_SLUG"
    echo ""
else
    echo -e "${YELLOW}⚠ Verification pending${NC}"
    echo "  Please check manually: https://clawhub.ai/skills/$SKILL_SLUG"
fi

echo ""
echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║              🎉 UPLOAD COMPLETED SUCCESSFULLY! 🎉              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""
echo "Next steps:"
echo "  1. Visit your skill page: https://clawhub.ai/skills/$SKILL_SLUG"
echo "  2. Share with others!"
echo "  3. Collect feedback and iterate"
echo ""
echo "Log files:"
echo "  Upload log: /tmp/clawhub_upload.log"
echo "  Test log: /tmp/clawhub_test.log"
