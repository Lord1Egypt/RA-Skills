---
name: desktop-control-linux
version: 0.1.0
description: Safe Linux desktop automation (mouse/keyboard/screenshot) with approval mode and X11/Wayland checks.
---

# Desktop Control (Linux)

Safe desktop automation for Linux using PyAutoGUI with explicit approvals and environment checks.

## Requirements

- Linux with GUI session (X11 recommended)
- Python packages:
  - `pyautogui`
  - `pillow`
  - `pygetwindow` (window ops; not supported on Linux)
  - `pyperclip` (clipboard ops)
  - `opencv-python` (optional, image match)

System packages (common):
- `python3-tk`, `scrot`, `xclip` or `xsel`
- `wmctrl` (window list/activate)
- `xdotool` (active window)

## Quick Start

```bash
python - <<'PY'
from skills.desktop_control_linux import DesktopControllerLinux

dc = DesktopControllerLinux(require_approval=True)
print(dc.get_screen_size())
PY
```

### Screenshot to file
```bash
python - <<'PY'
from skills.desktop_control_linux import DesktopControllerLinux

dc = DesktopControllerLinux(require_approval=False)
print(dc.screenshot_to('/tmp/screen.png'))
PY
```

### Record screen (ffmpeg)
```bash
python - <<'PY'
from skills.desktop_control_linux import DesktopControllerLinux

dc = DesktopControllerLinux(require_approval=False)
print(dc.record_screen('/tmp/record.mp4', seconds=30))
PY
```

### Launch Chrome + open URL (default wait 15s; use 15–30s for heavy apps)
```bash
python - <<'PY'
from skills.desktop_control_linux import DesktopControllerLinux

dc = DesktopControllerLinux(require_approval=False)
dc.open_chrome('http://localhost:8000', wait_seconds=15)
PY
```

### Preset examples
```bash
python - <<'PY'
from skills.desktop_control_linux import DesktopControllerLinux

dc = DesktopControllerLinux(require_approval=False)

def preset_open_site():
    dc.open_chrome('http://localhost:8000', wait_seconds=15)

def preset_login_site():
    dc.open_chrome('http://localhost:8000/login', wait_seconds=15)
    dc.login_form('user@example.com', 'password', wait_seconds=10)

dc.register_preset('open-site', preset_open_site)
dc.register_preset('login-site', preset_login_site)

# run presets
# dc.run_preset('open-site')
# dc.run_preset('login-site')
PY
```

### Workflow (DSL) example
```bash
python - <<'PY'
from skills.desktop_control_linux import DesktopControllerLinux

dc = DesktopControllerLinux(require_approval=False)
steps = [
  {"action": "open_chrome", "url": "http://localhost:8000/login", "wait": 15},
  {"action": "login_form", "email": "user@example.com", "password": "secret", "wait": 10},
  {"action": "open_url", "url": "http://localhost:8000/target", "wait": 15},
  {"action": "screenshot", "path": "/tmp/target.png"}
]

dc.run_steps(steps)
PY
```

### OCR & State Detection example
```bash
python - <<'PY'
from skills.desktop_control_linux import DesktopControllerLinux

dc = DesktopControllerLinux(require_approval=False)

# Read text from screen
text = dc.read_text_on_screen()
print(text)

# Wait for text to appear (requires pytesseract)
if dc.wait_for_text("Success", timeout=30):
    print("Text detected!")
PY
```

### Multi-monitor example
```bash
python - <<'PY'
from skills.desktop_control_linux import DesktopControllerLinux

dc = DesktopControllerLinux(require_approval=False)

# Get all monitors
monitors = dc.get_monitors()
print(monitors)  # [{'name': 'HDMI-1', 'x': 0, 'y': 0, 'width': 1920, 'height': 1080}, ...]

# Click on second monitor (relative 0.5, 0.5 = center)
dc.click_monitor(1, 0.5, 0.5)
PY
```

### Multi-browser example
```bash
python - <<'PY'
from skills.desktop_control_linux import DesktopControllerLinux

dc = DesktopControllerLinux(require_approval=False)

# Open different browsers
dc.open_firefox('https://google.com', wait_seconds=15)
dc.open_edge('https://github.com', wait_seconds=15)
PY
```

