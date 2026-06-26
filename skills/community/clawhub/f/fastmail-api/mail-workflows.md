# Mail Workflows — Fastmail API

## Mailbox Inventory

Use `Mailbox/get` to capture mailbox IDs before move or delete actions.
Always reference mailbox IDs, not display names, during writes.

## Search and Batch Processing

Preferred sequence for large inbox operations:
1. `Email/query` with narrow filters and explicit limit
2. `Email/get` for selected IDs only
3. `Email/set` in small batches for move, flag, or delete

## Draft and Send Flow

Use staged operations:
1. Create or update draft with `Email/set`
2. Validate recipients and identity
3. Send with submission method
4. Confirm sent state via read-back

## High-Impact Guardrails

Before destructive changes:
- Confirm exact message count affected
- Confirm target mailbox IDs
- Snapshot request payload to `~/fastmail-api/snapshots/`
- Execute one small batch before full rollout
