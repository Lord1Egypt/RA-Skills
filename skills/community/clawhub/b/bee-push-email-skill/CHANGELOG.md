# Changelog — bee-push-email

All notable changes to this project will be documented in this file.

## [1.5.3] - 2026-03-24

### Fix: SKILL.md frontmatter non-standard fields
- **Frontmatter simplified to OpenClaw standard schema**: removed non-standard fields (`requires`, `credentials`, `install`, `persistence`, `version`) that caused the OpenClaw parser to silently reject the SKILL.md. The parser only recognises `name`, `description`, `emoji`, and `requirements.bins`.
- **`requirements.bins`** now uses the correct field name (was `requires.binaries`): lists `python3`, `systemctl`, `openclaw`.
- **`_meta.json` cleaned**: removed non-standard extended fields (`requires`, `credentials`, `install`, `persistence`) — registry only uses `ownerId`, `slug`, `version`, `publishedAt`. Security documentation moved to SKILL.md body where it belongs.
- All extended security/install documentation remains intact in the SKILL.md body (Security & Permissions section).

---

## [1.5.2] - 2026-03-23

### Bug Fix (Critical)
- **Gateway token missing for non-root service user**: the `imap-watcher` system user has no home directory, so `openclaw agent --deliver` failed with `gateway token missing` on fresh installs. The watcher was looking for the token in `/opt/imap-watcher/.openclaw/openclaw.json` which doesn't exist.

### Changes
- **`read_openclaw_gateway_token()`** in `setup.py`: reads `gateway.auth.token` from the OpenClaw config at install time (as root), trying `$OPENCLAW_HOME`, `/root/.openclaw/openclaw.json`, and `~/.openclaw/openclaw.json`
- **`validate_config()`**: automatically reads and stores the gateway token as `openclaw_token` in `watcher.conf` (chmod 600) during install. Shows warning if not found with instructions for manual fallback.
- **`notify_openclaw()`** in `imap_watcher.py`: passes `--token <openclaw_token>` to every `openclaw agent --deliver` call. Logs `[SECURITY] WARNING` if token is missing.
- **`verify()` step [5/5]**: calls `verify_openclaw_deliver()` — a real `openclaw agent --deliver` test with the stored token. Install fails if delivery fails, ensuring the issue is caught at install time not at runtime.
- **`CONFIG_MIGRATIONS`**: added `openclaw_token` entry (v1.5.2) so existing installs get prompted to add the token via `--reconfigure`
- **`SECURITY_CRITICAL_FIELDS`**: added `openclaw_token` — watcher logs `[SECURITY] WARNING` on startup if field is absent and notifies the agent

### Upgrade Note
Existing installs are missing `openclaw_token`. The watcher will log a `[SECURITY] WARNING` on next restart and notify the agent. Run `--reconfigure` to add the token without reinstalling.

---

## [1.5.1] - 2026-03-23

### Bug Fix (Medium)
- **Auto-reply approval missing email details** (reported v1.4.1): when `auto_reply_mode: "ask"`, the agent was receiving a generic message without sender or subject, making it impossible for the user to decide whether to approve a reply.

### Changes
- **`fetch_email_metadata(uids, config)`** added to `imap_watcher.py`: uses himalaya CLI to fetch `From` and `Subject` for each new UID before calling the agent. Graceful fallback if himalaya is unavailable or fails — watcher continues with a text-only prompt.
- **`_format_email_summary(metadata)`**: formats metadata list into a readable summary string used in `false` and `true` modes.
- **`notify_openclaw(config, new_uids=None)`**: signature updated to accept new UIDs. All 3 call sites updated.
- **Enriched messages in all modes**:
  - `ask`: per-email approval block with From, Subject, UID, and explicit instruction for the agent to ask the user `"Do you want me to reply to this email from X (subject: Y)? [Yes / No]"` — only acts on confirmation
  - `false` / `true`: context block with From+Subject prepended to the notification message
- Himalaya config for metadata fetch uses a temp file cleaned up via `finally` block (same pattern as `test_himalaya` in `setup.py`)

---

## [1.5.0] - 2026-03-23

### New Features
- **4 new Telegram bot commands** to control `auto_reply_mode` directly from Telegram without SSH:
  - `/beemail_reply` — show current mode (DISABLED / ASK / ENABLED)
  - `/beemail_reply_off` — set `auto_reply_mode=false`, restarts service automatically
  - `/beemail_reply_ask` — set `auto_reply_mode=ask`, restarts service automatically
  - `/beemail_reply_on` — set `auto_reply_mode=true` with explicit security warning, restarts service
