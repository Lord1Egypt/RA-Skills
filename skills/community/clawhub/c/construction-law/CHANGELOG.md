# Changelog

All notable changes to the Construction Law Skill are documented here.

🚨 = Legal accuracy change (review before relying on existing output)
✨ = New feature  |  🔧 = Maintenance  |  🐛 = Bug fix

## [2.11.5] — 2026-05-17

### 🚨 Critical fix + test hardening
- **MUST-FIX:** `_check_year_coverage` wired into all public functions (`is_sop_day`, `add_sop_days`, `sop_days_between`). Previously only called from `calc_timeline` — direct callers of the lower-level functions got silent wrong answers for uncovered years. Year-crossing within `add_sop_days` also checked.
- `is_sop_day` docstring: clarifies Saturday/Sunday semantics, ValueError on uncovered years, ad-hoc holiday caveat
- `add_sop_days(start, 0)` semantics documented
- Ad-hoc holiday (e.g. Polling Day) warning added to timeline output
- Error message uses `_HOLIDAY_JSON.name` instead of hardcoded path
- Tests: 73 → 85. New classes: `TestSaturdayDeadline`, `TestInLieuCollision`, expanded `TestOutOfRangeYear`. Golden row 9 (Saturday deadline). Property test bounds tightened.

## [2.11.4] — 2026-05-17

### 🔧 Maintenance
- Sanitised test docstrings and comments to avoid static-analysis false positives on function-call patterns in English text

## [2.11.3] — 2026-05-17

### 🔧 Maintenance
- Replaced string-grep forbidden-imports test with `ast.parse` tree-walking — catches forbidden calls regardless of whitespace/indirection, no false-positives on comments/docstrings/strings

## [2.11.2] — 2026-05-17

### 🔧 Maintenance — Trust-gap fixes
- **Title updated** to "Construction Law: FIDIC, PSSCOC, SIA & Singapore SOP Act"
- **v2.11.0 user advisory banner** added to SKILL.md top for non-SG deadline re-check (with removal-date comment: 2026-08-17)
- SKILL.md changelog backfilled with v2.10.0–v2.11.1 entries (CHANGELOG.md remained the source of truth; SKILL.md was out of sync)
- Added CLI overview (unified dispatcher `--help` output) to SKILL.md
- Tightened "No telemetry" statement: "No telemetry from skill code — the bundled scripts do not collect or transmit data. (Note: your LLM provider’s normal data handling still applies.)"
- Added "Files written" section documenting all script output paths
- Added `test_security.py` — scans all 13 scripts for forbidden imports (subprocess, socket, requests, urllib.request, http.client, importlib, pickle, marshal, os.system, exec, eval, compile)
- Added `python3 -m unittest` as recommended test runner (stdlib-only alternative to pytest)
- Updated test count to 73 (72 existing + 1 security)

## [2.11.1] — 2026-05-10

### 🚨 Legal Accuracy — Action required if you used v2.11.0
- If you ran v2.11.0's FIDIC Deadline Calculator against an AE, MY, or GB seat, the bundled holiday data for those jurisdictions was best-effort and not verified against authoritative sources. Re-check those deadlines against your jurisdiction's official gazette or equivalent before relying on them.
- v2.11.1 removes the unverified data and replaces it with a bring-your-own-holidays mechanism (see below).

### 🔧 Maintenance — Scope correction
- v2.11.0 shipped with bundled best-effort holiday data for AE, MY (federal only), and GB (England & Wales only). Verifying that data against authoritative sources for each jurisdiction was outside the maintainer's capacity, and shipping unverified holiday data in a legal-deadline tool was the wrong call.
- v2.11.1 narrows the supported surface to Singapore (gazette-verified) and adds a `--holidays-file` mechanism for users in other jurisdictions to supply their own verified data.

### ✨ Features
- **FIDIC Deadline Calculator (Singapore seat; bring-your-own-holidays for other jurisdictions)** — `fidic_deadline.py` computes contractual deadlines in three modes: `calendar` (calendar-day counting), `exclude_ph` (excludes PHs only), and `working` (excludes weekends + PHs).
- **Singapore holiday data bundled and maintained** — only SG ships out of the box, verified against eGazette / MOM source data.
- **User-supplied holiday support for non-SG seats** — use `--holidays-file` with your own jurisdiction/year-specific JSON file.
- Added `docs/holiday-file-format.md` with JSON schema, worked example, and source guidance.

### 🔧 Maintenance
- Removed bundled AE / MY / GB holiday files from the supported surface.
- Reduced golden deadline scenarios to Singapore-only cases; retained generic property tests against user-supplied holiday data.
- Added helpful CLI error for non-SG seat use without `--holidays-file`.

## [2.10.1] — 2026-05-09

