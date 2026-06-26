# Gateway Guardian

<p align="center"><a href="https://github.com/Dios-Man/gateway-guardian/blob/main/README.md">中文</a>丨English</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/platform-Linux-blue.svg" alt="Platform: Linux">
  <img src="https://img.shields.io/badge/OpenClaw-Skill-brightgreen.svg" alt="OpenClaw Skill">
</p>

> An OpenClaw skill that automatically rolls back corrupted configs, restarts a crashed gateway, and notifies you the moment something goes wrong.

---

## What problem does it solve?

OpenClaw's AI capabilities depend entirely on the gateway. If the gateway goes down, you lose access to your AI.

There are two common causes:

**1. Corrupted config file**  
When an AI modifies your config (e.g., adding an API key or switching models), a formatting error or missing field can make `openclaw.json` invalid. The gateway will fail to start on the next restart.

**2. Unexpected gateway crash**  
Memory issues, resource exhaustion, or intermittent bugs can bring the gateway down mid-session.

Gateway Guardian handles both automatically and notifies you right away.

---

## How it works

### Config protection (real-time)

Every time `openclaw.json` changes, Guardian validates it in milliseconds across three checks:

1. Valid JSON syntax
2. Required fields present (`gateway.port` must exist)
3. OpenClaw's own schema validation

If validation fails, Guardian immediately rolls back to the most recent valid backup. The whole process is automatic — you don't need to do anything.

### Crash recovery (OnFailure)

If the gateway crashes 3 times within 60 seconds, Guardian takes over:
1. Checks the config (rolls back if needed)
2. Restarts the gateway
3. Waits up to 30 seconds for the port to become available
4. Sends a success notification if recovered, or an urgent alert if not

### Notifications

Whether Guardian fixes things automatically or needs your help, it sends a notification to your messaging channel (Feishu / Telegram / Discord / etc.).

---

## Notification examples

**Config auto-fixed (no action needed):**

```
✅ OpenClaw Gateway Guardian

⏰ Time: 2026-03-09 22:10
📋 Event: Config file corrupted — auto-rolled back and recovered
🔧 Rolled back to: openclaw.json.20260309-221005
📝 Recent log:
[22:10:03] ❌ Config invalid: missing gateway.port
[22:10:04] ✅ Rolled back to timestamp backup
[22:10:04] ✅ Gateway is running

💬 If this alert was triggered by my own action, please forward this message to me directly — no explanation needed. I'll understand the context and continue automatically.
```

**Gateway crash — auto-recovered (no action needed):**

```
✅ OpenClaw Gateway Guardian — Gateway Recovered

⏰ Time: 2026-03-09 22:10
📋 Event: Gateway crashed (config healthy) — auto-restarted
🔧 Action: Reset failed count + restart gateway
✅ Result: Gateway is back online

💬 If this alert was triggered by my own action, please forward this message to me directly — no explanation needed. I'll understand the context and continue automatically.
```

**Manual intervention required:**

```
🚨 OpenClaw Gateway Guardian — Gateway Recovery Failed

⏰ Time: 2026-03-09 22:10
📋 Event: Gateway crashed and could not be restarted automatically
❌ Reason: Gateway still unresponsive after restart attempts
📝 Recent log:
[22:10:03] Gateway failed repeatedly — starting recovery
[22:10:36] ❌ Gateway still unresponsive after 30s
🔍 Gateway log:
Mar 09 22:10:06 node[xxx]: Error: EADDRINUSE: port 18789 already in use

Please log into the server to handle this manually.
```

**When the gateway restarts (two messages):**

```
⚙️ Gateway is restarting, please wait...
```
```
✅ Gateway recovered. You can continue your conversation.
```

> **About "forward this message to me":**  
> A gateway restart interrupts any task that was in progress. If the AI was in the middle of helping you when the restart happened, just forward this notification back to it — no explanation needed. It will pick up where it left off. Alternatively, you can just say "the gateway just restarted" and it will understand.

