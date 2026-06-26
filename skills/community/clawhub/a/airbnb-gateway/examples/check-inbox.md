# Example — `check_inbox`

A READ operation. No approval, no write. Goal: surface threads needing attention,
prioritized, without changing anything.

> Tool names below are from the reference deployment. Map them via
> `references/airbnb-tool-priority.md`.

## Procedure
1. Tier 1: call the Airbnb messages-list role.
2. For each thread, note: `thread_id`, guest name, last-message direction
   (inbound/outbound), last-message time, unread flag, linked reservation if
   available.
3. Prioritize: unread inbound > inbound awaiting reply > everything else.
   Within a bucket, sort by most recent.
4. Emit a structured summary. Do not open/draft/send anything.

## Reference-deployment call

```
GET /tools/airbnb/messages          # tier 1
```

## Sample output

```json
{
  "op": "check_inbox",
  "tier": "READ",
  "path_used": "airbnb-endpoint",
  "threads": [
    { "thread_id": "t_88213", "guest": "Marco R.", "last": "inbound",
      "at": "2026-06-03T14:22:00Z", "unread": true, "reservation_id": "r_5521",
      "snippet": "Hi! Is early check-in possible on Friday?" },
    { "thread_id": "t_88190", "guest": "Dana P.", "last": "outbound",
      "at": "2026-06-03T09:10:00Z", "unread": false, "reservation_id": "r_5498",
      "snippet": "Thanks, enjoy your stay!" }
  ],
  "needs_attention": ["t_88213"],
  "human_action_needed": false
}
```

## Degradation
- Tier-1 list role missing or hard-down twice → agent-browser navigate to the
  inbox and read the rendered list (still READ). If that's also unavailable →
  DevTools DOM read. If all absent → escalate (required read role missing).

## Anti-patterns
- ❌ Auto-drafting replies during an inbox check. `check_inbox` is read-only;
  drafting is a separate, explicit step.
