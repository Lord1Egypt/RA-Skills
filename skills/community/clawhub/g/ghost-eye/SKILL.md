---
name: "ghost-eye"
description: "Ghost Eye 👁️ — Let any pure-text LLM see images through any vision model. OCR + visual summary in one shot."
metadata:
  {
    "openclaw":
      {
        "emoji": "👁️",
        "requires": { "env": ["NEXN2_API_KEY"] },
        "primaryEnv": "NEXN2_API_KEY",
      },
  }
---

# Ghost Eye 👁️

Give your text-only LLM the power to see. Ghost Eye is a lightweight image preprocessing bridge: when an image enters the conversation, it calls any OpenAI-compatible vision model (default: `nex-agi/Nex-N2-Pro`), produces a structured plain-text output (full OCR + visual summary), and feeds it back into the conversation — so your pure-text model can "see" without ever touching a multimodal API.

## What it does

```
User sends image → Ghost Eye detects → vision model analyzes → OCR text + scene summary → your LLM answers
```

## Two modes

### Mode 1: Auto-preprocess (recommended)
When `multimodalPreprocess` is configured, Ghost Eye fires automatically on any inbound image. The user never knows it's there — they just get answers about images.

### Mode 2: Tool-call mode
Registered as `analyze_image_by_nexn2` tool (name stays for backward compatibility). Your LLM calls it explicitly when it sees an image. Add this to the system prompt:

> When the user sends an image, screenshot, photo, or document scan, call the analyze_image_by_nexn2 tool to extract text and describe the image, then answer based on the returned content.

## Workflow

### Step 1: Receive image

**Priority: `--image-path` > `--image-url` > `--image-base64`**

⛔ Always prefer `--image-path` to avoid command-line `Argument list too long` errors with large base64 strings. Only fall back to `--image-url` or `--image-base64` when no local path is available.

```bash
# Preferred: local file path (no size limit)
python3 {baseDir}/scripts/analyze.py --image-path "<absolute path>"

# Fallback: public URL
python3 {baseDir}/scripts/analyze.py --image-url "<url>"

# Last resort: base64 (small images only, <50KB)
python3 {baseDir}/scripts/analyze.py --image-base64 "<base64>"
```

The script handles:
- Format validation (JPG/PNG/WebP/GIF/BMP via magic bytes)
- Cache check / read / write (MD5-based, 7-day TTL)
- Image compression (Pillow, max 1920px longest edge, quality 85%)
- API call with 1 automatic retry
- Structured JSON output

### Step 2: Parse JSON output

Success:
```json
{"success": true, "content": "【OCR文字提取】\n...\n\n【画面内容总结】\n...", "metadata": {"model": "...", "tokens_used": 1200, "cached": false, "process_time_ms": 1500}}
```

Error:
```json
{"success": false, "content": "error message", "metadata": {}}
```

Pass `content` directly into the LLM conversation context.

### Step 3: Caching

- Cache directory: `{baseDir}/cache/` (auto-created)
- Cache key: MD5 hash of raw image bytes
- TTL: 7 days (`NEXN2_CACHE_TTL_DAYS`)
- Clear cache: delete all `.json` files in `{baseDir}/cache/`
- Toggle: `NEXN2_CACHE_ENABLE=true/false`

## Environment variables

| Variable | Required | Default |
|----------|----------|---------|
| NEXN2_API_KEY | ✅ Yes | — |
| NEXN2_BASE_URL | No | https://api.siliconflow.cn/v1 |
| NEXN2_MODEL_NAME | No | nex-agi/Nex-N2-Pro |
| NEXN2_PROMPT_TEMPLATE | No | Built-in structured template |
| NEXN2_IMAGE_COMPRESS | No | true |
| NEXN2_CACHE_ENABLE | No | true |
| NEXN2_CACHE_TTL_DAYS | No | 7 |
| NEXN2_TIMEOUT_MS | No | 30000 |

If `NEXN2_API_KEY` is not set, returns a friendly Chinese error message.

## Error handling

| Scenario | Returns |
|----------|---------|
| Network/API failure (after retry) | Friendly "service unavailable" message |
| Unsupported format | "Please use JPG/PNG/WebP format" |
| Content safety block | "Image flagged by safety filter" |
| Empty model output | "No content returned, try a different image" |

⚠️ Errors never crash the conversation — structured JSON response is always returned.

## Setup

In `openclaw.json` under `skills.entries`:

```json5
"ghost-eye": {
  "enabled": true,
  "apiKey": { "source": "env", "provider": "default", "id": "NEXN2_API_KEY" },
  "env": {
    "NEXN2_BASE_URL": "https://api.siliconflow.cn/v1",
    "NEXN2_MODEL_NAME": "nex-agi/Nex-N2-Pro",
    "NEXN2_IMAGE_COMPRESS": "true",
    "NEXN2_CACHE_ENABLE": "true",
    "NEXN2_CACHE_TTL_DAYS": "7",
    "NEXN2_TIMEOUT_MS": "30000"
  }
}
```

For `multimodalPreprocess` auto-mode, see `references/multimodal-config.md`.

## Supported platforms

- SiliconFlow (default, China-accessible)
- OpenRouter
- Any OpenAI-compatible chat completions endpoint

## Safety

- ⛔ Image base64 is never logged or written to conversation text
- ⛔ API key is never hardcoded
- ⛔ Temporary files are cleaned up immediately after processing
- ⚠️ Output is always plain text / Markdown — never binary, never images
