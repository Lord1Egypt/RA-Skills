# Desktop Automation Skill for OpenClaw

**âš ï¸  PRIVACY WARNING**: The macro recorder captures **ALL** keyboard events (including passwords, credit card numbers, private messages) and window titles. **Never record while entering credentials.** Only use for non-sensitive workflows. Store recorded macros securely.

Full desktop automation: control mouse, keyboard, windows, OCR, image recognition â€” all local.

- **PyAutoGUI** for basic actions
- **OpenCV** for image recognition
- **pytesseract** for OCR

---

## ðŸ” Security & Privacy

### âš ï¸ Keyboard Recording Warning
The **macro recorder** captures **ALL** keyboard events, including passwords, credit card numbers, and personal data. **Never** record macros while entering credentials. Use only for non-sensitive workflows. Recorded macro files contain raw keystrokes â€” store them securely.

**Summary**:
- No network access â€” completely local
- No credential storage (unless you record them)
- All dependencies are standard Python packages
- You are responsible for macro file security

---

## Installation

### Prerequisites
- Python 3.10+
- Pip

### Install dependencies

```bash
pip install -r requirements.txt
```

### ðŸ¤– Advanced Features (v2+)

The skill includes powerful advanced features for power users.

---

### Multi-Scale Image Detection

`find_image_multiscale` searches for a template at multiple scales. Useful when the UI element size varies (e.g., high-DPI displays).

```javascript
sessions_spawn({
  task: 'find_image_multiscale',
  params: {
    template_path: "C:/templates/button.png",
    confidence: 0.85,
    scale_factors: [0.5, 0.75, 1.0, 1.25, 1.5]  // optional, default includes these
  },
  label: 'desktop-automation-ultra-local'
});
```

**Response**:
```json
{
  "status": "ok",
  "x": 400,
  "y": 300,
  "confidence": 0.92,
  "scale": 1.25
}
```

---

### Find All Text Occurrences

`find_all_text_on_screen` returns every match, not just the first. Great for extracting tables or lists.

```javascript
sessions_spawn({
  task: 'find_all_text_on_screen',
  params: {
    text: "Total",
    lang: "eng"
  },
  label: 'desktop-automation-ultra-local'
});
```

**Response**:
```json
{
  "status": "ok",
  "matches": [
    {"text": "Total", "left": 100, "top": 200, "width": 50, "height": 20, "conf": 98.5},
    {"text": "Total", "left": 300, "top": 200, "width": 50, "height": 20, "conf": 97.2}
  ],
  "count": 2
}
```

---

### Detect UI Elements

`detect_ui_elements` uses shape heuristics to find common UI components.

```javascript
sessions_spawn({
  task: 'detect_ui_elements',
  params: {
    element_type: "button"  // omit for all types
  },
  label: 'desktop-automation-ultra-local'
});
```

**Response**:
```json
{
  "status": "ok",
  "elements": [
    {"type": "button", "x": 120, "y": 80, "w": 80, "h": 30, "area": 2400},
    {"type": "field", "x": 120, "y": 130, "w": 200, "h": 25, "area": 5000}
  ],
  "count": 2
}
```

---

### Conditional Monitoring with Logic

`monitor_screen_with_logic` extends `monitor_screen` with AND/OR logic between conditions.

```javascript
sessions_spawn({
  task: 'monitor_screen_with_logic',
  params: {
    conditions: [
      {
        type: "image",
        template_path: "C:/templates/ok.png",
        confidence: 0.9,
        logic: "AND",
        actions: [
          {"action": "click", "params": {}}
        ]
      },
      {
        type: "text",
        text: "Success",
        logic: "OR",
        actions: [
          {"action": "press_key", "params": {"key": "enter"}}
        ]
      }
    ],
    timeout: 60,
    interval: 0.5
  },
  label: 'desktop-automation-ultra-local'
});
```

---

### Macros with Subroutines

`play_macro_with_subroutines` allows nested macro calls. Create a macro file that contains:
```json
{
  "events": [
    {"action": "type", "params": {"text": "Hello"}},
    {"action": "call_macro", "params": {"macro_file": "submacro.json"}}
  ]
}
```

Run it:
```javascript
sessions_spawn({
  task: 'play_macro_with_subroutines',
  params: {
    macro_path: "C:/macros/main.json",
    speed: 1.0,
    sub_macros_dir: "C:/macros/subs"
  },
  label: 'desktop-automation-ultra-local'
});
```

---

### Protected Macros (Password-Locked)

Create a macro encrypted with AES using a password:

