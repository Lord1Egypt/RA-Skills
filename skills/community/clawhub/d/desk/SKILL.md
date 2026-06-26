---
description: Optimized desktop automation with mouse, keyboard, and screen control
---

# Desktop Control Skill

**High-performance desktop automation for OpenClaw.** Optimized for minimal latency, efficient resource usage, and robust error handling.

## 🚀 Quick Start

```python
from desktop_control import DesktopController

# Context manager ensures cleanup
with DesktopController() as dc:
    dc.move_mouse(500, 300)
    dc.click()
    dc.type_text("Hello World!")
```

## 📦 Installation

```bash
pip install -r requirements.txt
```

## ✨ Features

### Mouse Control
- **Instant movements** (0ms overhead)
- **Smooth animations** with easing curves
- **Relative positioning** from current location
- **Click variations**: left, right, middle, double
- **Drag & drop** with configurable duration
- **Scroll**: vertical and horizontal

### Keyboard Control
- **Type text** with WPM or interval control
- **Hotkeys** (Ctrl+C, Alt+Tab, etc.)
- **Key combinations** via context manager
- **Individual key** press/hold/release

### Screen Operations
- **Fast screenshots** to file or PIL Image
- **Pixel color** reading
- **Image finding** on screen (OpenCV)
- **Region capture** for performance
- **Wait for image** with timeout

### Window Management
- **List all windows**
- **Activate by title** (partial match)
- **Get active window**

### Safety Features
- **Corner failsafe** - move mouse to any corner to abort
- **Bounds checking** - prevents off-screen coordinates
- **Retry logic** - auto-retry flaky operations
- **Approval mode** - ask before each action

---

## 🔧 API Reference

### DesktopController

```python
DesktopController(
    failsafe: bool = True,          # Abort on corner detection
    require_approval: bool = False,  # Ask before actions
    log_level: int = logging.INFO   # Verbosity
)
```

**Context Manager Support:**
```python
with DesktopController() as dc:
    # Automatic cleanup on exit
    dc.type_text("Hello")
```

---

### Mouse Operations

#### `move_mouse(x, y, duration=0, smooth=True)`
Move to absolute coordinates instantly or with animation.

```python
dc.move_mouse(1000, 500)                    # Instant
dc.move_mouse(1000, 500, duration=0.5)      # Smooth 0.5s
dc.move_mouse(1000, 500, smooth=False)      # Linear movement
```

#### `move_relative(dx, dy, duration=0)`
Move from current position.

```python
dc.move_relative(100, -50)   # Right 100, Up 50
```

#### `click(x=None, y=None, button='left', clicks=1, interval=0.05)`
Click with retry logic.

```python
dc.click()                          # Current position
dc.click(500, 300)                  # Specific position
dc.click(button='right')            # Right click
dc.double_click(500, 300)           # Double click (convenience)
```

#### `drag(x1, y1, x2, y2, duration=0.3, button='left')`
Drag from point to point.

```python
# Drag file from A to B
dc.drag(200, 200, 800, 500, duration=0.5)
```

#### `scroll(amount, x=None, y=None, horizontal=False)`
Scroll wheel.

```python
dc.scroll(-5)              # Down 5 clicks
dc.scroll(10, 500, 300)    # Scroll at position
dc.scroll(3, horizontal=True)  # Horizontal
```

---

### Keyboard Operations

#### `type_text(text, interval=None, wpm=None)`
Type text with speed control.

```python
dc.type_text("Instant!", interval=0)      # No delay
dc.type_text("Human-like", wpm=80)        # 80 words per minute
dc.type_text("Custom", interval=0.1)     # 100ms between keys
```

#### `hotkey(*keys, interval=0.01)`
Execute keyboard shortcuts.

```python
dc.hotkey('ctrl', 'c')      # Copy
dc.hotkey('alt', 'tab')     # Switch window
dc.hotkey('ctrl', 'shift', 'esc')  # Task manager
```

#### `press(key, presses=1, interval=0.05)`
Press individual keys.

```python
dc.press('enter')
dc.press('space', presses=3)
dc.press('f5')              # Refresh
```

#### Key Hold Context Manager
Hold keys during a block:

```python
with dc.hold_keys('ctrl', 'shift'):
    dc.press('end')         # Ctrl+Shift+End
    dc.click(500, 300)      # Ctrl+Shift+Click
```

---

### Screen Operations

#### `screenshot(region=None, filename=None)`
Capture screen with retry logic.

```python
# Full screen to PIL Image
img = dc.screenshot()

# Save to file (returns None)
dc.screenshot(filename="screen.png")

# Region only (left, top, width, height)
dc.screenshot(region=(100, 100, 800, 600), filename="region.png")
```

