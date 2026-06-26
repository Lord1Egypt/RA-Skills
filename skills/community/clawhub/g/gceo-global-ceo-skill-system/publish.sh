#!/bin/bash
# GCCEO Publish Script
# Publishes GCCEO to GitHub for user: yjkj999999

set -e

echo "=========================================="
echo "  GCCEO v4.0.0 Publish Script"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# GitHub User
GH_USER="yjkj999999"
REPO_NAME="GCCEO-GlobalCEO-Skill-System"
REPO_URL="https://github.com/$GH_USER/$REPO_NAME"

echo -e "${GREEN}Target: $GH_USER/$REPO_NAME${NC}"
echo ""

# Check if we have gh CLI with auth
if gh auth status &>/dev/null; then
    echo -e "${BLUE}Using GitHub CLI (gh) for automated publish...${NC}"
    echo ""

    echo -e "${BLUE}Step 1: Creating GitHub repository...${NC}"
    if gh repo view "$GH_USER/$REPO_NAME" &>/dev/null; then
        echo -e "${YELLOW}Repository already exists.${NC}"
    else
        gh repo create "$REPO_NAME" \
            --public \
            --description "Global CEO Mastery System | 全球CEO帝王学技能体系" \
            --remote=origin \
            --push 2>/dev/null || {
            echo -e "${YELLOW}Could not auto-create. Please create manually at:${NC}"
            echo "$REPO_URL"
        }
    fi

    echo -e "${BLUE}Step 2: Creating GitHub Release v4.0.0...${NC}"
    gh release create v4.0.0 \
        --repo "$GH_USER/$REPO_NAME" \
        --title "GCCEO v4.0.0" \
        --notes "Global CEO Mastery System | 全球CEO帝王学技能体系 | 111 skills" \
        2>/dev/null || echo "Release creation skipped"
else
    echo -e "${YELLOW}GitHub CLI not authenticated.${NC}"
    echo "Please follow the manual steps in PUBLISH_GUIDE.md"
    echo ""
    echo -e "${BLUE}Quick manual steps:${NC}"
    echo "1. Create repo at: https://github.com/new"
    echo "2. Repository name: $REPO_NAME"
    echo "3. Set remote: git remote add origin $REPO_URL.git"
    echo "4. Push: git push -u origin main"
    echo "5. Create release at: $REPO_URL/releases/new"
fi

echo ""
echo -e "${GREEN}=========================================="
echo "  Target Repository"
echo "=========================================="
echo "GitHub: $REPO_URL"
echo "ClawHub: https://clawhub.ai/GCCEO (publish after GitHub)"
echo "SkillHub: https://skillhub.ai/GCCEO (publish after GitHub)"
echo -e "${NC}"
