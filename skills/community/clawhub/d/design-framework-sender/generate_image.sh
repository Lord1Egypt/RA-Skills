#!/usr/bin/env bash
set -e

PROMPT="${1:-}"
ASPECT_RATIO="${2:-}"   # 可选，如 16:9 / 9:16 / 1:1 / 4:3 / 3:4 等
OUTPUT_DIR="$HOME/.openclaw/workspace/outputs/design-framework"
API_KEY=$(python3 -c "import json; print(json.load(open('$HOME/.openclaw/openclaw.json'))['models']['providers']['openrouter']['apiKey'])")

if [ -z "$PROMPT" ]; then
  echo "Usage: ./generate_image.sh \"<prompt>\" [aspect_ratio]" >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"
TMPFILE="/tmp/openclaw-img-response-$$.json"
FINAL_FILE="$OUTPUT_DIR/design-$(date +%s)-$RANDOM.jpg"
PROMPT_TMPFILE="/tmp/openclaw-img-prompt-$$.txt"
KEY_TMPFILE="/tmp/openclaw-img-key-$$.json"

# 无论成功还是失败，退出时都清理临时文件
trap 'rm -f "$TMPFILE" "$PROMPT_TMPFILE" "$KEY_TMPFILE"' EXIT

echo "[generate_image] 开始生成图片... aspect_ratio=${ASPECT_RATIO:-默认1:1}" >&2

# 将所有变量写入 json，供 Python 读取
printf '%s' "$PROMPT" > "$PROMPT_TMPFILE"
python3 -c "
import json
data = {
    'api_key': '''$API_KEY''',
    'prompt_file': '$PROMPT_TMPFILE',
    'tmp_file': '$TMPFILE',
    'final_file': '$FINAL_FILE',
    'aspect_ratio': '''$ASPECT_RATIO'''
}
print(json.dumps(data))
" > "$KEY_TMPFILE"

python3 << PYEOF
import json, urllib.request, sys

with open("$KEY_TMPFILE") as f:
    env = json.load(f)

api_key = env["api_key"]
aspect_ratio = env.get("aspect_ratio", "").strip()

with open(env["prompt_file"]) as f:
    prompt = f.read().strip()

# 支持的标准宽高比（OpenRouter image_config.aspect_ratio）
SUPPORTED_RATIOS = {
    "1:1", "2:3", "3:2", "3:4", "4:3",
    "4:5", "5:4", "9:16", "16:9", "21:9"
}

payload = {
    "model": "bytedance-seed/seedream-4.5",
    "modalities": ["image"],
    "max_tokens": 4096,
    "messages": [{"role": "user", "content": prompt}]
}

# 如果传入了合法的宽高比，加入 image_config
if aspect_ratio and aspect_ratio in SUPPORTED_RATIOS:
    payload["image_config"] = {"aspect_ratio": aspect_ratio}
    print(f"[generate_image] 使用宽高比: {aspect_ratio}", file=sys.stderr)
elif aspect_ratio:
    print(f"[generate_image] ⚠️ 不支持的宽高比 '{aspect_ratio}'，使用默认1:1", file=sys.stderr)

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
)

# timeout=90：生图正常 ~15s，给足余量，超时自动抛异常触发异常处理
with urllib.request.urlopen(req, timeout=90) as resp:
    with open(env["tmp_file"], "wb") as f:
        f.write(resp.read())
PYEOF

python3 << PYEOF2
import json, base64, sys, os
from PIL import Image

with open("$KEY_TMPFILE") as f:
    env = json.load(f)

with open(env["tmp_file"]) as f:
    d = json.load(f)

choices = d.get("choices", [])
if not choices:
    print("ERROR: no choices in response", file=sys.stderr)
    print(json.dumps(d)[:200], file=sys.stderr)
    sys.exit(1)

msg = choices[0].get("message", {})
b64_data = None
images = msg.get("images", [])
if images:
    url = images[0].get("image_url", {})
    if isinstance(url, dict):
        url = url.get("url", "")
    if isinstance(url, str) and url.startswith("data:image"):
        b64_data = url.split(",", 1)[1]

if not b64_data:
    print("ERROR: no image in response", file=sys.stderr)
    sys.exit(1)

final_file = env["final_file"]
raw_bytes = base64.b64decode(b64_data)

# 最小尺寸校验：小于 10KB 视为无效图片
if len(raw_bytes) < 10240:
    print(f"ERROR: 图片数据过小（{len(raw_bytes)} bytes），疑似截断或无效，已中止", file=sys.stderr)
    sys.exit(1)

with open(final_file, "wb") as f:
    f.write(raw_bytes)

img = Image.open(final_file)
if img.width < 64 or img.height < 64:
    os.remove(final_file)
    print(f"ERROR: 图片尺寸异常（{img.width}x{img.height}），已删除，中止", file=sys.stderr)
    sys.exit(1)

print(f"[generate_image] 图片已保存: {final_file}, 尺寸: {img.width}x{img.height}", file=sys.stderr)
print(final_file)
PYEOF2
