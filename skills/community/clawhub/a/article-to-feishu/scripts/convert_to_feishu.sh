#!/bin/bash
# Convert a Toutiao article to Feishu document with images
# This is a template script showing the workflow
#
# IMPORTANT: This script requires the feishu MCP tools which can only be called
# from the AI agent, not from shell scripts directly. Use this as a reference.
#
# Workflow:
# 1. Download images locally
# 2. Create document with title
# 3. Append text + insert images alternately
#
# Usage (from AI agent):
#   1. Call download_images.sh to get images
#   2. Call fetch_article.sh to get content
#   3. Use feishu_create_doc and feishu_update_doc to build document
#   4. Use feishu_doc_media to insert images

set -e

if [ -z "$1" ]; then
    echo "Toutiao to Feishu Document Converter"
    echo ""
    echo "Usage: convert_to_feishu.sh <toutiao_url>"
    echo ""
    echo "This script demonstrates the conversion workflow."
    echo "Actual conversion must be done by AI agent using feishu tools."
    echo ""
    echo "Steps:"
    echo "  1. Download images: bash download_images.sh <url> /tmp/article-img/"
    echo "  2. Fetch content:   bash fetch_article.sh <url>"
    echo "  3. Create doc:      feishu_create_doc title='...' markdown='...'"
    echo "  4. Append text:     feishu_update_doc mode=append markdown='...'"
    echo "  5. Insert image:    feishu_doc_media action=insert file_path='...'"
    echo "  6. Repeat 4-5 until done"
    echo ""
    echo "Example workflow in AI agent:"
    echo ""
    echo "  # Step 1: Download images"
    echo "  bash download_images.sh '\$URL' /tmp/article-img/"
    echo ""
    echo "  # Step 2: Create document with title"
    echo "  feishu_create_doc title='Article Title' markdown='Introduction...'"
    echo ""
    echo "  # Step 3: Append section 1 text"
    echo "  feishu_update_doc doc_id='xxx' mode=append markdown='## Section 1\n\nContent...'"
    echo ""
    echo "  # Step 4: Insert section 1 image"
    echo "  feishu_doc_media action=insert doc_id='xxx' file_path='/tmp/article-img/01.jpg' type=image"
    echo ""
    echo "  # Step 5: Continue with more sections..."
    echo ""
    echo "  # Step 6: Cleanup"
    echo "  rm -rf /tmp/article-img/"
    exit 0
fi

URL="$1"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "=== Toutiao Article to Feishu Document ==="
echo ""
echo "URL: $URL"
echo ""

# Step 1: Download images
TEMP_DIR=$(mktemp -d)
echo "[Step 1] Downloading images to: $TEMP_DIR"
bash "$SCRIPT_DIR/download_images.sh" "$URL" "$TEMP_DIR"

# Step 2: Fetch content
echo ""
echo "[Step 2] Fetching article content..."
CONTENT=$(bash "$SCRIPT_DIR/fetch_article.sh" "$URL")

# Extract title (first line usually contains "Title: ...")
TITLE=$(echo "$CONTENT" | grep -m1 "^Title:" | sed 's/^Title: //')
if [ -z "$TITLE" ]; then
    TITLE="Imported Article"
fi

echo "Title: $TITLE"

# Count images
IMAGE_COUNT=$(ls -1 "$TEMP_DIR"/*.{jpg,png,gif,webp,jpeg} 2>/dev/null | wc -l)
echo "Images: $IMAGE_COUNT"

echo ""
echo "=== Next Steps (AI Agent) ==="
echo ""
echo "The article content and images are ready. AI agent should now:"
echo ""
echo "1. Create document:"
echo "   feishu_create_doc title='$TITLE' markdown='...'"
echo ""
echo "2. For each image in $TEMP_DIR:"
echo "   - Append text before the image"
echo "   - Insert the image with feishu_doc_media"
echo ""
echo "3. Cleanup after done:"
echo "   rm -rf $TEMP_DIR"
echo ""
echo "=== Article Content Preview ==="
echo "$CONTENT" | head -50
echo ""
echo "... (truncated)"