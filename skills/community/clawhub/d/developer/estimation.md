# Estimating, Scoping, and Saying What Will Not Fit

An estimate is a forecast under uncertainty, not a commitment. Its quality is measurable: compare what you said to what happened, and the next one gets better. Without that log, ten years of experience is one year repeated ten times.

**Before giving any estimate**, read `## Estimates` in `~/Clawic/data/developer/memory.md` (or `estimates.md` if `## Boxes` points there) and the `## Gotchas` of the repo profile. Your own past ratio is the single best input you have; the second best is knowing this repo's build takes 20 minutes.

## The Method

1. **Decompose until each piece is something you have done before.** Anything you cannot decompose is not an estimate, it is a research task — see Spikes.
2. **Estimate each piece optimistically** (the "if nothing surprises me" number). Humans are good at this part and bad at the rest.
3. **Apply your factor.** `S` = the optimistic sum from step 2; `f` = the median `actual ÷ S` of the closed rows in your calibration log. Until the log has ~10 closed rows, use **`f = 2.0`** and say it is uncalibrated. `f` is always measured against `S`, never against the range you quoted — the quoted range already contains `f`, so a ratio taken from it converges to 1.0 exactly as your calibration starts working, and the factor silently dies.
4. **Quote a range**, in `estimate_units`: `low = S × f`, `high = S × f × 1.5`, rounded outward to whole units. `S` = 3 days with `f` = 1.8 gives 5.4 and 8.1 → **"5-9 days"**. The low end is your calibrated median — half your work lands under it — and the high end covers the tail; "3 days" hides both and gets remembered as a promise.
5. **State the assumptions the range depends on** — three at most, the ones that would blow it: the API exists and works, review turnaround is a day, the staging data is representative. An estimate without assumptions cannot be renegotiated when one breaks.

## The Costs Nobody Estimates

Add these explicitly; they are why the optimistic number is optimistic.

| Cost | Typical weight |
|---|---|
| Understanding the existing code | 20-30% of a first change in an unfamiliar repo (SKILL.md Rule 3) |
| Tests worth keeping | 30-50% on top of implementation for a change with real branches |
| Code review round trips | Wall-clock days, not work hours — bounded by the team's review latency, which is in the repo profile |
| CI, flaky retries, environment repair | Whatever the suite time is, times the number of pushes |
| Migration, backfill, and its contract step | Often larger than the feature (`migrations.md`) |
| Rollout, flag, monitoring, and the cleanup | A day for anything user-visible (`shipping.md`) |
| The interruption tax | On-call weeks, meeting-heavy weeks: real capacity is 50-60% of nominal |
| The unknown-unknowns of integration | Everything you have not run against the real thing yet |

The last row is why systems that must talk to something you do not control are the highest-variance estimates you will give. Verify the integration first, on day one, with the smallest possible call.

## Spikes

When you cannot decompose it, the honest answer is "I don't know yet, and here is what it costs to find out": a **timeboxed spike** — fixed duration (a day, two days), a written question to answer, and a throwaway output. What comes back is an estimate, not a feature.

- The spike's deliverable is the answer plus the estimate, not the code. Say up front that the code is disposable, or it ships.
- If the spike overruns its box, that is the finding: the thing is bigger than the sponsor thinks.
- Put the answer in `artifacts/spike-<question>.md` when it will outlive the ticket — "we cannot use their bulk endpoint, it caps at 100 and rate-limits at 5/s" is exactly the fact that gets rediscovered next quarter.

## Reference Class Beats Introspection

Kahneman and Tversky's planning fallacy: people estimate the specific case by imagining how it will go, and the imagining leaves out interruptions, mistakes, and everything unplanned. The correction is to ignore the story and ask "how long did the last three things like this take?" — that is what the calibration log is for. When your inside view and your log disagree, the log is right, and it is right by a factor, not by a bit.

## Communicating an Estimate

- **Range plus assumptions**, always. "5-9 days, assuming the payments sandbox works and review lands same-day."
- **Give a date only when you also give the range** behind it, and only counting working days at real capacity.
- **Re-forecast when an assumption breaks**, the day it breaks. A silent overrun is a trust problem; a same-day "the sandbox is down, this moves to 8-12" is a status update.
- **The 90% syndrome**: work reported as 90% done stays there. Report by *what is verifiably complete* — merged, tested, deployed — not by felt progress.
- **When pressed for a smaller number**, do not shrink the estimate; change the scope and say which part is dropped. The estimate is a measurement, not a negotiating position.

## Scope Negotiation

| Ask | Response |
|---|---|
| "Can it be done by Friday?" | "Yes, if we drop X and Y" or "no, here is what fits by Friday" — never a bare yes |
| "Just make it quick and dirty" | Name the debt and where it will surface, and get the payoff on the board (`tech-debt`) |
| Scope grows mid-work | Re-estimate the delta out loud, then let the sponsor choose what moves |
| Two urgent things | Ask which one ships if only one can; ambiguity here always resolves against you |
| Deadline is fixed and external | Fix the date, flex the scope, cut in slices that each ship value (`shipping.md`) |

## Traps

| Trap | Why it fails | Do instead |
|------|-------------|------------|
| Estimating the code and nothing else | Coding is often under half the elapsed time | Add the cost table above, item by item |
| A single number | It gets recorded as a commitment and remembered as a miss | Range in `estimate_units`, with assumptions |
| Padding silently | The padding gets consumed by Parkinson's law and your credibility takes the miss anyway | Explicit factor from the log, stated openly |
| Estimating for someone else's speed | Their factor is not yours; unfamiliarity dominates | Estimate for who will actually do it |
| Never closing the loop | The factor stays a guess forever | Close every row with the actual (`## Estimates`) |
| Committing before understanding | The number is anchored before the first surprise | Spike, then estimate |
| Treating a range as a bet on the low end | The low end is the median: half the time you are past it before anything goes wrong | Plan against the high end, communicate the range |

## Write Down Both Ends

- **When the estimate is given**: a row in `## Estimates` of `~/Clawic/data/developer/memory.md` — date, what, the optimistic sum `S`, the quoted range, the assumptions (`memory-template.md`). Without `S` the row cannot be closed: it is the denominator of the ratio.
- **When the work lands**: the same row's `Actual` and `Ratio = actual ÷ S`, then recompute the factor line as the median of the closed ratios. This is the only input to Rule 5 that improves with time.
- **A spike's answer** that will outlive the ticket → `artifacts/spike-<question>.md` with its `## Boxes` line.
- **A scope decision the sponsor made** → the project file at `~/Clawic/data/projects/<project>.md`, one line under `## Decisions`.
