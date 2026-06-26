# baoyu-post-to-x-enhanced

> One-click publish to X/Twitter via Chrome CDP — custom enhanced fork

## Overview

Posts text, images, videos, and long-form X Articles to X (Twitter) through a real Chrome browser session, bypassing anti-bot detection. This is a heavily modified fork of the original [baoyu-post-to-x](https://github.com/JimLiu/baoyu-skills#baoyu-post-to-x) skill.

## Key Features

- **Three-tier text insertion**: CDP `Input.insertText` → `document.execCommand` → macOS `osascript` keyboard simulation
- **Unicode hashtag truncation**: Hard limit of 3 hashtags per post with `/#[\p{L}\p{N}_]+/gu` regex for CJK support
- **Smart Reset editor cleanup**: Conditional `about:blank` navigation only when keyboard cleanup fails
- **`beforeunload` dialog handling**: Auto-accept dialogs that block SPA navigation
- **CDP timeout optimization**: Configurable timeouts (10s for blank, 45s for X compose)
- **Chrome process detachment**: `detached: true` prevents parent process SIGKILL from terminating Chrome
- **Auto file-path detection**: Automatically reads file content when a path is passed as text argument
- **Post-click error detection**: Detects "hashtag exceeds" errors and auto-retries with stripped hashtags

## Scripts

| Script | Purpose |
|--------|---------|
| `x-browser.ts` | Post tweets (text + images) with `--submit` for full automation |
| `x-article.ts` | Publish X Articles (long-form) with cover image and in-article images |
| `x-video.ts` | Post video content |
| `x-quote.ts` | Quote-tweet existing posts |
| `copy-to-clipboard.ts` | Copy content to macOS clipboard |
| `paste-from-clipboard.ts` | Paste from clipboard via CDP or osascript |
| `md-to-html.ts` | Convert Markdown to HTML for X Articles |
| `check-paste-permissions.ts` | Verify Chrome automation permissions |

## Requirements

- **Runtime**: `bun` (preferred) or `npx -y bun`
- **Browser**: Google Chrome with `--remote-debugging-port` enabled
- **OS**: macOS (for `osascript` fallback strategy)

## Version History

### v3.0.0 (2026-04-14)

Major reliability overhaul for the publishing pipeline:

- Implemented three-tier text insertion strategy with `execCommand` fallback
- Fixed Unicode hashtag detection regex for CJK languages
- Added Smart Reset for Chrome reuse (conditional `about:blank` navigation)
- Added `beforeunload` dialog auto-accept
- Increased CDP timeouts (blank: 10s, compose: 45s, image processing: 30s)
- Chrome launched with `detached: true` to survive parent SIGKILL
- Auto-detect file paths passed as text arguments (`--text-file` support)
- Post-click error detection with automatic hashtag stripping retry
- Enhanced Post button click with `mouseMoved` events and `Enter` key fallback

### v2.0.0

- Initial enhanced fork with DOM.setFileInputFiles image upload fix
- Path leak cleanup in editor
- Post-publish verification

## Installation

```bash
# From ClawHub
clawhub install baoyu-post-to-x-enhanced

# Or via OpenClaw TUI
/skills install @clawstore-labs/baoyu-post-to-x-enhanced
```

Or install as part of the **Viralix X-Marketing** Persona.
