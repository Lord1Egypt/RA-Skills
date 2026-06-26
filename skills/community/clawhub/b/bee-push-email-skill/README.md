# 🐝 bee-push-email v1.5.3

**Real-time push email notifications for OpenClaw agents.**

bee-push-email detects new emails the instant they arrive using IMAP IDLE (push, not polling) and triggers your OpenClaw agent to process and notify you through your active channel — Telegram, Discord, or any other connected surface.

## What It Does

```
📧 Email arrives
    ↓
🖥️ IMAP IDLE (push, ~1s latency)
    ↓
🤖 OpenClaw agent processes it
    ↓
📱 You get notified on Telegram/Discord/etc.
```

- **Push, not polling** — IMAP IDLE keeps a persistent connection. The mail server pushes events to you instantly. No 15-minute intervals, no wasted API calls.
- **Agent-driven** — Your OpenClaw agent reads, analyzes, and decides what to do: notify you, move spam, flag important emails, or stay silent.
- **Non-interactive setup** — Designed for agent use. The agent asks you questions, builds the config, and runs the installer. Zero TTY required.
- **Self-healing** — Auto-reconnects on connection loss. Runs as a systemd service with automatic restart.
- **Multi-account** — Configure once per email account. Each runs as an independent watcher service.

## How It Works

### Architecture

| Component | Role |
|---|---|
| `imap_watcher.py` | Python script maintaining IMAP IDLE connection |
| `setup.py` | Installer with dependency checks, connection tests, and post-install verification |
| `uninstall.sh` | Clean removal script |
| `imap-watcher.service` | Systemd unit for daemon management |

### Flow

1. **IMAP IDLE** connection stays open (near-zero resource usage)
2. Mail server pushes new email event
3. Watcher detects it, triggers `openclaw agent --deliver`
4. Agent reads email with **Himalaya**, analyzes it, notifies user

### Tracking

Uses **UID tracking** (not SEEN flags) — doesn't matter if another client reads the email first. Every new UID triggers a notification.

## Dependencies

| Tool | Required | Auto-installed | Purpose |
|---|---|---|---|
| **python3** | ✅ | No | Runs the watcher |
| **python3-venv** | ✅ | No | Isolated environment for imapclient |
| **openclaw** | ✅ | No | Triggers the agent on new email |
| **systemd** | ✅ | No | Service management |
| **curl** | ⚠️ | No | Auto-installs himalaya if missing |
| **himalaya** | ⚠️ | Yes* | Agent uses it to read/move/reply emails |
| **imapclient** | ✅ | Yes | Python IMAP library (installed in venv, not system-wide) |

*\*Himalaya is downloaded from GitHub Releases only if not already installed. Supports x86_64, arm64, armv7.*

## Security & Permissions

This skill makes the following system-level changes. **The agent should inform the user and get approval before installing.**

| Action | Details |
|---|---|
| **Python venv** | Creates `/opt/imap-watcher/` with isolated Python environment |
| **pip install** | Installs `imapclient` inside the venv only (not system-wide) |
| **himalaya download** | Downloads binary from GitHub Releases to `/usr/local/bin/` (only if missing) |
| **systemd service** | Creates `/etc/systemd/system/imap-watcher.service`, enables and starts it |
| **Config file** | Writes `/opt/imap-watcher/watcher.conf` with chmod 600 (owner-only read/write) |
| **System user** | Creates `imap-watcher` system user — service runs as non-root |
| **Bot token read** | Reads `botToken` from `~/.openclaw/openclaw.json` to register Telegram menu commands |
| **Log files** | Writes to `/var/log/imap-watcher.log` and systemd journal |

**Uninstall** removes everything: service, files, systemd unit, log files, system user, and bot commands.

### Auto-reply control

By default the agent **never replies to senders** (`auto_reply_mode: false`). This prevents exposing that the system is active and avoids unintentional replies to spam or phishing emails. You can change this at any time from Telegram:

