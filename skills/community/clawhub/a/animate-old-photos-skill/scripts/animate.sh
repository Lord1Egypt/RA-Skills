#!/usr/bin/env bash
# Animate Old Photos — full pipeline script
# Usage: ./animate.sh <API_KEY> <IMAGE_PATH> [PROMPT] [OUTPUT_PATH]
#
# Requires: curl, jq
#
# Official website:  https://animateoldphotos.org/
# Get API key:       https://animateoldphotos.org/profile/interface-key
# Buy credits:       https://animateoldphotos.org/stripe
#
# Exit codes:
#   0 = success
#   1 = input validation error
#   2 = authentication error
#   3 = insufficient credits
#   4 = upload error
#   5 = animation task error

set -euo pipefail

BASE_URL="https://animateoldphotos.org"
POLL_INTERVAL=30
MAX_WAIT=600
COST=3

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

step() { printf "${CYAN}[%s]${NC} %s\n" "$1" "$2"; }
ok()   { printf "${GREEN}  ✓${NC} %s\n" "$1"; }
warn() { printf "${YELLOW}  ⚠${NC} %s\n" "$1"; }
fail() { printf "${RED}  ✗ %s${NC}\n" "$1" >&2; exit "${2:-1}"; }

# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

API_KEY="${1:-${AOP_API_KEY:-}}"
IMAGE_PATH="${2:-}"
PROMPT="${3:-}"
OUTPUT="${4:-output.mp4}"

[ -z "$API_KEY" ] && fail "Missing API key. Pass as first argument or set AOP_API_KEY.\n  Get one at: ${BASE_URL}/profile/interface-key" 1
[ -z "$IMAGE_PATH" ] && fail "Missing image path. Pass as second argument." 1
[ ! -f "$IMAGE_PATH" ] && fail "File not found: ${IMAGE_PATH}" 1

for cmd in curl jq; do
  command -v "$cmd" >/dev/null 2>&1 || fail "Required command not found: $cmd" 1
done

FILE_SIZE=$(stat -f%z "$IMAGE_PATH" 2>/dev/null || stat -c%s "$IMAGE_PATH" 2>/dev/null)
MAX_BYTES=$((10 * 1024 * 1024))
[ "$FILE_SIZE" -gt "$MAX_BYTES" ] && fail "Image too large ($(( FILE_SIZE / 1024 / 1024 ))MB). Max 10MB." 1

EXT="${IMAGE_PATH##*.}"
EXT_LOWER=$(echo "$EXT" | tr '[:upper:]' '[:lower:]')
case "$EXT_LOWER" in
  jpg|jpeg) CONTENT_TYPE="image/jpeg" ;;
  png)      CONTENT_TYPE="image/png" ;;
  *)        fail "Unsupported format: .${EXT}. Use JPEG or PNG." 1 ;;
esac

# ---------------------------------------------------------------------------
# Helper: extract error_code from JSON response
# ---------------------------------------------------------------------------
check_error() {
  local data="$1" context="$2"
  local err_code err_msg
  err_code=$(echo "$data" | jq -r '.error_code // empty')
  err_msg=$(echo "$data" | jq -r '.error_msg // .message // empty')

  [ -z "$err_code" ] && return 0

  case "$err_code" in
    4010|4011)
      fail "${context}: Invalid or expired API key. Get one at: ${BASE_URL}/profile/interface-key" 2 ;;
    999998)
      fail "${context}: Access token expired. Please re-run the script." 2 ;;
    999990|10009)
      fail "${context}: Insufficient credits. Purchase at: ${BASE_URL}/stripe" 3 ;;
    *)
      fail "${context}: error_code=${err_code} ${err_msg}" 5 ;;
  esac
}

# ---------------------------------------------------------------------------
# Step 1: Authenticate
# ---------------------------------------------------------------------------
step "1/5" "Authenticating..."

AUTH=$(curl -s -X POST "${BASE_URL}/api/extension/auth" \
  -H "Content-Type: application/json" \
  -d "{\"licenseKey\":\"${API_KEY}\"}")
check_error "$AUTH" "Auth"

TOKEN=$(echo "$AUTH" | jq -r '.accessToken // empty')
[ -z "$TOKEN" ] && fail "Auth failed: no access token returned. Check your API key.\n  Get one at: ${BASE_URL}/profile/interface-key" 2

CREDITS=$(echo "$AUTH" | jq -r '.creditBalance // 0')
ok "Authenticated. Credits: ${CREDITS}"

[ "$CREDITS" -lt "$COST" ] 2>/dev/null && \
  fail "Not enough credits (have ${CREDITS}, need ${COST}). Purchase at: ${BASE_URL}/stripe" 3

