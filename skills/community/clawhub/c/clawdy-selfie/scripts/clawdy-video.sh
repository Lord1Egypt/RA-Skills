#!/bin/bash
# clawdy-video.sh
# Generate a Clawdy selfie VIDEO using Seedance 2.0 API + reference image.
# Uses the same male reference as clawdy-selfie.sh.

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# --- Config ---
SEEDANCE_API_KEY="${SEEDANCE_API_KEY:-}"
SEEDANCE_BASE_URL="${SEEDANCE_BASE_URL:-https://api.outai.top/api}"
REFERENCE_PUBLIC_URL="${CLAWDY_REFERENCE_URL:-}"
CREATE_RETRIES="${SEEDANCE_CREATE_RETRIES:-3}"
POLL_INTERVAL="${SEEDANCE_POLL_INTERVAL:-60}"
MAX_POLLS="${SEEDANCE_MAX_POLLS:-20}"
FALLBACK_MODELS_CSV="${SEEDANCE_FALLBACK_MODELS:-seedance_2_0_fast,seedance_2_0}"

if [ -z "$SEEDANCE_API_KEY" ]; then
  log_error "SEEDANCE_API_KEY environment variable not set"
  exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
  log_error "jq is required but not installed"
  exit 1
fi

# --- Args ---
PROMPT_RAW="${1:-}"
CHANNEL="${2:-}"
CAPTION="${3:-Here is a video for you}"
DURATION="${4:-5}"
RATIO="${5:-9:16}"
MODEL="${6:-seedance_2_0_fast}"

if [ -z "$PROMPT_RAW" ] || [ -z "$CHANNEL" ]; then
  echo "Usage: $0 <prompt> <channel> [caption] [duration] [ratio] [model]"
  echo "  duration: 4-15 (default 5)"
  echo "  ratio: 16:9 | 9:16 | 1:1 | 4:3 | 3:4 | 21:9 (default 9:16)"
  echo "  model: seedance_2_0 | seedance_2_0_fast (default seedance_2_0_fast)"
  exit 1
fi

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REFERENCE_PATH="$SKILL_DIR/assets/clawdy.png"

if [ ! -f "$REFERENCE_PATH" ]; then
  log_error "Reference image missing: $REFERENCE_PATH"
  exit 1
fi

upload_reference_image() {
  if [ -n "$REFERENCE_PUBLIC_URL" ]; then
    log_info "Using provided public reference URL"
    echo "$REFERENCE_PUBLIC_URL"
    return 0
  fi

  log_info "Uploading reference image to get public URL..."

  local upload_resp=""
  local image_url=""

  if [ -z "$image_url" ]; then
    log_info "Using file.io for temporary image hosting..."
    upload_resp=$(curl -fsSL -X POST "https://file.io" -F "file=@$REFERENCE_PATH" 2>/dev/null || echo "")
    image_url=$(echo "$upload_resp" | jq -r '.link // empty' 2>/dev/null || echo "")
  fi

  if [ -z "$image_url" ]; then
    log_info "Trying 0x0.st for image hosting..."
    image_url=$(curl -fsSL -X POST "https://0x0.st" -F "file=@$REFERENCE_PATH" 2>/dev/null || echo "")
    image_url=$(echo "$image_url" | tr -d '\r')
  fi

  if [ -z "$image_url" ]; then
    return 1
  fi

  echo "$image_url"
}

create_task_once() {
  local model="$1"
  local image_url="$2"
  local video_prompt="$3"

  curl -fsSL -X POST "${SEEDANCE_BASE_URL}/v1/video/seedance-2" \
    -H "Authorization: Bearer $SEEDANCE_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$(jq -n \
      --arg model "$model" \
      --arg prompt "$video_prompt" \
      --arg ratio "$RATIO" \
      --argjson duration "$DURATION" \
      --arg img "$image_url" \
      '{model:$model,prompt:$prompt,function_mode:"omni_reference",ratio:$ratio,duration:$duration,image_urls:[$img],audio_urls:[],video_urls:[]}')"
}

