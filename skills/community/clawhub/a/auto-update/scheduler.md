# Scheduler and Timing - Auto-Update

Use the real update mechanism that matches the current OpenClaw docs and is easiest to understand.

## Default Scheduler

The default and preferred scheduler is `openclaw cron add`.

Reason:
- it is the documented OpenClaw scheduling path
- it keeps timing exact
- it delivers the result back into the product
- it avoids external scripts for the common case

Store in `schedule.md`:
- cron job name
- cron expression
- timezone
- delivery style
- whether the run is `apply` or `notify-first`

## What the Cron Job Must Do

The cron message must explicitly tell the agent to:
1. read `memory.md`, `openclaw.md`, `skills.md`, and `migrations.md`
2. inspect OpenClaw updates and respect the mode in `openclaw.md`
3. inspect skill updates and respect the per-skill rules in `skills.md`
4. back up affected core files and skill folders
5. skip blocked items
6. apply only the allowed changes
7. verify and summarize

If the user approves recurring automation, create that cron entry in the same setup flow. Do not stop at "schedule saved".

## Fallback Schedulers

Only use these if OpenClaw cron is unavailable in the user's environment:
- Linux fallback: `cron`
- macOS fallback: `launchd`
- Windows fallback: Task Scheduler

## Timing Rules

- store timezone explicitly
- separate discovery cadence from apply cadence when the user wants more caution
- keep quiet hours explicit
- do not edit cron, launchd, Task Scheduler, or OpenClaw config without approval or standing permission
- never use heartbeat as the exact daily trigger for updates
- use heartbeat only for adaptive follow-up after updates or for pending migration reminders

## Good Defaults

- daily apply around local off-hours for all-in users
- daily notify-first review for cautious users
- weekly apply for mixed-risk environments
