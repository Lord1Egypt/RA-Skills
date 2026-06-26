#!/bin/bash
# ntfy Callback - Send callback via ntfy notification

set -euo pipefail

# Default values
STATUS="done"
MODE="single"
TASK=""
MESSAGE=""
OUTPUT=""
NTFY_SERVER=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --status)
            STATUS="$2"
            shift 2
            ;;
        --mode)
            MODE="$2"
            shift 2
            ;;
        --task)
            TASK="$2"
            shift 2
            ;;
        --message)
            MESSAGE="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        --server)
            NTFY_SERVER="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Get ntfy server from env if not provided
if [[ -z "$NTFY_SERVER" ]]; then
    NTFY_SERVER="${NTFY_SERVER:-ntfy.sh}"
fi

# Build title based on status
case "$STATUS" in
    done)
        TITLE="✅ Claude Code Task Complete"
        ;;
    error)
        TITLE="❌ Claude Code Task Failed"
        ;;
    progress)
        TITLE="🔄 Claude Code Task Progress"
        ;;
    *)
        TITLE="📋 Claude Code Update"
        ;;
esac

# Build message
if [[ -n "$MESSAGE" ]]; then
    BODY="$MODE: $TASK - $MESSAGE"
else
    BODY="$MODE: $TASK"
fi

# Append output if provided (truncate if too long for ntfy)
if [[ -n "$OUTPUT" ]]; then
    # Get last 1000 chars of output to avoid size limits
    OUTPUT_TRUNCATED="${OUTPUT: -1000}"
    BODY="$BODY

--- Response ---
${OUTPUT_TRUNCATED}"
fi

# Check if ntfy is available
if command -v ntfy &> /dev/null; then
    ntfy send -t "$TITLE" "$BODY" "$NTFY_SERVER"
else
    # Fallback to curl
    curl -s -X POST "$NTFY_SERVER" \
        -H "Title: $TITLE" \
        -d "$BODY"
fi

echo "ntfy notification sent"
