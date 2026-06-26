#!/bin/bash
#
# list-decisions.sh - List decision records with filtering
# Usage: ./list-decisions.sh [--status pending|decided|validated] [--since YYYY-MM-DD]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="${DECISION_DATA_DIR:-$SKILL_DIR/data}"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Parse arguments
FILTER_STATUS=""
FILTER_SINCE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --status)
            FILTER_STATUS="$2"
            shift 2
            ;;
        --since)
            FILTER_SINCE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check if data directory exists
if [[ ! -d "$DATA_DIR" ]]; then
    echo "No decisions found (data directory doesn't exist)"
    exit 0
fi

# Find all decision files
DECISIONS=$(find "$DATA_DIR" -name "DEC-*.md" -type f 2>/dev/null | sort -r)

if [[ -z "$DECISIONS" ]]; then
    echo "No decisions found"
    exit 0
fi

# Header
echo -e "${BLUE}📋 Decisions${NC}"
echo "============"

# Filter and display
COUNT=0
for decision in $DECISIONS; do
    # Extract metadata
    ID=$(basename "$decision" .md)
    TITLE=$(grep "^# Decision:" "$decision" 2>/dev/null | sed 's/# Decision: //' | cut -d'-' -f1 | sed 's/ *$//')
    STATUS=$(grep "^\\*\\*Status\\*\\*:" "$decision" 2>/dev/null | cut -d: -f2- | sed 's/^ *//')
    DOMAIN=$(grep "^\\*\\*Domain\\*\\*:" "$decision" 2>/dev/null | cut -d: -f2- | sed 's/^ *//')
    
    # Apply filters
    if [[ -n "$FILTER_STATUS" && "$STATUS" != "$FILTER_STATUS" ]]; then
        continue
    fi
    
    # Display
    STATUS_COLOR="$NC"
    case "$STATUS" in
        pending) STATUS_COLOR="\033[0;33m" ;;    # Yellow
        decided) STATUS_COLOR="\033[0;34m" ;;    # Blue
        validated) STATUS_COLOR="\033[0;32m" ;;  # Green
        revised) STATUS_COLOR="\033[0;35m" ;;    # Purple
        archived) STATUS_COLOR="\033[0;37m" ;;   # Gray
    esac
    
    echo ""
    echo -e "${GREEN}$ID${NC} [${STATUS_COLOR}${STATUS}${NC}]"
    echo "  Title: $TITLE"
    if [[ -n "$DOMAIN" ]]; then
        echo "  Domain: $DOMAIN"
    fi
    
    COUNT=$((COUNT + 1))
done

echo ""
echo "============"
echo "Total: $COUNT decisions"
