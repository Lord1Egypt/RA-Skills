#!/usr/bin/env bash
set -e

# 用法：send_text.sh <消息文件路径> <telegram_chat_id>
MSG_FILE="${1:-}"
TARGET="${2:-}"

if [ -z "$MSG_FILE" ] || [ -z "$TARGET" ]; then
  echo "Usage: ./send_text.sh <msg_file> <chat_id>" >&2
  exit 1
fi

BOT_TOKEN=$(python3 -c "import json; print(json.load(open('$HOME/.openclaw/openclaw.json'))['channels']['telegram']['botToken'])")

KEY_TMPFILE="/tmp/openclaw-sendtext-key-$$.json"

# 无论成功还是失败，退出时都清理临时文件（含 Bot Token 明文）
trap 'rm -f "$KEY_TMPFILE"' EXIT

python3 -c "
import json
print(json.dumps({'bot_token': '''$BOT_TOKEN''', 'chat_id': '$TARGET'}))
" > "$KEY_TMPFILE"

python3 << PYEOF
import json, urllib.request, time, sys

with open("$KEY_TMPFILE") as f:
    env = json.load(f)

with open("$MSG_FILE") as f:
    text = f.read()

bot_token = env["bot_token"]
chat_id = env["chat_id"]
# 按字节安全切割，确保每段UTF-8编码后不超过Telegram 4096字节限制
chunk_byte_limit = 4000  # 留96字节余量

def split_by_bytes(text, limit):
    chunks = []
    while text:
        # 贪心取尽可能多的字符，但字节数不超过limit
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
        print(f"[send_text] 发送失败，Telegram响应: {result}", file=sys.stderr)
        sys.exit(1)
    if i < len(chunks) - 1:
        time.sleep(0.5)

print(f"[send_text] 已发送至 {chat_id}，共 {len(chunks)} 条")
PYEOF

