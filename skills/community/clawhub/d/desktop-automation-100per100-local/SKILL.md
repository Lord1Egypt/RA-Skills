# Desktop Automation Skill v2.0

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://github.com/openclaw/openclaw)

**Complete desktop automation for Windows/macOS/Linux. Zero-error edition.**

---

## ⚠️ **Privacy & Security**

**CRITICAL**: This skill captures ALL keyboard and mouse events. 
- **NEVER record while entering passwords, credit cards, or secrets**
- Recorded macros are stored as JSON in `recorded_macro/` directory
- Always use **dry_run=true** to test before actual execution
- Store macros in secure locations only
- Enable safe mode by default (it is)

---

## 🎯 **What It Does**

Automate desktop interactions without APIs:
- ✅ Click, type, drag, scroll
- ✅ Capture screenshots
- ✅ Recognize images (OpenCV template matching)
- ✅ Extract text (Tesseract OCR)
- ✅ Record and replay macros
- ✅ Find windows by title
- ✅ Clipboard operations
- ✅ Safe mode with dry_run for testing

---

## 🔐 **Safety Features (Built-In)**

### 1. **Safe Mode** (Default: ON)
Blocks dangerous actions when enabled:
- `type`, `press_key`, `click`, `drag` are monitored
- Parameters are scanned for dangerous patterns: `rm `, `del `, `C:\Windows\`, `/etc/`, `sudo`, etc.
- Blocked actions are logged

### 2. **Dry-Run Mode**
All actions support `dry_run=true`:
- Action is logged but NOT executed
- Use for testing before running real automation

### 3. **Audit Logging**
Every action logged to `~/.openclaw/skills/desktop-automation-logs/automation_YYYY-MM-DD.log`

### 4. **Thread Safety**
All modules use locks to prevent race conditions.

---

## 📦 **Installation**

### 1. Extract Files
Place `desktop-automation-ultra-local/` in:
- Windows: `C:\Users\<User>\.openclaw\workspace\skills\`
- Linux/macOS: `~/.openclaw/workspace/skills/`

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Optional: Tesseract for OCR
For `find_text_on_screen` functionality:
- **Windows**: Download installer from https://github.com/UB-Mannheim/tesseract/wiki
- **Linux**: `sudo apt install tesseract-ocr`
- **macOS**: `brew install tesseract`

### 4. Restart OpenClaw
```bash
openclaw gateway restart
```

---

## 🚀 **Quick Start**

### Basic Click
```yaml
action: click
params:
  x: 100
  y: 100
  dry_run: true  # Test first!
```

### Type Text
```yaml
action: type
params:
  text: "Hello World"
  interval: 0.05  # Delay between keys
  dry_run: false
```

### Find Image
```yaml
action: find_image
params:
  template_path: "templates/button.png"
  confidence: 0.95
```

### Extract Text (OCR)
```yaml
action: read_text_ocr
params:
  lang: "fra"  # French
