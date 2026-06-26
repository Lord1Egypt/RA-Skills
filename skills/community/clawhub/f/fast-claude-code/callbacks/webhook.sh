#!/bin/bash
# Webhook Callback - Send callback via HTTP webhook

set -euo pipefail

# Default values
STATUS="done"
MODE="single"
TASK=""
MESSAGE=""
OUTPUT=""
WEBHOOK_URL=""

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
        --webhook)
            WEBHOOK_URL="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Get webhook URL from env if not provided
if [[ -z "$WEBHOOK_URL" ]]; then
    WEBHOOK_URL="${CC_WEBHOOK_URL:-}"
fi

if [[ -z "$WEBHOOK_URL" ]]; then
    echo "Error: --webhook URL or CC_WEBHOOK_URL env required"
    exit 1
fi

# Escape strings for JSON
escape_json() {
    local string="$1"
    # Escape backslashes, quotes, and newlines
    string="${string//\\/\\\\}"
    string="${string//\"/\\\"}"
    string="${string//$'\n'/\\n}"
    string="${string//$'\r'/\\r}"
    string="${string//$'\t'/\\t}"
    printf '%s' "$string"
}

STATUS_JSON=$(escape_json "$STATUS")
MODE_JSON=$(escape_json "$MODE")
TASK_JSON=$(escape_json "$TASK")
MESSAGE_JSON=$(escape_json "$MESSAGE")
OUTPUT_JSON=$(escape_json "$OUTPUT")

# Build JSON payload
PAYLOAD=$(cat << EOF
{
    "status": "$STATUS_JSON",
    "mode": "$MODE_JSON",
    "task": "$TASK_JSON",
    "message": "$MESSAGE_JSON",
    "output": "$OUTPUT_JSON"
}
EOF
)

# Send webhook
curl -s -X POST "$WEBHOOK_URL" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" || echo "Webhook failed"

echo "Webhook sent to $WEBHOOK_URL"
