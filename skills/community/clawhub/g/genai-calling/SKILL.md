---
name: genai-calling
description: >
  Unified interface for all providers and all modalities: use the `genai-calling`
  skill to operate the published `genai-calling` CLI/SDK across
  text/image/audio/video/embedding workflows, with support for authenticated
  local MCP workflows.
---

# genai-calling

This skill is named `genai-calling` in this repository.

The runtime package is `genai-calling`, the Python import path is
`gravtice.genai`, and the environment variable prefix is
`GENAI_CALLING_*`.

## Quick Start

**IMPORTANT:** If you rely on project-local `.env.*` files, run commands in the
directory that contains those files (typically this skill base directory). If
no project-local env file is present, the runtime also falls back to
`~/.genai-calling/.env`. If you pass runtime env vars (inline/export), working
directory is not restricted.

```bash
# 1) Create `.env.local` in this skill directory
(cd "<SKILL_BASE_DIR>" && { test -f .env.local || touch .env.local; })

# 2) Edit `<SKILL_BASE_DIR>/.env.local` and set at least one provider key (see "Configuration Templates" and "Supported Environment Variables").
# Example (OpenAI):
#   OPENAI_API_KEY=...

# 3) Text
(cd "<SKILL_BASE_DIR>" && uvx --from genai-calling genai --model openai:gpt-4o-mini --prompt "Hello")

# 4) See what you can use (requires at least one provider key configured)
(cd "<SKILL_BASE_DIR>" && uvx --from genai-calling genai model available --all)
```

For user-wide defaults shared across projects, create `~/.genai-calling/.env`
and put provider credentials there. Project-local `.env.*` files still win.

If `uvx` is unavailable, install once and use `genai` directly:

```bash
python -m pip install --upgrade genai-calling
(cd "<SKILL_BASE_DIR>" && genai --model openai:gpt-4o-mini --prompt "Hello")
```

## Configuration (Env Vars, Zero-parameter)

Configuration is managed via environment variables.

You can set env vars in two ways:

1. Runtime env vars (inline before command, or `export` in shell)
2. Env files (`.env.local`, `.env.production`, `.env.development`, `.env.test`, `~/.genai-calling/.env`)

Recommended for this skill:

- Put reusable provider credentials in `~/.genai-calling/.env`
- Put project-level overrides in `<SKILL_BASE_DIR>/.env.local`
- Use runtime env vars for one-off overrides

Runtime example (inline):

```bash
(cd "<SKILL_BASE_DIR>" && OPENAI_API_KEY=... uvx --from genai-calling genai --model openai:gpt-4o-mini --prompt "Hello")
```

When env files are used, SDK/CLI/MCP loads them automatically with priority (high -> low):

- `.env.local > .env.production > .env.development > .env.test > ~/.genai-calling/.env`

Process env vars override file-based config.

Minimal `.env.local` (OpenAI text only):

```bash
OPENAI_API_KEY=...
GENAI_CALLING_TIMEOUT_MS=120000
```

Minimal `~/.genai-calling/.env`:

```bash
OPENAI_API_KEY=...
GOOGLE_API_KEY=
ANTHROPIC_API_KEY=
```

Notes:

- Do not commit `.env.local` (add it to `.gitignore` if needed).
- `~/.genai-calling/.env` is user-level config and should hold only values you want shared across projects.
- Provider credentials should use the shorter provider-specific variable names such as `OPENAI_API_KEY`.

## Configuration Templates

Project-local `.env.local` example:

