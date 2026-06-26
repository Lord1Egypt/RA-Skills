# export-safety

## Before any external publish/export
Check whether the payload contains:
- `.git/`
- virtual environments (`.venv*`, `venv/`)
- local logs and caches
- memory files
- audit logs
- absolute paths
- plaintext credentials
- unrelated project files

## Recommended event
When the check is completed, log:
- `kind=export_safety_check`
- publish scope
- whether the export set is clean
- excluded paths
- notes about anything suspicious found
