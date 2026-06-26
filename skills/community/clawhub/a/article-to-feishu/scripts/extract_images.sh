#!/bin/bash
# Extract image URLs from a Toutiao article
# Usage: extract_images.sh <toutiao_url>

set -e

if [ -z "$1" ]; then
    echo "Usage: extract_images.sh <toutiao_url>"
    echo "Example: extract_images.sh 'https://m.toutiao.com/is/m3EX1m0Z3Mo/'"
    exit 1
fi

URL="$1"
JINA_API="https://r.jina.ai/"

# Fetch article content
CONTENT=$(curl -sL "${JINA_API}${URL}" 2>/dev/null)

# Extract image URLs (common patterns)
# Pattern 1: https://p3-sign.toutiaoimg.com/...
# Pattern 2: https://p9-sign.toutiaoimg.com/...
# Pattern 3: Generic image URLs
echo "$CONTENT" | grep -oE 'https?://[^)"'\'' ]+\.(jpg|jpeg|png|gif|webp)' | sort -u