### Window Manager example
```bash
python - <<'PY'
from skills.desktop_control_linux import DesktopControllerLinux

dc = DesktopControllerLinux(require_approval=False)

# Resize window to 800x600
dc.resize_window('Chrome', 800, 600)

# Minimize window
dc.minimize_window('Telegram')

# Maximize window
dc.maximize_window('VSCode')
PY
```

### Flow Recorder example
```bash
python - <<'PY'
from skills.desktop_control_linux import DesktopControllerLinux

dc = DesktopControllerLinux(require_approval=False)

# Start recording
dc.start_recording()

# Do some actions (manual for now, or wrap them)
dc.click(x=100, y=200)
dc.type_text('hello')
dc.press('enter')

# Stop and replay
actions = dc.stop_recording()
print(f"Recorded {len(actions)} actions")

# Replay later
dc.replay_actions(actions, delay_multiplier=1.0)
PY
```

### AI Vision & Smart Wait example
```bash
python - <<'PY'
from skills.desktop_control_linux import DesktopControllerLinux

dc = DesktopControllerLinux(require_approval=False)

# Find element by color (RGB)
pos = dc.find_element_by_color((255, 0, 0), tolerance=20)  # red
if pos:
    dc.click(x=pos[0], y=pos[1])

# Smart wait - poll until condition is true
dc.smart_wait(lambda: dc.active_window_contains('Done'), timeout=30)
PY
```

### Drag & Drop example
```bash
python - <<'PY'
from skills.desktop_control_linux import DesktopControllerLinux

dc = DesktopControllerLinux(require_approval=False)

# Drag from point A to B
dc.drag_drop(100, 200, 500, 600)

# Drag file to app
dc.drag_file_to_app('/path/to/file.txt', 400, 300)
PY
```

### Robust retry example
```bash
python - <<'PY'
from skills.desktop_control_linux import DesktopControllerLinux

dc = DesktopControllerLinux(require_approval=False)

# Click with automatic retry
dc.robust_click(100, 200)

# Type with automatic retry
dc.robust_type("Hello world")
PY
```

## API

Same interface as `DesktopController`:
- mouse: `move_mouse`, `click`, `drag`, `scroll`, `get_mouse_position`
- keyboard: `type_text`, `press`, `hotkey`, `wait`, `launch_app`, `open_url`, `open_chrome`, `wait_retry_window`, `wait_retry_new_window`, `smart_retry`
- screen/ui: `click_image`, `click_image_or`, `login_form`
- state: `ensure_window`, `active_window_contains`, `wait_for_text`, `detect_state`
- recovery: `recover_reload`, `recover_back`, `retry_with_recovery`
- workflows: `run_steps`
- presets: `register_preset`, `run_preset`
- ocr: `read_text_on_screen`
- multi-monitor: `get_monitors`, `click_monitor`
- robust: `robust_click`, `robust_type`
- smart-wait: `smart_wait`, `wait_for_window_stable`
- drag-drop: `drag_drop`, `drag_file_to_app`
- window-manager: `resize_window`, `minimize_window`, `maximize_window`
- multi-browser: `open_firefox`, `open_edge`
- keyboard: `detect_keyboard_layout`
- ai-vision: `find_element_by_color`, `find_button_vision`
- recorder: `start_recording`, `record_action`, `stop_recording`, `replay_actions`

`launch_app(app_name, wait_seconds=15, window_title=None, auto_detect_window=True)`
- If `window_title` is provided: waits 15s, retries once, then errors if not found.
- If `auto_detect_window=True`: detects a new window title automatically, waits 15s, retries once.

`smart_retry(action_fn, check_fn, wait_seconds=15, retries=2)`
- Runs action → wait → check → retry (with wait) to avoid rapid loops.
- screen: `screenshot`, `screenshot_to`, `record_screen`, `get_pixel_color`, `find_on_screen`
- windows: `get_all_windows`, `activate_window`, `focus_window_or_click`, `get_active_window`
- clipboard: `copy_to_clipboard`, `get_from_clipboard`

## Safety

- **Approval mode** enabled by default
- **Failsafe**: move mouse to any corner to abort
- **Environment guard**: warns on Wayland or headless sessions
- **Auto-detect DISPLAY**: tries `/tmp/.X11-unix` when DISPLAY is missing
