---
name: a2a-market-stake-freeze
description: Provide stake freeze and release rules for participants during negotiation and order execution. Use when implementing stake locking policy, slashing triggers, and stake lifecycle integration with orders.
---

# a2a-Market Stake Freeze

Build the rule engine shell for stake lock lifecycle in A2A transactions.

Current status: registration-first scaffold with explicit policy points.

## Scope
- Lock stake when node accepts an intent or enters negotiation.
- Release or slash stake based on final outcome and policy.
- Keep stake decisions auditable for dispute resolution.

## Suggested Project Layout
- `app/domain/rules/stake_rules.py`
- `app/application/services/stake_service.py`
- `app/infrastructure/db/stake_repository.py`
- `app/infrastructure/tasks/stake_timeout_worker.py`

## Minimum Contracts (MVP P0)
1. `freeze_stake(node_id, intent_id, amount)` returns lock record.
2. `release_stake(lock_id, reason)` closes lock and restores available stake.
3. `slash_stake(lock_id, reason, evidence)` applies penalty and emits incident log.
4. `evaluate_timeout_locks(now_ts)` handles automatic release/slash decisions.

## Policy Baseline
- Lock amount should be deterministic from intent risk tier.
- Slashing requires evidence payload and policy version.
- Timeout defaults to release unless explicit breach condition is met.

## Events
- Emit `NEGOTIATION_STARTED` when stake lock is confirmed.
- Emit risk/stake incident events for policy engine and logging.

## Implementation Backlog
- Add dynamic stake multipliers by market volatility.
- Add external arbitration hook for manual dispute outcomes.

## Runtime Implementation
- Status: implemented in local runtime package.
- Primary code paths:
- `runtime/src/domain/stake-policy.js`
- Validation: covered by `runtime/tests` and `npm test` in `runtime/`.
