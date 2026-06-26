# Claw Time Machine Usage Notes

## Backup location

Backups are stored in:

```bash
~/.ctm/
```

Files are named like:

```bash
openclaw-soul-YYYYMMDD-HHMMSS.tar.gz
```

Each backup archive also includes a top-level `manifest.txt` file so you can inspect what was captured without guessing.

## Recommended operator flow

### Before restore

Inspect the backup list first:

```bash
./scripts/ctm.sh list
```

Then restore by index, filename, or `latest`.

## Migration behavior

The migration flow does not assume the skill is installed on the target machine. It restores by running shell commands over SSH on the target host.

High-level sequence:

1. Create a fresh backup on the source machine
2. Copy the archive to the target machine
3. Ensure `~/.openclaw` exists on the target machine
4. Create a safety backup of target state paths if they exist
5. Remove only the preserved state paths on the target machine
6. Extract the archive into `~/.openclaw`
7. Do not automate gateway start or stop as part of this skill

If you want the copied archive removed from the target machine after a successful restore, use:

```bash
./scripts/ctm.sh migrate user@host --clean-remote-archive
```

## Safety backup behavior

Restore creates a safety backup directory like:

```bash
~/.openclaw.bak.<timestamp>/
```

This safety backup contains only the preserved state paths, not the entire OpenClaw installation.

## Non-interactive usage

Use `--force` for automation only when interactive confirmation is not desired:

```bash
./scripts/ctm.sh restore latest --force
./scripts/ctm.sh migrate root@example.com --force
```

## Archive inspection

To inspect the bundled manifest without restoring:

```bash
tar xOf ~/.ctm/openclaw-soul-YYYYMMDD-HHMMSS.tar.gz ./manifest.txt
```

## Troubleshooting

### Missing dependencies

The script checks for required tools and reports which binary is missing.


### Empty backup list

If no backups exist yet, create one with:

```bash
./scripts/ctm.sh backup
```

### Rollback after a bad restore

If the script printed a safety backup path, copy its contents back into `~/.openclaw` manually.

### Large skills directory

If `skills/` is large, backup and restore can take noticeably longer. This is expected because custom skills are part of the preserved OpenClaw state.
