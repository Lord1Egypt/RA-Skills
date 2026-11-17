---
name: garage-door-safety-audit
description: Use when auditing garage door safety, planning spring/opener maintenance, or after a door fails to reverse, jams, or drops — CPSC-injury-class hazard audit, auto-reverse 2x4 test protocol, spring cycle-life math with replace-by dates, and service-now verdicts.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [garage-door, home-safety, springs, maintenance, opener-reverse]
---

# Garage Door Safety Audit

## Overview
A garage door is the largest moving object in most homes — 130–180 kg of steel or wood suspended over your car, kids, and pets, held up by springs under lethal tension. US emergency rooms treat ~30,000 garage-door injuries per year (CPSC estimate), and a door that fails to auto-reverse has killed children as recently as the 2010s. Yet almost nobody tests the reverse system — it takes 90 seconds with a roll of paper towels.

This skill is a two-part instrument: (1) a **safety audit** — the 2×4 auto-reverse test, photo-eye check, force settings, pinch points, and control placement, each with pass/fail logging; (2) a **cycle-life forecaster** — torsion/extension springs are wear parts rated in cycles (10k/20k/33k), and from your daily opening count the tool computes remaining spring life % and a dated replace-by window so you schedule replacement *before* the 7 PM crash-and-stuck event.

## When to Use
- New home, rental turnover, or child/grandchild now has garage access
- Door "seems heavy", opener strains, or reverses for no reason mid-travel
- Planning maintenance budget; want to know if springs are near end of life
- After any auto-reverse failure, spring snap, cable fray, or photo-eye fault
- Teaching household members the manual-release and keypad safety rules

**Don't use for:** doors already off their tracks, snapped torsion springs (cable under tension), or any visible cable/spring damage — those are STOP-and-call-pro technician situations, covered in the DANGER section below.

## Quick Start
```bash
# 1. Register the door (installed year + openings per day guess)
python3 scripts/garage_door_audit.py init --installed 2018 --openings 4 --rating 10000

# 2. Run the 90-second safety test protocol (interactive checklist)
python3 scripts/garage_door_audit.py audit

# 3. Log a real auto-reverse test result (2x4 flat under the closing door)
python3 scripts/garage_door_audit.py log-test --test reverse_2x4 --result pass

# 4. Current status: spring life %, replace-by date, open safety issues
python3 scripts/garage_door_audit.py status
```

## The 90-Second Safety Test (do this twice a year)
1. **Contact reverse (2×4 test):** place a 2×4 (or thick rolled towel) flat on the floor, centered under the door. Close the door with the remote. The door MUST touch the wood and reverse within 2 seconds. A door that crushes the board and keeps pushing FAILS — adjust opener force/down-limit or replace the opener if pre-1993.
2. **Photo-eye (non-contact):** press close, then sweep your broomstick vertically through the beam path ~5 cm off the floor. The door must reverse immediately. Never test with a hand, child, or pet.
3. **Force check by hand:** with the opener disengaged (manual release), the door should lift with one hand effort and stay at any half-open position. Drifting down = spring imbalance → technician.
4. **Manual release drill:** every adult should pull the red release once (door closed!) and hand-lift once — this is how you get the car out during a power outage.
5. **Wall button height:** must be ≥ 5 ft / 1.5 m, out of children's reach, in sight of the door. Never let kids race the closing door.

## Spring Cycle Math (how the script thinks)
- 1 cycle = 1 open + 1 close. Standard residential springs: **10,000 cycles** (budget), 20k (standard 4-lift), 33k+ (long-life/high-lift).
- Daily cycles ≈ 2 × vehicle trips (each departure + return) + pedestrian use. 4 openings/day = 1,460 cycles/yr → a 10k spring lasts ~6.8 years from install.
- Springs installed as a **pair age together**: when one snaps, replace both. The second is always months behind.
- Remaining life < 20% → schedule replacement on your terms; < 10% or > rating → replace now (a snapping extension spring can spear through drywall; torsion failures drop the door instantly).

## DANGER — Call a Pro, Do Not DIY
- **Torsion springs** (above the door, on a shaft, with drums and winding cones): adjusting them means loading a steel bar against stored energy that can break arms and skulls. Pro-only, typically $150–$350 for a pair.
- **Snapped cables, off-track door, door stuck open**: the door is an uncontrolled load. Don't force it; don't disengage the opener on an open stuck door — it will fall.
- **Pre-1993 openers** (no photo-eyes, dip-switch remotes): not repairable to modern safety standard — replace the opener, and destroy old remotes (they open your neighbors' doors too).

## Anti-Features (things that sound fine and aren't)
- **Lubricating with WD-40**: it's a solvent, not a lube. Use lithium/ silicone spray on hinges, rollers (non-nylon), and spring coils — twice a year, 10 minutes.
- **Extending opener run time to "fix" reversing**: that's defeating a safety feature. Fix the force setting limit or the binding point instead.
- **Leaving the manual release dangling**: a child-pullable handle. Shorten the rope to adult reach.
- **Keypad code 1234 or house number**: garage keypads are the most brute-forced entry point in suburbia. 6-digit random code, changed at move-in.

## Security Addendum
- Remote = car key. Don't leave remotes in parked cars on the driveway.
- Modern openers use rolling codes (pre-1996 fixed-code remotes are code-grabbable).
- Vacation lock switch on the wall console disables all remotes while traveling.

## Common Pitfalls
1. **Never testing auto-reverse** — the #1 failure mode; sun misalignment, dirty lenses, and force drift make it fail silently over years.
2. **Replacing one spring of a pair** — you will pay the labor twice within a year.
3. **Reading "10-year warranty" as door life** — warranty counts cycles, not years, and labor is never included.
4. **Nylon roller + lithium grease** — nylon rollers run dry; greasing them gums up.
5. **Testing photo-eye by hand or foot** — always a broomstick. The 2-second reverse assumption is what you're testing, not trusting.

## Verification Checklist
- [ ] Registry file exists (`garage_door.json`) with installed year and rating
- [ ] 2×4 reverse test logged within the last 6 months (PASS)
- [ ] Photo-eye sweep test logged (PASS)
- [ ] Spring remaining-life % > 20% or replacement scheduled
- [ ] Manual-release drill done by every driving adult in the house

## Example Session
```
$ python3 scripts/garage_door_audit.py init --installed 2018 --openings 5 --rating 10000
Door registered: installed 2018, 10,000-cycle springs, ~5 openings/day.
$ python3 scripts/garage_door_audit.py status
Cycles used: ~13,875 of 10,000 (139%) — OVERRUN
Verdict: REPLACE SPRINGS NOW (probability of failure high; pair replacement)
Safety issues open: reverse_2x4=FAIL (2026-08-02) → adjust down-force, retest
```
