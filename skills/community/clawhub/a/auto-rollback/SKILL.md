---
name: auto-rollback
description: Timed rollback safety net for edits to ~/.openclaw/openclaw.json on macOS. Use when changing Gateway config, restarting Gateway after config edits, or needing backup + auto-restore protection via launchd and BOOT.md health-check cancellation.
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "os": ["darwin"],
        "requires": { "bins": ["bash", "launchctl", "jq", "curl", "plutil"] }
      }
  }
---

# Auto-Rollback

Use this skill before editing `~/.openclaw/openclaw.json`.

It creates a timestamped backup, schedules a rollback job for 10 minutes later, and restores the backup if Gateway still cannot come up. Rollback auto-cancellation is available only if the workspace `BOOT.md` includes the bundled snippet from this skill and the `boot-md` hook is already installed.

## Quick Flow

1. Run `skills/auto-rollback/auto-rollback.sh start --reason "what changed"`
2. Edit `~/.openclaw/openclaw.json`
3. Restart Gateway
4. If Gateway becomes healthy, `BOOT.md` cancels the rollback
5. If Gateway stays unhealthy, launchd executes the rollback script

## Commands

### Start protection

```bash
skills/auto-rollback/auto-rollback.sh start --reason "update gateway bindings"
```

Short form also works:

```bash
skills/auto-rollback/auto-rollback.sh start "update gateway bindings"
```

### Cancel pending rollback

```bash
skills/auto-rollback/auto-rollback.sh cancel
```

### Inspect current state

```bash
skills/auto-rollback/auto-rollback.sh status
```

## BOOT.md Integration

This skill does not install the `boot-md` hook by itself.

To enable automatic cancellation after a healthy restart:

1. Ensure your OpenClaw workspace already has the `boot-md` hook installed.
2. Merge `skills/auto-rollback/BOOT.md` into the workspace root `BOOT.md`.

Without that integration, rollback still works, but you must cancel it manually after a successful restart.

## Files

- Script: `skills/auto-rollback/auto-rollback.sh`
- BOOT snippet: `skills/auto-rollback/BOOT.md`
- Backups: `~/.openclaw/openclaw.json.YYYYMMDD-HHMMSS`
- State: `~/.openclaw/state/rollback-pending.json`
- Log: `~/.openclaw/logs/rollback.log`
- launchd plist: `~/.openclaw/ai.openclaw.rollback.plist`

## Agent Rule

If you want agents to always use this safety net, add an SOP rule in `AGENTS.md` that any `openclaw.json` change must run `start` first.
