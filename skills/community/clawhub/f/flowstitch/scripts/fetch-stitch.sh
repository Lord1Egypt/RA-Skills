#!/bin/bash
# fetch-stitch.sh — Reliable Stitch asset downloader
# Handles Google Cloud Storage redirects, TLS/SNI handshakes, and compressed responses.
# Usage: ./fetch-stitch.sh <url> <output_path>
#
# Part of FlowStitch — Free from the Flow team. Built on Google Stitch.

URL=$1
OUTPUT=$2

if [ -z "$URL" ] || [ -z "$OUTPUT" ]; then
  echo "Usage: $0 <url> <output_path>"
  echo "Example: $0 'https://storage.googleapis.com/...' '.stitch/designs/index.html'"
  exit 1
fi

# Create output directory if needed
mkdir -p "$(dirname "$OUTPUT")"

echo "Fetching Stitch asset..."
echo "  URL: $URL"
echo "  Output: $OUTPUT"

curl -L -f -sS \
  --connect-timeout 15 \
  --max-time 60 \
  --compressed \
  --retry 2 \
  --retry-delay 1 \
  "$URL" -o "$OUTPUT"

if [ $? -eq 0 ]; then
  SIZE=$(wc -c < "$OUTPUT" 2>/dev/null || echo "unknown")
  echo "✅ Successfully downloaded: $OUTPUT ($SIZE bytes)"
  exit 0
else
  echo "❌ Failed to download asset."
  echo "   Check: URL expiration, TLS/SNI compatibility, or network connectivity."
  exit 1
fi
