---
name: bee-push-email
description: Push email notifications via IMAP IDLE + Himalaya + OpenClaw agent. Detects new emails in real-time and triggers the agent to process and notify the user. Use when: setting up email push notifications, configuring IMAP watcher, installing bee-push-email system, testing email connectivity, checking system dependencies, viewing email-push config, troubleshooting IMAP IDLE watcher, or managing the imap-watcher systemd service. Also handles uninstall/cleanup of the bee-push-email system. Trigger on beemail commands: /beemail, /beemail_start, /beemail_stop, /beemail_status, /beemail_test, /beemail_reply, /beemail_reply_off, /beemail_reply_ask, /beemail_reply_on. Also: start watcher, stop watcher, watcher status, email push status, registrar comandos, comandos no aparecen, beemail no funciona en telegram.
emoji: 📧
requirements:
  bins:
    - python3
    - systemctl
    - openclaw
---

# Email Push — IMAP IDLE → OpenClaw Agent → User Notification

Real-time email monitoring: IMAP IDLE detects new emails, triggers OpenClaw agent to process and notify the user via their active channel.

## Security & Permissions

**The agent MUST explicitly inform the user of all actions below and obtain approval before starting installation. Do not proceed without confirmed user consent.**

### What this skill installs (requires root)

| Action | Path / Target | Notes |
|---|---|---|
| **System user** | `imap-watcher` (useradd -r) | Service runs as this non-root user |
| **Python venv** | `/opt/imap-watcher/` | Isolated env, not system-wide |
| **pip package** | `imapclient` (inside venv only) | Not installed system-wide |
| **Watcher script** | `/opt/imap-watcher/imap_watcher.py` | Copied from skill directory |
| **systemd unit** | `/etc/systemd/system/imap-watcher.service` | Enabled + started, restarts on boot |
| **Config file** | `/opt/imap-watcher/watcher.conf` | chmod 600, owner imap-watcher only |
| **Log file** | `/var/log/imap-watcher.log` | chmod 640, owner imap-watcher |

### External downloads (requires user awareness)

| What | From | Condition |
|---|---|---|
| `himalaya` binary | `github.com/pimalaya/himalaya/releases/latest/` | Only if not already installed |
| Method | `curl \| tar` into `/usr/local/bin/` | Writes a system binary |

### Credentials accessed

| Credential | Source | Usage |
|---|---|---|
| IMAP email password | Provided by user at install time | IMAP IDLE connection |
| Telegram `botToken` | Read from `~/.openclaw/openclaw.json` | Registers `/beemail*` commands via Telegram API (`setMyCommands`) |

The bot token is **never stored** by this skill.

### Auto-reply behaviour

By default, the agent is instructed **not to reply to email senders**. This prevents exposing that the system is active and avoids phishing/spam risks. The `allow_auto_reply` field in `watcher.conf` controls this:

| Value | Behaviour |
|---|---|
| `false` (default) | Agent notifies you via Telegram only. **Never** replies to senders. |
| `ask` | Agent asks you for **explicit approval** via Telegram before replying. |
| `true` | Agent may reply to senders if it deems appropriate (least safe). |

Configured interactively during install. Change anytime with `--reconfigure` + `systemctl restart imap-watcher`.

**If `auto_reply_mode` is missing from an existing install**, the watcher logs `[SECURITY] WARNING` on startup and notifies the agent to alert you. The safe default `false` is applied until you run `--reconfigure`. It is read once per operation and used only to call `api.telegram.org`. The agent must inform the user that their bot token will be used to modify the bot's command menu.

### Persistence

This skill installs a **persistent background service** (`Restart=always`, starts on boot). It maintains a continuous IMAP connection. The service runs as the dedicated `imap-watcher` user, not as root.

**Uninstall** removes everything: service, systemd unit, `/opt/imap-watcher/`, log file, system user, and Telegram bot commands.

## Install Flow (4 stages)

### Stage 1: Dependencies (`--deps`)
```bash
python3 /root/.openclaw/workspace/skills/bee-push-email/scripts/setup.py --deps
```

### Stage 2: Test Connection (`--test`)
```bash
echo '{"host":"...","port":993,"ssl":true,"email":"...","password":"..."}' | python3 /root/.openclaw/workspace/skills/bee-push-email/scripts/setup.py --test
```

### Stage 3: Install (only if Stage 1+2 passed)
```bash
echo '{"host":"...","port":993,"ssl":true,"email":"...","password":"..."}' | python3 /root/.openclaw/workspace/skills/bee-push-email/scripts/setup.py
```

