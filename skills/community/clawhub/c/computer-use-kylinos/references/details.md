# KylinOS GUI Automation Details

Two backends, picked by `scripts/detect-os.sh`:

- **Part A — KylinOS V11** (Wayland / UKUI / wlcom) → `wlcctrl`
- **Part B — KylinOS V10SP1** (X11 / UKUI) → `xdotool`

---

# Part A — V11 (Wayland / wlcctrl)

## Context

KylinOS V11 Desktop uses UKUI on Wayland with `wayland-compositor` / `wlcom`. Prefer `wlcctrl` over X11 assumptions for GUI automation.

## Output and scale

```bash
wlcctrl --outputs
wlcctrl --getdisplaygeometry <output_uuid>
gsettings get org.ukui.SettingsDaemon.plugins.xsettings scaling-factor 2>/dev/null || true
```

Example output:

```text
physical size: 300x190 mm
scale: 1.750000
mode: 2880 x 1800 @ 90
position: 0, 0
```

`xdpyinfo` may show Xwayland logical DPI such as `96x96`; do not use it alone for Wayland coordinate conversion.

**Multi-monitor:** each output has a `position` (e.g. a screen right of primary shows `1920,0`). On tested setups `--getwindowgeometry` returns global coordinates that already include this offset, so the click/drag scripts work directly. If a machine reports window geometry relative to its output, add that output's `position` to `WX,WY` before computing `logical`, or the cursor lands on the wrong display. Actions that accept `-o <o_uuid>` to target a specific output: `--fullscreencapture`, `--setarea`, `--getpixelcolor`, `--windowmaximize`, `--windowfullscreen`. `--mousemove` has no `-o` and uses global coordinates.

## Windows

```bash
wlcctrl --list
wlcctrl --search '<regex>'
wlcctrl --getactivewindow
wlcctrl --getwindowname <w_uuid>
wlcctrl --getwindowgeometry <w_uuid>
wlcctrl --windowactivate <w_uuid>
wlcctrl --windowmove <w_uuid> -x 0 -y 0   # only when a known position is required
wlcctrl --windowsize <w_uuid> -w 800 -h 600
wlcctrl --movewindowtooutput <w_uuid>:<o_uuid>
```

## Screenshots

```bash
wlcctrl --windowcapture <w_uuid> --path /tmp/window.png
wlcctrl --fullscreencapture --path /tmp/full.png
wlcctrl --setarea <x,y,width,height> --path /tmp/area.png
wlcctrl --workspacecapture <workspace_uuid:output_uuid> --path /tmp/workspace.png
```

## Keyboard and pointer

```bash
wlcctrl --key ctrl+alt+t
wlcctrl --keystring 'text to type'
wlcctrl --mousebutton 1
wlcctrl --mousepress 1 --mouserelease 1
wlcctrl --scroll -y 10
wlcctrl --getmouselocation
```

For drag actions, move to start, press, move to end, release. `--mousemove` and `--windowmove` are absolute despite the man page describing displacement (see the ⚠️ warning in SKILL.md).

### Keyboard key names, aliases, and combos

`--key` / `--keydown` / `--keyup` accept single keys or `+`-separated combos (e.g. `--key ctrl+alt+t`). The following friendly names are aliases `wlcctrl` resolves automatically — you usually do **not** need to write the raw `control_l` form:

| Type this | Resolves to |
|-----------|-------------|
| `ctrl`    | `control_l` |
| `shift`   | `shift_l`   |
| `alt`     | `alt_l`     |
| `winleft` | `super_l`   |
| `esc`     | `escape`    |
| `enter`   | `return`    |
| `PrintScreen` | `sys_req` |

Other valid keys include `escape, return, shift_l/r, control_l/r, alt_l/r, meta_l/r, page_up, page_down, menu, caps_lock, pause, break, print, sys_req, scroll_lock, num_lock`, etc.

- **Lock-key warning:** `CapsLock` (code 58), `NumLock` (69), and `ScrollLock` (70) may **not** toggle reliably via `wlcctrl`. For reliable lock-key state changes, use `ydotool` instead.
- **Hold a key:** `--keydown <key>` ... `--keyup <key>`, optionally with `--sleep <ms>` between (e.g. `--keydown a --sleep 500 --keyup a`).
- **Type text:** `--keystring 'text'` (no commands can chain after `--keystring`).

