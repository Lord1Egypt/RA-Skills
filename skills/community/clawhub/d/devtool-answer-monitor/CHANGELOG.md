# Changelog

## Unreleased

## v0.3.0

### Added
- Added a zero-install static demo viewer under `docs/` powered by committed sample-run summaries.
- Added public benchmark stories for MinerU and Sciverse API to show concrete before-after outcomes and activation gaps.
- Added the new preferred CLI alias `python -m devtool_answer_monitor` while keeping older aliases for compatibility.

### Changed
- Renamed the public project brand to **DevTool Answer Monitor** for clearer GitHub positioning and less naming collision.
- Reworked both README front pages to lead with result images, proof links, and public benchmark stories instead of long-form explanation.
- Tightened repository metadata, documentation language, and skill homepage links around developer-tool answer monitoring.
- Added a public zero-install demo entry and tightened the repository topic set.

## v0.2.4

### Changed
- Reduced the root ClawHub skill to a read-only workflow router so shell execution is no longer requested from the main entry point.
- Declared optional environment variables and local binary requirements in `metadata.openclaw` for the root skill and `visibility-monitor`.
- Reworded quickstart and API collection guidance so users keep secrets in local environment variables instead of chat prompts.
- Aligned root and sub-skill manifest versions to `0.2.4` for the scanner-compliance republish.

## v0.2.3

### Changed
- Replaced the old logo asset with a new AI Visibility Toolkit wordmark in both SVG and PNG formats.
- Restored the logo to the top of the English and Chinese README files so the new public brand is visible at first glance.

## v0.2.2

### Changed
- Renamed the public repository and skill brand to **AI Visibility Toolkit**.
- Switched the preferred CLI entry point to `python -m ai_visibility` while keeping a legacy alias for existing automation.
- Renamed packaged sub-skills to `visibility-monitor`, `visibility-content-check`, `visibility-repair`, and `visibility-query-matrix`.
- Updated onboarding docs, playbook links, sample report titles, and ClawHub links to the new unified name.

## v0.2.1

### Added
- Added activation-focused AI visibility documentation for downloads, installs, API adoption, and agent invocation analysis.
- Added agent-readiness, developer-tool surface priority, and scientific product visibility playbooks.
- Added a Sciverse API query-pool example plus a complete Sciverse sample run with annotations, summary, metrics, and weekly report artifacts.

### Changed
- Refined the root skill and repository messaging around the AI Visibility Toolkit brand.
- Updated the skill title to a more direct user-facing promise for ClawHub discovery.
- Added copyable starter prompts, a 30-second result section, and cross-links between the repo and the companion ClawHub skill.
- Added a new Sciverse API query pool example and optional query metadata for funnel stage, target surface, and desired action.
- Upgraded summary and weekly report outputs to include funnel-stage slices and stage-aware sample data.

## v0.2.0

### Added
- Added executable monitoring workflow with raw response capture, score draft generation, structured summaries, and weekly reports.
- Added reproducible scoring rubric, annotation protocol, and JSON schemas for query pools, run summaries, and repair validation.
- Added CLI entry points for run, report, leaderboard, and validate tasks.
- Added lightweight model leaderboard outputs in CSV, Markdown, and PNG formats.
- Added sample raw artifacts, additional repair-loop case studies, issue templates, and contribution guide.

### Changed
- Upgraded README to highlight release readiness, quick demo, expected outputs, and sample artifacts.
- Expanded repository collaboration surface with templates and release notes.
