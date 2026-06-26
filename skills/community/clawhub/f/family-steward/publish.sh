#!/usr/bin/env bash
#
# ClawHub Skill Publishing Script
# Automates the publishing process for Family Steward skill
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Family Steward - ClawHub Skill Publisher${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Parse arguments
VERSION=${1:-$(jq -r '.version' skill.json)}
CHANGELOG=${2:-"See CHANGELOG.md for details"}

echo "📦 Publishing Configuration:"
echo "   Slug:      family-steward"
echo "   Version:   $VERSION"
echo "   Changelog: $CHANGELOG"
echo ""

# Step 1: Validate
echo -e "${YELLOW}Step 1/5:${NC} Validating configuration..."
if [ -f "validate.sh" ]; then
    chmod +x validate.sh
    if ! ./validate.sh; then
        echo -e "${RED}❌ Validation failed. Fix errors and try again.${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠ validate.sh not found, skipping validation${NC}"
fi
echo ""

# Step 2: Check authentication
echo -e "${YELLOW}Step 2/5:${NC} Checking ClawHub authentication..."
if ! clawhub whoami &>/dev/null; then
    echo -e "${RED}❌ Not logged in to ClawHub${NC}"
    echo ""
    echo "Please login first:"
    echo "  clawhub login"
    echo ""
    exit 1
fi

USER=$(clawhub whoami 2>/dev/null | grep -oP 'ZhenStaff' || echo "unknown")
echo -e "   ${GREEN}✓${NC} Logged in as: $USER"
echo ""

# Step 3: Pre-publish checks
echo -e "${YELLOW}Step 3/5:${NC} Pre-publish checks..."

# Check if parent project exists
if [ ! -d "../src" ]; then
    echo -e "${RED}✗${NC} Parent project src/ directory not found"
    exit 1
fi
echo -e "   ${GREEN}✓${NC} Parent project exists"

# Check if skill already exists
if clawhub inspect family-steward &>/dev/null; then
    echo -e "   ${GREEN}✓${NC} Skill exists, will update"
else
    echo -e "   ${BLUE}ℹ${NC} New skill, will create"
fi
echo ""

# Step 4: Publish
echo -e "${YELLOW}Step 4/5:${NC} Publishing to ClawHub..."
echo ""

PUBLISH_CMD="clawhub publish $SCRIPT_DIR --slug family-steward --version $VERSION --changelog \"$CHANGELOG\""

echo "   Command: $PUBLISH_CMD"
echo ""

if eval "$PUBLISH_CMD"; then
    echo ""
    echo -e "${GREEN}✅ Successfully published to ClawHub!${NC}"
else
    echo ""
    echo -e "${RED}❌ Publishing failed${NC}"
    exit 1
fi
echo ""

# Step 5: Verify
echo -e "${YELLOW}Step 5/5:${NC} Verifying publication..."

sleep 2  # Wait for ClawHub to process

if clawhub inspect family-steward &>/dev/null; then
    echo -e "   ${GREEN}✓${NC} Skill is visible on ClawHub"

    # Show skill info
    echo ""
    echo "📊 Skill Information:"
    clawhub inspect family-steward 2>/dev/null | head -10
else
    echo -e "   ${YELLOW}⚠${NC} Skill is under security review"
    echo "   This is normal for new uploads, wait 5-10 minutes"
fi
echo ""

# Success summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎉 Publication Complete!${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "📍 Skill URL:"
echo "   https://clawhub.ai/ZhenStaff/family-steward"
echo ""
echo "💻 Installation:"
echo "   clawhub install family-steward"
echo ""
echo "🔗 Links:"
echo "   GitHub:  https://github.com/ZhenRobotics/openclaw-family-steward"
echo "   NPM:     https://www.npmjs.com/package/openclaw-family-steward"
echo "   ClawHub: https://clawhub.ai/ZhenStaff/family-steward"
echo ""
echo "📝 Next Steps:"
echo "   1. Wait for security scan to complete (5-10 minutes)"
echo "   2. Verify skill is accessible: clawhub inspect family-steward"
echo "   3. Test installation: clawhub install family-steward"
echo "   4. Share on social media and announce release"
echo ""
