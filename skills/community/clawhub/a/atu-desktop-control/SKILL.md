---
name: desktop-control
description: Full desktop automation - screenshots, mouse, keyboard, window management, clipboard, screen info
version: 1.0.0
author: AtuTheDragon
tags: [desktop, automation, windows, screenshot, mouse, keyboard, clipboard, pyautogui]
platforms: [windows]
requirements: [python3]
---

# Desktop Control Skill

> Automate the desktop: screenshots, mouse, keyboard, window management, clipboard, and screen info.
> All commands output **JSON** with `"ok": true/false` for reliable agent parsing.

## Setup

Run the setup script to create a Python venv and install dependencies.
The skill directory is wherever this SKILL.md lives — all paths below are **relative to the skill root**.

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```

**Linux / macOS:**
```bash
bash scripts/setup.sh
```

## How to Run

The Python executable lives in the venv. Resolve it relative to the skill directory:

| OS | Python Path |
|---|---|
| Windows | `.venv\Scripts\python.exe` |
| Linux/Mac | `.venv/bin/python` |

All commands follow this pattern:
```
<python> scripts/desktop.py <command> [subcommand] [args]
```

**Agent shorthand** — set the working directory to the skill root, then:
```
exec({ command: ".venv\\Scripts\\python.exe scripts\\desktop.py <command> [args]", workdir: "<skillPath>" })
```

Where `<skillPath>` is the absolute path to this skill's directory (the folder containing this SKILL.md).

## Commands

### Screenshot

```bash
# Full screen (saves to captures/ dir, timestamped filename)
python scripts/desktop.py screenshot

# Save to specific path
python scripts/desktop.py screenshot -o C:\tmp\shot.png

# Region capture (left top width height)
python scripts/desktop.py screenshot --region 0 0 800 600
```

Output: `{"ok": true, "path": "...", "width": 1920, "height": 1080}`

### Mouse

```bash
# Current position
python scripts/desktop.py mouse pos

# Move to coordinates
python scripts/desktop.py mouse move 500 300
python scripts/desktop.py mouse move 500 300 --duration 0.5

# Click (left/right/middle, single/double/triple)
python scripts/desktop.py mouse click 500 300
python scripts/desktop.py mouse click 500 300 --button right
python scripts/desktop.py mouse click --clicks 2

# Drag from (100,100) to (400,400)
python scripts/desktop.py mouse drag 100 100 400 400 --duration 1.0

# Scroll (positive=up, negative=down)
python scripts/desktop.py mouse scroll 3
python scripts/desktop.py mouse scroll -5
python scripts/desktop.py mouse scroll 3 --direction horizontal
```

### Keyboard

```bash
# Type ASCII text
python scripts/desktop.py key type "hello world"

# Type with interval between keys
python scripts/desktop.py key type "slow typing" --interval 0.1

# Type Unicode / CJK text (auto-uses clipboard paste)
python scripts/desktop.py key type "你好世界"

# Press single key (repeat with --times)
python scripts/desktop.py key press enter
python scripts/desktop.py key press tab --times 3

# Hotkey combination
python scripts/desktop.py key hotkey ctrl c
python scripts/desktop.py key hotkey ctrl shift s
python scripts/desktop.py key hotkey alt f4
```

**Note:** For non-ASCII text (CJK, emoji, etc.), `key type` automatically uses clipboard paste via Ctrl+V.

### Window

```bash
# List all windows (title + hwnd)
python scripts/desktop.py window list

# Activate (bring to front) — matches title substring, case-insensitive
python scripts/desktop.py window activate "Chrome"
python scripts/desktop.py window activate 1234567   # by hwnd

# Minimize / Maximize
python scripts/desktop.py window minimize "Notepad"
python scripts/desktop.py window maximize "Code"

# Close a window
python scripts/desktop.py window close "Notepad"

# Get window info (position, size, state)
python scripts/desktop.py window info "Chrome"

# Resize a window (width height in pixels)
python scripts/desktop.py window resize "Notepad" 800 600

