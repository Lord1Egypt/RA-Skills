# DeadClaw

**One tap. Everything stops.**

DeadClaw is an emergency kill switch for OpenClaw agents. When something goes wrong with your agents — whether it's a runaway loop, suspicious behavior, or you just need everything stopped right now — DeadClaw halts all running agents instantly from wherever you are. Your phone, your browser, any messaging app. One action, everything stops.

---

## Why DeadClaw Exists

In February 2026, the ClawHavoc attack exposed 1,184 malicious skills in the OpenClaw ecosystem. The attack made one thing clear: if you're running agents autonomously — especially overnight or unattended — you need a fast, reliable way to shut everything down from anywhere.

Existing security tools like openclaw-defender and clawsec are comprehensive multi-layer suites, but they require technical knowledge to set up and operate. They're built for developers.

DeadClaw takes a different approach. It does one thing: stops everything. It's designed for anyone — technical or not — to set up in under five minutes and activate from their phone lock screen.

---

## Three Ways to Activate

All three methods execute the exact same kill sequence. Pick whichever one matches your situation.

### 1. Message Trigger

Send any of these words to any connected OpenClaw channel (Telegram, WhatsApp, Discord, Slack):

- `kill` or `KILL`
- `dead`
- `stop everything`
- `emergency stop`
- `deadclaw`
- `🔴`

DeadClaw detects the trigger, executes the kill, and confirms back to that same channel. Works from anywhere in the world. No computer access needed.

### 2. WebChat Kill Button

A persistent red button in your OpenClaw WebChat dashboard. Always visible. One click stops everything. For when something is visibly going wrong at your desk.

### 3. Phone Home Screen Shortcut

A big red DeadClaw button sitting on your phone's home screen, right next to your other apps. One tap sends the kill trigger to Telegram. Works from your lock screen.

Setup guides:

- [iPhone setup guide](docs/iphone-shortcut-guide.md) (iOS Shortcuts, 5 minutes)
- [Android setup guide](docs/android-widget-guide.md) (Tasker or HTTP Shortcuts, 5 minutes)

---

## What Happens When DeadClaw Fires

When triggered (by any method), DeadClaw:

