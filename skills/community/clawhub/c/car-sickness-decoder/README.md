# Car Sickness Decoder

**Stop cleaning up after carsickness — prevent it with the mismatch model.**

Motion sickness peaks in children 2–12 (worst ~9 y): pale, sweaty, miserable,
and managed badly by default — pills after nausea starts (too late), screens
as distraction (the worst trigger), no plan until the episode. The mechanism
is sensory mismatch: the inner ear feels motion the eyes don't confirm, so
every working countermeasure (forward gaze, center rear seat, smooth driving,
pre-trip meds) re-syncs the senses.

## What it does

- **`triage`** — classifies the pattern from symptom clues: CLASSIC
  KINETOSIS / VESTIBULAR-MIGRAINE-SUSPECT (headache, vertigo-at-rest,
  photo/phonophobia → pediatrician) / CONDITIONED (nausea before the trip —
  graded exposure, not pills), with hard red flags (hearing loss, imbalance
  between episodes, vomiting >2 h) routed to same-day medical care.
- **`plan`** — trip protocol: seating (center rear + booster for the horizon
  line), gaze rule (audio yes, screens no), nap/night timing, stop cadence
  (30 min on winding roads), pre-trip light-carb food + ginger, cabin air,
  smooth-driving rules, and what actually rescues mid-episode.
- **`dose`** — label-band OTC dosing (dimenhydrinate/diphenhydramine/meclizine)
  with weight-vs-age sanity check, 30–60 min BEFORE timing, per-day maximums,
  hard gates (nothing under 2 y; meclizine ≥12 y; no stacking).
- **`log`** — episode CSV analyzer: dominant seat/activity/hour = your trigger
  conditions; severity trend flags when to escalate.

## Who needs this

Families with a carsick child planning any drive over 30 minutes, adults
with motion sickness, and caregivers deciding whether meds are appropriate.

## Usage

```bash
python3 scripts/carsick.py triage --age 7 \
  --symptoms "pale,sweaty,nausea on winding roads, fine on highway, resolves after stop"
python3 scripts/carsick.py plan --age 7 --trip-hours 5 --winding --history
python3 scripts/carsick.py dose --age 7 --weight 23 --med dimenhydrinate
python3 scripts/carsick.py log --csv episodes.csv
```

Mechanism + classification + full dosing table: `references/motion-sickness-guide.md`.

## License

MIT © 2026 Denis Voronin
