---
name: arise-browser
description: >
  Browser automation for AI agents — control Chrome via CLI commands with persistent element refs,
  YAML accessibility snapshots, and WebRTC live view. Install once, snap/act/snap loop.
homepage: https://github.com/AriseOS/arise-browser
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      bins: ["npx", "docker"]
---

# AriseBrowser

You are controlling a **real Chrome browser**, like a human sitting in front of a screen. You see the page through snapshots, and you interact by clicking, typing, and selecting — not by writing JavaScript or constructing URLs.

## MANDATORY RULES

1. **Snapshot is your eyes.** After every navigate or action, run `arise-browser snap` to see the page. Read refs (e0, e5, e12...) from the output.
2. **Act through refs.** Use `click`, `type`, `select` with refs from your snapshot. Do NOT construct URLs with query parameters to change page state.
3. **Refs are persistent.** Do NOT re-snap just to reuse a ref. Only re-snap when the page content changes.

## Install

```bash
npm install -g arise-browser
```

## Start

```bash
arise-browser start --virtual-display
# → "Server ready on port 16473"
```

First run takes ~2 minutes (Docker pulls Chrome image ~700MB). Everything is automatic.

**Watch the browser:** Open `http://localhost:6090` in your browser, password: `neko`

## Core Loop

```bash
# Navigate to a page
arise-browser open https://example.com

# See the page — YAML accessibility tree with refs
arise-browser snap

# Interact using refs from the snapshot
arise-browser click e5
arise-browser type e12 "laptop"
arise-browser select e187 "Best Sellers"
arise-browser press Enter
arise-browser scroll down 500

# See updated page after actions
arise-browser snap
```

### Example: Sort Amazon results by Best Sellers

```bash
# 1. Navigate
arise-browser open "https://amazon.com/s?k=laptop"

# 2. Snapshot — see the page
arise-browser snap
# → combobox "Sort by:" [ref=e187]
# → link "Product Name" [ref=e226]
# → generic "$599.99" [ref=e246]

# 3. Select from dropdown using ref
arise-browser select e187 "exact-aware-popularity-rank"

# 4. Snapshot again — results are now sorted
arise-browser snap
```

## All Commands

| Command | What it does |
|---------|-------------|
| `arise-browser start [--virtual-display]` | Start server (daemon) |
| `arise-browser stop` | Stop server + cleanup |
| `arise-browser open <url>` | Navigate to URL |
| `arise-browser snap` | Page snapshot (YAML) |
| `arise-browser click <ref>` | Click element |
| `arise-browser type <ref> <text>` | Type into element |
| `arise-browser select <ref> <value>` | Select dropdown value |
| `arise-browser press <key>` | Press key (Enter, Tab, Escape...) |
| `arise-browser scroll <dir> [amount]` | Scroll (up/down/left/right) |
| `arise-browser screenshot [file]` | Save screenshot |
| `arise-browser tabs` | List open tabs |
| `arise-browser health` | Check server status |

## Stop

```bash
arise-browser stop
```

## How to Think

You are a person using a browser. Snapshot is your eyes, commands are your hands.

- **To sort results** → find the sort dropdown ref in snap → `select` it
- **To search** → find the search box ref → `type` your query → `press Enter`
- **To go to next page** → find the "Next" button ref → `click` it
- **To read product info** → it's already in the snapshot (names, prices, ratings are all there)

## Tips

- **Read the snapshot carefully.** Product names, prices, ratings, links — they're all there. No need for JavaScript.
- Screenshot is useful to show the user what you see.
- After scrolling, snap again to see newly visible elements.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| First run slow | Docker pulling Chrome image (~700MB), wait ~2 min |
| `health` returns "not running" | Run `arise-browser start --virtual-display` |
| Action returns error | Snap first to get valid refs, then act on them |
| Can't find an element | `arise-browser scroll down` then `arise-browser snap` |
