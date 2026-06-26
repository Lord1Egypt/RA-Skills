# Changelog

All notable changes to the OpenClaw Correlation Plugin will be documented in this file.

## [2.1.0] - 2026-04-15

### Added

- **Correlation Stack Consolidation** — Phases 0-3 complete:
  - P0: 12 rules mapped, 51/51 contexts resolved
  - P1: `correlation-surfacing.sh` — lightweight session scanning for correlation surfacing
  - P2: HEARTBEAT.md integration (correlation surfacing every 5 heartbeats)
  - P3: 17 stub memory files created for missing contexts

### Changed

- Rule engine optimizations: batch logger, Unicode word-boundary (German umlauts + emojis), action truncation fix
- Confidence scoring: keyword count + historical accuracy weighted scoring
- Incremental scanner: mtime-based skip for unchanged sessions
- Recommendation engine: unused rules + overlapping rules detection

### Fixed

- Rule overwrite bug (dict collision → list-based accumulation)
- Cursor crash-safety (save per-session, not end-of-run)
- Action truncation (iterate all actions, not just first)

### Security

- Webhook HMAC-SHA256 + exponential backoff retry
- XSS sanitization in alerting config
- Secrets via environment variables (not hardcoded)

## [2.0.1] - 2026-03-20

### Security

- Removed legacy reference files causing false positive security alerts
- Added comprehensive security documentation to plugin code (JSDoc comments)
- Passed deep security audit (March 20, 2026)

### Changed

- Removed `src/` directory (contained only legacy reference files)
- Added "Security" section to README.md
- Removed workspace dependency from package.json for better public distribution

### Fixed

- False positive security alerts from legacy reference files that were not actually loaded by OpenClaw

### Documentation

- Added security JSDoc comments to `index.ts`
- Added "Security" section to README.md documenting audit findings
- Created this CHANGELOG.md for version tracking

## [2.0.0] - 2026-03-18

### Added

- Initial release of correlation-aware memory search plugin
- Automatic context retrieval based on configurable rules
- Debug tools for rule matching
- Comprehensive documentation and deployment guides

---

*Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)*