# Tracking — The Clock, the Gray Zone, and Streaks

## The Clock

- Fast start = timestamp of last caloric intake (SKILL.md rule 1). Record with UTC offset: `2026-07-22T20:00-05:00`.
- Elapsed = absolute difference between now and start. Never recompute from local wall clocks: travel and DST change the clock, not the fast. A 20:00 Chicago start read 30h later in Madrid is still 30h.
- Vague start ("after dinner"): ask once for the hour, or take their typical dinner end from memory and mark the entry `est`.
- Retroactive logging: accept it, mark `retro`; never refuse a log for being late.
- Two boundaries in one message ("ate at 8, fasting till noon tomorrow") → set start AND target in one entry; the target is their ceiling (rule 7).
- The clock has one definition in both directions: the fast closes at first caloric intake, not at the "real meal" afterward.

## What Breaks a Fast (gray-zone rulings)

Strict (default): anything above ~10 kcal or sweet-tasting breaks. Lenient: up to ~50 kcal non-sweet keeps the clock, logged flagged. A stored user ruling overrides this table for its item.

| Intake | Strict | Lenient | Note |
|---|---|---|---|
| Water, sparkling water, black coffee, plain tea | keeps | keeps | Coffee ≈2 kcal/cup — under threshold |
| Salt / unsweetened electrolyte powder | keeps | keeps | Encouraged from 24h (rule 4) |
| Prescribed medication | keeps | keeps | Never advise skipping or delaying a dose to protect a fast — that call belongs to the prescriber (`safety.md`) |
| Plain creatine (0 kcal) | keeps | keeps | Timing-agnostic (`training.md`) |
| Apple cider vinegar, lemon squeeze in water | keeps | keeps | ≈3-5 kcal, not sweet |
| Sugar-free gum, diet soda, sweetener drops | breaks (sweet taste) | keeps, flagged | The cephalic-response dispute (SKILL.md, Where Experts Disagree) |
| Splash of milk in coffee (~10-20 kcal) | breaks | keeps, flagged | The most common accidental break |
| Bone broth (~30-50 kcal/cup) | breaks | keeps, flagged | Sometimes used as an electrolyte vehicle on long fasts — still a flagged break under strict |
| Bulletproof/MCT coffee (100+ kcal) | breaks | breaks | Preserves ketosis, ends the fast — different things; say both |
| BCAAs, protein, caloric or sweetened pre-workout | breaks | breaks | Insulin-triggering by design (`training.md`) |
| Alcohol | breaks | breaks | On an empty extended-fast stomach it hits far harder — warn once |
| Anything unlisted | apply the ~10 kcal / sweet-taste test | apply the ~50 kcal non-sweet test | When in doubt: log it, flag it, let the user rule — then store the ruling |

## Streaks and Targets

- Streak = consecutive days the target was met. A 14h fast against a 16h target: log "14h completed"; the streak simply doesn't increment — no loss framing, no mention unless the user tracks streaks (rule 7).
- Window creep: logged eating windows drifting ≥1h beyond `eating_window` for 3+ days → mention once, neutrally. It is the top silent cause of "fasting stopped working" (`weight-loss.md`).
- Never infer a fast from silence (rule 2). An unlogged day is a gap in the log, not a broken fast.

## Edge Cases

- Overnight shift workers: define the day wake-to-wake; anchor the window to their sleep schedule, not the calendar date (`protocols.md`).
- Forgot to log the break: reconstruct from the first meal they mention; mark `est`.
- 5:2 and ADF are calorie protocols, not clock protocols: on fast days track the 500-600 kcal budget (`protocols.md`), not elapsed hours.
- Ramadan and dry fasts: sunset breaks the fast regardless of any hour target; observance mode changes the prompts (`religious.md`).
