#!/usr/bin/env bash
# End-to-end Sparki Business API video processing workflow.
#
# Orchestrates upload → wait for asset ready → create project → poll until done.
# Progress logs are written to stderr; the final result_url is written to stdout,
# making this script safe to use in pipelines.
#
# Usage:
#   edit_video.sh <file_path> <tips> [user_prompt] [aspect_ratio] [duration]
#
# Args:
#   file_path:    Local path to a video file (mp4 only, max 3GB)
#   tips:         Single tip ID integer (e.g. "22"). See SKILL.md for full tip reference.
#                 Leave empty ("") to use Prompt Freely Mode (user_prompt required, min 10 chars).
#   user_prompt:  (optional) Free-text requirement (min 10 chars if tips is empty)
#   aspect_ratio: (optional) "9:16" (default) | "1:1" | "16:9"
#   duration:     (optional) Target duration in seconds
#
# Environment variables:
#   SPARKI_API_KEY        Required. Your Sparki Business API key.
#   WORKFLOW_TIMEOUT      Optional. Max seconds to wait for project completion (default: 3600).
#   ASSET_TIMEOUT         Optional. Max seconds to wait for asset processing (default: 300).
#
# Outputs (stdout): result_url — the 24-hour pre-signed download URL of the processed video.
# Exit codes:
#   0 — success
#   1 — input/config error
#   2 — asset processing timed out or failed
#   3 — project processing timed out
#   4 — project failed

set -euo pipefail

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SPARKI_API_BASE="${SPARKI_API_BASE:-https://agent-enterprise-dev.aicoding.live/api/v1}"
RATE_LIMIT_SLEEP=3
ASSET_POLL_INTERVAL=5
PROJECT_POLL_INTERVAL=10
WORKFLOW_TIMEOUT="${WORKFLOW_TIMEOUT:-3600}"
ASSET_TIMEOUT="${ASSET_TIMEOUT:-300}"

# Resolve scripts directory relative to this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

