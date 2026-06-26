# Example — `read_thread`

A READ operation. Open one thread, read the live messages, summarize guest
intent. No drafting, no sending.

## Procedure
1. Tier 1: call the Airbnb thread-read role for `thread_id`.
2. Capture the full message list in order; identify the **last inbound** guest
   message (this is what a reply would answer).
3. Summarize guest intent in one line (question / request / complaint / logistics
   / smalltalk).
4. Map to a reservation if a link is available (helps later replies cite dates).
5. Emit a structured summary.

## Reference-deployment call

```
GET /tools/airbnb/messages?thread_id=t_88213     # tier 1
```

## Sample output

```json
{
  "op": "read_thread",
  "tier": "READ",
  "path_used": "airbnb-endpoint",
  "thread_id": "t_88213",
  "reservation_id": "r_5521",
  "last_inbound": {
    "at": "2026-06-03T14:22:00Z",
    "text": "Hi! Is early check-in possible on Friday? We land at 10am."
  },
  "intent": "request: early check-in on Friday (arrival ~10am)",
  "messages_count": 6,
  "human_action_needed": false
}
```

## Verification re-use
The same read path is what `verify_sent` and the send state machine use to
confirm an outbound message. Reading a thread is always safe and never counts as
a send.

## Degradation
- Tier-1 read missing/hard-down twice → agent-browser navigate to the thread and
  read rendered messages → DevTools DOM read → escalate.
- If two read paths disagree on dates/guest count, report both and flag (see
  `references/airbnb-safety-rules.md`).

## Anti-patterns
- ❌ Summarizing intent from the inbox snippet without opening the thread —
  snippets truncate and you may miss the actual ask.
