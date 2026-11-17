# Retention — Diagnosing A Deck That Is Not Working

Work symptom-first. Each chain below is ordered by probability, and every step is a measurement, not a guess.

## The Universal First Three

1. **True retention**, not "retention rate". Stats shows a True Retention table (`anki >=24.11`; older versions need an add-on). Read the **mature** row — cards with `interval >= 21 days`. Young cards fail often by design and drown the signal.
2. **Again-rate by deck**, not overall. One deck of badly written cards can sink the whole collection's number while the rest is healthy. Compare decks before touching any setting.
3. **Review count vs card count**. Total reviews ÷ total cards is `reviews_per_card` — the multiplier in every workload estimate (SKILL.md rule 5). Rising over time means cards are failing and re-entering learning.

## Reviews Per Day Keep Climbing

1. Arithmetic first: `new_per_day × reviews_per_card` (SKILL.md Workload Math). If today's count is below that product, the deck is still growing into its steady state — the climb is scheduled, not pathological.
2. Check Stats → Future Due. A rising slope with new cards still enabled = intake problem: cut `new_per_day`, and the curve flattens after roughly one interval cycle, not overnight.
3. If intake is already 0 and reviews still climb, cards are lapsing back into learning: go to the low-retention chain below.
4. Under SM-2, check the ease distribution (`prop:ease<2.0` in Browse) — an ease-hell population reviews several times more often than a healthy one at the same card count.
5. Last: desired retention set high (0.95+) genuinely costs roughly double the reviews of 0.90. Price it in the deck-options simulator before assuming it is the culprit.

## Retention Below Target

Target = whatever you set as desired retention (default 0.90); measured mature retention should land within a few points of it.

1. **Grading drift** (most common, always check first). Habitual Hard on passing cards or Again on "knew it, said it slowly" makes the model over-schedule and your number lie. Re-read SKILL.md The Four Buttons; correct the habit, then wait two weeks before measuring again.
2. **Card quality**, second. Sort Browse by lapses (`prop:lapses>3`): if the failures concentrate in a few dozen cards, this is a writing problem, not a memory problem.
3. **Interference**, third: the failing cards look like each other. The fix is a discriminator on both twins, not a smaller interval.
4. **Material not understood** when the failing cards share a topic. Cards cannot install understanding; study the topic and then rewrite them.
5. **Stale FSRS parameters** last: if the collection changed a lot since the last Optimize (new subject, new grading standard), the model is fitting an old you.

## Retention Suspiciously High (0.95+ unplanned)

Not a win — you are paying reviews for recall you already had.

- Intervals too short for the material: raise desired retention's inverse, i.e. LOWER desired retention toward 0.90 and let intervals stretch.
- Cards below your knowledge floor: `prop:reps>8` with zero lapses is a delete list (SKILL.md Card Diseases).
- Easy-button farming inflates the number without the memory. Compare against the mature row only.

## Ease Hell (SM-2 only)

The spiral: fail → ease −20pp → shorter interval → fail again → ease bottoms out at 130% → the card returns every few days forever.

- **The two numbers, reconciled** (canonical home for both): the ease-hell population itself sits in the **core band 130-180%**; you screen for it with **`prop:ease<2.0`** (=200%), deliberately wider so cards on the way down are caught before they bottom out. Band = the diagnosis, `<2.0` = the query. Every other file quotes these two, never a third number.
- **Detection**: a cluster of cards inside that band, reviews dominated by the same faces, and acceptable overall retention with an exploding review count.
- **Fix order**: (1) switch that preset to FSRS — it has no ease factor and rebuilds the schedule from the same history; (2) if staying on SM-2, rewrite the offending cards first, because ease dropped for a reason; (3) only then reset ease to 250% in Browse for the cluster.
- Resetting ease without fixing the cards recreates the spiral in about a month, with the added cost of the reset.
- FSRS's analogue is a high difficulty value, but it does not spiral: difficulty rises and falls with performance, and intervals stay proportional to measured stability.

## Leeches

Threshold 8 lapses (default). A collection is healthy at roughly 1-2% of cards tagged leech; past ~5% the problem is card writing, not memory.

1. Find them: `tag:leech`.
2. Classify each in one pass — wording, interference, hidden list, or genuinely not understood. The class determines the fix; skipping this step produces rewrites that fail the same way.
3. Rewrite — split a hidden list into one card per item, add the discriminator to both twins of an interfering pair, or add the context prefix (SKILL.md rule 2) — then **reset the history** so the scheduler stops carrying the old difficulty, and remove the leech tag.
4. Suspend anything you cannot fix today. A suspended leech costs nothing; a live one costs minutes every week.
5. Measure the fix: tag the rewrite batch and check its Again-rate in a month. Rewrites that did not help mean the fact needs understanding, not carding.

## Backlog Recovery

Applies after a holiday, an illness, or a bad month. The order is what makes it work.

1. **New cards to 0** across affected presets. This is what stops tomorrow's inflow; everything else is bailing.
2. **Cap reviews** at a number you will finish daily — typically 100-200, or whatever `minutes_available × 60 / seconds_per_review` yields (SKILL.md Workload Math). A cap you meet daily beats an uncapped queue you avoid.
3. **Burn down oldest-first**: set the deck's review sort order to descending overdue-ness so the most-forgotten cards come back first.
4. **Project the end**: `days_to_clear ≈ backlog / (cap − incoming_due)`. If that number is negative, the cap is too low or the collection is too big — cut cards, do not raise the cap.
5. **Do not reschedule the backlog away** with Set Due Date across thousands of cards. It hides the debt and destroys the review history FSRS needs. The exception is a hard deadline where the backlog cannot be cleared honestly.
6. Restore new cards only after the queue is stable for a week, and restore at half the old rate.

## Reading The Stats Screen

| Panel | What to read | What it means |
|---|---|---|
| True Retention | Mature row, month column | The only retention number worth acting on |
| Answer Buttons | Again share on review cards | Your effective failure rate; drift here explains most bad numbers |
| Future Due | Slope and the tallest bar | A rising slope with new cards on = intake exceeds throughput |
| Card Counts | Suspended and new totals | A big new pile is a decision you have not made yet, not a backlog |
| Review Intervals | Spike at the low end | Ease hell (SM-2) or a lapse cluster (FSRS) |
| Difficulty (FSRS) | Right-hand tail | Where the rewrite candidates live |
| Calendar / heatmap | Gaps, not totals | Consistency drives retention more than session length |
| Hourly breakdown | Retention by hour | If one hour is much worse, you are studying while unable to concentrate |

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Reading overall retention instead of mature | Young cards fail by design and mask the real number | Mature row only |
| Changing several settings at once | The result is uninterpretable and usually gets reverted wholesale | One change, two weeks |
| "Forget" on everything that feels shaky | Destroys history, resets the model, and adds a wave of new-card load | Rewrite the specific bad cards |
| Marathon sessions to catch up | Retention on rushed reviews is poor, so the cards come back sooner | Fixed daily cap |
| Treating a bad week as a settings problem | Life happens; the collection is fine | Recover the routine before touching options |
