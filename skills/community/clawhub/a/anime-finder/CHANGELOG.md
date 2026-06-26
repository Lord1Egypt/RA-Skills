# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.0] - 2026-04-12

### Added
- **Intent normalization layer** — `scripts/intent.py` now converts raw user wording into stable `title / episode / season / latest / action / preference / confidence` fields for `workflow.py`
- **Decision contract** — `workflow.py --json` always includes top-level `intent` and `decision`, giving agents a stable surface for autonomy, confidence, and clarification decisions
- **Strong local preferences** — explicit user wording can now persist profile settings into `state/user_profile.json`, based on the tracked `state/user_profile.template.json`
- **Follow-up download status** — runtime state in `state/last_download.json` enables `刚才那个下载怎么样` and similar status queries
- **Intent replay fixtures** — fixture-driven tests now cover trigger phrases, intent parsing, decision behavior, and conversation-style workflow requests
- **Intent examples reference** — `references/intent_examples.md` documents high-signal trigger wording and non-trigger examples for future skill maintenance
- **Single-entry workflow contract** — `scripts/workflow.py --json` remains the formal public interface, with stable top-level statuses: `need_disambiguation`, `no_results`, `ready`, `queued`, `fallback_to_magnet`, and `blocked`
- **Series overrides** — `scripts/data/series_overrides.json` remains the machine-readable mapping layer for franchise-specific resolution; first entry covers `JOJO`
- **Best-result field** — workflow output continues to expose `best_result`, so agents do not need to rediscover it from `search.results[0]`

### Changed
- **Trigger surface** — rewrote `SKILL.md` frontmatter and agent docs around real user wording such as `找番`, `追更`, `最新一集`, `只要磁力`, and follow-up progress checks
- **Agent-first runtime** — `workflow.py` now accepts raw user utterances instead of assuming the caller already extracted a clean title
- **Preference-aware ranking** — workflow-level result selection now respects subtitle, resolution, file-size cap, and preferred/blocked release group preferences
- **Documentation sync** — `README.md`, `_meta.json`, and `agents/openai.yaml` now describe the current workflow-first, intent-aware behavior instead of the older title-only interface
- **Skill-first docs** — rewrote `README.md` around `workflow.py`, `SKILL.md`, install path, and compatibility wrappers instead of the old three-step CLI story
- **Compatibility CLI positioning** — `find.sh` remains supported but is now explicitly documented as a thin wrapper, not the primary interface
- **Workflow decision order** — latest-season handling now follows `series override -> Bangumi verify -> alias expansion -> search consensus`

### Fixed
- **One-question ceiling** — decision output now centralizes when clarification is required, so upper-layer agents do not improvise repeated questioning
- **Status follow-up handling** — follow-up download queries no longer require the model to reconstruct prior state from conversation alone
- **Search auto-resolution** — broad franchise queries can now auto-continue when search results show a clear consensus instead of always forcing user confirmation
- **Non-video filtering** — replay coverage now protects against manga, PDF, and game entries leaking into anime result sets
- **Episode parsing** — `Part 1-2` style titles are covered by tests to prevent regression into false single-episode matches

## [1.2.0] - 2026-04-11

### Added
- **Batch release detection** — recognizes `131-133 合集`, `01-12` range patterns and matches specified episodes within the range
- **Latest episode inference** — when no `--episode` specified, outputs `latest_episode` field in JSON
- **Nyaa 403 fallback** — retries with different browser User-Agent headers before giving up
- **Bangumi API retry** — up to 2 retries with 3s interval on network timeout
- **Download failure fallback** — transmission-daemon failure auto-falls back to cli-only magnet link output
- **API error distinction** — Bangumi API now returns `api_error` (network issue) vs `not_found` (no results)

### Fixed
- Year-like numbers (e.g. `[2023]`) no longer matched as episode numbers
- Episode filter now suggests batch search when single episode not found

## [1.1.0] - 2026-04-06

### Added
- **CLI-only magnet mode** — `--downloader cli-only` returns magnet link and torrent URL without pushing to any downloader, lets user use any BT client
- **Auto-fallback downloader chain** — unspecified `--downloader` tries: qBittorrent → transmission-daemon → magnet link output
- **transmission-daemon auto-start** — `--downloader transmission` automatically starts daemon if not running

### Changed
- **Removed qBittorrent support** — eliminated GUI dependency, Transmission daemon is now the sole downloader
- **Simplified downloader logic** — no more fallback chain; transmission-daemon auto-starts on demand
- **Removed `qbt_add.py`** — no longer needed

## [1.0.0] - 2026-04-06

### Added
- **Bangumi API identity verification** (`verify.py`) — confirm anime identity before searching resources, prevents downloading wrong shows
- **Continuous multi-dimensional scoring** — replaces step-function scoring with weighted Gaussian curves for file size, log-scale for seeders, release quality tiers (BDMV > REMUX > BDRip > WEB-DL > HDTV)
- **Smart episode filtering** — supports EP/E/第X集/SXXEXX formats with OP/ED/OST exclusion
- **qBittorrent & Transmission integration** — auto-push torrents to downloader
- **Zero external dependencies** — Python 3.8+ standard library only, no pip install needed
- **JSON output mode** — machine-readable output for AI integration
- **SKILL.md** — AI execution guide for Claude Code / OpenClaw
