#!/usr/bin/env python3
"""
Nex-N2-Pro Image Analyzer — main execution script.

Usage:
  python3 analyze.py --image-base64 <b64> [--detail medium]
  python3 analyze.py --image-url <url>
  python3 analyze.py --image-path <path>

Environment:
  NEXN2_API_KEY        required
  NEXN2_BASE_URL        default https://api.siliconflow.cn/v1
  NEXN2_MODEL_NAME      default nex-agi/Nex-N2-Pro
  NEXN2_PROMPT_TEMPLATE  optional custom prompt
  NEXN2_IMAGE_COMPRESS  default true
  NEXN2_CACHE_ENABLE    default true
  NEXN2_CACHE_TTL_DAYS  default 7
  NEXN2_TIMEOUT_MS      default 30000
"""

import argparse, hashlib, json, os, sys, time, urllib.request, io, base64
from datetime import datetime, timedelta, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CACHE_DIR = os.path.join(SKILL_DIR, "cache")

# ── helpers ──────────────────────────────────────────────

def _env(key, default=None):
    return os.environ.get(key, default)

def _md5(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _detect_format(data: bytes) -> str:
    """Detect image format from magic bytes. Returns 'jpeg','png','webp','gif','bmp' or None."""
    if data[:3] == b'\xff\xd8\xff':
        return 'jpeg'
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return 'png'
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return 'webp'
    if data[:6] in (b'GIF87a', b'GIF89a'):
        return 'gif'
    if data[:2] == b'BM':
        return 'bmp'
    return None

# ── cache ────────────────────────────────────────────────

def _cache_path(md5_hash: str) -> str:
    return os.path.join(CACHE_DIR, f"{md5_hash}.json")

def _cache_get(md5_hash: str) -> dict | None:
    if _env("NEXN2_CACHE_ENABLE", "true").lower() != "true":
        return None
    path = _cache_path(md5_hash)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            entry = json.load(f)
        expires = datetime.fromisoformat(entry["expires_at"])
        if datetime.now(timezone.utc) > expires:
            os.remove(path)
            return None
        return entry
    except Exception:
        return None

def _cache_set(md5_hash: str, content: str, model: str, tokens: int):
    if _env("NEXN2_CACHE_ENABLE", "true").lower() != "true":
        return
    os.makedirs(CACHE_DIR, exist_ok=True)
    ttl_days = int(_env("NEXN2_CACHE_TTL_DAYS", "7"))
    now = datetime.now(timezone.utc)
    entry = {
        "content": content,
        "cached_at": now.isoformat(),
        "expires_at": (now + timedelta(days=ttl_days)).isoformat(),
        "model": model,
        "tokens_used": tokens,
    }
    with open(_cache_path(md5_hash), "w") as f:
        json.dump(entry, f, ensure_ascii=False)

# ── image loading ────────────────────────────────────────

def _load_image_bytes(args) -> bytes:
    """Load raw image bytes from whichever source was provided."""
    if args.image_base64:
        import base64
        raw = args.image_base64
        # strip data URI prefix if present
        if "," in raw and raw.startswith("data:"):
            raw = raw.split(",", 1)[1]
        return base64.b64decode(raw)

    if args.image_url:
        req = urllib.request.Request(args.image_url, headers={"User-Agent": "OpenClaw-NexN2/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read()

    if args.image_path:
        with open(args.image_path, "rb") as f:
            return f.read()

    raise ValueError("必须提供 image_base64 / image_url / image_path 中的一个")

# ── compression ──────────────────────────────────────────

def _get_jpeg_dims(data: bytes) -> tuple:
    """Extract JPEG dimensions from header without Pillow. Returns (w, h) or (0, 0)."""
    end = min(len(data), 65536)
    i = 2
    while i < end - 8:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker == 0xDA:  # SOS
            break
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            if i + 9 <= end:
                h = int.from_bytes(data[i + 5:i + 7], 'big')
                w = int.from_bytes(data[i + 7:i + 9], 'big')
                return (w, h)
        length = int.from_bytes(data[i + 2:i + 4], 'big')
        i += 2 + length
    return (0, 0)

def _compress(data: bytes, fmt: str) -> str:
    """Compress image and return base64-encoded string.

    Strategy: Pillow preferred -> pure-Python JPEG pass-through -> raw base64.
    """
    if _env("NEXN2_IMAGE_COMPRESS", "true").lower() != "true":
        return base64.b64encode(data).decode()

    # Strategy 1: Pillow (best quality/size)
    try:
        from PIL import Image as PILImage
        img = PILImage.open(io.BytesIO(data))
        w, h = img.size
        max_dim = 1920
        if max(w, h) > max_dim:
            ratio = max_dim / max(w, h)
            img = img.resize((int(w * ratio), int(h * ratio)), PILImage.LANCZOS)
        buf = io.BytesIO()
        save_fmt = "JPEG" if fmt in ("jpeg", "jpg") else fmt.upper()
        if save_fmt == "JPEG":
            img = img.convert("RGB")
        img.save(buf, format=save_fmt, quality=85)
        result = base64.b64encode(buf.getvalue()).decode()
        raw_b64 = base64.b64encode(data).decode()
        if len(result) < len(raw_b64) * 0.95:
            return result
    except (ImportError, Exception):
        pass

    # Strategy 2: JPEG pass-through (no Pillow needed for JPEG)
    if fmt == "jpeg":
        return base64.b64encode(data).decode()

    # Strategy 3: raw base64
    return base64.b64encode(data).decode()

# ── prompt template ──────────────────────────────────────

DEFAULT_PROMPT = """请严格按照以下格式输出分析结果，不要遗漏任何内容：

【OCR文字提取】
完整提取图片中所有可见文字，保留原文的段落、列表、表格排版结构，表格自动转为 Markdown 格式；不遗漏标题、注释、小字标注。

【画面内容总结】
1. 核心主题：一句话概括图片是什么、用途是什么
2. 元素与布局：描述图片的整体结构、分区、关键视觉元素
3. 关键信息提炼：提炼图片中最核心的结论、数据、逻辑关系"""

def _get_prompt() -> str:
    return _env("NEXN2_PROMPT_TEMPLATE", DEFAULT_PROMPT)

# ── API call ─────────────────────────────────────────────

def _call_api(img_b64: str, fmt: str) -> tuple[str | None, int, str]:
    """Call the Nex-N2-Pro API. Returns (content, tokens, model)."""
    api_key = _env("NEXN2_API_KEY")
    if not api_key:
        raise RuntimeError("图片分析功能未配置 API Key，请联系管理员设置 NEXN2_API_KEY 环境变量")

    base_url = _env("NEXN2_BASE_URL", "https://api.siliconflow.cn/v1").rstrip("/")
    model = _env("NEXN2_MODEL_NAME", "nex-agi/Nex-N2-Pro")
    timeout = int(_env("NEXN2_TIMEOUT_MS", "60000")) / 1000

    mime_map = {"jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp",
                "gif": "image/gif", "bmp": "image/bmp"}
    mime = mime_map.get(fmt, "image/jpeg")

    payload = {
        "model": model,
        "temperature": 0.1,
        "max_tokens": 4096,
        "messages": [
            {"role": "system", "content": "你是一个专业的图片分析助手。"},
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{img_b64}"}},
                    {"type": "text", "text": _get_prompt()},
                ],
            },
        ],
    }

    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        return None, 0, _parse_error(err_body)
    except Exception as e:
        raise RuntimeError(f"图片分析服务暂时不可用，请稍后重试: {e}") from e

    content = body.get("choices", [{}])[0].get("message", {}).get("content", "")
    tokens = body.get("usage", {}).get("total_tokens", 0)
    return content, tokens, model

def _parse_error(err_body: str) -> str:
    """Try to classify the API error."""
    try:
        err = json.loads(err_body)
        msg = str(err.get("error", {}).get("message", err_body)).lower()
    except Exception:
        msg = err_body.lower()

    if any(k in msg for k in ("safety", "moderation", "content_filter", "violation", "违规")):
        return "图片包含违规内容，无法分析"
    if any(k in msg for k in ("invalid_image", "unsupported_format", "decode")):
        return "暂不支持该图片格式，请使用 JPG/PNG/WebP 格式"
    return "图片分析服务暂时不可用，请稍后重试"

def _call_api_with_retry(img_b64: str, fmt: str) -> tuple[str | None, int, str]:
    """Call API with 1 retry."""
    last_error = None
    for attempt in range(2):
        try:
            return _call_api(img_b64, fmt)
        except RuntimeError as e:
            last_error = e
            if attempt == 0:
                time.sleep(2)
    raise last_error  # type: ignore[misc]

# ── output ───────────────────────────────────────────────

def _success(content: str, model: str, tokens: int, cached: bool, elapsed_ms: int):
    return json.dumps({
        "success": True,
        "content": content,
        "metadata": {
            "model": model,
            "tokens_used": tokens,
            "cached": cached,
            "process_time_ms": elapsed_ms,
        },
    }, ensure_ascii=False)

def _fail(message: str):
    return json.dumps({
        "success": False,
        "content": message,
        "metadata": {},
    }, ensure_ascii=False)

# ── main ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Nex-N2-Pro Image Analyzer")
    parser.add_argument("--image-base64", help="Base64 encoded image")
    parser.add_argument("--image-url", help="Public image URL")
    parser.add_argument("--image-path", help="Local image file path")
    parser.add_argument("--detail", default="medium", choices=["low", "medium", "high"])
    args = parser.parse_args()

    t0 = time.time()

    # 1. load + validate
    try:
        data = _load_image_bytes(args)
    except ValueError as e:
        print(_fail(str(e)), flush=True)
        sys.exit(1)
    except Exception as e:
        print(_fail(f"无法读取图片: {e}"), flush=True)
        sys.exit(1)

    fmt = _detect_format(data)
    if fmt is None:
        print(_fail("暂不支持该图片格式，请使用 JPG/PNG/WebP 格式"), flush=True)
        sys.exit(0)

    # 2. cache check
    h = _md5(data)
    cached_entry = _cache_get(h)
    if cached_entry:
        elapsed = int((time.time() - t0) * 1000)
        print(_success(cached_entry["content"], cached_entry.get("model", "cached"),
                       cached_entry.get("tokens_used", 0), True, elapsed), flush=True)
        return

    # 3. compress
    try:
        img_b64 = _compress(data, fmt)
    except Exception:
        import base64
        img_b64 = base64.b64encode(data).decode()

    # 4. call API (with retry)
    try:
        content, tokens, model = _call_api_with_retry(img_b64, fmt)
    except RuntimeError as e:
        print(_fail(str(e)), flush=True)
        sys.exit(0)

    # 5. validate output
    if not content or not content.strip():
        print(_fail("图片分析完成，但模型未返回有效内容，请尝试更换图片"), flush=True)
        sys.exit(0)

    # If API returned an error message
    if isinstance(content, str) and any(content.strip().startswith(p) for p in
        ("图片分析服务暂时不可用", "暂不支持该图片格式", "图片包含违规内容")):
        print(_fail(content), flush=True)
        sys.exit(0)

    # 6. cache + output
    _cache_set(h, content, model, tokens)
    elapsed = int((time.time() - t0) * 1000)
    print(_success(content, model, tokens, False, elapsed), flush=True)

if __name__ == "__main__":
    main()
