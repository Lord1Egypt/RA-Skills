#!/bin/bash
# Download images from a Toutiao article with anti-hotlink bypass
# Usage: download_images.sh <toutiao_url> <output_dir>
#
# Features:
# - Automatically extracts image URLs from article
# - Downloads with Referer header (anti-hotlink bypass)
# - Names files sequentially (01.jpg, 02.png, ...)

set -e

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: download_images.sh <toutiao_url> <output_dir>"
    echo "Example: download_images.sh 'https://m.toutiao.com/is/m3EX1m0Z3Mo/' /tmp/article-images/"
    exit 1
fi

URL="$1"
OUTPUT_DIR="$2"
JINA_API="https://r.jina.ai/"
REFERER="https://www.toutiao.com/"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Fetching article content..."
CONTENT=$(curl -sL "${JINA_API}${URL}" 2>/dev/null)

# Extract image URLs
IMAGE_URLS=$(echo "$CONTENT" | grep -oE 'https?://[^)"'\'' ]+\.(jpg|jpeg|png|gif|webp)' | sort -u)

if [ -z "$IMAGE_URLS" ]; then
    echo "No images found in the article."
    exit 0
fi

# Count images
TOTAL=$(echo "$IMAGE_URLS" | wc -l)
echo "Found $TOTAL images. Downloading..."

# Download images with Referer header
i=1
for IMG_URL in $IMAGE_URLS; do
    # Extract extension
    EXT="${IMG_URL##*.}"
    # Handle query parameters in extension
    EXT=$(echo "$EXT" | cut -d'?' -f1)
    
    # Format filename with zero-padding
    printf -v FILENAME "%02d.%s" $i "$EXT"
    FILEPATH="${OUTPUT_DIR}/${FILENAME}"
    
    echo "[$i/$TOTAL] Downloading: $FILENAME"
    
    # Download with Referer header (anti-hotlink bypass)
    curl -sL -H "Referer: $REFERER" "$IMG_URL" -o "$FILEPATH"
    
    # Check if download succeeded
    if [ -f "$FILEPATH" ]; then
        SIZE=$(stat -c%s "$FILEPATH" 2>/dev/null || stat -f%z "$FILEPATH" 2>/dev/null || echo "unknown")
        echo "  Size: $SIZE bytes"
    else
        echo "  Failed to download!"
    fi
    
    ((i++))
done

echo ""
echo "Download complete. Files saved to: $OUTPUT_DIR"
ls -la "$OUTPUT_DIR"