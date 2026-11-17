---
name: computer-use-kylinos
description: GUI automation on KylinOS. V11 (Wayland/wlcom) uses wlcctrl; V10SP1 (X11) uses xdotool. Find/launch/focus windows, screenshot, click/type/drag with correct coordinates, and verify GUI results.
---

# Computer Use KylinOS

GUI automation across KylinOS V11 (Wayland) and V10SP1 (X11). Resolve script paths relative to this skill directory.

## Step 0 — detect the OS

Always run first; pick the backend by result.

```bash
bash scripts/detect-os.sh   # -> v11 | v10sp1 | unknown
```

| Result   | Backend  | Tool      | Protocol |
|----------|----------|-----------|----------|
| `v11`    | Wayland  | `wlcctrl` | wlcom    |
| `v10sp1` | X11      | `xdotool` | X        |

## Fast path

### V11 (Wayland) — wlcctrl

```bash
bash scripts/wlcctrl-info.sh                      # inspect once per task
wlcctrl --search '<app_id_or_title_regex>'
wlcctrl --getwindowgeometry <w_uuid>
wlcctrl --windowcapture <w_uuid> --path /tmp/win.png   # pick coords from this
wlcctrl --windowactivate <w_uuid>
wlcctrl --keystring 'text'                         # keyboard is fastest
wlcctrl --key ctrl+s
bash scripts/wlcctrl-window-click.sh <w_uuid> <rx> <ry> [button]   # scale-aware click
bash scripts/wlcctrl-window-dblclick.sh <w_uuid> <rx> <ry> [button] [delay_ms]  # double-click (geometry queried ONCE, no re-verify)
bash scripts/wlcctrl-drag.sh <w_uuid> <sx> <sy> <ex> <ey> [button] # drag
```

For Kaiming apps: `kaiming list | grep -i '<app>'; kaiming run <app-id>`.

### V10SP1 (X11) — xdotool

```bash
bash scripts/xdotool-info.sh                      # inspect once per task
xdotool search --name '<title_regex>'
xdotool getwindowgeometry <wid>
import -window <wid> /tmp/win.png                  # screenshot to pick coords (needs imagemagick)
xdotool windowactivate <wid>
xdotool type 'text'                                # keyboard is fastest
xdotool key ctrl+s
bash scripts/xdotool-window-click.sh <wid> <rx> <ry> [button]   # click
bash scripts/xdotool-window-dblclick.sh <wid> <rx> <ry> [button] [delay_ms]  # double-click (native --repeat 2, single process)
bash scripts/xdotool-drag.sh <wid> <sx> <sy> <ex> <ey> [button] # drag
```

Find the app window, screenshot it, read target `(rx,ry)` from the image, then click/drag with the relative coordinates.

## Universal rules

- Do **not** move a window to `(0,0)` by default. Use the move-window script only when a known position is required, the window is partly off-screen, or the user asks.
- Prefer keyboard shortcuts/input over pointer clicks when available.
- Capture the window in its current position; identify targets from the screenshot.
- For wheel/spinner controls prefer small drag gestures over scroll (scroll may jump values).
- Avoid closing/killing windows unless explicitly requested.
- Cache window geometry / display info per task — repeated probes are expensive.

## V11 (wlcctrl) specifics

- ⚠️ **man page is WRONG about coordinates.** It documents `--mousemove`/`--windowmove` as *relative displacements*; both are actually **ABSOLUTE**. Pass the absolute target, never add current position.
- `--mousemove` input = logical × output scale `S`; `--getmouselocation` returns logical.
- `--windowmove -x/-y` takes **logical** coordinates directly (NO × S).
- Multi-monitor: if window geometry is output-relative, add that output's `position` to `WX,WY` first.
- Use `wlcctrl --outputs` + `--getdisplaygeometry <o_uuid>` for scale/position.
- Lock keys (CapsLock/NumLock) don't toggle reliably — use `ydotool`.

## V10SP1 (xdotool) specifics

- **No fractional scaling.** Screen coordinates = window origin + relative offset. No scale factor anywhere.
- `xdotool mousemove` / `windowmove` take **screen pixel** coordinates directly (absolute).
- Screenshot via `import` (ImageMagick): `import -window <wid> /tmp/win.png`. Requires `sudo apt install imagemagick`.
- Window IDs are **decimal integers** (not UUIDs).
- `xdotool getwindowgeometry --shell <wid>` prints `X=`, `Y=`, `WIDTH=`, `HEIGHT=` for easy parsing.

## Coordinate formula

### V11 — multiply by scale (mousemove/clicks/drags)

Given window geometry `(WX,WY)`, output scale `S`, target `(RX,RY)` in window screenshot:

```text
logical_x = WX + RX
mousemove_x = round(logical_x * S)     # every --mousemove arg, start and end
```

### V11 — windowmove: NO scale

```text
windowmove -x = TX    # logical target, do NOT × S
```

### V10SP1 — no scale at all (clicks/drags/windowmove all the same)

```text
screen_x = WX + RX
```

The `xdotool-window-click.sh` / `xdotool-drag.sh` / `xdotool-move-window.sh` scripts do this for you.

## Core commands

### wlcctrl (V11)

```bash
wlcctrl --outputs; wlcctrl --getdisplaygeometry <o_uuid>
wlcctrl --list; wlcctrl --search '<regex>'; wlcctrl --getactivewindow
wlcctrl --getwindowname <w_uuid>; wlcctrl --getwindowgeometry <w_uuid>
wlcctrl --windowactivate <w_uuid>
wlcctrl --windowmove <w_uuid> -x <x> -y <y>
wlcctrl --windowsize <w_uuid> -w <w> -h <h>
wlcctrl --windowminimize|maximize|fullscreen <w_uuid> [-o <o_uuid>]
wlcctrl --windowmap <w_uuid>
wlcctrl --windowcapture <w_uuid> --path /tmp/w.png
wlcctrl --fullscreencapture --path /tmp/f.png [-o <o_uuid>]
wlcctrl --mousemove <x>,<y>; wlcctrl --getmouselocation
wlcctrl --mousebutton 1; wlcctrl --mousepress 1 --mouserelease 1
wlcctrl --scroll -y <delta>
wlcctrl --keystring 'text'; wlcctrl --key ctrl+s
wlcctrl --keydown <key>; wlcctrl --keyup <key>
```

### xdotool (V10SP1)

```bash
xdotool search --name '<regex>'; xdotool search --onlyvisible --name ''
xdotool getactivewindow; xdotool getwindowname <wid>
xdotool getwindowgeometry [--shell] <wid>
xdotool windowactivate <wid>; xdotool windowfocus <wid>
xdotool windowmove <wid> <x> <y>
xdotool windowsize <wid> <w> <h>
xdotool getmouselocation; xdotool mousemove <x> <y>
xdotool click <button>; xdotool mousedown <button>; xdotool mouseup <button>
xdotool type 'text'; xdotool key ctrl+s
xdotool keydown <key>; xdotool keyup <key>
import -window <wid> /tmp/w.png        # screenshot (imagemagick)
```

## When more detail is needed

Read `references/details.md` for keyboard aliases, multi-step test patterns, spinner controls, screenshots, multi-monitor handling, and X11 caveats.
