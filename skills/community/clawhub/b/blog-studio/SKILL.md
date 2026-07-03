---
name: blog-studio
description: Standalone CMS for GitHub Pages Jekyll blogs — browse, edit, create posts, and deploy with one click.
version: 1.0.0
author: TheSolAI
permissions: ["file.read", "file.write", "http.request"]
---

# Blog Studio

A standalone Python HTTP server that serves as a self-contained CMS for GitHub Pages Jekyll blogs. Browse posts, edit content, create new posts with live markdown preview, and deploy directly to GitHub.

## Triggers

Use when managing a Jekyll blog hosted on GitHub Pages and you want a UI for:
- Browsing all posts, guides, and pages
- Editing existing content
- Creating new posts with live preview
- One-click deploy to GitHub

## Actions

- **Browse** — List all blog posts, guides, and pages with metadata (date, tags, status)
- **Edit** — Open any post in the editor with live markdown preview
- **Create** — Scaffold a new post with frontmatter, open editor
- **Deploy** — Commit and push changes to GitHub
- **Preview** — Serve the Jekyll site locally to preview changes

## Requirements

- `gh` CLI authenticated (`gh auth login`)
- GitHub repository with write access
- Python 3.8+
- Jekyll (optional, for local preview)

## Running

```bash
cd /path/to/BlogStudio
python3 server.py
# Opens at http://localhost:8765
```
