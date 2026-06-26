# Changelog

All notable changes to gateway-guardian are documented here.

## [1.6.2] - 2026-03-24

### Fixed

- **SKILL.md: guardian.conf placeholder resolution** — added explicit table showing how to
  resolve `FALLBACK_CHANNEL` and `FALLBACK_TARGET` from conversation context before writing
  the conf file; Step 4 now clearly states placeholders must be substituted before running
- **inotify-tools install**: added non-sudo fallback and manual install prompt for
  environments without elevated permissions

---

## [1.6.1] - 2026-03-24

### Fixed

- **SKILL.md: removed hardcoded bot name** — replaced all references to '小木' with
  generic terms (`通知群`, `网关`) so the skill works correctly for any user, not just
  installations where the bot is named '小木'

---

## [1.6.0] - 2026-03-24

### Added

- **Team/staff group notifications** — optional group notification on gateway recovery
  - New `STAFF_GROUP_CHAT_ID` field in `guardian.conf` (empty by default, opt-in only)
  - New `BOT_NAME` field in `guardian.conf` — display name used in staff messages (default: `OpenClaw`)
  - Recovery message uses `BOT_NAME` so teams with custom agent names get friendly, branded notifications
  - Supported channels: Feishu (`oc_xxx`), Telegram (`-100xxx`), Discord (numeric channel id)
  - `notify_success()` calls `_send_staff_group_notify()` after owner notification; urgent alerts do NOT notify the group
  - Gracefully skipped when `STAFF_GROUP_CHAT_ID` is empty — no config change required for existing installs

- **Post-install team group setup flow** in SKILL.md
  - Installer now asks for `BOT_NAME` during setup
  - After install, AI prompts user with optional group config command (`设置小木通知群: oc_xxx` / `set guardian group: <id>`)
  - New "Set Team Group" skill section handles the config command and updates `guardian.conf`

### Changed

- `guardian.conf` template expanded with `BOT_NAME` and `STAFF_GROUP_CHAT_ID` fields (both optional, with inline format docs)
- Installation steps renumbered (Step 3 split into bot-name prompt + conf write)

### Design principles

