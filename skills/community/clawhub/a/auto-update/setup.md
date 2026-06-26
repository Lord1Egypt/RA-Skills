# Setup - Auto-Update

Read this when `~/auto-update/` does not exist or is empty. Start naturally. Keep the conversation focused on what the user wants updated and how hands-off they want it to feel.

## Your Attitude

This should feel like setting up one reliable cron-backed maintenance flow, not filling out a form. The user wants freshness without surprise.

## Priority Order

### 1. First: Pick the Fast Path

Start with the simplest mental model:
- one `openclaw cron add` job handles the recurring run
- that cron message reads `~/auto-update/` before it changes anything
- the control files decide what is allowed

If the user says "just set it up", use:
- OpenClaw mode: `auto`
- new skills default: `all-in`
- schedule: daily in local off-hours
- migration handling: pause and ask
- backups: minimal core snapshot plus per-skill folder snapshot

### 2. Then: Decide the Defaults

Get the one choice that drives future behavior:
- all-in: new skills inherit auto-update unless explicitly excluded
- all-out: new skills stay manual unless explicitly included

Then ask how OpenClaw itself should behave inside that cron flow:
- `auto`: apply when a core update is available
- `notify`: inspect and report, but do not apply
- `manual`: skip core updates entirely

### 3. Then: Calibrate the First Safe Run

Only after defaults are clear, gather:
- preferred schedule and timezone
- whether to back up only core tailoring or a broader snapshot
- whether migration changes should always pause skill updates
- whether OpenClaw updates should end with a tailored "what changed for you" review
- whether the cron should update everything allowed or run in notify-first mode

If the user approves recurring updates:
- propose the exact `openclaw cron add` entry now
- make the cron message explicitly read `~/auto-update/memory.md`, `~/auto-update/openclaw.md`, `~/auto-update/skills.md`, and `~/auto-update/migrations.md`
- apply it only after approval
- record it in `schedule.md`

### 4. Finally: Offer the Tiny Reminder Hook

If the user wants the system to remember install-time questions automatically, propose the exact AGENTS snippet from `workspace-integration.md`. Do not push broader workspace hooks unless they ask.

## What You're Saving Internally

- `memory.md`: activation notes, global defaults, and summary preferences
- `openclaw.md`: OpenClaw mode, channel, backup scope, and post-update review preferences
- `skills.md`: per-skill policy, installed version, backup pointer, and migration state
- `schedule.md`: timezone, cadence, cron job name, scheduler owner, and run mode
- `backups.md`: latest OpenClaw and skill backup paths
- `migrations.md`: pending migration questions and decisions
- `run-log.md`: compact history of checks, applies, failures, and next actions

## Early Wins

As soon as you know the defaults, offer one concrete setup path:
- "Create the daily OpenClaw cron now"
- "Keep new skills manual, but let the cron auto-update OpenClaw"
- "Set everything to daily, but let the cron pause when a skill needs migration review"

When the user chooses one of these, translate it into a real `openclaw cron add` entry immediately instead of leaving it as a future intention.