1. **Kills all running OpenClaw agent processes** immediately (SIGTERM, then SIGKILL for anything that doesn't stop)
2. **Backs up your crontab** to a timestamped file, then removes all OpenClaw cron entries
3. **Terminates all active agent sessions** via the OpenClaw CLI
4. **Writes an incident log** capturing exactly what was running, what was killed, and why
5. **Sends confirmation** back to whatever triggered it:

```
🔴 DeadClaw activated. All agents stopped. 2026-02-21T03:45:12Z — 4 processes killed. 2 cron jobs paused. See deadclaw.log for full report.
```

---

## Watchdog (Automatic Protection)

DeadClaw includes a background watchdog that monitors your agents silently and auto-triggers the kill if it detects dangerous conditions — no human action needed.

The watchdog checks every 60 seconds for:

- **Runaway loops** — Any agent running longer than 30 minutes continuously
- **Token burn** — More than 50,000 tokens spent in under 10 minutes
- **Unauthorized network calls** — Outbound connections to domains not on your whitelist
- **Sandbox escape** — Any process writing files outside your designated workspace

When the watchdog fires, you get an alert explaining exactly why:

```
🔴 DeadClaw auto-triggered. Reason: agent loop exceeded 30min threshold. All processes stopped. Check deadclaw.log.
```

All thresholds are configurable via environment variables. See the [SKILL.md](SKILL.md) for the full configuration table.

---

## Installation

```bash
openclaw skill install deadclaw
```

That's it. DeadClaw is ready to use immediately via message triggers.

For the WebChat button and phone shortcut, see the setup sections below.

---

## Setup

### Message Triggers (works immediately)

No setup required. Once installed, DeadClaw listens for trigger words on all connected OpenClaw channels. Just send `kill` to any channel.

### WebChat Button

Add this to your OpenClaw WebChat configuration:

```javascript
OpenClaw.WebChat.registerWidget('deadclaw-button', {
  src: 'skills/deadclaw/ui/deadclaw-button.html',
  position: 'top-bar',
  persistent: true
});
```

The red kill button will appear at the top of your WebChat dashboard.

### Phone Home Screen Shortcut

Follow the step-by-step guides:

- **iPhone**: [docs/iphone-shortcut-guide.md](docs/iphone-shortcut-guide.md)
- **Android**: [docs/android-widget-guide.md](docs/android-widget-guide.md)

Both guides are written for non-technical users and take under 5 minutes.

### Watchdog

Start the watchdog:

```bash
# Inside the DeadClaw skill directory
./scripts/watchdog.sh start
```

Optional: configure thresholds via environment variables before starting:

```bash
export DEADCLAW_MAX_RUNTIME_MIN=45          # default: 30
export DEADCLAW_MAX_TOKENS=100000           # default: 50000
export DEADCLAW_WHITELIST=./my-whitelist.txt # one domain per line
export DEADCLAW_WORKSPACE=/path/to/workspace
```

### Network Whitelist

Create a `network-whitelist.txt` file in the DeadClaw skill directory with one allowed domain per line:

```
api.openai.com
api.anthropic.com
github.com
# Add your own domains here
```

The watchdog will kill agents that make outbound calls to any domain not in this list.

---

## Checking Status

Send `status` to any connected channel to get a health report:

```
DeadClaw Status Report
======================

Agents: 3 running
  - openclaw-agent (PID 12345) — up 12m 34s
  - claw-agent (PID 12346) — up 5m 12s
  - openclaw-skill (PID 12347) — up 1m 3s

Token spend: ~12,340 tokens/10min

Watchdog: Active (PID 99999)
```

---

## Restoring After a Kill

After a kill, send `restore` to any connected channel. DeadClaw will:

1. Show you exactly what will be restored
2. Wait for your explicit confirmation
3. Restore your crontab from the most recent backup
4. Attempt to restart the OpenClaw gateway
5. Restart the watchdog

Nothing restarts without your say-so.

---

## Testing (Dry Run)

Every script supports `--dry-run` which logs what would happen without actually killing anything:

```bash
./scripts/kill.sh --dry-run
./scripts/watchdog.sh start --dry-run
./scripts/status.sh --dry-run
./scripts/restore.sh --dry-run
```

Always test with `--dry-run` first.

---

## Configuration Reference

| Environment Variable | Default | What It Controls |
|---|---|---|
| `DEADCLAW_MAX_RUNTIME_MIN` | 30 | Max agent runtime before watchdog auto-kills |
| `DEADCLAW_MAX_TOKENS` | 50000 | Max token spend in the monitoring window |
| `DEADCLAW_TOKEN_WINDOW_MIN` | 10 | Token spend monitoring window (minutes) |
| `DEADCLAW_WHITELIST` | `./network-whitelist.txt` | Path to allowed outbound domains file |
| `DEADCLAW_WORKSPACE` | `$OPENCLAW_WORKSPACE` | Designated workspace directory |
| `OPENCLAW_PROCESS_PATTERN` | _(none)_ | Additional process name pattern to match |

---

## FAQ

**Is DeadClaw safe to trigger accidentally?**
Yes. The kill is idempotent — triggering it when no agents are running does nothing harmful. Your crontab is always backed up before any changes, and you can restore everything with the `restore` command.

**Will it kill non-OpenClaw processes?**
No. DeadClaw only targets processes matching OpenClaw agent patterns. It does not touch your other applications.

**Does the watchdog use a lot of resources?**
No. The watchdog runs a lightweight check every 60 seconds. It uses negligible CPU and memory.

**Can I customize the trigger words?**
Yes. Edit the `trigger_keywords` list in the SKILL.md frontmatter.

**What if I'm offline when the watchdog triggers?**
The kill still executes locally. The alert message is sent when connectivity is available. The full incident is always logged to `deadclaw.log` regardless of network status.

**Does DeadClaw work on both macOS and Linux?**
Yes. The kill script handles both platforms — using `launchctl` on macOS and `systemctl` on Linux for scheduled task management.

---

## Files

```
deadclaw/
  SKILL.md                    — OpenClaw skill definition
  README.md                   — This file
  deadclaw.log                — Incident log (auto-populated)
  scripts/
    kill.sh                   — Core kill script
    watchdog.sh               — Background monitor daemon
    status.sh                 — Health report
    restore.sh                — Post-kill recovery
  ui/
    deadclaw-button.html      — WebChat kill button widget
  docs/
    clawhub-listing.md        — ClawHub product listing
    launch-post.md            — Community announcement
    iphone-shortcut-guide.md  — iOS Shortcuts setup guide
    android-widget-guide.md   — Android widget setup guide
    competitive-notes.md      — Competitive analysis (internal)
    roadmap.md                — v1–v3 roadmap
```

---

## License

MIT

---

## Links

- **ClawHub**: `openclaw skill install deadclaw`
- **GitHub**: https://github.com/Kintupercy/deadclaw
- **Issues**: https://github.com/Kintupercy/deadclaw/issues
