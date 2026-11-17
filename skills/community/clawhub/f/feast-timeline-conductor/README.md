# Feast Timeline Conductor

**Dinner at 19:00 — every dish, hot, at the same minute.** A multi-dish meal
is a scheduling problem people run from memory and lose. This tool
backward-schedules your menu from the serve time across your real kitchen:
one oven with N shelves and a temperature window, M burners, and one pair
of hands.

## The real-world problem

Holiday dinners and dinner parties fail the same way every time: the roast
runs long, the sides fight for oven space at different temperatures, and
"food's ready!" becomes a 40-minute stagger of lukewarm dishes. Recipe
cards tell you how to cook each dish — nothing tells you **when each dish
goes in so they finish together**.

## What it does

- **Backward scheduling** from your serve time through each dish's
  `prep → cook → rest` chain
- **Oven as a shared resource**: dishes co-bake only within ±25°F and
  available shelf slots; conflicting dishes are sequenced automatically
- **Hold windows as slack**: a braised dish with 60 min of hold finishes
  early so the 450°F popovers can take the oven at the end
- **Hands-busy audit**: warns when two knife-work tasks collide
- **Make-ahead split**: moves cranberry sauce / pies / casseroles to a
  day-before list
- **Feasibility check**: "it's 15:20 — when could I realistically serve?"
  → earliest feasible serve time

## Quick start

```bash
python3 scripts/feast.py example --out dishes.json   # then edit
python3 scripts/feast.py plan --serve 19:00 --dishes dishes.json
python3 scripts/feast.py plan --dishes dishes.json --now 15:20   # earliest serve?
```

Output is a minute-by-minute timeline: PREP tasks, OVEN/BURNER entries with
temperatures, OUT/rest events, READY times with hold-slack usage, plus
warnings for infeasibility and prep collisions.

Stdlib-only Python 3. No dependencies.

## License

MIT © 2026 Denis Voronin
