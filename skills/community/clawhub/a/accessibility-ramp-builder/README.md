# Accessibility Ramp Builder

**Problem.** A walker or wheelchair enters a family and the entry steps
become a wall overnight. People discover that "two small steps" is 20+
feet of ramp, that hardware-store portable ramps are dangerously steep,
that the yard is too short, and that the door at the top is 30 inches
wide — after buying the wrong thing. Falls on ramps are falls from
height with a person who already can't walk well.

**What it does.** `scripts/ramp_builder.py` from three measurements
(rise, yard space, door width):

- **geometry engine**: required run at the correct slope for the user
  class (1:12 self-propelled / 1:10 assisted / 1:8 walker — with the
  descending-runaway physics behind the numbers), rest platforms every
  30 in, 60×60 in landings, handrails above 6 in rise;
- **fit analysis**: straight / L-shape / 180° switchback footprints,
  and the honest DOES-NOT-FIT verdict routing to re-grading or a
  vertical platform lift;
- **door logic**: <32 in clear → swing-clear hinge fix; ≤1.5 in rise
  → $30 threshold wedge instead of a ramp;
- **audit mode**: grade any existing ramp against all three user
  classes and flag DANGEROUS;
- **lumber takeoff + cost bands** for wood / modular aluminum /
  concrete.

**Why broadly useful.** ~3.6M US adults use a wheelchair full-time and
far more use walkers after surgery or with age; every hip replacement,
stroke, and MS diagnosis in a house with steps creates this project
within weeks. The math is one afternoon, the injury risk of getting it
wrong is permanent, and nobody at the ramp store runs it for you.

**Example.**

```bash
python3 scripts/ramp_builder.py --rise 22 --use self-propelled \
    --space-ft 14 --door-width 30
# → 22 ft run at 1:12, switchback doesn't fit 14 ft, door below 32 in:
#   the two fixes (door hinges, VPL or re-grade) before any wood ships.
```

Verify local permit rules and call-before-you-dig before footings.
MIT license.
