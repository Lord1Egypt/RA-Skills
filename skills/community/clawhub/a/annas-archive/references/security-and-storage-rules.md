# Security and Storage Rules

## Required runtime defaults
- Download path: `/tmp/annas-archive-downloads`
- Base host: `annas-archive.gl`
- Allowed hosts:
  - `annas-archive.gl`
  - `annas-archive.vg`
  - `annas-archive.pk`
  - `annas-archive.gd`
  - `annas-archive.li`
  - `annas-archive.pm`
  - `annas-archive.in`
  - `annas-archive.org`

## Hard constraints
- Keep `https` only for base and download URLs.
- Block downloads when URL host is outside allowlist.
- Keep `ANNAS_SECRET_KEY` out of logs and chat replies.
- Prefer `epub` when available.
- If no book match exists, report in chat and stop.

## Workspace hygiene
- Never write downloaded files under `~/.openclaw/workspace`.
- Keep temporary artifacts under `/tmp`.
- Use `scripts/cleanup_annas_tmp.sh` to purge old downloads when needed.
