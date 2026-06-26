---
name: cliproxy-media
description: Analyze images (jpg, png, gif, webp) and PDFs via CLIProxyAPI — a Claude Max proxy that routes requests through your subscription at zero extra cost. Use this skill whenever you need to analyze, describe, or extract information from an image or photo ("analyze image", "describe photo", "what is in this picture"), read or summarize a PDF document ("read PDF", "summary of this document"), or process any media file via a CLIProxy-compatible endpoint ("process media via proxy", "cliproxy vision", "cliproxy media"). NEVER use the built-in `image` or `pdf` tools when using CLIProxyAPI — they fall back to direct Anthropic API which requires separate credits. Use this skill instead for all vision and document analysis tasks.
---

# cliproxy-media

**Source:** https://github.com/bencoremans/site/tree/main/skills/cliproxy-media

Analyze images and PDFs via CLIProxyAPI (Claude Max subscription, zero extra cost).

## Setup

Set the endpoint to your CLIProxy instance:

```bash
export CLIPROXY_URL=http://your-host:8317/v1/messages
```

For Docker setups, replace `your-host` with your container hostname (e.g. `cliproxyapi`, `localhost`, or the container IP).

## Quick start

```bash
# Analyze an image
python3 skills/cliproxy-media/scripts/analyze.py /path/to/image.jpg "What is in this image?"

# Read a PDF
python3 skills/cliproxy-media/scripts/analyze.py /path/to/document.pdf "Give a summary"

# Compare multiple images
python3 skills/cliproxy-media/scripts/analyze.py img1.jpg img2.jpg "Compare these images"

# With streaming (output appears immediately)
python3 skills/cliproxy-media/scripts/analyze.py --stream image.jpg "Describe in detail"

# With system prompt
python3 skills/cliproxy-media/scripts/analyze.py --system "You are a medical expert" scan.jpg "What do you see?"

# With higher token limit
python3 skills/cliproxy-media/scripts/analyze.py --max-tokens 4096 document.pdf "Extensive analysis"
```

## What works ✅ / What doesn't ❌

### ✅ Supported file types

| Type | Format | Note |
|------|--------|------|
| Image | `.jpg` / `.jpeg` | Requires valid JPEG data |
| Image | `.png` | Fully supported |
| Image | `.gif` | Fully supported |
| Image | `.webp` | Fully supported |
| Document | `.pdf` | Base64-encoded, via `document` content type |
| Image via URL | `http://` / `https://` | Direct URL reference, no download needed |

**Multiple files at once:** Provide multiple paths before the question. Max ~100 per request (Anthropic limit).

### ❌ Not supported

- **Office files** (`.docx`, `.xlsx`, `.pptx`) — Workaround: convert to PDF
- **Audio** (`.mp3`, `.wav`, `.ogg`) — Use Whisper for transcription
- **Video** (`.mp4`, `.mov`, `.avi`) — Not supported by the model
- **Other document types** (`.txt`, `.html`, `.md` as document) — Send text directly as a string

## ⚠️ System prompt warning

CLIProxyAPI accepts **only** the array notation for system prompts. The string notation is **silently ignored** — the model does not see it, but you also won't get an error message!

```python
# ❌ DOES NOT WORK — ignored without error message
payload["system"] = "You are an expert."

# ✅ WORKS — always use array notation
payload["system"] = [{"type": "text", "text": "You are an expert."}]
```

The `--system` argument in `analyze.py` automatically uses the correct array notation.

## Configuration (env vars)

| Variable | Default | Description |
|----------|---------|-------------|
| `CLIPROXY_URL` | `http://localhost:8317/v1/messages` | Full endpoint URL |
| `CLIPROXY_MODEL` | `claude-sonnet-4-6` | Model to use |

Example:
```bash
export CLIPROXY_URL=http://localhost:8317/v1/messages
export CLIPROXY_MODEL=claude-opus-4-6
python3 skills/cliproxy-media/scripts/analyze.py image.jpg "question"
```

## Additional options

```
--stream          Streaming output via SSE (output appears immediately)
--system TEXT     System prompt (automatically sent as array)
--max-tokens N    Maximum output tokens (default: 1024)
--model MODEL     Model override (overrides CLIPROXY_MODEL)
--url URL         Endpoint override (overrides CLIPROXY_URL)
```

## Compatibility

This script works with any API that supports the Anthropic Messages format:

| Provider | Compatible | Note |
|----------|-----------|------|
| **CLIProxyAPI** | ✅ Yes | Primarily tested, system prompt array required |
| **OpenRouter** | ✅ Yes | Use Bearer token instead of `x-api-key: dummy` |
| **LiteLLM** | ✅ Yes | As proxy for Anthropic format |
| **Anthropic direct** | ✅ Yes | Use `ANTHROPIC_API_KEY` as x-api-key |

**Note for non-CLIProxy endpoints:** Some proxies do accept string notation for system prompts. Always use array notation for maximum compatibility.

## Known limitations of CLIProxyAPI

- `temperature` and `top_p` may **not** be used at the same time (HTTP 400)
- PDF as document with URL source does not work (`Unable to download the file`)
- Only `claude-sonnet-4-6` and `claude-opus-4-6` available (haiku is deprecated)
- `inference_geo` is always `not_available` in the response

## Direct Python API

If you want to call the script from your own Python code:

```python
import subprocess, json

result = subprocess.run(
    ["python3", "skills/cliproxy-media/scripts/analyze.py", "image.jpg", "Describe this"],
    capture_output=True, text=True
)
print(result.stdout)
```

Or use the built-in exec tool:
```
exec: python3 skills/cliproxy-media/scripts/analyze.py /path/to/image.jpg "question"
```
