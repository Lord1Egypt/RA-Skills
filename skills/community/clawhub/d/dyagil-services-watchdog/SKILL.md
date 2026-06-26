---
name: dyagil-services-watchdog
description: Set up a systemd-based watchdog that keeps long-running Node.js services (Telegram bots, Express dashboards, etc.) alive across shell exits, ssh disconnects, agent-runtime restarts, and server reboots. Use whenever the user reports "the bot died again", "service is down after restart", or after any event that may have killed child processes. Provides a 2-minute user-systemd timer that detects and auto-restarts services with their `.env` correctly loaded.
version: 1.0.0
license: MIT
author: dyagil
---

# Services Watchdog

## Problem

Long-running Node services launched from a parent shell (or as children of an agent runtime) die when the parent exits. Runtime restarts are especially aggressive — they tend to take down everything they spawned as collateral damage. Manual `nohup`/`setsid` rituals survive an ssh disconnect but not a reboot.

## Architecture

```
my-watchdog.timer          (systemd --user; OnUnitActiveSec=2min)
    ↓
my-watchdog.service        (Type=oneshot; KillMode=process)
    ↓
services-watchdog.sh
    ↓
for each service: check → if down → systemd-run --user --scope → exec node
```

Two non-obvious details make this actually work:

1. **`KillMode=process` + `systemd-run --user --scope`** — without this, systemd kills the children of a `Type=oneshot` service as soon as the service exits. The combination puts each restarted service in its own transient scope, outside the watchdog's cgroup.
2. **`.env` is loaded INSIDE the new scope.** The watchdog wraps the start command in `bash -c 'cd <project> && set -a && . ./.env; set +a && exec node <entry>'`. This propagates every env var without the watchdog having to know which ones the service needs (`TELEGRAM_BOT_TOKEN`, `OPENAI_API_KEY`, …).

## Files

- [scripts/services-watchdog.sh](scripts/services-watchdog.sh) — the script. Customize the per-service `check_*` / `restart_*` blocks.
- [scripts/sahi-watchdog.service](scripts/sahi-watchdog.service) — systemd unit template.
- [scripts/sahi-watchdog.timer](scripts/sahi-watchdog.timer) — runs every 2 minutes.

Rename the unit files to match your own prefix (e.g. `mybot-watchdog.*`) when adopting.

## Install

```bash
WORKSPACE="$HOME/.openclaw/workspace"     # or wherever your projects live
mkdir -p "$WORKSPACE/scripts" "$WORKSPACE/logs" ~/.config/systemd/user

cp scripts/services-watchdog.sh   "$WORKSPACE/scripts/"
cp scripts/sahi-watchdog.service  ~/.config/systemd/user/
cp scripts/sahi-watchdog.timer    ~/.config/systemd/user/
chmod +x "$WORKSPACE/scripts/services-watchdog.sh"

systemctl --user daemon-reload
systemctl --user enable --now sahi-watchdog.timer
loginctl enable-linger "$USER"   # keeps the timer running when not logged in
```

## Verify

```bash
# State after most recent run:
cat ~/.openclaw/workspace/memory/watchdog-state.json
# Recent recoveries / failures:
tail ~/.openclaw/workspace/logs/watchdog.log
# Schedule:
systemctl --user list-timers sahi-watchdog.timer --no-pager
```

End-to-end test (replace `4321` with the port your service listens on):

```bash
PID=$(ss -tlnp 2>/dev/null | awk '/:4321 /{print $NF}' | grep -oP 'pid=\K[0-9]+' | head -1)
kill "$PID"
systemctl --user start sahi-watchdog.service   # don't wait 2 min
ss -tln | grep 4321                            # should be listening again
```

(Do NOT use `pkill -f "myservice/server.js"` to kill the test target — your own exec shell often matches the same regex and gets SIGTERM'd.)

## Adapt to a New Service

In `services-watchdog.sh`, add three things and append the service name to the `services=()` array:

```bash
check_myservice() {
  pgrep -f "<unique-marker-in-cmdline>" >/dev/null 2>&1
}

restart_myservice() {
  cd "$WORKSPACE/projects/myservice" || return 1
  systemd-run --user --scope --quiet --unit="myservice-$(date +%s%N)" \
    --setenv=PATH="$PATH" --setenv=HOME="$HOME" \
    bash -c 'cd '"$WORKSPACE"'/projects/myservice && set -a && [ -f .env ] && . ./.env; set +a && exec nohup node src/index.js >> logs/svc.log 2>&1 < /dev/null' &
  disown 2>/dev/null || true
  sleep 3
  check_myservice
}

labels_myservice="My Service"
```

## Gotchas (Learned the Hard Way)

- **Don't use `Type=simple`** for the systemd service — that keeps the watchdog itself alive long after it should have exited, and it re-enters every 2 minutes.
- **PATH inside `systemd-run --user --scope` is minimal.** Always pass `--setenv=PATH="$PATH"` if a child relies on `~/.npm-global/bin` or similar; or call binaries by absolute path.
- **`pgrep -f` matches the watchdog shell itself.** Use a unique marker (file path) when defining `check_*`, e.g. `pgrep -f "myservice/src/index"`, not just `pgrep -f "node src/index.js"` which can collide with other projects.
- **`Type=oneshot` with default `KillMode=control-group`** kills the children you just spawned. Always set `KillMode=process` AND launch via `systemd-run --user --scope` so the new process lives outside the watchdog's cgroup.

## See Also

- A `taskflow` or cron skill for one-shot scheduled tasks. The watchdog is for "always-on" services, not periodic jobs.
