---
name: baby-nap-navigator
description: "Use when a caregiver asks about infant/ toddler nap timing, 'wake windows', overtiredness, nap transitions, or building a daily sleep schedule from wake times. Computes age-banded wake windows, projects the next 24h of naps and bedtime, detects nap drift and late-day overtiredness, and prints a day-plan — without ever giving medical or sleep-training advice."
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [baby, infant, naps, sleep-schedule, wake-windows, parenting, caregiving]
---

# Baby Nap Navigator

## Overview

Every new parent eventually asks the same 3AM question: *"the baby woke up at 2:05 — when is the next nap?"* The answer lives in **wake windows**: the age-dependent stretch of awake time after which an infant's sleep pressure tips from "easy to settle" into "second wind cortisol spiral". Nailing the window is the difference between a 12-minute rock-to-sleep and a 45-minute scream-lullaby marathon.

This skill turns a log of wake-up times into:

1. **Age-banded wake windows** (evidence-informed ranges from the empirical tables pediatric sleep consultants use — 0–6 weeks through 2+ years).
2. **A projected next-24h schedule** — next nap start, expected length, the one after that, and a bedtime window.
3. **Drift detection** — is the morning nap creeping later day by day? (That's the classic 2→1 transition signal.)
4. **Overtiredness flags** — late-day wake windows stretched past the band produce a cortisol-second-wind warning and a "pull bedtime earlier" correction.
5. **A 7-day report** — naps per day, average lengths, night onset, and which days broke.

It is deliberately a **timing instrument, not a sleep-training method**. It never tells you to let a baby cry, never overrides a pediatrician, and bakes the safe-sleep rules (AAP: back-to-sleep, bare crib, no weighted blankets) into every printed plan.

## When to Use

- "Baby woke at 6:40, when should her first nap be?"
- "Construct today's nap schedule" / "project the next 24 hours"
- "Is he ready to drop from 3 naps to 2?" (drift analysis)
- "She's been fighting bedtime — are the naps too late?"
- Caregiver handoff: print a day plan for a grandparent/nanny
- Tracking a week of naps and getting a summary report

**Don't use for:** medical sleep problems (apnea, reflux pain, failure-to-thrive sleep disruption → pediatrician), sleep-training method selection (Ferber/Chair/whatever — out of scope by design), or night-waking feed plans for young infants (hunger-driven, not clock-driven).

## How It Works — Numbered Workflow

1. **Profile once**: record age in weeks (`log` does this automatically) and timezone-free clock times (works with any local HH:MM).
2. **Log each wake-up** (and optionally each nap start/end). The state file is a plain JSON you own — no cloud, no account.
3. **Ask `now`**: given the last wake time, print the current window (earliest–latest nap start) and the ideal start (window midpoint).
4. **Run `projections`**: simulate the rest of the day — each wake → window midpoint → age-typical nap length → next window — through a bedtime window, flagging any wake window that exceeds the band (⚠️ OVERTIRED RISK).
5. **Run `drift` weekly**: linear regression of nap-start times over the last 7–14 days per nap slot; >10 min/week creep in the morning nap + shortening second nap = transition brewing.
6. **Run `report`** for the weekly picture and hand it to whoever covers the next shift.

## Wake-Window Table (built into the script)

| Age band | Wake window (min–max) | Naps/day | Typical nap | Bedtime window |
|---|---|---|---|---|
| 0–6 wks | 45–70 min | 5–6 (chaotic) | 40–90 min | 20:30–22:00 |
| 6–12 wks | 60–90 min | 4–5 | 45–105 min | 19:30–20:30 |
| 3–5 mo | 75–120 min | 4→3 | 45–120 min | 19:00–20:00 |
| 5–7 mo | 2.0–2.75 h | 3 | 45–90 min | 18:30–19:30 |
| 7–10 mo | 2.5–3.0 h | 3→2 | 45 min–2 h | 18:30–19:30 |
| 10–14 mo | 2.75–3.5 h | 2 | 1–2 h | 18:30–19:30 |
| 14–18 mo | 3.0–4.0 h | 2→1 | 1.5–2.5 h | 19:00–20:00 |
| 18 mo–2 y | 4.5–5.5 h | 1 | 1.5–2.5 h | 19:00–20:00 |
| 2–3 y | 5.0–6.0 h | 1 (or none) | 1–2 h | 19:00–20:30 |

Read the full rationale, transition signals, and the "watch the baby, not the clock" caveats in `references/wake-window-science.md`.

## Quick Start

```bash
# one-time: age in weeks at first log
python3 scripts/nap_navigator.py log --age-weeks 22 --wake 06:50
python3 scripts/nap_navigator.py log --wake 09:35            # woke from nap 1
python3 scripts/nap_navigator.py log --wake 12:40

# what's happening right now
python3 scripts/nap_navigator.py now          # last wake + age → current window

# full day projection from the last wake
python3 scripts/nap_navigator.py projections  # next 24h schedule + OT flags

# weekly analytics
python3 scripts/nap_navigator.py drift        # nap-creep regression
python3 scripts/nap_navigator.py report       # 7-day summary
```

State lives in `nap_state.json` next to the script (override with `--state /path/x.json`). Times are your local clock; the script never fetches anything — pure offline stdlib.

## Interpreting the Output

- **Window** `14:12–15:12` means: earlier edge = drowsy-cue zone (best settle odds), later edge = cortisol risk zone. The midpoint is the default suggestion.
- **⚠ OVERTIRED RISK** on a projected window means the schedule ran long — the fix is almost always *shorten the previous nap or pull bedtime 15–20 min earlier*, not "tire the baby out more".
- **Drift verdicts**: `STABLE`, `CREPING (n min/wk) — watch for 2→1 transition`, `REGRESSION (later bedtime pressure)`.
- **Every printed plan** ends with the safe-sleep footer: baby on back, firm flat surface, nothing in the crib, room ~20–22°C, no hats/weighted items.

## Common Pitfalls

1. **Chasing the clock instead of the baby.** Windows are bands, not train times. Yawning, pink eyebrows, gaze-averting, fist-to-ear — cues beat the midpoint every time. The script says this too, because at 3AM nobody remembers.
2. **One bad nap day ≠ a schedule change.** Regressions need 3–5 consecutive days before you conclude anything. `drift` uses 7+ data points for exactly this reason.
3. **Bedtime too late "so he'll sleep in".** The classic trap: late bedtime → OT cortisol → night wakes → worse mornings. The projection pulls bedtime *earlier* on bad-nap days.
4. **Dropping a nap too early.** Most 3→2 drops happen 7–9 months, 2→1 at 13–18 months. Dropping at the first sign of a nap strike buys you a month of 35-minute naps. Check drift first.
5. **Fourth-trimester expectations.** Under ~12 weeks, circadian rhythm barely exists. The script marks this band "PATTERN-SEEKING, NOT SCHEDULING" and refuses to shame anyone.
6. **Using it as a medical device.** Snoring, pauses in breathing, feeding-pain wakes, or a baby who never sleeps more than 20 min for days → pediatrician, not a projection.

## Verification Checklist

- [ ] `log --age-weeks N --wake HH:MM` wrote `nap_state.json` (cat it)
- [ ] `now` prints a window consistent with the age band table
- [ ] `projections` lists ≥2 future events and flags any window over the band max
- [ ] `drift` prints a verdict (needs ≥3 logged days for slope; says so otherwise)
- [ ] `report` covers each logged day with nap counts and lengths
- [ ] No network calls anywhere in the script (grep for `requests|urllib|socket` — must be empty)

## One-Shot Recipes

**"She woke at 6:50, it's 8:55 and she's rubbing eyes — nap now or push?"**
```bash
python3 scripts/nap_navigator.py log --age-weeks 22 --wake 06:50
python3 scripts/nap_navigator.py now
# window 08:50–09:40 → 8:55 is inside the drowsy zone: go now.
```

**Handoff sheet for the grandmother:**
```bash
python3 scripts/nap_navigator.py log --age-weeks 30 --wake 07:05
python3 scripts/nap_navigator.py projections
# print the output; it includes cues-to-watch and the safe-sleep footer.
```

**"Is the morning nap creeping late?"**
```bash
python3 scripts/nap_navigator.py drift   # after ≥7 days of logs
```

## License & Disclaimer

MIT. Informational scheduling aid for caregivers; not medical advice, not a sleep-training program. Safe sleep per AAP guidance: infant on back, firm flat sleep surface, no loose bedding, no weighted items, room-sharing for at least the first 6 months. When in doubt about any sleep problem — call your pediatrician.
