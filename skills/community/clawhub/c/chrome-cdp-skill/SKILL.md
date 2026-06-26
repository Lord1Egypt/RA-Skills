---
name: chrome-cdp
description: Interact with a local Chrome-family browser session over CDP when the user explicitly asks to inspect, debug, or interact with a page they already have open.
homepage: https://github.com/web3toolshub/chrome-cdp-skill
user-invocable: false
metadata:
  openclaw:
    requires:
      bins:
        - node
    os:
      - darwin
      - linux
      - win32
    emoji: "🌐"
  version: 1.0.6
---

# Chrome CDP

Lightweight Chrome DevTools Protocol CLI. Connects directly via WebSocket, does not need Puppeteer, and works well with large tab counts.

## Prerequisites

- Chrome (or Chromium, Brave, Edge, Vivaldi) with remote debugging enabled: open `chrome://inspect/#remote-debugging` and toggle the switch
- Node.js 22+ (uses built-in WebSocket)
- No Python or pip packages are required
- No `npm install` step is required
- If your browser's `DevToolsActivePort` is in a non-standard location, set `CDP_PORT_FILE` to its full path

## Quick setup

1. Open Chrome and keep it running.
2. Open `chrome://inspect/#remote-debugging`.
3. Turn on remote debugging.
4. Keep the browser open while using this skill.
5. Run `{baseDir}/scripts/cdp.mjs list` to confirm that tabs are visible.

On first access to a tab, Chrome may ask the user to approve debugging access.

## Installation

- Recommended: `clawhub install chrome-cdp-skill`
- Manual: place this skill directory in your OpenClaw workspace `skills/` folder
- This skill does not require `npm install`, Python, or pip packages

## Safety

This skill can inspect and control a real local browser session. Commands such as `eval`, `evalraw`, `click`, `type`, and `nav` are intentionally powerful and may trigger warnings from security scanners.

Only use this skill when the user explicitly wants you to inspect or operate pages they already have open. Assume those tabs may contain sensitive logged-in content.

The skill only works after the user enables Chrome remote debugging. On first access to a tab, Chrome may ask the user to approve debugging access.

## Commands

All commands use `{baseDir}/scripts/cdp.mjs`. The `<target>` is a **unique** targetId prefix from `list`; copy the full prefix shown in the `list` output (for example `6BE827FA`). The CLI rejects ambiguous prefixes.

### List open pages

```bash
{baseDir}/scripts/cdp.mjs list
```

### Take a screenshot

```bash
{baseDir}/scripts/cdp.mjs shot <target> [file]    # default: screenshot-<target>.png in runtime dir
```

Captures the **viewport only**. Scroll first with `eval` if you need content below the fold. Output includes the page's DPR and coordinate conversion hint (see **Coordinates** below).

### Accessibility tree snapshot

```bash
{baseDir}/scripts/cdp.mjs snap <target>
```

### Evaluate JavaScript

```bash
{baseDir}/scripts/cdp.mjs eval <target> <expr>
```

> **Watch out:** avoid index-based selection (`querySelectorAll(...)[i]`) across multiple `eval` calls when the DOM can change between them (e.g. after clicking Ignore, card indices shift). Collect all data in one `eval` or use stable selectors.

### Other commands

```bash
{baseDir}/scripts/cdp.mjs html    <target> [selector]      # full page or element HTML
{baseDir}/scripts/cdp.mjs nav     <target> <url>           # navigate and wait for load
{baseDir}/scripts/cdp.mjs net     <target>                 # resource timing entries
{baseDir}/scripts/cdp.mjs click   <target> <selector>      # click element by CSS selector
{baseDir}/scripts/cdp.mjs clickxy <target> <x> <y>         # click at CSS pixel coords
{baseDir}/scripts/cdp.mjs type    <target> <text>          # Input.insertText at current focus; works in cross-origin iframes unlike eval
{baseDir}/scripts/cdp.mjs loadall <target> <selector> [ms] # click "load more" until gone (default 1500ms between clicks)
{baseDir}/scripts/cdp.mjs evalraw <target> <method> [json] # raw CDP command passthrough
{baseDir}/scripts/cdp.mjs open    [url]                    # open new tab (each triggers Allow prompt)
{baseDir}/scripts/cdp.mjs stop    [target]                 # stop daemon(s)
```

## Coordinates

`shot` saves an image at native resolution: image pixels = CSS pixels × DPR. CDP Input events (`clickxy` etc.) take **CSS pixels**.

```
CSS px = screenshot image px / DPR
```

`shot` prints the DPR for the current page. Typical Retina (DPR=2): divide screenshot coords by 2.

## Tips

- Prefer `snap --compact` over `html` for page structure.
- Use `type` (not eval) to enter text in cross-origin iframes — `click`/`clickxy` to focus first, then `type`.
- Chrome shows an "Allow debugging" modal once per tab on first access. A background daemon keeps the session alive so subsequent commands need no further approval. Daemons auto-exit after 20 minutes of inactivity.
