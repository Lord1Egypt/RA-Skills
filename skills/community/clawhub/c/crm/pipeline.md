# Pipeline — Stages, Stalls, and a Forecast You Can Defend

A pipeline is a claim about the future made in public. Everything here exists to make that claim survive contact with the quarter.

**Contents:** [When A Lead Becomes A Deal](#when-a-lead-becomes-a-deal) · [Stage Discipline](#stage-discipline) · [What "Value" Means](#what-value-means) · [The Stall Protocol](#the-stall-protocol) · [Close Dates And Slippage](#close-dates-and-slippage) · [Forecast Math](#forecast-math) · [The Weekly Review](#the-weekly-review) · [Razor Questions](#razor-questions) · [Losing Well](#losing-well) · [Multiple Pipelines](#multiple-pipelines) · [Renewals And Expansion](#renewals-and-expansion)

**Before answering any pipeline, forecast or "how are we doing" question**, read `## Pipeline` in `~/Clawic/data/crm/memory.md` — or `deals.md` if the `## Boxes` index points there — plus `closed-deals.md` for the rates. A forecast computed without the closed history is the tool's default probabilities wearing a suit.

## When A Lead Becomes A Deal

A deal exists when there is **something specific being bought, by someone who can buy it, on a timeframe either side has named**. Before that it is a contact with a next step.

Creating deals too early is the most common way to ruin a pipeline: coverage looks healthy, conversion rates collapse, and the stalled list becomes so long nobody reads it. Creating them too late loses the one thing worth measuring — how long qualification actually takes.

Test: could you write the deal's value and close date without inventing both? Yes → deal. No → contact with a next step (`followup.md`).

## Stage Discipline

The exit criteria table lives in `SKILL.md`; this is what enforcing it looks like.

- **Stages describe the buyer's progress, not yours.** Rename any stage whose name is a verb you perform ("Proposal sent", "Contacted") to the buyer's state ("Proposal under review").
- **One stage moves at a time, and the date moves with it.** `stage_entered` is what makes stall detection and cycle-length reporting possible; overwriting a stage without it destroys both.
- **Backward movement is legal and informative.** A deal that returns to Qualified because the champion left is honest data. A deal that stays at Negotiation for two months because moving it back feels like failure is a lie that will be discovered at quarter end.
- **Skipping is fine, back-dating is not** (SKILL.md).
- **Cap the stage count at six.** Every added stage divides your sample, and conversion rates need volume to mean anything (`metrics.md`).

## What "Value" Means

Pick one definition, write it in `## System`, and never mix two in one number.

| Definition | What it counts | Use when |
|---|---|---|
| First-year value | Year one only, recurring plus one-off | Default for most subscription and retainer work — comparable across deal types |
| TCV (total contract value) | Whole committed term | Multi-year contracts, board reporting |
| ARR / MRR | Recurring only, annualized or monthly | The business is a subscription and one-offs are noise |
| Gross margin value | Value minus pass-through cost | Agencies and resellers, where a 50,000 EUR deal can carry 6,000 EUR of margin |

Rules that keep the number honest: recurring values carry their period in the cell (`2400 EUR/mo`); currency always in the value (`memory-template.md`); a range gets stored as its low end, never its midpoint, because midpoints are how a pipeline inflates 20% without anyone lying.

## The Stall Protocol

A deal is stalled when **any** of these is true: no next step, next-step date in the past, or `stage_entered` older than `stall_days` (default 21).

At every review, each stalled deal takes exactly one of three exits — no fourth option, and never "leave it for next week":

1. **Revive** — a new next step with a date, agreed *with the buyer*, not chosen by you. An internal action ("follow up again") is not a next step.
2. **Regress** — back to the stage whose exit criterion actually holds. Usually Qualified, usually because the budget owner was never confirmed.
3. **Close lost** with a reason. Including the reason that matters most: **no decision**, which in most pipelines beats every named competitor combined.

The breakup message is a tool of the protocol, not a courtesy: after two unanswered attempts, one message that makes closing the file the easy reply ("assuming this is not a priority this quarter — I will close it out unless you say otherwise") gets a response rate that no third "just checking in" does. Two replies to that message are both wins: a revival, or a clean lost.

## Close Dates And Slippage

- The close date belongs to the **buyer's** timeline: their budget cycle, their launch, their contract end. A date derived from your quarter end is a wish.
- **Never overwrite silently.** Keep the previous date and the day it moved (`memory-template.md`). Two slips on one deal means the qualification was wrong, not the calendar (SKILL.md Rule 7).
- **Measure your own slippage and apply it.** `median_slip_days` over the last ~20 closed deals is the correction every forecast date needs. If half of last quarter's deals slipped a median of 18 days, a deal dated for the 25th is a next-month deal.
- A close date more than one full sales cycle away is a placeholder. Mark it as such rather than letting it anchor a forecast.

## Forecast Math

Three numbers, each computed from your own history, none from the tool's defaults.

**Weighted pipeline.** `Σ (deal value × conversion rate of its current stage)`, where the conversion rate is measured from `closed-deals.md`: of deals that ever reached this stage, what fraction were won. A tool's stock "Proposal = 60%" against a measured 25% overstates that slice by 2.4×.

**Required coverage.** `required_coverage = 1 / win_rate`. The famous "3× pipeline" is simply a 33% win rate restated — at a measured 20% win rate you need 5× your target in open pipeline, and at 50% you need 2×. Coverage below the required ratio is a prospecting problem this quarter, whatever the deals in it look like.

**Pipeline velocity.** `(qualified deals × average deal value × win rate) ÷ average cycle length in days` = revenue per day. Its value is diagnostic, not predictive: it names which of the four levers is cheapest to move. Halving cycle length doubles velocity exactly as much as doubling deal count, and is usually the one you control (`metrics.md`).

**Commit / best case / pipeline.** Below roughly 20 deals per period, weighting is noise: call each deal instead. *Commit* = you would bet your quarter on it, evidence in writing. *Best case* = plausible with a specific thing going right, named. *Pipeline* = everything else. A commit deal that slips is a process defect worth a teardown, not a rounding error.

## The Weekly Review

Twenty minutes, on `review_day`, in this order — the order matters because it puts the money-losing items before the pleasant ones:

1. **Stalled list first** (above). Every one takes an exit.
2. **Close dates inside the next 30 days**: is the exit criterion of the *current* stage actually met? If not, the date is wrong today, not at month end.
3. **Deals with no interaction in 14 days**: those are stalls that have not aged into the rule yet.
4. **New deals since last review**: value defined, source set, primary contact named, next step dated.
5. **Coverage against target** using the formula above; a shortfall is prospecting work booked this week, not a note.
6. **One closed deal, won or lost**, read aloud from `closed-deals.md`. This is what keeps the reason codes honest.

**Write the result in the same turn**: stage changes and next steps to `## Pipeline` (or `deals.md`), closed deals moved to `closed-deals.md` with reason, cycle and slips, and the review's date into `## Due` (`memory-template.md`). A review whose output is a feeling gets skipped next week.

## Razor Questions

Four questions that end most pipeline arguments. Any "no" is the deal's real stage.

- **Who signs, and have they been in a conversation?** Not "who did we meet" — who signs. A deal whose signer has never appeared is at Qualified regardless of the quotes exchanged.
- **What happens to them if they do nothing?** If the honest answer is "nothing much", the competitor is no-decision and no discount fixes it.
- **What is the next thing *they* do?** If every next action on the list is yours, there is no deal, there is a pursuit.
- **How did the last three deals that looked like this end?** `closed-deals.md` answers it in ten seconds, which is the entire reason that file exists.

## Losing Well

- Record the reason from the closed list the same day, while the reason is still true. A week later, every loss becomes "price".
- Ask the question that gets answered: not "why did we lose" but **"what would we have had to do differently, and when?"** — it produces a stage, not a sentiment.
- **No-decision losses get their own reason code.** Merging them into "price" hides the qualification defect that produced them, and they are usually the largest single bucket.
- A loss to an in-house build is a positioning result, not a pricing one; a loss on timing gets a dated re-open next step in `followup.md`, which is the highest-conversion source of pipeline most solo operators have.
- After a loss that mattered, write `artifacts/win-loss-<org>.md` with the turning point and the repeatable lesson, and index it (`memory-template.md`).

## Multiple Pipelines

Split into a second pipeline only when the **stages differ**, never when the deals merely differ in size or product. New business and renewals genuinely differ (renewals start at a known value with a fixed date); enterprise and SMB usually do not, and splitting them halves your sample for every conversion rate.

Each pipeline gets its own `## <name>` heading in `deals.md` and its own conversion table. A deal never appears in two.

## Renewals And Expansion

- A renewal is a deal with a **known value, a fixed close date and an inverted default**: it closes unless something breaks it. Open it one full sales cycle before the contract end, not one month.
- The renewal risk signal is not sentiment, it is **usage plus contact recency**: an account with no interaction in a quarter is at risk regardless of how the last call felt.
- Expansion is a separate deal, never an edited renewal value — merging them makes it impossible to say whether the base is shrinking while add-ons grow.
- Renewal dates belong in `## Due` in `memory.md` the day the deal is won, with the open-a-renewal reminder set one cycle before. That is the single highest-value row that table will ever hold.
