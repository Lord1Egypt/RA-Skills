# Release v0.6.0 — 2026-07-05

## Codename
**Verify-then-Share** — open the previously-private specs database

## What's New

### 🎉 specs/ is now public

The `specs/` YAML directory, which used to live in a separate private repository, is now bundled with the skill release. This unlocks:

- **Transparent provenance**: every numeric spec the skill cites can be traced to its `link_status` field and underlying datasheet page
- **Community contribution**: PRs adding new chips, fixing stale fields, or upgrading `link_status` from `placeholder_*` → `verified_*` are welcome
- **Cross-verification**: a second pair of eyes catches transcription errors that one person would miss

The contribution workflow is documented in `README.md` under `## Contributing — specs/ is open` (kept out of SKILL.md by design — SKILL.md defines how the skill behaves, README.md explains how to contribute to the project).

### 🆕 Comparison-query trigger (forwarded from v0.5.4)

When the user asks a **comparison** (`对比`, `vs`, `compare`, `X 和 Y`, `spec table`, etc.):

- **Don't stop at HTML-only** — vendor product pages don't expose electrical characteristics in tables, so an L1 (HTML-only) table leaves 30-60% of cells empty
- **Auto-escalate to L2 = Tier 3c PDF** (curl + pdfplumber) for any cell still showing `not in HTML` or `[~]`
- **Pattern-match the keywords**; don't ask the user — the trigger list is in SKILL.md
- **Outcome**: ≥ 95% cell coverage instead of 41%

### 🧹 House-keeping

- Front-matter version bumped `0.5.0 → 0.6.0`
- Internal references (`v0.5.4 — added 2026-07-04`) updated to `v0.6.0 — added 2026-07-05` to match the release tag
- `related_skills: [renesas-search]` removed from front matter (`renesas-search` is `.disabled` and no longer an active skill — listing it would mislead the skill loader)
- v0.5.4's `L2 escalation offer` Step 6 block removed — the v0.6.0 comparison-query trigger already auto-escalates to PDF without asking the user, so the offer was redundant

## Round-by-round summary

| Round | What | Result |
|-------|------|--------|
| 1 | Sync SKILL.md v0.5.4 → v0.6.0 from clawhub-installed `skills/embedded-solution/SKILL.md` | 3 hunks: version bump, anti-pattern row, Step 4 trigger |
| 2 | Add `## Contributing — specs/ is Open` section to SKILL.md | 32 new lines (later relocated to README.md in v0.6.0-rc2) |
| 3 | Drop `RELEASE-v0.5.0.md`, ship `RELEASE-v0.6.0.md` | this file |
| 4 | Mirror SKILL.md + specs/ into `embedded-solution-release/` | one-shot mirror for github push |
| 5 | git tag `v0.6.0` + commit | waiting on user confirmation before push |
| 6 | v0.6.0-rc2 cleanup: remove L2 offer, remove `related_skills`, relocate Contributing to README | cleaner SKILL.md, single-source-of-truth for contribution docs |

## Tool inventory

- `git` (publish + release commit + tag)
- `sed` (front-matter rewrite)
- `python3` (precise regex-based section removal)
- `cat` (RELEASE file generation)
- `cp` (publish → release mirror)

## Verification checklist

- [x] `version:` in SKILL.md front matter = `0.6.0`
- [x] No leftover `v0.5.4` references in SKILL.md
- [x] `L2 escalation offer` removed from Step 6
- [x] `related_skills: [renesas-search]` removed from front matter
- [x] `## Contributing — specs/ is open` present in README.md (not SKILL.md)
- [x] RELEASE file matches current version
- [ ] github push — **waiting on user**