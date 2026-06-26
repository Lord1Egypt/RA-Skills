# Daily Execution Order - Auto-Update

When the user approves a recurring daily run, use this exact model.

## Scheduler Choice

Use `openclaw cron add` by default.

Preferred scheduler order:
1. OpenClaw cron
2. `cron` on Linux if OpenClaw cron is unavailable
3. `launchd` on macOS if OpenClaw cron is unavailable
4. Task Scheduler on Windows if OpenClaw cron is unavailable

Heartbeat is not an acceptable replacement for this exact-time scheduler.

## Recommended Cron Shape

Use an isolated scheduled turn with a message that leaves no gaps:

```bash
openclaw cron add \
  --name "Auto-Update" \
  --cron "0 4 * * *" \
  --tz "<USER_TIMEZONE>" \
  --session isolated \
  --wake now \
  --announce \
  --message "Run the auto-update routine. Before changing anything, read ~/auto-update/memory.md, ~/auto-update/openclaw.md, ~/auto-update/skills.md, and ~/auto-update/migrations.md. Respect the modes saved there. Run openclaw update status --json. Run clawhub update --all --dry-run. Create backups. Skip blocked items. If openclaw mode is auto, run openclaw update --json. Apply only the allowed skill updates. Verify health. Write backups.md and run-log.md. Summarize updated, unchanged, skipped, and failed items."
```

## What Happens Each Day

Before running any daily update:
1. read `~/auto-update/memory.md`
2. read `~/auto-update/openclaw.md`
3. read `~/auto-update/skills.md`
4. read `~/auto-update/migrations.md`

Then run this order:
1. inspect OpenClaw update status
2. if `openclaw_mode: auto`, apply `openclaw update --json`; if `notify` or `manual`, do not apply it
3. inspect pending skill updates
4. back up the approved OpenClaw files if core may change
5. back up each skill that is allowed to update
6. skip any skill with `auto_update: no`
7. skip any skill with `migration_state: pending` or `ask-first`
8. apply updates only to the allowed skills
9. verify versions and obvious post-update health
10. write `backups.md` and `run-log.md`
11. send the summary

## Install-Time Trigger

After every new `clawhub install`, ask:
1. "Do you want a quick explanation of what this skill adds?"
2. "Should this skill auto-update with the rest, stay manual, or inherit your default?"

Write the answer to `skills.md` immediately.

## Heartbeat Role

Heartbeat may do follow-up work only:
- remind that a migration review is pending
- suggest reviewing new OpenClaw features after a core update
- re-check a failed run that already has a logged incident

Heartbeat must not be the system that fires the daily update itself.