- **`set_auto_reply_mode(mode)`** in `setup.py`: updates `watcher.conf` (preserves chmod 600), calls `systemctl restart imap-watcher`, returns success/error message
- **`get_auto_reply_mode()`** in `setup.py`: reads current mode from config
- **CLI flags**: `--reply-status`, `--reply-off`, `--reply-ask`, `--reply-on` for agent use
- `/beemail_reply_on` requires explicit user confirmation before proceeding (agent must ask)

### Documentation
- README fully updated to v1.5.0: new Telegram commands section, auto-reply control section, updated config table, updated commands table, new FAQ entries
- SKILL.md updated with `/beemail_reply*` command handlers and instructions

---

## [1.4.1] - 2026-03-23

### Fix: Registry metadata mismatch (ClawHub security scanner)
- **`_meta.json` fully populated**: moved all security declarations from SKILL.md frontmatter into `_meta.json` so the ClawHub registry entry matches what the scanner reads from the files. Previously the registry showed "no install spec / no required binaries / no env vars" while SKILL.md declared all of them — causing a mismatch warning.
- Added to `_meta.json`: `requires` (binaries, optional_binaries, env_vars, privileges, platform), `credentials` (IMAP password + Telegram bot token with consent_required), `install` (type, spec, creates, downloads, network_calls, requires_user_approval, interactive_questions, uninstall), `persistence` (type, unit, restart_policy, runs_as, starts_on_boot)
- `$OPENCLAW_HOME` now explicitly declared as optional env var in registry metadata
- `/root/.openclaw/openclaw.json` search path explicitly listed under Telegram token credential

---

## [1.4.0] - 2026-03-23

### Security
- **`auto_reply_mode` replaces `allow_auto_reply`**: three explicit values instead of boolean:
  - `false` (default) — agent never replies to senders
  - `ask` — agent requests explicit user approval via Telegram before replying
  - `true` — agent decides whether to reply (least safe, use with caution)
- **Startup security check**: on every start, `imap_watcher.py` checks for missing security-critical config fields. If any are absent, logs `[SECURITY] WARNING` and notifies the OpenClaw agent to alert the user to run `--reconfigure`. Does not stop the watcher — safe defaults are applied.
- **`SECURITY_CRITICAL_FIELDS`**: versioned list of fields that trigger the startup check. Extensible for future security-sensitive config additions.
- **Unknown `auto_reply_mode` value**: if the field contains an unrecognised value, logs `[SECURITY] WARNING` and defaults to `false` (no reply).

### Changes
- `CONFIG_MIGRATIONS` updated to v1.4.0 with `auto_reply_mode` entry (replaces v1.3.0 `allow_auto_reply`)
- `ask_auto_reply()` renamed to `ask_auto_reply_mode()` with three-option interactive prompt
- `--reconfigure` now detects and migrates both old `allow_auto_reply` installs (missing field → prompts for `auto_reply_mode`)

### Upgrade Note
Existing installs missing `auto_reply_mode` will receive a `[SECURITY]` notification via the agent on next watcher restart. Run `--reconfigure` to set the value explicitly.

---

## [1.3.0] - 2026-03-23

### Bug Fix (Critical)
- **Auto-reply disabled by default**: the `--deliver` message sent to OpenClaw now explicitly instructs the agent `DO NOT reply to the sender under any circumstances` unless `allow_auto_reply: true` is set. Previously, the ambiguous instruction "analyze if important" caused OpenClaw to reply to senders automatically, exposing system activity and potentially leaking internal details.

### New Features
- **`allow_auto_reply` config field**: boolean field in `watcher.conf` controlling whether the agent may reply to email senders. Default `false` (safe). Configured interactively during install.
- **`--reconfigure` flag**: detects config fields missing from an existing install (e.g. after `clawhub update`) and asks about each one interactively without touching existing values. Run `systemctl restart imap-watcher` after.
- **`CONFIG_MIGRATIONS` system**: versioned list of new config fields with their defaults and interactive prompts. Makes future config additions self-documenting and migration-safe.

### Upgrade Note
Existing installs do **not** get `allow_auto_reply` automatically. The agent will warn the user and suggest running `--reconfigure` after updating. Until then, the watcher defaults to `false` (auto-reply disabled) at runtime via `config.get('allow_auto_reply', False)`.

---

## [1.2.1] - 2026-03-23

