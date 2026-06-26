# Changelog

All notable changes to this project will be documented in this file.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.2.5] - 2026-04-23

### Changed

- **Renamed repo and skill**: `openclaw-autoresearch` → `brainforge-autoresearch`
- SKILL.md `name` field: `autoresearch` → `brainforge-autoresearch`
- Updated README, plugin.json, and SKILL.md metadata to point at the new repo URL
- Added to the [brainforge](https://github.com/zning1994/brainforge) Claude Code plugin marketplace
- Published to ClawHub as `brainforge-autoresearch`; old slug `openclaw-autoresearch` merged in as redirect

### Compatibility

- GitHub: old URL `https://github.com/zning1994/openclaw-autoresearch` auto-redirects
- ClawHub: `openclaw skills install openclaw-autoresearch` continues to work via ClawHub slug merge/redirect
- No behavior changes to the optimizer itself

## [0.2.4] - 2026-03-29

### Fixed

- SKILL.md: `pass`/`fail` → `pass_description`/`fail_description` in LLM eval docs and examples (field names didn't match actual API)
- SKILL.md: `contains`/`not_contains` parameter documented as `value` (string) → `values` (list) to match actual usage
- SKILL.md: LLM eval table now includes required `type` and `name` fields

### Changed

- SKILL.md self-optimized via autoresearch (2 rounds: MiniMax 48.6%→68.1%, Claude 80.6%→91.7%)
- Procedure rewritten: added 3-step summary upfront, renamed steps for clarity, added actionable result-review guidance
- Example section restructured: removed "confirm target" preamble, simplified to "create eval → run → review" flow
- Added `self-eval.json` for self-optimization (dogfooding eval definition)

### Tested

- Self-optimization: Round 1 (MiniMax M2.7, 15 exp, 3 keep) and Round 2 (Claude, 15 exp, 1 keep) independently discovered same doc bugs

## [0.2.3] - 2026-03-25

### Added

- `--timeout` CLI flag to control HTTP timeout per LLM call (default: 180s)
  - Large prompts (e.g., 14KB style guides) need longer timeouts for mutation calls
  - Previously hardcoded, now user-configurable

### Changed

- Default HTTP timeout increased from 60s to 180s (was causing mutation failures on Anthropic API with large prompts)
- Timeout is now stored on the provider instance, passed through `detect_provider()`

## [0.2.2] - 2026-03-25

### Fixed

- `.gitignore`: removed incorrect entries (`.git`, `.github`), added `autoresearch-*/` and `*.baseline`
- README: added ClawHub badge and link, fixed install slug to `openclaw-autoresearch`

## [0.2.1] - 2026-03-25

### Fixed

- ClawHub security flag: changed `requires.env` (all required) to `requires.anyEnv` (any one suffices)
- Declared optional env vars `OPENAI_BASE_URL` / `OPENAI_API_BASE` in metadata

## [0.2.0] - 2026-03-25

### Fixed

- MiniMax extended thinking support — models with thinking blocks (M2.7, Claude) no longer crash the parser
- Fallback to thinking content when text block is missing (thinking exhausts `max_tokens`)
- LLM judge `max_tokens` increased from 16 to 256 (thinking models need headroom)
- Rule type field: accept both `"rule"` and `"check"` keys for backwards compatibility
- `contains`/`not_contains`: accept both `"values"` (list) and `"value"` (string)
- LLM eval fields: accept both `"pass_description"`/`"fail_description"` and `"pass"`/`"fail"`
- `test_inputs`: accept both plain strings and `{"name": ..., "input": ...}` objects
- `contains` rule now supports `"match": "all"` mode (require all values present)
- Convergence counter double-increment bug fixed
- `regex` rule now uses `re.MULTILINE` for correct `^`/`$` matching
- CJK-aware word counting in `word_count` rule (counts Chinese/Japanese/Korean characters individually)

### Added

- `--model` CLI flag to override the default model per provider
- JSON fallback: `runs_per_experiment` and `max_experiments` from eval.json used when CLI defaults unchanged
- Shared `_extract_text()` helper for Anthropic-style response parsing across all providers

### Tested

- Successfully optimized `brain-search` skill: 37.5% → 54.2% pass rate in 5 experiments with MiniMax M2.7

## [0.1.0] - 2026-03-24

### Added

- Core `autoresearch.py` script — autonomous skill prompt optimizer
  - Zero external dependencies (Python 3.9+ stdlib only)
  - LLM providers: MiniMax, OpenAI, Anthropic (auto-detect from env vars)
  - Custom endpoint support via `OPENAI_BASE_URL`
  - `--model` flag to override default model per provider
- Hybrid eval system
  - Rule-based evals: `regex`, `banned_phrases`, `word_count`, `contains`, `not_contains`
  - `contains` supports `match: "all"` and `match: "any"` modes
  - LLM-as-judge evals with binary YES/NO scoring
  - CJK-aware word counting for Chinese/Japanese/Korean text
- Experiment loop
  - Baseline measurement before any changes
  - One mutation per experiment (targeted, not bulk rewrites)
  - Automatic keep/discard based on score comparison
  - Convergence exit: 95%+ pass rate for 3 consecutive experiments
  - Budget cap via `--max-experiments`
- Output artifacts
  - `results.tsv` — tab-separated score log
  - `changelog.md` — detailed mutation history with reasoning
  - `results.json` — structured data for tooling
  - `dashboard.html` — self-contained Chart.js dashboard (opt-in via `--dashboard`)
  - `SKILL.md.baseline` — original skill backup
- `SKILL.md` — agent instructions for OpenClaw / Claude Code / Cursor / Cline
- `eval-guide.md` — practical guide for writing binary eval criteria
- Example eval configs: `weekly-report.json`, `search-skill.json`
- Compatible with `npx skills add` (Vercel Labs skills ecosystem)

[0.2.4]: https://github.com/zning1994/openclaw-autoresearch/releases/tag/v0.2.4
[0.2.3]: https://github.com/zning1994/openclaw-autoresearch/releases/tag/v0.2.3
[0.2.2]: https://github.com/zning1994/openclaw-autoresearch/releases/tag/v0.2.2
[0.2.1]: https://github.com/zning1994/openclaw-autoresearch/releases/tag/v0.2.1
[0.2.0]: https://github.com/zning1994/openclaw-autoresearch/releases/tag/v0.2.0
[0.1.0]: https://github.com/zning1994/openclaw-autoresearch/releases/tag/v0.1.0
