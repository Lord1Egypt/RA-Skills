#!/bin/bash
# Fetch web content using Cloudflare's Markdown for Agents protocol
# Usage: fetch-markdown.sh <URL>

set -e

URL="$1"

if [ -z "$URL" ]; then
    echo "Usage: $0 <URL>"
    echo "Example: $0 https://developers.cloudflare.com/agents/"
    exit 1
fi

echo "Fetching Markdown from: $URL"
echo "---"

# Fetch with Accept header for Markdown
curl -sSL "$URL" \
    -H "Accept: text/markdown, text/html;q=0.9" \
    -D - \
    --compressed
