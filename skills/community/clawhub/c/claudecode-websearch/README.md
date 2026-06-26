# openclaw-claudecode-websearch

An OpenClaw skill that uses **Claude Code CLI** (or Codex CLI) as a free web search backend.

## When to use

- You don't have a Tavily / Brave / Exa API key configured
- Your search quota has run out
- You already have Claude Code (or Codex) CLI installed and authenticated

No extra API keys. No extra setup. Just borrows the built-in `WebSearch` tool from the CLI you already have.

## How it works

```
User: "search the web for X"  →  OpenClaw runs websearch.sh  →  claude -p "..." --allowedTools "WebSearch"
```

Claude Code CLI handles the actual web search. Results come back clean with source links.

Codex CLI is supported as a fallback (`--backend codex`) but is slower and less reliable.

## Install

```bash
# Clone this skill into your OpenClaw skills directory
git clone https://github.com/jinghan23/openclaw-claudecode-websearch \
  ~/.openclaw/workspace/skills/claude-websearch

# Optional: install global alias
ln -sf ~/.openclaw/workspace/skills/claude-websearch/scripts/websearch.sh \
  ~/.local/bin/ccws
```

## Usage

```bash
# Via script
scripts/websearch.sh "your query"
scripts/websearch.sh "your query" --max 3
scripts/websearch.sh "your query" --backend codex   # fallback

# Via alias
ccws "your query"
```

## Requirements

- [Claude Code CLI](https://claude.ai/code) — `npm install -g @anthropic-ai/claude-code`
- Or [Codex CLI](https://github.com/openai/codex) — `npm install -g @openai/codex`