For wheel/spinner controls such as time pickers, prefer drag gestures over `--scroll` when exact values matter. In testing, `--scroll` on the UKUI Clock minute wheel jumped several values, while repeated one-row drags changed minutes predictably.

## Coordinate recipe

Given:

- output scale = `S`
- window geometry = `(WX, WY) WIDTH x HEIGHT`
- target point in captured window image = `(RX, RY)`

Then:

```text
logical_x = WX + RX
logical_y = WY + RY
mousemove_x = round(logical_x * S)
mousemove_y = round(logical_y * S)
```

Run:

```bash
wlcctrl --mousemove "${mousemove_x},${mousemove_y}"
wlcctrl --getmouselocation
wlcctrl --mousebutton 1
```

Known tested example:

- output `eDP-1`, scale `1.75`
- calculator window `geometry: (607, 176) 432 x 628`
- `=` center in window screenshot `(376,593)`
- logical target `(983,769)`
- `--mousemove` input about `(1720,1346)`
- `--getmouselocation` returns about `(983,769)`

## Reliable test pattern (V11)

1. Launch or focus the app and identify the target window.
2. Capture the window in its current position; do not move it unless the test requires fixed placement, visibility recovery, or multi-monitor placement.
3. Identify target controls from screenshot coordinates.
4. Prefer keyboard shortcuts/input when possible.
5. For pointer tests, use scaled absolute `--mousemove`, verify `--getmouselocation`, then click.
6. For spinners/wheels, use controlled drags and verify after a few steps rather than relying on large scroll deltas.
7. Capture again and verify visually or with OCR/image analysis.
8. Log commands and outputs under `artifacts/` when reproducibility matters.

## Performance notes (V11)

- A single `wlcctrl` invocation can cost ~0.3s due to startup/graphics initialization.
- Avoid repeated `--outputs`, `--getdisplaygeometry`, and `--getwindowgeometry` inside loops when values are stable.
- Avoid screenshot + vision analysis unless the UI changed or verification is required.
- For known apps, cache window geometry and known control coordinates.
- Use one shell block for short deterministic sequences to reduce round trips, but keep a screenshot/vision checkpoint before fragile branches.
- For Kaiming apps, executable symlinks under `/opt/kaiming/bin/` may be wrappers; use `kaiming list` to find the app ID and launch with `kaiming run <app-id>`.

## Double-click (V11)

**Why calling the click script twice fails:** each invocation of `wlcctrl-window-click.sh` re-queries geometry, outputs, and display scale (~3 × 0.3s), re-moves the mouse, and re-verifies location — totalling ~2s per click. Two sequential calls produce a ~4s gap, far exceeding the compositor's double-click threshold (~300–500ms).

**Solution:** use `wlcctrl-window-dblclick.sh`. It queries geometry and scale **once**, moves the mouse **once** (no `--getmouselocation` verification), then fires two `--mousepress/--mouserelease` pairs separated by a configurable delay (default 80ms). The two clicks land within ~0.4s total, well inside the threshold.

```bash
bash scripts/wlcctrl-window-dblclick.sh <w_uuid> <rx> <ry> [button] [delay_ms]
```

---

# Part B — V10SP1 (X11 / xdotool)

## Context

KylinOS V10SP1 Desktop uses UKUI on X11. There is no Wayland compositor, so use `xdotool` for pointer/keyboard and ImageMagick `import` (or `maim`/`scrot`) for screenshots.

## Prerequisites

```bash
sudo apt install xdotool imagemagick   # imagemagick provides `import` for screenshots
xdotool version
import -version
```

If `import` is unavailable, alternatives: `maim -i <wid> /tmp/w.png` or `scrot` (full screen only). Prefer `import -window <wid>` because it captures just the target window, matching the coordinate space of the click/drag scripts.

## Display and scale

```bash
xdpyinfo | grep -Ei 'dimensions|resolution'
```

**No fractional scaling in X11.** Screen coordinates are physical pixels; there is no output scale factor to apply. If the desktop uses integer scaling / DPI, `xdotool` mousemove coordinates still map 1:1 to `xdpyinfo` dimensions and to window-geometry coordinates, so no conversion is needed.