create_task_with_retry() {
  local model="$1"
  local image_url="$2"
  local video_prompt="$3"
  local attempt=1
  local resp=""
  local code=""

  while [ "$attempt" -le "$CREATE_RETRIES" ]; do
    log_info "Creating Seedance task (model=$model, attempt=$attempt/$CREATE_RETRIES)..."
    resp=$(create_task_once "$model" "$image_url" "$video_prompt" || echo '{"code":"curl_error","message":"curl failed"}')
    code=$(echo "$resp" | jq -r '.code // empty' 2>/dev/null || echo "")

    if [ "$code" = "200" ]; then
      echo "$resp"
      return 0
    fi

    local msg
    msg=$(echo "$resp" | jq -r '.message // .data.result.error_message // "Unknown error"' 2>/dev/null || echo "Unknown error")
    log_warn "Create task failed (code=$code): $msg"

    if [ "$attempt" -lt "$CREATE_RETRIES" ]; then
      sleep $((attempt * 5))
    fi
    attempt=$((attempt + 1))
  done

  echo "$resp"
  return 1
}

poll_task_until_done() {
  local task_id="$1"
  local poll_count=0
  local status_resp=""
  local task_status=""

  while [ "$poll_count" -lt "$MAX_POLLS" ]; do
    sleep "$POLL_INTERVAL"
    poll_count=$((poll_count + 1))

    status_resp=$(curl -fsSL -X GET "${SEEDANCE_BASE_URL}/v1/tasks?task_id=${task_id}" \
      -H "Authorization: Bearer $SEEDANCE_API_KEY")

    task_status=$(echo "$status_resp" | jq -r '.data.status // empty')
    log_info "Poll #$poll_count: status=$task_status"

    if [ "$task_status" = "completed" ] || [ "$task_status" = "succeed" ] || [ "$task_status" = "success" ]; then
      echo "$status_resp"
      return 0
    fi

    if [ "$task_status" = "failed" ] || [ "$task_status" = "error" ]; then
      echo "$status_resp"
      return 2
    fi
  done

  echo "$status_resp"
  return 3
}

IMAGE_PUBLIC_URL="$(upload_reference_image || true)"
if [ -z "$IMAGE_PUBLIC_URL" ]; then
  log_error "Failed to upload reference image to any public host"
  exit 1
fi
log_info "Reference image URL: $IMAGE_PUBLIC_URL"

BASE_LOCK="same exact person as the reference image. Preserve identity perfectly."
VIDEO_PROMPT="$BASE_LOCK Selfie video: $PROMPT_RAW. Natural subtle motion, slight head movement, blinking, realistic lighting. Handheld selfie camera feel."

IFS=',' read -r -a FALLBACK_MODELS <<< "$FALLBACK_MODELS_CSV"
FIRST_MODEL="$MODEL"
ALL_MODELS=("$FIRST_MODEL")
for m in "${FALLBACK_MODELS[@]}"; do
  if [ -n "$m" ] && [ "$m" != "$FIRST_MODEL" ]; then
    ALL_MODELS+=("$m")
  fi
done

FINAL_CREATE_RESP=""
FINAL_STATUS_RESP=""
FINAL_TASK_ID=""
FINAL_CREDITS_COST=""
FINAL_MODEL=""
LAST_ERROR_MSG=""

