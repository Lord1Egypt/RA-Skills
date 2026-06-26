#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <audio-file> [url]"
  exit 1
fi

FILE="$1"
URL="${2:-https://lotfi-whisper-worker.medtouradmin.workers.dev/transcribe}"

if [[ ! -f "$FILE" ]]; then
  echo "Error: file not found: $FILE"
  exit 1
fi

if [[ -z "${WHISPER_WORKER_TOKEN:-}" ]]; then
  echo "Error: WHISPER_WORKER_TOKEN is not set"
  echo "Set it with: export WHISPER_WORKER_TOKEN=\"<token>\""
  exit 1
fi

ext="${FILE##*.}"
ext="$(echo "$ext" | tr '[:upper:]' '[:lower:]')"

case "$ext" in
  wav) ctype="audio/wav" ;;
  mp3) ctype="audio/mpeg" ;;
  m4a) ctype="audio/mp4" ;;
  ogg|opus) ctype="audio/ogg" ;;
  webm) ctype="audio/webm" ;;
  *) ctype="application/octet-stream" ;;
esac

curl -sS -X POST "$URL" \
  -H "content-type: $ctype" \
  -H "authorization: Bearer $WHISPER_WORKER_TOKEN" \
  --data-binary "@$FILE" \
| jq -r '.result.text // .text // .result.response // empty'
