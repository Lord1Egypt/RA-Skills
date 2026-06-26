#!/bin/bash
# control_host_browser.sh - Create a new Chrome tab and navigate to a URL
#
# Usage: ./control_host_browser.sh <profile> <url>
#   profile: main | financier | programmer
#   url: the URL to navigate to
#
# This script:
# 1. Creates a new tab via Chrome DevTools Protocol (CDP)
# 2. Navigates to the specified URL using CDP over WebSocket

set -e

if [ $# -ne 2 ]; then
    echo "Usage: $0 <profile> <url>"
    echo "  profile: main | financier | programmer"
    echo "  url: the URL to navigate to"
    exit 1
fi

PROFILE=$1
URL=$2

# Port mapping for different browser instances
case $PROFILE in
    main)
        PORT=18800
        ;;
    *)
        echo "ERROR: Invalid profile '$PROFILE'. Use: main, financier, or programmer"
        exit 1
        ;;
esac

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ">>> Step 1: Creating new tab on $PROFILE (port $PORT)"

# Create new tab via CDP JSON API
RESPONSE=$(curl -s -X PUT "http://172.17.0.1:$PORT/json/new")

# Extract page ID from response
PAGE_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; data=json.load(sys.stdin); print(data.get('id', ''))" 2>/dev/null)

if [ -z "$PAGE_ID" ]; then
    echo "ERROR: Failed to create new tab. Response: $RESPONSE"
    exit 1
fi

echo ">>> Page ID: $PAGE_ID"

echo ">>> Step 2: Navigating to: $URL"

# Navigate using Python CDP script
python3 "$SCRIPT_DIR/cdp_navigate.py" "$PORT" "$PAGE_ID" "$URL"

if [ $? -eq 0 ]; then
    echo ">>> AGENT_RESULT:OK:$PAGE_ID:$URL"
    echo ">>> SUCCESS: Tab created and navigated to $URL"
else
    echo ">>> AGENT_RESULT:ERROR:$PAGE_ID:$URL"
    echo ">>> ERROR: Navigation failed"
    exit 1
fi