```javascript
sessions_spawn({
  task: 'create_protected_macro',
  params: {
    output_path: "C:/macros/secure.enc",
    password: "MySecret123",
    macro_events: [
      {"action": "click", "params": {"x":100,"y":200}}
    ]
  },
  label: 'desktop-automation-ultra-local'
});
```

Load and decrypt:
```javascript
sessions_spawn({
  task: 'load_and_decrypt_protected_macro',
  params: {
    encrypted_path: "C:/macros/secure.enc",
    password: "MySecret123"
  },
  label: 'desktop-automation-ultra-local'
});
// Returns {"status":"ok", "events": [...]} â€” you can then play them
```

---

### Macro Execution Reports

`generate_macro_report` creates HTML and JSON logs of macro execution:

```javascript
sessions_spawn({
  task: 'generate_macro_report',
  params: {
    macro_path: "C:/macros/my_macro.json",
    execution_log: {
      "status": "ok",
      "actions": [
        {"action": "click", "params": {"x":100,"y":200}, "result": {"status":"ok"}}
      ],
      "elapsed": 12.34
    }
  },
  label: 'desktop-automation-ultra-local'
});
```

**Response**:
```json
{
  "status": "ok",
  "report_json": "C:/macros/reports/report_2026-03-15_00-54-00.json",
  "report_html": "C:/macros/reports/report_2026-03-15_00-54-00.html"
}
```

---

### Macro Stop Hotkey (Safety)