### 🔧 Maintenance
- Reconciled CHANGELOG v2.8.1/v2.9.1 duplication — merged in-lieu fix into single v2.8.1 entry with explicit "this is the only version that changed in-lieu logic" note; v2.9.1 now only lists Silver Book features
- Recategorized out-of-range ValueError as 🚨 Legal Accuracy (was 🔧 Maintenance)
- Added per-year source field to `data/sg_holidays.json` (MOM gazette cite, eGazette URL, moon sighting notes)
- Added holiday names array per year in `data/sg_holidays.json`
- Attempted dynamic version resolution via `[tool.setuptools.dynamic]` in pyproject.toml — reverted in v2.11.0 (see above)

## [2.10.0] — 2026-05-09

### 🚨 Legal Accuracy
- **Out-of-range year protection:** Calculator now raises `ValueError` with a clear message when the claim date's year has no holiday data (previously silently computed using weekday-only arithmetic, producing wrong dates). Scripts using 2028+ claim dates will now fail — update `data/sg_holidays.json` with gazetted holidays first.

### 🔧 Maintenance
- Added `pyproject.toml` with optional extras (`[excel]`, `[word]`, `[all]`, `[test]`)
- Added comprehensive test suite: 57 tests across golden-file, property-based (Hypothesis), and boundary layers
- Added `data/sg_holidays.json` as the single source of truth for holiday data
- Added disclaimer injection to all generated templates (visible text + HTML comment)
- Deprecated `--add` pipe-delimited flag in delay_analysis.py; replaced with `--add-event` and `--events-csv`
- Added `CHANGELOG.md` with categorized convention (🚨 Legal Accuracy vs ✨ Features)

### ✨ Features
- (Rolled from v2.9.1) FIDIC Silver Book obligations register (33 contractor + 11 employer), notice calendar (12 entries), Excel register

## [2.9.1] — 2026-05-09

### ✨ Features
- Complete FIDIC Silver Book support: added obligations register (33 contractor + 11 employer), notice calendar (12 entries), and Excel register
- v2.9.0 had claim templates only — this completes the full Silver Book toolkit across all 4 tools

## [2.9.0] — 2026-05-09

### ✨ Features
- Added FIDIC Silver Book (EPC/Turnkey) 2017 as a fully-supported form
- Added fidic-silver obligations register (33 contractor obligations, 11 employer obligations)
- Added fidic-silver notice calendar (12 key notices)
- Excel register now produces fidic-silver sheets for obligations and notices
- Expanded full support matrix to 35 combos (7 claim types × 5 forms)

### 🔧 Maintenance
- Updated cross-references to companion skill `construction-claim-strategy` v1.5.0

## [2.8.1] — 2026-05-09

### 🚨 Legal Accuracy
- **Sunday → Monday in-lieu rule now applied automatically** under the Holidays Act 1998 s.4(2)
- Fixed missing in-lieu Mondays for 1 Jun 2026 (Vesak), 10 Aug 2026 (National Day), 9 Nov 2026 (Deepavali), and 8 Feb 2027 (CNY Day 2)
- SOP day arithmetic now derives in-lieu Mondays from gazetted Sunday holidays automatically — no manual listing needed
- **Action required:** Re-run any previously generated SOP timelines if they crossed those dates. This is the only version that changed in-lieu logic; v2.9.0+ builds on this fix without further changes to holiday handling.

## [2.8.0] — 2026-05-09

### ✨ Features
- Added FIDIC Yellow Book 2017 as a fully-supported form
- Added fidic-yellow obligations register (33 contractor obligations, 12 employer obligations)
- Excel register now produces fidic-yellow obligations sheets in addition to notices
- All new templates are edition-tagged in HTML comments and visible body
- Expanded full support matrix to 28 combos (7 claim types × 4 forms)

## [2.7.0] — 2026-05-09

### ✨ Features
- Added 6 new claim templates filling the PSSCOC + SIA gap for eot-application, variation-claim, and interim-claim
- Added full PSSCOC (7th Ed., 2014 rev. 2020) and SIA (9th Ed., 2010 rep. 2016) versions for those templates
- Edition-tagged all new templates in HTML comment header and visible body
- Interim-claim templates now dual-purpose as SOP Act s.10 payment claims with s.10(3) requirements ticked off
- Expanded full support matrix to 21 combos (7 claim types × 3 forms)

## [2.6.0] — 2026-05-09

### 🚨 Legal Accuracy
- SOP calculator now uses holiday-aware SOP day arithmetic instead of calendar-day arithmetic
- SOP timeline conceptual fix: removed misleading min/max determination and payment-due rows; replaced with single statutory deadlines and a +7-day extension note

### 🔧 Maintenance
- Argparse now rejects unsupported forms and unsupported (form, type) combinations at parse time with helpful messages
- Excel register now refuses half-empty workbooks via pre-flight coverage checks
- Version sprawl resolved with `scripts/version.py` as the single source of truth
