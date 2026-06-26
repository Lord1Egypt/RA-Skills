# Changelog

## [0.3.4] - 2026-04-12

### Fixed (F-035 gap — scripts missed in 0.3.3 publish)
- `recall.js`: added headless environment detection and headless-auth setup prompt (was already in claudecode but missed in awareness-memory during F-035).
- `poll-auth.js`: updated TTL from 600s to 900s to match backend Redis TTL change.

### Changed (F-036 — shared scripts SSOT)
- All 14 shared scripts now carry a 4-line "DO NOT EDIT" header pointing to `sdks/_shared/scripts/` as the single source of truth.

## [0.3.3] - 2026-04-12

### Added (F-035 — headless device auth)
- New `scripts/headless-auth.js` CommonJS helper: zero-dep `isHeadlessEnv()` / `openBrowserSilently()` / `renderDeviceCodeBox()`. Detects SSH, Codespaces, Gitpod, no-TTY, and Linux without DISPLAY.
- `scripts/setup.js` now renders the user code inside a prominent ASCII box instead of a plain `console.log`, and gracefully skips the browser-open attempt on headless hosts. Poll timeout extended from 300s to 840s to match the backend's 900s Redis TTL.
- Users running the skill over SSH or inside Docker containers can now complete device auth by opening the URL on a second device (phone / local laptop).

### Why
- The previous flow tried `open`/`xdg-open`/`start` and just printed a one-line URL on failure. On a remote host with no browser, users couldn't tell what to do next. F-035 fixes this across all 4 SDK distribution channels (this skill, OpenClaw plugin, Claude Code plugin, setup-cli).

## [0.3.2] - 2026-04-11

Same as 0.3.1. Version bumped because 0.3.1 was already reserved on ClawHub from an earlier test publish.

## [0.3.1] - 2026-04-11

### Added
- **F-034 `_skill_crystallization_hint` surfacing**: `record.js` now caches a synthetic `crystallization` signal into `perception-cache.json` when the daemon/cloud returns `_skill_crystallization_hint`. The next `UserPromptSubmit` recall injects it into the agent context with explicit action guidance: "synthesize the similar cards into a skill and submit via `awareness_record(insights={skills:[...]})`".
- **Crystallization in `<action-required>`**: `recall.js` extends the perception action-required block with a crystallization branch so agents know exactly what to do when they see the synthetic signal.

### Spec sync
- `awareness-spec.json` synced from backend SSOT (step 5 crystallization, deprecated `skill` category).

### Compatibility
- Fully backward compatible with local daemon v0.5.13+ and v0.5.16 (perception center).
- Works in both cloud mode and local-daemon mode — the `_skill_crystallization_hint` shape is identical across both.
