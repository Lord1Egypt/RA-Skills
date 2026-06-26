# APM Skill — Changelog

## 1.6.0 (2026-06-20)

### Added

- **New hook**: `apm_session_start` — auto-injects APM context per chat
  type on every agent run.
  - Chat-type aware: DM gets `APM_SESSION_START.md`; groups get
    `APM_GROUP_SESSION_START.md` with privacy gate.
  - Channel-agnostic sessionKey parsing (Matrix / Telegram / Slack / Discord).
  - Group-name resolution via `memory/groups/group_names.json` (full
    key match + Matrix-specific room-only fallback).
  - Idempotent per session (cached via `bootstrapFiles`).
- **New chapter in SKILL.md**: `MEMORY.md Discipline` — explicit
  allowed/forbidden rules for what belongs in `MEMORY.md` vs other
  memory layers.
- **New chapter in SKILL.md**: `MEMORY.md Audit Checklist` — quick
  mental check whenever editing `MEMORY.md`.
- **New chapter in ADDENDUM.md**: `File Templates` — three canonical
  templates: `MEMORY.md` (lean, ≤ 50 lines), `projects/{name}.md`,
  `longterm.md` (experience index).
- **New chapter in ADDENDUM.md**: `MEMORY.md Size Audit` — line-count
  rating table and a quick-extract script (grep) for finding
  bloat candidates.
- **New chapter in HOOKS.md**: `Hook Interaction` flow diagram and
  shared conventions (mtime-based deltas, idempotency, flush-state shape).
- **Shipped hook code**: `hooks/apm_session_start/{HOOK.md,handler.js}`
  in this skill (operators can `cp -r` to install).
- **Shipped hook code**: synced `hooks/remem-flush/` and
  `hooks/precompact-remem/` from deployed state (catch up to current
  `~/.openclaw/hooks/` versions).
- **CHANGELOG.md** — this file.

### Changed

- `SKILL.md` — added new chapters; existing content unchanged.
- `ADDENDUM.md` — added new templates and audit section; existing
  content unchanged.
- `HOOKS.md` — restructured as pure overview + links (was duplicating
  per-hook content); install instructions consolidated.
- `_meta.json` — version bumped 1.5.0 → 1.6.0.

### Privacy / Channel Improvements

- All skill documentation **stripped of personal references** (agent
  name, project names, server paths, specific room IDs).
- `apm_session_start` hook explicitly documents channel support matrix
  (Matrix primary, others compatible) and Matrix-specific fallbacks
  (room-only key match) are noted as such.
- All non-English references in `apm_session_start` translated
  to English (e.g. "Progressive Disclosure Protocol",
  "Entry Gate", "First-Join Flow") to keep the skill monolingual.

### Known Limitations (unchanged)

- `MEMORY.md` is still injected by OpenClaw as a workspace bootstrap
  file in group sessions; the privacy gate is enforced by agent
  discipline until OpenClaw adds filtering.
- `chatType === 'unknown'` falls back to DM protocol + warning.

## 1.5.0 (2026-05-19)

- Initial published version.
- Two hooks: `remem-flush`, `precompact-remem`.
- Group 5-step + DM 3-layer loading protocol.
- File templates in ADDENDUM.md (group index, attention, experience).

---

## Versioning

- **Major** (1.x → 2.x) — breaking protocol change (loading flow,
  file layout, hook contract).
- **Minor** (1.5.x → 1.6.x) — additive, backward-compatible
  (new hooks, new templates, new chapters).
- **Patch** (1.6.0 → 1.6.1) — docs fixes, comment clarifications,
  no protocol change.
