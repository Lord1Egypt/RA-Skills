#!/bin/bash
# download-bilibili.sh - Download video from Bilibili URL
# Usage: ./download-bilibili.sh <bilibili-url> <output-directory>

set -euo pipefail

if [ $# -lt 2 ]; then
    echo "Usage: $0 <bilibili-url> <output-directory>"
    exit 1
fi

URL="$1"
OUT_DIR="$2"

mkdir -p "$OUT_DIR"

echo "Downloading from Bilibili: $URL"
echo "Output directory: $OUT_DIR"

# Use yt-dlp to download the best quality available
# For Bilibili, we get 720p by default unless cookies are provided for higher quality
yt-dlp -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]' \
    --yes-playlist \
    -o "$OUT_DIR/%(title)s.%(ext)s" \
    "$URL"

echo "Download completed"
ls -lh "$OUT_DIR"
