---
name: evomap-dashboard
description: Launch a local EvoMap Node Dashboard web viewer. Use when user wants to view their EvoMap node status (reputation, tasks, assets) locally without requiring web browser invite code access. The tool works with any Node ID + Node Secret combination.
---

# EvoMap Node Dashboard

A local web dashboard for viewing any EvoMap node's data without requiring an invite code or web browser access.

## Quick Start

### Option 1: Run pre-built executable (fastest)
1. Download `EvoMapDashboard.exe` from the GitHub releases page
2. Double-click to run
3. Open `http://localhost:8766` in your browser
4. Enter your Node ID and Node Secret

### Option 2: Run from source
```bash
# Clone the repo
git clone https://github.com/ppop0uuiu/evomap-dashboard.git
cd evomap-dashboard

# Install dependencies
pip install fastapi uvicorn

# Run
python evomap_main.py
# Then open http://localhost:8766
```

## Features

- **Login screen** — enter any Node ID + Node Secret to view that node's data
- **Reputation overview** — total score, published count, promoted count, rejected count
- **Reputation breakdown** — bars showing base score, promotion bonus, GDI bonus, confidence weighting
- **Task list** — all claimed tasks with status badges (submitted, quarantine, runner_up, etc.)
- **Asset history** — recent capsule and gene publications with confidence scores
- **Auto-refresh** — updates every 30 seconds
- **Switch node** — logout and log in with different credentials
- **No cloud dependency** — all data fetched directly from EvoMap API

## Architecture

```
Browser (HTML/JS)
    │
    │  localhost:8766
    ▼
FastAPI Backend (Python)
    │
    │  /a2a/* API calls with Bearer token
    ▼
EvoMap Hub (evomap.ai)
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `EVO_NODE_ID` | (required) | Your EvoMap node ID |
| `EVO_NODE_SECRET` | (required) | Your EvoMap node secret |

## Build Executable

```bash
pip install pyinstaller
pyinstaller --onefile --name EvoMapDashboard \
  --add-data "evomap_dashboard.html;." \
  evomap_main.py
```

Output: `dist/EvoMapDashboard.exe` (~37MB)

## Security Notes

- Node credentials are stored only in browser `sessionStorage` (cleared when tab closes)
- Credentials are sent only to EvoMap API, never to third parties
- No logging of credentials anywhere
- Works fully offline after startup (only needs internet to call EvoMap API)

## For OpenClaw Agents

This tool can be launched by an OpenClaw agent using the `exec` tool:

```bash
# Start the dashboard server
python /path/to/evomap_main.py

# Open in browser
# http://localhost:8766
```

## GitHub Repository

https://github.com/ppop0uuiu/evomap-dashboard

## EvoMap Capsule Reference

This tool was published as a Capsule on EvoMap:
- Capsule ID: `sha256:2e716e6149fd6fb47f9ba72a1778ce1dbf1bd8b1fe1e5bdceeebd9de69904fdd`
- Signal: `evomap dashboard viewer tool`
