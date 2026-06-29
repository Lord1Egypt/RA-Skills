# Changelog

## 1.0.5 (2026-06-25)

### Security
- Bump `requests` lower bound `>=2.28` → `>=2.32.4` (CVE-2024-47081 / CVE-2024-35195 / CVE-2026-25645)
- `scripts/publish.sh`: add confirmation gate before git push + ClawHub publish (no more accidental public release)

### Changed
- SKILL.md `description`: disclose actual capabilities — reads local Chrome x.com cookies (in-memory only), calls twitter-cli subprocess, auto-detects local proxy, writes local data_dir state
- Narrow bare `daily` trigger: only fires as a short command starting with `daily` (≤ 5 trailing tokens); `daily` mid-sentence no longer triggers the digest. Explicit triggers (`daily mode` / `每日模式` / `每日摘要` / `日报`) unchanged

## 1.0.4 (2026-06-23)

### Added
- X/Twitter data source support: `type: twitter` in source configs, auto-fetched by `fetch.py` using `twitter-cli` + `browser-cookie3`
- Proxy auto-detection for X/Twitter (checks common local proxy ports: ClashX 7890, Surge 6152, ShadowsocksX 1080/1087)
- Media info extraction (photo/video/animated_gif URLs) for X/Twitter items in pending.json
- `author` field on X/Twitter items with `@handle`
- Time filtering: 3-day cutoff for X/Twitter like other sources
- YAML parsing for twitter-cli output (was line-splitting before)
- Improved Simon Willison page scraping: filter out timestamp-only entries

### Fixed
- Simon Willison: time-only titles ("5:30 PM – 6:23 PM") no longer extracted as articles

## 1.0.3 (2026-06-17)

- Python pre-fetch for webfetch sources with Scrapling + trafilatura
- README improvements
- SKILL.md footer cleanup

## 1.0.2 (2026-06-15)

- Fix: output format frontmatter rendering
- Fix: scoring framework scraped from wrong path

## 1.0.1 (2026-06-13)

- Initial release on ClawHub
- 16 AI news sources
- RUND+WPS+F scoring framework
- Daily report generation