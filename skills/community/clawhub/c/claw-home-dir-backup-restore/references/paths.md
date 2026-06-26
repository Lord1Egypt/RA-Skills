# OpenClaw Backup — Path Policy

## OpenClaw Home

Default: `~/.openclaw`  
Override: `OPENCLAW_HOME` environment variable

## Backup strategy

The entire `~/.openclaw` directory is archived as-is — no files or subdirectories are excluded.

This guarantees that the restored machine has an exact copy of the original setup and OpenClaw
works immediately without any missing configuration, credentials, skills, or runtime state.

## Restore target

The archive preserves the `.openclaw` directory name. Extracting to `~/` reproduces `~/.openclaw`
exactly as it was on the source machine.

## Sensitive paths

The following directories contain secrets and should be stored securely:

| Path | Contents |
|---|---|
| `identity/` | Auth tokens and device identity |
| `credentials/` | API keys per service |
| `secrets/` | Encrypted secrets store |

The restore script sets `chmod 700` on these directories after extraction.
Use `--encrypt` with a GPG key for backups stored in cloud or shared drives.
