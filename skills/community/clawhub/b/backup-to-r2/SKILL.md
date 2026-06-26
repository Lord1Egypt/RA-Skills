---
name: openclaw-backup-r2
description: Set up and run complete, encrypted, off-site backups of an OpenClaw install to Cloudflare R2 via restic, plus portable restore. Use when the user wants to back up, protect, restore, or migrate their OpenClaw config, agents, and credentials.
---

# OpenClaw Backup → Cloudflare R2 (via restic)

This skill helps the user create **complete, encrypted, off-site backups** of their OpenClaw installation and restore them on any machine. It backs up everything OpenClaw's built-in `.bak` misses: credentials, agents, workspace, and cron — not just `openclaw.json`.

## When to use

- The user wants to back up their OpenClaw setup (config, agents, credentials).
- The user lost agents/config (e.g., after `openclaw doctor --fix`) and wants protection going forward.
- The user wants to restore a backup or migrate OpenClaw to a new PC.
- The user wants automatic daily backups.

## What it backs up

`openclaw backup create --verify` produces a verified `.tar.gz` containing config, credentials, agents, workspace, and cron. `restic` then encrypts and deduplicates it locally and uploads to Cloudflare R2. Retention keeps 7 daily + 4 weekly + 6 monthly snapshots.

## Prerequisites (guide the user to set these up)

1. **restic** installed (on PATH or at `./restic/restic.exe`).
2. A **Cloudflare R2** bucket + S3 API token.
3. Copy `.env.example` → `.env` and fill `RESTIC_REPOSITORY`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`.
4. Create `.restic-pass` with a strong password. **Critical:** this is the only key to the encrypted backups — store it safely and separately. Without it, restore is impossible.
5. Initialize once: `restic init`.

> Never commit `.env` or `.restic-pass`. They are git-ignored. Never print their contents.

## Running a backup

```powershell
.\backup.ps1
```
This runs `openclaw backup create --verify`, uploads via restic to R2, prunes old snapshots, and removes the local tar. Logs go to `logs/`.

## Testing a restore (safe, non-destructive)

```powershell
.\test-restore.ps1
```
Downloads the latest snapshot, extracts it, and validates with `openclaw backup verify`. Does **not** touch the live `.openclaw`.

## Restoring (any PC) — ⚠️ destructive

Copy the `portable/` folder (with `restic/restic.exe`, `.env`, `.restic-pass`) to the target machine and run:
```powershell
.\portable\restore-portable.ps1
```
It stops the gateway, pulls the latest backup from R2, and installs to `%USERPROFILE%\.openclaw`.

> ⚠️ **This OVERWRITES the live `.openclaw`.** Anything created after the last backup is lost. The script requires the user to type `RESTAURAR` to confirm and moves the current folder to `.openclaw.backup-<date>` first (this local backup can fail if files are locked, in which case it overwrites in place). **Always have the user run `test-restore.ps1` first** to inspect the backup non-destructively, and only run the real restore when they accept replacing the active install. `$env:OPENCLAW_RESTORE_YES = 1` skips the prompt for automation — never set it on the user's behalf without explicit consent.

## Automating daily backups (Windows)

Register a Task Scheduler job that runs `backup.ps1` daily with `-StartWhenAvailable` so it catches up if the PC was off. See the README for the exact `Register-ScheduledTask` command.

## Safety notes

- Always confirm the user has saved their `.restic-pass` somewhere safe before relying on backups. It is the only key — losing it makes every backup unrecoverable.
- When helping configure, never echo secret values; have the user paste them into `.env`/`.restic-pass` themselves.
- This uploads OpenClaw secrets (credentials/auth profiles) to a third-party bucket. Encryption is client-side, but its strength depends entirely on the password. Make sure the user uses a strong passphrase, keeps the R2 bucket private, and never shares the `portable/` folder (it bundles both the R2 credentials and the decryption key).
- The restore normally preserves the existing `.openclaw` as a timestamped backup (so it is reversible) — but that safety copy can fail if files are locked. Recommend `test-restore.ps1` before any real restore.
