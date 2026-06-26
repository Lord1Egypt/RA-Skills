#!/usr/bin/env bash
set -euo pipefail

# 用法:
#   send_feishu_voice.sh "要合成的文本" [open_id] [voice]
# 环境变量(可选):
#   FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_OPEN_ID, EDGE_TTS_VOICE

TEXT="${1:-}"
OPEN_ID_ARG="${2:-}"
VOICE_ARG="${3:-}"

if [[ -z "$TEXT" ]]; then
  echo "Usage: $0 \"text\" [open_id] [voice]" >&2
  exit 1
fi

CFG="$HOME/.openclaw/openclaw.json"
if [[ ! -f "$CFG" ]]; then
  echo "openclaw config not found: $CFG" >&2
  exit 2
fi

read_cfg() {
  python3 - <<'PY' "$CFG"
import json,sys
p=sys.argv[1]
obj=json.load(open(p,'r',encoding='utf-8'))
acc=obj.get('channels',{}).get('feishu',{}).get('accounts',{}).get('feishu-main',{})
print(acc.get('appId',''))
print(acc.get('appSecret',''))
PY
}

CFG_PAIR="$(read_cfg)"
APP_ID_RAW="$(printf '%s\n' "$CFG_PAIR" | sed -n '1p')"
APP_SECRET_RAW="$(printf '%s\n' "$CFG_PAIR" | sed -n '2p')"
APP_ID="${FEISHU_APP_ID:-$APP_ID_RAW}"
APP_SECRET="${FEISHU_APP_SECRET:-$APP_SECRET_RAW}"
OPEN_ID="${FEISHU_OPEN_ID:-$OPEN_ID_ARG}"
VOICE="${VOICE_ARG:-${EDGE_TTS_VOICE:-zh-CN-YunxiNeural}}"

if [[ -z "$APP_ID" || -z "$APP_SECRET" ]]; then
  echo "missing Feishu app credentials (FEISHU_APP_ID / FEISHU_APP_SECRET)" >&2
  exit 3
fi
if [[ -z "$OPEN_ID" ]]; then
  echo "missing open_id (arg2 or FEISHU_OPEN_ID)" >&2
  exit 4
fi

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found" >&2
  exit 5
fi

EDGE_TTS_CMD=""
if command -v edge-tts >/dev/null 2>&1; then
  EDGE_TTS_CMD="edge-tts"
elif [[ -x "$HOME/Library/Python/3.14/bin/edge-tts" ]]; then
  EDGE_TTS_CMD="$HOME/Library/Python/3.14/bin/edge-tts"
else
  # 尝试 python 模块方式
  if python3 -m edge_tts --help >/dev/null 2>&1; then
    EDGE_TTS_CMD="python3 -m edge_tts"
  else
    echo "edge-tts not found. install with: python3 -m pip install --user edge-tts" >&2
    exit 6
  fi
fi

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
MP3="$TMP_DIR/voice.mp3"
OPUS_OGG="$TMP_DIR/voice.ogg"

# 1) 文本转语音
# shellcheck disable=SC2086
$EDGE_TTS_CMD --text "$TEXT" --voice "$VOICE" --write-media "$MP3" >/dev/null 2>&1

# 2) 转为飞书语音常用格式（opus in ogg）
ffmpeg -y -i "$MP3" -c:a libopus -ar 16000 -ac 1 -b:a 24k "$OPUS_OGG" >/dev/null 2>&1
DURATION_MS=$(python3 - <<'PY' "$OPUS_OGG"
import subprocess,sys
p=sys.argv[1]
out=subprocess.check_output([
  'ffprobe','-v','error','-show_entries','format=duration',
  '-of','default=nw=1:nk=1',p
],text=True).strip()
sec=float(out) if out else 0
print(int(sec*1000))
PY
)

# 3) 获取 tenant_access_token
TOK_JSON=$(curl -sS -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d "{\"app_id\":\"$APP_ID\",\"app_secret\":\"$APP_SECRET\"}")
TOK_CODE=$(python3 - <<'PY' "$TOK_JSON"
import json,sys
print(json.loads(sys.argv[1]).get('code'))
PY
)
if [[ "$TOK_CODE" != "0" ]]; then
  echo "$TOK_JSON" >&2
  exit 7
fi
TOKEN=$(python3 - <<'PY' "$TOK_JSON"
import json,sys
print(json.loads(sys.argv[1])['tenant_access_token'])
PY
)

# 4) 上传语音文件
UPLOAD_JSON=$(curl -sS -X POST 'https://open.feishu.cn/open-apis/im/v1/files' \
  -H "Authorization: Bearer $TOKEN" \
  -F 'file_type=opus' \
  -F 'file_name=voice.ogg' \
  -F "duration=$DURATION_MS" \
  -F "file=@$OPUS_OGG;type=audio/ogg")
UP_CODE=$(python3 - <<'PY' "$UPLOAD_JSON"
import json,sys
print(json.loads(sys.argv[1]).get('code'))
PY
)
if [[ "$UP_CODE" != "0" ]]; then
  echo "$UPLOAD_JSON" >&2
  exit 8
fi
FILE_KEY=$(python3 - <<'PY' "$UPLOAD_JSON"
import json,sys
print(json.loads(sys.argv[1])['data']['file_key'])
PY
)

CONTENT=$(python3 - <<'PY' "$FILE_KEY"
import json,sys
print(json.dumps({'file_key':sys.argv[1]}, ensure_ascii=False))
PY
)
CONTENT_ESCAPED=$(python3 - <<'PY' "$CONTENT"
import json,sys
print(json.dumps(sys.argv[1], ensure_ascii=False))
PY
)

# 5) 发送 audio 消息
SEND_JSON=$(curl -sS -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id' \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json; charset=utf-8' \
  -d "{\"receive_id\":\"$OPEN_ID\",\"msg_type\":\"audio\",\"content\":$CONTENT_ESCAPED}")
SEND_CODE=$(python3 - <<'PY' "$SEND_JSON"
import json,sys
print(json.loads(sys.argv[1]).get('code'))
PY
)
if [[ "$SEND_CODE" != "0" ]]; then
  echo "$SEND_JSON" >&2
  exit 9
fi

python3 - <<'PY' "$SEND_JSON" "$FILE_KEY"
import json,sys
j=json.loads(sys.argv[1])
out={
  'success': True,
  'message_id': (j.get('data') or {}).get('message_id'),
  'file_key': sys.argv[2]
}
print(json.dumps(out, ensure_ascii=False))
PY
