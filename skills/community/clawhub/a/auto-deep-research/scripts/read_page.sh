#!/bin/bash
# Read page script - 封装 Jina Reader API

URL="$1"
OUTPUT_FILE="${2:-page.md}"

if [ -z "$URL" ]; then
  echo "Usage: read_page.sh <url> [output_file]"
  exit 1
fi

# Jina Reader API
curl -s "https://r.jina.ai/readability/page?url=$URL" > "$OUTPUT_FILE"

echo "Page saved to $OUTPUT_FILE"