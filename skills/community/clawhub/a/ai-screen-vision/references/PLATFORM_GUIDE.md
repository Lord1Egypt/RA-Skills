# Platform Setup Guide

## Platform Detection

Run `scripts/platform/detect_os.sh` to identify the current OS and check dependencies.

## Linux

### Headless Server (no desktop)

```bash
bash scripts/setup/setup-linux.sh --headless
```

Installs: XFCE4, xdotool, scrot, noVNC, Chromium
Memory: ~300MB additional
VNC access: `http://<server-ip>:6080/vnc.html`

### Desktop Environment (Ubuntu Desktop etc.)

```bash
bash scripts/setup/setup-linux.sh --desktop
```

Installs: xdotool, scrot
Uses existing display.

### Tools

| Function | Tool | Command |
|----------|------|---------|
| Screenshot | scrot | `DISPLAY=:1 scrot -z -overwrite /tmp/sv_screenshot.png` |
| Click | xdotool | `DISPLAY=:1 xdotool mousemove X Y click 1` |
| Type text | xdotool | `DISPLAY=:1 xdotool type --delay 50 "text"` |
| Key press | xdotool | `DISPLAY=:1 xdotool key Return` |
| Scroll | xdotool | `DISPLAY=:1 xdotool click 4` (up) / `click 5` (down) |
| Drag | xdotool | `DISPLAY=:1 xdotool mousemove X1 Y1 mousedown 1 mousemove X2 Y2 mouseup 1` |
| Double click | xdotool | `DISPLAY=:1 xdotool mousemove X Y click --repeat 2 1` |
| Right click | xdotool | `DISPLAY=:1 xdotool mousemove X Y click 3` |

## macOS

### Setup

```bash
bash scripts/setup/setup-mac.sh
```

Requires: Accessibility + Screen Recording permissions granted to Terminal/OpenClaw.

### Tools

| Function | Tool | Command |
|----------|------|---------|
| Screenshot | screencapture | `screencapture -x /tmp/sv_screenshot.png` |
| Click | cliclick | `cliclick c:X,Y` |
| Type text | cliclick | `cliclick t:text` |
| Key press | cliclick | `cliclick kp:return` |
| Scroll | cliclick | `cliclick "scroll:0,-300"` |
| Drag | cliclick | `cliclick "dd:X1,Y1 dm:X2,Y2 du:X2,Y2"` |
| Double click | cliclick | `cliclick "dc:X,Y"` |
| Right click | cliclick | `cliclick "rc:X,Y"` |

## Windows

### Setup

```
python3 scripts/setup/setup-win.py
```

### Tools (Python/pyautogui)

```python
import pyautogui
pyautogui.screenshot('/tmp/sv_screenshot.png')
pyautogui.click(x, y)
pyautogui.typewrite('text', interval=0.05)
pyautogui.press('enter')
pyautogui.scroll(-300)
pyautogui.moveTo(x1, y1)
pyautogui.dragTo(x2, y2, duration=0.5)
pyautogui.doubleClick(x, y)
pyautogui.rightClick(x, y)
```
