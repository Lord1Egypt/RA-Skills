#!/bin/bash

# ClawHub Install Script
# Downloads and installs skills from ClawHub, bypassing rate limits

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Function to install a single skill
install_skill() {
    local skill_name="$1"

    echo -e "${YELLOW}Installing skill: ${skill_name}${NC}"

    # Step 1: Get workspace directory path
    echo "Getting workspace directory..."
    workspace_path=$(openclaw config get agents.defaults.workspace 2>/dev/null)

    if [ -z "$workspace_path" ]; then
        echo -e "${RED}Error: Could not get workspace path. Make sure OpenClaw is configured.${NC}"
        return 1
    fi

    echo "Workspace: $workspace_path"

    # Step 2: Download skill package
    echo "Downloading $skill_name from ClawHub..."
    download_url="https://wry-manatee-359.convex.site/api/v1/download?slug=${skill_name}"
    zip_path="/tmp/${skill_name}.zip"

    if curl -L -o "$zip_path" "$download_url" --fail --silent --show-error; then
        echo "Downloaded successfully"
    else
        echo -e "${RED}Error: Failed to download ${skill_name}. The skill may not exist or rate limited.${NC}"
        rm -f "$zip_path"
        return 1
    fi

    # Check if zip file is valid
    if [ ! -s "$zip_path" ]; then
        echo -e "${RED}Error: Downloaded file is empty${NC}"
        rm -f "$zip_path"
        return 1
    fi

    # Step 3: Extract to workspace/skills
    skills_dir="$workspace_path/skills"
    target_dir="$skills_dir/$skill_name"

    echo "Extracting to $target_dir..."

    # Create skills directory if not exists
    mkdir -p "$skills_dir"

    # Remove existing skill if it exists
    if [ -d "$target_dir" ]; then
        echo "Removing existing $skill_name..."
        rm -rf "$target_dir"
    fi

    # Create the skill directory
    mkdir -p "$target_dir"

    # Extract the zip
    if unzip -q "$zip_path" -d "$target_dir"; then
        echo -e "${GREEN}Successfully installed $skill_name${NC}"
    else
        echo -e "${RED}Error: Failed to extract ${skill_name}${NC}"
        rm -rf "$target_dir"
        rm -f "$zip_path"
        return 1
    fi

    # Clean up zip file
    rm -f "$zip_path"

    echo ""
}

# Check if at least one skill name is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <skill_name> [skill_name2] [skill_name3] ..."
    echo "Example: $0 finnhub massive-api tavily"
    exit 1
fi

# Check if required commands are available
for cmd in curl unzip; do
    if ! command -v $cmd &> /dev/null; then
        echo -e "${RED}Error: '$cmd' is required but not installed.${NC}"
        exit 1
    fi
done

# Check if openclaw command is available
if ! command -v openclaw &> /dev/null; then
    echo -e "${RED}Error: 'openclaw' command is required but not found.${NC}"
    exit 1
fi

# Install each skill
echo "========================================="
echo "ClawHub Skill Installer"
echo "========================================="
echo ""

success_count=0
fail_count=0

for skill_name in "$@"; do
    if install_skill "$skill_name"; then
        ((success_count++))
    else
        ((fail_count++))
    fi
done

echo "========================================="
echo "Installation complete!"
echo -e "Success: ${GREEN}${success_count}${NC}"
echo -e "Failed: ${RED}${fail_count}${NC}"
echo "========================================="

if [ $fail_count -gt 0 ]; then
    exit 1
fi
