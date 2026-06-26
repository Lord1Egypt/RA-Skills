# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [3.2.0] - 2026-05-11

### Added

- Modular skill structure: `SKILL.md` + `knowledge/` (patterns-es, patterns-en, vocabulary-es, vocabulary-en)
- 49 pattern detectors documented in `knowledge/` (20 ES + 29 EN)
- IDs estandarizados: `PatternES-01`–`PatternES-20`, `PatternEN-1`–`PatternEN-29`
- CI workflow: auto-publish to ClawHub on changes to `SKILL.md` or `knowledge/`
- `.clawhubignore` to control what gets published to ClawHub

### Changed

- `SKILL.md` reescrito: 6 correcciones de calidad, sección de modos de operación, principios de reescritura humana, indicadores estadísticos
- Documentación reducida: eliminados `docs/PATTERNS.md`, `docs/IMPROVEMENTS.md`, `docs/EXAMPLES.md`, `references/ai-vocabulary.md`, `references/patterns.md`
- `docs/INTEGRATIONS.md` y `README.md` actualizados: ClawHub es solo para OpenClaw; otros agentes clonan repo
- Versión sincronizada en `SKILL.md` y `package.json`

---

## [1.0.0] - 2026-02-01

### Added

- Initial project scaffold
- OpenClaw AI writing humanizer skill
- Phase 2 production-quality upgrade
- Always-on mode integration guide for SOUL.md, Claude, and ChatGPT
- ESLint v9 flat config migration
- Shared @bwise/config ESLint rules
- Humanizer CLI with core commands (score, analyze, humanize)
- Hidden unicode obfuscation detection
- Scan and compare workflows for CLI
- Humanizer integrations and examples documentation

---

## [2.1.0] - 2026-02-01

### Added

- MCP server for Claude, ChatGPT, VS Code and other MCP clients
- API server with OpenAPI spec
- 4 new patterns and 60+ vocabulary terms
- OpenAI GPT instructions configuration

### Changed

- Bumped to 2.1.0
- Fixed heading case
- Published to ClawHub

---

## [2.2.0] - 2026-02-08

### Added

- Scan with cross-file pattern hotspots
- Config-driven scan defaults and ignore controls
- Code-aware ignore mode for docs analysis
- Baseline-aware scan regression gating
- Confidence calibration and short-sample warnings
- Spanish locale selector (es default, en via --lang)
- Spanish vocabulary TIER_1/2/3, AI_PHRASES, CONNECTORS
- Spanish syllable counting (estimateSyllablesES)
- createPatterns factory with language filtering
- ES-01 to ES-10 Spanish pattern detectors
- IFSZ, HLR, connector density for Spanish
- --lang flag threading through analyzer, humanizer, workflows, CLI

### Changed

- Updated SKILL.md to v2.2.0 with 28 patterns and new vocabulary

---

## [3.0.0] - 2026-05-07

### Added

- Complete architecture refactor
- core/analyzer.js (pure data, no formatting)
- core/humanizer.js (pure data, no formatting)
- core/stats.js (text statistics engine)
- formatters/report.js, formatters/suggestions.js, formatters/scan.js, formatters/stats.js
- Spanish integration tests
- Complete usage guide (docs/GUIDE.md)
- Spanish patterns expansion design spec (ES-11 to ES-20)
- Spanish patterns expansion implementation plan (ES-11 to ES-20)
- Spanish vocabulary expansion: TIER_1 +30, TIER_3 +33, AI_PHRASES +21

### Changed

- Rewrote README for v3.0.0
- Updated SKILL.md to v3.0 bilingual (es default, en via --lang)
- Extracted constants.js as single source of truth for DEFAULT_LANG and labels
- Split patterns.js into core/patterns/{helpers,registry,en,es,index}
- Split cli.js into cli/{flags,input,renderer,commands/,index.js}

### Fixed

- ES-02 hoy-en-dia pattern to allow comma-less variant
- ES-01 description, added missing ES-02 test
- ES-04, ES-07, ES-08, ES-09, ES-10 with expanded patterns
- ES-09 duplicate removal
- ES-10 hay-que false positive
- Expanded -ido/-ada forms
- formatGroupedSuggestions empty case
- humanizeResult autofix null when no originalText
- scoreLabel duplication in utils.js
- buildSummary AI casing
- ES fixture paths to include language subdirs

---

## [3.1.0] - 2026-05-08

### Added

- ES-11 (framing), ES-12 (copula avoidance), ES-13 (pregunta retórica)
- ES-14 (hedging), ES-15 (paralelismo negativo), ES-16 (desafíos formulaicos)
- ES-17 (estructura), ES-18 (apertura artículo), ES-19 (cierre chatbot), ES-20 (clickbait)
- Fixture index.yaml as single source of truth for all fixtures
- Structured fixture directories with language subdirs

### Changed

- Moved existing txt files into language subdirs
- Moved legacy samples into structured dirs

### Fixed

- ES-17 and ES-18 trailing space in te-pattern alternation

[unreleased]: https://github.com/SitoSt/bilingual-humanicer/compare/v3.1.0...HEAD
[3.1.0]: https://github.com/SitoSt/bilingual-humanicer/compare/v3.0.0...v3.1.0
[3.0.0]: https://github.com/SitoSt/bilingual-humanicer/compare/v2.2.0...v3.0.0
[2.2.0]: https://github.com/SitoSt/bilingual-humanicer/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/SitoSt/bilingual-humanicer/compare/v1.0.0...v2.1.0
[1.0.0]: https://github.com/SitoSt/bilingual-humanicer/compare/ef05fe6...v1.0.0