## Windows

```bash
xdotool search --name '<title_regex>'          # window IDs by title
xdotool search --onlyvisible --name ''         # all visible windows
xdotool getactivewindow
xdotool getwindowname <wid>
xdotool getwindowgeometry --shell <wid>        # prints X=, Y=, WIDTH=, HEIGHT=
xdotool windowactivate <wid>
xdotool windowfocus <wid>
xdotool windowmove <wid> <x> <y>               # absolute screen pixels
xdotool windowsize <wid> <w> <h>
```

Window IDs are **decimal integers**. `getwindowgeometry --shell` is the easiest to parse in scripts (see `xdotool-window-click.sh`).

## Screenshots

```bash
import -window <wid> /tmp/window.png           # single window (preferred)
import /tmp/full.png                           # whole screen (interactive; needs click)
maim /tmp/full.png                             # whole screen (non-interactive)
```

The window screenshot's `(0,0)` is the window top-left, matching the `(RX,RY)` used by the click/drag scripts.

## Keyboard and pointer

```bash
xdotool type 'text to type'
xdotool key ctrl+s
xdotool key alt+F4
xdotool keydown <key> ... xdotool keyup <key>  # hold a key
xdotool getmouselocation
xdotool mousemove <x> <y>                       # absolute screen pixels
xdotool click <button>                          # 1=left 2=middle 3=right
xdotool mousedown <button> ... xdotool mouseup <button>   # drag
```

Key names use X11 keysym names (`Return`, `Escape`, `Tab`, `space`, `Control_L`, `Alt_L`, etc.). Combos use `+`: `xdotool key ctrl+alt+t`. `xdotool type` sends literal text; use `--clearmodifiers` if stuck modifiers interfere.

## Coordinate recipe (V10SP1)

Given:

- window geometry `X=WX, Y=WY`
- target point in captured window image = `(RX, RY)`

Then (no scale):

```text
screen_x = WX + RX
screen_y = WY + RY
```

Run:

```bash
xdotool mousemove "$screen_x" "$screen_y"
xdotool getmouselocation
xdotool click 1
```

The `xdotool-window-click.sh` and `xdotool-drag.sh` scripts do this conversion for you.

## Reliable test pattern (V10SP1)

1. Launch or focus the app; find the target window via `xdotool search --name`.
2. `xdotool windowactivate <wid>` and capture with `import -window <wid> /tmp/w.png`.
3. Identify target controls from screenshot coordinates `(RX,RY)`.
4. Prefer keyboard shortcuts/`xdotool type` when possible.
5. For pointer tests, run `xdotool-window-click.sh <wid> <rx> <ry> [button]`; it verifies `getmouselocation` before clicking.
6. For spinners/wheels, use `xdotool-drag.sh` with small steps and verify between steps.
7. Capture again and verify visually or with OCR/image analysis.

## Caveats (V10SP1)

- `import -window <wid>` may include window decorations (title bar / borders) depending on the WM; if clicks land offset, measure the decoration height from a full-screen capture and subtract it from `RY`.
- `xdotool` needs the window to be mapped/visible; a minimized window must be activated first.
- On multi-monitor X11, `xdotool mousemove` uses the combined root-window coordinate space (monitors tiled), so `WX,WY` from `getwindowgeometry` are already global — no per-output offset needed.
- If the session runs under Xwayland (rare on V10SP1), coordinates can differ; confirm protocol with `echo $XDG_SESSION_TYPE` (should be `x11`).

## Double-click (V10SP1)

**Why calling the click script twice is fragile:** two separate `xdotool-window-click.sh` invocations each re-query geometry, re-move, and re-verify (~0.2s each), plus two bash process startups. The total gap (~0.5–0.7s) sits right at the X server's double-click threshold and fails intermittently.

**Solution:** use `xdotool-window-dblclick.sh`. It queries geometry **once**, moves the mouse **once**, then uses `xdotool click --repeat 2 --delay <ms>` — a **single xdotool process** that fires both clicks internally with precise timing (default 80ms apart). No inter-process gap.

```bash
bash scripts/xdotool-window-dblclick.sh <wid> <rx> <ry> [button] [delay_ms]
```
