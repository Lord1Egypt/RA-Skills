# Electrical Circuit Detective

**The breaker trips again. The outlet is dead. Can this circuit take one more plug?** — three questions every household hits, all answerable in under a minute with arithmetic and a diagnostic tree, before anyone opens a panel or calls a $150 service minimum.

## The Real Problem

1. **Repeated breaker trips** — people reset, reset, reset, and never learn the cause. The trip *pattern* (instant vs. minutes vs. only-when-two-things-run vs. random-at-night) is a fingerprint that points at overload, short, ground fault, or a failing appliance — each with a completely different fix.

2. **Dead outlets** — ~60% of "dead outlet" cases are a tripped GFCI in a *different room* protecting downstream outlets. The rest are switched half-outlets, half-latched breakers, and failed backstab connections — all fixable in minutes once ranked by probability. Instead, people assume "blown outlet," replace receptacles blind, or live with dead outlets for years.

3. **"Can I plug this in?"** — a 1500 W space heater plus a 1500 W microwave is 25 A on a circuit whose honest continuous ceiling is 16 A. Nobody does this math, breakers trip at dinner time, and extension cords get abused as a "fix" (they *derate* capacity; they don't add it).

## What It Does

- **Load math** with a ~80-appliance *input*-watt database (microwaves advertise 1000 W output but draw 1400-1600 W input — the classic trap) and the NEC 80% continuous rule: `OK / TIGHT / OVERLOAD` verdicts naming exactly which item to move.
- **Trip-pattern decoder** — 7 patterns → meaning → first move.
- **Dead-outlet tree** — 6 causes ranked by real-world probability, from the cross-room GFCI hunt to the backstabbed-connection signature ("several outlets dead in a line = fault is in the last *working* outlet").
- **Circuit mapping logger** — build the panel map nobody has, once.
- **Hard safety gates**: burning smell/scorch/tingle → breaker OFF + electrician, aluminum wiring (1965-73) → specialist, FPE Stab-Lok panels → replacement consultation, never upsize a breaker (14 AWG wire is *why* it's 15 A).

## Quick Start

```bash
python3 scripts/circuit_doctor.py load --volts 120 --amps 20 \
    --items "microwave (1000w out),kettle,toaster"
# -> OVERLOAD: over by 12.5 A. Move 'kettle' to another circuit.

python3 scripts/circuit_doctor.py dead-outlet   # ranked diagnosis tree
python3 scripts/circuit_doctor.py trip --pattern "trips when fridge starts"
```

## Who Needs This

Homeowners and renters (dead outlets are landlord-fixable evidence), anyone heating with space heaters this winter, home-office/server-rack operators, workshop tinkerers, VRBO/rental owners fielding guest calls, and anyone who's ever reset the same breaker four times in a week without knowing why.

**Not for**: panel interiors, new 240V circuits, aluminum-branch-wiring repairs — the skill flags and routes those to licensed electricians instead of walking you into them.

## Safety

Diagnosis and planning only. Non-contact tester first, one hand in pocket, panel stays closed. Read `SKILL.md` safety gates before any dead-outlet hunt.

## License

MIT © Denis Voronin
