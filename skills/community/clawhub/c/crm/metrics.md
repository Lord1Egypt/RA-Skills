# Metrics — The Six Numbers, and How to Not Fool Yourself

A CRM number is only worth producing if a decision changes when it moves. Everything else is a dashboard, which is a screen people stop opening in week three.

**Contents:** [The Six Numbers](#the-six-numbers) · [Cohorts, Not Snapshots](#cohorts-not-snapshots) · [Sample Size](#sample-size) · [Cycle Length](#cycle-length) · [Win Rate Has Three Definitions](#win-rate-has-three-definitions) · [Source Attribution](#source-attribution) · [Leading Indicators](#leading-indicators) · [The Activity Metrics Trap](#the-activity-metrics-trap) · [The Monthly Snapshot](#the-monthly-snapshot)

**Before producing any number**, read `closed-deals.md` (the only honest source of rates), `## Metrics` in `~/Clawic/data/crm/memory.md` for the prior months, and `## Pipeline` for what is open. A number without its previous twelve is a fact without a meaning.

## The Six Numbers

| Number | Formula | Decides |
|---|---|---|
| Open pipeline | Σ open deal value, by stage | Whether prospecting is needed this week (`pipeline.md`) |
| Coverage | open pipeline ÷ target | Same, with a threshold: required = 1 ÷ win rate |
| Win rate | won ÷ (won + lost), on closed deals only | Every forecast weight, and the coverage you need |
| Median cycle length | days from creation to close, median | When today's pipeline turns into money |
| Conversion by stage | of deals that ever reached stage N, fraction that reached N+1 | Which stage to fix; the biggest drop is the only place effort pays |
| Revenue by source | won value grouped by source | Where the next hour of effort goes |

Six is the ceiling for a small operation. A seventh gets looked at once.

## Cohorts, Not Snapshots

The most common measurement error: computing conversion from deals **currently** in a stage.

- **Snapshot conversion** ("40% of my deals are in Proposal") describes today's inventory and moves every time a deal is created. It is not a rate.
- **Cohort conversion** takes deals *created* in a period — say Q1 — and asks how many ever reached each stage. It is a rate, it is comparable across quarters, and it needs the stage-entry history to compute (`schema.md`).
- The cohort has to be **old enough to have resolved**: a cohort younger than one median cycle length looks catastrophic because half of it is still open. Measure Q1's conversion in Q3.
- Same rule for win rate: deals *closed* in a period, never deals open in it.

## Sample Size

Small pipelines produce confident nonsense. Rules worth stating out loud when reporting a number:

- **Under ~20 closed deals**: give counts, not rates. "3 of 7 won" is honest; "43% win rate" is not.
- **Under ~10 deals in a stage**: no conversion rate for that stage. Merge stages for the purpose of the calculation rather than publishing noise.
- One large deal can move a value-based win rate by tens of points. Give count-based and value-based side by side, or say which one you used — mixing them across months is how a flat quarter looks like growth.
- When the sample is too small for rates, the useful output is the **list**: every closed deal with its reason. Seven rows read aloud beats a percentage computed from seven rows.

## Cycle Length

- **Median, never mean.** The distribution has a long right tail — one deal that took 14 months drags the average past anything useful.
- Measure from **deal creation** to close, and be consistent. Measuring from first contact is also valid and gives a very different number; whichever you pick goes into `## System`, once.
- Separate won and lost cycle lengths. Losses that take longer than wins mean qualification is happening too late, which is a `pipeline.md` fix, not a measurement one.
- **Time in each stage** is where the actionable version lives: the stage with the longest median dwell is the one to redesign, and it is usually the one before your own biggest effort.

## Win Rate Has Three Definitions

Pick one, write it in `## System`, never mix them in one sentence.

| Definition | Formula | Use |
|---|---|---|
| Deal count | won ÷ (won + lost) | Default; the one that feeds coverage |
| Value | won value ÷ (won + lost) value | When deal sizes vary by more than ~3× |
| Including no-decision | won ÷ all closed, with no-decision counted as lost | The honest one — and the one that reveals a qualification problem |

No-decision deals are the ones people quietly exclude, which is exactly why the win rate looks fine while revenue does not.

## Source Attribution

- **One source per deal, set at creation, never edited.** Multi-touch attribution is unaffordable and unresolvable below enterprise scale; a single first-touch field answers the only question a small business acts on.
- Group by source over closed deals: **count, win rate, median value, median cycle**. A source with a high count and a low win rate is a time sink that looks like success — the most common misallocation this calculation catches.
- **Referral is nearly always the best row** on win rate and cycle, and nearly always the least resourced. That gap is the usual payoff (`followup.md`).
- Track the *referrer* too (`referred_by`, `schema.md`): grouping over that field names the five relationships worth protecting.

## Leading Indicators

Lagging numbers (revenue, win rate) describe a quarter you can no longer change. Leading ones are the only kind worth a weekly review.

| Leading indicator | Predicts | Healthy shape |
|---|---|---|
| New qualified deals per week | Revenue one cycle out | Stable, not spiky — spikes mean prospecting only happens when panic does |
| Deals with a future dated next step ÷ open deals | How much of the pipeline is real | Near 1.0; anything below ~0.8 means the review is not being run |
| Interactions per open deal per week | Whether live deals are being worked | Falling counts precede a stall by weeks (`pipeline.md`) |
| Qualified-stage entries per week | The top of the funnel, without lead-count vanity | Compare to the cycle-adjusted target |
| Contacts past `stale_days` | Relationship debt | Flat or falling; growing means the follow-up loop is broken |

## The Activity Metrics Trap

Counting calls and emails is measurable, easy, and corrupting: what gets counted gets gamed, and the cheapest way to raise an activity count is to lower the quality of each activity. Rules that keep activity data useful:

- Use activity counts **diagnostically** — "this deal has had no contact in three weeks" — never as a target.
- Never compare activity counts across people with different territories or deal sizes.
- If an activity target is unavoidable, target the **buyer-side event** (meetings booked, replies received), which cannot be manufactured unilaterally.
- A CRM whose primary output is an activity leaderboard will have accurate activity data and no other accurate data (`adoption.md`).

## The Monthly Snapshot

Ten minutes, once a month, right after the hygiene sweep:

1. Close out the month's row in `## Metrics`: open pipeline, won, lost, win rate, median cycle, `As of` = last day of the month.
2. Recompute conversion by stage from the resolved cohorts, and update the weights used by the forecast (`pipeline.md`).
3. Compare against the previous three months, not against the previous one — a single month is noise.
4. Name one thing the numbers change. If nothing changes, the exercise is a ritual and one of the six numbers should be dropped.

**Write in the same turn**: the month row into `## Metrics` in `~/Clawic/data/crm/memory.md` with its `As of` date — overwriting the current month's row rather than adding a second — and, once `## Metrics` passes ~15 rows, split it to `metrics-log.md` with the same headings plus `## Conversion By Stage` and `## By Source`, adding its `## Boxes` line in the same turn (`memory-template.md`).
