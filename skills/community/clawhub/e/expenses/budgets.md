# Budgets — Bounded Envelopes That Do Not Quietly Overrun

An envelope is one file: `~/Clawic/data/expenses/budgets/<kebab-name>.md`. **Read the envelope file before any spend that plausibly belongs to it, and before answering any "how much is left" question** — the remaining number is in the file, and recomputing it from the ledger misses everything committed but unpaid.

This covers renovations, weddings and events, launches and campaigns, moves, and any other bounded pot. Trip envelopes use the same shape with the trip specifics in `travel.md`. Ongoing monthly category targets are a different thing and live in the shared `~/Clawic/data/finances/budget.md`.

**Contents:** [Anatomy](#anatomy) · [Contingency](#contingency) · [Committed Beats Paid](#committed-beats-paid) · [Are We Over?](#are-we-over) · [Overrun Protocol](#overrun-protocol) · [Quotes, Change Orders and Retainage](#quotes-change-orders-and-retainage) · [Events and Guest-Count Scaling](#events-and-guest-count-scaling) · [Closing an Envelope](#closing-an-envelope)

## Anatomy

Envelope total · contingency (separate, named, not distributed into the lines) · one row per line item with **Budgeted / Committed / Paid / Remaining** · a status line with a date.

The envelope is created **when the number is agreed**, not when the first money moves. An envelope that appears after three payments has already lost the only thing it was for: the comparison against the original intention.

Every paid line still gets its ordinary ledger row, tagged with the envelope. The envelope file is the view; the ledger is the record. Two records of the same payment with no shared tag is how the two disagree by 400 units and nobody can say which is right.

Cross-references, name only, never duplicated: the project plan lives in `~/Clawic/data/projects/<project>.md`, the people in `~/Clawic/data/contacts/contacts.md`, the bookings in `~/Clawic/data/bookings/<year>.md`.

## Contingency

A renovation budget with no contingency is a renovation budget that will be broken, and the breaking will be attributed to bad luck rather than to arithmetic.

| Envelope | Common contingency | Why |
|---|---|---|
| Renovation, known building, cosmetic work | 10-15% | Surprises are finish-level |
| Renovation touching structure, plumbing, wiring, or an older building | 15-20%+ | The cost driver is behind a wall and nobody has seen it |
| Wedding or event | 5-10% | Prices are quoted; the variance is scope, not discovery |
| Software or campaign | 10-20% | Scope discovery, same mechanism as a wall |

Keep contingency as its **own line, never distributed** into the item budgets. Distributed contingency is spent invisibly and the envelope reports healthy right up to the moment the last item has no money. Every draw against contingency is a dated line saying what it covered — that record is what makes the next envelope's contingency an estimate instead of a guess.

## Committed Beats Paid

**The envelope is consumed on the day a quote is signed or an order is placed, not on the day the money leaves.**

This is the single rule that separates envelopes that work from envelopes that surprise people. A kitchen with three signed quotes and one deposit paid looks 20% spent by cash and is 60% committed. The 60% is the true number, and it is the one `budget_alert_pct` is measured against.

| State | Meaning | Counts against the envelope |
|---|---|---|
| Budgeted | The plan | No |
| Quoted | A price exists, nothing signed | No — but flag it when quoted exceeds budgeted |
| Committed | Signed, ordered, or a deposit paid | **Yes, in full** |
| Paid | Money gone | Yes (already counted at commitment) |

Remaining = `envelope − Σ committed`. A second number, `envelope − Σ paid`, is cash timing and is only interesting to someone managing cashflow.

## Are We Over?

Depends on what bounds the envelope, and using the wrong one produces confident nonsense.

- **Time-boxed** (trip, campaign, monthly pot): expected = `envelope × elapsed ÷ total`. A 2,000 envelope on day 9 of 30 should be around 600 committed; 1,100 is not "a bit high", it is a projected 3,667.
- **Scope-boxed** (renovation, wedding): elapsed time means nothing — work is lumpy and the expensive phase is rarely in the middle. Compare **committed against the budget of the lines that are complete or ordered**. If the four finished lines came in 12% over, the unfinished ones will too, and the projection is `envelope × 1.12`, not `envelope`.
- Flag unprompted at `budget_alert_pct` of committed, and again on any single line exceeding its own budget by more than roughly 10% — a line overrun is early information, an envelope overrun is late information.

## Overrun Protocol

There are exactly three levers, and the value of naming which one is being pulled is higher than the value of pulling any of them:

1. **Cut scope.** The only lever that does not cost money. Which line, decided explicitly.
2. **Draw contingency.** Legitimate, dated, and recorded as a draw against the contingency line so the remaining contingency is visible.
3. **Raise the envelope.** A decision, with a new total and a date, not an adjustment.

Silently eating contingency is the failure mode: the envelope keeps reporting healthy, contingency reaches zero unnoticed, and the last line item — always the one nobody was excited about, usually the one that makes the rest usable — has no money.

State the lever in one line when it is used. Write it in the envelope's status line.

## Quotes, Change Orders and Retainage

- **Estimate vs quote vs fixed price** commit different amounts of nothing: an estimate is a guess with no obligation, a quote is a stated price usually with conditions attached, a fixed price is a contract. Record which one a number is, because the difference is the whole variance.
- **Every change is a dated line.** Renovation overruns are almost never one big surprise; they are eleven small changes nobody wrote down. A change order with no line means the final variance has no explanation.
- **Deposits** paid against an envelope are `Paid` and were already `Committed`; they are not `#deposit` receivables (`capture.md`) unless they are genuinely refundable.
- **Retainage / final payment held** back until completion is committed money that has not moved. Keep it in Committed or the last week of the project appears free.
- A quote that expires is not a commitment. Move it back to Quoted and note the date.

## Events and Guest-Count Scaling

For weddings and events, mark every line **fixed** or **per-head**, because cutting the guest list only moves the per-head lines and everyone assumes it moves all of them.

- Per-head: catering, drinks, place settings, favours, some staffing.
- Fixed: venue, photography, music, flowers, stationery design, transport.

`per-head total = guests × per-head sum`. Cutting 20 guests from 120 at a per-head sum of 95 saves 1,900 — and moves the fixed 14,000 not at all. Say both numbers when a guest cut is proposed, or the cut gets made expecting a different result.

Vendor deposits at booking are commitments across the whole envelope, so an event budget is typically 60-80% committed months before anything is paid. That is normal; it is only alarming if the envelope was being read by cash.

## Closing an Envelope

1. Final variance per line and in total, with the date.
2. **The per-unit numbers**, which are the only part worth keeping: cost per m², per guest, per campaign week, per room. That is what makes the next envelope's estimate real rather than optimistic.
3. What the contingency was actually spent on, and whether the percentage was right.
4. Move the envelope's `## Boxes` condition to "read for reference when planning a similar one" and leave the file. A closed envelope with real numbers is one of the most valuable artifacts this skill produces.
5. If the envelope corresponds to something the user tracks as a project, the project entry is referenced by name only; the final number, the variance and every per-unit figure stay in this envelope file. Nothing is written into `~/Clawic/data/projects/` — a number that lives in two boxes is a number two skills will disagree about.

**Write on the way out.** Creating an envelope writes `budgets/<name>.md` and its `## Boxes` line in the same turn; every commitment, payment, change order and contingency draw updates the line and the dated status line; crossing `budget_alert_pct` writes the flag and the date it was raised; a review cadence goes to `## Due`; closing writes the final variance and the per-unit numbers, and the closing summary goes to `artifacts/` if the user will reuse it. Formats in `memory-template.md`.
