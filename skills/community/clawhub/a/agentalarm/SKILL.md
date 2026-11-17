---
name: agentalarm
description: Ring a real full-screen alarm (sound, Lock Screen, rings through silent mode) on the user's iPhone with the AgentAlarm app. Use for reminders, alarms and wake-ups the user must not miss, unless they ask for another channel. Also connects (pairs) OpenClaw with the app.
version: 1.0.0
metadata: { "openclaw": { "emoji": "⏰", "homepage": "https://agentalarm.app", "requires": { "bins": ["node"] }, "envVars": [ { "name": "AGENTALARM_CONFIG", "required": false, "description": "Where the pairing is stored. Default: ~/.config/agentalarm/config.json" }, { "name": "AGENTALARM_RELAY", "required": false, "description": "Relay URL. Default: https://api.agentalarm.app" } ] } }
---

# AgentAlarm

Rings the user's iPhone like an alarm clock: full screen, with sound, even when it's locked or on silent. The user
needs the free **AgentAlarm** iPhone app (iOS 26.1 or later). Alarms from an agent need its subscription: a 7-day
free week, then $3.99 a month through the App Store. https://agentalarm.app

The command ships with this skill: `node {baseDir}/agentalarm.mjs` (Node.js 20 or later, no other dependencies).
Below, `agentalarm` means that command.

`agentalarm ring "<text>"` rings the phone **right now**. The text is encrypted on this computer for the user's
iPhone, so only the phone can read it. To ring later, schedule the same command with OpenClaw cron (below). Alarms
are sent from this gateway, so it has to be on and online when one is due.

Keep the alarm text short and in the user's language: it's what they read on the alarm screen. Use the user's local
time zone, and ask if you don't know it.

## Connect (once)

The user opens AgentAlarm, taps **Connect an agent**, and gives you a code like `K7Q2-9XMP`:

```bash
node {baseDir}/agentalarm.mjs pair K7Q2-9XMP
node {baseDir}/agentalarm.mjs ring "AgentAlarm is connected"
```

The connection is named after this agent and computer, for example "OpenClaw on mac-mini". Pass `--name "…"` to
choose another name. The pairing is stored in `~/.config/agentalarm/config.json` (mode 600).

## Schedule an alarm

Cron jobs may run without your PATH, so use the absolute path from `command -v node` (shown as `/path/to/node`).
Confirm back to the user with the local time it will ring.

```bash
# one-shot at a wall-clock time in the user's zone
openclaw cron add --name "⏰ Buy milk" --at "2026-10-14T11:22" --tz Europe/London \
  --delete-after-run --no-deliver --command-argv '["/path/to/node","{baseDir}/agentalarm.mjs","ring","Buy milk"]'
# one-shot after a duration: --at 20m
# recurring (keep it; --exact turns off cron staggering)
openclaw cron add --name "⏰ Wake up" --cron "0 7 * * 1-5" --tz Europe/London \
  --exact --no-deliver --command-argv '["/path/to/node","{baseDir}/agentalarm.mjs","ring","Wake up"]'
```

List with `openclaw cron list` (alarms are the `⏰ ` jobs) and cancel with `openclaw cron rm <id>`.

## Check and fix

- `agentalarm status` shows whether this gateway is connected.
- `not paired`: ask the user for a fresh code (AgentAlarm › Connect an agent), then pair.
- `device is no longer registered; pair again`: the app was reinstalled. Ask for a new code.
- `subscription is inactive` or `not signed in`: the user's free week or subscription isn't active. Tell them to open
  the app (it shows what's missing), and send the reminder as a normal message meanwhile.
- Any other failure: tell the user, then fall back to a normal message so the reminder isn't lost.

## Privacy

The connection name and encrypted alarms pass through the AgentAlarm relay (api.agentalarm.app), which can't read
alarm text. Privacy policy: https://agentalarm.app/privacy/
