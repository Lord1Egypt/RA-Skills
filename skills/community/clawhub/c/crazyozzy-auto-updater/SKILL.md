---
name: auto-updater
description: "Automatically update OpenClaw and installed skills on a schedule. Use when setting up or maintaining daily/weekly update automation, checking for OpenClaw updates, updating all skills, and sending a summary of what changed."
metadata: {"version":"1.0.1","openclaw":{"emoji":"🔄","os":["darwin","linux"]}}
---

# Auto-Updater Skill

Keep OpenClaw and installed skills up to date with a scheduled update routine.

## What It Does

This skill helps set up an automated job that:

1. Updates **OpenClaw** itself
2. Updates installed skills via **ClawHub**
3. Sends a concise summary of what changed

## Preferred OpenClaw Approach

For current OpenClaw versions, prefer the **cron tool / scheduler** over legacy `clawbot` / `clawdbot` CLI examples.

Use an **isolated scheduled agent turn** that:

1. Runs `openclaw update` (or `openclaw update --dry-run` for preview-only flows)
2. Runs `clawhub update --all`
3. Optionally runs `openclaw doctor` if the update flow reports config/service issues
4. Sends a short summary back to the user

## Core Commands

### OpenClaw updates

Preferred command:

```bash
openclaw update
```

Useful variants:

```bash
openclaw update status
openclaw update --dry-run
openclaw update --json
openclaw doctor
```

Notes:

- `openclaw update` is the current first-class update path.
- On source installs it handles the safe update flow.
- On package-manager installs it uses the package-manager-aware update path.
- `openclaw doctor` is the follow-up health/fix command, not the main updater.

### Skills

```bash
clawhub update --all
clawhub list
```

## Scheduling Guidance

When asked to configure automatic updates in OpenClaw:

- Prefer the **cron tool** instead of legacy CLI `openclaw cron add` / `clawdbot cron add` examples.
- Create an **isolated** scheduled run.
- Deliver a concise summary to the user.
- If the user does not specify a time, ask once and pick a quiet hour in the user’s timezone.

## Suggested Scheduled Task Prompt

Use a prompt along these lines for the scheduled run:

```text
Run the scheduled OpenClaw maintenance routine:

1. Check/update OpenClaw with `openclaw update`
2. Update installed skills with `clawhub update --all`
3. If update output suggests config or service problems, run `openclaw doctor`
4. Summarize:
   - whether OpenClaw changed
   - which skills updated
   - any failures or manual follow-up needed

Keep the final report concise and user-facing.
```

## Summary Format

Preferred shape:

```text
🔄 Auto-update complete

OpenClaw: updated / already current / failed
Skills updated: ...
Issues: none / short list
```

Keep it scan-friendly:

- version changes if known
- updated skills grouped together
- errors surfaced clearly
- avoid long raw logs

## Manual Checks

```bash
openclaw update status
openclaw status
clawhub list
```

## Troubleshooting

### Update failed

Check:

1. `openclaw update status`
2. `openclaw doctor`
3. `openclaw gateway status`
4. `clawhub list`

### Skills failed to update

Common causes:

- network failure
- registry/package resolution issue
- local file modifications in installed skill
- permission issues on the workspace

Try targeted repair:

```bash
clawhub update --all --force
```

Or update one skill explicitly.

## Legacy Translation Notes

If older instructions mention these commands, translate them as follows:

- `clawdbot` / `clawbot` → `openclaw`
- `clawdhub` → `clawhub`
- `clawdbot doctor` as updater → usually `openclaw update`, with `openclaw doctor` as follow-up diagnostics
- legacy CLI cron examples → OpenClaw cron tool / scheduler jobs

## Resources

- OpenClaw update docs: `docs/cli/update.md` in the local OpenClaw install
- OpenClaw doctor / status / gateway docs in local OpenClaw docs
- ClawHub CLI skill for installing/updating skills
