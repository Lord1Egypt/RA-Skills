# Example — `lookup_reservation` / `booking_summary`

READ operations. Find reservations and map them to message threads. No writes.

## `booking_summary` — upcoming bookings

### Procedure
1. Tier 1: call the Airbnb reservations role.
2. Filter to upcoming/active; sort by check-in ascending.
3. For each: guest, check-in/out, status, `reservation_id`, linked `thread_id`.
4. Emit a structured list.

### Reference-deployment call
```
GET /tools/airbnb/reservations        # tier 1
```

### Sample output
```json
{
  "op": "booking_summary",
  "tier": "READ",
  "path_used": "airbnb-endpoint",
  "bookings": [
    { "reservation_id":"r_5521", "guest":"Marco R.", "status":"confirmed",
      "check_in":"2026-06-06", "check_out":"2026-06-09", "thread_id":"t_88213" },
    { "reservation_id":"r_5540", "guest":"Lena K.", "status":"confirmed",
      "check_in":"2026-06-11", "check_out":"2026-06-14", "thread_id":"t_88301" }
  ],
  "human_action_needed": false
}
```

## `lookup_reservation` — by id or guest

### Procedure
1. Tier 1: query reservations by `reservation_id` or guest name.
2. Return full detail + the linked `thread_id` so a reply ties to the right
   booking.
3. If multiple guests match a name, return all matches — do not guess.

### Sample output
```json
{
  "op": "lookup_reservation",
  "tier": "READ",
  "reservation_id": "r_5521",
  "guest": "Marco R.",
  "status": "confirmed",
  "check_in": "2026-06-06",
  "check_out": "2026-06-09",
  "guests": 2,
  "thread_id": "t_88213",
  "human_action_needed": false
}
```

## Thread ↔ reservation mapping
The link is what lets a reply cite correct dates/guest counts. When the endpoint
doesn't provide the link directly, correlate by guest name + dates across the
inbox and reservations lists, and flag any ambiguity rather than guessing.

## Degradation
- Tier-1 reservations role missing/hard-down twice → agent-browser read of the
  reservations page → DevTools DOM read → escalate.

## Anti-patterns
- ❌ Picking one match when a name is ambiguous. Return all; let the caller
  disambiguate.
- ❌ Treating a calendar block as a reservation — they are different objects.
