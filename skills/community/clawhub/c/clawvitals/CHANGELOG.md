# Changelog

## [Unreleased]

## [1.4.3] — 2026-04-16

### Fixed
- Added `displayName: ClawVitals` to SKILL.md frontmatter — fixes ClawHub listing title showing as "Skill" instead of "ClawVitals"

## [1.4.2] — 2026-04-16

### Changed
- Tightened data collection instructions: now specifies exact fields to extract per command rather than "collect full output" — addresses ClawHub Instruction Scope scanner flag
- `openclaw update status` network note moved inline to that command only (not in general preamble)

## [1.4.1] — 2026-04-16

### Changed
- Skill output now starts with `ClawVitals Skill v1.4.1 🔎` header in both summary and detail formats — clearly distinguishes skill output from plugin output (which shows `ClawVitals Plugin vX.Y.Z 🔌`)

## [1.4.0] — 2026-04-16

### Added
- NC-OC-012 (Critical) — Gateway authentication not configured. Detects `gateway.loopback_no_auth` checkId — fires when the OpenClaw gateway has no bearer token set.
- NC-OC-013 (Critical) — Browser control requires gateway authentication. Detects `browser.control_no_auth` — fires when browser control is enabled with no gateway auth.
- NC-OC-014 (High) — Gateway auth token meets minimum length. Detects `gateway.token_too_short` — fires when the configured token is below OpenClaw's minimum length requirement.

### Changed
- Control count updated: 6 → 9 scored stable controls
- Control library version bumped: 1.0.0 → 1.1.0
- Removed NC-OC-001 (Webhook signing secret) — permanently deferred. The underlying OpenClaw feature (`hooks.webhooks` signing secret) is not user-configurable. No user-facing change — control was always SKIPPED.

## [1.2.0] — 2026-03-21

### Changed
- SKILL.md completely rewritten as v2 — explicit CLI commands, exact control evaluation rules, precise PASS/FAIL conditions keyed to actual `checkId` values, deterministic iMessage exception logic, explicit anti-hallucination instruction, N/A handling, graceful degradation on command failure
- Added 6 experimental controls (NC-OC-002, NC-OC-005, NC-OC-006, NC-OC-007, NC-VERS-004, NC-VERS-005) — reported separately, never affect score
- Removed telemetry, scheduling, exclusions, config commands — these are plugin-only features
- Removed network permission (`telemetry.clawvitals.io`) — skill is now zero-network
- Removed cron permission — scheduling is plugin-only
- Reduced intents to 2: `handleScan` and `handleDetail`
- Added plugin/dashboard discovery touchpoints in scan output and first-run welcome
- Updated tags: added `openclaw`, removed `anguarda`
- Repository updated to ANGUARDA/clawvitals (monorepo with skill/ and plugin/)

## [1.x] — 2026-03-19 to 2026-03-21

Pre-release development. All earlier work (v0.1.x through v1.1.2) is represented in the v1.2.0 release.
