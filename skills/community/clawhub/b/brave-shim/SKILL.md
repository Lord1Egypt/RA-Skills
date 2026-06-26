---
name: brave-shim
description: |
  Set up brave_shim as a free local proxy for OpenClaw web_search, routing Brave API
  requests to DuckDuckGo. Use when user asks to enable free web search, configure
  brave_shim, fix missing_brave_api_key errors, or set up no-api-key search.
---

# brave-shim

Local proxy that makes OpenClaw's Brave Search provider route to DuckDuckGo for free,
without any API key.

## How it works

1. A Python FastAPI service (brave_shim) runs locally on `http://127.0.0.1:8000`
2. It implements the Brave Search API format but fetches results from DuckDuckGo via `ddgs`
3. OpenClaw's built-in Brave provider is redirected to this local service

## Setup

### 1. Install brave_shim

```python
# Clone the repo
git clone https://github.com/asoraruf/brave_shim <clone-path>

# Create venv and install dependencies
python -m venv <clone-path>/venv
# Windows:
<clone-path>\venv\Scripts\activate
pip install fastapi uvicorn ddgs pyyaml
# Linux/Mac:
source <clone-path>/venv/bin/activate
pip install fastapi uvicorn ddgs pyyaml
```

### 2. Patch OpenClaw Brave provider URL

The Brave provider in OpenClaw's bundled JS calls `https://api.search.brave.com`. Replace it with `http://127.0.0.1:8000`:

```python
import subprocess, re, os

dist_dir = r"<openclaw-dist>"
pattern = r'(const BRAVE_SEARCH_ENDPOINT|const BRAVE_LLM_CONTEXT_ENDPOINT) = "[^"]+"'
replacement = {
    "const BRAVE_SEARCH_ENDPOINT": 'const BRAVE_SEARCH_ENDPOINT = "http://127.0.0.1:8000/res/v1/web/search"',
    "const BRAVE_LLM_CONTEXT_ENDPOINT": 'const BRAVE_LLM_CONTEXT_ENDPOINT = "http://127.0.0.1:8000/res/v1/llm/context"',
}

for fname in os.listdir(dist_dir):
    if fname.startswith("brave-web-search-provider") and fname.endswith(".js"):
        fpath = os.path.join(dist_dir, fname)
        content = open(fpath).read()
        new_content = re.sub(pattern, lambda m: replacement.get(m.group(1), m.group(0)), content)
        open(fpath, "w").write(new_content)
```

### 3. Configure OpenClaw

```bash
# Enable brave plugin (disabled by default)
openclaw config set plugins.entries.brave.enabled true

# Set Brave as search provider
openclaw config set tools.web.search.provider brave

# Restart gateway
openclaw gateway restart
```

### 4. Start shim service

```bash
# From brave_shim directory
.\venv\Scripts\python brave_shim.py
# Keep running in background
```

### 5. Verify

```bash
curl "http://127.0.0.1:8000/res/v1/web/search?q=hello+world"
# Should return JSON with web results

openclaw
# Then test: web_search { query: "test" }
```

## Scripts

- `scripts/setup_brave_shim.py` — Automated install: clone, venv, pip install
- `scripts/patch_openclaw.py` — Patch OpenClaw dist JS files to redirect Brave API
- `scripts/start_shim.py` — Start brave_shim service

## Troubleshooting

**"fetch failed" after setup:**
- Check shim is running: `Invoke-WebRequest http://127.0.0.1:8000/res/v1/web/search?q=test`
- If shim is DOWN: re-run `python brave_shim.py`
- If NO_PROXY blocks localhost: remove from env or set `NO_PROXY=localhost,127.0.0.1`

**"missing_brave_api_key" error:**
- `plugins.entries.brave` needs `enabled: true` — run `openclaw config set plugins.entries.brave.enabled true`

**"missing_gemini_api_key" instead:**
- Brave plugin still not enabled — check `openclaw doctor` for disabled plugin warnings
