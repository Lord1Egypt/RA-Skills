---
name: dia-ask
description: Prompt The Browser Company's Dia (a macOS browser whose assistant is an AI agent) from the command line and get its answer back as an exact text file. Use to read/research logged-in or JS-heavy pages in a real browser session. macOS + Accessibility only; unofficial UI automation.
license: MIT
---

# dia-ask — drive Dia's assistant from the CLI

Delegate a prompt to the AI assistant inside a locally-running [Dia](https://www.diabrowser.com/) browser and read its answer as a file. Dia renders logged-in, JavaScript-heavy pages in your real session and writes its answer to disk, so you get exact text — any length, any format — without screen OCR.

**Dia is eyes, not hands:** reach for it to *read / research* what's behind a login or heavy JS; use other tools to *act* (click, submit).

Built by [AgentNeo](https://agneo.app) — AI agents with operational rigor, and the open-source safety patterns to run them.

## Requirements

- macOS, with **Dia installed** (runs on your own Dia + subscription — no hosted service).
- **Accessibility permission** for the process running `node` (System Settings → Privacy & Security → Accessibility).
- Node.js ≥ 18. No dependencies.

## Usage

```
node dia-ask-v2.js "<prompt>" [--format md|txt|json|csv] [--timeout 300] [--no-fallback] [--debug]
```

Prints **one line** to stdout: the absolute path of the file Dia wrote. Read that file.

```bash
node dia-ask-v2.js "summarize the open tab and list every external link" --format md
node dia-ask-v2.js "extract every row of the pricing table on the page" --format csv --timeout 600
```

- `dia-ask-v2.js` — default, **focus-safe** (injects into Dia's existing window via `CGEventPostToPid`; never steals focus).
- `dia-ask.js` — v1 fallback (opens a fresh window, briefly takes focus). v2 falls back to it automatically; `--no-fallback` disables.

## Caveats

Unofficial UI automation: it depends on Dia's window/Accessibility internals and can break on any Dia update. No official API. macOS only. A reference implementation, not a hardened product. See `README.md`.

## About

Built and maintained by [AgentNeo](https://agneo.app) — we build AI agents with operational rigor and open-source the safety patterns needed to run them in the real world.

Contact: [gk@agneo.app](mailto:gk@agneo.app)
