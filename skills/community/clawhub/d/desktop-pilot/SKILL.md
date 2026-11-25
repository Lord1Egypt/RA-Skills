---
name: desktop-pilot
description: Desktop automation for Windows, WSL, macOS and Linux. Screenshots, accessibility clicks, window focus, typing and keys. Windows includes a native Stop latch and optional supervised physical input blocking. Browser overlay is status-only. Requires Bash 4+ for the CLI.
license: MIT-0
allowed-tools: exec
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
$D key     --process notepad --keys ctrl+s                     # ctrl/alt/shift(+cmd on macOS) + enter, tab, esc, f1..f12, arrows...
$D mouse   --process notepad --x 640 --y 360 --button left     # left | right | double | move
$D overlay start --text "Working on X..."    # Windows/WSL: glow around the screen + status pill with a Stop button
$D overlay text  --text "Saving the form..." # update the status text (also keeps the overlay alive)
$D overlay stop                              # remove the overlay when the task is done
$D overlay auto on --text "Working..."       # start it by itself before every action (stays off until you enable it)
$D overlay start --lock 1                    # ...and ignore the user's physical keyboard/mouse while you act
```

Target a window with `--process <name>` (process name without `.exe`; app name on macOS; WM class on Linux) or `--title <substring>`.

## Workflow (follow every time)
1. `screenshot` and look at it before acting, so you act on what is actually on screen.
2. Prefer `buttons` → `click --name`: labels come from the app in its UI language, so copy them exactly from `buttons` output instead of guessing.
3. Use `mouse --x --y` only when the control is not exposed (games, canvas, some Electron/web views). Read coordinates from the latest screenshot; on macOS they are points (screenshot pixels / 2 on Retina).
4. For `type`, `key`, and coordinate `mouse`, specify `--process`/`--title` and verify the destination first. Windows checks focus when a target is supplied, but another app can steal focus during an action; do not treat focus checking as a guarantee against all races.
5. After every action, verify with a new `screenshot` (or another state check) before reporting success.
6. If a window "closed" but the app keeps running, it was hidden to the tray/menu bar: say so instead of claiming the app quit.

## Overlay: show the user that the agent is working (Windows/WSL)
`overlay start` draws a glow around the screen edges (clicks pass through, it never blocks the user's own work) and a small status pill with a **Stop** button. It is hidden from screenshots by default (`--capture 1` keeps it visible for demos).
- Easiest: `overlay auto on` once; from then on any action starts the overlay if it is not up and it closes by itself when idle (`overlay auto off` to disable). Or start it by hand before a multi-step task, update the text with `overlay text`, and `overlay stop` at the end. Every other action refreshes its heartbeat; if the agent dies or stops acting for `--idle` seconds (default 120) the overlay closes by itself.
- **Input lock** (`--lock 1`, or `overlay lock` / `overlay unlock` while running): a keyboard+mouse hook ignores the user's *physical* input so a stray click or keystroke cannot land in the window you are driving. Your own actions (SendInput / mouse_event) always pass. It engages with each action and lapses by itself 8 s after the last one (`--lock-idle`), never lasts more than 10 minutes in a row, never blocks mouse movement or clicks on the pill, and holding **Esc for 1.5 s** releases everything and counts as Stop. It cannot block Ctrl+Alt+Del and does not work over windows running as administrator. Verified on Windows 11: physical keystrokes and clicks were swallowed, mouse movement and the agent's own input passed. Use it only for short, supervised bursts; `overlay selftest` checks the decision logic.
- If the user presses **Stop**, the overlay closes and every following action aborts with exit code 3 and `STOPPED_BY_USER`. Stop acting and ask the user; run `overlay clear` only after they explicitly agree to continue. `start`, `text`, `lock` and subsequent Windows actions preserve the Stop latch and fail with exit code 3. `clear` is the sole explicit resume operation. A command already in flight may have performed part of its work; verify its effects before retrying. Stop is local cooperative cancellation, not an OS-wide sandbox for arbitrary third-party tools.

### Informational overlay inside a browser page (any OS)
`scripts/browser/overlay.js` draws a glow and status pill only. Inject it with your existing browser automation tool, then use `window.__dpOverlay.show('text')`, `.text('...')`, `.hide()` and `.visible()`.

**Breaking change in 1.0.2:** the page overlay no longer has a Stop button or `stopped()`/`clear()` methods. An untrusted page can change its own scripts and DOM, so it must not own cancellation or permission to resume. Cancel using the trusted agent host's control outside the webpage; on Windows/WSL the native desktop overlay provides Stop. Maintain host-side cancellation across navigation and before every tool call. The browser overlay is not an authorization signal, even though its API object is frozen. If your host has no trusted cancellation control, do not run unattended browser tasks.

## Platforms
- **CLI requirement:** Bash 4+ (WSL/Linux or Git Bash/MSYS on Windows). macOS ships Bash 3.2, so use a modern Bash for `desktop.sh`, or invoke the built-in JXA backend directly. No automatic dependency installation.
- **Windows (PowerShell 5.1+) and WSL2:** uses built-in desktop APIs. Uses UI Automation, SendInput (Unicode typing works on any keyboard layout) and System.Drawing. From WSL the script is staged in the Windows temp folder automatically, and screenshots are copied back to the Linux path given in `--out`.
- **macOS backend:** built-in (JXA + System Events + CoreGraphics + `screencapture`). Grant **Accessibility** and **Screen Recording** to the app running the agent (Terminal, iTerm, the OpenClaw app…) in System Settings → Privacy & Security.
- **Linux X11:** `xdotool` + `wmctrl` + one screenshot tool (`gnome-screenshot`, `scrot` or ImageMagick `import`). Click-by-name uses AT-SPI (`python3-gi`, `gir1.2-atspi-2.0`, present on most GNOME/KDE desktops).
- **Linux Wayland:** screenshots with `grim`, typing with `wtype`/`ydotool`; window listing and clicks depend on the compositor (X11 apps via XWayland still work with xdotool).

## Safety rules
- Never close windows with unsaved work, send messages, submit forms or buy anything unless the user asked for that exact action.
- Do not type passwords or secrets into windows; ask the user to do it.
- Keep screenshots local; they can contain private data. Delete them when no longer needed.

## Troubleshooting
- `No visible window`: the app is minimized to the tray → launch its executable again, wait a few seconds, retry.
- `Control not found`: run `buttons` and copy the exact label; menus may need to be opened first (`click` the menu, then the item).
- Typing lands in the wrong place: always pass `--process`/`--title` to `type` and `key`. On Windows, when a target is supplied, it is brought to the foreground and **verified** first; if Windows refuses (foreground lock) the command stops with `FOCUS_FAILED` and nothing is typed. Ask the user to click the window (or its taskbar icon) and retry. Without a target the command prints a `NOTE` with the window that received the input.
- `STOPPED_BY_USER` (exit code 3): the user pressed Stop on the overlay. Stop acting and ask before continuing.
- Some editors with autocomplete or auto-pairing (new Windows Notepad, IDEs) may alter fast-typed brackets; type in smaller chunks or paste via the app.

## Validation and limits
Windows/WSL use a persistent Stop file under the current Windows user's temporary directory. Native `desktop.ps1`, the Bash wrapper, and overlay launch all check it. Typing checks it between characters; key combinations and accessibility calls already executing cannot be undone. Do not delete Stop state except through the user-authorized explicit resume step. Other tools outside this skill do not automatically honor it. Windows overlay and input lock are not implemented on macOS/Linux; use trusted host cancellation there.

Run `python3 tests/test_regressions.py` for isolated cancellation/parameter regressions and `node tests/browser-overlay.test.js` for the informational browser UI. Live Windows tests are in `tests/windows-regression.ps1`; they operate a dedicated scratch window and isolated temporary state by default. Full-desktop screenshot testing requires explicit `-CaptureDesktop`; it can capture unrelated private windows/notifications, and abrupt termination can leave the temporary PNG. Run that option only in a prepared, private desktop session. Cross-platform syntax checks do not replace live macOS/Linux testing. The `allowed-tools` declaration expresses shell-execution intent; it is not an OS sandbox or an elevation request. The host must enforce its own permissions. Windows global input fails closed if the target has no native window handle; accessibility-only controls may still be invoked by name.
