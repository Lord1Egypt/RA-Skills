# Changelog

## [0.3.10] - 2026-04-19

### Added — F-059/F-060 protocol updates
- Shared `skill-extraction` SSOT prompt now emits F-059 `pitfalls` +
  `verification` arrays in skill shape (via SSOT sync).
- `awareness_recall` accepts optional F-060 `hyde_hint` for client-
  side HyDE boost — CC/OpenClaw agents get 8-15pp Recall@1 lift on
  queries with large query-vs-document gap.

## [0.3.9] - 2026-04-19

### Added — F-056 SSOT wire-up (recall-friendliness guidance)
- `SKILL.md` now embeds the full shared prompt SSOT (5 slots) via
  `<!-- SHARED:... BEGIN/END -->` markers auto-synced from
  `sdks/_shared/prompts/`. ClawHub users get the same extraction
  guidance as Claude Code and OpenClaw:
  - When-to-extract / when-NOT-to-extract (envelope + greeting + noise filters)
  - Per-card scoring (novelty / durability / specificity)
  - Daemon quality gate R1-R5 (structural) + R6-R8 (recall-friendliness)
  - Skill extraction under `insights.skills[]`
- Previous `SKILL.md` only showed a trivial record example with the
  no-longer-existing `category:"architecture"`. Fixed to use a proper
  `category:"decision"` example with required scoring fields.
- `scripts/harness-builder.mjs` record-rule also carries the new
  R6-R8 guidance so local-mode hook users get the same lift.

### Compatibility
- Requires `@awareness-sdk/local@0.9.0+` for daemon-side R1-R5 enforcement.

## [0.3.8] - 2026-04-18

### Fixed — MCP `insights` arg no longer rejected as `expected object, received string`
- **Root cause**: old `mcp-stdio.cjs` declared `awareness_record.required=['action']`
  (pre-F-053) and `insights: { type: 'object' }` with strict type. When
  Claude Code's MCP client serialized a large nested `insights` payload
  on the wire, client-side Zod validation rejected the call with
  `-32602 Input validation error: [insights] expected object, received string`
  BEFORE the request ever reached the plugin's stdio bridge.
- **Fix — three layers** (aligned with `@awareness-sdk/local@0.8.0`):
  1. `mcp-stdio.cjs` schema updated to F-053 single-parameter surface:
     `awareness_record.required=['content']`, `awareness_recall.required=['query']`.
  2. `insights` no longer declares `type: 'object'` — permissive shape
     means both native object and JSON-string forms pass validation.
  3. `proxyToolCall` normalizes stringified `insights` / `items` / `tags`
     back to native form before forwarding to the daemon, so the daemon
     always receives the structured payload.
- New L1 guard `scripts/verify-mcp-stdio-schema-aligned.mjs` (in repo
  root) pins both invariants across `sdks/claudecode/mcp-stdio.cjs`
  and `sdks/awareness-memory/mcp-stdio.cjs`.
- 11 new `node:test` assertions in `sdks/claudecode/test-mcp-stdio-normalize.cjs`
  cover `tryParseJson`, `normalizeToolArgs`, and the F-053 schema shape.

### Added — F-053 single-parameter surface (recall/record)
- `awareness_recall({ query: "..." })` and `awareness_record({ content: "..." })`
  are the only parameters callers need. Legacy multi-parameter forms still
  work (marked `[DEPRECATED]` in schema descriptions) so older clients
  keep functioning during the 8-week deprecation window.
- Two new tools exposed: `awareness_mark_skill_used` and
  `awareness_apply_skill` (F-032/F-043 skill-system parity).

### Compatibility
- Requires local daemon `@awareness-sdk/local@0.8.0+` for full Phase 3
  routing + recency channel + budget-tier shaping. Older daemons still
  work but without the Phase 3 quality lift.
- No breaking change to existing callers — old argument shapes continue
  to work via deprecation path.

## [0.3.7] - 2026-04-16

### Changed
- Aligning with overall system improvements in OpenClaw plugin v0.6.9
- Awareness system now uses consistent parameters schema across all integrations
- No functional changes to scripts, but improved compatibility with latest OpenClaw versions

## [0.3.6] - 2026-04-16

### Changed
- Aligning with overall system improvements in OpenClaw plugin v0.6.9
- Awareness system now uses consistent parameters schema across all integrations
- No functional changes to scripts, but improved compatibility with latest OpenClaw versions

## [0.3.5] - 2026-04-16

### Changed
- Aligning with overall system improvements in OpenClaw plugin v0.6.9
- Awareness system now uses consistent parameters schema across all integrations
- No functional changes to scripts, but improved compatibility with latest OpenClaw versions

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
