# Control Host Browser Skill Package

This package provides a reliable way to control the host Chrome browser by:
1. Creating new tabs via Chrome DevTools Protocol (CDP)
2. Navigating to URLs using WebSocket-based CDP commands

## Why this skill?

The previous `browsercontrol` skill had a bug in `cdp_navigate.js` where the WebSocket navigation command didn't reliably execute. This new skill uses a Python-based approach that has been tested and proven to work.

## Files

- `control_host_browser.sh` - Main script that orchestrates the two-step process
- `cdp_navigate.py` - Python script for sending CDP commands via WebSocket
- `SKILL.md` - Skill metadata and usage instructions
- `README.md` - This file

## Usage

```bash

# Navigate to example on the 'main' browser instance
./control_host_browser.sh financier "https://www.example.com"
```

## Technical Details

### Step 1: Create Tab
Uses `curl` to call Chrome's CDP JSON API:
```bash
curl -s -X PUT "http://172.17.0.1:<PORT>/json/new"
```
Returns page metadata including the `id` (Tab ID).

### Step 2: Navigate
Uses a Python script to:
1. Establish a WebSocket connection to `/devtools/page/<PAGE_ID>`
2. Perform the WebSocket handshake
3. Send a CDP `Page.navigate` command
4. Wait for confirmation and close

## Port Mapping

| Profile   | Port  |
|-----------|-------|
| main      | 18800 |

## Requirements

- Python 3.x (for `cdp_navigate.py`)
- `curl` (for tab creation)
- Host Chrome browser with CDP enabled on the specified ports
