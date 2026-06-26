#!/usr/bin/env bash
# fetch-feishu-images.sh — 从飞书文档 markdown 中提取所有图片 token，下载并输出 assets JSON
#
# Usage:
#   ./scripts/fetch-feishu-images.sh <doc_token_or_url>
#
# Output (stdout): JSON array，可直接作为 publish 请求的 assets 字段
# Logs (stderr): 下载进度和错误信息
#
# Example:
#   ASSETS=$(./scripts/fetch-feishu-images.sh B3Gmd1R9sop8LExGkqzc23jmnMb)
#   # Then use $ASSETS in your publish request body

set -euo pipefail

INPUT="${1:?Usage: $0 <doc_token_or_url>}"

# Extract doc token from URL or raw token
DOC_TOKEN=$(echo "$INPUT" | grep -oP '(?:wiki|docx)/\K[A-Za-z0-9]+' || echo "$INPUT")

WORK_DIR="/tmp/feishu-images-${DOC_TOKEN}"
rm -rf "$WORK_DIR"
mkdir -p "$WORK_DIR"

# Step 1: Fetch document markdown
>&2 echo "[1/3] Fetching document markdown..."
MD_JSON=$(lark-cli docs +fetch --doc "$DOC_TOKEN" --format json 2>/dev/null)
MARKDOWN=$(echo "$MD_JSON" | python3 -c "
import json, sys
output = sys.stdin.read()
start = output.find('{')
end = output.rfind('}')
if start >= 0 and end >= 0:
    d = json.loads(output[start:end+1])
    md = d.get('data',{}).get('markdown','') or d.get('markdown','') or ''
    print(md)
")

if [ -z "$MARKDOWN" ]; then
    >&2 echo "ERROR: Failed to fetch document markdown"
    echo "[]"
    exit 1
fi

# Step 2: Extract image tokens
TOKENS=$(echo "$MARKDOWN" | grep -oP '<image\s+token="\K[^"]+' || true)
TOKEN_COUNT=$(echo "$TOKENS" | grep -c . || echo 0)

if [ "$TOKEN_COUNT" -eq 0 ]; then
    >&2 echo "No image tokens found in document."
    echo "[]"
    exit 0
fi

>&2 echo "[2/3] Found $TOKEN_COUNT image tokens. Downloading..."

# Step 3: Download each image and build assets JSON
ASSETS="["
FIRST=true
SUCCESS=0
FAILED=0

while IFS= read -r token; do
    [ -z "$token" ] && continue
    
    >&2 echo "  Downloading $token..."
    
    DOWNLOAD_RESULT=$(cd "$WORK_DIR" && lark-cli docs +media-download --token "$token" --output "./$token" --overwrite 2>/dev/null || echo '{"ok":false}')
    
    # Parse saved_path from result
    SAVED_PATH=$(echo "$DOWNLOAD_RESULT" | python3 -c "
import json, sys, os
output = sys.stdin.read()
start = output.find('{')
end = output.rfind('}')
if start >= 0 and end >= 0:
    d = json.loads(output[start:end+1])
    sp = d.get('data',{}).get('saved_path','')
    if sp and not os.path.isabs(sp):
        sp = os.path.join('$WORK_DIR', sp)
    print(sp)
" 2>/dev/null)
    
    if [ -z "$SAVED_PATH" ] || [ ! -f "$SAVED_PATH" ]; then
        >&2 echo "  ⚠ Failed to download $token, skipping"
        FAILED=$((FAILED + 1))
        continue
    fi
    
    # Detect mime type
    MIME=$(file -b --mime-type "$SAVED_PATH" 2>/dev/null || echo "image/png")
    EXT="${SAVED_PATH##*.}"
    FILENAME="${token}.${EXT}"
    
    # Base64 encode
    B64=$(base64 -w 0 "$SAVED_PATH")
    
    if [ "$FIRST" = true ]; then
        FIRST=false
    else
        ASSETS="${ASSETS},"
    fi
    
    ASSETS="${ASSETS}{\"id\":\"${token}\",\"kind\":\"image\",\"filename\":\"${FILENAME}\",\"mimeType\":\"${MIME}\",\"data\":\"${B64}\"}"
    SUCCESS=$((SUCCESS + 1))
    >&2 echo "  ✓ $token ($(du -h "$SAVED_PATH" | cut -f1))"
    
done <<< "$TOKENS"

ASSETS="${ASSETS}]"

>&2 echo "[3/3] Done. $SUCCESS/$TOKEN_COUNT images downloaded ($FAILED failed)."

# Output the JSON array
echo "$ASSETS"
