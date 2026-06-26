---
name: a2a-market-compute-ledger
description: Manage compute account ledgers, frozen balances, charge events, and settlement records for A2A commerce flows. Use when implementing or operating compute billing, debit, freeze, unfreeze, and audit trails.
---

# a2a-Market Compute Ledger

Build and operate the compute ledger module for RealMarket A2A runtime.

Current status: scaffold-first skill for early registration. Keep APIs stable, add production logic incrementally.

## Scope
- Own `ComputeAccount` domain object, balance snapshots, and immutable transaction journal.
- Support reserve/freeze before negotiation and final debit after order confirmation.
- Emit billing events to event bus for reputation, websocket push, and finance logs.

## Suggested Project Layout
- `app/domain/entities/compute_account.py`
- `app/application/services/billing_service.py`
- `app/infrastructure/db/ledger_repository.py`
- `app/infrastructure/tasks/reconcile_ledger.py`

## Minimum Contracts (MVP P0)
1. `freeze(account_id, amount, reason)` returns hold id and expiry.
2. `capture_hold(hold_id, order_id)` converts hold to settled charge.
3. `release_hold(hold_id)` unlocks unused balance.
4. `list_ledger_entries(account_id, from_ts, to_ts)` returns ordered journal records.

## Event Mapping
- On hold created: emit `INTENT_CREATED` + billing extension payload.
- On charge captured: emit `ORDER_CREATED` and settlement payload.
- On charge finalized: emit `PAYMENT_SUCCEEDED`.

## Guardrails
- Use integer minor units for money; avoid float math.
- Enforce idempotency key on every mutating operation.
- Keep journal append-only; never rewrite posted entries.

## Implementation Backlog
- Add double-entry validation rules.
- Add monthly statement export and audit tooling.

## Runtime Implementation
- Status: implemented in local runtime package.
- Primary code paths:
- `runtime/src/domain/compute-ledger.js`
- Validation: covered by `runtime/tests` and `npm test` in `runtime/`.
