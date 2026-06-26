#!/usr/bin/env bash
set -e

FRAMEWORK_TEXT="${1:-}"
TARGET="${2:-}"

if [ -z "$TARGET" ]; then
  echo "Usage: ./send.sh \"<设计框架文本或文件路径>\" \"<telegram_user_id>\"" >&2
  exit 1
fi

BOT_TOKEN=$(python3 -c "import json; print(json.load(open('$HOME/.openclaw/openclaw.json'))['channels']['telegram']['botToken'])")

# 写入临时文件供 Python 读取
MSG_TMPFILE="/tmp/openclaw-send-msg-$$.txt"
KEY_TMPFILE="/tmp/openclaw-send-key-$$.json"

# 无论成功还是失败，退出时都清理临时文件（含 Bot Token 明文）
trap 'rm -f "$MSG_TMPFILE" "$KEY_TMPFILE"' EXIT

if [ -f "$FRAMEWORK_TEXT" ]; then
  # 用 cat 直接写入临时文件，避免命令替换吞末尾换行
  printf '%s\n' "📋 设计框架（来自群组设计需求）：" > "$MSG_TMPFILE"
  printf '\n' >> "$MSG_TMPFILE"
  cat "$FRAMEWORK_TEXT" >> "$MSG_TMPFILE"
else
  printf '%s' "📋 设计框架（来自群组设计需求）：

${FRAMEWORK_TEXT}" > "$MSG_TMPFILE"
fi

python3 -c "
import json
print(json.dumps({'bot_token': '''$BOT_TOKEN''', 'chat_id': '$TARGET'}))
" > "$KEY_TMPFILE"

# 分段发送，每段 ≤ 4000 字符
python3 << PYEOF
import json, urllib.request, time, sys

with open("$KEY_TMPFILE") as f:
    env = json.load(f)

with open("$MSG_TMPFILE") as f:
    text = f.read()

bot_token = env["bot_token"]
chat_id = env["chat_id"]
# 按字节安全切割，确保每段UTF-8编码后不超过Telegram 4096字节限制
chunk_byte_limit = 4000  # 留96字节余量

def split_by_bytes(text, limit):
    chunks = []
    while text:
        chunk = text[:limit]
        while len(chunk.encode('utf-8')) > limit:
            chunk = chunk[:-1]
        chunks.append(chunk)
        text = text[len(chunk):]
    return chunks

chunks = split_by_bytes(text, chunk_byte_limit)

for i, chunk in enumerate(chunks):
    payload = json.dumps({"chat_id": chat_id, "text": chunk}).encode()
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{bot_token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        result = json.load(resp)
    if not result.get("ok"):
        print(f"[send] 发送失败，Telegram响应: {result}", file=sys.stderr)
        sys.exit(1)
    if i < len(chunks) - 1:
        time.sleep(0.5)

print(f"✅ 设计框架文本已私发给 {chat_id}（共 {len(chunks)} 条）")
PYEOF