- Default behavior unchanged: existing installs continue to work without any config update
- Staff sees human-friendly message; owner sees technical detail — two separate notification paths
- Failed/urgent alerts never reach the staff group (employees can't fix gateway crashes)

## [1.5.0] - 2026-03-16

### Reverted

- **Removed maintenance mode** (`MAINTENANCE_FLAG`, `check_maintenance()`) — introduced a new
  failure path: if maintenance mode was left on, core config monitoring silently stopped.
  The problem it solved (imprecise upgrade notifications) was cosmetic; the risk introduced
  was real. Reverted to keep the guardian simple and reliable.
- **Removed `upgrade-openclaw.sh`** — existed solely to manage maintenance mode; no longer needed.
- **Removed upgrade flag handling** in `pre-stop.sh` and `monitor_gateway_recovery()` —
  dead code without the maintenance mode that wrote the flag.
- **Removed maintenance-related language strings** from `config-lib.sh`.
- **Cleaned up SKILL.md** — removed maintenance mode and upgrade script sections.

### Principle applied

> "Don't let cosmetic improvements introduce breaking risks."
> If the old behavior was merely imperfect (not broken), keep it.
> Maintenance mode made upgrade notifications prettier but made the guardian itself fragile.

---

## [1.4.3] - 2026-03-16

### Added

- **`upgrade-openclaw.sh`** — safe upgrade script that wraps `npm install -g openclaw`
  with automatic maintenance mode management
  - Step 1: enables maintenance mode (sends 🔧 notification)
  - Step 2: runs `npm install -g openclaw@<version>`
  - Step 3: validates config (auto-rollback on failure)
  - Step 4: disables maintenance mode (triggers ⚙️ upgrade notification)
  - `trap EXIT` ensures maintenance flag is always cleaned up, even on failure
  - Usage: `bash upgrade-openclaw.sh` or `bash upgrade-openclaw.sh 2026.3.13`

- **SKILL.md**: "Upgrading OpenClaw" section now documents script-based upgrade workflow
  as the required method; direct `npm install -g openclaw` is discouraged

### Motivation

During testing (2026-03-15), manual maintenance mode was forgotten/interrupted multiple
times, causing incorrect notifications. The upgrade script eliminates human error by
making maintenance mode an intrinsic part of the upgrade process.

---

## [1.4.2] - 2026-03-15

### Fixed

- **Upgrade notification lost on process restart** — when gateway restarts during upgrade,
  config-watcher process itself gets restarted by systemd, causing the upgrade notification
  sent by `monitor_gateway_recovery()` to be lost mid-flight
- **check_maintenance()**: when maintenance mode turns OFF, now checks if `upgrade` flag
  exists in `MANAGED_RESTART_FLAG` — if so, sends deferred upgrade notification instead of
  the generic maintenance-off message
- Upgrade notification is now guaranteed to be delivered regardless of process restarts

### Result: reliable 2-notification upgrade sequence
1. 🔧 维护模式已开启 (on `touch` maintenance flag)  
2. ⚙️ 检测到 OpenClaw 升级 — 网关已自动重启 (on `rm` maintenance flag)

---

## [1.4.1] - 2026-03-15

### Fixed

- **Upgrade notification race condition** — previously required manually writing
  `echo "upgrade" > /tmp/guardian-managed-restart` before upgrading, which was
  unreliable and easily lost to timing issues
- **pre-stop.sh**: when maintenance mode is active during a clean gateway stop,
  now writes `upgrade` flag instead of sending the generic "restarting" notification
- **monitor**: upgrade flag path now correctly triggers `_MSG_UPGRADE_DETECTED`
  ("检测到 OpenClaw 升级 — 网关已自动重启")

### New upgrade workflow (no manual flag needed)
```bash
touch ~/.openclaw/.guardian-maintenance   # pause monitoring
npm install -g openclaw@latest            # upgrade
rm ~/.openclaw/.guardian-maintenance      # resume → upgrade notification sent automatically
```

---

## [1.4.0] - 2026-03-15

### Added

- **Maintenance mode** (`touch ~/.openclaw/.guardian-maintenance`)
  - Pauses config monitoring during planned operations (upgrades, config edits)
  - Guardian sends a Feishu/Telegram/Discord notification when maintenance mode turns on/off
  - Monitoring resumes automatically when the file is deleted
  - Startup validation is also skipped while maintenance mode is active

- **Upgrade-aware notifications**
  - New managed restart flag type `upgrade` (write `echo "upgrade" > /tmp/guardian-managed-restart` before upgrading)
  - When gateway recovers after an upgrade, notification reads "OpenClaw upgrade detected — gateway restarted automatically" instead of the generic restart message
  - Distinguishes planned upgrade restarts from crash recovery and manual restarts

- **Maintenance mode language strings** (zh + en)
  - `_MSG_MAINTENANCE_ON` / `_MSG_MAINTENANCE_OFF` / `_MSG_MAINTENANCE_SKIPPED`
  - `_MSG_UPGRADE_DETECTED`

### Motivation

Discovered during a live OpenClaw upgrade (2026-03-15): guardian could not be stopped via
`pkill` because systemd auto-restarted it immediately. The only workaround was
`systemctl --user stop openclaw-config-watcher.service`, which required remembering the exact
service name. The maintenance flag provides a simpler, script-friendly alternative.

Also observed that guardian's gateway-restart notification used the generic "restart complete"
message even when triggered by an upgrade — making it hard to tell in chat history whether
the restart was intentional.

---

## [1.3.0] - 2026-03-08

### Added
- Dynamic session detection: finds the most recently active direct session at runtime
- `guardian.conf` fallback when session detection fails
- Bilingual support (zh/en): all notifications and log messages in both languages
- `LOCALE` setting in `guardian.conf` (auto-detected from user's conversation language)

### Changed
- Notifications now use `openclaw message send` instead of hardcoded curl calls
- SKILL.md includes `LOCALE` configuration instructions

---

## [1.2.0] - 2026-03-05

### Added
- `gateway-recovery.sh`: systemd OnFailure handler for crash recovery
- `pre-stop.sh`: ExecStopPost hook — sends "gateway restarting" notification before clean stops
- Background monitor in `config-watcher.sh`: detects gateway down→up transitions
- `MANAGED_RESTART_FLAG` coordination to avoid duplicate notifications across scripts

### Changed
- Three-layer architecture: config watcher + crash recovery + pre-stop hook

---

## [1.1.0] - 2026-03-02

### Added
- Timestamp-based config backups (`~/.openclaw/config-backups/`)
- Multi-source rollback: timestamp backups → openclaw native backups
- Lock file (`/tmp/openclaw-config.lock`) prevents concurrent config writes

---

## [1.0.0] - 2026-02-28

### Initial release
- `config-watcher.sh`: inotifywait-based config file monitor
- Auto-rollback on invalid config (JSON syntax + openclaw schema validation)
- Feishu notification on rollback success/failure
- systemd user service (`openclaw-config-watcher.service`)
