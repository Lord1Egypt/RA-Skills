# 🖥️ Desktop Control

**Full desktop automation for AI agents** — screenshots, mouse, keyboard, window management, clipboard, and screen info.

Built for [OpenClaw](https://github.com/nichochar/openclaw) agents. All commands output structured JSON for reliable parsing.

## Features

- 📸 **Screenshots** — full screen, region capture, custom output path
- 🖱️ **Mouse** — move, click, drag, scroll (vertical & horizontal)
- ⌨️ **Keyboard** — type text (ASCII + Unicode/CJK), press keys, hotkey combos
- 🪟 **Window Management** — list, activate, minimize, maximize, close, resize, move
- 📋 **Clipboard** — read and write
- 🖥️ **Screen** — resolution, pixel color
- ⏱️ **Wait** — timed delays for automation sequences

## Quick Start

### Windows
```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
.venv\Scripts\python.exe scripts\desktop.py screen size
```

### Linux / macOS
```bash
bash scripts/setup.sh
.venv/bin/python scripts/desktop.py screen size
```

## Example Output

```json
{"ok": true, "width": 1920, "height": 1080}
```

Every command returns JSON with `"ok": true` on success or `"ok": false, "error": "..."` on failure.

## Requirements

- Python 3.8+
- A desktop GUI session (not headless/SSH)
- Windows recommended for full feature set

## Platform Support

| Feature | Windows | Linux | macOS |
|---|:---:|:---:|:---:|
| Screenshots | ✅ | ✅ | ✅ |
| Mouse | ✅ | ✅ | ✅ |
| Keyboard | ✅ | ✅ | ✅ |
| Window Mgmt | ✅ | ⚠️ | ⚠️ |
| Clipboard | ✅ | ✅ | ✅ |

⚠️ = Partial support; may require additional packages.

## License

MIT
