#!/bin/bash
# FormatFerry conversion wrapper script
# Usage: ./convert-to-md.sh [--input FILE] [--output FILE] [--flavour FORMAT] [--url URL] [stdin]
#
# Safe wrapper with no eval — uses bash arrays for argument passing.

set -euo pipefail

# Defaults
INPUT_FILE=""
OUTPUT_FILE=""
FLAVOUR="github"
URL=""
USE_STDIN=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --input|-i)
            INPUT_FILE="$2"
            shift 2
            ;;
        --output|-o)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        --flavour|--format|-f)
            FLAVOUR="$2"
            shift 2
            ;;
        --url)
            URL="$2"
            shift 2
            ;;
        -)
            USE_STDIN=true
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Check formatferry is installed
if ! command -v formatferry &> /dev/null; then
    echo "Error: formatferry not found. Install with: npm install -g formatferry" >&2
    exit 1
fi

# Build command as bash array (safe — no eval)
ARGS=(formatferry -f "$FLAVOUR")

# Add input source
if [[ "$USE_STDIN" == "true" ]]; then
    : # stdin piped through below
elif [[ -n "$INPUT_FILE" ]]; then
    if [[ ! -f "$INPUT_FILE" ]]; then
        echo "Error: Input file not found: $INPUT_FILE" >&2
        exit 1
    fi
    ARGS+=(-i "$INPUT_FILE")
elif [[ -n "$URL" ]]; then
    ARGS+=(--url "$URL")
else
    echo "Error: No input provided. Use --input, --url, or pipe to stdin." >&2
    exit 1
fi

# Add output if specified
if [[ -n "$OUTPUT_FILE" ]]; then
    ARGS+=(-o "$OUTPUT_FILE")
fi

# Execute
if [[ "$USE_STDIN" == "true" ]]; then
    cat - | "${ARGS[@]}"
else
    "${ARGS[@]}"
fi

exit 0
