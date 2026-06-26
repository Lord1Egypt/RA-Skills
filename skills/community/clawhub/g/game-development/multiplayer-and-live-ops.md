# Multiplayer and Live Operations

Use this file only when single-player loop quality is already validated.

## Multiplayer Escalation Path

- Local multiplayer or async ghost data first
- Lightweight online sync for non-critical interactions
- Authoritative server for competitive or economy-sensitive games

Do not jump directly to full authoritative architecture without product evidence.

## Netcode Decision Heuristics

- Turn-based or low-frequency interactions: lockstep or command sync
- Action gameplay with precision demands: client prediction plus reconciliation
- Social/co-op relaxed gameplay: state replication with smoothing

## Session Reliability Basics

- Explicit reconnect states
- Clear host/server authority rules
- Deterministic timeout and retry policy
- Duplicate message handling via idempotent message IDs

## Live Ops Baseline

Before live events or seasonal content:
- telemetry for retention and drop-off points
- remote-config or data-driven tunables
- rollback plan for faulty content updates
- support playbook for incident communication

## Scope Warning

Multiplayer and live ops multiply cost across code, QA, hosting, and support.
Only enable when business goals require it.
