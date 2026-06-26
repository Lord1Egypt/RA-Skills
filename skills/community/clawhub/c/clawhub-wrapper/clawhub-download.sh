#!/bin/bash

# ClawHub Skill Download Tool
# Usage: clawhub-download.sh <slug|url>
# Downloads and installs a skill from ClawHub

set -e

API_URL="https://wry-manatee-359.convex.site/api/v1"
SKILLS_DIR="$HOME/.agents/skills/clawhub-skills"
TEMP_DIR="/tmp/clawhub-download-$$"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Parse input - can be slug or full URL
input="$1"

if [ -z "$input" ]; then
    echo -e "${RED}Error: No skill specified.${NC}"
    echo "Usage: clawhub-download.sh <slug|url>"
    echo ""
    echo "Examples:"
    echo "  clawhub-download.sh github"
    echo "  clawhub-download.sh https://clawhub.ai/steipete/github"
    exit 1
fi

# Extract slug from URL or use as-is
if [[ "$input" == https://clawhub.ai/* ]]; then
    # Extract slug from URL (format: https://clawhub.ai/owner/slug)
    slug=$(echo "$input" | sed 's|https://clawhub.ai/[^/]*/||')
else
    slug="$input"
fi

echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  ClawHub Skill Downloader${NC}"
echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}Skill:${NC} $slug"
echo -e "${BLUE}Source:${NC} https://clawhub.ai/$slug"
echo ""

# Check dependencies
if ! command -v curl &> /dev/null; then
    echo -e "${RED}Error: curl is required but not installed.${NC}"
    exit 1
fi

if ! command -v unzip &> /dev/null; then
    echo -e "${RED}Error: unzip is required but not installed.${NC}"
    exit 1
fi

# Create temp directory
mkdir -p "$TEMP_DIR"

# Cleanup on exit
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# Download skill package
echo -e "${YELLOW}Downloading skill package...${NC}"
download_url="$API_URL/download?slug=$slug"

http_code=$(curl -s -w "%{http_code}" -o "$TEMP_DIR/skill.zip" "$download_url")

if [ "$http_code" != "200" ]; then
    echo -e "${RED}Error: Failed to download skill (HTTP $http_code)${NC}"
    echo -e "${RED}URL: $download_url${NC}"
    exit 1
fi

# Check if it's a valid zip file
if ! unzip -t "$TEMP_DIR/skill.zip" &> /dev/null; then
    echo -e "${RED}Error: Downloaded file is not a valid zip archive.${NC}"
    exit 1
fi

# Extract skill package
echo -e "${YELLOW}Extracting skill package...${NC}"
unzip -o "$TEMP_DIR/skill.zip" -d "$TEMP_DIR/extracted" &> /dev/null

# Check for SKILL.md
if [ ! -f "$TEMP_DIR/extracted/SKILL.md" ]; then
    echo -e "${RED}Error: Downloaded package does not contain SKILL.md${NC}"
    exit 1
fi

# Create skill directory
skill_dir="$SKILLS_DIR/$slug"
mkdir -p "$skill_dir"

# Copy files to skill directory
echo -e "${YELLOW}Installing skill to $skill_dir...${NC}"
cp -r "$TEMP_DIR/extracted/"* "$skill_dir/"

# Display skill info
echo ""
echo -e "${GREEN}✓ Skill installed successfully!${NC}"
echo ""
echo -e "${CYAN}────────────────────────────────────────────────────────────────${NC}"

# Show skill details
if [ -f "$skill_dir/SKILL.md" ]; then
    echo -e "${BLUE}Skill Description:${NC}"
    echo ""
    # Extract name and description from SKILL.md
    skill_name=$(grep -m1 "^name:" "$skill_dir/SKILL.md" | sed 's/name: *//' | tr -d '"')
    skill_desc=$(grep -m1 "^description:" "$skill_dir/SKILL.md" | sed 's/description: *//' | tr -d '"')
    
    if [ -n "$skill_name" ]; then
        echo -e "  ${GREEN}Name:${NC} $skill_name"
    fi
    if [ -n "$skill_desc" ]; then
        echo -e "  ${GREEN}Description:${NC} $skill_desc"
    fi
    echo ""
fi

# Show _meta.json info if exists
if [ -f "$skill_dir/_meta.json" ]; then
    version=$(jq -r '.version // "N/A"' "$skill_dir/_meta.json")
    published=$(jq -r '.publishedAt // "N/A"' "$skill_dir/_meta.json")
    
    echo -e "  ${GREEN}Version:${NC} $version"
    if [ "$published" != "null" ] && [ "$published" != "N/A" ]; then
        # Convert timestamp to readable date
        if [[ "$published" =~ ^[0-9]+$ ]]; then
            pub_date=$(date -d "@$((published/1000))" "+%Y-%m-%d" 2>/dev/null || echo "N/A")
            echo -e "  ${GREEN}Published:${NC} $pub_date"
        fi
    fi
fi

echo -e "${CYAN}────────────────────────────────────────────────────────────────${NC}"
echo ""
echo -e "${YELLOW}Skill files:${NC}"
ls -la "$skill_dir"
echo ""
echo -e "${GREEN}The skill is now available for use!${NC}"
echo -e "Restart your agent to load the new skill, or it will be loaded on next session."