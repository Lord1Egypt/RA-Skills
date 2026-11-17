# Exam Prep — When A Date Is Fixed

A deadline turns every Anki question into arithmetic. Run the capacity math before touching content: it decides whether the plan is "learn the deck" or "triage the deck", and those are different projects.

## Capacity Math (do this first)

```
days_available   = exam_date − today
usable_new_days  = days_available − 21          # maturity floor: interval >= 21 days
new_per_day      = remaining_new_cards / usable_new_days
daily_reviews    ≈ new_per_day × reviews_per_card        (SKILL.md rule 5)
minutes_per_day  = daily_reviews × seconds_per_review / 60
```

Worked example: 1,800 unseen cards, exam in 90 days, 10 reviews/card, 9 s/review.
`usable_new_days = 69` → `new/day = 26` → `daily_reviews ≈ 260` → `≈ 39 min/day`, plus the new-card learning time. Feasible.

Same deck, exam in 30 days: `usable_new_days = 9` → `new/day = 200` → `≈ 2,000 reviews/day`. Not feasible — that is the signal to cut the deck, not to try harder.

**If the number does not fit, cut cards.** In order: low-yield tags, cards you have never seen and cannot afford to mature, then whole topics you will accept losing. Deciding now beats discovering it in week three.

## The 21-Day Rule

A card first seen inside the final three weeks never reaches mature interval (`interval >= 21 days`) and is still in the high-failure young population on exam day. Consequences:

- Stop introducing new cards 21 days out for anything that must be reliable.
- Cards introduced inside that window are cram, not learning: keep them in a separate tag and expect to re-see them daily.
- The exception is pure recognition material (drug names, vocabulary lists, definitions) where a week of daily exposure genuinely holds — accept it will decay right after.

## Phase Plan

| Phase | New cards | Reviews | Settings |
|---|---|---|---|
| >21 days out | At the computed `new_per_day` | Full | Normal preset |
| 21-7 days out | 0 new | Full, protected | Leech threshold to 4; max interval capped at the days remaining so nothing schedules past the exam |
| Final week | 0 | Full + targeted filtered decks on weak tags | Consider desired retention 0.95 for exam-tagged material: expensive in reviews, and the reviews now have a deadline to justify them |
| Night before | 0 | One cram filtered deck, Reschedule OFF | Sleep beats the last 100 cards; interrupted sleep costs more recall than the session adds |
| After | Restore at half the old rate | Normal | Suspend exam-only tags, uncap max interval, restore leech threshold |

## Triage When The Deck Does Not Fit

Rank what remains by expected points per review minute, not by discomfort:

1. **High-yield tags first** — whatever the exam actually weights.
2. **Nearly-learned cards over never-seen cards.** A card at interval 5 needs one more review to hold; a new card needs four. Search: `is:review prop:ivl<10 -is:suspended`.
3. **Suspend leeches immediately.** A card that failed 4+ times in the run-up will not be learned by exam day and is eating the time of cards that would be.
4. **Suspend, do not delete.** After the exam you may want them back.
5. Cards you have never seen and cannot fit: leave suspended and read the material instead — passive exposure beats a card you will see twice.

## Filtered Decks For Cram

- Weak-area session: `deck:X tag:high-yield (rated:14:1 or prop:lapses>2)`, order by relative overdueness, Reschedule ON.
- Night-before pass: the exam tag, order random, limit to what fits the time, **Reschedule OFF** so a rushed session does not corrupt the schedule you will resume afterwards.
- Do not use `is:due` in a cram deck — it excludes exactly the cards not yet scheduled, which are the ones you are worried about.
- Empty every filtered deck after the exam so the cards return home before you restart normal study.

## Forcing A Card To Appear Before The Exam

Set Due Date on the exam-tagged selection with a range (`3-7`) so the reviews spread instead of stacking on one day. Use it sparingly and never on the whole collection: it rewrites the schedule the model learned, and after the exam you inherit the distortion.

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Adding new cards in the final two weeks | They cannot mature and they steal review time from cards that would hold | Freeze intake at 21 days |
| Raising the daily review cap to "catch up" | Rushed reviews retain poorly and burn the last week's energy | Triage the card list instead |
| A marathon the day before | Costs sleep, which costs more recall than the session adds | Cram deck with a time limit, then stop |
| Deleting cards under pressure | Irreversible decisions made while stressed | Suspend |
| Upgrading Anki or add-ons during exam term | A broken client on exam week is a self-inflicted crisis | Freeze the setup |
| Keeping desired retention at 0.95 after the exam | You inherit double the daily reviews with no deadline paying for them | Restore 0.90 and uncap max interval |
| No post-exam plan | Collections die in the week after an exam more than at any other time | Half-rate restart, suspend exam-only tags |
