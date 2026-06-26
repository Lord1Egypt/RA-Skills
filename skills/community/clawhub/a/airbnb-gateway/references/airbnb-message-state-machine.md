# Reference — Airbnb message send state machine

This is the authoritative definition of the send discipline. `SKILL.md` carries
the operational summary; this file carries the full machine, timings, and edge
cases. **This logic is universal — do not fork it per deployment.**

## States

| State | Meaning | Terminal? |
|---|---|---|
| `drafted` | Reply text composed, thread + dedupe-key recorded. Nothing sent yet. | no |
| `attempted` | Send endpoint called exactly once and returned. **Delivery NOT proven.** | no |
| `confirmed` | Outbound message verified visibly present in the live thread. | yes ✅ |
| `unconfirmed` | Send returned but the message could not be seen after the verify window. | yes ⚠️ |
| `failed` | The send call itself errored (4xx/5xx/timeout). | yes ❌ |

## Transitions

```
            approval (if required)              send endpoint
  drafted ───────────────────────► (ready) ───── exactly once ─────► attempted
                                                                         │
                                              re-read same thread        │
                                          ┌──────────────────────────────┤
                                          │                              │
                            visible ◄─────┘                              └─────► call errored
                               │                                                     │
                               ▼                                                     ▼
                          confirmed ✅                                            failed ❌
                                                                                     │
                            absent after verify window                               │
                               │                                                     │
                               ▼                                                     ▼
                         unconfirmed ⚠️  ◄──────── (treat like) ──────────── re-read thread
                               │                                                     │
                               └──────────► ESCALATE. No automatic resend. ◄─────────┘
```

## The dedupe-key

`dedupe_key = hash(thread_id + "\n" + normalize(draft_text))`

`normalize` = trim, collapse internal whitespace, lowercase. The key makes "the
same reply to the same thread" idempotent regardless of retries.

## The ledger (duplicate-prevention backbone)

An append-only record, ideally persisted (survives restarts). One row per
`attempted`:

```json
{
  "dedupe_key": "…",
  "thread_id": "…",
  "attempted_at": "ISO-8601",
  "final_state": "confirmed | unconfirmed | failed",
  "verified_at": "ISO-8601 | null",
  "operator": "agent-id | human-id"
}
```

Rules:
- Write the row at `attempted`, **before** verifying. A crash between send and
  verify must never look like "never sent."
- Before any new send, check the ledger for the dedupe-key:
  - `confirmed` recently → STOP, already handled.
  - `attempted`/`unconfirmed` present → STOP, do NOT resend; escalate.
- If no persistent ledger exists, keep an in-session ledger and treat a restart
  as "state unknown → verify by reading the thread before any send."

## Verify window

Re-read the thread at **t+2s, t+5s, t+10s** after `attempted` (Airbnb UI can
lag). Match by outbound text + a timestamp newer than the attempt. If still
absent after the last poll → `unconfirmed`. Do not extend indefinitely; do not
resend.

When the endpoint read is ambiguous (e.g., returns cached/empty), escalate the
*verification* (not the send) to a DevTools read of the live thread DOM. Reading
to verify is always allowed; it is never a second send.

## Edge cases

| Situation | Correct handling |
|---|---|
| Endpoint `sent:true`, message never appears | `unconfirmed`. Escalate. Never resend. |
| Send timed out, unknown if it landed | `failed`. Re-read thread. If the text is now present → reclassify `confirmed` (record it). If absent → escalate; do NOT blind-resend. |
| Two replies queued for one thread | Process serially; each gets its own dedupe-key and full machine. |
| Guest sends a new message mid-verify | Does not affect the outbound verification; verify your own message only. |
| Approval denied at the gate | Stay `drafted`. Discard or revise; never send. |
