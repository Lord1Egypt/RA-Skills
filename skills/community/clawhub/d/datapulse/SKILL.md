---
name: datapulse
description: Cross-platform content collection, web search, trending topics, confidence scoring, and watch/triage workflows for assistant and agent usage.
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---

# DataPulse Skill (v0.8.1)

Use this skill when the user needs one or more of the following:

- Read or batch-read URLs across X, Reddit, YouTube, Bilibili, Telegram, WeChat, Xiaohongshu, RSS, arXiv, Hacker News, GitHub, and generic web pages
- Search the web, inspect trending topics, or collect cross-platform signals
- Create watch missions, alert routes, triage queues, or story evidence packs
- Run assistant-ready URL intake through `datapulse_skill.run()`

## Python Entry Point

```python
from datapulse_skill import run

run("请处理这些链接: https://x.com/... https://www.reddit.com/...")
```

## Core Capabilities

- URL ingestion with normalized `DataPulseItem` output
- Confidence scoring and ranking
- Web search and trending discovery
- Watch missions and alert routing
- Triage queue and story workspace workflows

## Behavior Disclosure

### Browser Automation (optional)

DataPulse uses Playwright for platforms that require authenticated browser sessions (WeChat, Xiaohongshu). Browser automation is **opt-in only** — it activates when the user explicitly runs a `login` command and a valid session file exists. The `playwright` dependency is optional (`pip install datapulse[browser]`). No browser launches occur during normal URL reading.

### Subprocess Calls

- **MCP transport**: Story and triage modules invoke `subprocess.run()` to communicate with MCP tool servers via `subprocess_json` transport (stdin/stdout JSON-RPC). All calls have explicit timeouts (30s default).
- **YouTube fallback**: The YouTube collector may call `yt-dlp` as a subprocess for audio transcript extraction when the native API is unavailable.
- **CLI update check**: The CLI invokes `pip install --upgrade` only when the user explicitly runs `--upgrade`.

No subprocess call runs silently or without user-initiated action.

### Local Persistence

- **Session files**: Playwright login sessions are saved to `~/.datapulse/sessions/` for reuse. Sessions are TTL-cached (12h) and can be invalidated via `invalidate_session_cache()`.
- **Data files**: Watch missions, alert routes, triage queues, story workspaces, and entity stores persist as JSON files under the working directory (`data/` folder). All writes use atomic save patterns.

No data is written outside the working directory or `~/.datapulse/` without explicit user action.

### Outbound HTTP (alert delivery)

When the user configures alert routes, DataPulse sends POST requests to user-specified endpoints:
- **Webhook**: arbitrary URL provided by the user
- **Feishu**: Feishu bot webhook URL provided by the user
- **Telegram**: Telegram Bot API (`api.telegram.org`) using a user-provided bot token

Alert delivery only fires when: (1) a watch mission matches new content, AND (2) the user has explicitly configured a route with a destination URL or token. No outbound POST occurs without user-configured routes.

### Local Server (optional)

`datapulse-console` starts a local FastAPI/Uvicorn HTTP server for the browser-based console UI. It binds to `localhost` by default and is **never started automatically** — only when the user explicitly runs `datapulse-console` or `python -m datapulse.console_server`.

### External API Calls (read-only)

Normal operation makes outbound GET/POST requests to:
- **Jina AI** (`r.jina.ai`, `s.jina.ai`): URL reading and web search (requires `JINA_API_KEY`)
- **Tavily** (`api.tavily.com`): web search (requires `TAVILY_API_KEY`)
- **Groq** (`api.groq.com`): YouTube audio transcription fallback (requires `GROQ_API_KEY`)
- **Target URLs**: the URLs the user asks to read

All API keys are read from environment variables; none are bundled or hard-coded.

## Environment Notes

- Python `3.10+`
- Optional search enhancement: `JINA_API_KEY`, `TAVILY_API_KEY`
- Optional platform enhancement: `TG_API_ID`, `TG_API_HASH`, `GROQ_API_KEY`
- Optional browser sessions: `pip install datapulse[browser]` (Playwright)
- Optional console UI: `pip install datapulse[console]` (FastAPI + Uvicorn)
