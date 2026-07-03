# BlogStudio

Standalone blog CMS for thesolai.github.io — a Python HTTP server serving a self-contained HTML app that talks directly to GitHub.

## Quick Start

```bash
cd /Users/amre/Projects/BlogStudio
python3 server.py
```

Opens automatically at `http://localhost:8765`

Requires: `gh auth login` (already done on this machine)

## What it does

- **Browse** blog posts, guides, pages from `TheSolAI/thesolai.github.io`
- **Edit** any existing post (click to open)
- **Create** new posts with live markdown preview
- **Publish** straight to GitHub (main branch)
- **Sync** to pull latest content

## Architecture

- `server.py` — Python HTTP server; injects GitHub token from `gh auth token` and serves the app
- `index.html` — standalone HTML/CSS/JS app (no build step, no dependencies)
- `python/` — legacy PyQt version (not maintained)

## Keyboard

- Click any post card to edit it
- Cancel button returns to list
- Publish pushes directly to GitHub main

## Tech

- Python 3 http.server (no pip install needed)
- Vanilla JS (no framework)
- GitHub REST API v3
- Token via `gh auth token`
