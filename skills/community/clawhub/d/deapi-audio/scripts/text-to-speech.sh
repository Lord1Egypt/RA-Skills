#!/usr/bin/env bash
set -euo pipefail

# deAPI Text-to-Speech
# Converts text to speech using Kokoro, Chatterbox, or Qwen3 model via deAPI
# Usage: bash text-to-speech.sh --text "Hello world" [--model Kokoro] [--voice af_bella] [--lang en-us] [--speed 1.0] [--format mp3]

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

# --- Argument parsing ---
TEXT=""
MODEL="Kokoro"
VOICE=""
LANG=""
SPEED=""
FORMAT="mp3"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --text) TEXT="$2"; shift 2 ;;
    --model) MODEL="$2"; shift 2 ;;
    --voice) VOICE="$2"; shift 2 ;;
    --lang) LANG="$2"; shift 2 ;;
    --speed) SPEED="$2"; shift 2 ;;
    --format) FORMAT="$2"; shift 2 ;;
    --help)
      echo "Usage: bash text-to-speech.sh --text <text> [--model Kokoro|Chatterbox|Qwen3] [--voice af_bella] [--lang en-us] [--speed 1.0] [--format mp3]"
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

# --- Validation ---
deapi_check_deps
deapi_check_auth
[[ -z "$TEXT" ]] && { echo "Error: --text is required" >&2; exit 1; }

# --- Apply model defaults ---
if [[ "$MODEL" == "Chatterbox" ]]; then
  VOICE="default"
  SPEED="1"
  [[ -z "$LANG" ]] && LANG="en"
elif [[ "$MODEL" == "Qwen3" ]]; then
  MODEL="Qwen3_TTS_12Hz_1_7B_CustomVoice"
  [[ -z "$VOICE" ]] && VOICE="Vivian"
  SPEED="1"
  [[ -z "$LANG" ]] && LANG="English"
else
  [[ -z "$VOICE" ]] && VOICE="af_bella"
  [[ -z "$SPEED" ]] && SPEED="1.0"
  # Auto-detect language from voice ID if not specified
  if [[ -z "$LANG" ]]; then
    case "${VOICE:0:1}" in
      a) LANG="en-us" ;;
      b) LANG="en-gb" ;;
      e) LANG="es" ;;
      f) LANG="fr-fr" ;;
      h) LANG="hi" ;;
      i) LANG="it" ;;
      p) LANG="pt-br" ;;
      *) LANG="en-us" ;;
    esac
  fi
fi

# --- Validate text length ---
TEXT_LEN=${#TEXT}
case "$MODEL" in
  Chatterbox)
    MIN_TEXT=10; MAX_TEXT=2000 ;;
  Qwen3_TTS_12Hz_1_7B_CustomVoice)
    MIN_TEXT=10; MAX_TEXT=5000 ;;
  *)
    MIN_TEXT=3; MAX_TEXT=10001 ;;
esac
if [[ $TEXT_LEN -lt $MIN_TEXT || $TEXT_LEN -gt $MAX_TEXT ]]; then
  echo "Error: Text must be ${MIN_TEXT}-${MAX_TEXT} characters (got $TEXT_LEN)" >&2
  exit 1
fi

echo "Generating speech..." >&2
echo "Model: $MODEL | Voice: $VOICE | Lang: $LANG" >&2

# --- Submit job ---
RESPONSE=$(deapi_submit_json "txt2audio" "{
  \"text\": $(printf '%s' "$TEXT" | jq -Rs .),
  \"voice\": \"${VOICE}\",
  \"model\": \"${MODEL}\",
  \"lang\": \"${LANG}\",
  \"speed\": ${SPEED},
  \"format\": \"${FORMAT}\",
  \"sample_rate\": 24000,
  \"mode\": \"custom_voice\"
}")

REQUEST_ID=$(deapi_extract_request_id "$RESPONSE") || exit 1
echo "Request ID: $REQUEST_ID" >&2

# --- Poll for result ---
RESULT=$(deapi_poll_result "$REQUEST_ID" "Generating speech") || exit 1
RESULT_URL=$(echo "$RESULT" | jq -r '.result_url // empty')

echo "" >&2
echo "Speech generated!" >&2
echo "Audio URL: $RESULT_URL" >&2
echo "Format: $FORMAT" >&2

# Output JSON to stdout
jq -n \
  --arg url "$RESULT_URL" \
  --arg model "$MODEL" \
  --arg voice "$VOICE" \
  --arg format "$FORMAT" \
  --arg request_id "$REQUEST_ID" \
  '{audio_url: $url, model: $model, voice: $voice, format: $format, sample_rate: 24000, request_id: $request_id}'
