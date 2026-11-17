# Changelog

All notable changes to this project will be documented in this file.

## [1.7.0] - 2026-09-29

### Added

- Added practical guidance for statistical inference and uncertainty, experiment and quasi-experiment design, KPI trees and guardrails, and resource-constrained option prioritization.
- Integrated the new methods into the main skill routing and the end-to-end business decision framework.

### Changed

- Updated the README capability summary and bumped the project version to `1.7.0`.

## [1.6.0] - 2026-09-24

### Added

- Added a modern, clearly attributed “Wei Liaozi” business analysis framework connecting decision definition, constraints, market comparison, segmentation, readiness, decision gates, execution, and validation.
- Added variance bridge/PVM, unit economics and contribution margin, scenario and sensitivity, and Pareto/concentration guidance.
- Expanded market research and business reporting guidance for source traceability, contextual freshness, decision implications, and evidence-based qualitative prioritization.

### Changed

- Clarified output selection, model routing, and research stopping criteria; removed universal source-age and mismatch thresholds.
- Bumped the project version to `1.6.0` across `README.md`, `SKILL.md`, and `package.json`.

## [1.5.0] - 2026-09-24

### Added

- Added `references/business-reporting.md` with guidance for executive summaries, KPI scorecards, driver analysis, WBR/MBR/QBR structures, action tracking, and report quality checks.
- Integrated business reporting guidance into `SKILL.md` and added the reference to the README project overview.

### Changed

- Bumped the project version to `1.5.0` across `README.md`, `SKILL.md`, and `package.json`.

## [1.4.0] - 2026-09-24

### Added

- Added Node.js built-in router tests for all analysis intents, tie handling, negative signals, and English keyword routing.
- Added an `npm test` script and documented the package's host-provided data and search tool requirements.

### Changed

- Updated router documentation to describe the implemented input, scoring, priority, and output behavior.
- Replaced machine-specific README and changelog links with repository-relative links.
- Made intent priorities explicit and prevented overlapping phrases from inflating intent scores.
- Rewrote the README with a clearer project overview, usage example, scenario table, repository structure, and capability boundaries.
- Bumped the project version to `1.4.0` across `README.md`, `SKILL.md`, and `package.json`.

## [1.3.0] - 2026-06-12

### Added

- Added `market_research` intent to `src/router.js`, supporting 23 keywords for market research, industry analysis, competitive analysis, and market sizing scenarios.
- Added `references/market-research.md` — a comprehensive market research reference covering: research process design, search strategy and tool usage discipline, market sizing methods (TAM/SAM/SOM, top-down, bottom-up, analogy), competitive intelligence gathering, customer research methods, industry trend tracking, cross-validation rules, and integration guidance with existing analysis frameworks.
- Added **市场调研** analysis framework (section 6) to `SKILL.md`, defining when and how to conduct market research, priority paths, and search discipline.
- Added **搜索工具使用纪律** section to `SKILL.md`, specifying when to use external search, keyword structuring, source grading, multi-round convergence, and result distillation rules.
- Added 3 new model selection rules to `SKILL.md` mapping market research scenarios to appropriate models (market + strategy, market + competitive, market + marketing).
- Added market research output structure template to `SKILL.md` covering research questions, information sources, market sizing, competitive landscape, and customer insights.
- Updated `SKILL.md` routing/references section and 参考材料 section to cross-link `references/market-research.md`.
- Updated `README.md` to reflect the new market research capability, directory listing, and usage instructions.

### Changed

- Bumped the project version to `1.3.0` across `README.md` and `package.json`.
- `buildPromptHint()` in `src/router.js` now includes a prompt hint for the `market_research` intent.

## [1.2.0] - 2026-04-20

### Added

- Added `响应语言与信息缺口规则` to `SKILL.md`, clarifying language following, missing-data handling, and conditional judgment discipline.
- Added `模型使用纪律` to `SKILL.md` so strategic and financial models stay subordinate to the main analysis flow instead of turning into framework dumping.
- Added `路由与参考材料使用` to `SKILL.md` so hosts know when to use `src/router.js` and when to read `references/router-design.md`, `references/examples.md`, and `references/metric-playbook.md`.

### Changed

- Bumped the project version to `1.2.0` across `README.md` and `package.json`.
- Strengthened `SKILL.md` so the skill now covers response language, uncertainty handling, model selection discipline, and progressive disclosure guidance more explicitly.

## [1.1.0] - 2026-04-20

### Added

- Added `src/router.js` for internal skill intent routing.
- Added `src/index.js` as the public export entry for router utilities.
- Added intent routing support for `growth_analysis`, `funnel_analysis`, `retention_analysis`, `revenue_analysis`, `efficiency_analysis`, and `business_diagnosis`.
- Added [references/router-design.md](references/router-design.md) to document the routing design and expected contract.
- Added strategic, competitive, marketing, operational, and financial analysis model guidance to [SKILL.md](SKILL.md) and [references/metric-playbook.md](references/metric-playbook.md).

### Changed

- Updated [README.md](README.md) to document the new runtime routing layer and point change history to `CHANGELOG.md`.
