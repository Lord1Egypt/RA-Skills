#!/bin/bash

# Document Spell Check Script
# Usage: ./doc-spellcheck.sh [check|fix] [options] <file_or_directory>

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default settings
MODE="check"
DRY_RUN=false
INTERACTIVE=false
EXCLUDE_PATTERNS=("node_modules" ".git" "dist" "build")
FILE_EXTENSIONS=("md" "mdx" "txt" "rst")

# Function to display usage
usage() {
    echo "Usage: $0 [check|fix] [options] <file_or_directory>"
    echo ""
    echo "Commands:"
    echo "  check     Check for spelling errors (default)"
    echo "  fix       Automatically fix common spelling errors"
    echo ""
    echo "Options:"
    echo "  --dry-run     Preview changes without applying them"
    echo "  --interactive Interactive mode for manual review"
    echo "  --exclude PATTERN  Exclude files matching pattern"
    echo "  --extensions EXT   Comma-separated file extensions to check"
    echo "  --help            Show this help message"
    exit 1
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        check)
            MODE="check"
            shift
            ;;
        fix)
            MODE="fix"
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --interactive)
            INTERACTIVE=true
            shift
            ;;
        --exclude)
            EXCLUDE_PATTERNS+=("$2")
            shift 2
            ;;
        --extensions)
            IFS=',' read -ra FILE_EXTENSIONS <<< "$2"
            shift 2
            ;;
        --help)
            usage
            ;;
        -*)
            echo "Unknown option: $1"
            usage
            ;;
        *)
            TARGET="$1"
            shift
            ;;
    esac
done

# Validate target
if [[ -z "$TARGET" ]]; then
    echo -e "${RED}Error: Please specify a file or directory to check${NC}"
    usage
fi

if [[ ! -e "$TARGET" ]]; then
    echo -e "${RED}Error: Target '$TARGET' does not exist${NC}"
    exit 1
fi

# Check if aspell is installed
if ! command -v aspell &> /dev/null; then
    echo -e "${YELLOW}Warning: aspell not found. Installing...${NC}"
    if command -v brew &> /dev/null; then
        brew install aspell
    elif command -v apt-get &> /dev/null; then
        sudo apt-get install aspell
    else
        echo -e "${RED}Error: Cannot install aspell automatically. Please install it manually.${NC}"
        exit 1
    fi
fi

# Function to check if file should be excluded
should_exclude() {
    local file="$1"
    for pattern in "${EXCLUDE_PATTERNS[@]}"; do
        if [[ "$file" == *"$pattern"* ]]; then
            return 0
        fi
    done
    return 1
}

# Function to check if file extension is supported
has_supported_extension() {
    local file="$1"
    local ext="${file##*.}"
    for supported_ext in "${FILE_EXTENSIONS[@]}"; do
        if [[ "$ext" == "$supported_ext" ]]; then
            return 0
        fi
    done
    return 1
}

# Function to find all files to process
find_files() {
    local target="$1"
    if [[ -f "$target" ]]; then
        if has_supported_extension "$target" && ! should_exclude "$target"; then
            echo "$target"
        fi
    elif [[ -d "$target" ]]; then
        while IFS= read -r -d '' file; do
            if has_supported_extension "$file" && ! should_exclude "$file"; then
                echo "$file"
            fi
        done < <(find "$target" -type f -print0 2>/dev/null)
    fi
}

# Function to check spelling in a file
check_file() {
    local file="$1"
    echo -e "${GREEN}Checking: $file${NC}"
    
    # Get spelling errors
    local errors
    errors=$(aspell --lang=en --mode=markdown list < "$file" 2>/dev/null | sort | uniq)
    
    if [[ -n "$errors" ]]; then
        echo -e "${YELLOW}Spelling errors found:${NC}"
        echo "$errors" | head -10  # Show first 10 errors
        if [[ $(echo "$errors" | wc -l) -gt 10 ]]; then
            echo "... and $(( $(echo "$errors" | wc -l) - 10 )) more"
        fi
        return 1
    else
        echo -e "${GREEN}No spelling errors found${NC}"
        return 0
    fi
}

# Function to fix common spelling errors
fix_file() {
    local file="$1"
    local temp_file="${file}.tmp"
    
    echo -e "${GREEN}Fixing: $file${NC}"
    
    # Common misspelling corrections
    cp "$file" "$temp_file"
    
    # Basic misspellings
    sed -i '' 's/\brecieve\b/receive/g' "$temp_file"
    sed -i '' 's/\bteh\b/the/g' "$temp_file"
    sed -i '' 's/\bseperate\b/separate/g' "$temp_file"
    sed -i '' 's/\boccured\b/occurred/g' "$temp_file"
    sed -i '' 's/\bdefinately\b/definitely/g' "$temp_file"
    sed -i '' 's/\bexistance\b/existence/g' "$temp_file"
    sed -i '' 's/\bwether\b/whether/g' "$temp_file"
    sed -i '' 's/\badress\b/address/g' "$temp_file"
    sed -i '' 's/\buntill\b/until/g' "$temp_file"
    sed -i '' 's/\bcomming\b/coming/g' "$temp_file"
    sed -i '' 's/\bdissapear\b/disappear/g' "$temp_file"
    sed -i '' 's/\bformating\b/formatting/g' "$temp_file"
    
    # Check if file changed
    if ! cmp -s "$file" "$temp_file"; then
        if [[ "$DRY_RUN" == true ]]; then
            echo -e "${YELLOW}Dry run: Would fix spelling errors in $file${NC}"
            diff "$file" "$temp_file" || true
        else
            mv "$temp_file" "$file"
            echo -e "${GREEN}Fixed spelling errors in $file${NC}"
        fi
    else
        rm "$temp_file"
        echo -e "${GREEN}No spelling errors to fix in $file${NC}"
    fi
}

# Main execution
echo -e "${GREEN}Document Spell Check Tool v1.0.0${NC}"
echo "Mode: $MODE"
echo "Target: $TARGET"

error_count=0
total_files=0

while IFS= read -r file; do
    ((total_files++))
    if [[ "$MODE" == "check" ]]; then
        if ! check_file "$file"; then
            ((error_count++))
        fi
    elif [[ "$MODE" == "fix" ]]; then
        fix_file "$file"
    fi
done < <(find_files "$TARGET")

echo ""
echo -e "${GREEN}Summary:${NC}"
echo "Total files processed: $total_files"
if [[ "$MODE" == "check" ]]; then
    echo "Files with errors: $error_count"
    if [[ $error_count -gt 0 ]]; then
        exit 1
    fi
fi

echo -e "${GREEN}Spell check completed successfully!${NC}"