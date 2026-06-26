---
name: dont-be-scary
description: Update OpenClaw safely on macOS (brew cask install) with automatic snapshot of the npm package + .app bundle, post-update health check, and automatic rollback to the previous version if the gateway doesn't come back. The update script runs detached so it survives the gateway restart that kills the calling agent. Notifies progress via Telegram at every step (start, success, failure, rollback). Use when the user asks to update OpenClaw, upgrade to a new version, run "openclaw update", or wants protection against a broken update breaking their gateway. Mac-only (requires brew cask install + launchctl). Requires Telegram configured in openclaw.json and ~500MB free in /tmp.
---

# dont-be-scary

Safe OpenClaw update with snapshot + auto-rollback. Survives the gateway restart that would otherwise kill the agent mid-operation.

## When to invoke

Trigger when the user requests an OpenClaw update or upgrade. Examples: "update openclaw", "upgrade openclaw", "actualízate", "openclaw update".

Do NOT call `openclaw update` directly — the gateway restart kills the calling agent before it can verify success or roll back.

## How to use

Launch the script **detached** so it survives the gateway restart:

```bash
nohup "<path-to-skill>/scripts/safe-update.sh" </dev/null >/dev/null 2>&1 & disown
```

Then tell the user: "Update launched in background. You'll get Telegram updates at each step." Do not wait for the script to finish — the gateway restart will likely terminate the current agent session. The user is the source of truth via Telegram.

The script's path inside an installed skill workspace is typically:
`<workspace>/skills/dont-be-scary/scripts/safe-update.sh`

## What the script does

1. Reads bot token + chat_id from the user's `~/.openclaw/openclaw.json` (Telegram default account, delivery target).
2. Snapshots `/opt/homebrew/lib/node_modules/openclaw` and `/Applications/OpenClaw.app` to `/tmp/openclaw-rollback/<timestamp>/` (~500MB).
3. Sends Telegram: "🔄 Updating from <X>".
4. Runs `openclaw update --json` (which restarts the gateway by itself).
5. Health check loop (180s) hitting `http://localhost:18789/`.
6. **Success** → Telegram "✅ <X> → <Y>", prunes old snapshots (keeps last 2).
7. **Failure** → restores snapshot, restarts gateway via launchctl, Telegram "⚠️ rollback OK".
8. **Critical** (rollback also failed) → Telegram urgent message pointing to `references/rescue-prompt.md`.

## Configuration via env vars (all optional)

Defaults match a standard `brew install --cask openclaw` setup. Override only if non-standard:

- `OPENCLAW_TG_CHAT_ID` — Telegram chat to notify (default: auto-detect from `delivery.targets[]`)
- `OPENCLAW_TG_BOT` — bot account name in config (default: `default`)
- `OPENCLAW_CONFIG` — path to openclaw.json (default: `~/.openclaw/openclaw.json`)
- `OPENCLAW_NPM_DIR` — npm install path (default: `/opt/homebrew/lib/node_modules/openclaw`)
- `OPENCLAW_APP_DIR` — .app bundle (default: `/Applications/OpenClaw.app`)
- `OPENCLAW_GATEWAY_PORT` — health check port (default: `18789`)
- `OPENCLAW_PLIST` — LaunchAgent (default: `~/Library/LaunchAgents/ai.openclaw.gateway.plist`)
- `OPENCLAW_BIN` — openclaw binary (default: `/opt/homebrew/bin/openclaw`)
- `OPENCLAW_SNAP_ROOT` — snapshot root (default: `/tmp/openclaw-rollback`)

## Requirements

- macOS with brew cask install of OpenClaw
- ~500MB free in `/tmp`
- Telegram configured in `openclaw.json` (`channels.telegram.accounts.default.botToken` + a delivery target with `channel: telegram` and `to: <chat_id>`)
- `python3` and `curl` available (both shipped with macOS)

## If the worst happens

If the script reports **🚨 CRITICAL**, the gateway is down and the agent inside OpenClaw can't help itself. Open Claude Code on the same Mac and use the prompt in `references/rescue-prompt.md` to recover manually.

## Logs

- Per-run log: `/tmp/openclaw-update-<timestamp>.log`
- Update output: `/tmp/openclaw-update-<timestamp>.update.json`
- Snapshots retained: 2 most recent in `/tmp/openclaw-rollback/`
