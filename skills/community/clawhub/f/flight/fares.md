# Fares, Fare Families, and Fare Rules

Scope: what you are actually buying. The price is the smallest part of a fare; the rules decide what happens on every day that is not the day you fly.

**Contents:** [Fare Families](#fare-families) · [Booking Class Is Not Cabin](#booking-class-is-not-cabin) · [The Rules That Matter](#the-rules-that-matter) · [Basic Economy](#basic-economy) · [Refundable Versus Flexible](#refundable-versus-flexible) · [Taxes, Fees and Surcharges](#taxes-fees-and-surcharges) · [Why Prices Move](#why-prices-move) · [Mistake Fares](#mistake-fares) · [Tactics That Void The Ticket](#tactics-that-void-the-ticket) · [Legal Ways To Get The Same Saving](#legal-ways-to-get-the-same-saving)

## Fare Families

Airlines sell the same seat as three or four products. The branded names differ by carrier; the ladder does not.

| Rung | Typically includes | Typically excludes | Buy it when |
|---|---|---|---|
| Basic / Light | The seat, a personal item | Cabin bag on some carriers, checked bag, seat choice, changes, refunds, sometimes points | Non-stop, short, certain, carry-on only, and the gap to the next rung is real money |
| Standard / Classic | Cabin bag, seat choice at some point, a checked bag on long-haul, changes for a fee | Refunds | The default for almost everything |
| Flex | Free or cheap changes, refundable in part, priority, full points earning | — | Dates genuinely uncertain, or the trip has a fixed commitment at the far end |
| Premium cabins | Everything above plus the cabin | — | Priced against the cash gap, or via points where the ratio is best (`points.md`) |

The bundle is regularly cheaper than the base fare plus the same items bought as extras. Price both before recommending Basic.

## Booking Class Is Not Cabin

The single-letter code on the ticket (the fare basis / booking class) is what the airline's systems actually read. Two passengers in adjacent economy seats can be in classes that earn 25% and 100% of distance flown, one upgradeable and one not, one changeable and one not.

- Earning rate, upgrade eligibility, partner crediting and change rules all key off this letter, not the word "economy" (`points.md`).
- Deep-discount classes are excluded from upgrades and often from partner earning entirely. If the plan involves upgrading later, the class must be checked before purchase, not after.
- Record the fare class in `flown/<year>.md` after the flight — it is unrecoverable once the boarding pass is gone, and it is what any earning dispute turns on.

## The Rules That Matter

Read these five before recommending any fare, and state them in the shortlist:

1. **Change**: allowed at all? Fee, fare difference, or both? Many carriers dropped change fees on higher rungs but still charge the fare difference, which is usually the bigger number.
2. **Cancel**: refund to card, credit voucher, or nothing? A credit is worth less than cash by the odds of using it before expiry.
3. **No-show**: on many international fares, missing a flight without cancelling first cancels the entire remaining itinerary. Cancelling before departure preserves whatever residual value exists; not turning up destroys it.
4. **Name change**: usually impossible on airline tickets, sometimes possible for a fee on low-cost carriers. Spelling corrections are a different, easier process — do them early (`booking.md`).
5. **Validity and routing**: how long the ticket is valid for reissue, and whether the reissue must be on the same routing.

Screenshot the fare-rule page at purchase — it wins arguments that emails do not — and put the change and cancel terms in the `Changeable until` field of the booking's row in `~/Clawic/data/bookings/<year>.md`.

## Basic Economy

Not one product — it is whatever each carrier decided to strip. The recurring pattern: no seat selection, last boarding group, no changes, sometimes no cabin bag, reduced or zero points, and no standby. On some carriers it is now also excluded from same-day disruption rebooking flexibility.

Buy it when the trip is short, non-stop, certain, and carry-on only. Avoid it whenever there is a connection: the fare that cannot be changed is the fare you are holding when the connection breaks. Users who ask for "the cheapest" mean the cheapest workable, not the cheapest row.

## Refundable Versus Flexible

- **Flexible** = change without a fee, still pay any fare difference, usually no cash back.
- **Refundable** = money returns to the card, often minus an administration amount, and the fare is typically 2-4× the restricted one.
- The maths: buy refundable when `probability of cancelling × (fare + non-recoverable extras) > refundable premium`. At a 20% chance of cancelling, a premium above 20% of the fare loses on average. Travel insurance covers the same risk more cheaply for named causes only (`refunds.md`).
- A statutory 24-hour cancellation window (US-anchored tickets bought at least 7 days out) makes every fare briefly refundable. It is the cheapest hedge in the domain: hold the fare, verify documents and connections, cancel free inside the window if something is wrong.

## Taxes, Fees and Surcharges

- The displayed total is fare + government taxes + airport charges + carrier-imposed surcharges. Only the last is the airline's choice, and it is the one that reappears on award tickets.
- Departure taxes are refundable when a ticket goes unused, even on non-refundable fares, because they were never earned. Claiming them takes a request; nobody refunds them automatically (`refunds.md`).
- Fuel or carrier surcharges on award tickets can exceed the cash value of the points spent. Always compute cpp with the surcharge subtracted (`points.md` Rule 7 formula).
- Currency: buy in the fare's own currency and let the card convert. Airline-side conversion and dynamic currency conversion at payment both cost more than a card's foreign-transaction fee.

## Why Prices Move

Fares are inventory buckets, not a curve. Each bucket has a fixed number of seats at a fixed price; the price "rises" because a bucket emptied.

- Consequences: the same flight can be cheaper tomorrow if a bucket reopens from cancellations, and party size matters — four seats must all come from one bucket, so a family search often shows the price a solo search does not.
- Booking passengers separately can therefore be cheaper, at the cost of splitting the reservation (`passengers.md` — do not do it for anyone travelling with a child).
- Schedule loads open roughly 330-360 days ahead, and the cheapest buckets are commonly available at load and again after the airline's own release cycles.

## Mistake Fares

Real, rare, and usually killed within hours. If one appears:

- Book directly with the airline, pay immediately, and do not call to ask about it.
- Buy nothing non-refundable around it — no hotels, no connecting tickets — until the ticket number is issued and has survived several days.
- Do not add extras or request changes; any touch of the record invites a review.
- Expect it may be cancelled. Where a regulator requires the carrier to refund rather than honour, that is the realistic outcome, and consequential losses are on you.

## Tactics That Void The Ticket

State the mechanism, then refuse to build on them:

| Tactic | What it is | What actually happens |
|---|---|---|
| Hidden city / skiplagging | Book A-B-C, get off at B | Every later segment on the ticket cancels, including the return; a checked bag flies to C; carriers pursue points clawback and account closure |
| Throwaway ticketing | Buy a return, fly one way | Same cancellation mechanic, plus repeat use is traceable to the frequent-flyer account |
| Back-to-back ticketing | Overlapping returns to defeat a stay requirement | Prohibited by most conditions of carriage; detected on the same passenger record |
| Fake onward ticket | A cancelled or forged reservation shown at check-in | A cancelled booking fails a live check; a forged one is a documents offence |

## Legal Ways To Get The Same Saving

- **One-ways instead of a return** — no stay requirement to defeat, each leg priced and changed on its own.
- **Open jaw** — fly into one city, out of another, and cover the gap overland. Prices at or below a return on most transatlantic and intra-Europe itineraries.
- **Positioning flight on a separate ticket** — a cheap hop to the city where the long-haul is cheap, with an overnight buffer and the 3-hour rule applied (`connections.md`).
- **Legitimate onward ticket** — a genuine refundable ticket bought and cancelled after entry, or a cheap real bus or train reservation, both of which survive a live check.
- **Stopover programmes** — a free second destination inside a single fare (`search.md`).

**When a fare rule turns out to be decisive** — a change fee that will apply, a credit with an expiry, a no-show clause on a multi-leg trip — write it into the booking's row in `~/Clawic/data/bookings/<year>.md` under `Changeable until`, and put any date it creates in `## Due`. The rule that is not written down is the rule nobody reads before rebooking.
