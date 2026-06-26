#!/bin/bash
#
# Everything CLI Search Script
# Fast file and folder search using Everything's command line interface.
#

# Default es.exe path
ES_PATH="${ES_PATH:-es.exe}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print error message
error() {
    echo -e "${RED}Error: $1${NC}" >&2
    exit 1
}

# Print info message
info() {
    echo -e "${BLUE}Info: $1${NC}"
}

# Print success message
success() {
    echo -e "${GREEN}Success: $1${NC}"
}

# Check if es.exe exists
check_es() {
    if ! command -v "$ES_PATH" &> /dev/null; then
        error "es.exe not found. Please install Everything from https://www.voidtools.com"
    fi
}

# Build es.exe command
build_cmd() {
    local cmd=("$ES_PATH")

    # Add options
    if [[ -n "$ES_PATH_ARG" ]]; then
        cmd+=("-p" "$ES_PATH_ARG")
    fi

    if [[ "$ES_REGEX" == "true" ]]; then
        cmd+=("-regex")
    fi

    if [[ "$ES_CASE" == "true" ]]; then
        cmd+=("-case")
    else
        cmd+=("-nocase")
    fi

    if [[ "$ES_WHOLE_WORD" == "true" ]]; then
        cmd+=("-wholeword")
    fi

    if [[ "$ES_MATCH_PATH" == "true" ]]; then
        cmd+=("-matchpath")
    fi

    if [[ -n "$ES_SORT" ]]; then
        cmd+=("-sort" "$ES_SORT")
    fi

    if [[ "$ES_SORT_DESC" == "true" ]]; then
        cmd+=("-sort-descending")
    fi

    if [[ "$ES_DETAILS" == "true" ]]; then
        cmd+=("-details")
    fi

    # Add query
    cmd+=("$ES_QUERY")

    echo "${cmd[@]}"
}

# Main search function
search() {
    local query="$1"
    shift

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -p|--path)
                ES_PATH_ARG="$2"
                shift 2
                ;;
            -r|--regex)
                ES_REGEX="true"
                shift
                ;;
            -c|--case)
                ES_CASE="true"
                shift
                ;;
            -w|--whole-word)
                ES_WHOLE_WORD="true"
                shift
                ;;
            -m|--match-path)
                ES_MATCH_PATH="true"
                shift
                ;;
            -s|--sort)
                ES_SORT="$2"
                shift 2
                ;;
            -d|--descending)
                ES_SORT_DESC="true"
                shift
                ;;
            --details)
                ES_DETAILS="true"
                shift
                ;;
            -l|--limit)
                ES_LIMIT="$2"
                shift 2
                ;;
            -j|--json)
                ES_JSON="true"
                shift
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                error "Unknown option: $1"
                ;;
        esac
    done

    # Set query
    ES_QUERY="$query"

    # Check if es.exe exists
    check_es

    # Build command
    local cmd
    cmd=$(build_cmd)

    # Execute search
    info "Searching for: $ES_QUERY"
    if [[ -n "$ES_PATH_ARG" ]]; then
        info "Path: $ES_PATH_ARG"
    fi

    # Run command
    if [[ "$ES_JSON" == "true" ]]; then
        # Output as JSON
        local output
        output=$(eval "$cmd" 2>&1)
        echo "$output" | jq -R 'split("\n") | map(select(length > 0)) | map({path: .})' 2>/dev/null || echo "$output"
    else
        # Output as text
        eval "$cmd"
    fi
}

# Show help
show_help() {
    cat << EOF
Everything CLI Search - Fast file and folder search

Usage:
    es_search.sh [OPTIONS] QUERY

Options:
    -p, --path PATH          Search in specific path
    -r, --regex              Enable regex search
    -c, --case               Case-sensitive search
    -w, --whole-word         Match whole word only
    -m, --match-path         Match full path
    -s, --sort FIELD         Sort by field (name, size, "Date Modified", etc.)
    -d, --descending         Sort in descending order
    --details                Show details view
    -l, --limit N            Limit number of results
    -j, --json               Output as JSON
    -h, --help               Show this help message

Examples:
    # Basic search
    es_search.sh "filename"

    # Search in specific path
    es_search.sh -p "F:\openclaw-skills" "SKILL.md"

    # Search with regex
    es_search.sh -r "test_.*\.py"

    # Case-sensitive search
    es_search.sh -c "FileName"

    # Sort by size (largest first)
    es_search.sh -s size -d "*.pdf"

    # Search for browser-related skills
    es_search.sh -p "F:\openclaw-skills\skills" -r ".*browser.*"

Environment Variables:
    ES_PATH                  Path to es.exe (default: es.exe)

For more information, see:
    https://www.voidtools.com/support/everything/command_line_options
EOF
}

# Main entry point
if [[ $# -eq 0 ]]; then
    show_help
    exit 1
fi

search "$@"
