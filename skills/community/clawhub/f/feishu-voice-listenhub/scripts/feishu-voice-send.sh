#!/usr/bin/env bash
# feishu-voice-send.sh — Generate TTS via ListenHub and send as Feishu voice message
# Usage: feishu-voice-send.sh <text> <receive_id> [receive_id_type] [speaker_id]
#
# Required env:
#   LISTENHUB_API_KEY     — ListenHub API key
#   FEISHU_APP_ID         — Feishu app ID
#   FEISHU_APP_SECRET     — Feishu app secret
#
# Optional env:
#   LISTENHUB_SPEAKER_ID  — Default speaker ID (default: chat-girl-105-cn)

set -euo pipefail

TEXT="${1:?Usage: feishu-voice-send.sh <text> <receive_id> [receive_id_type] [speaker_id]}"
RECEIVE_ID="${2:?Missing receive_id}"
RECEIVE_ID_TYPE="${3:-open_id}"
SPEAKER_ID="${4:-${LISTENHUB_SPEAKER_ID:-chat-girl-105-cn}}"

: "${LISTENHUB_API_KEY:?Set LISTENHUB_API_KEY}"
: "${FEISHU_APP_ID:?Set FEISHU_APP_ID}"
: "${FEISHU_APP_SECRET:?Set FEISHU_APP_SECRET}"

API_BASE="https://api.marswave.ai/openapi/v1"
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Step 1: Build request JSON
python3 -c "
import json, sys
with open(sys.argv[1], 'w') as f:
    json.dump({
        'sources': [{'type': 'text', 'content': sys.argv[2]}],
        'language': 'zh',
        'mode': 'direct',
        'speakers': [{'speakerId': sys.argv[3]}]
    }, f)
" "$TMPDIR/req.json" "$TEXT" "$SPEAKER_ID"

# Step 2: Create TTS task
TTS_RESP=$(curl -sS -X POST "$API_BASE/podcast/episodes" \
  -H "Authorization: Bearer $LISTENHUB_API_KEY" \
  -H "Content-Type: application/json" \
  -d @"$TMPDIR/req.json")

EPISODE_ID=$(echo "$TTS_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['episodeId'])")

# Step 3: Poll for completion (max 60s)
AUDIO_URL=""
for i in $(seq 1 12); do
  sleep 5
  STATUS_RESP=$(curl -sS "$API_BASE/podcast/episodes/$EPISODE_ID" \
    -H "Authorization: Bearer $LISTENHUB_API_KEY")

  STATUS=$(echo "$STATUS_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['processStatus'])")

  if [ "$STATUS" = "success" ]; then
    AUDIO_URL=$(echo "$STATUS_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['audioUrl'])")
    break
  elif [ "$STATUS" = "failed" ]; then
    echo "ERROR: TTS generation failed" >&2
    exit 1
  fi
done

if [ -z "$AUDIO_URL" ]; then
  echo "ERROR: TTS generation timed out" >&2
  exit 1
fi

# Step 4: Download audio
curl -sS "$AUDIO_URL" -o "$TMPDIR/voice.mp3"

# Step 5: Convert to opus
ffmpeg -y -i "$TMPDIR/voice.mp3" -c:a libopus -b:a 32k "$TMPDIR/voice.opus" >/dev/null 2>&1

# Step 6: Get duration
DURATION=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$TMPDIR/voice.opus" | cut -d. -f1)
[ -z "$DURATION" ] && DURATION=1

# Step 7: Get Feishu tenant_access_token
TOKEN=$(curl -sS -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json' \
  -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['tenant_access_token'])")

# Step 8: Upload opus
FILE_KEY=$(curl -sS -X POST 'https://open.feishu.cn/open-apis/im/v1/files' \
  -H "Authorization: Bearer $TOKEN" \
  -F 'file_type=opus' \
  -F 'file_name=voice.opus' \
  -F "file=@$TMPDIR/voice.opus" \
  -F "duration=$DURATION" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['data']['file_key'])")

# Step 9: Send audio message
RESULT=$(curl -sS -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=$RECEIVE_ID_TYPE" \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"receive_id\":\"$RECEIVE_ID\",\"msg_type\":\"audio\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}")

echo "$RESULT" | python3 -c "
import sys,json
d=json.load(sys.stdin)
if d['code']==0:
    print(f\"OK | message_id={d['data']['message_id']}\")
else:
    print(f\"ERROR | code={d['code']} msg={d['msg']}\")
    sys.exit(1)
"
