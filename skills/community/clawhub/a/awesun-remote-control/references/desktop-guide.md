# Desktop Control & Automation Guide

Detailed remote desktop GUI automation, normalized coordinate systems, and input simulation for `awesun-cli`.

---

## 1. Prerequisites & Coordinate System

All desktop automation commands require an active `type=desktop` session.

```bash
# Connect desktop session
awesun-cli session connect --type desktop --remote-id 1738789907
# Returns session_id: abc123xyz
```

### Normalized Coordinates (0.0 - 1.0)

All coordinates are **float values normalized from 0.0 to 1.0**:

- `(0.0, 0.0)` = Top-Left corner of the screen
- `(1.0, 1.0)` = Bottom-Right corner of the screen
- `(0.5, 0.5)` = Center of the screen

Use `scripts/coordinates.py` to convert pixel coordinates:

```bash
# Convert pixel coords (x=960, y=540 on 1920x1080 screen)
python3 scripts/coordinates.py norm 960 540 1920 1080
# Output: x=0.5000, y=0.5000
```

---

## 2. Screenshot Capture

Capture current desktop view to locate interactive elements:

```bash
awesun-cli session screenshot <session_id> --output /tmp/desktop.png
```

> [!TIP]
> **Screenshot Strategy**: Take one screenshot at the start of a task, identify all needed element coordinates simultaneously, and execute subsequent operations without re-capturing unless the screen layout significantly changes.

---

## 3. Mouse Operations

### Click & Double Click

```bash
# Single left click at center
awesun-cli desktop mouse click <session_id> --x 0.5 --y 0.5 --button left

# Right click
awesun-cli desktop mouse click <session_id> --x 0.5 --y 0.5 --button right

# Double click
awesun-cli desktop mouse click <session_id> --x 0.5 --y 0.5 --button left --clicks 2
```

### Mouse Move (Hover)

```bash
awesun-cli desktop mouse move <session_id> --x 0.25 --y 0.25
```

### Scroll Wheel

`--x` and `--y` specify the scroll trigger position:

```bash
# Scroll down 3 notches at cursor position
awesun-cli desktop mouse scroll <session_id> --x 0.5 --y 0.5 --direction down --count 3

# Scroll up
awesun-cli desktop mouse scroll <session_id> --x 0.5 --y 0.5 --direction up --count 2
```

### Drag & Drop

`--path` accepts comma-separated normalized coordinates `"x1,y1,x2,y2,..."`:

```bash
# Drag from (0.2, 0.3) to (0.6, 0.3) with left button
awesun-cli desktop mouse drag <session_id> --path "0.2,0.3,0.6,0.3" --button left

# Drag while holding modifier keys
awesun-cli desktop mouse drag <session_id> --path "0.2,0.3,0.6,0.3" --button left --hold-keys "ctrl"
```

---

## 4. Keyboard & Text Input

### Type Text

Simulates keystrokes directly into the active UI element:

```bash
awesun-cli desktop type <session_id> "Hello World"

# Type with custom millisecond keystroke delay
awesun-cli desktop type <session_id> "SecurePassword" --delay 50
```

### Paste Text

Directly sets clipboard / pastes text into remote focus:

```bash
awesun-cli desktop paste <session_id> "Long text or URL to paste"
```

### Key Combinations (Hotkeys)

```bash
# Copy / Paste hotkeys
awesun-cli desktop key combo <session_id> --keys ctrl,c
awesun-cli desktop key combo <session_id> --keys ctrl,v

# Windows task manager / security
awesun-cli desktop key combo <session_id> --keys ctrl,alt,del
```

### Key Press & Release

Controls explicit key down/up states (e.g. holding Enter, Escape):

```bash
# Press and release Enter key
awesun-cli desktop key press <session_id> --keys enter --press down
awesun-cli desktop key press <session_id> --keys enter --press up
```

---

## 5. UI Element Recognition Resources

- **`references/ui-locator.md`**: Step-by-step visual guidance for extracting normalized coordinates.
- **`references/ui-patterns.md`**: Common button, input box, and dialog recognition patterns.