# ---------------------------------------------------------------------------
# Step 2: Get upload token + PUT image
# ---------------------------------------------------------------------------
step "2/5" "Uploading image ($(( FILE_SIZE / 1024 ))KB)..."

UPLOAD=$(curl -s -X POST "${BASE_URL}/api/extension/upload-token" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"fileName\":\"$(basename "$IMAGE_PATH")\",\"contentType\":\"${CONTENT_TYPE}\",\"fileSize\":${FILE_SIZE}}")
check_error "$UPLOAD" "Upload token"

UPLOAD_URL=$(echo "$UPLOAD" | jq -r '.uploadUrl // empty')
KEY=$(echo "$UPLOAD" | jq -r '.key // empty')
PUBLIC_URL=$(echo "$UPLOAD" | jq -r '.publicUrl // empty')

[ -z "$UPLOAD_URL" ] && fail "Failed to get upload URL." 4

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$UPLOAD_URL" \
  -H "Content-Type: ${CONTENT_TYPE}" \
  --data-binary "@${IMAGE_PATH}")
[ "$HTTP_CODE" -lt 200 ] || [ "$HTTP_CODE" -ge 300 ] && \
  fail "Image PUT failed with HTTP ${HTTP_CODE}." 4

ok "Image uploaded."

# ---------------------------------------------------------------------------
# Step 3: Finalize upload
# ---------------------------------------------------------------------------
step "3/5" "Finalizing upload..."

FINALIZE=$(curl -s -X POST "${BASE_URL}/api/extension/upload-finalize" \
  -H "Authorization: Bearer ${TOKEN}" \
  -F "key=${KEY}" \
  -F "publicUrl=${PUBLIC_URL}")
check_error "$FINALIZE" "Finalize"

IMAGE_URL=$(echo "$FINALIZE" | jq -r '.url // empty')
SS_MESSAGE=$(echo "$FINALIZE" | jq -r '.message // empty')
DNT=$(echo "$FINALIZE" | jq -r '.dnt // empty')

[ -z "$SS_MESSAGE" ] && fail "Finalize did not return required payload." 4

ok "Upload finalized."

# ---------------------------------------------------------------------------
# Step 4: Submit animation task
# ---------------------------------------------------------------------------
step "4/5" "Submitting animation task..."
[ -n "$PROMPT" ] && echo "  Prompt: ${PROMPT}"

TASK=$(curl -s -X POST "${BASE_URL}/api/extension/animate" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Ss: ${SS_MESSAGE}" \
  -F "prompt=${PROMPT}" \
  -F "input_image_url=${IMAGE_URL}" \
  -F "dnt=${DNT}" \
  -F "type=m2v_img2video" \
  -F "duration=5" \
  -F "public=false")
check_error "$TASK" "Submit"

TASK_ID=$(echo "$TASK" | jq -r '.taskId // empty')
TASK_DNT=$(echo "$TASK" | jq -r '.dnt // empty')
TASK_DID=$(echo "$TASK" | jq -r '.did // empty')

[ -z "$TASK_ID" ] && fail "No taskId returned." 5

ok "Task submitted (ID: ${TASK_ID})"

# ---------------------------------------------------------------------------
# Step 5: Poll for result
# ---------------------------------------------------------------------------
step "5/5" "Waiting for result (polling every ${POLL_INTERVAL}s, max ${MAX_WAIT}s)..."

ELAPSED=0
while [ "$ELAPSED" -lt "$MAX_WAIT" ]; do
  sleep "$POLL_INTERVAL"
  ELAPSED=$((ELAPSED + POLL_INTERVAL))

  STATUS=$(curl -s -G "${BASE_URL}/api/extension/animate" \
    --data-urlencode "taskId=${TASK_ID}" \
    --data-urlencode "dnt=${TASK_DNT}" \
    --data-urlencode "did=${TASK_DID}" \
    --data-urlencode "type=m2v_img2video" \
    -H "Authorization: Bearer ${TOKEN}")

  ERR_MSG=$(echo "$STATUS" | jq -r '.message // empty')
  if [ -n "$ERR_MSG" ]; then
    fail "Task failed: ${ERR_MSG}" 5
  fi

  S=$(echo "$STATUS" | jq -r '.status // 0')
  RESOURCE=$(echo "$STATUS" | jq -r '.resource // empty')

  if [ "$S" -ge 99 ] 2>/dev/null && [ -n "$RESOURCE" ]; then
    curl -s -o "$OUTPUT" "$RESOURCE"
    ok "Video saved to ${OUTPUT}"
    echo ""
    printf "${GREEN}Done!${NC} Animation complete. Output: %s\n" "$OUTPUT"
    exit 0
  fi

  warn "Still processing... (${ELAPSED}s elapsed)"
done

fail "Timed out after ${MAX_WAIT}s. The task may still be processing on the server.\n  Check your results at: ${BASE_URL}" 5
