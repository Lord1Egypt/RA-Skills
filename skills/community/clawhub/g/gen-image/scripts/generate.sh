#!/bin/bash
# Generate image via SiliconFlow API

API_KEY="${SILICONFLOW_API_KEY}"
MODEL="${MODEL:-Kolors/Kolors}"
PROMPT="$1"
OUTPUT="${2:-/tmp/siliconflow-image.png}"
SIZE="${SIZE:-1024x1024}"

if [ -z "$API_KEY" ]; then
    echo "Error: SILICONFLOW_API_KEY not set"
    exit 1
fi

if [ -z "$PROMPT" ]; then
    echo "Usage: $0 <prompt> [output_file]"
    exit 1
fi

echo "Generating image with $MODEL..."
echo "Prompt: $PROMPT"

RESPONSE=$(curl -s -X POST "https://api.siliconflow.cn/v1/images/generations" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
        \"model\": \"$MODEL\",
        \"prompt\": \"$PROMPT\",
        \"image_size\": \"$SIZE\",
        \"num_inference_steps\": 20
    }")

# Check for error
if echo "$RESPONSE" | grep -q '"error"'; then
    echo "API Error: $(echo "$RESPONSE" | jq -r '.error.message // .error')"
    exit 1
fi

# Extract image URL
IMAGE_URL=$(echo "$RESPONSE" | jq -r '.images[0].url // empty')

if [ -z "$IMAGE_URL" ]; then
    echo "Error: No image URL in response"
    echo "$RESPONSE"
    exit 1
fi

echo "Downloading image from: $IMAGE_URL"
curl -s -o "$OUTPUT" "$IMAGE_URL"

if [ -f "$OUTPUT" ]; then
    echo "Image saved: $OUTPUT"
    echo "MEDIA: $OUTPUT"
else
    echo "Error: Failed to download image"
    exit 1
fi