# Car Seat Stage Pilot

**Which car seat stage is my child in — and when is the next transition?**

Car-seat safety runs on three clocks at once: the child's **age**, **weight**, and **height**,
plus the specific seat's limits. Most parents transition too early — turning the seat forward at
age 1 because legs "look cramped", boosting a tall 3-year-old, or dropping the booster at 6.
Premature transitions are among the most common and most dangerous car-seat errors.

## What it does

Give it a birthday (or age in months) plus optional weight/height, and it returns:

- **Stage verdict** — rear-facing / forward-facing harness / booster / adult belt, with the seat
  type and harness rule that applies right now.
- **Limit warnings** — fires when a measurement is at or over a typical seat limit.
- **Next transition** — the earliest of age-, weight-, and height-driven dates, so you know when
  to re-check ("booster window opens 2028-03-15, driven by age").
- **Lifetime timeline** — projected milestones from infant-carrier outgrow check to back-seat-until-13.
- **5-step belt-fit test** — the checklist that actually gates leaving the booster.

## Quick start

```bash
python3 scripts/car_seat_pilot.py --birthday 2024-03-15 --weight-lb 24 --height-in 31
python3 scripts/car_seat_pilot.py --months 100 --height-in 54        # booster-age kid
python3 scripts/car_seat_pilot.py --months 9 --weight-lb 20 --json   # machine output
```

## Real-world problem it solves

A parent asks: *"Grandma says my 30-month-old can face forward now."* The honest answer needs
age floors, seat weight caps, strap-height direction, and tether rules — evaluated together.
This tool computes it in one pass: yes, the age floor passed at 24 months, but at 24 lb she's
years from booster territory, and the harness rules (straps above shoulders, top tether) apply
today. No forum threads, no outdated blog posts.

## Basis & limits

Guidance basis: AAP 2018 policy, NHTSA, Safe Kids Worldwide. The child's seat manual and state
law always supersede this tool. When in doubt, use NHTSA's free certified car-seat inspection
station locator.

Pure Python 3 standard library — no dependencies. MIT license.
