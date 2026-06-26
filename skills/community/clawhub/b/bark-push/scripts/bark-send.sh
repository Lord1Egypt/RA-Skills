#!/bin/bash
# Bark Push Notification Script
# Usage: bark-send.sh [options]
#
# Options:
#   -t, --title     Push title (required)
#   -b, --body     Push body/content (required)
#   -k, --key      Device key (optional, uses $BARK_KEY if not provided)
#   -s, --sound    Sound name (optional, default: default)
#   -B, --badge    Badge number (optional)
#   -u, --url      Click跳转URL (optional)
#   -g, --group    Group name (optional)
#   -l, --level    Notification level: critical/active/timeSensitive/passive (optional)
#   -i, --image    Image URL (optional)
#   -S, --subtitle Subtitle (optional)
#   -h, --help     Show help
#
# Examples:
#   bark-send.sh -t "标题" -b "内容"
#   bark-send.sh --title "提醒" --body "时间到了" --sound alarm
#   BARK_KEY=your_key bark-send.sh -t "测试" -b "推送测试"

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
SOUND="default"
BADGE=""
URL=""
GROUP=""
LEVEL=""
IMAGE=""
SUBTITLE=""
DEVICE_KEY="${BARK_KEY:-${BARK_DEVICE_KEY:-}}"

# Usage function
usage() {
    head -32 "$0" | tail -28
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--title)
            TITLE="$2"
            shift 2
            ;;
        -b|--body)
            BODY="$2"
            shift 2
            ;;
        -k|--key)
            DEVICE_KEY="$2"
            shift 2
            ;;
        -s|--sound)
            SOUND="$2"
            shift 2
            ;;
        -B|--badge)
            BADGE="$2"
            shift 2
            ;;
        -u|--url)
            URL="$2"
            shift 2
            ;;
        -g|--group)
            GROUP="$2"
            shift 2
            ;;
        -l|--level)
            LEVEL="$2"
            shift 2
            ;;
        -i|--image)
            IMAGE="$2"
            shift 2
            ;;
        -S|--subtitle)
            SUBTITLE="$2"
            shift 2
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            usage
            ;;
    esac
done

# Validate required parameters
if [[ -z "$TITLE" ]]; then
    echo -e "${RED}Error: Title is required${NC}"
    usage
fi

if [[ -z "$BODY" ]]; then
    echo -e "${RED}Error: Body is required${NC}"
    usage
fi

if [[ -z "$DEVICE_KEY" ]]; then
    echo -e "${RED}Error: Device key is required. Set BARK_KEY env or use -k option${NC}"
    exit 1
fi

# Build request URL
API_URL="https://api.day.app/${DEVICE_KEY}"

# Build query string
QUERY_PARAMS=""

if [[ -n "$SOUND" ]]; then
    QUERY_PARAMS="${QUERY_PARAMS}sound=${SOUND}&"
fi

if [[ -n "$BADGE" ]]; then
    QUERY_PARAMS="${QUERY_PARAMS}badge=${BADGE}&"
fi

if [[ -n "$URL" ]]; then
    QUERY_PARAMS="${QUERY_PARAMS}url=${URL}&"
fi

if [[ -n "$GROUP" ]]; then
    QUERY_PARAMS="${QUERY_PARAMS}group=${GROUP}&"
fi

if [[ -n "$LEVEL" ]]; then
    QUERY_PARAMS="${QUERY_PARAMS}level=${LEVEL}&"
fi

if [[ -n "$IMAGE" ]]; then
    QUERY_PARAMS="${QUERY_PARAMS}image=${IMAGE}&"
fi

if [[ -n "$SUBTITLE" ]]; then
    QUERY_PARAMS="${QUERY_PARAMS}subtitle=${SUBTITLE}&"
fi

# Remove trailing &
QUERY_PARAMS="${QUERY_PARAMS%%&}"

# Send notification using POST with JSON
JSON_PAYLOAD=$(cat <<EOF
{
    "title": "$TITLE",
    "body": "$BODY"$(if [[ -n "$SUBTITLE" ]]; then echo ", \"subtitle\": \"$SUBTITLE\""; fi)$(if [[ -n "$SOUND" ]]; then echo ", \"sound\": \"$SOUND\""; fi)$(if [[ -n "$BADGE" ]]; then echo ", \"badge\": $BADGE"; fi)$(if [[ -n "$URL" ]]; then echo ", \"url\": \"$URL\""; fi)$(if [[ -n "$GROUP" ]]; then echo ", \"group\": \"$GROUP\""; fi)$(if [[ -n "$LEVEL" ]]; then echo ", \"level\": \"$LEVEL\""; fi)$(if [[ -n "$IMAGE" ]]; then echo ", \"image\": \"$IMAGE\""; fi)
}
EOF
)

# URL encode title and body for GET fallback
ENCODED_TITLE=$(echo -n "$TITLE" | jq -Rs '.' | sed 's/^"//;s/"$//' | jq -Rs '@uri' | sed 's/^"//;s/"$//')
ENCODED_BODY=$(echo -n "$BODY" | jq -Rs '.' | sed 's/^"//;s/"$//' | jq -Rs '@uri' | sed 's/^"//;s/"$//')

# Try POST first (more reliable)
if [[ -n "$QUERY_PARAMS" ]]; then
    FULL_URL="${API_URL}?${QUERY_PARAMS}"
else
    FULL_URL="${API_URL}"
fi

# Send request
RESPONSE=$(curl -s -X POST "$FULL_URL" \
    -H 'Content-Type: application/json' \
    -d "$JSON_PAYLOAD" 2>&1)

# Check response
if echo "$RESPONSE" | grep -q '"code":200'; then
    echo -e "${GREEN}✓ Push notification sent successfully!${NC}"
    echo "  Title: $TITLE"
    echo "  Body: $BODY"
    exit 0
else
    echo -e "${RED}✗ Failed to send push notification${NC}"
    echo "  Response: $RESPONSE"
    exit 1
fi
