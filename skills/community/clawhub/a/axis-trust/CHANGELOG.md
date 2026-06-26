# Changelog — AXIS Trust Infrastructure Skill

All notable changes to this skill are documented here.

## v1.1.0 — 2026-03-13

Initial ClawHub release. This version corresponds to AXIS platform v1.1 (Security Update).

### Added
- Full API reference for all public and authenticated endpoints
- Trust Decision Framework with clear delegation, transaction, and data-sharing thresholds
- `agentId` type clarification: all procedures expect a numeric integer, not a string
- Corrected `apiKeys.create` field name: `label` (not `name`); no `scope` field
- Corrected `agents.register` field name: `agentClass` (not `class`)
- All five `agentClass` values documented: `enterprise`, `personal`, `research`, `service`, `autonomous`
- `trust.addEvent` procedure fully documented with all 13 event types
- Health check endpoint (`GET /health`) documented
- PVQ webhook signature verification notes
- Security notes explaining dual-party verification and audit chain
- Examples folder with shell and Python code snippets
- README.md with quick-reference tables for T-Score tiers and C-Score grades

### Platform (v1.1 — 2026-03-13)
- Full security subsystem: replay prevention, credibility multiplier, cluster detection, anomaly detection, interaction graph analysis, audit chain with Merkle roots
- PVQ webhook callbacks with HMAC-SHA256 signatures and exponential backoff
- Rate limiting: 120 req/min on `/api/trpc`, 20 req/min on `/api/oauth`
- SSRF protection and HTTPS-only enforcement on outbound webhooks
- 109 automated tests passing

### Platform (v1.0 — 2026-03-11)
- Initial platform launch
- Agent registration and AUID assignment
- T-Score (11-dimension behavioral reputation) and C-Score (economic reliability) computation
- Agent directory with public search
- API key management
- API Explorer