get_asset_status() {
  local object_key="$1"
  local response

  response=$(curl -sS \
    -X POST "${SPARKI_API_BASE}/business/assets/batch" \
    -H "X-API-Key: $SPARKI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"object_keys\":[\"${object_key}\"]}")

  if [[ "$(echo "$response" | jq -r '.code // "unknown"')" != "200" && "$(echo "$response" | jq -r '.code // "unknown"')" != "0" ]]; then
    echo "unknown"
    return 0
  fi

  echo "$response" | jq -r '
    (.data.assets // [])[0] as $asset
    | if $asset == null then
        "not_found"
      elif (($asset.status | type) == "string") then
        $asset.status
      elif ($asset.status == 1) or ((($asset.duration // 0) > 0) and ((($asset.resolution // "") | length) > 0)) then
        "completed"
      elif $asset.status == 2 then
        "failed"
      else
        "processing"
      end'
}

# ---------------------------------------------------------------------------
# Validate environment
# ---------------------------------------------------------------------------
: "${SPARKI_API_KEY:?Error: SPARKI_API_KEY environment variable is required}"

# ---------------------------------------------------------------------------
# Validate arguments
# ---------------------------------------------------------------------------
if [[ $# -lt 2 ]]; then
  echo "Usage: edit_video.sh <file_path> <tips> [user_prompt] [aspect_ratio] [duration]" >&2
  echo "  Example: edit_video.sh my_video.mp4 '22' 'make it dynamic' '9:16' 60" >&2
  exit 1
fi

FILE_PATH="$1"
TIPS="$2"
USER_PROMPT="${3:-}"
ASPECT_RATIO="${4:-9:16}"
DURATION="${5:-}"

# ---------------------------------------------------------------------------
# Step 1: Upload asset
# ---------------------------------------------------------------------------
echo "[1/4] Uploading asset: $FILE_PATH" >&2

OBJECT_KEY=$(bash "${SCRIPT_DIR}/upload_asset.sh" "$FILE_PATH")

if [[ -z "$OBJECT_KEY" ]]; then
  echo "Error: upload_asset.sh returned empty object_key" >&2
  exit 1
fi

echo "[1/4] Asset accepted. object_key=$OBJECT_KEY" >&2

# ---------------------------------------------------------------------------
# Step 2: Poll until asset status = completed
# ---------------------------------------------------------------------------
echo "[2/4] Waiting for asset processing to complete (timeout=${ASSET_TIMEOUT}s)..." >&2

ASSET_START=$(date +%s)
while true; do
  sleep "$ASSET_POLL_INTERVAL"

  ASSET_STATUS=$(get_asset_status "$OBJECT_KEY")
  echo "[2/4] Asset status: $ASSET_STATUS" >&2

  if [[ "$ASSET_STATUS" == "completed" ]]; then
    echo "[2/4] Asset ready." >&2
    break
  fi

  if [[ "$ASSET_STATUS" == "failed" ]]; then
    echo "Error: Asset processing failed." >&2
    exit 2
  fi

  ELAPSED=$(( $(date +%s) - ASSET_START ))
  if (( ELAPSED >= ASSET_TIMEOUT )); then
    echo "Error: Asset processing timed out after ${ASSET_TIMEOUT}s (status=$ASSET_STATUS)." >&2
    exit 2
  fi
done

# ---------------------------------------------------------------------------
# Step 3: Create project
# ---------------------------------------------------------------------------
echo "[3/4] Creating video project (tips=$TIPS, aspect_ratio=$ASPECT_RATIO)..." >&2

sleep "$RATE_LIMIT_SLEEP"

PROJECT_ID=$(bash "${SCRIPT_DIR}/create_project.sh" \
  "$OBJECT_KEY" "$TIPS" "$USER_PROMPT" "$ASPECT_RATIO" "$DURATION")

if [[ -z "$PROJECT_ID" ]]; then
  echo "Error: create_project.sh returned empty project_id" >&2
  exit 1
fi

echo "[3/4] Project created. project_id=$PROJECT_ID" >&2

# ---------------------------------------------------------------------------
# Step 4: Poll until project completes
# ---------------------------------------------------------------------------
echo "[4/4] Waiting for video processing (timeout=${WORKFLOW_TIMEOUT}s)..." >&2

PROJECT_START=$(date +%s)
while true; do
  sleep "$PROJECT_POLL_INTERVAL"

  # Use get_project_status.sh; disable errexit since exit code 2 = in-progress
  set +e
  STATUS_LINE=$(bash "${SCRIPT_DIR}/get_project_status.sh" "$PROJECT_ID" 2>/dev/null)
  STATUS_EXIT=$?
  set -e

  # STATUS_LINE format: "completed <url>" | "failed <msg>" | "processing"
  STATUS_WORD="${STATUS_LINE%% *}"

  echo "[4/4] Project status: $STATUS_WORD" >&2

  if [[ "$STATUS_WORD" == "completed" ]]; then
    RESULT_URL="${STATUS_LINE#completed }"
    echo "[4/4] Processing complete!" >&2
    # Write result_url to stdout — safe for pipeline capture
    echo "$RESULT_URL"
    exit 0
  fi

  if [[ "$STATUS_WORD" == "failed" ]]; then
    ERROR_MSG="${STATUS_LINE#failed }"
    echo "Error: Project failed — $ERROR_MSG" >&2
    exit 4
  fi

  ELAPSED=$(( $(date +%s) - PROJECT_START ))
  if (( ELAPSED >= WORKFLOW_TIMEOUT )); then
    echo "Error: Project processing timed out after ${WORKFLOW_TIMEOUT}s (status=$STATUS_WORD)." >&2
    echo "Tip: Query the project manually: bash get_project_status.sh $PROJECT_ID" >&2
    exit 3
  fi
done
