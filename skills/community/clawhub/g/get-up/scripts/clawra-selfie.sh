#!/bin/bash
# clawra-selfie.sh
# Get an image url and send it via OpenClaw
#
# Usage: ./clawra-selfie.sh "<prompt>" "<channel>" "<target>" ["<caption>"]
#
#

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check for openclaw
if ! command -v openclaw &> /dev/null; then
    log_warn "openclaw CLI not found - will attempt direct API call"
    USE_CLI=false
else
    USE_CLI=true
fi

# Parse arguments
PROMPT="${1:-}"
CHANNEL="${2:-}"
TARGET="${3:-}"

if [ -z "$PROMPT" ] || [ -z "$CHANNEL" ]; then
    echo "Usage: $0 <prompt> <channel> <target>"
    echo ""
    echo "Arguments:"
    echo "  prompt        - Image description (required)"
    echo "  channel       - channel (required) e.g., whatsapp,signal"
    echo "  target        - target (required) e.g., E.164, +860123456789"
    echo ""
    echo "Example:"
    echo "  $0 \"A night\" \"whatsapp\" \"+1234567890\" "
    exit 1
fi

randnum() {
    local seed=$$
    seed=$((seed * $(date +%s) % 32767))
    case "$1" in
        31|52)
            local num=$(( (seed * 1103515245 + 12345) % $1 + 1 ))
            printf "%03d" $num
            # printf "%03d" $((RANDOM % $1 + 1))
            ;;
        *)
            echo -n "001"
            ;;
    esac
}

whatwant() {
    if [ $# -eq 0 ]; then
        num=$(randnum 52)
        printf "haocun-dance-frames/haocun-m%03d.png" $num
    fi
    echo $1

    want=$(openclaw agent --timeout 10 --thinking "off" --agent main -m "check user wants me 'dance' or 'selfie', JUST IN ONE lowercase WORD: $1" | grep -E "dance|selfie" | tr -d '\r\n\t ')

    if [[ "$want" =~ "selfie" ]]; then
        num=$(randnum 31)
        printf "haocun-selfie-frames/haocun-s%03d.png" $((10#$num))
    else ## if [[ "$want" =~ "dance" ]]; then
        num=$(randnum 52)
        printf "haocun-dance-frames/haocun-m%03d.png" $((10#$num))
    fi
}

imagepath=$(whatwant $PROMPT)

imagedir="https://cdn.jsdelivr.net/gh/christoagent/haoclaw@main/assets/"

IMAGE_URL=$(printf "%s%s" $imagedir $imagepath)

# Send via OpenClaw
log_info "Sending to channel: $CHANNEL"

if [ "$USE_CLI" = true ]; then
    # Use OpenClaw CLI
    openclaw message send \
        --channel "$CHANNEL" \
        --target "$TARGET" \
        --message "I am here" \
        --media "$IMAGE_URL"
else
    # Direct API call to local gateway
    GATEWAY_URL="${OPENCLAW_GATEWAY_URL:-http://localhost:18789}"
    GATEWAY_TOKEN="${OPENCLAW_GATEWAY_TOKEN:-}"

    HEADERS="-H \"Content-Type: application/json\""
    if [ -n "$GATEWAY_TOKEN" ]; then
        HEADERS="$HEADERS -H \"Authorization: Bearer $GATEWAY_TOKEN\""
    fi

    curl -s -X POST "$GATEWAY_URL/message" \
        -H "Content-Type: application/json" \
        ${GATEWAY_TOKEN:+-H "Authorization: Bearer $GATEWAY_TOKEN"} \
        -d "{
            \"action\": \"send\",
            \"channel\": \"$CHANNEL\",
            \"message\": \"Get you back\",
            \"media\": \"$IMAGE_URL\"
        }"
fi

log_info "Done! Image sent to $CHANNEL"

# Output JSON for programmatic use
echo ""
echo "--- Result ---"
jq -n \
    --arg url "$IMAGE_URL" \
    --arg channel "$CHANNEL" \
    --arg prompt "$PROMPT" \
    '{
        success: true,
        image_url: $url,
        channel: $channel,
        prompt: $prompt
    }'
