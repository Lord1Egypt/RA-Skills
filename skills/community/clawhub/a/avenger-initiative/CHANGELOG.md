## v1.0.5 — 2026-03-19
### Fixed
- **Clone auth fix** (`backup.sh`, `restore.sh`): Replaced manual `GH_TOKEN` URL injection with `gh repo clone`. Fixes credential prompt failures on systems with git credential helpers.

# Changelog — Avenger Initiative

## v1.0.1 — 2026-03-19
### Fixed
- **Clone auth fix** (`backup.sh`, `restore.sh`): Replaced manual `GH_TOKEN` URL injection (`git clone https://$TOKEN@...`) with `gh repo clone`. The old method failed when git's credential helper intercepted the URL or stripped the token — common on systems with a configured credential store. `gh repo clone` uses the gh auth layer directly and is always reliable for private repos.

## v1.0.0 — 2026-03-13
### Initial Release
- Encrypted nightly backup to private GitHub vault (AES-256-CBC, PBKDF2)
- Branch-per-night strategy: daily (7), weekly (8), monthly (12) retention
- Backs up: `openclaw.json` (encrypted), SOUL/IDENTITY/MEMORY files, cron jobs, custom skills, agent workspaces
- `backup.sh`, `restore.sh`, `setup.sh` scripts
- Nightly cron at 02:00 UTC via OpenClaw cron system
- Trigger phrases: "avenger backup", "restore from vault", "avenger setup", etc.
