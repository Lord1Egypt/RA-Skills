# Scheduling — Deck Options Without Guesswork

Every number below is a default you can read on screen. Change one at a time and give it two weeks; changing four settings at once makes the result uninterpretable.

## Defaults Worth Knowing By Heart

| Setting | Default | What moving it does |
|---|---|---|
| New cards/day | 20 | Sets steady-state workload: `new/day × reviews_per_card` (SKILL.md rule 5) |
| Maximum reviews/day | 200 | A cap, not a target. In the v3 scheduler it limits the whole day, new cards included, unless "new cards ignore review limit" is on |
| Learning steps | 1m 10m | Two exposures before graduation. More steps ≠ better retention; they only delay the first real interval |
| Graduating interval | 1 day | Interval after the last learning step |
| Easy interval | 4 days | Interval when Easy is pressed during learning |
| Relearning steps | 10m | Path back after a lapse |
| Leech threshold | 8 lapses | Tags (and optionally suspends) the card — SKILL.md rule 4 |
| Maximum interval | 36500 days | Cap it at 365 only when a real deadline exists |
| Desired retention (FSRS) | 0.90 | The workload dial (SKILL.md rule 6) |
| Starting ease (SM-2) | 250% | Only exists under SM-2; FSRS has no ease factor |

SM-2 button arithmetic, for collections not yet on FSRS: Again → ease −20pp and the card relearns; Hard → ease −15pp, interval ×1.2; Good → interval × ease; Easy → ease +15pp, interval × ease × 1.3 (easy bonus). Minimum ease is 130%, which is what makes ease hell a one-way street.

## FSRS: The Five Moves

FSRS is built into Anki (`anki >=23.10`) and replaces ease factors with a per-card model of stability and difficulty.

1. **Turn it on** per preset in deck options. Existing history is reused; nothing is lost.
2. **Optimize** to fit the parameters to your own reviews. With only a few hundred reviews the optimizer has nothing to fit and keeps the defaults — that is fine, run it again later. Re-optimize every couple of months, or after a large batch of new material or a change in grading habits.
3. **Set desired retention deliberately.** 0.90 default; the deck-options simulator projects reviews/day and retention from your history for a candidate value — run it rather than guessing (SKILL.md rule 6).
4. **Decide about rescheduling.** "Reschedule cards on change" rewrites due dates of existing cards to match the new model. Leave it OFF for a routine optimize (the change lands gradually as cards come up); turn it ON only when you deliberately want the whole backlog redistributed, and expect a due-count spike that day.
5. **Shorten learning steps.** Steps of a day or more override FSRS's own first intervals. Keep steps under a day — `1m 10m` is a fine permanent answer, and a single `1m` step is defensible for easy material.

Separate presets get separately optimized parameters. That is the reason to split presets by material type (vocabulary vs reasoning), not by deck name.

## Daily Limits That Behave

- Limits belong to the **preset**, and the v3 scheduler applies the limits of the deck you clicked: study from the parent and the parent's limits govern, no matter what the subdecks allow. "My subdeck says 20 new and I get 5" is this.
- "This deck / Today only / Preset" scoping exists in the limits UI: use **Today only** for a one-off catch-up so you do not permanently raise a limit you meant to raise once.
- New cards ignore the review limit only if you enable that option; otherwise a review-heavy day starves new cards with no notice, which is usually the correct behaviour.
- The **learn-ahead limit** (Preferences, default 20 minutes) is why cards from learning steps appear early when nothing else is due — it is not a scheduling bug.

## Display Order (the sibling and interference lever)

- **Bury new siblings / bury review siblings**: on. Two cards from the same note on the same day means the first one answers the second. Buried cards return the next day automatically.
- **New card gather order**: `deck` keeps subdecks sequential (a syllabus); `ascending position` follows the order cards were added; `random notes` breaks up material that entered together.
- **New/review order**: putting reviews first protects retention on days you quit early — the reviews are the memory you already paid for; new cards are optional.
- **Interday learning first** keeps relearning cards from being pushed past the day boundary when the queue is long.

## Leech Handling

Threshold 8 (default). The action is `Tag Only` or `Suspend`:

- Tag Only for material you must eventually know (boards, core vocabulary) — the tag becomes your rewrite queue (`tag:leech -is:suspended` in Browse).
- Suspend for optional material — it removes the daily cost immediately and you decide later.
- Halve the threshold to 4 during a deadline sprint: a card failing four times before an exam will not be learned by exam day and is stealing time from cards that will.

## Deck Presets

- A preset is a named settings bundle used by many decks. Read the preset name at the top of deck options and its "used by" count before editing (SKILL.md rule 7).
- Useful preset split: **Default** (everything), **Vocabulary** (higher new/day, short steps), **Heavy** (reasoning-dense cards, lower new/day), **Paused** (new = 0, for material on hold). Four presets covers almost every collection; twenty presets is the same problem as twenty note types.
- Save-menu options (Save to all subdecks) apply the preset downward in one action; use it after restructuring decks.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Long learning steps (`1m 10m 1d 3d`) | You hand scheduling back to fixed steps and disable the model's judgment | Steps under a day; let FSRS pick the rest |
| Raising max reviews/day to clear a backlog | The backlog reappears tomorrow, plus burnout | Set new to 0 and burn down at a fixed cap |
| Optimizing after every session | Parameters wobble on tiny increments of data and you learn nothing from the noise | Every couple of months, or after a large behaviour change |
| Reschedule-on-change enabled by habit | An unexpected due spike lands on a day you did not plan for | Leave off unless the redistribution is the goal |
| Max interval of 21 days "to keep things fresh" | Every card returns forever; the collection becomes a treadmill | Cap only against a real date, and lift the cap after |
| Copying a stranger's FSRS parameters | Parameters model that person's memory and grading habits | Optimize on your own history |
