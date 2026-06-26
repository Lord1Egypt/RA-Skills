#!/bin/bash

# ClawHub Skill Search Tool
# Usage: clawhub-search.sh [keyword]
# If no keyword provided, lists top skills by downloads

set -e

API_URL="https://wry-manatee-359.convex.site/api/v1/skills"
SKILLS_DIR="$HOME/.agents/skills/clawhub-skills"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

search_keyword="$1"

# Fetch skills from API
fetch_skills() {
    local cursor="$1"
    local url="$API_URL"
    if [ -n "$cursor" ]; then
        url="$API_URL?cursor=$cursor"
    fi
    curl -s "$url"
}

# Search in skill data
search_skills() {
    local keyword="$1"
    local all_skills="[]"
    local cursor=""
    local total=0
    
    # Fetch up to 100 skills (multiple pages if needed)
    while [ $total -lt 100 ]; do
        local response
        response=$(fetch_skills "$cursor")
        
        # Parse items
        local items
        items=$(echo "$response" | jq -r '.items // []')
        local count
        count=$(echo "$items" | jq 'length')
        
        if [ "$count" -eq 0 ]; then
            break
        fi
        
        all_skills=$(echo "$all_skills" "$items" | jq -s 'add')
        total=$(echo "$all_skills" | jq 'length')
        
        # Get next cursor
        cursor=$(echo "$response" | jq -r '.nextCursor // empty')
        if [ -z "$cursor" ]; then
            break
        fi
    done
    
    # Filter by keyword if provided
    if [ -n "$keyword" ]; then
        echo "$all_skills" | jq --arg kw "$keyword" '
            [.[] | select(
                (.slug // "" | ascii_downcase | contains($kw | ascii_downcase)) or
                (.displayName // "" | ascii_downcase | contains($kw | ascii_downcase)) or
                (.summary // "" | ascii_downcase | contains($kw | ascii_downcase))
            )] | sort_by(.stats.downloads) | reverse | .[0:20]
        '
    else
        # Sort by downloads, show top 20
        echo "$all_skills" | jq 'sort_by(.stats.downloads) | reverse | .[0:20]'
    fi
}

# Format and display results
display_results() {
    local skills_json="$1"
    local count
    count=$(echo "$skills_json" | jq 'length')
    
    if [ "$count" -eq 0 ]; then
        echo -e "${YELLOW}No skills found matching your search.${NC}"
        return
    fi
    
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  ClawHub Skills (${count} results)${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    echo "$skills_json" | jq -r '.[] | @base64' | while read -r encoded; do
        local skill
        skill=$(echo "$encoded" | base64 -d)
        
        local slug displayName summary downloads stars installed
        slug=$(echo "$skill" | jq -r '.slug // "N/A"')
        displayName=$(echo "$skill" | jq -r '.displayName // "N/A"')
        summary=$(echo "$skill" | jq -r '.summary // "No description"')
        downloads=$(echo "$skill" | jq -r '.stats.downloads // 0')
        stars=$(echo "$skill" | jq -r '.stats.stars // 0')
        
        # Check if already installed
        if [ -d "$SKILLS_DIR/$slug" ]; then
            installed="${GREEN}[installed]${NC}"
        else
            installed=""
        fi
        
        # Truncate summary if too long
        if [ ${#summary} -gt 80 ]; then
            summary="${summary:0:77}..."
        fi
        
        echo -e "${GREEN}$slug${NC} $installed"
        echo -e "  ${BLUE}Name:${NC} $displayName"
        echo -e "  ${BLUE}Summary:${NC} $summary"
        echo -e "  ${BLUE}Downloads:${NC} $downloads  ${BLUE}Stars:${NC} $stars"
        echo ""
    done
    
    echo -e "${CYAN}────────────────────────────────────────────────────────────────${NC}"
    echo -e "To install a skill, use: ${YELLOW}clawhub-download.sh <slug>${NC}"
    echo -e "Or visit: ${YELLOW}https://clawhub.ai/<slug>${NC}"
    echo -e "${CYAN}────────────────────────────────────────────────────────────────${NC}"
}

# Main
if ! command -v jq &> /dev/null; then
    echo "Error: jq is required but not installed."
    echo "Install it with: sudo apt-get install jq"
    exit 1
fi

if [ -n "$search_keyword" ]; then
    echo -e "${BLUE}Searching for: ${YELLOW}$search_keyword${NC}..."
else
    echo -e "${BLUE}Fetching top skills from ClawHub...${NC}"
fi

skills_json=$(search_skills "$search_keyword")
display_results "$skills_json"