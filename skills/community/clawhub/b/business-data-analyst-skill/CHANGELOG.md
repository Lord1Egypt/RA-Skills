# Changelog

All notable changes to this project will be documented in this file.

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
- Added [references/router-design.md](/d:/home/business-data-analyst-skill/references/router-design.md) to document the routing design and expected contract.
- Added strategic, competitive, marketing, operational, and financial analysis model guidance to [SKILL.md](/d:/home/business-data-analyst-skill/SKILL.md) and [references/metric-playbook.md](/d:/home/business-data-analyst-skill/references/metric-playbook.md).

### Changed

- Updated [README.md](/d:/home/business-data-analyst-skill/README.md) to document the new runtime routing layer and point change history to `CHANGELOG.md`.
