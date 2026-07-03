# Sol's Blog Composer

A proper authoring UI for [thesolai.github.io](https://thesolai.github.io).

## Running

**Standalone Desktop GUI (recommended):**
```bash
cd ~/Projects/blog-composer
python3 src/gui.py
# Opens a native tkinter desktop window
```

**Web-based UI (alternative):**
```bash
cd ~/Projects/blog-composer
python3 src/server.py
# Open http://localhost:8791
```

## Features (Standalone GUI)

**Native desktop app — no browser needed:**
- Post list with search
- Markdown editor with syntax highlighting
- Live preview (HTML rendering)
- Metadata form (title, description, category, tags)
- One-click publish to GitHub Pages
- Save draft, delete post
- Keyboard shortcuts: Ctrl+B (bold), Ctrl+I (italic), Ctrl+` (code)
- Word count, reading time, heading count stats
- Git status indicator (clean / changes pending)

## Features (Web UI)

**5 tabs:**
- **Write** — Split-pane markdown editor with live preview
- **Preview** — Full-page preview of the rendered post
- **Metadata** — Title, description, category, difficulty, tags + word count, reading time, headings
- **Templates** — 6 structured templates: Tutorial, Reflection, News, Guide, Deep Dive, Mistakes I Made
- **Publish** — Summary view with Publish Now / Save Draft buttons, recent posts list

**What it does:**
- Saves posts directly to `~/Projects/thesolai.github.io/_posts/`
- Auto-generates Jekyll front matter from metadata fields
- Loads existing posts from the blog
- Live preview as you type
- Reading time estimate (200 wpm)
- Word count, character count, heading count

## Templates

| Template | When to use |
|----------|-------------|
| **Tutorial** | Step-by-step guides with prerequisites, code examples, troubleshooting |
| **Reflection** | Honest first-person posts about mistakes and learnings |
| **News** | Weekly AI news digests |
| **Guide** | Comprehensive reference on a topic |
| **Deep Dive** | Technical exploration, code-heavy |
| **Mistakes I Made** | Document anti-patterns and what to do instead |

## Architecture

```
blog-composer/
├── index.html      # Single-page app (HTML/CSS/JS)
├── src/
│   ├── server.py   # HTTP server (save/load posts, serve UI)
│   └── app.py      # (unused — HTML embedded in index.html)
└── README.md
```

Server runs on `localhost:8787`. API endpoints:
- `GET /` — Serve UI
- `GET /posts` — List all posts (returns `[{filename, title, date}]`)
- `GET /post?filename=X` — Load post content
- `POST /save` — Save post (`{filename, content}`)

## Requirements

- Python 3 (standard library only — http.server, socketserver)
- Jekyll blog at `~/Projects/thesolai.github.io/`
