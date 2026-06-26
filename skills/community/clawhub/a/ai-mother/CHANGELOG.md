# AI Mother - Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- Dynamic patrol frequency (5min for active conversations, 30min baseline)
- Flexible permission handling (accepts any input format: 1, y, allow once, etc.)
- OpenCode permission prompt detection (Allow once/Allow always/Reject)
- Task completion notifications (deduplicated)
- Duplicate workdir detection and cleanup (`cleanup-duplicates.sh`)
- File locking to prevent concurrent patrol runs
- Temp file cleanup on errors
- HEARTBEAT.md configuration in setup wizard

### Fixed
- handle-owner-response.sh syntax error
- manage-patrol-frequency.sh JSON parsing
- Cron command (`remove` → `rm`)
- tmux send-keys split into two commands (message + Enter separately)
- Patrol excludes tmux wrapper PIDs

### Changed
- All documentation now in English (internationalized)
- Permission notifications show exact prompt from AI
- SKILL.md and README.md updated with all new features

## v2.0.0 - Enhanced Edition

### Added
- Auto-healing system (`auto-heal.sh`)
- Health check system (`health-check.sh`)
- Performance analytics (`analytics.py`)
- SQLite database for agent history
- Conversation tracking with 10-round limit
- Smart diagnostics (`smart-diagnose.sh`)
- TUI dashboard (`dashboard.py`)

### Changed
- Improved state tracking
- Better error detection
- Enhanced notification system

## v1.0.0 - Initial Release

### Added
- Basic patrol functionality
- Feishu DM notifications
- Process detection
- Manual intervention alerts
