#!/bin/bash
# Upload video file to W3Stream (create + upload in one step)
# Usage: STREAM_PUBLIC_KEY=... STREAM_SECRET_KEY=... ./upload_video_file.sh FILE_PATH TITLE

PUBLIC_KEY="${STREAM_PUBLIC_KEY}"
SECRET_KEY="${STREAM_SECRET_KEY}"
INPUT_SOURCE="$1"
TITLE="$2"

is_video_extension() {
  local input="$1"
  local clean
  clean=$(echo "$input" | sed 's/[?#].*$//')
  case "${clean,,}" in
    *.mp4|*.mov|*.mkv|*.avi|*.webm|*.m4v|*.wmv|*.flv|*.mpg|*.mpeg|*.3gp|*.ts)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

is_video_mime() {
  local mime="$1"
  case "$mime" in
    video/*)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

if [ -z "$PUBLIC_KEY" ] || [ -z "$SECRET_KEY" ] || [ -z "$INPUT_SOURCE" ] || [ -z "$TITLE" ]; then
  echo "Usage: STREAM_PUBLIC_KEY=<key> STREAM_SECRET_KEY=<key> $0 FILE_PATH TITLE"
    exit 1
fi

WORK_FILE="$INPUT_SOURCE"

if [ ! -f "$WORK_FILE" ]; then
  echo "Error: File not found: $WORK_FILE"
  exit 1
fi

if ! is_video_extension "$WORK_FILE"; then
  if command -v file >/dev/null 2>&1; then
    MIME_FROM_FILE=$(file --mime-type -b "$WORK_FILE" 2>/dev/null)
    if [ -z "$MIME_FROM_FILE" ] || ! is_video_mime "$MIME_FROM_FILE"; then
      echo "Error: Input is not a video file (mime-type: ${MIME_FROM_FILE:-unknown})"
      exit 1
    fi
  else
    echo "Error: Input does not have a recognized video extension"
    exit 1
  fi
fi

# Step 1: Create video object
echo "Creating video object..."
CREATE_RESPONSE=$(curl -s -X POST 'https://api.aiozstream.network/api/media/create' \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H 'Content-Type: application/json' \
  -d "{
    \"title\": \"$TITLE\",
    \"type\": \"video\"
  }")

# Extract video ID
VIDEO_ID=$(echo "$CREATE_RESPONSE" | jq -r '.data.id')

if [ "$VIDEO_ID" == "null" ] || [ -z "$VIDEO_ID" ]; then
    echo "Error creating video object:"
    echo "$CREATE_RESPONSE"
    exit 1
fi

echo "Video object created with ID: $VIDEO_ID"

# Step 2: Calculate file size and MD5 hash
echo "Calculating file size and hash..."
FILE_SIZE=$(stat -f%z "$WORK_FILE" 2>/dev/null || stat -c%s "$WORK_FILE")
END_POS=$((FILE_SIZE - 1))
HASH=$(md5sum "$WORK_FILE" | awk '{print $1}')

echo "File size: $FILE_SIZE bytes"
echo "MD5 hash: $HASH"

# Step 3: Upload the file using multipart form-data with Content-Range header
echo "Uploading file..."
UPLOAD_RESPONSE=$(curl -s -X POST "https://api.aiozstream.network/api/media/$VIDEO_ID/part" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY" \
  -H "Content-Range: bytes 0-$END_POS/$FILE_SIZE" \
  -F "file=@$WORK_FILE" \
  -F "index=0" \
  -F "hash=$HASH")

echo "Upload response:"
echo "$UPLOAD_RESPONSE" | jq '.'

# Step 4: Complete the upload to trigger transcoding
echo ""
echo "Completing upload..."
COMPLETE_RESPONSE=$(curl -s -X GET "https://api.aiozstream.network/api/media/$VIDEO_ID/complete" \
  -H 'accept: application/json' \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY")

echo "Complete response:"
echo "$COMPLETE_RESPONSE" | jq '.'

# Step 5: Get final video details
echo ""
echo "Fetching video details..."
sleep 2
DETAIL_RESPONSE=$(curl -s "https://api.aiozstream.network/api/media/$VIDEO_ID" \
  -H "stream-public-key: $PUBLIC_KEY" \
  -H "stream-secret-key: $SECRET_KEY")

echo ""
echo "=== Final Video Details ==="
echo "$DETAIL_RESPONSE" | jq '.'

# Extract and display URLs
HLS_URL=$(echo "$DETAIL_RESPONSE" | jq -r '.data.assets.hls_url // .data.assets.hls // empty')
HLS_PLAYER_URL=$(echo "$DETAIL_RESPONSE" | jq -r '.data.assets.hls_player_url // empty')
MP4_URL=$(echo "$DETAIL_RESPONSE" | jq -r '.data.assets.mp4_url // empty')
STATUS=$(echo "$DETAIL_RESPONSE" | jq -r '.data.status // empty')

echo ""
echo "=== Upload Status ==="
echo "Status: $STATUS"

if [ -n "$HLS_PLAYER_URL" ]; then
    echo ""
  echo "=== Video Player URL (Click to Play) ==="
    echo "$HLS_PLAYER_URL"
fi

if [ -n "$HLS_URL" ]; then
    echo ""
    echo "=== HLS Manifest URL (for developers) ==="
    echo "$HLS_URL"
fi

if [ -n "$MP4_URL" ]; then
  echo ""
  echo "=== MP4 URL ==="
  echo "$MP4_URL"
fi

if [ "$STATUS" == "transcoding" ]; then
    echo ""
  echo "Note: Video is still transcoding. Check back later for the streaming URL."
elif [ -z "$HLS_PLAYER_URL" ] && [ -z "$HLS_URL" ] && [ -z "$MP4_URL" ]; then
    echo ""
  echo "Note: No streaming URLs available yet. The video may still be processing."
fi

