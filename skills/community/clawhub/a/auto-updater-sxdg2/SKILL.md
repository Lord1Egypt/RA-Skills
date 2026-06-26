---
name: auto-updater
description: "Automatically update OpenClaw and all installed skills once daily. Runs via cron, checks for updates, applies them, and messages the user with a summary of what changed."
metadata: {"version":"1.1.0","openclaw":{"emoji":"🔄","os":["windows","darwin","linux"]}}
---

# Auto-Updater Skill

Keep your OpenClaw and skills up to date automatically with daily update checks.

## What It Does

This skill sets up a daily cron job that:

1. Updates OpenClaw itself (via `openclaw update`)
2. Updates all installed skills/plugins
3. Restarts the service via `sudo systemctl restart openclaw`
4. Messages you with a summary of what was updated

## Setup

### Quick Start

Ask OpenClaw to set up the auto-updater:

```
Set up daily auto-updates for yourself and all your skills.
```

Or manually add the cron job:

```bash
openclaw cron add \
  --name "Daily Auto-Update" \
  --cron "0 4 * * *" \
  --tz "America/Chicago" \
  --session isolated \
  --wake now \
  --deliver \
  --message "Run daily auto-updates: run 'openclaw update --yes' followed by 'sudo systemctl restart openclaw'. Update skills and report what was updated."
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| Time | 4:00 AM | When to run updates (use `--cron` to change) |
| Timezone | America/Chicago | Set with `--tz` |
| Delivery | Main session | Where to send the update summary |

## How Updates Work

### OpenClaw Updates

The primary update command used is:
```bash
openclaw update --yes && sudo systemctl restart openclaw
```

This updates the core CLI, builds any source checkouts, and updates all installed plugins/skills.

### Skill Updates

Skills are updated as part of the `openclaw update` command. To update skills specifically:

```bash
openclaw skills update --all
```

## Update Summary Format

After updates complete, you'll receive a message like:

```
🔄 Daily Auto-Update Complete

**OpenClaw**: Updated to v2026.2.2-3 (was v2026.2.1)

**Skills Updated (3)**:
- discord: 2.0.3 → 2.0.4
- browser: 1.2.0 → 1.2.1  
- nano-banana-pro: 3.1.0 → 3.1.2

**Skills Already Current (5)**:
gemini, weather, reddit, twitter, yahoo-finance

Service restarted successfully via systemd.
```

## Manual Commands

Check for updates without applying:
```bash
openclaw update status
```

View current skill versions:
```bash
openclaw skills list
```

Check OpenClaw version:
```bash
openclaw --version
```

## Troubleshooting

### Updates Not Running

1. Verify cron is enabled: check `cron.enabled` in config
2. Confirm Gateway is running continuously
3. Check cron job exists: `openclaw cron list`

### Update Failures

If an update fails, the summary will include the error. Common fixes:

- **Permission errors**: Ensure the Gateway user has passwordless sudo for `systemctl restart openclaw`.
- **Network errors**: Check internet connectivity
- **Package conflicts**: Run `openclaw doctor` to diagnose

### Disabling Auto-Updates

Remove the cron job:
```bash
openclaw cron remove "Daily Auto-Update"
```

Or disable temporarily in config:
```json
{
  "cron": {
    "enabled": false
  }
}
```

## Resources

- [OpenClaw Updating Guide](https://docs.openclaw.ai/cli/update)
- [Cron Jobs](https://docs.openclaw.ai/cron)
