# Changelog

## [2.0.0] - 2026-03-18

### Breaking Changes
- **Auto-promotion removed.** `count:3+` now stages to `.learnings/promotion-queue.md` instead of auto-writing to instruction files. Human approval required before any promotion.

### Added
- **Promotion queue** (`.learnings/promotion-queue.md`) — staged candidates with source, evidence, proposed rule, and approval status
- **Source labels** (`source:agent`, `source:user`, `source:external`) — injection defense; external entries blocked from promotion
- **Severity field** (`severity:low|medium|high|critical`) — critical entries trigger immediate review at count:1
- **Prevention tracking** (`prevented:N`) — loop closure; tracks whether recalled learnings changed behavior
- **Structured IDs** (`id:ERR-YYYYMMDD-NNN`, `id:LRN-YYYYMMDD-NNN`) — stable dedup by ID, fallback to keyword grep
- **Detail files** (`.learnings/details/`) — optional linked markdown for complex failures
- **Expiry field** (`expires:YYYY-MM-DD`) — optional staleness control with quarterly revalidation
- **install.sh** — creates all v2 directories and files (replaces setup.sh, which now delegates)
- **review.sh v2** — pending promotions, stale entries, expired entries, source distribution, prevention stats
- **references/** — design tradeoffs, detail template, promotion queue format
- **README.md**, **LICENSE** (MIT), **CHANGELOG.md**, **.gitignore**

### Changed
- Author attribution: Don Zurbrick (was Zye)
- Comparison table moved to `references/design-tradeoffs.md` and reframed as design tradeoffs
- Version bumped to 2.0.0

### Backward Compatibility
All new fields are optional. Existing v1 one-line entries (`[date] CATEGORY | what | action | count:N`) continue to work without modification.

## [1.0.0] - 2026-03-05

### Added
- Initial release
- One-line format for errors, learnings, and wishes
- grep-based dedup
- Auto-promotion at count:3+
- Pre-flight review checklist
- setup.sh and review.sh scripts
