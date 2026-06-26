---
name: cmus
description: AI skill to launch cmus in a Xubuntu terminal and enforce playback rules (single track vs shuffle folder). Robust against high latency and headless daemon environment.
homepage: https://github.com/cmus/cmus
metadata: {"clawdbot":{"emoji":"🎹","requires":{"bins":["cmus","cmus-remote","xfce4-terminal","pgrep"]},"install":[{"id":"apt-cmus","kind":"apt","formula":"cmus","bins":["cmus","cmus-remote"],"label":"Install cmus (apt)"}]}}
---

# cmus (OpenClaw Playback Controller)

Workflow: Receive file path from yt-dlp -> Launch cmus UI (if not running) -> Wait for socket -> Apply user's specific playback rules -> Play.

## Find the active daemon & Launch UI

When OpenClaw runs in the background, it lacks X11/Wayland display variables. The agent MUST inject the environment variables and dynamically poll for the cmus socket instead of using hardcoded sleep.

Execute this precise bash block to ensure the terminal opens and the socket is ready:
export DISPLAY=${DISPLAY:-:0.0}
export XAUTHORITY=${XAUTHORITY:-$HOME/.Xauthority}
export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$(id -u)/bus"

if ! pgrep -x cmus > /dev/null; then
    xfce4-terminal -e cmus &
    for i in {1..20}; do
        cmus-remote -C "status" >/dev/null 2>&1 && break
        sleep 0.5
    done
fi

## Playback Rule Engine

The agent must parse the user's prompt to determine the playback mode. **CRITICAL:** The agent MUST resolve `<path_to_file>` using `eval echo` to ensure absolute pathing before passing to `cmus-remote`.

### Mode A: Play track and shuffle the rest (Default)
Trigger Intent: "Play this track", "Open song...", "Play and shuffle".
Execute this bash block:
TARGET_FILE=$(eval echo "<path_to_file>")
cmus-remote -C "clear"
cmus-remote -C "add $HOME/.openclaw/workspace/music/"
cmus-remote -C "set continue=true"
cmus-remote -C "set shuffle=true"
cmus-remote -f "$TARGET_FILE"

### Mode B: Play ONLY the requested track
Trigger Intent: "Play only this track", "Do not shuffle", "Single track mode".
Execute this bash block:
TARGET_FILE=$(eval echo "<path_to_file>")
cmus-remote -C "clear"
cmus-remote -C "add $TARGET_FILE"
cmus-remote -C "set continue=false"
cmus-remote -C "set repeat=false"
cmus-remote -p
