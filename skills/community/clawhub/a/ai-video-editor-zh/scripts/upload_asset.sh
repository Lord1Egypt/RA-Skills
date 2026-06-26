#!/usr/bin/env bash
# Upload a video asset to Sparki Business API for processing.
#
# Usage: upload_asset.sh <file_path>
#
# Args:
#   file_path: Local path to the video file (mp4 only, max 3GB)
#
# Outputs (stdout): object_key on success
# Exits with 1 on validation error, 2 on API error.

set -euo pipefail

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SPARKI_API_BASE="https://agent-enterprise-dev.aicoding.live/api/v1"
RATE_LIMIT_SLEEP=3

# ---------------------------------------------------------------------------
# Validate environment
# ---------------------------------------------------------------------------
: "${SPARKI_API_KEY:?Error: SPARKI_API_KEY environment variable is required}"

# ---------------------------------------------------------------------------
# Validate arguments
# ---------------------------------------------------------------------------
if [[ $# -lt 1 ]]; then
  echo "Usage: upload_asset.sh <file_path>" >&2
  exit 1
fi

FILE_PATH="$1"

if [[ ! -f "$FILE_PATH" ]]; then
  echo "Error: File not found: $FILE_PATH" >&2
  exit 1
fi

# Check extension (mp4 only)
FILE_EXT="${FILE_PATH##*.}"
FILE_EXT_LOWER="$(echo "$FILE_EXT" | tr '[:upper:]' '[:lower:]')"
if [[ "$FILE_EXT_LOWER" != "mp4" ]]; then
  echo "Error: Unsupported format '$FILE_EXT_LOWER'. Only mp4 is accepted." >&2
  exit 1
fi

# Check file size (<= 3 GB)
MAX_BYTES=$((3 * 1024 * 1024 * 1024))
FILE_BYTES=$(wc -c < "$FILE_PATH" | tr -d ' ')
if (( FILE_BYTES > MAX_BYTES )); then
  echo "Error: File too large ($(( FILE_BYTES / 1024 / 1024 )) MB). Maximum is 3 GB." >&2
  exit 1
fi

# ---------------------------------------------------------------------------
# Upload via multipart POST
# ---------------------------------------------------------------------------
sleep "$RATE_LIMIT_SLEEP"

RESPONSE=$(curl -sS \
  -X POST "${SPARKI_API_BASE}/business/assets/upload" \
  -H "X-API-Key: $SPARKI_API_KEY" \
  -F "files=@${FILE_PATH};type=video/mp4")

# Parse response
HTTP_CODE=$(echo "$RESPONSE" | jq -r '.code // "unknown"')
MESSAGE=$(echo "$RESPONSE" | jq -r '.message // "unknown"')

if [[ "$HTTP_CODE" != "200" && "$HTTP_CODE" != "0" ]]; then
  echo "Error: Upload failed (code=$HTTP_CODE): $MESSAGE" >&2
  exit 2
fi

OBJECT_KEY=$(echo "$RESPONSE" | jq -r '.data.uploads[0].object_key // empty')
if [[ -z "$OBJECT_KEY" ]]; then
  echo "Error: No object_key in response. Full response:" >&2
  echo "$RESPONSE" >&2
  exit 2
fi

# Output only the object_key so callers can capture it
echo "$OBJECT_KEY"