The `MacroStopManager` class (used internally) can stop a running macro via a hotkey combination. This is a safety feature to abort long-running or misbehaving macros. (In the current version, hotkey is configurable but not exposed as a direct action; it's used by the framework.)

---

### Dependencies Explained
The skill uses several Python packages. Here's a quick summary:

| Package | Purpose | Actions that need it |
|---------|---------|---------------------|
| pyautogui | mouse/keyboard control, screenshots | all basic actions |
| pygetwindow | window management | activate_window, list_windows, get_active_window |
| Pillow | image processing | used by pyautogui |
| pynput | macro recording (listeners) | record_macro |
| opencv-python | image recognition | find_image, wait_for_image, find_image_multiscale, find_on_screen, click_image |
| pytesseract | OCR (text from images) | find_text_on_screen, extract_screen_data, find_all_text_on_screen, read_text_ocr, read_text_region |
| pyperclip | clipboard access | copy_to_clipboard, paste_from_clipboard |
| openpyxl | Excel read/write | excel_read, excel_write |
| pandas | CSV/DataFrame conversion | data_to_csv (and used by excel functions) |
| cryptography | AES encryption for protected macros | create_protected_macro, load_and_decrypt_protected_macro |
| mss | fast screen capture | screenshot_mss, vision functions (fallback if missing) |
| numpy | array operations (OpenCV, mss) | used by opencv-python and mss |

**Optional packages**: If a package is missing, related actions will return an error. You can install selectively:
```bash
# Minimal
pip install pyautogui pygetwindow Pillow pynput
# + Image recognition
pip install opencv-python
# + OCR
pip install pytesseract
# + Clipboard
pip install pyperclip
# + Excel/CSV
pip install openpyxl pandas
```

For full details, see `DEPENDENCIES.md` in this skill folder.

---

### Enable skill
Place the folder `desktop-automation-ultra-local` in your OpenClaw skills directory:
```bash
pip install -r requirements.txt
```

### Enable skill
Place the folder `desktop-automation-ultra-local` in your OpenClaw skills directory:
- **Windows**: `C:\Users\<YourUsername>\.openclaw\workspace\skills\`
- **Linux/macOS**: `~/.openclaw/workspace/skills/`

Then restart OpenClaw:
```bash
openclaw gateway restart
```

---

## Available Actions

### Basic Actions
- `click` â€” click at coordinates
- `type` â€” type text
- `screenshot` â€” capture screen
- `get_active_window` â€” get active window info
- `list_windows` â€” list all windows
- `activate_window` â€” activate window by title substring
- `move_mouse` â€” move cursor
- `press_key` â€” press a single key
- `scroll` â€” scroll screen
- `copy_to_clipboard` â€” copy text to clipboard
- `paste_from_clipboard` â€” paste from clipboard
- `drag` â€” drag from start to end

### Advanced Actions
- `find_image` â€” locate image on screen (OpenCV)
- `wait_for_image` â€” wait until image appears
- `monitor_screen` â€” conditional monitoring: watch for images/text and trigger actions
- `find_text_on_screen` â€” OCR text search
- `extract_screen_data` â€” extract structured text data (OCR) from screen or region
- `excel_read` â€” read data from an Excel file into list of dicts
- `excel_write` â€” write list of dicts/lists to an Excel file
- `data_to_csv` â€” convert list of dicts to CSV (string or file)

---

## Examples

```javascript
// Click and type
sessions_spawn({ task: 'click {"x":100,"y":200}', label: 'desktop-automation-ultra-local' });
sessions_spawn({ task: 'type {"text":"Hello World"}', label: 'desktop-automation-ultra-local' });

// Take screenshot
sessions_spawn({ task: 'screenshot {"path":"~/Desktop/screen.png"}', label: 'desktop-automation-ultra-local' });

// Activate Notepad
sessions_spawn({ task: 'activate_window {"title_substring":"Notepad"}', label: 'desktop-automation-ultra-local' });

// Find an image
sessions_spawn({
  task: 'find_image {"template_path":"C:/button.png","confidence":0.9}',
  label: 'desktop-automation-ultra-local'
});
```

---

## Macro Recording

### GUI Recorder
Run the Tkinter GUI to record macros:
```bash
python scripts/record_macro.py
```
Records: mouse moves, clicks, scrolling, keyboard, window switches.
Saves JSON files to `recorded_macro/`.

#### Mouse Move Debouncing
To avoid recording hundreds of `move_mouse` events during a smooth drag, the recorder uses **debouncing**:

- **Configurable debounce time** (default: 1 second) via the GUI entry field
- When you move the mouse, events are suppressed during movement
- After you **stop moving** for the debounce period, the **final position** is recorded
- This reduces macro size dramatically while preserving intended end positions

**Example:**
- Fast horizontal line â†’ 1 `move_mouse` event (end coordinates)
- Slow, stop-and-go â†’ multiple `move_mouse` events (one per "stop")

Adjust the debounce time in the GUI to suit your workflow (0.1â€“10 seconds).

### CLI Player
Replay a recorded macro:
```bash
python scripts/play_macro.py recorded_macro/macro_2026-03-14_22-00-00.json 1.0
```
Speed factor optional (1.0 = normal).

---

## ðŸ” Monitor Screen (Conditional Automation)

The `monitor_screen` action watches the screen for specific visual elements (images or text) and executes actions when they appear.

### Parameters

```json
{
  "checks": [
    {
      "type": "image" | "text",
      "template_path": "path/to/template.png",
      "confidence": 0.9,
      "text": "string to find",
      "lang": "fra",
      "action": "click",
      "action_params": { "button": "left" }
    }
  ],
  "timeout": 60,
  "interval": 0.5,
  "stop_condition": "first_match",
  "fallback_confidence": 0.85
}
```

- `checks`: array of conditions to monitor
- `timeout`: max seconds to monitor (default 60)
- `interval`: check every N seconds (default 0.5)
- `stop_condition`:
  - `"first_match"`: stop after first condition matches (default)
  - `"all_matched"`: stop when all conditions have matched at least once
  - `null` or omitted: run until timeout
- `fallback_confidence`: if image not found at initial confidence, automatically retry with lower thresholds (0.85, 0.8, 0.75, ...). Set to `null` to disable.

### Example: Click a pop-up as soon as it appears

```javascript
sessions_spawn({
  task: 'monitor_screen',
  params: {
    checks: [
      {
        type: "image",
        template_path: "C:/templates/ok_button.png",
        confidence: 0.9,
        action: "click"
      }
    ],
    timeout: 30,
    stop_condition: "first_match"
  },
  label: 'desktop-automation-ultra-local'
});
```

### Example: Type credentials when fields appear

```javascript
sessions_spawn({
  task: 'monitor_screen',
  params: {
    checks: [
      {
        type: "text",
        text: "Email",
        lang: "eng",
        action: "type",
        action_params: { "text": "user@example.com", "interval": 0.05 }
      },
      {
        type: "text",
        text: "Password",
        lang: "eng",
        action: "type",
        action_params: { "text": "secret123", "interval": 0.05 }
      }
    ],
    timeout: 20,
    stop_condition: "all_matched"
  },
  label: 'desktop-automation-ultra-local'
});
```

---

## Configuration

### OCR (pytesseract)
- Install [Tesseract](https://github.com/tesseract-ocr/tesseract) on your OS.
- On Windows, add to PATH or set:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```
- Install language packs (`fra`, `eng`, etc.)

### Pyperclip
- Linux: install `xclip` or `xsel`
- Windows/macOS: usually works out of the box

---

## ðŸ“Š Data Integration

### extract_screen_data
Extract structured text data from the screen (or a specific region) using Tesseract OCR. Returns bounding boxes, text, and confidence scores.

```javascript
sessions_spawn({
  task: 'extract_screen_data',
  params: {
    region: {x: 0, y: 0, width: 800, height: 600},  // optional
    output_format: 'json'  // default
  },
  label: 'desktop-automation-ultra-local'
});
```

**Response**:
```json
{
  "status": "ok",
  "data": [
    {"text": "Total", "left": 100, "top": 200, "width": 50, "height": 15, "conf": 98.5},
    {"text": "$123.45", "left": 200, "top": 200, "width": 60, "height": 15, "conf": 99.1}
  ],
  "count": 2
}
```

### excel_read
Read an Excel file (.xlsx) and return rows as an array of objects (keys = column headers).

```javascript
sessions_spawn({
  task: 'excel_read',
  params: {
    filepath: "C:/data/input.xlsx",
    sheet_name: 0,      // or "Sheet1"
    range: "A1:C10"     // optional; reads whole sheet if omitted
  },
  label: 'desktop-automation-ultra-local'
});
```

**Response**:
```json
{
  "status": "ok",
  "data": [
    {"Name": "Alice", "Age": 30},
    {"Name": "Bob", "Age": 25}
  ],
  "columns": ["Name", "Age"],
  "rows": 2
}
```

### excel_write
Write an array of objects (or array of arrays) to an Excel file.

```javascript
sessions_spawn({
  task: 'excel_write',
  params: {
    filepath: "C:/data/output.xlsx",
    data: [
      {"Product": "Widget", "Price": 9.99},
      {"Product": "Gadget", "Price": 19.99}
    ],
    sheet_name: "Results",
    start_cell: "A1"
  },
  label: 'desktop-automation-ultra-local'
});
```

**Response**:
```json
{"status":"ok","filepath":"C:/data/output.xlsx","rows":2,"columns":2}
```

### data_to_csv
Convert a list of dictionaries to CSV format. Returns CSV string or writes to a file.

```javascript
sessions_spawn({
  task: 'data_to_csv',
  params: {
    data: [{"a":1,"b":2},{"a":3,"b":4}],
    filepath: "C:/data/out.csv"  // optional; if omitted, CSV string is returned
  },
  label: 'desktop-automation-ultra-local'
});
```

**Response** (without filepath):
```json
{
  "status": "ok",
  "csv": "a,b\n1,2\n3,4\n",
  "rows": 2,
  "columns": 2
}
```

---

## Safety & Best Practices

âš ï¸ **This skill controls mouse and keyboard. Use with extreme caution.**

### Safe Mode (enabled by default)
- Blocks risky actions (`type`, `press_key`, `click`, `drag`) to prevent accidental damage.
- Disable with: `sessions_spawn({ task: 'set_safe_mode', params: {enabled: false} })`
- Also blocks dangerous patterns (e.g., `rm `, `del `, system paths).

### Dry-Run (Sandbox)
Add `"dry_run": true` to any action to simulate without side effects. Great for testing.

### Audit Logging
All actions are logged to daily files under:
- **Windows**: `C:\Users\<User>\.openclaw\skills\desktop-automation-logs\`
- **Linux/macOS**: `~/.openclaw/skills/desktop-automation-logs/`

Use logs to debug or audit activity.

### General
- Verify coordinates before clicking.
- Test macros in dry-run or slow speed first.
- `activate_window` requires exact or partial title match.
- No network access â€” completely local.
- May require admin rights for certain applications on Windows.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `pyautogui.FailSafeException` | Move mouse to corner (0,0) to disable failsafe, or set `pyautogui.FAILSAFE = False` |
| OCR not working | Ensure Tesseract is installed and in PATH. Check language pack. |
| `find_image` fails | Template must match screen exactly (scale, colors). Lower confidence if needed (0.7â€“0.95). |
| `activate_window` can't find window | Use `list_windows` to get exact titles. |
| Missing modules | Run `pip install -r requirements.txt` |
| Tkinter GUI not opening | Linux: `sudo apt-get install python3-tk`. Windows: usually already installed. |

---

## License

MIT Â© 2026 Jordane Guemara & contributors

See `LICENSE` file.

---

## Contributing

See `CONTRIBUTING.md` to contribute to this skill.

---

## Author

Created by **Jordane Guemara** â€” [@JordaneParis](https://github.com/JordaneParis)



