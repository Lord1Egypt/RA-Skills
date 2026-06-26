#!/bin/bash
# Convert audio file to OPUS format for Feishu voice messages
# Usage: ./convert-audio.sh <input-file> [output-file]

set -e

INPUT_FILE="$1"
OUTPUT_FILE="${2:-${INPUT_FILE%.*}.opus}"

if [ -z "$INPUT_FILE" ]; then
    echo "Usage: $0 <input-file> [output-file]"
    echo ""
    echo "Examples:"
    echo "  $0 voice.mp3              # Creates voice.opus"
    echo "  $0 voice.mp3 output.opus  # Creates output.opus"
    exit 1
fi

if [ ! -f "$INPUT_FILE" ]; then
    echo "❌ Error: File not found: $INPUT_FILE"
    exit 1
fi

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ Error: ffmpeg is not installed"
    echo "Install with: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
    exit 1
fi

echo "🎵 Converting audio to OPUS format..."
echo "   Input: $INPUT_FILE"
echo "   Output: $OUTPUT_FILE"

# Convert to OPUS
ffmpeg -i "$INPUT_FILE" -c:a libopus -b:a 32k -y "$OUTPUT_FILE" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Conversion complete!"
    
    # Get duration using ffprobe
    if command -v ffprobe &> /dev/null; then
        DURATION=$(ffprobe -v quiet -show_format -print_format json "$INPUT_FILE" | grep '"duration"' | sed 's/.*: "\([^"]*\)".*/\1/')
        DURATION_MS=$(echo "$DURATION * 1000" | bc | cut -d. -f1)
        echo ""
        echo "📊 Audio info:"
        echo "   Duration: ${DURATION}s (${DURATION_MS}ms)"
        echo ""
        echo "💡 Use this duration when sending:"
        echo "   node scripts/send-voice.mjs --duration $DURATION_MS ..."
    fi
else
    echo "❌ Conversion failed"
    exit 1
fi
