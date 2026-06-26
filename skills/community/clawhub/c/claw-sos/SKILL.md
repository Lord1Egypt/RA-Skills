---
name: claw-sos
description: Install, run, and manage the SOS emergency recovery tool for OpenClaw instances. Use when (1) the bot stops responding on Telegram/Discord and needs diagnosis or recovery, (2) you need to install SOS on a new or existing machine, (3) autofix, rollback, network check, or Telegram test is needed, (4) the user mentions "sos", "recovery", "bot is down", "not responding", or "emergency fix".
---

# claw-sos

Emergency recovery tool for OpenClaw. Diagnoses and fixes unresponsive bots via SSH.

## Install

The script is bundled at `scripts/sos.sh`. Install locally:
```bash
cp scripts/sos.sh /usr/local/bin/sos
chmod +x /usr/local/bin/sos
```

To install on a remote machine:
```bash
scp scripts/sos.sh root@<IP>:/usr/local/bin/sos
ssh root@<IP> "chmod +x /usr/local/bin/sos"
```

Alternative — install from GitHub:
```bash
curl -fsSL https://raw.githubusercontent.com/clawsos/claw-sos/main/install.sh | bash
```

## Usage

### Interactive (human via SSH)
```bash
sos          # whiptail arrow-key menu
```

### Non-interactive (agent or cron)
```bash
sos auto     # autofix: diagnose → doctor → restart → force → nuclear
sos net      # network check only
sos tg       # telegram test message
sos --version
sos --help
```

### When the bot is down — decision tree

1. Run `sos auto` — handles 95% of cases automatically
2. If autofix fails → run `sos net` — if network is broken, fix DNS/internet first
3. If network is fine but bot still down → run `sos tg` — check Telegram delivery
4. If Telegram fails → check bot token validity
5. Last resort → `sos` menu option 9 (Nuclear) — kills everything and starts fresh

## Menu Options

| # | Name | What it does | Safe? |
|---|------|-------------|-------|
| 1 | Check status | Gateway running, RAM, disk, version | ✅ Read-only |
| 2 | Restart | Graceful restart | ✅ Safe |
| 3 | Force kill | Kill process + restart | ⚠️ Drops active sessions |
| 4 | Rollback | Revert to previous version + config | ⚠️ Downgrade |
| 5 | View logs | Last 50 lines of gateway log | ✅ Read-only |
| 6 | Full diagnostic | RAM, disk, Telegram, sessions, process | ✅ Read-only |
| 7 | Backup config | Save config + version before changes | ✅ Safe |
| 8 | Self-test | Verify SOS script works | ✅ Read-only |
| 9 | Nuclear | Kill ALL openclaw processes, reload | 🔴 Last resort |
| 10 | Autofix | Escalating auto-repair | ⚠️ May restart |
| 11 | Network check | DNS, internet, Telegram API, Anthropic | ✅ Read-only |
| 12 | Telegram test | Send real test message | ✅ Safe |

## Autofix Escalation Order

1. Diagnose: process, RAM, disk
2. Clean RAM/disk if critical
3. `openclaw doctor --fix`
4. Graceful restart → wait 15s → check
5. Force kill + restart → wait 15s → check
6. Nuclear (kill all + reload)

Stops as soon as gateway is healthy.

## Log Location

All actions logged to `~/.openclaw/backups/sos.log`. Read this to understand what happened during recovery:
```bash
cat ~/.openclaw/backups/sos.log
```

## Platform Support

- **Linux:** Full support (systemd, journalctl, free, /proc)
- **macOS:** Full support (launchctl, log show, vm_stat, purge, dialog fallback)
- **Docker:** Partial — no systemd, manual fallback works

## Credentials

This skill uses **no API keys or tokens of its own**. It reads existing OpenClaw config to:
- Check gateway status (local process, no network)
- Send Telegram test messages (uses the bot token already configured in `openclaw.json`)
- Check Anthropic API reachability (HTTPS ping only, no auth)

No credentials are stored, transmitted, or required to install or run SOS.

## Source

GitHub: https://github.com/clawsos/claw-sos
