---
name: openclaw-backup
description: Create, inspect, configure, and restore self-contained backup bundles for ~/.openclaw. Use when the user wants full-state backup, backup listing, changing the default backup directory, bundle selection, or guarded restore of OpenClaw state. Public default path is ~/backups/openclaw-snapshots; private local setups can override it with config or CLI.
---

# OpenClaw Backup

Use this skill as the unified backup and restore entrypoint for `~/.openclaw`.

## Main commands

Create a backup bundle:

```bash
bash scripts/create_backup.sh
```

List existing bundles:

```bash
bash scripts/list_backups.sh
```

Show current configuration and effective values:

```bash
bash scripts/show_config.sh
```

Change the default backup directory:

```bash
bash scripts/set_backup_dir.sh /absolute/path
```

Select a bundle, audit it, extract it, and print the restore command:

```bash
bash scripts/select_and_restore.sh
```

## Bundle format

Each backup is a self-contained tar.gz bundle with this structure:

```text
occt7pkbak-YYYYMMDD-HHMMSS/
├── .openclaw/
├── restore.sh
├── manifest.txt
└── SHA256SUMS
```

The bundled `restore.sh` is the primary restore path.

## Public defaults vs local overrides

Public default path:

```bash
~/backups/openclaw-snapshots
```

Local/private setups can override that path in two ways:
- environment variable: `OPENCLAW_SNAPSHOT_DIR`
- local config file: `config.env`

## Configuration model

This skill keeps long-term local defaults in `config.env`.

Current configurable values:
- `OPENCLAW_SNAPSHOT_DIR`
- `OPENCLAW_SNAPSHOT_PREFIX`
- `OPENCLAW_SNAPSHOT_KEEP`

Priority order is:
- command-line flags
- skill config file (`config.env`)
- `OPENCLAW_SNAPSHOT_*` environment variables
- built-in defaults

Important: in the current design, values stored in `config.env` override same-name environment variables.
If you want a one-off override, prefer command-line flags such as `--out-dir`.

`show_config.sh` shows stored config values, environment values, and final effective values.

## CLI notes

Primary CLI flag for backup location:
- `--out-dir`

Compatibility alias still accepted:
- `--backup-dir`

## Safety model

- integrity verification is mandatory during restore
- symbolic links and special files are rejected
- tar entries are audited before extraction, including hard-link rejection
- dangerous target paths are rejected
- the restore target basename must match the bundled source basename, normally `.openclaw`
- the bundle is portable across environments; restore uses the current runtime target path rather than a build-time HOME lock
- do not rename the extracted bundle root before running `restore.sh`
