#!/bin/bash
# Coze Text-to-Speech Script
# Usage: ./text_to_speech.sh <text> [-o output_file] [-v voice_id] [-f format]

set -e

# Configuration
API_ENDPOINT="https://api.coze.cn/v1/audio/speech"

# Get API key from environment
if [ -z "$COZE_API_KEY" ]; then
    echo "Error: COZE_API_KEY environment variable is not set" >&2
    echo "" >&2
    echo "To fix:" >&2
    echo "1. Get a key from https://www.coze.cn/" >&2
    echo "2. Run: export COZE_API_KEY=\"your-key\"" >&2
    exit 1
fi

# Default values
VOICE_ID=6
OUTPUT_FORMAT="mp3"
OUTPUT_FILE=""

# Parse arguments
TEXT="$1"
shift || true

while [[ $# -gt 0 ]]; do
    case $1 in
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -v|--voice)
            VOICE_ID="$2"
            shift 2
            ;;
        -f|--format)
            OUTPUT_FORMAT="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 <text> [options]"
            echo ""
            echo "Options:"
            echo "  -o, --output    Output file path (default: auto-generated)"
            echo "  -v, --voice     Voice ID (default: 1)"
            echo "  -f, --format    Output format: mp3/ogg_opus/wav/pcm (default: mp3)"
            echo "  -h, --help      Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0 \"你好世界\""
            echo "  $0 \"你好\" -o greeting.mp3"
            echo "  $0 \"你好\" -v 2 -f wav"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Use -h or --help for usage information" >&2
            exit 1
            ;;
    esac
done

# Validate text
if [ -z "$TEXT" ]; then
    echo "Error: Text is required" >&2
    echo "Usage: $0 <text> [options]" >&2
    echo "Use -h or --help for more information" >&2
    exit 1
fi

# Generate output filename if not provided
if [ -z "$OUTPUT_FILE" ]; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    HASH=$(echo "$TEXT" | md5sum | cut -c1-8)
    OUTPUT_FILE="coze_tts_${TIMESTAMP}_${HASH}.${OUTPUT_FORMAT}"
fi

# Validate output format
case "$OUTPUT_FORMAT" in
    mp3|ogg_opus|wav|pcm)
        ;;
    opus)
        # Auto-convert opus to ogg_opus for API
        OUTPUT_FORMAT="ogg_opus"
        ;;
    *)
        echo "Error: Unsupported format '$OUTPUT_FORMAT'" >&2
        echo "Supported formats: mp3, ogg_opus, wav, pcm" >&2
        exit 1
        ;;
esac

# Make API request
echo "Generating speech..." >&2
if [ ${#TEXT} -gt 50 ]; then
    echo "  Text: $(echo "$TEXT" | cut -c1-50)..." >&2
else
    echo "  Text: $TEXT" >&2
fi
echo "  Voice ID: $VOICE_ID" >&2
echo "  Format: $OUTPUT_FORMAT" >&2
echo "" >&2

# Build JSON payload
JSON_PAYLOAD=$(jq -n \
    --arg input "$TEXT" \
    --argjson voice_id "$VOICE_ID" \
    --arg response_format "$OUTPUT_FORMAT" \
    '{
        input: $input,
        voice_id: $voice_id,
        response_format: $response_format
    }')

# Make API request and save response
HTTP_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$API_ENDPOINT" \
    -H "Authorization: Bearer $COZE_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$JSON_PAYLOAD" \
    -o "$OUTPUT_FILE")

HTTP_CODE=$(echo "$HTTP_RESPONSE" | tail -n1)

# Check for HTTP errors
if [ "$HTTP_CODE" != "200" ]; then
    echo "Error: API request failed with HTTP $HTTP_CODE" >&2
    
    # Try to parse error from response
    if [ -f "$OUTPUT_FILE" ]; then
        ERROR_MSG=$(cat "$OUTPUT_FILE" | jq -r '.msg // .error // "Unknown error"' 2>/dev/null || echo "")
        if [ -n "$ERROR_MSG" ]; then
            echo "Error message: $ERROR_MSG" >&2
        fi
        # Remove the error response file
        rm -f "$OUTPUT_FILE"
    fi
    exit 1
fi

# Check if file was created and has content
if [ ! -f "$OUTPUT_FILE" ] || [ ! -s "$OUTPUT_FILE" ]; then
    echo "Error: Failed to generate audio file" >&2
    exit 1
fi

# Get file size
FILE_SIZE=$(stat -c%s "$OUTPUT_FILE" 2>/dev/null || stat -f%z "$OUTPUT_FILE" 2>/dev/null || echo "0")
FILE_SIZE_KB=$(echo "scale=1; $FILE_SIZE / 1024" | bc 2>/dev/null || echo "$((FILE_SIZE / 1024))")

# Output success message
echo "✓ Audio saved: $OUTPUT_FILE"
echo "  Size: ${FILE_SIZE_KB} KB"

# Try to get audio duration if ffprobe is available
if command -v ffprobe > /dev/null 2>&1; then
    DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv="p=0" "$OUTPUT_FILE" 2>/dev/null || echo "")
    if [ -n "$DURATION" ]; then
        DURATION_SEC=$(echo "$DURATION" | cut -d. -f1)
        echo "  Duration: ~${DURATION_SEC} seconds"
    fi
fi
