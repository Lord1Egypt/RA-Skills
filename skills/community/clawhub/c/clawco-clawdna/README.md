# ClawDNA -- Identity Backup & Sync

**ClawhHub Skill** | Version 1.0.0 | License: MIT-0

A skill that teaches your OpenClaw bot to proactively manage its own identity backups using ClawDNA.

## What this skill does

When installed, your bot will:

- **Suggest snapshots** before risky changes (upgrades, personality edits, plugin installs)
- **Warn about stale backups** when the last push is more than 24 hours old
- **Detect identity drift** when files change without a corresponding sync
- **Guide recovery** on new machines or after broken updates
- **Explain what's protected** -- which files are backed up and how secrets are handled

## Install

Upload the `skill/` folder to ClawhHub, or install from the ClawhHub registry:

```
Slug: clawdna
```

## Prerequisites

The user's machine needs the ClawDNA CLI installed:

```bash
npm install -g clawdna
clawdna init
```

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Core skill file loaded by OpenClaw -- contains all instructions and command reference |
| `README.md` | This file -- displayed on the ClawhHub listing page |

## Tags

`backup`, `sync`, `identity`, `version-control`

## Links

- [ClawDNA Repository](https://github.com/clawco-io/clawdna)
- [ClawDNA Documentation](https://github.com/clawco-io/clawdna#readme)
