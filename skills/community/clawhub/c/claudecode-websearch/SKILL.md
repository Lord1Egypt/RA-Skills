---
name: claude-websearch
description: >
  Free web search using Claude Code CLI or Codex CLI's built-in WebSearch tool — no Tavily,
  Brave, or Exa API key required. Activate when the user says "websearch", "搜一下", "search the web",
  or when Tavily/Brave quota is exhausted and you need to search the web.
metadata:
  openclaw:
    emoji: 🔍
    requires:
      anyBins:
        - claude
        - codex
---

# Claude WebSearch Skill

Use the bundled script to search the web via **Claude Code CLI** (primary) or **Codex CLI** (fallback). Both CLIs expose a native `WebSearch` tool — no third-party search API key needed.

## When to Use

- Tavily / Brave / Exa quota is exhausted
- User says "websearch搜一下X", "search for X", "查一下X"
- Any web search need where no API key is configured

## Quick Usage

```bash
# Primary (Claude Code CLI — fast, recommended)
scripts/websearch.sh "your query"

# With result count
scripts/websearch.sh "your query" --max 3

# Explicit backend
scripts/websearch.sh "your query" --backend codex
```

**Or use the global alias** (if installed):
```bash
ccws "your query"
```

## How It Works

| Backend | CLI flag | Notes |
|---------|----------|-------|
| `claude` (default) | `--allowedTools "WebSearch"` | Fast (~5s), clean output |
| `codex` | `--search` + `reasoning_effort=low` | Slower (~30-60s), use as fallback |

The script auto-detects which CLI is available; `claude` is preferred when both exist.

## Setup (one-time)

Install the global alias `ccws` for quick access:

```bash
ln -sf "$(pwd)/scripts/websearch.sh" ~/.local/bin/ccws
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `claude: command not found` | Install Claude Code CLI: `npm install -g @anthropic-ai/claude-code` |
| `codex: command not found` | Install Codex CLI: `npm install -g @openai/codex` |
| Claude returns empty output | Check `claude auth status`; re-login if expired |
| Codex times out | Normal — use `--backend claude` instead |
| `Not inside a trusted directory` (Codex) | Script handles this by running from a temp dir |
