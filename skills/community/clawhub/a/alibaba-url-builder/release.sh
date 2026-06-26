#!/bin/bash
#
# alibaba-sourcing 发布脚本
# 自动完成 ClawHub 发布和 GitHub 仓库创建
#
# 使用方法:
#   ./release.sh
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目配置
SKILL_NAME="alibaba-sourcing"
VERSION="1.0.0"
DESCRIPTION="Build Alibaba.com URLs for agent navigation with traffic tracking (traffic_type=ags_llm)"
GITHUB_REPO="zhouzeyu/openclaw-skill-${SKILL_NAME}"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  ${SKILL_NAME} 发布脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查 ClawHub CLI
echo -e "${YELLOW}[1/6] 检查 ClawHub CLI...${NC}"
if command -v clawdhub &> /dev/null; then
    echo -e "${GREEN}✓ ClawHub CLI 已安装${NC}"
    clawdhub --cli-version
else
    echo -e "${RED}✗ ClawHub CLI 未安装${NC}"
    echo "请先安装："
    echo "  npm install -g clawdhub"
    echo "或"
    echo "  npx clawdhub@latest"
    exit 1
fi
echo ""

# 检查登录状态
echo -e "${YELLOW}[2/6] 检查 ClawHub 登录状态...${NC}"
if clawdhub whoami &> /dev/null; then
    echo -e "${GREEN}✓ 已登录到 ClawHub${NC}"
    clawdhub whoami
else
    echo -e "${YELLOW}! 未登录，正在启动登录流程...${NC}"
    clawdhub login
fi
echo ""

# 重新打包 skill
echo -e "${YELLOW}[3/6] 重新打包 skill...${NC}"
cd "$SKILL_DIR"
if [ -f "alibaba-sourcing.skill" ]; then
    rm alibaba-sourcing.skill
    echo "  删除旧的 .skill 文件"
fi
python3 scripts/package_skill.py .
mv .skill alibaba-sourcing.skill
echo -e "${GREEN}✓ 打包完成：alibaba-sourcing.skill${NC}"
echo ""

# 发布到 ClawHub
echo -e "${YELLOW}[4/6] 发布到 ClawHub...${NC}"
echo "  版本：${VERSION}"
echo "  描述：${DESCRIPTION}"
echo ""
read -p "确认发布？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}发布已取消${NC}"
    exit 0
fi

clawdhub publish . --version "$VERSION" --tags latest --changelog "$DESCRIPTION"
echo -e "${GREEN}✓ 发布成功！${NC}"
echo ""

# 创建/更新 GitHub 仓库
echo -e "${YELLOW}[5/6] 配置 GitHub 仓库...${NC}"
if [ -d ".git" ]; then
    echo -e "${GREEN}✓ Git 仓库已初始化${NC}"
    read -p "是否推送到 GitHub？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if git remote -v | grep -q origin; then
            echo "  远程仓库已配置"
            git remote -v | grep origin
        else
            echo "  请设置远程仓库 URL:"
            read -p "GitHub Repo URL: " repo_url
            git remote add origin "$repo_url"
        fi
        
        echo "  添加所有文件..."
        git add .
        
        echo "  创建提交..."
        git commit -m "Release v${VERSION}

${DESCRIPTION}

Features:
- 10+ URL patterns for Alibaba.com navigation
- Automatic traffic tracking (traffic_type=ags_llm)
- Python CLI helper script
- Complete documentation
- MIT-0 license" || echo "  没有需要提交的更改"
        
        echo "  推送到 GitHub..."
        git branch -M main 2>/dev/null || true
        git push -u origin main
        echo -e "${GREEN}✓ 已推送到 GitHub${NC}"
    fi
else
    echo -e "${YELLOW}! 未初始化 Git 仓库${NC}"
    read -p "是否初始化并创建 GitHub 仓库？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git init
        git add .
        git commit -m "Initial release: ${SKILL_NAME} v${VERSION}"
        git branch -M main
        
        echo "  请在 GitHub 上创建仓库后输入 URL:"
        read -p "GitHub Repo URL: " repo_url
        git remote add origin "$repo_url"
        git push -u origin main
        echo -e "${GREEN}✓ GitHub 仓库已创建${NC}"
    fi
fi
echo ""

# 显示后续步骤
echo -e "${YELLOW}[6/6] 后续步骤${NC}"
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  发布完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "📦 ClawHub 页面:"
echo "   https://clawhub.ai/skills/${SKILL_NAME}"
echo ""
echo "🔗 GitHub 仓库:"
echo "   https://github.com/${GITHUB_REPO}"
echo ""
echo "📢 宣传渠道:"
echo "   1. Discord: https://discord.com/invite/clawd"
echo "   2. Twitter: 使用 #OpenClaw #AI #Agent 标签"
echo "   3. LinkedIn: 分享专业文章"
echo "   4. 微信/朋友圈: 中文社区分享"
echo ""
echo "📋 查看 PROMOTION.md 获取完整宣传文案"
echo ""
echo "🎉 恭喜！"
echo ""
