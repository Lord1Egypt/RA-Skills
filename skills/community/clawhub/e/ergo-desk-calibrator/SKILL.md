---
name: ergo-desk-calibrator
description: "Use when setting up or fixing a home-office/desk workstation (new desk, new chair, aching neck/wrists by 3 PM, standing-desk height question) — computes your personal chair/monitor/desk numbers from body height with anthropometric proportions (seat 0.26H, desk 0.415H, seated eye 0.674H, standing elbow 0.63H), checks any monitor size for height/distance compliance, gives the laptop-compromise protocol (riser + external keyboard), maps your specific pain (neck/shoulder/wrist/eye/lower-back) to ranked likely causes with fixes, and prints the posture self-audit + 20-20-20 eye schedule."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [ergonomics, home-office, desk, posture, health, wfh]
---

# Ergo Desk Calibrator

## Overview
Almost every home desk is wrong in the same direction: the desk is too
high for the person (75 cm "standard" suits ~185 cm people — everyone
shorter hunches shoulders), the monitor sits 10-20 cm below eye line
(neck flexion), and the laptop is used flat on the desk (worst of all
worlds). The result shows up as the 3 PM neck ache, wrist tingles, and
eye fatigue that people blame on "too much computer" when it's a
geometry problem with exact numbers.

This skill computes YOUR numbers from your height using standard
anthropometric proportions, then checks your setup against them:

1. **calibrate** — height → seat height, desk height, monitor top-edge
   height above floor AND above desk, viewing distance, lumbar support
   point, keyboard slope. Standing-desk variant included.
2. **monitor** — any screen size: does its top edge land at/below your
   eye line on your desk? Riser cm needed.
3. **laptop** — the laptop compromise protocol (laptop screen + built-in
   keyboard is unsolvable; riser + external keyboard is).
4. **symptom** — pain → ranked likely causes → exact fixes.
5. **checklist** — 12-point posture self-audit + 20-20-20 eye rule
   schedule.

Pure stdlib, offline. Guidance reflects widely published ergonomic
practice (OSHA computer-workstation concepts); not medical advice —
persistent pain deserves a clinician.

## When to Use
- New desk / chair / monitor, or building a WFH corner
- "What height should my standing desk be?"
- Neck/shoulder/wrist/eye strain after work sessions
- Buying decisions: will a 27" monitor be too tall/close for my setup?
- Periodic re-check after moving furniture

**Don't use for:** clinical rehabilitation, existing RSI diagnosis
treatment (see a professional), or industrial/manual-handling ergonomics
(different domain).

## The Math (why these numbers)
Proportions of stature H (population-average, seated erect):

| Quantity | Fraction | 175 cm example |
|---|---|---|
| Seat height (popliteal + shoe allowance) | 0.26 H | 45.5 cm |
| Sitting elbow above seat | 0.155 H | 27 cm |
| **Desk (keyboard) height** | **0.415 H** | **72.6 cm** |
| Seated eye height (erect) | 0.674 H | 118 cm |
| Standing elbow height | 0.63 H | 110 cm |
| Viewing distance target | 0.38 H, clamped 50-85 cm | 66 cm |

Consequences worth knowing:
- A 75 cm fixed desk forces shoulder shrugging on everyone under ~181 cm.
- Eyes sit ~0.26 H above the desk surface → a 24" monitor's top edge on
  its lowest stand lands close to eye line; bigger monitors need
  LOWERING or more distance, not risers.
- Monitor top edge AT or slightly BELOW eye line; screen center 10-15 cm
  below eyes; never top edge above eye line.

## How It Works — Numbered Steps
1. Get your numbers:
   ```
   python3 scripts/ergo_setup.py calibrate --height 175
   python3 scripts/ergo_setup.py calibrate --height 163 --standing
   ```
2. Check a monitor against your setup:
   ```
   python3 scripts/ergo_setup.py monitor --height 175 --size 27
   ```
   → prints top-edge height above desk on a typical stand and the cm of
   riser/lowering needed to hit eye line.
3. If you work on a laptop:
   ```
   python3 scripts/ergo_setup.py laptop --height 175
   ```
4. Diagnose from symptoms:
   ```
   python3 scripts/ergo_setup.py symptom --pain neck
   python3 scripts/ergo_setup.py symptom --pain wrist
   ```
5. Audit yourself weekly:
   ```
   python3 scripts/ergo_setup.py checklist
   ```

## Common Pitfalls
1. **Desk too high is the #1 home-office error.** Fix by raising the
   chair to elbow height and adding a footrest — not by lowering the
   chair and shrugging.
2. **Monitor directly on laptop-stand height for the built-in keyboard.**
   When you raise the screen to eye level, the built-in keyboard becomes
   unusable — external keyboard + mouse are mandatory, not optional.
3. **Top edge above eye line.** Bigger monitors (27"+) frequently need
   to be LOWERED or pushed farther away; a 32" at 60 cm distance forces
   head extension. Distance target scales with screen size.
4. **Keyboard positive tilt.** Little feet folded OUT tilt keyboards
   toward you and extend wrists — keep them folded (neutral or slight
   negative tilt).
5. **Feet crossed / dangling.** Both destroy lumbar position. Footrest
   or lower chair + footrest.
6. **Static "perfect" posture.** The best posture is the NEXT posture:
   vary position; standing desk users should stand 15-30 min per hour,
   not all day.
7. **Eyes at arm's length minimum.** Closer than 50 cm forces
   accommodation strain; if you can't read at 60 cm, that's an eye
   exam, not a closer monitor.
8. **Ignoring glare.** Screen facing a window = contrast collapse and
   adopted neck twist. Screen perpendicular to windows.

## Example
```
$ ergo_setup.py calibrate --height 175
PERSONAL NUMBERS for height 175 cm (sitting):
  Chair seat height:      45.5 cm  (feet flat, knees ~90-100°)
  Desk / keyboard height: 72.6 cm  (elbows 90-110°, shoulders relaxed)
  Monitor TOP edge:       118.0 cm from floor (31.4 cm above desk)
  Screen center:          ~13 cm below eye line
  Viewing distance:       50-85 cm (target ~66 cm)
  Lumbar support:         at belt line (L4-L5), slight recline 100-110°
  Feet:                   flat on floor or footrest, never crossed

$ ergo_setup.py monitor --height 175 --size 27
27" monitor: panel height ~33.5 cm. On a lowest-stand ~5 cm above desk:
  top edge ≈ 39 cm above desk vs eye line 31 cm → 8 cm TOO HIGH.
  Fix: lower the stand; if at minimum, increase distance to ~75-80 cm
  and tilt slightly up toward eyes.
```

## Verification Checklist
- [ ] Elbows at 90-110°, shoulders relaxed (not shrugged) at keyboard
- [ ] Monitor top edge at or slightly below eye line
- [ ] Screen 50+ cm from eyes (arm's length check: press monitor —
      arm fully extended touches it)
- [ ] Feet flat, knees ~90-100°, no crossed legs
- [ ] Lumbar support contacts belt line
- [ ] Wrists neutral, keyboard feet folded
- [ ] 20-20-20: every 20 min, 20 seconds, 6 m away
