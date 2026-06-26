---
name: screenshot-tool
description: Capture screenshots and screen recordings. Use when user needs to take screenshots, record screen activity, capture windows, or create screen recordings for tutorials.
---

# Screenshot Tool

Capture screenshots and screen recordings.

## Quick Start

```bash
# Take screenshot
python scripts/screenshot.py --capture

# Capture specific window
python scripts/screenshot.py --window "Chrome"
```

## Usage

```bash
python scripts/screenshot.py [OPTIONS]

Options:
  --capture         Take screenshot
  --record         Start screen recording
  --stop           Stop recording
  --window NAME    Capture specific window
  --area X,Y,W,H   Capture area (x,y,width,height)
  --output PATH    Output file path
  --format FORMAT  Format: png, jpg (default: png)
```

## Examples

```bash
# Full screen
python scripts/screenshot.py --capture

# Window
python scripts/screenshot.py --window "Terminal" --output terminal.png

# Region
python scripts/screenshot.py --area 0,0,800,600 --output region.png

# With delay
python scripts/screenshot.py --delay 5 --output delayed.png
```

## Features

- Full screen capture
- Window capture
- Region capture
- Screen recording
- Delayed capture
- Multiple formats
