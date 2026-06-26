# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-03-22

### Added
- Initial release of autooptimise
- Karpathy-style autonomous benchmark-driven skill optimisation loop
- 10-task benchmark suite targeting the OpenClaw weather skill
- LLM judge scoring rubric (0–10 scale, four criteria)
- Autonomous loop agent instructions (`runner/run_experiment.md`)
- Human approval gate — no changes auto-applied in v0.1
- Experiment log (`runner/experiment_log.md`, gitignored)
- Maximum 3 iterations per run
- Decision rule: keep change if mean score improves by ≥0.5 points
- MIT licence

[Unreleased]: https://github.com/your-org/autooptimise/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/your-org/autooptimise/releases/tag/v0.1.0
