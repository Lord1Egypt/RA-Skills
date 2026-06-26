#!/usr/bin/env bash
set -euo pipefail

# deAPI Voice Clone
# Clones a voice from a reference audio sample using Qwen3 TTS
# Usage: bash voice-clone.sh --text "Hello world" --ref-audio <path-or-url> [--ref-text "transcript"] [--lang English] [--format mp3]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# --- Argument parsing ---
TEXT=""
REF_AUDIO=""
REF_TEXT=""
LANG="English"
FORMAT="mp3"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --text) TEXT="$2"; shift 2 ;;
    --ref-audio) REF_AUDIO="$2"; shift 2 ;;
    --ref-text) REF_TEXT="$2"; shift 2 ;;
    --lang) LANG="$2"; shift 2 ;;
    --format) FORMAT="$2"; shift 2 ;;
    --help)
      echo "Usage: bash voice-clone.sh --text <text> --ref-audio <path-or-url> [--ref-text <transcript>] [--lang English] [--format mp3]"
      echo "Supported languages: English, Italian, Spanish, Portuguese, Russian, French, German, Korean, Japanese, Chinese"
      echo "Ref audio: 5-15s, formats: mp3, wav, flac, ogg, m4a"
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# --- Validation ---
deapi_check_deps
deapi_check_auth
[[ -z "$TEXT" ]] && { echo "Error: --text is required" >&2; exit 1; }
[[ -z "$REF_AUDIO" ]] && { echo "Error: --ref-audio is required (path or URL to 5-15s audio sample)" >&2; exit 1; }

TEXT_LEN=${#TEXT}
if [[ $TEXT_LEN -lt 10 || $TEXT_LEN -gt 5000 ]]; then
  echo "Error: Text must be 10-5000 characters (got $TEXT_LEN)" >&2
  exit 1
fi

echo "Cloning voice..." >&2
echo "Model: Qwen3_TTS_12Hz_1_7B_Base | Lang: $LANG" >&2

# --- Ensure local file for ref_audio ---
LOCAL_FILE=$(deapi_ensure_local_file "$REF_AUDIO" "voiceclone") || exit 1
CLEANUP_FILE=""
[[ "$LOCAL_FILE" != "$REF_AUDIO" ]] && CLEANUP_FILE="$LOCAL_FILE"

# --- Build form data ---
FORM_ARGS=()
FORM_ARGS+=(-F "text=$(printf '%s' "$TEXT")")
FORM_ARGS+=(-F "ref_audio=@${LOCAL_FILE}")
FORM_ARGS+=(-F "model=Qwen3_TTS_12Hz_1_7B_Base")
FORM_ARGS+=(-F "mode=voice_clone")
FORM_ARGS+=(-F "voice=default")
FORM_ARGS+=(-F "lang=${LANG}")
FORM_ARGS+=(-F "speed=1")
FORM_ARGS+=(-F "format=${FORMAT}")
FORM_ARGS+=(-F "sample_rate=24000")

if [[ -n "$REF_TEXT" ]]; then
  FORM_ARGS+=(-F "ref_text=$(printf '%s' "$REF_TEXT")")
fi

# --- Submit job ---
RESPONSE=$(deapi_submit_form "txt2audio" "${FORM_ARGS[@]}")

# Cleanup temp file
[[ -n "$CLEANUP_FILE" ]] && rm -f "$CLEANUP_FILE"

REQUEST_ID=$(deapi_extract_request_id "$RESPONSE") || exit 1
echo "Request ID: $REQUEST_ID" >&2

# --- Poll for result ---
RESULT=$(deapi_poll_result "$REQUEST_ID" "Cloning voice") || exit 1
RESULT_URL=$(echo "$RESULT" | jq -r '.result_url // empty')

echo "" >&2
echo "Voice cloned!" >&2
echo "Audio URL: $RESULT_URL" >&2
echo "Format: $FORMAT" >&2

# Output JSON to stdout
jq -n \
  --arg url "$RESULT_URL" \
  --arg model "Qwen3_TTS_12Hz_1_7B_Base" \
  --arg format "$FORMAT" \
  --arg request_id "$REQUEST_ID" \
  '{audio_url: $url, model: $model, format: $format, sample_rate: 24000, request_id: $request_id}'
