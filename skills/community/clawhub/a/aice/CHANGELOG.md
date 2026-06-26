# AICE Skill — Changelog

All notable changes to the AICE skill. Format: [Semantic Versioning](https://semver.org/).

---

## [1.0.0] — 2026-03-01

**First versioned release.** Consolidates all features developed since inception (19-feb-2026).

### Core
- 5 bidirectional domains: TECH, OPS, JUDGMENT, COMMS, ORCH (§1)
- Scoring: errors (−1/−3/−5/−10), pro-patterns (+3), bonus, exceptional, streaks with ACC table (§2)
- Daily caps, warmup, clusters, reincidence, LEARNED_FROM_CORRECTION (§2)
- 6 agent anti-patterns: SECRETARY, EXCUSE, SELECTIVE, OVERAPOLOGY, CHEERLEAD, CAPITULATION (§3)
- 6 agent pro-patterns: ANTICIPATE, CLEAN_FIX, SMART_SILENCE, CTX_KEEP, DEEP_RESEARCH, GROUNDED_STAND (§4)

### User Scoring
- Bidirectional scoring with same mechanics (§5)
- ADR-like 3 levels: sin spec (−3), ADR-like (Δ0), ADR estricto (+1-3) (§5)
- 10 user anti-patterns, 10 user pro-patterns incl. CRITERIA_EVOLUTION (§5)
- Team Score ownership-weighted formula: GOOD/COMPENSATED/PROBLEM/BREAKDOWN quadrants (§5)

### Triggers
- 5 scoring triggers: puntúa, auto-score, task-complete, idea-validate, criteria-evolution (§8)
- 4 operational triggers: recuerda, lección, status, verifica, busca (§8)
- 4 Hub triggers: hub-register, hub-status, hub-sync, hub-key (§8)

### Pool Scoring
- Runtime-based scoring: platform + model + thinking (§12, ADR-048)
- Cross-pool diagnostic attribution (ADR-047)
- Runtime snapshot restore (ADR-044)

### Hub Integration
- Server-side scoring authority (ADR-049)
- Fire-and-forget event sync with circuit breaker (§14)
- Hub state = source of truth for online scores (§14)
- Batch/combo events (ADR-054)
- Privacy: zero conversation content sent

### Parameters
- 9 params (8 core + humor), dual definitions for agent and user (§13)

### Display
- 2-level scoring display: Nivel 1 (one-line) + Nivel 2 (table 2×5) (§11)

### Operational
- Auto-management checklist (§7)
- Anti-exaggeration rule for ×N counting (§7)
- Learning skill with anti-duplication (§9)
- Trust recovery, escalation chain (§6)
- Installation wizard (ADR-035/041)

### Versioning
- Semver in frontmatter, CHANGELOG, Hub version check (§15)