```bash
# Copy only what you need. Do not commit `.env.local`.

# --------------------
# Common
# --------------------
GENAI_CALLING_TIMEOUT_MS=120000
GENAI_CALLING_URL_DOWNLOAD_MAX_BYTES=134217728
# GENAI_CALLING_ALLOW_PRIVATE_URLS=1
# GENAI_CALLING_TRANSPORT=

# --------------------
# Providers
# --------------------
OPENAI_API_KEY=
GOOGLE_API_KEY=
ANTHROPIC_API_KEY=

ALIYUN_API_KEY=
ALIYUN_OAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

VOLCENGINE_API_KEY=
VOLCENGINE_OAI_BASE_URL=https://ark.cn-beijing.volces.com/api/v3

TUZI_BASE_URL=https://api.tu-zi.com
# TUZI_OAI_BASE_URL=https://api.tu-zi.com/v1
# TUZI_GOOGLE_BASE_URL=https://api.tu-zi.com
# TUZI_ANTHROPIC_BASE_URL=https://api.tu-zi.com
TUZI_WEB_API_KEY=
TUZI_OPENAI_API_KEY=
TUZI_GOOGLE_API_KEY=
TUZI_ANTHROPIC_API_KEY=

# --------------------
# MCP Server
# --------------------
GENAI_CALLING_MCP_HOST=127.0.0.1
GENAI_CALLING_MCP_PORT=6001
GENAI_CALLING_MCP_PUBLIC_BASE_URL=
# GENAI_CALLING_MCP_BEARER_TOKEN=
# GENAI_CALLING_MCP_TOKEN_RULES=token1: [openai google]; token2: [openai:gpt-4o-mini]
```

User-wide `~/.genai-calling/.env` example:

```bash
OPENAI_API_KEY=
GOOGLE_API_KEY=
ANTHROPIC_API_KEY=
```

Recommended usage:

- Put shared provider credentials in `~/.genai-calling/.env`
- Put project-specific overrides and MCP settings in `<SKILL_BASE_DIR>/.env.local`
- Keep only the providers and options you actually use

## Supported Environment Variables

### Common runtime

- `GENAI_CALLING_TIMEOUT_MS` (default: `120000`)
- `GENAI_CALLING_URL_DOWNLOAD_MAX_BYTES` (default: `134217728`)
- `GENAI_CALLING_ALLOW_PRIVATE_URLS` (`1/true/yes` to allow private/loopback URL download)
- `GENAI_CALLING_TRANSPORT` (internal transport marker; MCP server uses `mcp`, legacy `sse` is accepted)

### Provider credentials

- OpenAI: `OPENAI_API_KEY`
- Google (Gemini): `GOOGLE_API_KEY`
- Anthropic (Claude): `ANTHROPIC_API_KEY`
- Aliyun (DashScope/百炼): `ALIYUN_API_KEY`
- Volcengine (Ark/豆包): `VOLCENGINE_API_KEY`

### Provider base URL overrides

- `ALIYUN_OAI_BASE_URL` (default: `https://dashscope.aliyuncs.com/compatible-mode/v1`)
- `VOLCENGINE_OAI_BASE_URL` (default: `https://ark.cn-beijing.volces.com/api/v3`)
- `TUZI_BASE_URL` (default: `https://api.tu-zi.com`)
- `TUZI_OAI_BASE_URL` (optional override)
- `TUZI_GOOGLE_BASE_URL` (optional override)
- `TUZI_ANTHROPIC_BASE_URL` (optional override)

### Tuzi credentials

- `TUZI_WEB_API_KEY`
- `TUZI_OPENAI_API_KEY`
- `TUZI_GOOGLE_API_KEY`
- `TUZI_ANTHROPIC_API_KEY`

### MCP server

- `GENAI_CALLING_MCP_HOST` (default: `127.0.0.1`)
- `GENAI_CALLING_MCP_PORT` (default: `6001`)
- `GENAI_CALLING_MCP_PUBLIC_BASE_URL`
- `GENAI_CALLING_MCP_BEARER_TOKEN`
- `GENAI_CALLING_MCP_TOKEN_RULES`

Quick guidance:

- Most users only need one provider key plus `GENAI_CALLING_TIMEOUT_MS`
- Only set `GENAI_CALLING_ALLOW_PRIVATE_URLS` if you explicitly want to bypass private URL protection
- Only set MCP variables when you run `genai-mcp-server`

## Model Format

Model string is `{provider}:{model_id}` (example: `openai:gpt-4o-mini`).

Use this to pick a model by output modality:

