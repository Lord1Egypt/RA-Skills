#!/bin/bash
# send_audio.sh - Generate TTS (or use existing file) and send as audio message to Feishu
# Optionally appends a transcript as a thread reply below the audio bubble.
#
# Usage (TTS mode):
#   send_audio.sh "text to speak" <chat_id> [voice]
#
# Usage (TTS + auto transcript):
#   send_audio.sh --transcript "text to speak" <chat_id> [voice]
#
# Usage (file mode):
#   send_audio.sh --file /path/to/audio.mp3 <chat_id> [transcript text]
#
# Examples:
#   send_audio.sh "今日报数：1、2、3！" "oc_abc123"
#   send_audio.sh --transcript "今日报数：1、2、3！" "oc_abc123"
#   send_audio.sh --file /tmp/voice.mp3 "oc_abc123" "语音报数内容"

set -e

TRANSCRIPT_MODE=false
FILE_MODE=false

if [[ "$1" == "--transcript" ]]; then
  TRANSCRIPT_MODE=true
  TEXT="${2:?--transcript requires text}"
  CHAT_ID="${3:?chat_id required}"
  VOICE="${4:-zh-CN-XiaoyiNeural}"
  TMP_FILE="/tmp/feishu_audio_$$.mp3"
elif [[ "$1" == "--file" ]]; then
  FILE_MODE=true
  TMP_FILE="${2:?--file requires a path}"
  CHAT_ID="${3:?chat_id required}"
  TRANSCRIPT_TEXT="${4:-}"
  VOICE=""
else
  TEXT="${1:?Usage: send_audio.sh [--transcript|--file] <text|path> <chat_id> [voice]}"
  CHAT_ID="${2:?chat_id required}"
  VOICE="${3:-zh-CN-XiaoyiNeural}"
  TMP_FILE="/tmp/feishu_audio_$$.mp3"
fi

APP_ID="${FEISHU_APP_ID:-}"
APP_SECRET="${FEISHU_APP_SECRET:-}"
TTS_BIN="/app/openclaw/node_modules/.bin/node-edge-tts"

# --- 1. Resolve Feishu credentials ---
if [[ -z "$APP_ID" || -z "$APP_SECRET" ]]; then
  CONFIG_FILE="/root/.openclaw/openclaw.json"
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
echo "✅ Audio sent! message_id: $MSG_ID"

# --- 6. Send transcript as thread reply (optional) ---
TRANSCRIPT=""
if [[ "$TRANSCRIPT_MODE" == true ]]; then
  TRANSCRIPT="$TEXT"
elif [[ "$FILE_MODE" == true && -n "$TRANSCRIPT_TEXT" ]]; then
  TRANSCRIPT="$TRANSCRIPT_TEXT"
fi

if [[ -n "$TRANSCRIPT" ]]; then
  echo "💬 Sending transcript..."
  CARD=$(python3 -c "
import json, sys
transcript = sys.argv[1]
card = {
    'config': {'wide_screen_mode': False},
    'elements': [
        {'tag': 'div', 'text': {'tag': 'lark_md', 'content': f'💬 {transcript}'}}
    ]
}
print(json.dumps(json.dumps(card)))
" "$TRANSCRIPT")

  THREAD_RESP=$(curl -sf -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{
      \"receive_id\": \"$CHAT_ID\",
      \"msg_type\": \"interactive\",
      \"content\": $CARD,
      \"reply_in_thread\": true,
      \"root_id\": \"$MSG_ID\"
    }")
  echo "$THREAD_RESP" | python3 -c "import sys,json; r=json.load(sys.stdin); print('✅ Transcript sent!') if r.get('code')==0 else print('⚠️ Transcript failed:', r)"
fi

# Cleanup temp file (only if we created it)
if [[ "$FILE_MODE" == false ]]; then rm -f "$TMP_FILE"; fi
