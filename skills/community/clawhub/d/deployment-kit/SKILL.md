---
name: "deployment-kit"
description: "Deploy and maintain services on a VPS with 1 command: build → restart → verify → monitor with heartbeat + Telegram alerts. Complete DevOps package: systemd units, nginx reverse proxy, cron @reboot, watchdog restarts, deploy scripts. WARNING: runs systemd restarts, sudo, nohup/setsid and changes runtime state — only use on services you own, test on staging first."
metadata: {"deployment-kit": {"requires": {"bins": ["systemctl", "sudo", "curl", "nohup", "setsid"], "network": ["https://api.telegram.org"], "env": ["TG_BOT_TOKEN", "TG_CHAT_ID"], "files": ["~/.config/tg-alert.env"]}}}
---

# Deployment Kit 🚀🖥️

Get your service deployed and running 24/7 — with automatic restart on failure.

## What you get

1. **Deploy script** — 1 command: copy code → restart → verify
2. **Systemd unit** — auto-start on boot + auto-restart on crash
3. **Nginx reverse proxy** — port → domain
4. **Cron @reboot** — services that run without systemd
5. **Watchdog** — heartbeat check + restart + Telegram alert

## Quick start

```bash
# Preview first (no changes) — recommended
bash scripts/deploy.sh --dry-run myapp

# Deploy (asks for confirmation before restart)
bash scripts/deploy.sh myapp

# Watchdog (cron every 2 min)
*/2 * * * * bash /opt/myapp/watchdog.sh myapp

# Telegram alert on failure (scripts/notify.sh)
bash scripts/notify.sh "⚠️ myapp down — restarted"
```

## What the scripts actually do (transparency)

- **deploy.sh** — builds, then restarts the service: `sudo systemctl restart` for systemd services, or `pkill -f` + `nohup` relaunch for plain processes. **Always asks for confirmation** (or use `--dry-run` to preview). Can cause downtime.
- **watchdog.sh** — checks the heartbeat file age; restarts the service + sends a Telegram alert if stale.
- **notify.sh** — sends a Telegram message using a bot token read from `~/.config/tg-alert.env` (or env vars).

## Templates

```
deployment-kit/
├── SKILL.md
└── scripts/
    ├── deploy.sh      # build → restart → verify
    ├── watchdog.sh    # heartbeat + auto-restart + alert
    ├── notify.sh      # Telegram message (bot token + chat id)
    └── myapp.service  # systemd unit template
```

## Best practices (learned on 8 services)

- Heartbeat file is written by the app every 30-60s → watchdog checks mtime
- Never `pkill -f "pattern"` that matches itself — use `"pa[t]tern"` or lsof
- Slow processes: `setsid bash -c '...' </dev/null >/dev/null 2>&1 &` — intentional daemonization (process keeps running after shell exit)
- ALWAYS verify after deploy (curl /health, log line, MD5)

## 🔒 Security & responsibility (important — read before use)

- **Destructive:** deploy restarts services, replaces running code and can cause downtime. Test on staging first, and have a rollback plan.
- **sudo:** deploy.sh uses `sudo systemctl restart` — requires sudo rights and affects the whole system. Only run commands you understand.
- **Secrets:** Telegram token (TG_BOT_TOKEN) and chat id are credentials. Store them in `~/.config/tg-alert.env` with `chmod 600`, never in scripts, logs, shell history or git.
- **nohup/setsid:** used intentionally to run services in the background outside the terminal — normal daemon practice, not hidden behavior.
- **Always review scripts** before running them on a production server.
---
