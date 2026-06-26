# OpenClaw Policy Contract - Auto-Update

This document defines what the local OpenClaw policy file must capture.

## Must Track

- install method: website installer, npm or pnpm global install, or source checkout
- current channel and version
- whether updates should run in `auto`, `notify`, or `manual` mode
- which OpenClaw update command the cron flow should use on this machine
- backup scope before core updates
- whether post-update feature reviews are wanted

## Core Execution Rule

Do not assume a hidden background updater.

The default core model is:
- the recurring `openclaw cron add` job runs on schedule
- that scheduled turn reads `openclaw.md`
- it checks `openclaw update status --json`
- if mode is `auto`, it applies `openclaw update --json`
- if mode is `notify`, it reports but does not apply
- if mode is `manual`, it skips core updates

This keeps OpenClaw core on the same visible path as skills: scheduled turn, explicit rules, explicit summary.

## Default Backup Set

When the user wants a minimal tailored snapshot, prefer:
- `~/.openclaw/openclaw.json`
- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `HEARTBEAT.md`
- `USER.md`
- `IDENTITY.md`
- `MEMORY.md`

Use the workspace equivalents if the user keeps these outside `~/.openclaw/workspace/`.

## Optional Backup Scope

Offer, but do not assume:
- `~/.openclaw/workspace/`
- `~/.openclaw/credentials/`

These can be larger or more sensitive, so the user should decide explicitly.
