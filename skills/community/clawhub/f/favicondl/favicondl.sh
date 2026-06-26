#!/bin/bash
# FaviconDL - Download favicon via favicondl.com
# Usage: favicondl.sh <domain> [size] [output_path]

DOMAIN="${1:-}"
SIZE="${2:-128}"
OUTPUT="${3:-./favicon.png}"

if [ -z "$DOMAIN" ]; then
    echo "Usage: favicondl <domain> [size] [output_path]"
    echo "Example: favicondl github.com 128 ./logo.png"
    exit 1
fi

URL="https://favicondl.com/api/favicon?domain=${DOMAIN}&size=${SIZE}&format=redirect"

echo "Fetching favicon for ${DOMAIN} at ${SIZE}px..."

HTTP_CODE=$(curl -L -s -o "$OUTPUT" -w "%{http_code}" "$URL")

if [ "$HTTP_CODE" -eq 200 ] || [ "$HTTP_CODE" -eq 302 ] || [ "$HTTP_CODE" -eq 307 ]; then
    FILE_SIZE=$(stat -c%s "$OUTPUT" 2>/dev/null || stat -f%z "$OUTPUT" 2>/dev/null)
    echo "Saved: $OUTPUT (${FILE_SIZE} bytes)"
else
    echo "Error: HTTP $HTTP_CODE"
    rm -f "$OUTPUT"
    exit 1
fi
