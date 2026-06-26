#!/bin/bash
# extract-frames.sh - Extract frames from video for analysis
# Usage: ./extract-frames.sh <video-file> <output-dir> [fps]
# Default fps: 1 (one frame per second)

set -euo pipefail

if [ $# -lt 2 ]; then
    echo "Usage: $0 <video-file> <output-dir> [fps]"
    echo "Default fps: 1"
    exit 1
fi

VIDEO_FILE="$1"
OUT_DIR="$2"
FPS="${3:-1}"

mkdir -p "$OUT_DIR"

echo "Extracting frames from: $VIDEO_FILE"
echo "Output directory: $OUT_DIR"
echo "FPS: $FPS"

# Get video info
ffmpeg -i "$VIDEO_FILE" 2>&1 | grep -E "Duration|Input #|Stream #.*Video"

# Extract frames
# Output as JPEG with quality 2, scaled to max width 1280px
ffmpeg -y -i "$VIDEO_FILE" -vf "fps=$FPS,scale='min(1280,iw)':-2" -q:v 2 "$OUT_DIR/frame%04d.jpg"

FRAME_COUNT=$(ls -1 "$OUT_DIR"/frame*.jpg 2>/dev/null | wc -l)
echo "Extraction completed: $FRAME_COUNT frames extracted"
