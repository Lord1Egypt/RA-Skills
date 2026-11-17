# Example — `inspect_calendar`

A READ operation. Report calendar state and **flag** high-risk patterns.
`inspect_calendar` itself never changes the calendar — it is read-only, flag only.
*Changing* the calendar (block/open dates, price) is a separate, approval-gated
MUTATE-CAL operation (see SKILL.md → "Approved calendar mutations"); it is never a
side effect of an inspection.

## Procedure
1. Tier 1: call the Airbnb calendar role for the requested range (default: next
   60 days).
2. Classify each day/span: `booked`, `blocked`, `open`.
3. Run risk checks (flag, don't fix):
   - **Double-booking:** two reservations overlapping the same night.
   - **Anomalous price:** a night priced far outside the range's norm.
   - **Risky back-to-back:** check-out and next check-in same day with no buffer
     for turnover.
   - **Unexpected open gap:** open nights between two bookings that usually fill.
4. Emit state + a `flags` array. Recommend nothing irreversible.

## Reference-deployment call
```
GET /tools/airbnb/calendar?from=2026-06-03&to=2026-08-02     # tier 1
```

## Sample output
```json
{
  "op": "inspect_calendar",
  "tier": "READ",
  "path_used": "airbnb-endpoint",
  "range": { "from": "2026-06-03", "to": "2026-08-02" },
  "spans": [
    { "from":"2026-06-06", "to":"2026-06-09", "state":"booked", "reservation_id":"r_5521" },
    { "from":"2026-06-09", "to":"2026-06-11", "state":"open" },
    { "from":"2026-06-11", "to":"2026-06-14", "state":"booked", "reservation_id":"r_5540" }
  ],
  "flags": [
    { "type":"back_to_back", "date":"2026-06-09",
      "detail":"r_5521 check-out and r_5540-adjacent open night; verify turnover time" }
  ],
  "human_action_needed": false
}
```

## When a flag is serious
If a flag implies guest-visible risk (e.g., an actual double-booking), escalate
to a human immediately with the specifics. Do NOT attempt to resolve it by
changing the calendar during an inspection — that is a separate MUTATE-CAL
operation that requires its own explicit per-operation operator approval.

## Degradation
- Tier-1 calendar role missing/hard-down twice → agent-browser read of the
  calendar page → DevTools DOM read → escalate.

## Anti-patterns
- ❌ "Fixing" a double-booking by blocking dates *during an inspection*.
  `inspect_calendar` only flags + escalates; blocking is a separate approval-gated
  MUTATE-CAL op, never an automatic response to a flag.
- ❌ Reporting calendar state from a stale cache without noting it; if the read
  path is ambiguous, say so.
