# Changelog — accountability

All notable changes to this skill will be documented in this file.

## [1.0.0] — 2026-03-22

### Added
- Initial release
- Structured FOLLOWUPS.md format with mandatory fields (Verificar, Espero, Prazo, Se falhar)
- Item lifecycle: PENDENTE → DONE / FALHOU with automatic transitions
- Heartbeat cron configuration (every 2h) with self-monitoring
- Priority system (P0/P1/P2) with escalation rules
- Automatic cleanup of DONE items after 3 days with ARCHIVE.md audit trail
- Session start protocol (check FOLLOWUPS.md before any work)
- Daily and weekly summary reports
- Anti-pattern documentation based on March 2026 incidents