```

---

## 📖 **Core Actions**

### **Mouse & Keyboard**

| Action | Parameters | Returns |
|--------|------------|---------|
| `click` | `x`, `y`, `button="left"`, `dry_run` | `{status, x, y}` |
| `type` | `text`, `interval=0.05`, `dry_run` | `{status, text}` |
| `press_key` | `key`, `dry_run` | `{status, key}` |
| `move_mouse` | `x`, `y`, `duration=0.5`, `dry_run` | `{status, x, y}` |
| `scroll` | `amount=5`, `dry_run` | `{status, amount}` |
| `drag` | `start_x`, `start_y`, `end_x`, `end_y`, `duration=0.5`, `dry_run` | `{status}` |
| `copy_to_clipboard` | `text`, `dry_run` | `{status}` |
| `paste_from_clipboard` | `dry_run` | `{status, length}` |

### **Screenshots & Windows**

| Action | Parameters | Returns |
|--------|------------|---------|
| `screenshot` | `path="~/Desktop/screenshot.png"`, `dry_run` | `{status, path}` |
| `get_active_window` | `dry_run` | `{status, title, x, y, width, height}` |
| `list_windows` | `dry_run` | `{status, windows[], count}` |
| `activate_window` | `title_substring`, `dry_run` | `{status, title}` |

### **Image Recognition** (requires OpenCV)

| Action | Parameters | Returns |
|--------|------------|---------|
| `find_image` | `template_path`, `confidence=0.9`, `dry_run` | `{status, x, y, confidence}` |
| `find_image_multiscale` | `template_path`, `confidence`, `scale_factors`, `dry_run` | `{status, x, y, confidence, scale}` |
| `wait_for_image` | `template_path`, `timeout=30.0`, `interval=0.5`, `confidence=0.9`, `dry_run` | `{status, x, y, confidence}` |

### **OCR / Text Recognition** (requires Tesseract)

| Action | Parameters | Returns |
|--------|------------|---------|
| `find_text_on_screen` | `text`, `lang="fra"`, `dry_run` | `{status, locations[], count}` |
| `find_all_text_on_screen` | `text`, `lang="fra"`, `dry_run` | `{status, data[], count}` |
| `read_text_ocr` | `lang="fra"`, `dry_run` | `{status, text, length}` |
| `read_text_region` | `x`, `y`, `width`, `height`, `lang="fra"`, `dry_run` | `{status, text, length}` |
| `extract_screen_data` | `region={}`, `output_format="json"`, `lang="fra"`, `dry_run` | `{status, data[], count}` |

### **Macros**

| Action | Parameters | Returns |
|--------|------------|---------|
| `play_macro` | `macro_path`, `speed=1.0`, `dry_run` | `{status, executed, total, errors[]}` |
| `stop_macro` | — | `{status}` |
| `play_macro_with_subroutines` | `macro_path`, `speed=1.0`, `sub_macros_dir`, `dry_run` | `{status, executed, total, errors[]}` |

### **Safety Management**

| Action | Parameters | Returns |
|--------|------------|---------|
| `set_safe_mode` | `enabled=true` | `{status, safe_mode}` |
| `get_safety_status` | — | `{status, safe_mode_enabled, dangerous_patterns, dangerous_actions[]}` |

---

## 📝 **Macro Format**

Recorded macros are JSON with this structure:

```json
{
  "events": [
    {
      "action": "click",
      "params": {"x": 100, "y": 50},
      "wait": 500
    },
    {
      "action": "type",
      "params": {"text": "Hello"},
      "wait": 200
    },
    {
      "action": "press_key",
      "params": {"key": "return"},
      "wait": 100
    }
  ]
}
```

- `action` — action name
- `params` — action parameters
- `wait` — milliseconds to wait before next action

---

## 🔧 **Advanced: Mouse Move Debouncing**

To avoid recording hundreds of `move_mouse` events during a smooth drag, the recorder uses **debouncing**:

- When you move the mouse, events are **suppressed** during movement
- After you **stop moving** for `N` seconds (default: 1 sec), the **final position** is recorded
- This reduces macro size dramatically while preserving intended end positions
- Configurable via GUI: set debounce time (0.1–10 seconds)

**Example:**
- Fast horizontal line → 1 `move_mouse` event (end coordinates)
- Slow, stop-and-go → multiple `move_mouse` events (one per "stop")

---

## 🧪 **Testing**

Run the unit test suite:
```bash
python scripts/test_automation.py
```

Output:
```
test_dry_run_click ... ok
test_get_active_window ... ok
test_safe_mode_blocks_dangerous ... ok
...
Ran 13 tests
OK
```

---

## 📊 **Logging**

All actions logged to: `~/.openclaw/skills/desktop-automation-logs/automation_YYYY-MM-DD.log`

Example:
```
[2026-03-15 10:23:45] [INFO] ActionManager: ActionManager initialized with safe_mode=True
[2026-03-15 10:23:46] [INFO] ActionManager: Clicked at (100, 50) with left button
[2026-03-15 10:23:47] [INFO] ActionManager: Typed: Hello World
```

---

## ⚙️ **Configuration**

### Environment Variables
```bash
# Override log directory
export AUTOMATION_LOG_DIR=~/my_logs

# Disable safe mode globally (NOT recommended)
export AUTOMATION_SAFE_MODE=false
```

---

## 🐛 **Troubleshooting**

### "pyautogui failsafe triggered"
Move mouse to corner of screen to stop.

### OCR returns empty text
- Ensure Tesseract is installed correctly
- Check image quality (high contrast helps)
- Try `read_text_ocr` instead of `find_text_on_screen`

### Image recognition not finding template
- Ensure template image exists and is correct format (PNG, JPG)
- Try lower confidence threshold (e.g., 0.85 instead of 0.95)
- Use `find_image_multiscale` to detect at different scales

### Actions blocked by safe mode
This is intentional. To run dangerous actions:
```yaml
action: set_safe_mode
params:
  enabled: false
```
Then execute your action. Re-enable safe mode immediately after:
```yaml
action: set_safe_mode
params:
  enabled: true
```

---

## 📄 **License**

MIT License. See LICENSE file.

---

## 📚 **Files Structure**

```
desktop-automation-ultra-local/
├── SKILL.md                          (This file)
├── requirements.txt                  (Python dependencies)
├── lib/
│   ├── actions.py                   (Core click/type/drag actions)
│   ├── image_recognition.py         (OpenCV template matching)
│   ├── ocr_engine.py                (Tesseract OCR)
│   ├── macro_player.py              (Record/playback macros)
│   ├── safety_manager.py            (Safe mode, blocking)
│   └── utils.py                     (Logging, helpers)
├── scripts/
│   └── test_automation.py           (Unit tests)
└── recorded_macro/                  (Output: saved macros)
```

---

## ✅ **Validation Checklist**

- [x] All modules have proper error handling
- [x] Thread safety implemented (locks)
- [x] Safe mode enabled by default
- [x] Dry-run mode on all actions
- [x] Comprehensive logging
- [x] Unit tests (13 tests)
- [x] UTF-8 encoding for all text
- [x] No hardcoded paths (uses expanduser)
- [x] Graceful fallbacks for missing dependencies
- [x] Documentation complete

**Status: PRODUCTION READY** ✅

---

*Last updated: 2026-03-15*
*Version: 2.0.0*
