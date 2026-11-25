---
name: carpool-rotation-coordinator
description: School-run and activity carpool scheduler that is actually fair. Seat-credit rotation model (each ride a kid takes is a debt, each seat a driver supplies is a credit), weekday-availability constraints, booster-seat capacity checks, holiday/blackout skip calendar, fairness audit with drift warnings, and per-family cost split from mileage. Ends the "we always drive" resentment.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [carpool, school-run, parenting, scheduling, fairness, family]
---

# Carpool Rotation Coordinator

Generates a multi-week carpool driver schedule that is **provably fair**,
respects who can actually drive which weekday, never overfills a car
(including booster seats), skips holidays, and tells each family what they
owe in fuel money.

## When to trigger
- "set up a carpool for school / soccer / swim practice"
- "the rotation isn't fair, one family drives way more"
- "who drives next Tuesday?"
- "carpool cost split — what should each family pay"
- re-planning a carpool when a family joins/leaves or schedules change

## How it works

1. **Describe the carpool** in a JSON registry (see
   `sample_carpool.json`): families with kids on the route, driver seat
   capacity (passenger seats), booster seats available, which weekdays each
   driver can take, and the trip pattern (AM only / PM only / both).
2. **Run** `scripts/carpool_plan.py plan sample_carpool.json --weeks 12`.
3. **The seat-credit engine** (this is the fairness core):
   - Every ride a kid consumes = 1 seat-credit of **debt** for that family.
   - Every passenger seat a driver supplies on a trip = 1 seat-credit of
     **credit** for the driver's family.
   - Long-run fairness = every family's balance stays near zero. This is why
     naive "equal driving days" is wrong: the family with 3 kids in the
     pool owes 3× the seats even if it drives the same number of days.
4. **Greedy assignment with fairness pull**: each school day picks the
   available driver with (a) enough total capacity for all kids riding,
   including boosters for kids that need them, (b) the **lowest seat-credit
   balance**. Holidays/blackouts are skipped. Absent kids reduce demand and
   others' debts fairly.
5. **Audit output**: per-family drive-days, seats-supplied, seats-consumed,
   running balance with a ±15% tolerance band; DRIFT warning if any family
   leaves the band; suggested correction week.
6. **Cost split** (`--cost-per-km`): mileage × trips → per-family share
   computed from net credit balance, printed as who-pays-whom.

## Pitfalls encoded
- **"Equal days" is not fair** when kids-per-family differ — credits, not
  days, are the unit (the #1 carpool failure mode).
- **Booster math is a hard constraint**: 4 kids where 2 need boosters and
  the driver has 1 booster = that driver cannot take that day; the solver
  checks before assigning, not after.
- **Blackout dates** (holidays, camps, half-days) must live in the registry;
  a schedule that ignores them breaks in week 3.
- **Do not front-load a "nice" family** — greedy-by-balance naturally
  spreads load; manual overrides need a `--force` re-audit.
- Kids absent on a day don't create debt for their family that day (the
  engine charges only seats actually consumed).

## Examples

```bash
# Generate a 12-week schedule with fairness audit
python3 scripts/carpool_plan.py plan sample_carpool.json --weeks 12

# With cost split (fuel at 0.18 EUR/km, 6 km one-way route)
python3 scripts/carpool_plan.py plan sample_carpool.json --weeks 12 \
  --cost-per-km 0.18 --km-one-way 6

# Just audit the fairness of a registry + existing assignment file
python3 scripts/carpool_plan.py audit sample_carpool.json --weeks 12
```

## Output contract
- week-by-week Mon–Fri grid of drivers (SKIPPED for holidays)
- per-family stats table: drive-days, seats given, seats taken, balance
- FAIR / DRIFTING verdicts with corrective suggestions
- optional who-pays-whom settlement for fuel
