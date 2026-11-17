# Travel — What a Trip Actually Costs

A trip is an envelope: `~/Clawic/data/expenses/budgets/<trip>.md`, same shape as `budgets.md`. **Before the first trip entry**, read that file and `~/Clawic/data/bookings/<year>.md` — flights and hotels already recorded there are not re-entered as bookings; only their money comes here.

**Contents:** [Prepaid Is Most of It](#prepaid-is-most-of-it) · [Daily Burn](#daily-burn) · [Money on the Ground](#money-on-the-ground) · [Group Trips](#group-trips) · [Business Travel](#business-travel) · [The Trip Does Not End When You Land](#the-trip-does-not-end-when-you-land) · [The Post-Trip Summary](#the-post-trip-summary)

## Prepaid Is Most of It

Flights, accommodation and the big pre-booked items are commonly 50-70% of a leisure trip and are spent weeks before departure. Any "daily budget" that ignores them describes the small half of the trip.

Split the envelope in two from the start:

```
trip envelope = prepaid (booked before departure) + on-the-ground (everything after)
```

Both halves get lines. The prepaid half is usually near-fully committed before day one, which is correct and not an alarm (`budgets.md`, Committed Beats Paid).

Bookings already in the shared `~/Clawic/data/bookings/` box keep their locator, dates and provider there. Here they get a ledger row for the money and a line in the envelope. Duplicating a booking into the expenses box is how a cancellation gets recorded in one place and not the other.

## Daily Burn

The useful number is not a fixed per-day allowance, it is the recomputed one:

```
today's burn allowance = (on-the-ground envelope − on-the-ground spent) ÷ days remaining
```

Recompute every day. A fixed allowance that was blown on day two produces a week of guilt and no adjustment; a recomputed allowance turns an overspend into a smaller number tomorrow, which is a decision the traveller can actually make.

State it as a number, once, and only when asked or when the day's spend crossed it materially. Nobody wants a budget notification on a holiday.

Weight the days when the itinerary is uneven: three cities with different price levels are three sub-lines, not one average. A single average across Tokyo and a rural onsen is wrong in both directions on every day of the trip.

## Money on the Ground

- **Always pay in the local currency.** Terminals and ATMs offering to charge in your home currency are dynamic currency conversion, commonly 3-7% worse than letting the card network convert (`currency.md`).
- **Withdraw larger amounts less often.** ATM fees are largely fixed per withdrawal, so four small withdrawals cost several times what one does. The counterweight is carrying cash safely — that is the real trade, not the exchange rate.
- **Airport exchange counters** price their convenience into the spread. The rate on the board is not the cost; the gap between buy and sell is.
- **Cash abroad ends the trip as a stranded balance.** Count what is left at the end and either book it as `cash-unlogged` for the trip or carry it forward as an asset for the next trip to that currency — pick one and say which, because an unrecorded 8,000 JPY in a drawer reappears as a phantom saving next year.
- Tips and local service conventions vary enough to be a real line; where tipping is expected at 10-20%, the eating-out line is understated by the same amount if tips are logged separately from the meals.
- Deposits on rentals — cars, apartments, equipment — are `#deposit` receivables with a `## Due` line for the return date, not trip spending (`capture.md`).

## Group Trips

The full mechanics are in `sharing.md`; the trip-specific parts:

- **One payer per category** — one books accommodation, one handles transport, one covers group meals. Fewer entries, smaller settlement, and the fronting is distributed instead of landing on whoever is most organized.
- **Settle once at the end**, not nightly.
- **Convert each entry at its own rate date.** A single trip-average rate quietly moves money between whoever paid on a strong day and whoever paid on a weak one.
- **Beneficiaries are who was actually there.** The three who skipped the boat trip are not beneficiaries of it.
- Someone joining for part of the trip: their beneficiary set is their days only, and the group block gets their join and leave dates.
- Produce the settlement statement in `artifacts/` — a group trip is the case where a written statement most reliably prevents a slow-burning argument.

## Business Travel

- **Primary-purpose test** decides the travel itself; **business days ÷ total days** apportions everything running across the trip (`reimbursement.md`).
- A **per diem** replaces receipts for the items it covers and gets logged as one entry per day at the per-diem amount. Travel days are commonly paid at a reduced rate; confirm the employer's schedule.
- Keep business and personal legs as separate tags inside the same trip envelope, so the envelope answers "what did the trip cost" and the claim answers "what is recoverable". Two envelopes for one trip means neither has the whole picture.
- Companion costs are personal, always, and come out before any apportionment.
- Claim in the currency paid and let the employer convert, unless their policy says otherwise.

## The Trip Does Not End When You Land

The envelope stays open until every one of these has resolved:

- **Card FX settles.** Foreign charges post at the network's rate days later; the estimated rates in the ledger get replaced with the actual ones at reconciliation (`reconciliation.md`).
- **Refunds and cancellations** — a cancelled leg, an unused reservation, a partial hotel refund. These land weeks later and each is a negative row against its original category (`capture.md`).
- **Deposits come back**, or do not.
- **Insurance or airline compensation claims** are receivables with their own `## Due` dates, not trip income. Delay compensation and lost-baggage claims routinely take months.
- **Shared balances settle.**

Set a `## Due` row for the trip's final close, roughly one full statement cycle after returning. Closing it on the flight home guarantees the summary is wrong.

## The Post-Trip Summary

The artifact worth keeping, because it is what makes the next trip's budget real:

- Total, in home currency **and** in the trip's main local currency — the local number is the one the traveller remembers and can sanity-check.
- Prepaid vs on-the-ground split, actual against envelope.
- **Cost per day and cost per person** — the two numbers that transfer to the next trip.
- Category breakdown: lodging, transport, food, activities, fees.
- Variance and its one-line cause.
- What was overpaid for and would be avoided next time — the concrete one, not a resolution.

Write it into the trip envelope file, and to `artifacts/` as its own file if the user is likely to plan against it. Either way it gets its `## Boxes` line with a read condition naming the next similar trip.

**Write on the way out.** Trip spend goes to the ledger with the trip tag and to the envelope's lines in the same turn; the recomputed burn goes in the envelope's status line, never invented fresh each time; a new participant gets their `contacts.md` row and their dates in the group block; deposits, refunds due, insurance claims and the final trip close each get a `## Due` row; the post-trip summary goes to the envelope file and to `artifacts/` with its `## Boxes` line. Formats in `memory-template.md`.
