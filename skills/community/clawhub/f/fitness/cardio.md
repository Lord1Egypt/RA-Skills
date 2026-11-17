# Cardio — Zones, Intervals, Concurrent Training

Endurance prescription and mixing it with lifting. Canonical numbers in SKILL.md Rule 5: the 80/20 split, Karvonen, Tanaka. Run-specific pacing and race prep route to the `running` skill.

## Zones (talk test first, HR second)

| Zone | Talk test | %HRR (Karvonen) | Role |
|---|---|---|---|
| 1 | Effortless chat | 50-60% | Recovery, warm-up |
| 2 | Full sentences, nasal breathing possible | 60-70% | The 80% — aerobic base; most weekly minutes live here |
| 3 | Phrases only | 70-80% | Gray zone — race-specific for athletes, a trap as a default (SKILL.md Traps) |
| 4 | Words | 80-90% | Threshold intervals |
| 5 | No talking | 90%+ | VO2max work, sprints |

%HRR boundaries are conventions, not physiology-exact; the talk test self-corrects for heat, caffeine, and fatigue, so when HR and talk test disagree, trust the talk test.

Worked Karvonen (formula canonical in Rule 5): age 40, resting HR 60, no measured max → HRmax = 208 − 0.7 × 40 = 180. Zone 2 = 60 + (0.60…0.70) × (180 − 60) = **132-144 bpm**. With `measured_hrmax` set, use it instead of the estimate.

## Weekly Structure

- Count the 80/20 split in minutes, not sessions — one 30-min hard session against 120 easy minutes is already 20%.
- Fewer than ~3 h/week total: intensity distribution matters little; consistency and the ACSM floor (150 min moderate) are the whole game. 80/20 starts paying at higher volumes.
- Volume ramp: +10% weekly minutes per week as a ceiling heuristic, not a target; hold volume flat any week that adds new intensity.
- Every 4th week, cut cardio volume ~30% — aligned with the lifting deload when possible so recovery weeks coincide.

## Hard-Session Menu (the 20%)

| Session | Protocol | Best for |
|---|---|---|
| Norwegian 4x4 (Helgerud) | 4 × 4 min Zone 4-5, 3 min Zone 1-2 between | VO2max, time-efficient |
| Threshold | 2-3 × 8-12 min Zone 4 low end, 3 min easy | Sustained-pace goals |
| Short sprints | 6-10 × 20-30 s near-max, full recovery (2-3 min) | Power, low weekly time budgets |

One hard session per week is the default; two only above ~4 h/week total. All hard work presumes the Red Flags table is clear.

## Modality Choice

- Zone 2 modality is fungible — bike, row, incline walk, swim all count toward the same minutes; pick by joint tolerance and boredom resistance, not by "best" lists.
- High-impact minutes (running) are a separate budget: tendons and bone adapt slower than the heart. Runners increasing mileage route to `running`; here the rule is low-impact by default when lifting volume is high.

## Concurrent Training (lifting + cardio)

Interference (Hickson): high-volume endurance work in the same muscles blunts strength and power gains — meaningful at high volumes, minor at health-floor volumes.

- Priority order: whatever `primary_goal` is trains first and fresh; the other fits around it (placement rules canonical in SKILL.md, Program Design Defaults).
- Same-day: separate by 6+ hours when schedule allows; otherwise lift first, cardio after, and keep the cardio Zone 2.
- Never hard intervals the day before the heaviest lower-body session.
- Endurance `primary_goal`: lifting drops to maintenance — 2 full-body sessions, compounds at 3-6 reps, well short of failure; strength preserved cheaply.

## Cardio Plateaus

Pace flat at the same HR, or HR creeping at the same pace:

1. Distribution audit first: gray-zone drift is the usual cause (SKILL.md Traps).
2. Distribution clean → volume has been flat for 6+ weeks: add 10% or add the second hard session, not both.
3. HR creeping at all paces plus poor sleep → treat as a recovery problem: Rule 7 logic.