#### `screenshot_to_file(filename, region=None)`
Convenience method that returns filename.

```python
path = dc.screenshot_to_file(f"capture_{time.time()}.png")
```

#### `get_pixel(x, y)`
Get RGB color at coordinates.

```python
r, g, b = dc.get_pixel(500, 300)
```

#### `find_on_screen(image_path, confidence=0.9, grayscale=True)`
Find image on screen.

```python
# Returns (x, y, width, height) or None
location = dc.find_on_screen("button.png", confidence=0.9)
if location:
    x, y, w, h = location
    dc.click(x + w//2, y + h//2)  # Click center
```

#### `find_all_on_screen(image_path, confidence=0.9)`
Find all occurrences.

```python
matches = dc.find_all_on_screen("icon.png")
for x, y, w, h in matches:
    print(f"Found at ({x}, {y})")
```

#### `wait_for_image(image_path, timeout=10.0, interval=0.5)`
Wait for image to appear.

```python
location = dc.wait_for_image("loading_complete.png", timeout=30)
if location:
    print("Ready!")
```

---

### Window Operations

#### `get_all_windows()`
List all window titles.

```python
windows = dc.get_all_windows()
for title in windows:
    if "Chrome" in title:
        print(f"Found: {title}")
```

#### `activate_window(title, partial=True)`
Bring window to front.

```python
dc.activate_window("Chrome")        # Partial match
dc.activate_window("Untitled - Notepad", partial=False)  # Exact
```

#### `get_active_window()`
Get current window title.

```python
current = dc.get_active_window()
```

#### `find_window(title_substring)`
Find window by partial title.

```python
title = dc.find_window("Document")
if title:
    dc.activate_window(title)
```

---

### Clipboard

```python
# Copy to clipboard
dc.copy_to_clipboard("Hello")

# Get from clipboard
text = dc.get_clipboard()
```

---

### Utility

```python
# Sleep (same as time.sleep)
dc.sleep(0.5)

# Wait for key press
dc.wait_for_key('space', timeout=10.0)

# Show alert
dc.alert("Operation complete!")

# Confirm dialog
if dc.confirm("Proceed?"):
    print("User said yes")
```

---

## 🎯 Performance Tips

1. **Use context managers** for automatic cleanup:
   ```python
   with DesktopController() as dc:
       # operations
   ```

2. **Minimize screenshots** in loops:
   ```python
   # Bad - screenshot every iteration
   for _ in range(100):
       dc.screenshot()

   # Better - cache or use find_on_screen with interval
   ```

3. **Use instant movements** when smoothness isn't needed:
   ```python
   dc.move_mouse(x, y, duration=0)  # vs 0.5s
   ```

4. **Batch keyboard operations** with hotkeys:
   ```python
   # One hotkey call
   dc.hotkey('ctrl', 'a')

   # Instead of multiple key presses
   ```

5. **Use grayscale for image matching** (2x faster):
   ```python
   dc.find_on_screen("image.png", grayscale=True)
   ```

---

## 🛡️ Safety

### Failsafe Mode

```python
# Move mouse to any corner to abort all automation
dc = DesktopController(failsafe=True)
```

### Approval Mode

```python
# Ask before each action
dc = DesktopController(require_approval=True)
dc.click(500, 300)  # Prompts: "Allow left click at (500, 300)? [y/n]"
```

---

## 🔌 AI Agent (Optional)

For cognitive automation with task planning:

```python
from ai_agent import create_agent

with create_agent() as agent:
    result = agent.execute_task("Type Hello World in Notepad")
    print(f"Status: {result.status}")
```

See `ai_agent.py` for full capabilities.

---

## 📋 Quick Reference

```python
from desktop_control import (
    DesktopController, get_controller,
    move, click, typewrite, hotkey, screenshot
)

# Initialize
dc = DesktopController()

# Mouse
dc.move_mouse(x, y)
dc.click(x, y)
dc.drag(x1, y1, x2, y2)
dc.scroll(amount)
pos = dc.get_mouse_position()

# Keyboard
dc.type_text(text, wpm=80)
dc.hotkey('ctrl', 'c')
dc.press('enter')

with dc.hold_keys('ctrl'):
    dc.click(x, y)

# Screen
img = dc.screenshot()
dc.screenshot_to_file("out.png")
color = dc.get_pixel(x, y)
loc = dc.find_on_screen("image.png")

# Window
windows = dc.get_all_windows()
dc.activate_window("Chrome")
```

---

**Built for OpenClaw** - Optimized for speed and reliability 🦞
