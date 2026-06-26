# Changelog

All notable changes to `/depradar` are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2026-03-27

Initial production release.

### Added

**Core pipeline**
- Multi-phase parallel pipeline: registry → codebase scan → community signals
- `ThreadPoolExecutor`-based concurrency (8 workers registry, 5 workers community)
- 6-hour report cache with SHA-256 keying
- `--quick` (60s), default (180s), `--deep` (300s) timeout profiles
- `--refresh` flag to bypass cache

**Dependency file parsing** (`lib/dep_parser.py`)
- `package.json` (npm, with devDependencies support via `--all`)
- `requirements.txt` (pip, handles `==`, `>=`, `~=`, `!=` specifiers)
- `pyproject.toml` (PEP 621 `[project].dependencies`)
- `Pipfile` (Pipenv)
- `go.mod` (Go modules)
- `Cargo.toml` (Rust/crates.io)
- `Gemfile` (Ruby)
- `pom.xml` (Java/Maven)
- TOML parsing: `tomllib` (3.11+) → `tomli` → custom regex fallback

**Registry integrations**
- GitHub Releases API with changelog extraction (`lib/github_releases.py`)
  - Tries `CHANGELOG.md`, `CHANGELOG`, `HISTORY.md`, `RELEASES.md`
  - Checks multiple branches: `main`, `master`, `develop`
- npm Registry API — no auth required (`lib/npm_registry.py`)
- PyPI JSON API — no auth required (`lib/pypi_registry.py`)
- crates.io API with `User-Agent` header (`lib/crates_registry.py`)
- Maven Central Solr search API (`lib/maven_registry.py`)

**Breaking change extraction** (`lib/changelog_parser.py`)
- Pass 1: Section header detection (`## Breaking Changes`, `### ⚠ BREAKING CHANGES`)
- Pass 2: Conventional Commits (`feat!:`, `fix!:`, `BREAKING CHANGE:` footer)
- Pass 3: Keyword scan (`removed`, `renamed`, `deprecated`, `no longer`)
- Pass 4: Symbol extraction with migration note parsing
- Confidence scoring per extracted change

**Codebase impact scanning** (`lib/usage_scanner.py`, `lib/impact_analyzer.py`)
- AST-based Python scanning (high confidence)
- Regex-based JS/TS scanning (medium confidence)
- grep fallback for all other languages
- Skips: `node_modules`, `.git`, `__pycache__`, `.venv`, `dist`, `build`
- Returns file path + line number + usage text per match

**Semantic versioning** (`lib/semver.py`)
- `Version` dataclass with SemVer comparison
- Bump type detection: `major`, `minor`, `patch`
- Range parsing: `^`, `~`, `>=`, `==`, `~=`
- `latest_stable()` — skips pre-release, rc, alpha, beta versions

**Scoring** (`lib/score.py`)
- Package score: `0.35×severity + 0.25×recency + 0.30×impact + 0.10×community`
- Severity map: removed=100, renamed=80, signature_changed=70, behavior_changed=60, type_changed=50, deprecated=40, other=30
- Recency tiers: 0-7d=100, 8-14d=85, 15-30d=65, 31-60d=40, 61-90d=25, 91+d=10
- Community score: `min(100, log1p(total_signals) × 12)`
- Per-source scorers for GitHub Issues, Stack Overflow, Reddit, HN, Twitter

**Community signal sources**
- GitHub Issues search (`lib/github_issues.py`) — 2-4 queries per package
- Stack Overflow API (`lib/stackoverflow.py`) — graceful rate-limit handling
- Reddit via ScrapeCreators API (`lib/reddit_sc.py`) — ecosystem subreddit selection
- Hacker News Algolia + Firebase fallback (`lib/hackernews.py`) — notes Feb 2026 Algolia archive status
- X/Twitter via xAI Grok API (`lib/twitter_x.py`) — graceful empty list when no credentials

**Deduplication** (`lib/dedupe.py`)
- Character trigram + token Jaccard hybrid similarity
- Within-source threshold: 0.70
- Cross-source threshold: 0.40
- `cross_source_link()` links duplicate signals across sources

**Normalization** (`lib/normalize.py`)
- Min-max normalization per source
- Recency score application
- Composite score calculation

**Output formats** (`lib/render.py`)
- `compact` — rich terminal output with ANSI colours, graceful Windows degradation
- `json` — full `DepRadarReport` serialization
- `md` — complete markdown report
- `context` — minimal Claude-to-Claude snippet
- `auto_save()` → `~/Documents/DepRadar/{project}-{date}.md`

**Configuration** (`lib/env.py`)
- Config priority: `os.environ` → `.claude/depradar.env` → `~/.config/depradar/.env`
- `GITHUB_TOKEN`, `SCRAPECREATORS_API_KEY`, `XAI_API_KEY`, `STACKOVERFLOW_API_KEY`
- `--diagnose` flag shows configured vs missing keys

**CLI flags** (`scripts/depradar.py`)
- `--help`, `--version`, `--diagnose`, `--mock`
- `--emit=compact|json|md|context`
- `--depth=quick|default|deep`
- `--days=N` (default: 30)
- `--path=PATH`
- `--no-scan`, `--no-community`
- `--refresh`
- `--save`, `--save-dir=PATH`
- `--quick`, `--deep` (shorthand depth flags)
- `--all` (include devDependencies)

**Hooks**
- `SessionStart` hook (`hooks/scripts/check-config.sh`) — tips on missing `GITHUB_TOKEN`

**Infrastructure**
- `lib/cache.py` — SHA-256 keyed file cache, namespace support, TTL validation
- `lib/http.py` — stdlib-only HTTP client with retry on 5xx, immediate raise on 4xx
- `lib/ui.py` — Spinner, print_status/ok/warn/error/info, ANSI colours
- `lib/dates.py` — ISO date parsing, recency scoring, relative formatting
- `lib/schema.py` — Full dataclass hierarchy with `to_dict()`/`from_dict()`

**Tests** — 371 tests, all passing
- `test_semver.py` — version parsing, bump detection, range comparison
- `test_dates.py` — recency tiers, ISO parsing, relative formatting
- `test_cache.py` — TTL validation, namespace isolation, SHA-256 keying
- `test_schema_roundtrip.py` — dataclass serialization roundtrip
- `test_changelog_parser.py` — 4-pass extraction on real changelog fixtures
- `test_dep_parser.py` — all 8 ecosystem formats
- `test_score.py` — formula correctness, edge cases
- `test_usage_scanner.py` — AST detection, regex fallback, SKIP_DIRS
- `test_render.py` — all 4 output formats
- `test_smoke.py` — end-to-end mock pipeline

**Fixtures**
- `fixtures/github_release_stripe.json` — Stripe v8.0.0 release
- `fixtures/github_release_openai.json` — OpenAI v1.0.0 release
- `fixtures/npm_registry_stripe.json` — npm Registry response
- `fixtures/pypi_registry_openai.json` — PyPI JSON response
- `fixtures/github_issues_sample.json` — 3 Stripe v8 migration issues
- `fixtures/stackoverflow_sample.json` — 2 Stripe migration questions
- `fixtures/package_json_samples/` — sample dep files for testing

---

[1.0.0]: https://github.com/depradar/depradar-skill/releases/tag/v1.0.0
