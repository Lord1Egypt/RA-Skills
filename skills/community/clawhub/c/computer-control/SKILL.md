---
name: computer-control
description: >
  Control the computer like a human: take screenshots, move/click the mouse,
  type text, press hotkeys, scroll, launch apps, and run AppleScript — via the
  dependency-free `tarsx` CLI (zero config, no API keys). Click windows by app
  name (`clickwin`), no pixel guessing. Cross-platform core with auto-detected
  backends: macOS first (cliclick/osascript/screencapture), Linux (xdotool),
  Windows (PowerShell). Non-ASCII text (Cyrillic, emoji) works out of the box
  via clipboard paste. Use when the user asks to open/close an app, click or
  type somewhere, take a screenshot, automate a GUI application, fill a desktop
  form, check what is on screen, or any GUI automation that shell/browser tools
  cannot reach. Ukrainian triggers: "відкрий/закрий програму", "натисни",
  "набери", "зроби скріншот", "керуй комп'ютером". Inspired by Agent TARS
  (GUI-first computer use), implemented natively.
metadata:
  version: "1.0.3"
  license: "Apache-2.0"
  source: "tars-universum (Agent TARS-inspired native stack)"
---

# Computer Control (tarsx)

Control the computer through the `tarsx` CLI. Every command prints a one-line result;
errors are descriptive (most common: missing OS permissions, see Permissions).

## First step

Run `tarsx doctor` before any other action (falls back to `tarsx info` if missing).
It takes a real screenshot and nudges the mouse 2px to verify that macOS
Screen Recording and Accessibility permissions are actually granted to THIS
process — backends can be installed while events are still silently dropped.
If `doctor` reports a problem, follow its `hints` before trying to control anything.

## Install (once, if `tarsx` is not on PATH)

```bash
bash "$(dirname "$0")/scripts/install.sh"   # or an absolute path to this skill's scripts/install.sh
```

The installer copies the bundled, dependency-free `tarsx` to `~/.local/bin`.
No npm/network/API keys needed afterwards. Verify with `tarsx info`.

## Core loop (look → decide → act)

1. **Check**: `tarsx doctor` — confirm events are really delivered on this machine.
2. **Look**: `tarsx screenshot /tmp/shot.png` — then Read the PNG file to see the screen.
3. **Locate**: pick the target element's pixel coordinates from the screenshot,
   or skip coordinates entirely with `tarsx windows [App]` + `tarsx clickwin <App>`.
4. **Act**: `tarsx click X Y` / `tarsx type "text"` / `tarsx key k --cmd`.
5. **Verify**: take another screenshot and confirm the action landed before moving on.

## Command reference

```
tarsx screenshot [out.png] [--region x,y,w,h]   # screen capture (PNG path printed)
tarsx click <x> <y> [--right] [--double]        # click at global screen points
tarsx clickwin <AppName> [--offset dx,dy]       # BEST: click inside named app's window (center by default)
tarsx windows [AppName]                         # list visible windows: app, title, x,y,w,h
tarsx scroll [up|down] [lines]                  # scroll wheel
tarsx type "text"                               # keystrokes; non-ASCII goes via clipboard+⌘V
tarsx key <char|named> [--cmd] [--ctrl] [--alt] [--shift]
        # named keys: return, tab, escape, delete, home, end, page up, page down,
        # left/right/up/down arrow, space, f1..f12
tarsx wait <seconds>                            # pause between actions (let apps load)
tarsx apps                                      # list visible running apps
tarsx open <AppName>                            # launch app ("Calculator", "Safari"...)
tarsx open <https://url>                        # open URL in default handler
tarsx osa 'tell application "Finder" to ...'    # arbitrary AppleScript (macOS: full automation)
tarsx info [--json]                             # diagnostics: detected backends + config
tarsx doctor [--json]                           # self-test: real screenshot + 2px mouse probe,
                                                # catches missing Screen Recording / Accessibility
```
Add `--json` to any command for machine-readable output.

## Recipes

- Open an app and do something in it (no manual coordinates needed):
  `tarsx open "TextEdit"` → `tarsx wait 1.5` → `tarsx clickwin TextEdit` → `tarsx type "..."`.
- Need a specific spot inside a window: `tarsx windows TextEdit` gives x,y,w,h →
  compute the point → `tarsx click X Y`.
- Keyboard shortcut: `tarsx key s --cmd` (⌘S), `tarsx key w --cmd` (close tab/window).
- Ukrainian/Russian text: works automatically — non-ASCII is typed via clipboard paste,
  so the target field must be focused first.
- System queries that don't need GUI: prefer `tarsx osa` (e.g. battery, volume,
  window bounds: `tarsx osa 'tell application "System Events" to tell process "Safari" to get {position, size} of window 1'`).

## Permissions (macOS)

macOS gates clicks/typing (Accessibility) and screenshots (Screen Recording).
Bare binaries — e.g. a bot process launched by launchd — never get the permission
prompt and silently drop mouse events, so this skill ships a helper app.

**How it works now:** `tarsx` verifies delivery before acting. If direct events
don't land and `~/Applications/TarsX.app` exists (built by `scripts/install.sh`
or `scripts/make-app.sh`), actions automatically route through it — macOS shows
the standard "TarsX wants to control your computer" prompt on first use.
Ask the user to click **Allow/Дозволити** once; after that everything works.

If the helper is missing or still blocked:
1. Build it: `bash <skill-folder>/scripts/make-app.sh`
2. If no prompt appears, open the right pane for the user:
   `open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"`
   and ask them to add `~/Applications/TarsX.app` (for blank screenshots:
   the same in **Screen Recording**).
3. `tarsx doctor` re-verifies; do not retry GUI actions until it passes.

Classic grants (host terminal app or the agent's node binary) also still work.

## Safety rules

- Confirm before: deleting anything, sending messages/emails, purchases, logging out,
  closing windows with unsaved work ("Изменено"/"Edited" in the title).
- Never type passwords or one-time codes into GUI fields — ask the user to do it.
- After finishing, leave the screen in a clean state (close what you opened,
  discard test documents without saving).
- If a click "didn't land", re-screenshot instead of blindly retrying — UI may have changed.
