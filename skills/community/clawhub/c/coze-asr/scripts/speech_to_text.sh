#!/bin/bash
# Coze Speech-to-Text Script
# Usage: ./speech_to_text.sh <audio_file> [language]

set -e

# Configuration
API_ENDPOINT="https://api.coze.cn/v1/audio/transcriptions"

# Get API key from environment
if [ -z "$COZE_API_KEY" ]; then
    echo "Error: COZE_API_KEY environment variable is not set" >&2
    echo "" >&2
    echo "To fix:" >&2
    echo "1. Get a key from https://www.coze.cn/" >&2
    echo "2. Run: export COZE_API_KEY=\"your-key\"" >&2
    exit 1
fi

# Parse arguments
AUDIO_FILE="$1"
LANGUAGE="${2:-zh}"

# Validate audio file
if [ -z "$AUDIO_FILE" ]; then
    echo "Usage: $0 <audio_file> [language]" >&2
    echo "" >&2
    echo "Examples:" >&2
    echo "  $0 recording.mp3" >&2
    echo "  $0 recording.wav en" >&2
    echo "" >&2
    echo "Supported formats: .mp3, .wav, .ogg" >&2
    exit 1
fi

# Check if file exists
if [ ! -f "$AUDIO_FILE" ]; then
    echo "Error: Audio file not found: $AUDIO_FILE" >&2
    exit 1
fi

# Check file format
FILE_EXT="${AUDIO_FILE##*.}"
FILE_EXT=$(echo "$FILE_EXT" | tr '[:upper:]' '[:lower:]')

# Supported formats: mp3, wav, ogg
if [ "$FILE_EXT" != "mp3" ] && [ "$FILE_EXT" != "wav" ] && [ "$FILE_EXT" != "ogg" ]; then
    echo "Warning: Format .$FILE_EXT may not be supported by Coze API" >&2
    echo "Supported formats: .mp3, .wav, .ogg" >&2
    echo "" >&2
fi

# Make API request using multipart/form-data
echo "Transcribing audio file: $AUDIO_FILE" >&2
echo "Language: $LANGUAGE" >&2
echo "" >&2

# Build curl command with multipart/form-data
RESPONSE=$(curl -s -X POST "$API_ENDPOINT" \
    -H "Authorization: Bearer $COZE_API_KEY" \
    -F "file=@$AUDIO_FILE" \
    -F "language=$LANGUAGE")

# Check for errors
if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
    ERROR_MSG=$(echo "$RESPONSE" | jq -r '.error.message // .error')
    echo "Error: $ERROR_MSG" >&2
    exit 1
fi

# Extract and display result
echo "$RESPONSE" | jq '.'

TRANSCRIBED_TEXT=$(echo "$RESPONSE" | jq -r '.data.text // .text // empty')

if [ -n "$TRANSCRIBED_TEXT" ]; then
    echo "" >&2
    echo "Transcribed text:" >&2
    echo "$TRANSCRIBED_TEXT" >&2
fi
