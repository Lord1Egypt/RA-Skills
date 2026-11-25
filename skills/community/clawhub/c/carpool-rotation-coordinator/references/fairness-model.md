# Carpool Rotation Coordinator — Reference

## 1. The problem
School-run and activity carpools are the classic informal arrangement that
works for a month and then quietly rots: one family ends up driving three
days a week, nobody notices because "we all take turns", and the pool
collapses into resentment or just dissolves. The failure is structural:

- Fairness is usually measured in **driving days**, but the real resource is
  **seat-trips**. A family with 3 kids in the pool consumes 3 seats every
  single run; a family with 1 kid consumes 1. Equal days ≠ equal load.
- Availability is weekday-shaped (one parent has Tuesday meetings, another
  does late shifts) — round-robin ignores that.
- Booster/child-seat capacity is invisible until a minivan shows up with
  more kids than belts.
- Holidays and camps punch holes in the calendar and desync any fixed
  rotation.

## 2. The seat-credit model
Define for each trip t (an AM or PM run on a school day):

- For every kid of family f riding t: `debt[f] += 1`.
- For the driver family d of t: `credit[d] += seats_filled(t)`
  (only occupied passenger seats count — driving an empty van is a route
  decision, not charity).

Fairness over a horizon = every family's balance
`B[f] = credit[f] − debt[f]` stays within a ±15 % band of zero (scaled by
trips per week). This model is self-correcting: a family that falls behind
in balance gets picked first by the scheduler next time it is available.

## 3. Assignment algorithm (greedy-by-balance)
For each school day in order, for each trip (AM, PM):

1. Skip if date in `blackouts` (holidays, camps, no-school days).
2. Compute riders: all kids not marked absent that day.
3. Candidate drivers = families whose driver is available that weekday with
   `passenger_seats ≥ #riders` and `boosters ≥ #riders_needing_booster`
   (drivers may also just have their own kid ride with someone else if
   capacity forces it — flagged, not silently assumed).
4. Pick the candidate with the lowest `B[f]`; tie-break by fewest
   drive-days, then round-robin pointer.
5. Apply credits/debts; log the day.

Complexity O(days × families); for a school year this is instant.

## 4. Absences
Kid absent (sick, appointment): that kid generates no debt that day. The
driver still gets credit only for seats actually filled. A driver
cancellation means the next-lowest-balance available family takes the day —
recorded, so no silent overload.

## 5. Cost split
Fuel/settlement from mileage: total route cost =
`2 × km_one_way × cost_per_km × trips`. Each family's fair share of the pot
is proportional to `debt[f]`, offset by driving already done (`credit[f] ×
per_seat_rate`). Print the minimum-transfer settlement (who pays whom what)
— same technique used by group-expense settlers.

## 6. Registry format (sample_carpool.json)
```json
{
  "name": "Elm Street school run",
  "kids": [
    {"name": "Mia",   "family": "Novak",  "booster": true,  "absent": ["2026-12-01"]},
    {"name": "Tom",   "family": "Novak",  "booster": false},
    {"name": "Sara",  "family": "Kowalski","booster": false},
    {"name": "Ben",   "family": "Rossi",  "booster": true}
  ],
  "drivers": [
    {"family": "Novak",   "name": "Ana",  "seats": 4, "boosters": 2,
     "weekdays": ["Mon","Tue","Thu"]},
    {"family": "Kowalski","name": "Piotr","seats": 3, "boosters": 1,
     "weekdays": ["Mon","Wed","Fri"]},
    {"family": "Rossi",   "name": "Elena","seats": 5, "boosters": 1,
     "weekdays": ["Tue","Wed","Thu","Fri"]}
  ],
  "trips": ["AM", "PM"],
  "start": "2026-11-30",
  "blackouts": ["2026-12-24", "2026-12-25", "2027-01-01"]
}
```

Note Mon–Fri only; weekend activities can be modelled by `weekdays` on a
7-day grid — the engine is calendar-agnostic.

## 7. Limitations
- Deterministic greedy, not global optimum — with heavy weekday
  constraints an LP could do marginally better; in practice the audit band
  catches any real drift, and the correction week fixes it.
- Assumes kids ride every non-blackout school day unless marked absent.
- Doesn't model en-route pickup order (no TSP); carpools with scattered
  addresses need a route order agreed by humans.
