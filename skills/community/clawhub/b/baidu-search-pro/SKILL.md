---
name: baidu-search
description: Compatibility entry for our in-house Baidu realtime search chain. Use for live information, documentation, or research topics.
metadata: { "openclaw": { "emoji": "🔍︎",  "requires": { "anyBins": ["python", "python3", "py"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# Baidu Search (compat alias)

> Cross-platform Python: on Windows prefer `py -3.11`; on Linux/macOS prefer `python3`; if plain `python` already points to Python 3, it also works.

This skill is a backward-compatible alias for `realtime-web-search`.
Use it only when an existing workflow still calls `skills/baidu-search`; new installs should prefer `realtime-web-search` directly.

## What this alias keeps working

Both commands run the same canonical Baidu-based search chain:

```bash
py -3.11 skills/baidu-search/scripts/search.py '<JSON>'
py -3.11 skills/realtime-web-search/scripts/search.py '<JSON>'
```

## Recommended modes

- `mode=auto` (default): `web_search -> chat -> web_summary`
- `mode=search`: `web_search -> chat`
- `mode=summary`: `web_summary` only

Prefer `mode=search` for speed and stability.

## Minimal request example

```bash
py -3.11 skills/baidu-search/scripts/search.py '{"query":"人工智能","mode":"search"}'
```

## Required environment variable

- `BAIDU_API_KEY`

## Optional endpoint overrides

- `BAIDU_WEB_SEARCH_ENDPOINT`
- `BAIDU_CHAT_SEARCH_ENDPOINT`
- `BAIDU_SUMMARY_ENDPOINT`
