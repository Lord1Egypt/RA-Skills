# browser-playwright-bridge

An [OpenClaw](https://github.com/openclaw/openclaw) skill that bridges the built-in browser tool with [Playwright](https://playwright.dev/) scripts — sharing the same Chrome instance, cookies, and login state.

## Problem

OpenClaw's browser tool and Playwright both use Chrome DevTools Protocol (CDP), but **they can't connect simultaneously**. This skill provides a lock-based manager that lets them take turns.

## How It Works

```
Chrome (shared cookies/login)
       ↕ mutually exclusive
┌──────────────┐    ┌──────────────────┐
│ OpenClaw     │ OR │ Playwright script │
│ browser tool │    │ (zero token cost) │
└──────────────┘    └──────────────────┘
```

1. **Explore** — Use OpenClaw's browser tool to figure out a new workflow
2. **Record** — Convert the steps into a Playwright script
3. **Replay** — Run via `browser-lock.sh` — zero token cost, deterministic, schedulable

## Quick Start

```bash
# Install Playwright (no browser download needed — connects to existing Chrome)
npm install playwright

# Run a script (auto-manages Chrome lifecycle + lock)
./scripts/browser-lock.sh run my-script.js

# With timeout (default: 300s)
./scripts/browser-lock.sh run --timeout 60 my-script.js
```

## Features

- 🔒 **Lock-based mutex** — prevents CDP conflicts between OpenClaw and Playwright
- 🍪 **Shared login state** — same Chrome user-data-dir, no re-authentication
- ⏱ **Timeout watchdog** — kills hung scripts, auto-releases lock
- 🖥 **Headless support** — auto-detects headless servers (Linux without display)
- 🔍 **CDP auto-discovery** — finds the debugging port from process args, env, or probing

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Full documentation for OpenClaw agents |
| `scripts/browser-lock.sh` | Lock manager (acquire/release/run/status) |
| `scripts/playwright-template.js` | Script starter template with CDP discovery |

## License

MIT