for candidate_model in "${ALL_MODELS[@]}"; do
  log_info "Trying model: $candidate_model"
  CREATE_RESP="$(create_task_with_retry "$candidate_model" "$IMAGE_PUBLIC_URL" "$VIDEO_PROMPT" || true)"
  API_CODE=$(echo "$CREATE_RESP" | jq -r '.code // empty' 2>/dev/null || echo "")

  if [ "$API_CODE" != "200" ]; then
    LAST_ERROR_MSG=$(echo "$CREATE_RESP" | jq -r '.message // "Unknown error"' 2>/dev/null || echo "Unknown error")
    log_warn "Skipping model $candidate_model after failed create: $LAST_ERROR_MSG"
    FINAL_CREATE_RESP="$CREATE_RESP"
    continue
  fi

  TASK_ID=$(echo "$CREATE_RESP" | jq -r '.data.task_id // empty')
  CREDITS_COST=$(echo "$CREATE_RESP" | jq -r '.data.credits_cost // "?"')
  if [ -z "$TASK_ID" ]; then
    LAST_ERROR_MSG="No task_id in response"
    log_warn "$LAST_ERROR_MSG for model $candidate_model"
    FINAL_CREATE_RESP="$CREATE_RESP"
    continue
  fi

  log_info "Task created: $TASK_ID (credits: $CREDITS_COST)"
  STATUS_RESP="$(poll_task_until_done "$TASK_ID" || true)"
  TASK_STATUS=$(echo "$STATUS_RESP" | jq -r '.data.status // empty' 2>/dev/null || echo "")

  if [ "$TASK_STATUS" = "completed" ] || [ "$TASK_STATUS" = "succeed" ] || [ "$TASK_STATUS" = "success" ]; then
    FINAL_CREATE_RESP="$CREATE_RESP"
    FINAL_STATUS_RESP="$STATUS_RESP"
    FINAL_TASK_ID="$TASK_ID"
    FINAL_CREDITS_COST="$CREDITS_COST"
    FINAL_MODEL="$candidate_model"
    break
  fi

  LAST_ERROR_MSG=$(echo "$STATUS_RESP" | jq -r '.data.result.error_message // .data.error // .message // "Unknown error"' 2>/dev/null || echo "Unknown error")
  log_warn "Model $candidate_model ended without success: $LAST_ERROR_MSG"
  FINAL_CREATE_RESP="$CREATE_RESP"
  FINAL_STATUS_RESP="$STATUS_RESP"
done

if [ -z "$FINAL_TASK_ID" ]; then
  log_error "Seedance did not produce a successful task. Last error: $LAST_ERROR_MSG"
  if [ -n "$FINAL_STATUS_RESP" ]; then
    echo "$FINAL_STATUS_RESP" | jq .
  elif [ -n "$FINAL_CREATE_RESP" ]; then
    echo "$FINAL_CREATE_RESP" | jq .
  fi
  exit 1
fi

VIDEO_URL=$(echo "$FINAL_STATUS_RESP" | jq -r '.data.video_url // .data.result.video_url // .data.output.video_url // empty')
if [ -z "$VIDEO_URL" ]; then
  log_warn "Could not find video_url in expected paths, dumping response:"
  echo "$FINAL_STATUS_RESP" | jq .
  VIDEO_URL=$(echo "$FINAL_STATUS_RESP" | jq -r '.. | strings' 2>/dev/null | grep -i '\.mp4' | head -1 || echo "")
fi

if [ -z "$VIDEO_URL" ]; then
  log_error "No video URL found in task result"
  echo "$FINAL_STATUS_RESP"
  exit 1
fi

LOCAL_FILE="${TMPDIR:-/tmp}/clawdy-video-$(date +%s)-$$.mp4"
log_info "Downloading video to: $LOCAL_FILE"
curl -fsSL "$VIDEO_URL" -o "$LOCAL_FILE"

if [ ! -s "$LOCAL_FILE" ]; then
  log_error "Downloaded video file is empty"
  exit 1
fi

log_info "Video size: $(du -h "$LOCAL_FILE" | cut -f1)"
log_info "Sending video via OpenClaw to channel: $CHANNEL"
openclaw message send \
  --action send \
  --channel "$CHANNEL" \
  --message "$CAPTION" \
  --filePath "$LOCAL_FILE"

log_info "Done"
jq -n \
  --arg video_url "$VIDEO_URL" \
  --arg local_file "$LOCAL_FILE" \
  --arg task_id "$FINAL_TASK_ID" \
  --arg channel "$CHANNEL" \
  --arg credits "$FINAL_CREDITS_COST" \
  --arg model "$FINAL_MODEL" \
  '{success:true, video_url:$video_url, local_file:$local_file, task_id:$task_id, channel:$channel, credits_cost:$credits, model:$model}'
