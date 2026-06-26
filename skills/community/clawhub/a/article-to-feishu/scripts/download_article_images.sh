#!/bin/bash
# Download images from a web article with anti-hotlink bypass
# Usage: download_article_images.sh <article_url> <output_dir> [referer]
#
# Features:
# - Auto-detect referer based on URL
# - Download images sequentially
# - Support multiple image hosts
#
# Examples:
#   download_article_images.sh "https://www.cnblogs.com/xxx/p/123" /tmp/img/
#   download_article_images.sh "https://m.toutiao.com/is/xxx/" /tmp/img/
#   download_article_images.sh "https://example.com/article" /tmp/img/ "https://example.com/"

set -e

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: download_article_images.sh <article_url> <output_dir> [referer]"
    echo ""
    echo "Examples:"
    echo "  download_article_images.sh 'https://www.cnblogs.com/xxx/p/123' /tmp/img/"
    echo "  download_article_images.sh 'https://m.toutiao.com/is/xxx/' /tmp/img/"
    exit 1
fi

URL="$1"
OUTPUT_DIR="$2"
CUSTOM_REFERER="$3"

# Auto-detect referer based on URL domain
detect_referer() {
    local url="$1"
    
    if [[ "$url" == *"cnblogs.com"* ]]; then
        echo "https://www.cnblogs.com/"
    elif [[ "$url" == *"toutiao.com"* ]]; then
        echo "https://www.toutiao.com/"
    elif [[ "$url" == *"csdn.net"* ]]; then
        echo "https://blog.csdn.net/"
    elif [[ "$url" == *"weixin.qq.com"* ]]; then
        echo "https://mp.weixin.qq.com/"
    elif [[ "$url" == *"jianshu.com"* ]]; then
        echo "https://www.jianshu.com/"
    elif [[ "$url" == *"zhihu.com"* ]]; then
        echo "https://zhuanlan.zhihu.com/"
    else
        # Extract domain from URL
        echo "https://$(echo "$url" | sed -E 's|https?://([^/]+).*|\1|')/"
    fi
}

# Determine referer
if [ -n "$CUSTOM_REFERER" ]; then
    REFERER="$CUSTOM_REFERER"
else
    REFERER=$(detect_referer "$URL")
fi

echo "Article URL: $URL"
echo "Output Dir: $OUTPUT_DIR"
echo "Referer: $REFERER"
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Fetch HTML content
echo "Fetching page content..."
HTML=$(curl -sL "$URL" 2>/dev/null)

# Extract image URLs
# Common patterns:
# - img src="..."
# - data-src="..." (lazy load)
# - background-image: url(...)
IMAGE_URLS=$(echo "$HTML" | grep -oE '(https?://[^"'\''()<>]+\.(jpg|jpeg|png|gif|webp))' | sort -u | head -50)

if [ -z "$IMAGE_URLS" ]; then
    echo "No images found in the article."
    exit 0
fi

# Count images
TOTAL=$(echo "$IMAGE_URLS" | wc -l)
echo "Found $TOTAL images."
echo ""

# Download images
i=1
for IMG_URL in $IMAGE_URLS; do
    # Skip common non-content images (icons, avatars, ads)
    if [[ "$IMG_URL" == *"avatar"* ]] || \
       [[ "$IMG_URL" == *"icon"* ]] || \
       [[ "$IMG_URL" == *"logo"* ]] || \
       [[ "$IMG_URL" == *"ad/"* ]] || \
       [[ "$IMG_URL" == *"advertisement"* ]]; then
        echo "[$i/$TOTAL] Skipping (icon/avatar/ad): $(basename "$IMG_URL" | cut -c1-30)..."
        ((i++))
        continue
    fi
    
    # Extract extension
    EXT="${IMG_URL##*.}"
    EXT=$(echo "$EXT" | cut -d'?' -f1 | tr '[:upper:]' '[:lower:]')
    
    # Default to jpg if no extension
    if [ -z "$EXT" ] || [ ${#EXT} -gt 5 ]; then
        EXT="jpg"
    fi
    
    # Format filename with zero-padding
    printf -v FILENAME "%02d.%s" $i "$EXT"
    FILEPATH="${OUTPUT_DIR}/${FILENAME}"
    
    echo "[$i/$TOTAL] Downloading: $FILENAME"
    
    # Download with Referer header
    HTTP_CODE=$(curl -sL -w "%{http_code}" -H "Referer: $REFERER" "$IMG_URL" -o "$FILEPATH" 2>/dev/null)
    
    # Check result
    if [ -f "$FILEPATH" ]; then
        SIZE=$(stat -c%s "$FILEPATH" 2>/dev/null || stat -f%z "$FILEPATH" 2>/dev/null || echo 0)
        if [ "$SIZE" -gt 1000 ]; then
            echo "  ✓ Size: $SIZE bytes"
        else
            echo "  ⚠ Small file ($SIZE bytes), might be placeholder"
        fi
    else
        echo "  ✗ Failed (HTTP $HTTP_CODE)"
    fi
    
    ((i++))
done

echo ""
echo "=== Download Complete ==="
echo "Files saved to: $OUTPUT_DIR"
echo ""
ls -la "$OUTPUT_DIR" 2>/dev/null | tail -n +2 | wc -l | xargs echo "Total files:"