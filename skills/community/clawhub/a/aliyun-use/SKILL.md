---
name: aliyun-use
version: 0.1.0
description: "Aliyun Bailian(百炼) for LLM chat, and language translation. Use when you need to  generate code, generate text with LLMs, or translate between languages."
metadata:
  openclaw:
    requires:
      env:
        - ALIYUN_BAILIAN_API_KEY
    primaryEnv: ALIYUN_BAILIAN_API_KEY
    os:
      - linux
      - darwin
      - win32
---

# Aliyun Bailian(百炼) for OpenClaw

Call Alibaba Cloud Bailian (百炼) LLM models via the DashScope API.

## Setup

Get your API key from: https://bailian.console.aliyun.com/ 

Set the environment variable:
```bash
export ALIYUN_BAILIAN_API_KEY="your-api-key"
export ALIYUN_BAILIAN_API_HOST="https://coding.dashscope.aliyuncs.com/apps/anthropic"  # optional, default provided
```

## CLI Commands

```bash
python -m scripts chat --model qwen3.5-plus --messages '[{"role": "user", "content": "Hello"}]'
python -m scripts translate --text "Hello" --target-lang zh
python -m scripts models
```

## Commands Overview

| Command | What it does |
|---------|-------------|
| `chat` | General-purpose chat completion with Qwen, GLM, Kimi, MiniMax models |
| `translate` | Translate text between languages |
| `models` | List all available models |

## Chat

General-purpose chat completion via DashScope Anthropic API.

### Usage
```bash
python -m scripts chat --model qwen3.5-plus --messages '[{"role": "user", "content": "Hello"}]'
```

### Parameters

- `--model` (string, optional) — Model name. Default: `qwen3.5-plus`
- `--messages` (string, required) — JSON array of `{role, content}`. Roles: `system`, `user`, `assistant`
- `--temperature` (float, optional) — Sampling temperature 0-1. Default: `0.7`
- `--max-tokens` (integer, optional) — Max tokens to generate. Default: `2048`
- `--stream` (boolean, optional) — Enable streaming. Default: `false`

### Available Models

**Flagship:** `qwen3.5-plus`, `qwen3-max-2026-01-23`

**Coder:** `qwen3-coder-next`, `qwen3-coder-plus`

**Other:** `glm-5`, `glm-4.7`, `kimi-k2.5`, `MiniMax-M2.5`

## Translate

Translate text between languages using the LLM.

### Usage
```bash
python -m scripts translate --text "Hello" --target-lang zh
python -m scripts translate --text "你好" --target-lang en --source-lang zh
```

### Parameters

- `--text` (string, required) — Text to translate
- `--target-lang` (string, optional) — Target language code. Default: `en`
- `--source-lang` (string, optional) — Source language code. Default: `auto`

### Supported Languages

`en` (English), `zh` (Chinese), `ja` (Japanese), `ko` (Korean), `es` (Spanish), `fr` (French), `de` (German), `ru` (Russian), `ar` (Arabic), `pt` (Portuguese), `it` (Italian), `th` (Thai), `vi` (Vietnamese), `id` (Indonesian)

## Python Usage

```python
from scripts import chat, translate

# Chat
result = chat(messages=[{"role": "user", "content": "Hello"}], model="qwen3.5-plus")

# Translate
result = translate(text="Hello", target_lang="zh")
```

## Response Format

```json
{ "success": true, "result": {...} }
{ "success": false, "error": "error message" }
```

## Notes

- Default API host: `https://coding.dashscope.aliyuncs.com/apps/anthropic` (set via `ALIYUN_BAILIAN_API_HOST`)
- The API uses Anthropic-compatible format — messages are converted to Anthropic API format internally
- Coding Plan API key (`sk-sp-xxx`) is different from regular DashScope API key
- For reasoning tasks: try `qwen3-max-2026-01-23` or `kimi-k2.5`
- For coding tasks: use `qwen3-coder-next` or `qwen3-coder-plus`

## Learn More

- Full API documentation: `references/API.md`
- Available models: `assets/models.json`
