# Changelog

## 2.0.1 — 2026-06-11

### Changed

- Skill description polished (secrets-safe encryption, lean modes, opt-in
  cron, staged restore) — the explicit-intent activation gate is unchanged.
  No functional changes; identical script behavior to 2.0.0.

## 2.0.0 — 2026-06-11

Complete redesign: the skill is now **the cloud layer for OpenClaw's native
backup**, and was rebuilt around the ClawHub security-scan findings of v1.1.5
(see SECURITY.md for the point-by-point map).

### Breaking

- The `full` engine is `openclaw backup create` (consistent SQLite snapshots,
  embedded manifest, multi-directory coverage) plus a lean filter. The
  `openclaw` CLI is therefore required for `backup full`.
- `full` is **lean by default**: session transcripts, Codex caches/log
  databases, `tools/`, `media/`, `logs/`, and old backups are excluded.
  `--everything` (or `config.everything=true`) restores the old behavior.
- `config.encrypt` now defaults to **true**, and encryption is **forced**
  (exit 14 rather than a warning) whenever the archive scope contains real
  secret material — detected automatically.
- The local archive store moves from `~/.openclaw/backups` to
  `~/.local/share/openclaw-backups` (`config.localDir`). Required: the native
  engine refuses output inside a source path, and v1's location made every
  new full backup swallow all previous ones.
- `cleanup` renamed to `prune`; mode `skills` folded into `workspace` (both
  aliases still work, with warnings).
- Restores are **staged by default** (new directory + printed next steps);
  in-place restores moved behind `--in-place` with typed confirmation
  (`--yes --force` for automation).

### Security (ClawHub scan remediation)

- **SQP-1**: activation narrowed to explicit OpenClaw-backup intent;
  SKILL.md adds per-action confirmation gates (config writes, first upload,
  credential storage, restore, prune, schedule creation) and an
  unattended-run policy.
- **SQP-2 (cron)**: the daily job is no longer created by default.
  Scheduling is opt-in, offered once after the first successful manual
  backup, with the exact `openclaw cron add` command and payload shown
  beforehand. The new `schedule` subcommand only prints.
- **SQP-2 (credentials)**: all provider docs now lead with least-privilege
  bucket-scoped keys in AWS named profiles or operator-managed env; the GPG
  passphrase moves to a chmod-600 passphrase file or an OpenClaw SecretRef
  (`apiKey` injected as `CLOUD_BACKUP_GPG_PASSPHRASE`); the passphrase is
  passed to gpg via file descriptor, never argv; plaintext
  `skills.entries.cloud-backup.env.*` still resolves but warns loudly on
  every run.
- Durable plaintext leftovers are structurally impossible: archives are
  built in a per-run mode-700 staging dir, removed on any exit, swept after
  hard kills. (v1 stranded unencrypted tarballs whenever a step failed
  between tar and gpg.)

### Added

- **OpenClaw secret-store integration**: `config.accessKeyRef` /
  `secretKeyRef` / `sessionTokenRef` / `passphraseRef` accept OpenClaw
  SecretRefs (`{source: env|file|exec, provider, id}` or `$NAME` templates),
  resolved against the instance's `.secrets.providers` with the gateway's own
  semantics (JSON-pointer file stores, env vars, protocolVersion-1 exec
  backends such as 1Password wrappers). Configured-but-unresolvable refs
  abort the run (exit 13/14) and show as `UNRESOLVABLE` in `status` — never a
  silent fallback to a weaker tier.
- `verify [name|--latest] [--deep]` — checksum + decrypt + listing; `--deep`
  also runs the native `openclaw backup verify` on the decrypted archive.
- Automatic post-backup verification (`config.verifyAfterBackup`, default
  `quick`: streamed decrypt + entry-count match) and post-upload HEAD
  verification (size + sha256 metadata).
- Sensitivity verdict (`refs-only` vs `secret-material`) shown in `status`
  and `--dry-run`, driving the forced-encryption policy;
  `config.excludeSecrets` to produce secret-free archives instead.
- `config.exclude` / `config.include` (state-relative globs), `--no-upload`,
  `--json`, `backup --dry-run` plan output.
- `prune --dry-run` with exact delete plan; failure-debris detection
  (plaintext leftovers, incomplete sets) in `list`/`status`/`prune`.
- Per-mode retention (count + days) — a daily `settings` run can no longer
  evict your `full` archives.
- `flock` concurrency lock, disk-space and cloud-reachability preflights,
  documented exit-code map for cron agents.
- `restore --target DIR` (staged), `--only GLOB` (selective), `--latest`;
  v1 archives remain fully restorable.
- New references: `credentials.md` (resolution chain + migration),
  `setup-flow.md` (guided, gated first-time setup).

### Deprecated (removed in v3)

- `skills.entries.cloud-backup.env.ACCESS_KEY_ID` / `SECRET_ACCESS_KEY` /
  `SESSION_TOKEN` / `GPG_PASSPHRASE` — still work, warn on every run.
- Command `cleanup`, mode `skills`.

## 1.1.5 — 2026-02

Last v1 release. See git history.