---

## Installation

**Requirements:**
- Linux with `systemd --user` available
- OpenClaw Gateway running
- `inotify-tools` (auto-installed if missing, or manually: `sudo apt-get install -y inotify-tools`)

Once the requirements are met, send the following link to your OpenClaw agent and say "install this":

```
https://raw.githubusercontent.com/Dios-Man/gateway-guardian/main/SKILL.md
```

OpenClaw will automatically detect your messaging channel and user ID, and configure everything. It will also set the notification language based on the language you're using in the conversation.

**What the installation does:**
1. Backs up your current config (pre-install snapshot)
2. Pulls script files from the GitHub repository
3. Registers the `openclaw-config-watcher` service (persistent config file monitor)
4. Registers the `openclaw-recovery` service (triggered on gateway crash via OnFailure)
5. Adds an `ExecStopPost` hook to the gateway service (sends notification before stop)
6. Generates `guardian.conf` (stores your fallback notification config)

---

## Uninstall

Tell your OpenClaw agent: "uninstall gateway-guardian"

Or run manually:

```bash
systemctl --user stop openclaw-config-watcher.service
systemctl --user disable openclaw-config-watcher.service
rm -f ~/.config/systemd/user/openclaw-config-watcher.service
rm -f ~/.config/systemd/user/openclaw-recovery.service
rm -f ~/.config/systemd/user/openclaw-gateway.service.d/recovery.conf
systemctl --user daemon-reload
systemctl --user reset-failed openclaw-gateway.service 2>/dev/null
```

Config backups in `~/.openclaw/config-backups/` are kept after uninstall. To delete them:

```bash
rm -rf ~/.openclaw/config-backups/
```

---

## Logs

```bash
tail -f /tmp/config-watcher.log    # Config monitor + notification log
tail -f /tmp/gateway-recovery.log  # Crash recovery log
ls -lt ~/.openclaw/config-backups/ # Timestamped backup list
```

---

## FAQ

**Q: Will Guardian interfere with normal OpenClaw operation?**  
No. The config-watcher uses inotifywait (event-driven), so it has near-zero CPU usage at rest. It only runs briefly when the config file changes.

**Q: What if notifications aren't coming through?**  
Check `FALLBACK_CHANNEL` and `FALLBACK_TARGET` in `guardian.conf`, or reinstall the skill to let OpenClaw re-detect your channel.

**Q: Where do notifications get sent?**  
Before each notification, Guardian queries the most recently active session and prefers DMs. If detection fails, it falls back to the channel and target stored in `guardian.conf` during installation.

**Q: Will Guardian roll back my intentional config changes?**  
No. As long as your changes are valid (correct JSON, required fields present), Guardian saves them as a new backup. Only invalid configs get rolled back.

**Q: Is `guardian.conf` safe?**  
It only stores your messaging channel and user ID (fallback config) — no API keys or passwords. It is never uploaded to GitHub.

---

## Architecture

```
config-watcher service starts
    ↓
Startup check: validate current config
    ├─ Valid → save backup
    └─ Invalid → rollback → notify user

openclaw.json changes
    ↓
config-watcher (inotifywait, persistent)
    ├─ Valid → save timestamped backup
    └─ Invalid → rollback → notify user

Gateway process crashes
    ↓
systemd auto-restart
    ↓
3 failures in 60s → OnFailure triggered
    ↓
gateway-recovery
    ├─ Check config (rollback if needed)
    ├─ Restart gateway
    ├─ Wait up to 30s for port
    ├─ Recovered → notify user
    └─ Failed → urgent alert (with error logs)

Gateway intentional restart
    ↓
ExecStopPost (pre-stop.sh) → send "restarting" notification
    ↓
config-watcher background monitor (polls every 5s)
    └─ Detects recovery → send "recovered" notification
```

---

## License

MIT