### Stage 4: Verify (automatic)

## Other Modes

### Register Bot Commands (after update)
```bash
python3 /root/.openclaw/workspace/skills/bee-push-email/scripts/setup.py --register-commands
```

### Reconfigure (after update)

After running `clawhub update bee-push-email`, new config fields may be available. Run:

```bash
python3 /root/.openclaw/workspace/skills/bee-push-email/scripts/setup.py --reconfigure
```

This detects fields missing from your existing `/opt/imap-watcher/watcher.conf` and asks about each one interactively — without touching your existing values. Restart the service after: `systemctl restart imap-watcher`.

### Force Reinstall
```bash
echo '{...}' | python3 /root/.openclaw/workspace/skills/bee-push-email/scripts/setup.py --force
```

### Show Config / Uninstall
```bash
python3 /root/.openclaw/workspace/skills/bee-push-email/scripts/setup.py --show
bash /root/.openclaw/workspace/skills/bee-push-email/scripts/uninstall.sh --yes
```

## Telegram Bot Commands

<details>
<summary>Click to expand command details</summary>

### `/beemail_status`
1. `systemctl is-active imap-watcher` + `systemctl status imap-watcher --no-pager -l`
2. Last 10 log lines: `journalctl -u imap-watcher -n 10 --no-pager`
3. UID state: `cat /opt/imap-watcher/last_seen_uids.json`
4. Report: status, uptime, last email, IMAP state

### `/beemail_start`
1. `systemctl start imap-watcher` → wait 3s → verify active → show last 5 log lines

### `/beemail_stop`
1. `systemctl stop imap-watcher` → verify inactive → report

### `/beemail_test`
1. Check service active → read target email from config → tell user to send test email
2. Optionally run: `setup.py --test`

### `/beemail`
Quick summary: service active? + last email processed + one-liner health

### `/beemail_reply`
Show current auto-reply mode:
1. Run `python3 <skill_dir>/scripts/setup.py --reply-status`
2. Report current mode with label: DISABLED / ASK / ENABLED

### `/beemail_reply_off`
Disable auto-reply immediately:
1. Run `python3 <skill_dir>/scripts/setup.py --reply-off`
2. Service restarts automatically
3. Confirm: "🔒 Auto-reply DISABLED"

### `/beemail_reply_ask`
Set approval-required mode:
1. Run `python3 <skill_dir>/scripts/setup.py --reply-ask`
2. Service restarts automatically
3. Confirm: "❓ Auto-reply set to ASK"

### `/beemail_reply_on`
Enable auto-reply — **warn the user first**:
1. Inform user: "⚠️ Enabling auto-reply exposes system activity to all senders including spam/phishing. Confirm?"
2. Only proceed if user confirms
3. Run `python3 <skill_dir>/scripts/setup.py --reply-on`
4. Service restarts automatically
5. Confirm: "⚠️ Auto-reply ENABLED"

</details>

## Telegram Bot Commands Troubleshooting

If `/beemail*` commands don't appear in the Telegram menu after install:

1. **Verify registration:**
   ```bash
   python3 /root/.openclaw/workspace/skills/bee-push-email/scripts/setup.py --register-commands
   ```

2. **Manual registration via BotFather:**
   - Open @BotFather in Telegram
   - Send `/setcommands`
   - Select your bot
   - Add each command:
     - `beemail` — Email push status & recent emails
     - `beemail_start` — Start IMAP email watcher
     - `beemail_stop` — Stop IMAP email watcher
     - `beemail_status` — Detailed watcher service status
     - `beemail_test` — Send test email to verify push

3. **If bot token not found:** The setup reads `botToken` from `~/.openclaw/openclaw.json`. Check that the Telegram channel is configured.

4. **Commands registered but agent doesn't respond:** The agent needs this skill installed to handle the commands. Verify with `clawhub list`.

## Troubleshooting

- **Logs:** `journalctl -u imap-watcher -f`
- **Status:** `systemctl status imap-watcher`
- **Restart:** `systemctl restart imap-watcher`
- **Config:** `/opt/imap-watcher/watcher.conf` (JSON, chmod 600)
- **State:** `/opt/imap-watcher/last_seen_uids.json`

## Architecture

1. `imap_watcher.py` maintains persistent IMAP IDLE connection
2. On new email, resolves active OpenClaw session (with 60s cache)
3. Triggers `openclaw agent --deliver` to process and notify user
4. Uses Himalaya for email operations (read, move, reply)
5. Runs as systemd service as dedicated `imap-watcher` user with auto-reconnect, exponential backoff, and health checks
