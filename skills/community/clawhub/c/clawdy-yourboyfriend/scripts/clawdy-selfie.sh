#!/bin/bash
# Clawdy images must ALWAYS be generated from the same male reference image.
# Uses fal.ai xAI Grok Imagine EDIT endpoint only. No text-to-image fallback.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

if [ -z "${FAL_KEY:-}" ]; then
  log_error "FAL_KEY environment variable not set"
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  log_error "jq is required but not installed"
  exit 1
fi

PROMPT_RAW="${1:-}"
CHANNEL="${2:-}"
CAPTION="${3:-For you}"
OUTPUT_FORMAT="${4:-jpeg}"

if [ -z "$PROMPT_RAW" ] || [ -z "$CHANNEL" ]; then
  echo "Usage: $0 <prompt> <channel> [caption] [output_format]"
  exit 1
fi

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REFERENCE_PATH="$SKILL_DIR/assets/clawdy.png"

if [ ! -f "$REFERENCE_PATH" ]; then
  log_error "Reference image missing: $REFERENCE_PATH"
  exit 1
fi

BASE_LOCK="same exact person as the reference image; preserve the exact same male identity, same face, same eyes, same nose, same eyebrows, same hairstyle, same skin tone, same jawline, same facial structure, same age, same vibe. clearly male. handsome young man. do not change identity. do not feminize. not female. not woman. not a different model. not a different person."

MODE="direct"
shopt -s nocasematch
if [[ "$PROMPT_RAW" =~ outfit|wearing|jacket|hoodie|suit|mirror|full-body|fashion ]]; then
  MODE="mirror"
fi
shopt -u nocasematch

if [ "$MODE" = "mirror" ]; then
  EDIT_PROMPT="Edit this SAME exact person into a mirror selfie. ${BASE_LOCK} Requested variation: ${PROMPT_RAW}. Keep it realistic and tasteful."
else
  EDIT_PROMPT="Edit this SAME exact person into a direct selfie. ${BASE_LOCK} Requested variation: ${PROMPT_RAW}. Keep it realistic and tasteful."
fi

DATA_URL=$(python3 - <<'PY' "$REFERENCE_PATH"
import base64, mimetypes, sys
p = sys.argv[1]
mime = mimetypes.guess_type(p)[0] or 'image/jpeg'
with open(p, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('ascii')
print(f'data:{mime};base64,{b64}')
PY
)

JSON_PAYLOAD=$(jq -n \
  --arg image_url "$DATA_URL" \
  --arg prompt "$EDIT_PROMPT" \
  --arg output_format "$OUTPUT_FORMAT" \
  '{image_url: $image_url, prompt: $prompt, num_images: 1, output_format: $output_format}')

RESPONSE=$(curl -fsSL -X POST "https://fal.run/xai/grok-imagine-image/edit" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD")

if echo "$RESPONSE" | jq -e '.error // .detail' >/dev/null 2>&1; then
  ERROR_MSG=$(echo "$RESPONSE" | jq -r '.error // .detail // "Unknown error"')
  log_error "Reference-edit generation failed: $ERROR_MSG"
  exit 1
fi

IMAGE_URL=$(echo "$RESPONSE" | jq -r '.images[0].url // empty')
if [ -z "$IMAGE_URL" ]; then
  log_error "Failed to extract image URL from response"
  echo "$RESPONSE"
  exit 1
fi

EXT="$OUTPUT_FORMAT"
if [ "$EXT" = "jpeg" ]; then EXT="jpg"; fi
LOCAL_FILE="${TMPDIR:-/tmp}/clawdy-selfie-$(date +%s)-$$.$EXT"

log_info "Downloading edited image to local file: $LOCAL_FILE"
curl -fsSL "$IMAGE_URL" -o "$LOCAL_FILE"

if [ ! -s "$LOCAL_FILE" ]; then
  log_error "Downloaded local file is empty"
  exit 1
fi

log_info "Sending local file via OpenClaw"
openclaw message send \
  --action send \
  --channel "$CHANNEL" \
  --message "$CAPTION" \
  --filePath "$LOCAL_FILE"

log_info "Done"
jq -n \
  --arg image_url "$IMAGE_URL" \
  --arg local_file "$LOCAL_FILE" \
  --arg channel "$CHANNEL" \
  --arg mode "$MODE" \
  '{success:true,image_url:$image_url,local_file:$local_file,channel:$channel,mode:$mode}'
