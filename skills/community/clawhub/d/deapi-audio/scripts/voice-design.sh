#!/usr/bin/env bash
set -euo pipefail

# deAPI Voice Design
# Generates speech with a custom voice described in natural language using Qwen3 TTS
# Usage: bash voice-design.sh --text "Hello world" --instruct "A warm female voice with a British accent" [--lang English] [--format mp3]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# --- Argument parsing ---
TEXT=""
INSTRUCT=""
LANG="English"
FORMAT="mp3"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --text) TEXT="$2"; shift 2 ;;
    --instruct) INSTRUCT="$2"; shift 2 ;;
    --lang) LANG="$2"; shift 2 ;;
    --format) FORMAT="$2"; shift 2 ;;
    --help)
      echo "Usage: bash voice-design.sh --text <text> --instruct <voice-description> [--lang English] [--format mp3]"
      echo "Supported languages: English, Italian, Spanish, Portuguese, Russian, French, German, Korean, Japanese, Chinese"
      echo "Instruct example: \"A deep male voice with a British accent, speaking confidently\""
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# --- Validation ---
deapi_check_deps
deapi_check_auth
[[ -z "$TEXT" ]] && { echo "Error: --text is required" >&2; exit 1; }
[[ -z "$INSTRUCT" ]] && { echo "Error: --instruct is required (natural language voice description)" >&2; exit 1; }

TEXT_LEN=${#TEXT}
if [[ $TEXT_LEN -lt 10 || $TEXT_LEN -gt 5000 ]]; then
  echo "Error: Text must be 10-5000 characters (got $TEXT_LEN)" >&2
  exit 1
fi

echo "Designing voice..." >&2
echo "Model: Qwen3_TTS_12Hz_1_7B_VoiceDesign | Lang: $LANG" >&2
echo "Voice: $INSTRUCT" >&2

# --- Submit job ---
RESPONSE=$(deapi_submit_json "txt2audio" "{
  \"text\": $(printf '%s' "$TEXT" | jq -Rs .),
  \"instruct\": $(printf '%s' "$INSTRUCT" | jq -Rs .),
  \"model\": \"Qwen3_TTS_12Hz_1_7B_VoiceDesign\",
  \"mode\": \"voice_design\",
  \"voice\": \"default\",
  \"lang\": \"${LANG}\",
  \"speed\": 1,
  \"format\": \"${FORMAT}\",
  \"sample_rate\": 24000
}")

REQUEST_ID=$(deapi_extract_request_id "$RESPONSE") || exit 1
echo "Request ID: $REQUEST_ID" >&2

# --- Poll for result ---
RESULT=$(deapi_poll_result "$REQUEST_ID" "Designing voice") || exit 1
RESULT_URL=$(echo "$RESULT" | jq -r '.result_url // empty')

echo "" >&2
echo "Voice designed!" >&2
echo "Audio URL: $RESULT_URL" >&2
echo "Format: $FORMAT" >&2

# Output JSON to stdout
jq -n \
  --arg url "$RESULT_URL" \
  --arg model "Qwen3_TTS_12Hz_1_7B_VoiceDesign" \
  --arg format "$FORMAT" \
  --arg request_id "$REQUEST_ID" \
  '{audio_url: $url, model: $model, format: $format, sample_rate: 24000, request_id: $request_id}'
