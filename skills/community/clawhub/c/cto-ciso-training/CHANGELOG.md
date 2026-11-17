# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Documentation switched to standalone-project wording: `README-FOR-AI.md` is
  now cited as the self-contained, sole authoritative generation & maintenance
  spec of this package, and every former citation of an external or upstream
  specification was replaced with a local section reference
  (`README-FOR-AI.md` §14 for the red lines P1–P55, §15 for the acceptance
  checks, §9.1 / §9.4 for the security invariants, §1 for the scale-tier
  ladder) across `AGENTS.md`, `CONTRIBUTING.md`, `README.md`, `README.en.md`,
  `README.zh.md`, and `SECURITY.md`. Red-line numbers (P1–P55) are unchanged.
- `CONTRIBUTING.md`: the micro-tier acceptance table now expects a total file
  count of 25, matching `README-FOR-AI.md` §15 and the Project Structure tree
  in the `README` files.

## [1.0.0] - 2026-09-21

### Added

- Initial micro-tier (XS) release of the `ai-company` skill package:
  2 departments, 18 function blocks, 25 files (including the self-contained
  generation spec `README-FOR-AI.md`, an integral part of this project).
- `README-FOR-AI.md`: the self-contained generation & maintenance spec for
  this standalone package, and its sole authority — parameters, contracts,
  red lines (**§14**, P1–P55) and acceptance checks (**§15**) are all defined
  locally, with no external document required.
- `SKILL.md` as the single runtime entry point (frontmatter within the 85-line
  budget, body within the 120-line budget).
- Two department specifications under `references/departments/`:
  `governance-and-delivery.md` (8 function blocks) and
  `engineering-and-safety.md` (10 function blocks).
- `references/method-patterns.md` as the single authoritative source for code
  templates (index first, code after) and prompt frameworks.
- `references/error-codes.md` with the full four-element error-code table
  (two department prefixes plus the `SCL_` prefix, numbering gapless within
  each prefix).
- `references/scaling.md` defining tier upgrade thresholds, paths, aliases, and
  the list of forbidden privilege escalations.
- `prompts/01-implement-method.md` and `prompts/02-robustness-checks.md`, both
  `human-paste` mode with no references to internal paths.
- `scripts/self-scale.ps1` and `scripts/scaling-config.json` for tier
  evaluation and human-approved upgrades; `.scaling-state.json` recording the
  tier history (current tier: `micro`).
- `tests/test-method-patterns.py` validating the real authoritative sources
  (no inline copies) and guarding upgrade proposals against changes to
  `tests/` or the `permissions` block.
- All 13 governance and community files required at every scale tier
  (`.editorconfig` through `_meta.json`), including this changelog.
- Bilingual documentation: `README.md` and `README.en.md` (English) plus
  `README.zh.md` (Chinese), with identifiers kept untranslated.
