---
name: easyclaw-config-migration
description: Migrate settings from EasyClaw into OpenClaw by locating EasyClaw desktop/runtime config files, comparing them with ~/.openclaw/openclaw.json, and safely generating or applying a selective merge. Use when a user mentions EasyClaw, wants to copy settings/configs from EasyClaw into OpenClaw, asks where EasyClaw stores its config, or needs a migration report or backup-aware merge.
---

# EasyClaw Config Migration

Locate three config sources before making changes:

1. `~/Library/Application Support/@cfmind/easyclaw/easyclaw.json` — EasyClaw desktop UI settings
2. `~/.openclaw/easyclaw.json` — EasyClaw/OpenClaw bridge config with reusable runtime settings
3. `~/.openclaw/openclaw.json` — active OpenClaw config

Most directly reusable settings live in `~/.openclaw/easyclaw.json`. The desktop `easyclaw.json` is mostly UI state and usually does **not** map cleanly into OpenClaw.

## Workflow

### 1. Inspect and compare

Run:

```bash
python3 scripts/report_easyclaw_config.py
```

This prints:
- which files exist
- redacted summaries
- fields that can be migrated automatically
- fields that are desktop-only / no direct OpenClaw equivalent

If you only need a report, stop here and summarize the findings.

### 2. Review the migration map

Read `references/mapping.md` when deciding what should be copied automatically versus left for manual review.

Default stance:
- copy only fields with clear semantic equivalents
- do not invent mappings for desktop-only UX settings
- preserve user changes already present in `~/.openclaw/openclaw.json` unless the migration is explicitly requested

### 3. Apply a selective merge

Run:

```bash
python3 scripts/merge_easyclaw_config.py --apply
```

Behavior:
- create a timestamped backup of `~/.openclaw/openclaw.json`
- merge only supported fields from `~/.openclaw/easyclaw.json`
- print changed paths

Dry run first when practical:

```bash
python3 scripts/merge_easyclaw_config.py
```

### 4. Validate and summarize

After applying, read `~/.openclaw/openclaw.json` or use normal OpenClaw validation/status commands if needed. Summarize:
- what was migrated
- what was intentionally skipped
- where the backup was written

## Notes

- Treat tokens, secrets, and auth blobs as sensitive. Redact them in chat unless the user explicitly wants raw values.
- If only the desktop EasyClaw file exists, explain that most of it is app/window preference state and not the main OpenClaw runtime config.
- If both `~/.openclaw/easyclaw.json` and `~/.openclaw/openclaw.json` exist, prefer a selective merge over wholesale overwrite.
- Never overwrite `~/.openclaw/openclaw.json` without creating a backup first.
