# Changelog

## 0.1.5 - 2026-03-30

Raw-log lifecycle policy release.

### Added
- Added `cls_prune_raw_log.py` for direct deletion of `telegraph_raw_log` rows older than 30 days
- Documented the operational cron for daily raw-log pruning

### Changed
- Standardized the retention rule to keep `telegraph_raw_log` online for 30 days only, with direct deletion and no archive retention

## 0.1.4 - 2026-03-30

CLS endpoint quick-reference documentation release.

### Added
- Recorded a live `telegraphList` measurement showing `20` rows per batch and an effective single-batch span of about `21.87 minutes`

### Changed
- Updated the recommended SQLite ingest cadence from `10 minutes` to `5 minutes` based on the live window measurement
- Added a raw-log lifecycle rule: keep `telegraph_raw_log` online for `30 days`, then delete directly without archive retention

### Added
- Documented which CLS endpoints are currently usable, limited, or signature-protected
- Added recommended call path for production ingestion and detail completion

### Changed
- Synced README and API contract docs with the current endpoint strategy

## 0.1.3 - 2026-03-30

SQLite index strategy documentation release.

### Added
- Documented current index strategy for `telegraph_raw_main`
- Added query-plan verification examples for `ctime` and `level` lookups

### Changed
- Clarified duplicate-index cleanup rules and maintenance workflow
- Synced README and SQLite mode docs with the actual production index layout
- Added a CLS endpoint quick-reference table covering usable NodeAPI paths, detail resolution paths, fallback pages, and signature-protected interfaces to avoid

## 0.1.2 - 2026-03-29

Current-version documentation sync release.

### Added
- Documentation for the current raw-first SQLite source-of-truth table `telegraph_raw_main`
- Documentation for current red-record interpretation using `level in {A, B}`
- SQLite usage note showing direct `sqlite3` inspection against the local database

### Changed
- Clarified that current live record counts may exceed the original 20-item hot cache because the canonical store is now `skills/cailianpress-unified/data/telegraph.db`
- Clarified that `telegraph_raw_main` is the canonical raw record table and `v_telegraph_main` is the recommended query surface
- Synced README / SKILL docs with the current observed database structure and query workflow
- Documented the current SQLite index strategy for `telegraph_raw_main`, including `ctime` / `level` query acceleration and duplicate-index avoidance rules

## 0.1.1 - 2026-03-28

Documentation and storage update release.

### Added
- SQLite ingest mode with `telegraph_main` and `telegraph_raw_log`
- SQLite query CLI and status CLI
- Subject relationship storage
- Documentation for stable NodeAPI-based ingestion
- Documentation for current 10-minute ingest cadence

### Changed
- Switched recommended persistence model from JSONL-first to SQLite-first
- Clarified current stable direct source as `nodeapi/telegraphList`
- Clarified that `/v1/roll/get_roll_list` is signature-protected and not the current stable direct ingest path

## 0.1.0 - 2026-03-27

Initial V1 release.

### Added
- Unified CLS telegraph CLI entrypoint
- Unified service layer for telegraph, red, hot, and article queries
- Canonical schema definitions
- NodeAPI adapter for `telegraphList`
- Page fallback adapter for `cls.cn/telegraph`
- Basic article share/detail extraction
- Text and Markdown formatters
- Initial tests for schema and filter logic
- GitHub-oriented documentation (`README.md`, `SKILL.md`, `docs/api_contract.md`)

### Notes
- Primary source is `https://www.cls.cn/nodeapi/telegraphList`
- Canonical red rule is `level in {A, B}`
- `pytest` execution still depends on the target environment having `pytest` installed
