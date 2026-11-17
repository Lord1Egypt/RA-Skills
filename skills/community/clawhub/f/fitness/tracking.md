# Tracking — Logs, Wearables, Trend Reading

Turning raw numbers into programming decisions — and knowing when a number is lying. File formats are in `memory-template.md`; the thresholds this file consumes are canonical in SKILL.md (Rule 7 deload triggers, readiness check, Red Flags RHR row).

## What Gets Logged (and what doesn't)

- Per session, in Rule 8 terms: exercise, sets x reps, load or RIR, plus a felt-state word and sleep hours. One line (`memory-template.md`); rep-by-rep granularity belongs to the `gym` skill.
- Missed sessions with reason — attendance rate and Rule 6 gap math depend on them; an empty day is ambiguous, a `missed` line is data.
- Bodyweight and waist logged for weekly-average comparison; resting HR each morning if the user has any device or a 30-second pulse count.
- Not logged: mood scores, gadget "strain" points, step counts beyond what the user already collects. Every extra field costs adherence; the log that survives is the minimal one.

## Trend Windows (the anti-noise table)

| Metric | Compare | Never react to |
|---|---|---|
| e1RM per lift | 3-4 week trend of best sets | One good or bad day |
| Bodyweight | Weekly average vs prior week | Any single weigh-in (1-2% daily water swings) |
| Resting HR | Today vs 7-morning baseline | A single morning; re-anchor after illness or time zones |
| Attendance | Rolling 4 weeks | One chaotic week |
| Cardio pace at HR | Same benchmark every 6-8 weeks | Runs in different heat, terrain, or fatigue states |

The decision thresholds these feed are canonical elsewhere: RHR 5+ bpm for 3+ mornings → Rule 7; RHR 5+ bpm a full week with performance decline → Red Flags; two flat weekly weight averages → intake or activity adjustment (SKILL.md Quick Reference: scale flat).

## Wearable Signal Quality

| Signal | Trust | Use |
|---|---|---|
| Resting HR | High | The workhorse: deload triggers, illness early warning (RHR often rises 1-2 days before symptoms) |
| Sleep duration | Decent | Readiness check input; stall diagnosis (under-7h average, canonical) |
| Sleep stages | Low | Ignore for programming; deep/REM estimates from wrist devices are unreliable |
| HRV | Medium, personal-baseline only | 7-day rolling average vs the user's own baseline; single-day HRV is noise; never compare across people or devices |
| Calorie burn | Low | Never program intake from it; deficit math routes to `calories` on intake-side numbers |
| Readiness/strain scores | Low | Proprietary blends (canonical trap): decompose to RHR + sleep hours + log before acting |

## When the Data Lies

- Alcohol, late heavy meals, heat, and dehydration all spike overnight HR and tank HRV without any training meaning — check the calendar before checking the program.
- New device or strap position change = new baseline; give any sensor 2 weeks before its numbers steer decisions.
- Manual logs drift optimistic: "3x8" with 20+ min between sets or RIR guessed generously mimics a plateau later — the log audit is step 1 of stall diagnosis (SKILL.md) for exactly this reason.
- A gap in the log is not a gap in training until confirmed — users train unlogged; ask the log question before applying Rule 6.

## Reporting Cadence to the User

- Per session: next prescription only (Rule 8 form), one line of why when the coaching register asks for it.
- Per 4 weeks: trend digest — e1RM deltas, attendance, weight trend vs phase target, one recommended change at most (one variable at a time).
- Flag proactively only on canonical triggers (Rule 7, Red Flags, two flat weeks); otherwise report when asked — data nagging trains users to ignore the coach.
