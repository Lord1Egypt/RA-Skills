---
name: "claude-code-custom-model-proxy"
description: "Configure Claude Code to work with custom model providers (like MiniMax, OpenAI-compatible APIs). This skill should be used when users want to: use Claude Code with non-Anthropic models, set up a proxy to convert between Anthropic and OpenAI API formats, troubleshoot Claude Code connection issues with custom endpoints."
agent_created: true
version: "1.0.0"
---

# Claude Code Custom Model Proxy

This skill helps configure Claude Code to work with custom model providers that use OpenAI API format (like MiniMax) by setting up a proxy server that converts between Anthropic Messages API and OpenAI Chat Completions API.

## When to Use This Skill

- User wants to use Claude Code with a custom model provider (not Anthropic)
- User's model provider uses OpenAI Chat Completions API format
- User sees errors like "There's an issue with the selected model" in Claude Code
- User needs to convert between Anthropic API format and OpenAI API format

## Overview

Claude Code uses Anthropic Messages API format (`/v1/messages`), but many custom model providers (like MiniMax) use OpenAI Chat Completions API format (`/v1/chat/completions`). This skill provides a Python proxy server that:

1. Listens on `http://127.0.0.1:4002`
2. Accepts Anthropic API format requests from Claude Code
3. Converts to OpenAI API format
4. Forwards to the upstream provider
5. Converts responses back to Anthropic SSE format
6. Handles model validation, URL query strings, and UTF-8 encoding

## Quick Start

### 1. Configure Claude Code

Create or edit `~/.claude/settings.json`:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:4002",
    "ANTHROPIC_API_KEY": "fake-key-not-needed"
  }
}
```

Or use environment variables:
```bash
export ANTHROPIC_BASE_URL="http://127.0.0.1:4002"
export ANTHROPIC_API_KEY="fake-key"
```

### 2. Start the Proxy Server

```bash
python3 ~/.workbuddy/skills/claude-code-custom-model-proxy/scripts/claude_code_proxy.py
```

Or run in background:
```bash
nohup python3 ~/.workbuddy/skills/claude-code-custom-model-proxy/scripts/claude_code_proxy.py > /tmp/claude_proxy.log 2>&1 &
```

### 3. Start Claude Code

```bash
claude --model sonnet
```

## Proxy Server Configuration

Edit `scripts/claude_code_proxy.py` to configure:

- `UPSTREAM_HOST`: Your provider's API host (e.g., "api.53hk.cn")
- `UPSTREAM_PATH`: API path (e.g., "/v1/chat/completions")
- `API_KEY`: Your provider's API key
- `LISTEN_PORT`: Proxy listen port (default: 4002)
- Forced model name (line 44): Change `"MiniMax-M2.7-highspeed"` to your model

## Common Issues and Solutions

### Issue 1: "There's an issue with the selected model"

**Cause**: Claude Code validates model names locally before connecting to the API.

**Solution**: The proxy's `GET /v1/models` endpoint must return the model name Claude Code expects.

For `--model sonnet`, Claude Code expects `claude-sonnet-4-6` in the models list.

The proxy already includes common model names in its response. Add more if needed:

```python
models = {
    "data": [
        {"type": "model", "id": "claude-sonnet-4-6", "display_name": "Claude Sonnet 4.6"},
        {"type": "model", "id": "claude-opus-4-5", "display_name": "Claude Opus 4.5"},
        # Add more models as needed
    ]
}
```

### Issue 2: 404 errors in proxy logs

**Cause**: Claude Code sends requests with query strings (e.g., `POST /v1/messages?beta=true`), but the proxy only checks `self.path == "/v1/messages"`.

**Solution**: The proxy now uses `urlparse()` to extract the path without query string:

```python
from urllib.parse import urlparse

parsed_path = urlparse(self.path)
path = parsed_path.path  # This removes ?beta=true
```

### Issue 3: Chinese characters appear as garbled text (乱码)

**Cause**: Incorrect handling of UTF-8 encoding in SSE streaming.

**Solution**: Use byte buffer instead of string buffer:

```python
buffer = b""  # Byte buffer
for chunk in r.iter_content(chunk_size=None, decode_unicode=False):
    if chunk:
        buffer += chunk
        while b"\n" in buffer:
            line_bytes, buffer = buffer.split(b"\n", 1)
            line = line_bytes.strip().decode("utf-8", errors="replace")
```

### Issue 4: Connection refused

**Cause**: Proxy server is not running.

**Solution**: Start the proxy server before starting Claude Code. Check with:
```bash
lsof -i :4002
```

## API Format Conversion

### Anthropic Messages API (Claude Code) → OpenAI Chat Completions (Provider)

**Request conversion** (`anthropic_to_openai()`):
- `messages` array: Extract text from `content` blocks
- `max_tokens` → `max_tokens`
- `temperature` → `temperature`
- `stream: true` (always enabled)

**Response conversion** (`openai_to_anthropic()`):
- OpenAI SSE chunks → Anthropic SSE events:
  - `message_start`
  - `content_block_start`
  - `content_block_delta`
  - `content_block_stop`
  - `message_delta`
  - `message_stop`

## Troubleshooting

### Check proxy logs

```bash
tail -f /tmp/claude_proxy.log
```

### Test proxy endpoints

```bash
# Test models endpoint
curl -s http://127.0.0.1:4002/v1/models | python3 -m json.tool

# Test messages endpoint
curl -X POST http://127.0.0.1:4002/v1/messages \
  -H "Content-Type: application/json" \
  -d '{"model":"claude-sonnet-4-6","messages":[{"role":"user","content":"Hello"}],"max_tokens":100}'
```

### Check Claude Code debug logs

```bash
ls -lt ~/.claude/debug/*.txt | head -1
tail -50 ~/.claude/debug/<latest>.txt
```

## File Structure

```
~/.workbuddy/skills/claude-code-custom-model-proxy/
├── SKILL.md                    # This file
└── scripts/
    └── claude_code_proxy.py    # Proxy server
```

## Advanced Configuration

### Change forced model

In `claude_code_proxy.py`, line 44:
```python
"model": "MiniMax-M2.7-highspeed",  # Change this to your model
```

### Change listen port

In `claude_code_proxy.py`:
```python
LISTEN_PORT = 4002  # Change to your preferred port
```

Then update `ANTHROPIC_BASE_URL` accordingly.

### Add retry logic for 429 errors

The proxy already includes retry logic (`call_upstream_with_retry()`). Configure:
- `MAX_RETRIES`: Maximum retry attempts (default: 3)
- `BASE_WAIT_SECONDS`: Base wait time between retries (default: 10)
