# Example — `send_reply` with verification (the critical path)

A WRITE operation. This is the example to internalize. It shows the full state
machine, including the **`unconfirmed` branch where the correct action is to NOT
resend.**

## Happy path (ends `confirmed`)

```
1. read_thread t_88213
   last_inbound: "Is early check-in possible on Friday? We land at 10am."
   dedupe_key = hash("t_88213\nhi marco! early check-in at 1pm works...")

2. ledger.check(dedupe_key) → not present. OK to proceed.

3. draft_reply:
   "Hi Marco! We can offer early check-in at 1pm on Friday — the cleaners
    finish by then. I'll note your ~10am arrival. Safe travels!"
   state = drafted

4. approval gate (policy: required)
   present thread + draft → approver: "go"

5. POST /tools/airbnb/messages/send  (EXACTLY ONCE)
   response: { "sent": true }
   → state = attempted
   → ledger.write({dedupe_key, thread_id:t_88213, attempted_at:now,
                    final_state:pending, operator:agent-7})

6. verify: re-read thread at t+2s
   GET /tools/airbnb/messages?thread_id=t_88213
   outbound message with our text present, timestamp newer than attempt ✓
   → state = confirmed
   → ledger.update(final_state=confirmed, verified_at=now)

7. report_status:
   { "op":"send_reply", "state":"confirmed", "thread_id":"t_88213",
     "human_action_needed": false }
```

## Unconfirmed path (ends `unconfirmed` — DO NOT RESEND)

```
5. POST /tools/airbnb/messages/send → { "sent": true }
   → state = attempted, ledger written

6. verify: re-read at t+2s  → outbound NOT present
   re-read at t+5s          → outbound NOT present
   re-read at t+10s         → outbound NOT present
   (optional) DevTools DOM read of the thread → still not present
   → state = unconfirmed

7. ⛔ DO NOT call /messages/send again.
   report_status + ESCALATE:
   {
     "op":"send_reply", "state":"unconfirmed", "thread_id":"t_88213",
     "draft":"Hi Marco! We can offer early check-in at 1pm ...",
     "what_happened":"endpoint sent:true but message not visible after t+2/5/10s",
     "do_not":"resend automatically",
     "human_action_needed": true
   }
```

Why no resend: the endpoint may have actually delivered (UI lag) — resending
would post the message twice to a real guest. A human reads the live thread and
decides.

## Failed path (send call errored)

```
5. POST /tools/airbnb/messages/send → 502 / timeout
   → state = failed
6. re-read thread once: is the text somehow present?
     yes → reclassify confirmed, record it.
     no  → escalate. Do NOT blind-resend.
```

## Anti-patterns
- ❌ Marking `confirmed` on `sent: true` without re-reading.
- ❌ Looping the send call until the thread shows the message.
- ❌ Resending from `unconfirmed` or `failed` without a human + a fresh live read.
- ❌ Calling `/messages/send` more than once per draft.
