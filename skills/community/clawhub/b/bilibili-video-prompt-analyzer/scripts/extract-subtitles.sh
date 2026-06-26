#!/bin/bash
# extract-subtitles.sh - Extract subtitles from Bilibili video
# Usage: ./extract-subtitles.sh <video-file> <output-text-file>
# Supports: soft subs (embedded in video) and hard subs (TODO: OCR not implemented yet)

set -euo pipefail

if [ $# -lt 2 ]; then
    echo "Usage: $0 <video-file> <output-text-file>"
    exit 1
fi

VIDEO_FILE="$1"
OUTPUT_FILE="$2"

echo "Extracting subtitles from: $VIDEO_FILE"
echo "Output to: $OUTPUT_FILE"

# Check if there are subtitle streams
SUB_STREAMS=$(ffprobe -v error -select_streams s -show_entries stream=index:stream_tags=language -of csv=p=0 "$VIDEO_FILE" || true)

if [ -z "$SUB_STREAMS" ]; then
    echo "No embedded subtitle streams found."
    echo "For hardsubs (subtitles burned into video), OCR extraction is not implemented in this version."
    echo "Creating empty output file..."
    touch "$OUTPUT_FILE"
    exit 0
fi

echo "Found subtitle streams:"
echo "$SUB_STREAMS"

# Get first subtitle stream (usually Chinese)
FIRST_SUB=$(echo "$SUB_STREAMS" | head -1 | cut -d',' -f1)

# Extract subtitles to SRT
ffmpeg -y -i "$VIDEO_FILE" -map 0:s:"$FIRST_SUB" "$OUTPUT_FILE.srt"

# Convert SRT to plain text
# Remove sequence numbers, timestamps, and empty lines
grep -v -E '^[0-9]+$|^[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{2}:[0-9]{2}:[0-9]{2} -->|^$' "$OUTPUT_FILE.srt" > "$OUTPUT_FILE"

# Cleanup
rm -f "$OUTPUT_FILE.srt"

LINE_COUNT=$(wc -l < "$OUTPUT_FILE")
echo "Subtitle extraction completed: $LINE_COUNT lines extracted to $OUTPUT_FILE"
