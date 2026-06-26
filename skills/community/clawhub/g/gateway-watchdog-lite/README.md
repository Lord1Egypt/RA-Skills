# Gateway Watchdog Lite

> **Supplied by [ConfusedUser.com](https://confuseduser.com) — OpenClaw tools & skills**

Keep your OpenClaw gateway running 24/7. This skill installs a lightweight background service that checks your gateway every **2 minutes** and automatically recovers it if it goes down — no manual intervention needed.

---

## What It Does

| Feature | Detail |
|---|---|
| Probe interval | Every 120 seconds |
| Health check | HTTP probe to `127.0.0.1:<your-port>` — accepts 200, 301, 302 |
| Auto-recovery | Full restart via launchd (macOS) or systemd (Linux) |
| Cooldown | 5 minutes between recovery attempts (prevents thrashing) |
| Telegram alerts | Optional — notifies you when gateway goes down and comes back |
| Logs | `/tmp/openclaw/gateway-watchdog.log` |

> **⚠️ Lite version** — Does not include crash loop detection or auto-mitigation.  
> Want that? Upgrade to the **full Gateway Watchdog** at [confuseduser.com](https://confuseduser.com).

---

## Requirements

- OpenClaw installed and configured
- macOS (Homebrew) **or** Linux (systemd)
- `curl` (almost certainly already installed)
- `gog` CLI — optional, only needed for Telegram alerts

---

## Quick Install

### macOS

```bash
WORKSPACE_PATH=/your/workspace OC_PORT=18789 TELEGRAM_ID=your_telegram_id bash scripts/install.sh
```

**Without Telegram alerts:**
```bash
WORKSPACE_PATH=/your/workspace OC_PORT=18789 TELEGRAM_ID="" bash scripts/install.sh
```

### Linux

```bash
WORKSPACE_PATH=/your/workspace OC_PORT=18789 TELEGRAM_ID=your_telegram_id bash scripts/install-linux.sh
```

### Finding your values

| Parameter | How to find it |
|---|---|
| `WORKSPACE_PATH` | Run `openclaw status` — look for workspace path |
| `OC_PORT` | Run `openclaw status` — look for gateway port (usually 18789) |
| `TELEGRAM_ID` | Message `@userinfobot` on Telegram |

---

## Verify It's Running

**macOS:**
```bash
launchctl list | grep watchdog
```

**Linux:**
```bash
systemctl --user status gateway-watchdog
```

---

## View Logs

```bash
tail -f /tmp/openclaw/gateway-watchdog.log
```

---

## Manual Test

Force a watchdog check right now (reset cooldown first if testing recovery):

```bash
rm -f /tmp/openclaw/watchdog-last-recovery
bash scripts/gateway-watchdog.sh
```

---

## Uninstall

**macOS:**
```bash
launchctl bootout gui/$UID/ai.openclaw.gateway-watchdog
rm ~/Library/LaunchAgents/ai.openclaw.gateway-watchdog.plist
```

**Linux:**
```bash
systemctl --user stop gateway-watchdog
systemctl --user disable gateway-watchdog
rm ~/.config/systemd/user/gateway-watchdog.service
systemctl --user daemon-reload
```

---

## Known Gotchas

See `references/gotchas.md` for OC-specific recovery notes:

- **GGML Metal crash** on Apple Silicon — add `GGML_NO_METAL=1` to env
- **Stale config** — run `openclaw gateway install --force` after config changes
- **Stuck launchd** — use bootout + bootstrap, not load/unload
- **Telegram not arriving** — check `gog telegram status` and PATH

---

## Want More?

The **full Gateway Watchdog** (paid) adds:

- 🔁 **Crash loop detection** — identifies if the gateway crashes 3+ times in 15 minutes
- 🛡️ **Auto-mitigation** — takes corrective action before alerting you
- 📊 **Recovery history** — tracks patterns over time

👉 **[Get it at ConfusedUser.com](https://confuseduser.com)**

---

*Gateway Watchdog Lite is free and open. If it saved your bacon, consider upgrading.*