| Command | Effect |
|---|---|
| `/beemail_reply` | Show current auto-reply mode |
| `/beemail_reply_off` | 🔒 Disable auto-reply (never reply) |
| `/beemail_reply_ask` | ❓ Ask for your approval before each reply |
| `/beemail_reply_on` | ⚠️ Enable auto-reply (agent decides — use with caution) |

Changes take effect immediately — the service restarts automatically.

## Installation

The agent guides you through 4 stages:

### Stage 1: Check Dependencies (`--deps`)
Verifies python3, venv, openclaw, systemd, curl are available.

### Stage 2: Test Connection (`--test`)
Validates IMAP + SMTP + Himalaya with your credentials. Nothing is installed.

### Stage 3: Install
Deploys the watcher as a systemd service. Automatically runs Stage 1 + 2 first.

### Stage 4: Verify (automatic)
Checks service is running, IMAP is connected, config is valid, agent is reachable.

### End-to-End Test
After installation, send an email to yourself. If you get the notification in your chat, everything works.

## Configuration

All config lives in `/opt/imap-watcher/watcher.conf` (JSON, chmod 600):

```json
{
  "host": "imap.example.com",
  "port": 993,
  "ssl": true,
  "email": "user@example.com",
  "password": "app-password",
  "folder": "INBOX",
  "poll_interval": 60,
  "preferred_channel": "telegram",
  "message": "Custom notification message (optional)"
}
```

| Field | Required | Default | Description |
|---|---|---|---|
| `host` | ✅ | — | IMAP server hostname |
| `port` | ✅ | — | IMAP port (usually 993) |
| `ssl` | ✅ | — | Use SSL/TLS |
| `email` | ✅ | — | Email address |
| `password` | ✅ | — | Password or app-specific password |
| `folder` | — | `INBOX` | IMAP folder to watch |
| `poll_interval` | — | `60` | Seconds between reconnect attempts (not polling) |
| `preferred_channel` | — | `telegram` | Channel to find active session on |
| `channel` | — | auto | Specific channel (bypasses auto-detection) |
| `target` | — | auto | Chat/user ID for the channel |
| `message` | — | see below | Custom prompt for the agent (overrides auto_reply_mode instruction) |
| `auto_reply_mode` | — | `false` | Agent reply behavior: `false` (never), `ask` (approval required), `true` (agent decides) |

### Session Resolution

The watcher dynamically finds your active OpenClaw session each time it fires:
1. If `channel` + `target` are set → uses `--channel --to` (most reliable)
2. Otherwise → parses `openclaw sessions` output to find your direct session

## Commands

| Command | Description |
|---|---|
| `setup.py --deps` | Check system dependencies |
| `setup.py --test` | Test IMAP/SMTP/Himalaya connection |
| `setup.py --show` | View current config (password hidden) |
| `setup.py --register-commands` | Register beemail Telegram bot commands (after update) |
| `setup.py --reconfigure` | Add new config fields after a skill update |
| `setup.py --reply-status` | Show current `auto_reply_mode` |
| `setup.py --reply-off` | Set `auto_reply_mode=false` + restart service |
| `setup.py --reply-ask` | Set `auto_reply_mode=ask` + restart service |
| `setup.py --reply-on` | Set `auto_reply_mode=true` + restart service |
| `setup.py <json>` | Full install (deps → test → install → verify) |
| `uninstall.sh --yes` | Complete removal (non-interactive) |
| `systemctl status imap-watcher` | Check service status |
| `journalctl -u imap-watcher -f` | Follow live logs |

## Troubleshooting

| Problem | Solution |
|---|---|
| Service won't start | Check logs: `journalctl -u imap-watcher -n 20` |
| Not getting notifications | Verify: `openclaw sessions` shows your session |
| IMAP connection fails | Run: `setup.py --test` to diagnose |
| Wrong session receiving alerts | Set `channel` + `target` in config |
| Duplicate notifications | Check UID state: `/opt/imap-watcher/last_seen_uids.json` |

