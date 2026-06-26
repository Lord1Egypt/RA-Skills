# Reference — Airbnb safety rules

The portable safety contract. Universal — do not weaken per deployment. The only
deployment-specific knob is the **approval policy** (who approves, and whether
approval is required for sends).

## Operation tiers

| Tier | Definition | Examples | Default gate |
|---|---|---|---|
| **READ** | Cannot change anything a guest or the host can see. | check inbox, read thread, lookup reservation, booking summary, inspect calendar, verify a sent message | None — proceed. |
| **WRITE** | Produces something a guest sees, but bounded & verifiable. | send a guest reply | Approval (if configured) **+ mandatory verify**. |
| **MUTATE** | Affects money, availability, or listing state; effectively irreversible. | change price, block/open dates, edit listing, accept/decline a booking, issue a refund | **v1: refuse + escalate.** (v2: own gated workflow.) |

Classify every operation into exactly one tier *before* acting. If an operation
spans tiers, split it; never let a READ workflow quietly perform a WRITE.

## Approval gate (WRITE)

- Per-message, never standing. One approval authorizes exactly one send of one
  draft to one thread.
- Present to the approver: the target thread id, the last inbound guest message,
  and the full draft text. Wait for explicit "go".
- Deployment policy decides whether approval is *required*. Safe default:
  required for all guest-facing sends. If disabled, verification is still
  mandatory.

## Irreversibility boundary

Treat everything a guest can see, and anything touching money or availability,
as irreversible in practice. You cannot reliably "unsend". This is why:
- WRITE ops always verify after the fact.
- MUTATE ops are refused in v1 rather than attempted optimistically.

## Ambiguous state — the default is caution

| Ambiguity | Action |
|---|---|
| Can't tell if a send landed | `unconfirmed`. Do NOT resend. Escalate. |
| Two read paths disagree on a material fact (dates, guest count, price) | Report BOTH, flag the discrepancy, escalate. Do not silently pick one. |
| Browser identity health unclear | Check the browser health role; if unhealthy, escalate rather than assuming. |
| Ledger state unknown after restart | Verify by reading the live thread before any send. |

## Escalate to a human when

- A send reaches `unconfirmed` or `failed`.
- You are asked to perform any MUTATE operation.
- The host browser identity reports unhealthy.
- Two read paths disagree on a material fact.
- You would need to send the same message twice for any reason.
- A required tool role for the requested operation is missing.

## Escalation report shape

When escalating, emit enough for a human to act without re-investigating:

```
ESCALATION
  op:            send_reply
  thread_id:     <id>
  reservation:   <id | none>
  state:         unconfirmed
  what happened: send endpoint returned sent:true; message not visible after
                 t+2/5/10s re-reads.
  draft:         "<the exact text>"
  do NOT:        resend automatically.
  human action:  open the thread, confirm whether the message is present; if
                 absent, decide whether to re-send manually.
```

## Observability

Every operation — read or write — emits a structured status:

```json
{
  "op": "send_reply",
  "tier": "WRITE",
  "path_used": "airbnb-endpoint",
  "thread_id": "…",
  "reservation_id": "… | null",
  "state": "confirmed | unconfirmed | failed | ok",
  "dedupe_key": "… | null",
  "human_action_needed": false
}
```

A human should be able to reconstruct exactly what happened from the report
stream alone.
