# CHANGELOG

All notable changes to this project will be documented in this file.

## [v1.1.0] - 2026-06-05

### Added
- Added `examples/` with realistic workflow examples:
  - landing page UI brief
  - SaaS dashboard build plan
  - review-to-iteration plan
- Added `references/templates/design-record-template.md`
- Added `DESIGN.md` workflow guidance for recording the current design scheme after frontend files are created or modified

### Improved
- Clarified recommended companion skill combinations:
  - `frontend-ui-pipeline`
  - `frontend-ui-pipeline` + `ui-ux-pro-max`
  - `frontend-ui-pipeline` + `frontend-design`
  - `web-design-guidelines` + `frontend-ui-pipeline`
  - full loop across planning, strategy, implementation, review, and iteration
- Expanded companion skill fallback guidance

## [v1.0.0] - 2026-06-05

### Added
- Initial public release of `frontend-ui-pipeline`
- Core workflow stages:
  - UI Brief
  - Design Direction
  - Build Plan
  - Review Plan
  - Iteration Plan
- Reusable templates under `references/templates/`
- Scenario pipelines under `references/pipelines/`:
  - landing page
  - SaaS dashboard
  - admin panel
  - mobile app
- Prompt guidance under `references/guides/prompt-help.md`
- English and Chinese project documentation:
  - `README.md`
  - `README_zh.md`
- MIT `LICENSE`

### Improved
- Refined `SKILL.md` for marketplace-style publishing
- Reduced prompt noise and improved trigger precision
- Clarified routing boundaries with related skills such as:
  - `ui-ux-pro-max`
  - `frontend-design`
  - `web-design-guidelines`
- Added explicit trigger and skip conditions
- Added formal output requirements for each workflow stage
- Added required ending behavior for each invocation
- Expanded supported audience beyond only non-frontend users

### Structured
- Reorganized references by function:
  - `references/templates/`
  - `references/pipelines/`
  - `references/guides/`
- Standardized publish-ready project structure for ClawHub / skills.sh submission

### Version status
- First formal release
- Recommended for public listing and early real-world usage
