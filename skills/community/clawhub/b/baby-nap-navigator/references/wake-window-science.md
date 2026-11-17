# Wake-Window Science & Nap Transitions — Reference

## 1. Where the bands come from

The table in SKILL.md is a synthesis of the empirical bands used across pediatric-sleep practice: the ranges popularized by Ferber's clinical work, the Weissbluth "90-minute-ish" observation for young infants, and the age-band tables used by certified pediatric sleep consultants (commonly attributed to Kim West / "Happy Sleepers" lineages). No single lab study defines "the wake window"; the bands are the distillation of decades of clinical observation of when settling difficulty curves bottom out. Treat them as priors, not physics.

Key structural facts:

- **Sleep pressure in infants is homeostatic + circadian.** Before ~10–12 weeks the circadian signal is nearly absent (no melatonin rhythm yet); naps are driven almost purely by accumulated wake time. This is why young infants *can* nap every 60–90 minutes around the clock, and why "scheduling" a 4-week-old is a category error.
- **The wake window grows across the day.** Morning window is the shortest; the pre-bedtime window is the longest the child can sustain (roughly 1.2–1.4× the morning window). The script uses the band midpoint for daytime naps and the band max for the final window.
- **Overshoot produces a second wind.** Past the window max, cortisol and adrenaline rise to keep the tired infant awake — the classic "wired at bedtime" presentation. The correction is earlier bedtime, never more stimulation.

## 2. Age-band mechanics (what changes and when)

**0–6 weeks — pattern-seeking.** Naps are 40–90 min, 5–6 a day, randomly distributed. Goal: feed-wake-sleep cycles, daylight exposure during day, dark+quiet at night to start seeding the circadian clock. Never diagnose a "schedule problem" here.

**6–12 weeks — social smiling, rhythm begins.** Morning nap starts to anchor (~9:00). 4–5 naps. Night onset pulls earlier toward 20:00. First realistic "schedule" appears late in this band.

**3–5 months — the 4-nap structure.** Naps 1–2 are the "restorative" pair (morning ~9:00, midday ~12:30); naps 3–4 are 30–45-min "bonus" naps (catnaps). Bedtime window 19:00–20:00. The 4→3 drop happens when the third nap start pushes past ~17:00 — you pull bedtime 15 min earlier instead.

**5–7 months — 3 solid naps.** Windows 2–2.75 h. The third nap is deliberate and short (cap ~45 min if it runs long and threatens bedtime).

**7–10 months — the 3→2 transition zone.** Signals, in order of reliability:
1. Third nap refused ≥5 days in a row (not illness/vacation days)
2. Morning nap start creeping later >10 min/week (drift output)
3. Morning nap lengthening past 90 min (consolidation)
4. Bedtime battles on 3-nap days

Method: cold-drop nap 3, pull bedtime 20 min earlier for a week, expect a rough 7–10 days.

**10–14 months — 2 naps stable.** ~9:00 and ~13:00, 1–2 h each. Ideal balance point of the whole chart.

**14–18 months — the 2→1 transition** (average ~15.5 months). Signals: afternoon nap refused repeatedly, morning nap starting later AND lasting longer, night waking appearing with no other cause, early-morning wakes. Method options: cold turkey to a midday nap (~11:30–12:00 start, cap 2.5 h) or a 2–3 week "bridging" period alternating 1-nap and 2-nap days by morning wake time/night quality. Bridging is gentler for daycares; cold turkey is cleaner for home.

**18 months–3 years — single midday nap**, then gradually resisted. Keep "quiet time" after the nap drops entirely; ~25% of children drop the nap by age 3, most by 3.5–4. A dropped nap that produces evening meltdowns for >2 weeks was dropped too early — reinstate a short car/stroller nap.

## 3. Reading the drift analysis

The script regresses each nap slot's start-time-of-day (in minutes from midnight) on day number over the logged window:

- **Slope > +10 min/week on nap 1** with **shortening nap 2** → transition brewing (2→1 or 3→2 depending on age band).
- **Slope < −10 min/week (earlier)** → usually chronic undertired-at-bedtime or an early-wake phase; check morning light exposure and bedtime placement.
- **Slope ≈ 0 but high variance** → environment problem (noise, light, daycare commotion), not a schedule problem.

Minimum 7 days of data before a verdict; 10–14 is better. Illness, travel, and vaccination days are noise — the report marks days with <2 logged naps as PARTIAL and drift excludes them when flagged `--clean`.

## 4. Overtiredness — the feedback loop

The failure mode every caregiver meets once:

```
late nap → overtired by bedtime → cortisol second wind → late bedtime
→ night wakes → early morning wake → short/late first nap → repeat
```

The exit is counterintuitive: **pull bedtime EARLIER** (15–30 min), sometimes for 3–4 nights, until night onset stabilizes. The projections command enforces this: any day whose final projected window exceeds the band max gets an ⚠ flag and an "earlier bedtime" correction line.

## 5. Cues beat clocks (the operating rule)

The window tells you when to *start watching*; the cues tell you when to *act*:

- **Early/drowsy zone**: decreased activity, slower sucking, quieter, eyes less focused, yawning
- **Mid window**: rubbing eyes/ears, fist in mouth past hunger, pink eyebrows, gaze aversion
- **Past max**: arching, fussiness spike, hyperactive "wired" state — you're now settling against the cortisol tide

The script prints the cue list with every projection because the person running it at 3AM is running on no sleep either.

## 6. Safe sleep (non-negotiable, every plan footer)

Per AAP (2022 policy reaffirmed):

- Infant on their **back** for every sleep, every caregiver, every time, until 1 year.
- **Firm, flat, non-inclined** surface; no car seats/rockers/bouncers for routine sleep.
- **Nothing in the sleep space**: no pillows, blankets, bumpers, toys, or weighted items.
- Room-sharing (same room, separate surface) ≥6 months.
- Avoid overheating; room ~20–22°C / 68–72°F; no hats indoors.
- Swaddling stops at the first roll attempt; then arms-free sleep sack.
- Pacifiers at sleep onset are fine once breastfeeding is established.

## 7. Red flags that exit this skill's scope immediately

- Snoring, mouth-breathing, pauses in breathing → airway evaluation
- Painful waking with back-arching, sour burps → reflux, see pediatrician
- Sleep disrupted with poor weight gain/feeding → pediatrician promptly
- Head-banging that leaves marks, or any breathing irregularity → pediatrician
- Sudden regression with fever/illness → treat the illness; fix sleep after

This tool computes *when*. Anything about *why a child can't* belongs to a clinician.
