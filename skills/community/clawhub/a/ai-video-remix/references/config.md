# Configuration Reference

## .env Variables

```env
# ── LLM Agent (optional — set AGENT_PROVIDER=none to skip) ───────────────────
AGENT_PROVIDER=claude              # 'claude' | 'openai' | 'openai-compat' | 'none'
ANTHROPIC_API_KEY=sk-ant-...       # Required when AGENT_PROVIDER=claude (sent only to api.anthropic.com)
OPENAI_API_KEY=sk-...              # Required when AGENT_PROVIDER=openai (sent only to api.openai.com)
OPENAI_COMPAT_BASE_URL=https://... # Required when AGENT_PROVIDER=openai-compat
OPENAI_COMPAT_API_KEY=sk-...       # Required when AGENT_PROVIDER=openai-compat (sent only to the URL above)
AGENT_MODEL=claude-sonnet-4-6      # Override default model name

# ── ShotAI MCP (required) ───────────────────────────────────────────────────
SHOTAI_URL=http://127.0.0.1:23817  # ShotAI local MCP server URL (localhost only)
SHOTAI_TOKEN=<token>               # Token from ShotAI Settings → MCP Server (sent only to SHOTAI_URL)

# ── Music ─────────────────────────────────────────────────────────────────────
BGM_PATH=/path/to/music.mp3        # Local MP3; if set, skips YouTube/yt-dlp entirely

# ── Output ────────────────────────────────────────────────────────────────────
OUTPUT_DIR=./output                # Final video output directory
FILE_PORT=8080                     # Localhost-only HTTP port for serving clips to Remotion (binds to 127.0.0.1)

# ── Quality ───────────────────────────────────────────────────────────────────
MIN_SCORE=0.5                      # Minimum shot quality score 0–1 (recommended: 0.5)
MAX_RETRIES=1                      # ShotAI search retry attempts
```

## LLM Provider Setup

### Claude (Anthropic)
```env
AGENT_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-...
AGENT_MODEL=claude-sonnet-4-6      # or claude-opus-4-6
```

### OpenAI
```env
AGENT_PROVIDER=openai
OPENAI_API_KEY=sk-...
AGENT_MODEL=gpt-4o
```

### OpenRouter (recommended for China / multi-provider access)
```env
AGENT_PROVIDER=openai-compat
OPENAI_COMPAT_BASE_URL=https://openrouter.ai/api/v1
OPENAI_COMPAT_API_KEY=sk-or-v1-...
AGENT_MODEL=deepseek/deepseek-chat-v3-0324   # or any available model
```
Note: Some models (Anthropic/OpenAI) may be region-restricted on OpenRouter. Use `deepseek/deepseek-chat-v3-0324`, `meta-llama/llama-3.3-70b-instruct`, or `mistralai/mistral-small-3.2-24b-instruct` as reliable alternatives.

### Ollama (local, no API key)
```env
AGENT_PROVIDER=openai-compat
OPENAI_COMPAT_BASE_URL=http://localhost:11434/v1
OPENAI_COMPAT_API_KEY=ollama
AGENT_MODEL=llama3.1
```

### DeepSeek (direct)
```env
AGENT_PROVIDER=openai-compat
OPENAI_COMPAT_BASE_URL=https://api.deepseek.com/v1
OPENAI_COMPAT_API_KEY=sk-...
AGENT_MODEL=deepseek-chat
```

### No LLM (heuristic fallback)
```env
AGENT_PROVIDER=none
```
Keyword-based composition selection, uses registry default search queries. No API key needed.

## Shot Quality Tuning

`MIN_SCORE` controls the minimum composite shot quality threshold:
- `0.50` (**recommended**) — stricter, filters out short/low-quality shots, reduces visual artifacts
- `0.35` (default) — permissive, good for small libraries with varied content
- `0.25` — very permissive, useful if library is small or niche

Score formula: `similarity×0.5 + durationFit×0.3 + moodMatch×0.2`

> **Tip**: Set `MIN_SCORE=0.5` to prevent very short clips (< 1s) from entering the pipeline. Short clips can cause visual glitches in transition-heavy compositions like `CyberpunkCity`.
