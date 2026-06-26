# Changelog

All notable changes to Agent OS skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2026-06-01

### Added
- **LICENSE**: MIT license file added (required for ClawHub distribution).
- **README.md §Why Agent OS**: Comparison table showing the value proposition (with/without).
- **SKILL.md description**: Chinese trigger words added (多Agent协作, Agent协作层, 审计发现, 上下文包, 健康视图, 飞行记录, 跨Agent交接).

### Fixed
- **README Quick Start**: Added missing `create` subcommand to upsert_finding.py example.

---

## [0.1.0] - 2026-06-01

### Added

- **SKILL.md**: Core skill definition with 6 commands, directory protocol, agent onboarding, and boundaries.
- **README.md**: Bilingual (English + Chinese) installation and usage guide.
- **_meta.json**: Machine-readable skill metadata.
- **CHANGELOG.md**: This file.
- **references/schemas.md**: JSON/Markdown schemas for findings, context packs, mission control, flight records, and experience log.
- **references/workflows.md**: Daily light check, weekly review, upgrade self-check, and MVP-scope workflows.
- **references/templates.md**: Copy-paste templates for all file types.
- **scripts/upsert_finding.py**: Create or update audit findings in `.agent-os/findings.jsonl`. Supports `--dry-run`.
- **scripts/compile_context_pack.py**: Generate context packs from workspace state. Supports `--dry-run`.
- **scripts/mission_control.py**: Generate one-page project health view. Supports `--dry-run`.

### MVP Scope

The following commands are implemented as **workflows/templates** only (no dedicated script yet):

- `record flight` — planned script for v0.2.0
- `compress decisions` — planned script for v0.2.0
- `promote learning` — planned script for v0.2.0

### Design Decisions

- File protocol root is `.agent-os/` (not `.workbuddy/memory/`) for portability.
- All data uses JSONL (for append-friendly records) or Markdown (for human-readable views).
- Zero external Python dependencies — only stdlib.
- All agents referred to generically (human, primary agent, audit agent) — no personalized names.
