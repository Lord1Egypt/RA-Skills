# High-Risk Batch Action Review Template

Use for moderation, deletion, publishing, permissions, financial operations, status changes, exports, and other multi-record mutations.

## Scope Inputs

- Action semantics, maximum scope, affected roles, and irreversible consequences.
- Selection model, hidden/filtered records, automation inputs, and approval policy.
- Undo window, rollback feasibility, audit retention, and incident response owner.

## Evidence Checklist

- Selection source and exact impact count remain visible through confirmation.
- Permissions combine role, record state, risk level, and environment where required.
- Confirmation names the action and consequence; typed confirmation is reserved for exceptional risk.
- Pending, partial success, retry, cancellation, idempotency, rollback, and conflict states are explicit.
- Results identify succeeded, failed, skipped, and still-pending records.
- Audit records capture actor, time, source selection, parameters, reason, and outcome.
- Sampling and secondary approval rules are visible and explainable.

## High-Risk Findings

- `P0`: unseen or unauthorized records can be changed, retry duplicates mutations, or there is no feasible recovery path.
- `P1`: impact scope, partial results, or audit evidence is unclear.
- `P2`: confirmation copy, progress presentation, or result filtering needs polish.

## Acceptance Examples

- Confirmation states the exact count, current filter scope, exclusions, and irreversible effects.
- A retry is idempotent and does not repeat successful mutations.
- Partial failure exposes record-level reasons and a safe retry subset.
- Undo/rollback behavior is timed, permission-aware, auditable, and verified against representative fixtures.
