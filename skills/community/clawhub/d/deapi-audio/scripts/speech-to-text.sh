#!/usr/bin/env bash
set -euo pipefail

# deAPI Speech-to-Text (Audio only)
# Transcribes audio files using Whisper Large V3 via deAPI
# Supports: AAC, MP3, OGG, WAV, WebM, FLAC (max 10MB)
# For video/YouTube transcription, use deapi-video/scripts/transcribe.sh
# Usage: bash speech-to-text.sh --audio <path-or-url> [--timestamps true]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# --- Argument parsing ---
AUDIO=""
TIMESTAMPS="true"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --audio) AUDIO="$2"; shift 2 ;;
    --timestamps) TIMESTAMPS="$2"; shift 2 ;;
    --help)
      echo "Usage: bash speech-to-text.sh --audio <path-or-url> [--timestamps true]"
      echo "Accepts local file path or URL. Formats: AAC, MP3, OGG, WAV, WebM, FLAC (max 10MB)"
      echo "For video/YouTube, use deapi-video/scripts/transcribe.sh instead."
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# --- Validation ---
deapi_check_deps
deapi_check_auth
[[ -z "$AUDIO" ]] && { echo "Error: --audio is required (file path or URL)" >&2; exit 1; }

INCLUDE_TS="true"
[[ "$TIMESTAMPS" == "false" ]] && INCLUDE_TS="false"

echo "Transcribing audio..." >&2
echo "Model: WhisperLargeV3 | Endpoint: audiofile2txt" >&2

# --- Ensure local file ---
LOCAL_FILE=$(deapi_ensure_local_file "$AUDIO" "stt") || exit 1
CLEANUP_FILE=""
[[ "$LOCAL_FILE" != "$AUDIO" ]] && CLEANUP_FILE="$LOCAL_FILE"

# --- Build form data ---
FORM_ARGS=()
FORM_ARGS+=(-F "audio=@${LOCAL_FILE}")
FORM_ARGS+=(-F "include_ts=${INCLUDE_TS}")
FORM_ARGS+=(-F "model=WhisperLargeV3")

# --- Submit job ---
RESPONSE=$(deapi_submit_form "audiofile2txt" "${FORM_ARGS[@]}")

# Cleanup temp file
[[ -n "$CLEANUP_FILE" ]] && rm -f "$CLEANUP_FILE"

REQUEST_ID=$(deapi_extract_request_id "$RESPONSE") || exit 1
echo "Request ID: $REQUEST_ID" >&2

# --- Poll for result ---
RESULT=$(deapi_poll_result "$REQUEST_ID" "Transcribing") || exit 1
RESULT_URL=$(echo "$RESULT" | jq -r '.result_url // empty')

echo "" >&2
echo "Transcription complete!" >&2

# Fetch transcription content
TRANSCRIPTION=$(curl -s "$RESULT_URL")
echo "$TRANSCRIPTION" >&2

# Output JSON to stdout
jq -n \
  --arg text "$TRANSCRIPTION" \
  --arg result_url "$RESULT_URL" \
  --arg request_id "$REQUEST_ID" \
  '{transcription: $text, result_url: $result_url, endpoint: "audiofile2txt", request_id: $request_id}'
