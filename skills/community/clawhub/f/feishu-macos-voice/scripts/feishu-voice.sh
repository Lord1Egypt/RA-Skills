#!/usr/bin/env bash
# feishu-voice.sh — Send a voice message to Feishu via TTS
#
# TTS engine priority:
#   1. OpenAI TTS  — if OPENAI_API_KEY is set (env var)
#   2. macOS say   — fallback
#
# Usage:
#   feishu-voice.sh <text> <receive_id> [receive_id_type] [voice] [openai_instructions]
#
# Args:
#   text                  Text to speak
#   receive_id            open_id (ou_xxx) or chat_id (oc_xxx)
#   receive_id_type       "open_id" or "chat_id" (default: auto-detect by prefix)
#   voice                 OpenAI voice (alloy/echo/fable/onyx/nova/shimmer) or macOS voice name
#                         Default: shimmer (OpenAI) / Tingting (macOS)
#   openai_instructions   Speaking style prompt for OpenAI TTS (optional)
#                         e.g. "Speak with a Taiwan Mandarin accent"
#
# Requires: ffmpeg, ffprobe, curl, python3
#           OpenAI TTS: OPENAI_API_KEY env var
#           macOS TTS:  macOS `say` command
#           Feishu credentials in ~/.openclaw/openclaw.json

set -euo pipefail

TEXT="${1:-}"
RECEIVE_ID="${2:-}"
RECEIVE_ID_TYPE="${3:-}"
VOICE="${4:-}"
OPENAI_INSTRUCTIONS="${5:-}"
TMP_OPUS="/tmp/feishu-voice-$$.opus"

# --- Validate args ---
if [[ -z "$TEXT" || -z "$RECEIVE_ID" ]]; then
  echo "Usage: $0 <text> <receive_id> [open_id|chat_id] [voice] [openai_instructions]" >&2
  exit 1
fi

# Auto-detect receive_id_type
if [[ -z "$RECEIVE_ID_TYPE" ]]; then
  if [[ "$RECEIVE_ID" == oc_* ]]; then
    RECEIVE_ID_TYPE="chat_id"
  else
    RECEIVE_ID_TYPE="open_id"
  fi
fi

# --- Read Feishu credentials ---
CONFIG="$HOME/.openclaw/openclaw.json"
APP_ID=$(python3 -c "import json; d=json.load(open('$CONFIG')); print(d['channels']['feishu']['appId'])")
APP_SECRET=$(python3 -c "import json; d=json.load(open('$CONFIG')); print(d['channels']['feishu']['appSecret'])")

if [[ -z "$APP_ID" || -z "$APP_SECRET" ]]; then
  echo "Error: Could not read Feishu credentials from $CONFIG" >&2
  exit 1
fi

# --- Step 1: TTS → opus ---
if [[ -n "${OPENAI_API_KEY:-}" ]]; then
  # ── OpenAI TTS ──────────────────────────────────────────────
  OAI_VOICE="${VOICE:-shimmer}"
  TMP_MP3="/tmp/feishu-voice-$$.mp3"
  echo "🎙️  TTS engine: OpenAI (voice=$OAI_VOICE)"

  # Build JSON payload — include instructions only if provided
  if [[ -n "$OPENAI_INSTRUCTIONS" ]]; then
    PAYLOAD=$(python3 -c "
import json, sys
print(json.dumps({
  'model': 'gpt-4o-mini-tts',
  'input': sys.argv[1],
  'voice': sys.argv[2],
  'instructions': sys.argv[3],
  'response_format': 'mp3'
}))" "$TEXT" "$OAI_VOICE" "$OPENAI_INSTRUCTIONS")
  else
    PAYLOAD=$(python3 -c "
import json, sys
print(json.dumps({
  'model': 'gpt-4o-mini-tts',
  'input': sys.argv[1],
  'voice': sys.argv[2],
  'response_format': 'mp3'
}))" "$TEXT" "$OAI_VOICE")
  fi

  curl -sf -X POST "https://api.openai.com/v1/audio/speech" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" \
    -o "$TMP_MP3"

  ffmpeg -y -i "$TMP_MP3" -acodec libopus -ac 1 -ar 16000 "$TMP_OPUS" 2>/dev/null
  rm -f "$TMP_MP3"

else
  # ── macOS say (fallback) ─────────────────────────────────────
  MAC_VOICE="${VOICE:-Tingting}"
  TMP_AIFF="/tmp/feishu-voice-$$.aiff"
  echo "🎙️  TTS engine: macOS say (voice=$MAC_VOICE)"

  say -v "$MAC_VOICE" "$TEXT" -o "$TMP_AIFF"
  ffmpeg -y -i "$TMP_AIFF" -acodec libopus -ac 1 -ar 16000 "$TMP_OPUS" 2>/dev/null
  rm -f "$TMP_AIFF"
fi

echo "🔄  Transcoded to opus"

# --- Step 2: Duration in milliseconds ---
DURATION_MS=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$TMP_OPUS" \
  | python3 -c "import sys; print(round(float(sys.stdin.read().strip()) * 1000))")
echo "⏱️  Duration: ${DURATION_MS}ms"

# --- Step 3: Get tenant_access_token ---
TENANT_TOKEN=$(curl -sf -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])")

# --- Step 4: Upload file ---
FILE_KEY=$(curl -sf -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TENANT_TOKEN" \
  -F "file_type=opus" \
  -F "file_name=voice.opus" \
  -F "duration=$DURATION_MS" \
  -F "file=@$TMP_OPUS" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['file_key'])")
echo "☁️  Uploaded: $FILE_KEY"

# --- Step 5: Send audio message ---
RESULT=$(curl -sf -X POST \
  "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=$RECEIVE_ID_TYPE" \
  -H "Authorization: Bearer $TENANT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"$RECEIVE_ID\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}")

MSG_ID=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data']['message_id'] if d['code']==0 else 'ERROR: '+d['msg'])")
echo "✅  Sent: $MSG_ID"

# Cleanup
rm -f "$TMP_OPUS"
