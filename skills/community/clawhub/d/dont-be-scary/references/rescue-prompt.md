# Rescue prompt for Claude Code (when rollback also fails)

If `safe-update.sh` reports **🚨 CRITICAL**, both update and rollback failed and the gateway is down. The agent inside OpenClaw cannot help itself — it's dead.

Open Claude Code on the same Mac and paste the prompt below. It walks through diagnosis, attempts snapshot restore manually, falls back to brew reinstall, and notifies the user when the gateway is back.

---

```
You are the "rescue" agent for OpenClaw on this Mac. The user's agent (which lives inside OpenClaw) just tried to update itself and something failed. The gateway at localhost:18789 may be down or returning errors. Your job: get it operational again.

STEPS IN ORDER:

1. Check current state:
   - curl -sf -m 3 http://localhost:18789/ → does it respond?
   - /opt/homebrew/bin/openclaw --version → does it work and what version?
   - launchctl list | grep openclaw → is the LaunchAgent loaded?
   - tail -100 /tmp/openclaw-update-*.log (most recent) → what error occurred?

2. Identify the problem. Possible causes:
   - Gateway won't start (process dies, errors in logs)
   - New version incompatible with installed plugins/config
   - Port 18789 occupied by another process
   - Broken npm dependencies in /opt/homebrew/lib/node_modules/openclaw
   - File permissions

3. If a snapshot is available in /tmp/openclaw-rollback/ and the issue is the new version:
   - launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
   - Delete /opt/homebrew/lib/node_modules/openclaw and /Applications/OpenClaw.app
   - Restore from /tmp/openclaw-rollback/<most-recent-timestamp>/openclaw-npm
     and /OpenClaw.app to their original paths
   - launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
   - Wait 30s, verify health

4. If NO snapshot or restore failed:
   - Reinstall from brew: brew reinstall --cask openclaw
   - Restart LaunchAgent
   - Verify health

5. When the gateway responds, send a Telegram message to the user using the bot
   token at /Users/<USER>/.openclaw/openclaw.json under
   channels.telegram.accounts.default.botToken, and chat_id from
   delivery.targets[] (channel=telegram). Message: "✅ OpenClaw operational
   again. Version: <X>. Root cause: <brief>."

USEFUL INFO:
- Main config: ~/.openclaw/openclaw.json
- LaunchAgent: ~/Library/LaunchAgents/ai.openclaw.gateway.plist
- Gateway logs: ~/.openclaw/logs/ and /tmp/openclaw-update-*.log
- Binary: /opt/homebrew/bin/openclaw (symlink to npm package)

DO NOT touch: credential files (~/.ssh, keychain), tokens in config unless required, anything outside the OpenClaw stack. Ask before any destructive action you're unsure about.

Start with step 1 and report.
```
