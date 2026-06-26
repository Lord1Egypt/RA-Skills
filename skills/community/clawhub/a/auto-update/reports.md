# Reports - Auto-Update

Use reports that help the user understand both the mechanics and the impact.

## Pre-Update Review

```text
Auto-update preview

OpenClaw:
- current: stable / 2026.x
- planned action: apply update after backup

Skills:
- will update: skill-a, skill-b
- paused for migration review: skill-c

Backups:
- core snapshot: yes
- per-skill backups: 2

Scheduler:
- daily trigger: openclaw cron | cron | launchd | task scheduler
```

## Post-Update Summary

```text
Auto-update summary

OpenClaw:
- updated: yes
- from -> to: 2026.x -> 2026.y

Skills:
- updated: skill-a, skill-b
- skipped: skill-c (migration review pending)

Backups:
- core snapshot saved
- skill backups saved

Next action:
- review migration note for skill-c
- optionally review OpenClaw changes for your workflow
```

## Tailored Feature Review

After OpenClaw updates, optionally add:
- what changed
- which changes matter for this user's workflow
- what to try next, always as an offer, never as an automatic rewrite
