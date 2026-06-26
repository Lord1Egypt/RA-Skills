# Reference — future adapter interface

This skill is the **behavioral contract**. A later, more formal adapter/tool
layer should harden the **mechanical guarantees** so correctness doesn't depend
on a model remembering a markdown rule. This file describes the adapter the
skill is designed to pair with, and how the skill should call it if/when it
exists.

## Design principle

> Judgment stays in the skill; guarantees move to the adapter.

- **Skill (prompt layer):** when to escalate, how to summarize guest intent,
  whether a state is ambiguous — model reasoning.
- **Adapter (code layer):** send-exactly-once, the dedupe ledger, the verify
  poll, tier fallback — properties you want *enforced*, not *hoped for*.

## Ideal adapter functions

The skill should prefer these when present, and fall back to its manual
procedures when they are not.

### `airbnb.sendVerified(thread_id, text, dedupe_key) → { state, visible_at, error? }`
Atomically: dedupe-check → send-once → write ledger → verify-poll. Returns a
final state from the same vocabulary (`confirmed | unconfirmed | failed`). This
is the single most valuable function — it makes the cardinal "no duplicate
sends" rule a code-level guarantee.

When present: `send_reply` delegates entirely and just reports `state`.
When absent: `send_reply` runs the manual state machine from
`airbnb-message-state-machine.md`.

### `airbnb.dedupeCheck(dedupe_key) → { already_sent, last_state, last_at }`
Lets the skill short-circuit before drafting if a reply already went out.

### Read functions
- `airbnb.listInbox(filter?) → Thread[]`
- `airbnb.readThread(thread_id) → { messages[], last_inbound, ... }`
- `airbnb.listReservations(filter?) → Reservation[]`
- `airbnb.readCalendar(range) → CalendarSpan[]`

These mirror the read verbs and let the skill avoid tier-selection logic when
the adapter already owns it.

### Future MUTATE functions (v2, each gated)
- `airbnb.setCalendar(range, state, dedupe_key)` — block/open dates.
- `airbnb.setPrice(range, amount, dedupe_key)` — pricing.
- `airbnb.respondToBooking(reservation_id, decision, dedupe_key)` — accept/decline.

Each MUTATE adapter function should follow the same shape as `sendVerified`:
do-once + ledger + verify, returning a final state. The skill wraps each in a
read → propose → approve → call → report flow.

## Capability detection

The skill should treat adapter functions as **optional**: detect availability,
prefer them, and degrade to manual procedures otherwise. Pseudocode:

```
if has(airbnb.sendVerified):
    result = airbnb.sendVerified(thread_id, text, dedupe_key)
    report(result.state)
else:
    run_manual_send_state_machine()   # per airbnb-message-state-machine.md
```

## Why both layers (defense in depth)

- The **adapter** prevents a duplicate send even if an agent misbehaves.
- The **skill** explains *why* and handles the judgment the adapter can't encode
  (intent, tone, when to escalate).

Shipping the skill first is correct: it makes the contract usable today. The
adapter promotes the riskiest guarantees into code as the deployment matures.