```bash
(cd "<SKILL_BASE_DIR>" && uvx --from genai-calling genai model available --all)
# Look for: out=text / out=image / out=audio / out=video / out=embedding
```

If you have not configured any keys yet, you can still view the SDK curated list:

```bash
(cd "<SKILL_BASE_DIR>" && uvx --from genai-calling genai model sdk)
```

## Common Scenarios

### Image understanding

```bash
(cd "<SKILL_BASE_DIR>" && uvx --from genai-calling genai --model openai:gpt-4o-mini --prompt "Describe this image" --image-path "/path/to/image.png")
```

### Image generation (save to file)

```bash
(cd "<SKILL_BASE_DIR>" && uvx --from genai-calling genai --model openai:gpt-image-1 --prompt "A red square, minimal" --output-path "/tmp/out.png")
```

### Speech-to-text (transcription)

```bash
(cd "<SKILL_BASE_DIR>" && uvx --from genai-calling genai --model openai:whisper-1 --audio-path "/path/to/audio.wav")
```

### Text-to-speech (save to file)

```bash
(cd "<SKILL_BASE_DIR>" && uvx --from genai-calling genai --model openai:tts-1 --prompt "你好" --output-path "/tmp/tts.mp3")
```

## Python SDK

Install:

```bash
python -m pip install --upgrade genai-calling
```

Minimal example:

```python
from gravtice.genai import Client, GenerateRequest, Message, OutputSpec, Part

client = Client()
resp = client.generate(
    GenerateRequest(
        model="openai:gpt-4o-mini",
        input=[Message(role="user", content=[Part.from_text("Hello")])],
        output=OutputSpec(modalities=["text"]),
    )
)
print(resp.output[0].content[0].text)
```

Note: `Client()` loads project-local `.env.*` from the current working
directory and then falls back to `~/.genai-calling/.env`; run your script in
the directory that contains your project env files, or export env vars in the
process environment.

## MCP Server

Start server (Streamable HTTP: `/mcp`, SSE: `/sse`):

```bash
(cd "<SKILL_BASE_DIR>" && uvx --from genai-calling genai-mcp-server)
```

Recommended: set auth via runtime env vars, `.env.local`, or
`~/.genai-calling/.env` before exposing the server:

```bash
# GENAI_CALLING_MCP_BEARER_TOKEN=sk-...
```

Debug with MCP CLI:

```bash
(cd "<SKILL_BASE_DIR>" && uvx --from genai-calling genai-mcp-cli env)
(cd "<SKILL_BASE_DIR>" && uvx --from genai-calling genai-mcp-cli tools)
(cd "<SKILL_BASE_DIR>" && uvx --from genai-calling genai-mcp-cli call list_providers)
(cd "<SKILL_BASE_DIR>" && uvx --from genai-calling genai-mcp-cli call generate --args '{"request":{"model":"openai:gpt-4o-mini","input":"Hello","output":{"modalities":["text"]}}}')
```

## Troubleshooting

### Missing/invalid API key (401/403)
Set provider credentials via runtime env vars, `<SKILL_BASE_DIR>/.env.local`,
or `~/.genai-calling/.env` (see "Supported Environment Variables"), then retry.

### File input errors (mime type)
If you see `cannot detect ... mime type`, verify the path exists and is a valid image/audio/video file.

### Timeout / long-running jobs
Increase `GENAI_CALLING_TIMEOUT_MS` (runtime env var, `.env.local`, or
`~/.genai-calling/.env`) and retry.

### URL download blocked / SSRF protection
Binary outputs may be returned as URLs. Private/loopback URLs are rejected by default. Only if you understand the risk, set `GENAI_CALLING_ALLOW_PRIVATE_URLS=1`.

### MCP auth (401 Unauthorized)
Set `GENAI_CALLING_MCP_BEARER_TOKEN` (or `GENAI_CALLING_MCP_TOKEN_RULES`) via
runtime env var, `.env.local`, or `~/.genai-calling/.env`, and ensure
`genai-mcp-cli` uses the same token.
