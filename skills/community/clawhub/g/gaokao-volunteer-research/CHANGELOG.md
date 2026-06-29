# Changelog

## 0.3.1 - 2026-06-14

### Added

- Added a Chinese `README.md` covering positioning, boundaries, directory structure, common prompts, CLI tooling, recommended package outputs, and validation commands.
- Linked `README.md` from `SKILL.md`.

## 0.3.0 - 2026-06-14

### Added

- Added deterministic tooling through `scripts/gaokao_toolkit.py`.
- Added the official-source seed index at `data/official-source-index.json`, covering national sources and province-level exam authority entry points.
- Added source snapshot support for official pages, PDFs, admissions charters, policy documents, exam-source entries, and metadata sidecars.
- Added table parsing support for score/rank tables, cutoff lines, undergraduate lines, junior-college lines, and admission-style tabular data from CSV, TSV, Markdown, and simple HTML tables.
- Added research-package validation for required files, source URLs, basic province/year/category consistency, and forbidden high-risk wording.
- Added static regression checks through `tests/regression-cases.json`.
- Added fixtures for score-table parsing, cutoff-table parsing, and sample package validation.
- Added `references/tooling.md` with command usage for the tool layer.
- Updated `references/test-scenarios.md` with tool-layer regression commands.

### Verified

- `index lookup --province 广东`
- `index verify --province 广东`
- `parse-table` on the Guangdong score-table fixture
- `parse-table` on the Jiangsu cutoff-line fixture
- `validate-package` on the sample package fixture
- `regression` against `tests/regression-cases.json`
- Python syntax check for `scripts/gaokao_toolkit.py`
- `SKILL.md` frontmatter parsing
- `git diff --check -- gaokao-volunteer-research`

### Boundaries

- The official-source index is a discovery seed, not proof of current-year data.
- The parser supports common simple table formats; unusual PDFs, scanned images, protected pages, CAPTCHAs, and dynamic pages still require manual handling or additional tooling.
- The skill still does not promise admission results, predict admission probability, submit official forms, or use non-public data.

## 0.2.0 - 2026-06-13

### Added

- Added explicit `Source Collection` and `Data Check` stages.
- Added triggers and workflow coverage for 高考真题、一分一段、分数换位次、本科线、专科线、批次线、院校专业信息 and policy-document collection.
- Added `templates/data-check.md`.
- Added `references/test-scenarios.md` as a durable behavior test document.

## 0.1.0 - 2026-06-08

### Added

- Created the standalone `gaokao-volunteer-research` skill.
- Added official-source-first research boundaries.
- Added `references/source-policy.md`.
- Added candidate matrix and family brief templates.
- Added a fictional sample run.
