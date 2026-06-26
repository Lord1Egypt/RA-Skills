#!/bin/bash
# Get comprehensive audio metadata

set -e

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <audio_file>"
    exit 1
fi

AUDIO="$1"

if [[ ! -f "$AUDIO" ]]; then
    echo "Error: Audio file not found: $AUDIO" >&2
    exit 1
fi

echo "=== Audio: $AUDIO ==="
echo ""

# File info
echo "--- File ---"
ls -lh "$AUDIO" | awk '{print "Size:", $5}'
echo ""

# Format info
echo "--- Format ---"
ffprobe -v quiet -print_format json -show_format "$AUDIO" 2>/dev/null | \
    jq -r '.format | "Format: \(.format_long // .format_name)\nDuration: \(.duration)s\nBitrate: \(.bit_rate)b/s\n" // "Could not read format info"'

# Stream info
echo "--- Audio Stream ---"
ffprobe -v quiet -print_format json -show_streams -select_streams a "$AUDIO" 2>/dev/null | \
    jq -r '.streams[0] | "Codec: \(.codec_name // "unknown")\nSample Rate: \(.sample_rate // "unknown") Hz\nChannels: \(.channels // "unknown")\nChannel Layout: \(.channel_layout // "unknown")\nBit Rate: \(.bit_rate // "unknown") b/s"' 2>/dev/null || echo "Could not read stream info"

# Tags
echo ""
echo "--- Tags ---"
ffprobe -v quiet -print_format json -show_format "$AUDIO" 2>/dev/null | \
    jq -r '.format.tags | to_entries[] | "\(.key): \(.value)"' 2>/dev/null || echo "No tags found"