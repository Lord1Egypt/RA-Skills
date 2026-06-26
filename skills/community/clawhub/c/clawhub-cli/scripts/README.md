# Scripts

This folder contains optional helpers for running common `clawhub` workflows.

## Design Principles

- **Safe by default**: scripts should not delete data or hide failures.
- **Portable**: prefer `bash` with `set -euo pipefail`.
- **Non-assumptive flags**: when using optional CLI flags, scripts should check `clawhub <command> --help` first.

## Linux

Shell helpers live in `scripts/linux/`:

- `install-skill.sh <slug> [semver]`
- `update-skills.sh --all` or `update-skills.sh --slug <slug> [--version <semver>]`
- `publish-skill.sh <folder> <slug> <display-name> <semver> [tags_csv]`
- `sync-all.sh [--tags <tag>]... [--changelog <text>] [--bump patch|minor|major] [--dry-run]`

Make executable:

```bash
chmod +x scripts/linux/*.sh
```

## macOS

See `scripts/macos/README.md` (the Linux scripts usually work on macOS).

## Windows

No `.ps1` scripts are shipped. See:

- `reference/WINDOWS-USAGE.md`
- `scripts/windows/README.md`

