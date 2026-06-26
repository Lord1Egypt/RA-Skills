---
name: e2b-desktop
description: Control E2B Desktop sandboxes (virtual Linux desktops) for computer-use agents. Use when you need to create/manage sandboxed desktop environments, take screenshots, perform mouse/keyboard actions, run commands, stream VNC output, or build computer-use agent loops with E2B Desktop SDK.
---

# E2B Desktop Skill

Control a headless Linux desktop (Ubuntu + XFCE) via the `e2b-desktop` Python SDK.
All scripts live in `scripts/` and wrap the SDK in bash for easy agent use.

## Prerequisites

```bash
pip install e2b-desktop
export E2B_API_KEY=e2b_***
```

## State Management

- `start_sandbox.sh` saves the sandbox ID to `~/.e2b_state`
- All other scripts auto-load it from there
- Override anytime with `export E2B_SANDBOX_ID=<id>`
- Sandboxes survive script exit — reconnect with `Sandbox.connect(sandbox_id)`

## Scripts

| Script | Usage | Description |
|---|---|---|
| `start_sandbox.sh` | `[--resolution 1280x800] [--timeout 300] [--stream]` | Create sandbox; optionally start VNC stream |
| `kill_sandbox.sh` | `[SANDBOX_ID]` | Kill sandbox and remove state |
| `screenshot.sh` | `[OUTPUT_FILE]` | Take screenshot → PNG (default: `/tmp/e2b_screenshot.png`) |
| `click.sh` | `X Y` | Left click at coordinates |
| `right_click.sh` | `X Y` | Right click |
| `double_click.sh` | `X Y` | Double click |
| `middle_click.sh` | `X Y` | Middle click |
| `move_mouse.sh` | `X Y` | Move cursor (no click) |
| `drag.sh` | `X1 Y1 X2 Y2` | Click-drag between two points |
| `scroll.sh` | `AMOUNT` | Scroll (positive=up, negative=down) |
| `type_text.sh` | `"text"` | Type text at current cursor |
| `press_key.sh` | `KEY [KEY2...]` | Press key or combo (e.g. `ctrl c`) |
| `run_command.sh` | `"cmd"` | Run shell command inside sandbox |
| `open_url.sh` | `URL_OR_PATH` | Open URL or file in default app |
| `launch_app.sh` | `APP_NAME` | Launch app (e.g. `firefox`, `vscode`) |
| `stream_start.sh` | `[--auth]` | Start VNC stream; `--auth` for password-protected |
| `stream_stop.sh` | _(none)_ | Stop VNC stream |
| `get_cursor.sh` | _(none)_ | Print `CURSOR_X` and `CURSOR_Y` |
| `get_screen_size.sh` | _(none)_ | Print `SCREEN_WIDTH` and `SCREEN_HEIGHT` |
| `list_windows.sh` | `[APP_NAME]` | List app windows or show active window |
| `wait.sh` | `MILLISECONDS` | Wait N ms (sandbox-side) |

## Computer-Use Agent Loop Pattern

```bash
SCRIPTS="skills/e2b-desktop/scripts"

# 1. Start sandbox
source <($SCRIPTS/start_sandbox.sh --resolution 1280x800 --stream)
echo "Sandbox: $SANDBOX_ID"
echo "View at: $STREAM_URL"

# 2. Agent loop
while true; do
  # Capture screen
  $SCRIPTS/screenshot.sh /tmp/screen.png

  # Send to LLM, parse action... (your code)
  ACTION=$(llm_decide /tmp/screen.png)

  case "$ACTION" in
    click:*)   IFS=: read -r _ x y <<< "$ACTION"; $SCRIPTS/click.sh $x $y ;;
    type:*)    $SCRIPTS/type_text.sh "${ACTION#type:}" ;;
    key:*)     $SCRIPTS/press_key.sh ${ACTION#key:} ;;
    done)      break ;;
  esac
done

# 3. Clean up
$SCRIPTS/kill_sandbox.sh
```

## Key Notes

- `scroll.sh AMOUNT`: positive = scroll up, negative = scroll down (matches `desktop.scroll(amount)` API)
- `press_key.sh ctrl c`: multiple args become a key combo via `desktop.press(["ctrl", "c"])`
- `run_command.sh` exits with the sandbox command's exit code
- All mouse coordinate scripts accept integer pixel coordinates matching sandbox resolution
- VNC stream: only one active stream at a time; stop before switching windows
