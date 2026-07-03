# BlogStudio — Specification

> Sol AI Content Management System for thesolai.github.io

## Overview

**BlogStudio** is a desktop app for managing all content on the Sol AI website — blog posts, guides, analysis, pages. It connects to GitHub and provides a rich editor with the site's design system.

## Requirements

### 1. GitHub Integration
- Connect to TheSolAI/thesolai.github.io
- Read all content (_posts, guides, pages)
- Write/push changes back to GitHub
- Sync button to pull latest content

### 2. Content Types
| Type | Location | Template |
|------|---------|----------|
| Blog Posts | _posts/ | post.html layout |
| Guides | guides/*.html | standalone HTML |
| Analysis | analysis/ | post layout |
| Pages | *.html | page layouts |

### 3. Editor Features
- Rich text editing (Markdown + preview)
- Follow site design system (Comic Neue, Bangers fonts)
- Tag support
- Featured image selection
- Draft/publish toggle

### 4. Sol Integration
- Sol can read all content
- Sol can generate blog post suggestions
- Sol can preview and edit
- Sync with Sol's memory

### 5. Publishing
- **Publish button** — immediate push to GitHub
- **Schedule posts** — set date/time for future publish
- Connect to OpenClaw cron jobs for scheduled publishing

### 6. Sync Features
- Pull latest from GitHub
- Push changes to GitHub
- Conflict detection
- Auto-sync option

## Architecture

```
BlogStudio/
├── main.py           # Python GUI (PyQt6)
├── main.js          # Electron main process
├── renderer/        # HTML/CSS/JS UI
├── github/         # GitHub API client
├── templates/      # Site templates
├── sync/           # Sync engine
└── scheduler/      # Post scheduling
```

## Design System (must match site)

- **Fonts**: Bangers (headings), Comic Neue (body)
- **Colors**: 
  - Primary: #FFD166 (yellow)
  - Accent: #E63946 (red)
  - Dark: #111111
- **Components**: Follow comic-ui.css

## GitHub API Endpoints

- GET /repos/{owner}/{repo}/contents/{path}
- PUT /repos/{owner}/{repo}/contents/{path}
- GET /repos/{owner}/{repo}/git/trees/{ref}
- POST /repos/{owner}/{repo}/actions/workflows/dispatch

## Cron Integration

Scheduled posts use OpenClaw cron:
- Job stored in workspace
- Triggers publish at scheduled time
- Visible in BlogStudio scheduler

## Deliverables

1. **Electron App** (primary)
   - `main.js` + `preload.js` + `renderer/`
   
2. **Python GUI** (secondary)
   - Using PyQt6 or Tkinter
   
Both share the same backend logic.

## Testing Checklist

- [ ] Can login to GitHub
- [ ] Can list all blog posts
- [ ] Can list all guides
- [ ] Can edit a post
- [ ] Can preview post (matches site style)
- [ ] Can publish immediately
- [ ] Can schedule a post
- [ ] Can sync with GitHub
- [ ] Sol can see all content
- [ ] Design matches site

## File Structure

```
BlogStudio/
├── SPEC.md                 # This file
├── README.md               # Usage docs
├── TODO.md                # Task list
├── electron/              # Electron version
│   ├── main.js
│   ├── preload.js
│   └── renderer/
│       ├── index.html
│       ├── styles.css
│       └── app.js
├── python/                # Python version
│   ├── main.py
│   ├── github_client.py
│   ├── editor.py
│   └── scheduler.py
├── shared/                # Shared backend
│   ├── github.py
│   ├── templates.py
│   └── config.example
└── build/                # Build outputs
```