### Security / Compliance
- **ClawHub security scanner**: resolved all warnings by adding explicit metadata declarations to SKILL.md frontmatter
- **`requires` block**: declares required binaries (`python3`, `systemctl`, `openclaw`), optional binaries (`himalaya`, `curl`), required privileges (`root` for install only), and target platform (`Linux with systemd`)
- **`credentials` block**: declares both credentials the skill accesses — IMAP password (stored at `/opt/imap-watcher/watcher.conf`, chmod 600) and Telegram `botToken` (read from `~/.openclaw/openclaw.json`, never stored, `consent_required: true`)
- **`install` block**: declares `type: full-system`, exact paths created, external download from `github.com/pimalaya/himalaya` via `curl | tar`, network calls to `api.telegram.org` and `github.com`, and `requires_user_approval: true`
- **`persistence` block**: declares `type: systemd service`, `restart_policy: always`, `starts_on_boot: true`, and that the service runs as the dedicated non-root `imap-watcher` user
- **Security & Permissions section**: rewritten with separate tables for installed files, external downloads, and credentials accessed; explicit language about bot token usage and consent

---

## [1.2.0] - 2026-03-23

### Bug Fixes
- **`FileHandler` crash on missing log file**: replaced `logging.basicConfig()` with `_build_logger()` — creates `/var/log/imap-watcher.log` if missing, degrades gracefully to stdout-only (captured by journald) if permissions block it. Process no longer crashes at startup.
- **`.tmp` file leak in `save_state()`**: added `os.unlink(tmp)` in the `except OSError` handler — stale `.tmp` files are now cleaned up if `os.replace()` fails.
- **`IDLEUnsupported` infinite loop**: added `use_polling` flag in `idle_loop()` — once a server reports IDLE unsupported, the connection switches permanently to polling mode without retrying `client.idle()` on every cycle.
- **`uninstall.sh` hardcoded path for `unregister_commands.py`**: added `SCRIPT_DIR` via `${BASH_SOURCE[0]}` as first search candidate — script resolves correctly regardless of where OpenClaw installs the skill.

### Meta
- `_meta.json`: `publishedAt` timestamp updated to current, version bumped to 1.2.0
- `SKILL.md`: version field updated to 1.2.0

---

## [1.1.0] - 2026-03-22

### Security
- **Non-root operation** — service now runs as dedicated `imap-watcher` system user (created automatically)
- systemd unit includes `User=imap-watcher` and `Group=imap-watcher`
- `install_service()` creates user via `useradd -r`, `fix_permissions()` chowns all files
- `check_deps()` warns about running as root instead of requiring it
- `uninstall.sh` removes system user on cleanup

### Robustness
- **Exponential backoff** on reconnection: 10s → 20s → 40s → … → 300s max (5 min)
- **Health check**: forces reconnect if no IDLE response received for >10 minutes
- **Session cache**: `get_active_session()` caches result for 60 seconds (avoids spamming `openclaw sessions` on email bursts)
- **KeyboardInterrupt**: clean IMAP logout before exit

### Bug Fixes
- **Telegram command registration**: retry with exponential backoff (3 attempts) on `bot_api_request()`
- **API error logging**: logs `description` field from Telegram API when `ok == false`
- **Non-critical bot commands**: `main()` no longer fails install if command registration fails; prints BotFather instructions
- **Post-registration verification**: `--register-commands` now calls `verify_bee_commands()` to confirm

### Code Quality
- **Telegram logic extracted** to `scripts/telegram_commands.py` module
- **Clean unregister**: `scripts/unregister_commands.py` standalone script (replaces exec hack in uninstall.sh)
- **uninstall.sh**: uses `set -uo pipefail` (removed -e), added `|| true` on non-critical operations
- **`--force` flag**: reinstall without treating existing config as a warning
- **Password validation**: rejects empty passwords before installation
- **SKILL.md**: added Telegram troubleshooting section, updated triggers, reduced length with collapsible details
- Fixed file handle leak in `verify()` (`json.load(open(...))`)

---

## [1.0.4] - 2026-03-22

### Added
- Security & Permissions section in SKILL.md and README.md
- `--register-commands` flag for post-update command registration
- `version` field in SKILL.md frontmatter

---

## [1.0.3] - 2026-03-22

### Added
- Telegram bot commands auto-registration (5 commands)
- Agent command handlers in SKILL.md
- Skill trigger phrases in frontmatter

---

## [1.0.1] - 2026-03-22

### Fixed
- UUID regex parsing (replaces fragile token-split)
- Fallback without --session-id

---

## [1.0.0] - 2026-03-22

### Added
- Initial release: IMAP IDLE push, 4-stage install, systemd service, UID tracking
