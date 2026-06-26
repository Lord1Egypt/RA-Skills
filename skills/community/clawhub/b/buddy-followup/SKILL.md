---
name: buddy-followup
version: 1.0.0
description: >
  Agents say "I'll follow up" — and then forget. This skill fixes that. When you kick off a
  long-running task (sub-agent, build, API call, script), set a timer before you move on.
  When it fires, you wake up with the original context on every configured channel and actually
  deliver the update you promised. If the task isn't done yet, set another timer and keep going.
  No hardcoded IDs — channels are read dynamically from OpenClaw config.
tags:
  - async
  - timer
  - followup
  - cron
  - workflow
---

# buddy-followup

**Agents say "I'll follow up" — and then forget. This skill fixes that.**

When you kick off a long-running task and tell the user "I'll get back to you", use this to actually follow through — automatically, on every configured channel.

## Installation

Via ClawHub (recommended):
```bash
npx clawhub install buddy-followup
```

## When to Use

- You launch a sub-agent, script, build, download, or API call that takes time
- You tell the user "I'll update you when it's done" or "give me a few minutes"
- You need to check back on something after a delay

## How It Works

1. **You estimate** how long the task will take and call the script with that delay
2. **Cron jobs fire** at the given time on every configured channel (Telegram, WhatsApp, etc.)
3. **You wake up** with the task context, check status, and reply to the user
4. **Still pending?** Set another timer and keep the loop going
5. **Done?** Report results and close the loop

No hardcoded IDs — channels and targets are read dynamically from `openclaw config get` at runtime.

## Usage

```bash
bash ~/clawd/skills/buddy-followup/scripts/followup.sh <delay> "task context"
```

**Delay formats:** `30s`, `5m`, `2h`

**Examples:**
```bash
bash ~/clawd/skills/buddy-followup/scripts/followup.sh 2m "check if sub-agent finished building the API"
bash ~/clawd/skills/buddy-followup/scripts/followup.sh 10m "check if deployment completed"
bash ~/clawd/skills/buddy-followup/scripts/followup.sh 30s "verify test results are ready"
```

Run via exec tool — the script exits immediately after scheduling. No background flag needed.

## When the Follow-Up Fires

On receiving `⏰ FOLLOW-UP (<delay>): <task>`:
1. Check the task status
2. Reply directly — routes to all configured channels automatically
3. **Done** → confirm results to the user
4. **Still running** → tell the user, reset the timer:
   ```bash
   bash ~/clawd/skills/buddy-followup/scripts/followup.sh 2m "still waiting for X, checking again"
   ```

## Requirements

- OpenClaw gateway running
- At least one channel configured (Telegram with `channels.telegram.defaultTo`, or WhatsApp with `channels.whatsapp.allowFrom`)
- `openclaw` CLI available in PATH

## Notes

- Channels are discovered at runtime — adding a new channel automatically includes it
- Each timer creates one cron job per channel, deleted after firing
- The agent decides the delay — base it on realistic task completion time
