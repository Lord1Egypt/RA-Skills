# Changelog

All notable changes to the docker-ops skill will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/).

## [0.4.0] - 2026-03-20

### Security
- All docker commands wrapped with `timeout 30` to prevent hanging on unresponsive proxy
- Added 168h (7 days) maximum period cap for log queries — prevents resource exhaustion
- Added restart cooldown: same container cannot be restarted more than once per 5 minutes
- Added audit logging for restart operations (`[AUDIT]` format with timestamp and container name)

### Changed
- SKILL.md: restart procedure now includes cooldown check and audit log step
- container-report.sh: period capped at 168h with user warning
- docker-commands.md: restart example updated with retry loop

## [0.3.0] - 2026-03-20

### Security
- container-report.sh now validates container name against whitelist before executing any Docker commands
- container-report.sh now requires `SYSCTL_WHITELIST_PATH` env var — exits with error if not set
- Added input validation for `SINCE` time period parameter (must match `<number>(s|m|h)`)
- Added log output sanitization guidance — mask tokens, passwords, connection strings before displaying
- Expanded env var redaction filter to cover `CREDENTIALS`, `AUTH`, `API_KEY`, `PASSPHRASE`, `PRIVATE`, `DSN`, `DATABASE_URL`, `CONNECTION_STRING`

### Fixed
- Logs are now fetched once and counted locally instead of calling docker logs twice per report
- Added `--tail 5000` limit to log counting commands to prevent resource exhaustion on long periods
- Fixed broken/duplicated text at end of SKILL.md (line 139 artifact)
- Fixed contradictory DOCKER_HOST guidance — now consistently says do NOT guess, report to user
- Fixed typo: "Recomendation" → "Recommendation"
- Removed whitelist.yml fallback from README.md to match SKILL.md (no fallback policy)

### Changed
- Restart verification now retries 3 times (every 10s, up to 30s total) instead of single hardcoded `sleep 10`
- Added `docker ps -a --format json` to allowed commands table for stopped container diagnostics
- Unified response language to English in SKILL.md whitelist error messages

## [0.2.0] - 2026-03-19

### Changed
- Whitelist path is now configurable via `SYSCTL_WHITELIST_PATH` environment variable
- Falls back to `whitelist.yml` in workspace root if env var is not set
- All agent configuration files converted to English

### Added
- README.md with full skill documentation
- LICENSE (MIT)
- CHANGELOG.md

## [0.1.0] - 2026-03-19

### Added
- Initial skill implementation
- SKILL.md with report, restart, and log procedures
- Whitelist-based container access control
- docker-commands.md reference
- container-report.sh automation script
- Allowed commands: ps, inspect, stats, logs, restart
- Forbidden commands enforcement
