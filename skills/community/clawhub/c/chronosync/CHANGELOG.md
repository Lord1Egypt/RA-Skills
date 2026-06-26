# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.1] - 2026-03-14

### Fixed
- Fixed Windows UTF-8 encoding issue in console output
- Fixed OpenClaw 2026.3.x path compatibility (`agents/main/sessions`)
- Fixed plugin system circular import issue by extracting `plugin_base.py`

### Changed
- Updated SKILL.md with generic descriptions (removed personal references)
- Added proper metadata (version, author, license, tags)

## [1.0.0] - 2026-03-10

### Added
- Initial release
- Basic session synchronization functionality
- JSON + Markdown dual format output
- Incremental sync with hash-based change detection
- Automatic sensitive information sanitization (email, phone, API keys)
- Plugin system with knowledge and todo plugins
- Cron job support for automatic syncing