# Move a window (x y position)
python scripts/desktop.py window move "Notepad" 100 100
```

### Clipboard

```bash
# Read clipboard content
python scripts/desktop.py clipboard get

# Write to clipboard
python scripts/desktop.py clipboard set "copied text"
```

### Screen

```bash
# Get screen resolution
python scripts/desktop.py screen size

# Get pixel color at (x, y)
python scripts/desktop.py screen pixel 100 200
```

Pixel output: `{"ok": true, "x": 100, "y": 200, "r": 255, "g": 128, "b": 0, "hex": "#ff8000"}`

### Wait

```bash
# Wait for N seconds (useful in automation sequences)
python scripts/desktop.py wait 2.5
```

### Version

```bash
python scripts/desktop.py --version
```

## Scenarios

### "Take a full screenshot and show me the desktop"
```
exec: .venv\Scripts\python.exe scripts\desktop.py screenshot
→ returns JSON with path → use image tool to show the screenshot
```

### "Open Notepad and type some text"
```
exec: .venv\Scripts\python.exe scripts\desktop.py key hotkey win r
exec: .venv\Scripts\python.exe scripts\desktop.py wait 0.5
exec: .venv\Scripts\python.exe scripts\desktop.py key type "notepad"
exec: .venv\Scripts\python.exe scripts\desktop.py key press enter
exec: .venv\Scripts\python.exe scripts\desktop.py wait 1
exec: .venv\Scripts\python.exe scripts\desktop.py key type "Hello from desktop-control!"
```

### "Maximize the Chrome window"
```
exec: .venv\Scripts\python.exe scripts\desktop.py window maximize "Chrome"
```

### "Read clipboard content"
```
exec: .venv\Scripts\python.exe scripts\desktop.py clipboard get
```

### "Move and resize a window"
```
exec: .venv\Scripts\python.exe scripts\desktop.py window move "Notepad" 0 0
exec: .venv\Scripts\python.exe scripts\desktop.py window resize "Notepad" 1024 768
```

## Safety

- **Failsafe ON by default**: Move mouse to top-left corner (0,0) to abort any pyautogui operation.
- Use `--no-failsafe` to disable (NOT recommended).
- All actions return structured JSON for audit trail.
- Screenshots saved locally only — no network requests.
- Captures directory: `captures/` (relative to skill root).

## Optional Dependencies

For advanced workflows, you may also install:

| Package | Use Case |
|---|---|
| `openpyxl` | Read/write Excel files |
| `python-docx` | Read/write Word documents |
| `pywin32` | Advanced Windows COM automation |

These are **not** installed by default setup scripts. Install manually if needed:
```
.venv\Scripts\pip install openpyxl python-docx pywin32
```

## Troubleshooting

| Problem | Solution |
|---|---|
| `pyautogui not installed` | Run `scripts/setup.ps1` (Windows) or `scripts/setup.sh` (Linux/Mac) |
| `Window not found` | Use `window list` to see available windows; matching is case-insensitive substring |
| `Failed to activate` | Window may be minimized — the script tries `restore()` first, but some apps resist |
| Screenshot is black | Common with GPU-accelerated apps; try capturing a region instead |
| `key type` garbled for CJK | Should auto-use clipboard paste; verify `pyperclip` is installed |
| `FAILSAFE` triggered | Mouse hit (0,0) corner; this is intentional safety — reposition mouse and retry |
| Permission denied on Linux | `pyautogui` needs X11/Wayland access; run from a GUI session, not SSH |

## Limitations

- **Windows-primary**: Full feature set (window management, all shortcuts) works on Windows. Linux/macOS have partial support via pyautogui but `pygetwindow` behavior may differ.
- **Requires GUI session**: Must run in a desktop session with a display. Headless servers or SSH sessions without X forwarding will fail.
- **Single monitor**: `screenshot` captures the primary monitor by default. Multi-monitor capture requires `--region`.
- **Admin windows**: Cannot interact with windows running as Administrator from a non-admin Python process (Windows UAC).
- **Screen scaling**: DPI scaling (125%, 150%) may cause coordinate mismatches. Use `screen size` to verify actual resolution.
