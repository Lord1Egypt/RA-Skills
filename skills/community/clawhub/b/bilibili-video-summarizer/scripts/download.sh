#!/bin/bash
# bilibili-download.sh - Download subtitles from Bilibili video
# Usage: ./download.sh "<BILIBILI_URL>" [output_dir]
# Requires: yt-dlp (pip3 install yt-dlp --break-system-packages)
# Cookie file: ~/.config/bilibili-cookies.txt (Netscape format)

set -e

if [ -z "$1" ]; then
    echo "ERROR: No URL provided"
    echo "Usage: $0 <BILIBILI_URL> [output_dir]"
    exit 1
fi

URL="$1"
OUT_DIR="${2:-/tmp/bili-subtitles}"
COOKIE_FILE="$HOME/.config/bilibili-cookies.txt"

mkdir -p "$OUT_DIR"

# Check for cookie
if [ ! -f "$COOKIE_FILE" ]; then
    echo "ERROR: Cookie file not found at $COOKIE_FILE"
    echo "Please provide your Bilibili SESSDATA cookie."
    exit 1
fi

# Get video title
VIDEO_TITLE=$(yt-dlp --cookies "$COOKIE_FILE" \
    --skip-download --no-playlist --print "%(title)s" \
    "$URL" 2>/dev/null | head -1 | sed 's/[\\/:*?"<>|]/_/g')

if [ -z "$VIDEO_TITLE" ]; then
    echo "ERROR: Could not fetch video title"
    exit 1
fi

echo "VIDEO_TITLE: $VIDEO_TITLE"

# Check available subtitles first
SUBS=$(yt-dlp --cookies "$COOKIE_FILE" --list-subs "$URL" 2>/dev/null | grep -E "^(zh-CN|zh-Hans|zh-Hant|en-US|ai-zh|ai-en)" | head -5)
echo "AVAILABLE_SUBS: $SUBS"

# Download subtitles (prefer zh-CN, then ai-zh, then en-US)
OUTPUT_TEMPLATE="$OUT_DIR/$VIDEO_TITLE"

if yt-dlp --cookies "$COOKIE_FILE" \
    --write-subs --sub-langs "zh-CN,zh-Hans,zh-Hant" \
    --convert-subs srt --skip-download --no-playlist \
    --output "$OUTPUT_TEMPLATE.%(ext)s" \
    "$URL" 2>/dev/null; then
    echo "SUBTITLE_TYPE: zh"
elif yt-dlp --cookies "$COOKIE_FILE" \
    --write-subs --sub-langs "ai-zh" \
    --convert-subs srt --skip-download --no-playlist \
    --output "$OUTPUT_TEMPLATE.%(ext)s" \
    "$URL" 2>/dev/null; then
    echo "SUBTITLE_TYPE: ai-zh"
elif yt-dlp --cookies "$COOKIE_FILE" \
    --write-subs --sub-langs "en-US" \
    --convert-subs srt --skip-download --no-playlist \
    --output "$OUTPUT_TEMPLATE.%(ext)s" \
    "$URL" 2>/dev/null; then
    echo "SUBTITLE_TYPE: en"
else
    echo "ERROR: No subtitles could be downloaded"
    exit 1
fi

# Find downloaded SRT file
SRT_FILE=$(ls "$OUT_DIR"/${VIDEO_TITLE}.*.srt 2>/dev/null | head -1)
if [ -z "$SRT_FILE" ]; then
    echo "ERROR: SRT file not found after download"
    exit 1
fi

echo "SUBTITLE_FILE: $SRT_FILE"
echo "SUCCESS"
