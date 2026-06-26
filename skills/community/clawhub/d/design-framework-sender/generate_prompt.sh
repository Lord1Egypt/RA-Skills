#!/usr/bin/env bash
set -e

FRAMEWORK_FILE="${1:-}"
IMAGE_FILE="${2:-}"

if [ -z "$FRAMEWORK_FILE" ]; then
  echo "Usage: ./generate_prompt.sh <framework_file> [image_file]" >&2
  exit 1
fi

API_KEY=$(python3 -c "import json; print(json.load(open('$HOME/.openclaw/openclaw.json'))['models']['providers']['openrouter']['apiKey'])")

echo "[generate_prompt] 开始生成图片 prompt..." >&2

# 将变量写入临时 json，供 Python 读取（避免 heredoc 变量展开问题）
ENV_FILE="/tmp/openclaw-genprompt-env-$$.json"

# 无论成功还是失败，退出时都清理临时文件（含 API Key 明文）
trap 'rm -f "$ENV_FILE"' EXIT

python3 -c "
import json, sys
data = {
    'api_key': '''$API_KEY''',
    'framework_file': '''$FRAMEWORK_FILE''',
    'image_file': '''$IMAGE_FILE'''
}
print(json.dumps(data))
" > "$ENV_FILE"

python3 << PYEOF
import json, base64, sys, re, urllib.request

with open("$ENV_FILE") as f:
    env = json.load(f)

api_key = env["api_key"]
framework_file = env["framework_file"]
image_file = env["image_file"]

framework = open(framework_file).read() if framework_file else ""
content = []

# ──────────────────────────────────────────────
# 降级函数：直接用设计框架文本提炼 prompt（不调用 API）
# ──────────────────────────────────────────────
def fallback_prompt(framework_text):
    """从设计框架提取关键段落拼成可用的生图 prompt（最多 400 字）。"""
    print("[generate_prompt] ⚠️  启用降级模式：直接用设计框架生成 prompt", file=sys.stderr)
    # 保留「视觉风格」「版式结构」「设计元素」「文案层级」相关行
    keep_sections = ["视觉风格", "版式结构", "设计元素", "文案层级", "字体", "配色", "构图", "光"]
    lines = framework_text.splitlines()
    selected = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if any(kw in line for kw in keep_sections):
            selected.append(line)
        elif len(selected) > 0 and len(line) > 8:
            selected.append(line)
        if len("".join(selected)) >= 350:
            break
    prompt = " ".join(selected)[:400].strip()
    if not prompt:
        # 终极兜底：截取框架前 300 字
        prompt = re.sub(r'\s+', ' ', framework_text)[:300].strip()
    return prompt
# ──────────────────────────────────────────────

if image_file and image_file.strip():
    try:
        with open(image_file, "rb") as f:
            img_data = base64.b64encode(f.read()).decode()
        ext = image_file.lower().split(".")[-1]
        mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}.get(ext, "image/jpeg")
        content.append({"type": "image_url", "image_url": {"url": f"data:{mime};base64,{img_data}"}})
        has_image = True
        print("[generate_prompt] 已加载参考图", file=sys.stderr)
    except Exception as e:
        print(f"[generate_prompt] 图片读取失败: {e}", file=sys.stderr)
        has_image = False
else:
    has_image = False

if has_image:
    text = f"""你是专业平面设计师和AI绘图prompt专家。

根据参考图和设计框架，生成一段高质量中文图片生成prompt。

设计框架：
{framework}

要求：
1. 分析参考图的风格、配色、构图、光效、核心元素，融入prompt
2. 严格遵循设计框架的要求
3. 中文输出，150-300字
4. 只输出prompt纯文本，不要标题、序号、markdown格式、解释说明"""
else:
    text = f"""你是专业平面设计师和AI绘图prompt专家。

根据设计框架生成一段高质量中文图片生成prompt。

设计框架：
{framework}

要求：
1. 严格遵循设计框架的风格、配色、文案、构图要求
2. 中文输出，150-300字
3. 只输出prompt纯文本，不要标题、序号、markdown格式、解释说明"""

content.append({"type": "text", "text": text})

payload = {
    "model": "qwen/qwen2.5-vl-32b-instruct",
    "messages": [{"role": "user", "content": content}],
    "max_tokens": 600
}

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps(payload).encode(),
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
)

# ── API 调用（网络超时或异常 → 降级）──
try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.load(resp)
except Exception as e:
    print(f"[generate_prompt] ⚠️  API 请求异常: {e}，启用降级", file=sys.stderr)
    print(fallback_prompt(framework))
    sys.exit(0)

choices = result.get("choices", [])
if not choices:
    # 可能是内容过滤（content filtered）或账户余额不足等原因导致空 choices
    print(f"[generate_prompt] ⚠️  API 返回空 choices（可能触发内容过滤）: {str(result)[:200]}", file=sys.stderr)
    print(fallback_prompt(framework))
    sys.exit(0)

raw = (choices[0].get("message") or {}).get("content") or ""
raw = raw.strip()

# ① 去除 markdown 代码块包裹（\x60 = 反引号，避免 bash heredoc 解析冲突）
clean = re.sub(r'^\x60{3}[a-zA-Z]*\s*\n?', '', raw)
clean = re.sub(r'\n?\x60{3}\s*$', '', clean)
clean = re.sub(r'\x60{3}', '', clean)  # 兜底清除残余代码块标记

# ② 去除其他 markdown 格式
clean = re.sub(r'\*\*.*?\*\*\s*[：:]\s*', '', clean)
clean = re.sub(r'^#{1,6}\s+', '', clean, flags=re.MULTILINE)
clean = re.sub(r'\*\*|\*|__', '', clean)
clean = re.sub(r'^\s*[-•]\s+', '', clean, flags=re.MULTILINE)
clean = re.sub(r'\n{3,}', '\n\n', clean)
clean = clean.strip()

if not clean:
    # 模型返回了 choices 但内容为空（finish_reason=content_filter 等）
    print("[generate_prompt] ⚠️  模型返回内容为空（内容过滤？），启用降级", file=sys.stderr)
    print(fallback_prompt(framework))
    sys.exit(0)

print(clean)
PYEOF