## Telegram Bot Commands

After install, these commands are available in your Telegram bot menu:

| Command | Description |
|---|---|
| `/beemail` | Quick status — service health + last email |
| `/beemail_status` | Detailed status + recent logs |
| `/beemail_start` | Start the watcher service |
| `/beemail_stop` | Stop the watcher service |
| `/beemail_test` | Verify end-to-end push delivery |
| `/beemail_reply` | Show current auto-reply mode |
| `/beemail_reply_off` | 🔒 Disable auto-reply |
| `/beemail_reply_ask` | ❓ Require approval before replying |
| `/beemail_reply_on` | ⚠️ Enable auto-reply (agent decides) |

## FAQ

### Does this work with custom IMAP servers?
Yes. Any server that supports IMAP (port 993, SSL) works — self-hosted, business email, or personal servers. Provide the host, port, and SSL settings in the config.

### Is it really instant push, or does it poll?
**Push.** IMAP IDLE maintains a persistent TCP connection. Your mail server pushes events through it. Latency is typically 1-3 seconds from email arrival to your Telegram notification.

### Can I run it from Telegram?
Yes. The entire setup is non-interactive — no TTY required. The agent asks you questions in Telegram, builds the JSON config, and runs the installer. All commands (`--deps`, `--test`, `--show`, `uninstall.sh --yes`) work without human interaction on the server.

### Can I monitor multiple email accounts?
Yes. Each account runs its own watcher service. You'd need to customize the service name and config path for each one. The agent can set this up for you.

### What happens if the connection drops?
The watcher auto-reconnects every `poll_interval` seconds (default 60s). The systemd unit also restarts the service automatically if it crashes.

### Does it work on ARM (Raspberry Pi, Mac)?
Yes. Himalaya binary detection supports x86_64, arm64, and armv7. The Python code is architecture-independent.

### Can I reconfigure if I change email?
Yes. Re-run the install with new credentials. The old config is backed up automatically to `watcher.conf.bak`. Or edit `/opt/imap-watcher/watcher.conf` directly and run `systemctl restart imap-watcher`.

### How do I apply new settings after updating the skill?
Run `setup.py --reconfigure`. It detects any new config fields added in the update, asks you about each one interactively, and leaves your existing values untouched. Then restart the service: `systemctl restart imap-watcher`.

### What if my agent reads the email before the watcher detects it?
No problem. The watcher uses **UID tracking**, not SEEN flags. Even if your agent or another client reads the email first, the watcher still detects the new UID and fires.

### Can the agent automatically process emails (not just notify)?
Yes. The agent receives the event and decides what to do — move spam to folders, flag urgent emails, reply to specific senders, or just notify you. The `message` field in config lets you customize the agent's instructions per account.

### Does it work without Himalaya?
The push notification still fires without Himalaya. But the agent won't be able to read, move, or reply to emails. Himalaya is strongly recommended.

### Can I customize the notification channel?
Yes. Set `channel` and `target` in the config (e.g., `telegram` + chat ID). Or let the watcher auto-detect your active session via `preferred_channel`.

### Can I control auto-replies without SSH?
Yes. Use `/beemail_reply_off`, `/beemail_reply_ask`, or `/beemail_reply_on` directly from Telegram. Changes apply immediately — the service restarts automatically. The default is `false` (never reply), which is the safest option.

### Is my password stored securely?
The config file is saved with chmod 600 (owner read/write only). The password never appears in logs or command output. Temporary himalaya test configs are cleaned up automatically.

### How do I completely remove it?
```bash
bash /root/.openclaw/workspace/skills/bee-push-email/scripts/uninstall.sh --yes
```
This stops the service, removes `/opt/imap-watcher/`, the systemd unit, and log files.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for full version history.

## License

MIT
