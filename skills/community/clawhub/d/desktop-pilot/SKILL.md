---
name: desktop-pilot
description: Computer use for Windows, macOS, Linux and WSL. Screenshot the screen, list windows, click buttons by name, close/focus apps, type text, press keys, click by coordinates, and show an "agent is working" overlay. Nothing to install on Windows/macOS; Linux needs xdotool and wmctrl.
---

# Desktop Pilot: computer use for any desktop

Control the real desktop of the machine running the agent: take screenshots, list open windows, read the buttons of a window, **click controls by their visible name** (accessibility APIs, robust to window moves and DPI), close or focus apps, type any Unicode text, press key combos, and click by coordinates as a fallback.

One CLI, same flags everywhere:

```bash
D=<skill-dir>/scripts/desktop.sh
$D os                                        # wsl | windows | macos | linux
$D screenshot --out /tmp/screen.png          # full desktop PNG
$D windows                                   # pid <tab> process <tab> title
$D buttons --process notepad                 # clickable controls of that app's window
$D click   --process notepad --name "Save"   # press a control by its exact label
$D close   --title "Untitled"                # same as the window's X
$D focus   --process chrome
$D type    --process notepad --text "Hola ñ €"
$D key     --keys ctrl+s                     # ctrl/alt/shift(+cmd on macOS) + enter, tab, esc, f1..f12, arrows...
$D mouse   --x 640 --y 360 --button left     # left | right | double | move
$D overlay start --text "Working on X..."    # Windows/WSL: glow around the screen + status pill with a Stop button
$D overlay text  --text "Saving the form..." # update the status text (also keeps the overlay alive)
$D overlay stop                              # remove the overlay when the task is done
$D overlay start --lock 1                    # ...and ignore the user's physical keyboard/mouse while you act
```

Target a window with `--process <name>` (process name without `.exe`; app name on macOS; WM class on Linux) or `--title <substring>`.

## Workflow (follow every time)
1. `screenshot` and look at it before acting, so you act on what is actually on screen.
2. Prefer `buttons` → `click --name`: labels come from the app in its UI language, so copy them exactly from `buttons` output instead of guessing.
3. Use `mouse --x --y` only when the control is not exposed (games, canvas, some Electron/web views). Read coordinates from the latest screenshot; on macOS they are points (screenshot pixels / 2 on Retina).
4. After every action, verify with a new `screenshot` (or another state check) before reporting success.
5. If a window "closed" but the app keeps running, it was hidden to the tray/menu bar: say so instead of claiming the app quit.

## Overlay: show the user that the agent is working (Windows/WSL)
`overlay start` draws a glow around the screen edges (clicks pass through, it never blocks the user's own work) and a small status pill with a **Stop** button. It is hidden from screenshots by default (`--capture 1` keeps it visible for demos).
- Start it before a multi-step task, update the text with `overlay text`, and `overlay stop` at the end. Every other action refreshes its heartbeat; if the agent dies or stops acting for `--idle` seconds (default 120) the overlay closes by itself.
- **Input lock** (`--lock 1`, or `overlay lock` / `overlay unlock` while running): a keyboard+mouse hook ignores the user's *physical* input so a stray click or keystroke cannot land in the window you are driving. Your own actions (SendInput / mouse_event) always pass. It engages with each action and lapses by itself 8 s after the last one (`--lock-idle`), never lasts more than 10 minutes in a row, never blocks mouse movement or clicks on the pill, and holding **Esc for 1.5 s** releases everything and counts as Stop. It cannot block Ctrl+Alt+Del and does not work over windows running as administrator. Verified on Windows 11: physical keystrokes and clicks were swallowed, mouse movement and the agent's own input passed. Use it only for short, supervised bursts; `overlay selftest` checks the decision logic.
- If the user presses **Stop**, the overlay closes and every following action aborts with exit code 3 and `STOPPED_BY_USER`. Stop acting and ask the user; run `overlay clear` only after they agree to continue.

### Same overlay inside a browser page (any OS)
`scripts/browser/overlay.js` draws the same glow + status pill with a Stop button inside the page, for browser automation (Playwright, CDP, Puppeteer, OpenClaw browser). Inject it once per page (`page.addInitScript({ path })` survives navigations), then call `window.__dpOverlay.show('text')`, `.text('...')`, `.stopped()` (true after the user pressed Stop: abort the task) and `.hide()`. The glow ignores pointer events and only the pill captures clicks, so automated clicks keep working; there is no input lock in the browser because it would break the automation's own clicks.

## Platforms
- **Windows (PowerShell 5.1+) and WSL2:** zero installs. Uses UI Automation, SendInput (Unicode typing works on any keyboard layout) and System.Drawing. From WSL the script is staged in the Windows temp folder automatically, and screenshots are copied back to the Linux path given in `--out`.
- **macOS:** zero installs (JXA + System Events + CoreGraphics + `screencapture`). Grant **Accessibility** and **Screen Recording** to the app running the agent (Terminal, iTerm, the OpenClaw app…) in System Settings → Privacy & Security.
- **Linux X11:** `xdotool` + `wmctrl` + one screenshot tool (`gnome-screenshot`, `scrot` or ImageMagick `import`). Click-by-name uses AT-SPI (`python3-gi`, `gir1.2-atspi-2.0`, present on most GNOME/KDE desktops).
- **Linux Wayland:** screenshots with `grim`, typing with `wtype`/`ydotool`; window listing and clicks depend on the compositor (X11 apps via XWayland still work with xdotool).

## Safety rules
- Never close windows with unsaved work, send messages, submit forms or buy anything unless the user asked for that exact action.
- Do not type passwords or secrets into windows; ask the user to do it.
- Keep screenshots local; they can contain private data. Delete them when no longer needed.

## Troubleshooting
- `No visible window`: the app is minimized to the tray → launch its executable again, wait a few seconds, retry.
- `Control not found`: run `buttons` and copy the exact label; menus may need to be opened first (`click` the menu, then the item).
- Typing lands in the wrong place: always pass `--process`/`--title` to `type` and `key`. On Windows the target is brought to the foreground and **verified** first; if Windows refuses (foreground lock) the command stops with `FOCUS_FAILED` and nothing is typed. Ask the user to click the window (or its taskbar icon) and retry. Without a target the command prints a `NOTE` with the window that received the input.
- `STOPPED_BY_USER` (exit code 3): the user pressed Stop on the overlay. Stop acting and ask before continuing.
- Some editors with autocomplete or auto-pairing (new Windows Notepad, IDEs) may alter fast-typed brackets; type in smaller chunks or paste via the app.
