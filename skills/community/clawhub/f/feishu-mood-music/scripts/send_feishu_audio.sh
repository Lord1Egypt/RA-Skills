#!/bin/bash
# send_audio.sh - Generate TTS (or use existing file) and send as audio message to Feishu
#
# Usage (TTS mode):
#   send_audio.sh "text to speak" <chat_id> [voice]
#
# Usage (file mode - for existing audio files):
#   send_audio.sh --file /path/to/audio.mp3 <chat_id>
#
# Examples:
#   send_audio.sh "今日报数：1、2、3，完毕！" "oc_abc123"
#   send_audio.sh --file /tmp/openclaw/tts-AiEBGW/voice-123.mp3 "oc_abc123"
#
# voice defaults: zh-CN-XiaoyiNeural (Chinese), en-US-AriaNeural (English)

set -e

FILE_MODE=false
if [[ "$1" == "--file" ]]; then
  FILE_MODE=true
  INPUT_FILE="${2:?--file requires a path}"
  CHAT_ID="${3:?chat_id required}"
  VOICE=""
  TMP_FILE="$INPUT_FILE"
else
  TEXT="${1:?Usage: send_audio.sh <text> <chat_id> [voice] OR --file <path> <chat_id>}"
  CHAT_ID="${2:?chat_id required}"
  VOICE="${3:-zh-CN-XiaoyiNeural}"
  TMP_FILE="/tmp/feishu_audio_$$.mp3"
fi

APP_ID="${FEISHU_APP_ID:-}"
APP_SECRET="${FEISHU_APP_SECRET:-}"
TTS_BIN="${EDGE_TTS:-edge-tts}"

# --- 1. Resolve Feishu credentials ---
if [[ -z "$APP_ID" || -z "$APP_SECRET" ]]; then
  CONFIG_FILE="${OPENCLAW_CONFIG:-$HOME/.openclaw/openclaw.json}"
  if [[ -f "$CONFIG_FILE" ]]; then
    APP_ID=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d['channels']['feishu']['accounts']['main']['appId'])" 2>/dev/null)
    APP_SECRET=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d['channels']['feishu']['accounts']['main']['appSecret'])" 2>/dev/null)
  fi
fi

if [[ -z "$APP_ID" || -z "$APP_SECRET" ]]; then
  echo "❌ Feishu credentials not found." >&2
  echo "   Set FEISHU_APP_ID and FEISHU_APP_SECRET env vars, or configure in openclaw.json" >&2
  exit 1
fi

# --- 2. TTS (skip if --file mode) ---
if [[ "$FILE_MODE" == false ]]; then
  echo "🎙️  Generating TTS (voice: $VOICE)..."
  "$TTS_BIN" -t "$TEXT" -f "$TMP_FILE" -v "$VOICE" -l "$(echo $VOICE | cut -d- -f1-2)" 2>&1
  echo "   Audio: $(du -h $TMP_FILE | cut -f1)"
else
  echo "📁 Using file: $TMP_FILE"
  [[ -f "$TMP_FILE" ]] || { echo "❌ File not found: $TMP_FILE" >&2; exit 1; }
fi

# --- 3. Get tenant access token ---
echo "🔑 Getting Feishu token..."
TOKEN=$(curl -sf -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d "{\"app_id\": \"$APP_ID\", \"app_secret\": \"$APP_SECRET\"}" \
  | python3 -c "import sys,json; r=json.load(sys.stdin); print(r['tenant_access_token']) if r.get('code')==0 else sys.exit(r.get('msg','auth failed'))")

# --- 4. Upload file (file_type=opus is required for audio messages) ---
echo "📤 Uploading to Feishu..."
UPLOAD_RESP=$(curl -sf -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=opus" \
  -F "file_name=voice.opus" \
  -F "file=@$TMP_FILE")

FILE_KEY=$(echo "$UPLOAD_RESP" | python3 -c "import sys,json; r=json.load(sys.stdin); print(r['data']['file_key']) if r.get('code')==0 else sys.exit(str(r))")
echo "   file_key: $FILE_KEY"

# --- 5. Send audio message (msg_type=audio) ---
echo "📨 Sending audio message..."
SEND_RESP=$(curl -sf -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\": \"$CHAT_ID\", \"msg_type\": \"audio\", \"content\": \"{\\\"file_key\\\": \\\"$FILE_KEY\\\"}\"}")

MSG_ID=$(echo "$SEND_RESP" | python3 -c "import sys,json; r=json.load(sys.stdin); print(r['data']['message_id']) if r.get('code')==0 else sys.exit(str(r))")
echo "✅ Sent! message_id: $MSG_ID"

# Cleanup temp file (only if we created it)
if [[ "$FILE_MODE" == false ]]; then rm -f "$TMP_FILE"; fi
