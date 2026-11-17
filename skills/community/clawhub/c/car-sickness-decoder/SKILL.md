---
name: car-sickness-decoder
description: "Use when a child (or adult) gets carsick — before a trip to prevent it, mid-episode to manage it, or when episodes keep repeating. Classifies the trigger pattern (classic motion sickness vs vestibular migraine vs anxiety-conditioned), builds the seating/food/timing/cadence protocol, prices OTC antiemetic dosing by weight with hard age gates, and flags the red flags that need a doctor."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [carsickness, motion-sickness, family, travel, children, dosing]
---

# Car Sickness Decoder

## Overview

Motion sickness hits **children 2–12 hardest** (peak ~9 years), turns every winding road into a gamble, and gets managed badly by default: pills given after the nausea starts (too late — antihistamines work before, not during), screens handed out as a distraction (the single worst trigger), and no plan until the episode. The mechanism is a **sensory mismatch**: the vestibular system feels motion the eyes don't confirm. Every effective countermeasure — forward gaze, front-most seat, smooth driving, pre-trip meds — attacks that mismatch directly.

This skill classifies the pattern (classic kinetosis vs vestibular migraine vs conditioned/anxious anticipation — they need different plans), builds the trip protocol (seating, food, stop cadence, activity rules), prices OTC dosing by weight with hard gates (no antihistamines under 2 years, dose bands from the labels), and separates the red flags that belong to a doctor from the normal misery.

## When to Use

- A child (or adult) gets carsick on trips; you want a prevention plan instead of cleanup
- Long drive coming up (holiday, vacation) with a known carsick passenger
- Episodes escalating or happening on short drives now — is this still normal motion sickness?
- Choosing whether/how to use OTC motion-sickness meds for a child (dimenhydrinate/diphenhydramine/meclizine)
- Don't use for: vomiting with fever/dehydration (illness, not motion), vertigo at rest, post-concussion dizziness — doctor territory, and the decoder says so.

## Quick Start

```bash
# 1. What kind of carsickness is this?
python3 scripts/carsick.py triage --age 7 \
  --symptoms "pale,sweaty,nausea on winding roads, fine on highway,resolves after stop" \
  --since "always" --on-trips-only yes

# 2. Build the protocol for a 5-hour mountain drive
python3 scripts/carsick.py plan --age 7 --trip-hours 5 --winding yes

# 3. OTC dosing by weight, with gates
python3 scripts/carsick.py dose --age 7 --weight 23 --med dimenhydrinate

# 4. Episode log → trigger analysis (which seat/activity/time is dangerous)
python3 scripts/carsick.py log --csv episodes.csv
```

## Classification Table (what `triage` scores)

| Pattern | Clues | Verdict |
|---|---|---|
| Classic kinetosis | pallor + cold sweat + nausea, starts on winding/stop-go motion, age 2–12, resolves <30 min after stopping, never occurs off-vehicles | CLASSIC — protocol + optional pre-med |
| Vestibular migraine | episodes include headache, light/noise sensitivity, spinning even at rest, family history of migraine | MIGRAINE-SUSPECT — see pediatrician; protocol still helps |
| Conditioned/anticipatory | nausea starts BEFORE the drive (at the mention of it), worse with a parent's worry, history of one bad episode | CONDITIONED — graded exposure + calm framing; meds usually unnecessary |
| Red flags | hearing loss/ringing, new-onset severe headache, imbalance walking between episodes, vomiting >2 h, dehydration signs | DOCTOR NOW / same-day |

## Protocol Core (what `plan` prints)

1. **Seating**: center rear seat (most forward-facing view, least head roll) or the spot with the clearest forward view; booster so the child sees over the dashboard line.
2. **Eyes rule**: forward gaze at the horizon; NO books, NO tablets, NO phone games; audio books and music are fine (ears don't conflict — eyes do).
3. **Timing**: travel during nap/night when possible (sleep = immunity); stops every 45–60 min for 5 minutes of walking; announce turns, drive smooth (late braking is a trigger).
4. **Food**: light carbs 30–60 min before (crackers, toast); avoid greasy/acidic/heavy meals and a full stomach; cold water sips; ginger chews (moderate evidence) 30 min before.
5. **Cool air on the face**, loose clothing, no strong smells in the cabin (air fresheners, food wrappers out).
6. **If pre-medicating**: antihistamine 30–60 min BEFORE departure (they prevent, they don't rescue); bedtime dosing for night drives doubles as sleep aid — discuss with pediatrician first.

## Common Pitfalls

1. **Giving the med when nausea starts.** Dimenhydrinate/diphenhydramine prevent the signal; once vomiting has started, oral meds come back up. Dose 30–60 min before.
2. **Screens as distraction.** Reading/watching in a moving car is the classic mismatch trigger — remove, don't add.
3. **Dosing by age when weight matters.** Labels are conservative by age band; a 40 kg 8-year-old is not a 25 kg 8-year-old. The `dose` command prices both and takes the safer line.
4. **Under-2 antihistamines.** Hard gate: not recommended under 2 years — non-med protocol only, and a doctor visit if episodes are frequent.
5. **Calling escalating episodes "just carsickness."** Progression to short drives, episodes at rest, headache-dominant attacks, or hearing symptoms = pediatrician, not a bigger pill.

## Verification Checklist

- [ ] Triage verdict states the pattern class and (if red flags) the escalation route
- [ ] Plan names: seat, gaze rule, stop cadence, food timing, and travel-at-nap option
- [ ] Dose output includes weight band, timing (30–60 min before), max/day, and gates
- [ ] No antihistamine suggested for age < 2
- [ ] Caregiver told what "rescue" actually works mid-episode: stop, walk, cool air, small sips — not a pill

## Example Session

```
$ python3 scripts/carsick.py dose --age 7 --weight 23 --med dimenhydrinate

MOTION-SICKNESS DOSING — dimenhydrinate, 7 y, 23 kg
════════════════════════════════════════════════════
Label bands (age): 2–6 y: 12.5–25 mg | 6–12 y: 25–50 mg per dose
Weight check: 23 kg → age band applies (weight not out of line)
DOSE: 37.5 mg (mid-band start), 30–60 min BEFORE departure
      repeat every 6–8 h, MAX 150 mg/day
Gates: never < 2 y · drowsiness is the main effect (useful at night) ·
      don't stack with other antihistamines/cold meds ·
      check with the pediatrician for regular use
Non-med arm: ginger 0.5–1 g 30 min before (moderate evidence), acupressure
      band (weak-but-harmless evidence), front-gaze + audio-book protocol.
```
