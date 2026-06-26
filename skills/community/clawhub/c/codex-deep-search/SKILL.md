---
name: codex-deep-search
description: Deep web search using Codex CLI for complex queries that need multi-source synthesis. Use when web_search (Brave) returns insufficient results, when the user asks for in-depth research, comprehensive analysis, or says "deep search", "详细搜索", "帮我查一下", or when a topic needs following multiple links and cross-referencing sources.
---

# Codex Deep Search

Use Codex CLI's web search capability for research tasks needing more depth than Brave API snippets.

## When to Prefer Over web_search

- Complex/niche topics needing multi-source synthesis
- User explicitly asks for thorough/deep research
- Brave results are too shallow or missing context

## Usage

### Dispatch Mode (recommended — background + callback)

```bash
nohup bash /home/ubuntu/clawd/skills/codex-deep-search/scripts/search.sh \
  --prompt "Your research query" \
  --task-name "notebooklm-research" \
  --telegram-group "-5006066016" \
  --timeout 120 > /tmp/codex-search.log 2>&1 &
```

After dispatch: tell user search is running, results will arrive via Telegram. Do NOT poll.

### Synchronous Mode (short queries only)

```bash
bash /home/ubuntu/clawd/skills/codex-deep-search/scripts/search.sh \
  --prompt "Quick factual query" \
  --output "/tmp/search-result.md" \
  --timeout 60
```

Then read the output file and summarize.

## Parameters

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--prompt` | Yes | — | Research query |
| `--output` | No | `data/codex-search-results/<task>.md` | Output file path |
| `--task-name` | No | `search-<timestamp>` | Task identifier |
| `--telegram-group` | No | — | Telegram chat ID for callback |
| `--model` | No | `gpt-5.3-codex` | Model override |
| `--timeout` | No | `120` | Seconds before auto-stop |

## Result Files

| File | Content |
|------|---------|
| `data/codex-search-results/<task>.md` | Search report (incremental) |
| `data/codex-search-results/latest-meta.json` | Task metadata + status |
| `data/codex-search-results/task-output.txt` | Raw Codex output |

## Key Design

- **Incremental writes** — results saved after each search round, survives OOM/timeout
- **Low reasoning effort** — reduces memory, prevents OOM SIGKILL
- **Timeout protection** — auto-stops runaway searches
- **Dispatch pattern** — background execution with Telegram callback, no polling
