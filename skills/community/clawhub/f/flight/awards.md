# Award Tickets — Finding And Booking Them

Scope: spending points on a specific flight. Whether to spend them at all, and how they were earned, is `points.md`.

**Before searching**, read `## Loyalty` in `~/Clawic/data/flight/memory.md` for which programmes and transferable balances actually exist, and `## Boxes` for any `artifacts/award-*.md` covering this route — a routing that worked once usually works again.

**Contents:** [The Order Of Operations](#the-order-of-operations) · [Award Chart Types](#award-chart-types) · [Where The Space Is](#where-the-space-is) · [Searching](#searching) · [Partner Rules That Break Searches](#partner-rules-that-break-searches) · [Surcharges](#surcharges) · [Transfers](#transfers) · [Booking And Holding](#booking-and-holding) · [Changing An Award](#changing-an-award) · [Upgrades With Points](#upgrades-with-points)

## The Order Of Operations

Doing these out of order is how points get stranded.

1. Establish the **cash price** of the ticket you would otherwise buy. Without it there is no cpp and no decision (`points.md`).
2. Find **confirmed award space** on a specific date and flight number.
3. Identify **every programme** that can book that space — usually the operating carrier's own, plus its alliance partners, plus non-alliance partners.
4. Compare the **points plus surcharges** across those programmes for the same seat. The spread between programmes booking identical metal is routinely a factor of two or more.
5. Only now, **transfer points** if needed, and only if the seat can be held or the transfer is instant.
6. Ticket, then verify the ticket number exists (`booking.md`).

## Award Chart Types

| Type | How pricing works | Consequence |
|---|---|---|
| Fixed region chart | Published bands by region and cabin | Sweet spots exist and are stable; the chart is the reason to hold that programme's points |
| Distance-based chart | Bands by great-circle distance of the whole itinerary | Long connections can cost the same as a short hop in the same band; routing rules decide the value |
| Dynamic | Points track the cash price | No sweet spots, no arbitrage, and cpp is capped around the programme's own sale rate |
| Hybrid | Own metal dynamic, partners on a chart | The partner chart is where the value is, and it is usually not searchable on the same website |

Programmes migrate from charts to dynamic pricing with little notice and never in the other direction. A chart-based sweet spot is worth using rather than saving.

## Where The Space Is

- **At schedule load**, roughly 330-360 days before departure, when the initial award inventory is released. The best long-haul premium space goes in the first hours.
- **Inside two weeks**, when airlines dump unsold premium seats into award inventory. The second-best window, and it suits flexible travellers.
- **After a schedule change** on the flight, when seats are re-inventoried.
- Space is per cabin, per fare bucket, and per partner: an airline commonly shows more award space to its own members than to partners.
- Two seats on the same flight is a materially harder ask than one; four is a different search entirely, and splitting across cabins or dates is often the only answer.

## Searching

- The operating carrier's own site is the ground truth for its own space. Alliance partners' sites are the ground truth for what partners can see, which is less.
- Several partner programmes cannot be searched online at all and must be booked by phone with the flight numbers you already found elsewhere. Finding the space on one website and booking it through another programme is normal practice, not a trick.
- Multi-partner award search tools save enormous time; they are also scraping-based, so treat their results as a lead to confirm, not as inventory.
- Search one segment at a time when a connecting search returns nothing — availability often exists on each leg separately, and a phone agent can piece it together.
- **Phantom space** — inventory shown that cannot be ticketed — is common with cached data and with married-segment logic. A seat is real when a ticket number exists.

## Partner Rules That Break Searches

- **Married segments**: airlines sell certain connections as a unit, so a segment bookable within a connection may be invisible on its own, and vice versa.
- **Routing rules**: distance-based and region charts have maximum permitted mileage, permitted transit points and limits on the number of stops. A routing the map allows may be refused by the fare engine.
- **Stopover allowances** on award tickets are one of the largest remaining sources of value: several programmes still permit a multi-day stopover on a one-way for no extra points.
- **Blackout and capacity control** on the airline's own programme frequently does not apply to partners booking the same seat.
- **One-way pricing at half a round trip** is the norm in most modern programmes, which makes mixing programmes for the outbound and return not just possible but usually optimal.

## Surcharges

Carrier-imposed surcharges on award tickets vary from nothing to a sum exceeding the cash value of the points. They depend on the **programme used to book**, not only on the airline flown — which is why the same seat costs wildly different totals through different programmes.

Always run the cpp formula with surcharges subtracted (`points.md`). An award with high surcharges and a low cash fare is a bad trade dressed as a free flight.

## Transfers

- Almost all bank-to-airline transfers are **one-way and irreversible**. There is no route back.
- Speed varies from instant to several days. A programme that takes days cannot be used for a seat that will not survive the wait — that is exactly the case for holding a seat first.
- Transfer bonuses improve the ratio; waiting for one is only rational when the seat will still be there, which for long-haul premium space it usually will not.
- Ratios are not always 1:1, and a poor ratio can make a "sweet spot" worse than a straight cash purchase.
- Never transfer to test whether a booking will work.

## Booking And Holding

- Where the programme allows a hold on award space, use it: it is the only safe sequencing for a slow transfer.
- Award ticket names must match documents exactly, and award tickets are usually not transferable to another person — some programmes allow booking for others from your account, some do not.
- Taxes and surcharges are paid with a card; use one with travel protection, since a card benefit generally applies to the paid portion (`refunds.md`).
- Confirm the ticket number. An award reservation without one is cancelled the same way a cash one is (`booking.md`).
- Record the booking in `~/Clawic/data/bookings/<year>.md` with both figures in the `Paid` column: `55,000 Avios + 180 EUR`.

## Changing An Award

- Award change and cancellation rules are frequently **more generous** than cash fares: several programmes now redeposit points for free or a small fee up to close to departure. This is a genuine, under-used advantage of booking with points on uncertain dates.
- On an involuntary change or cancellation, the passenger's statutory rights are identical to a cash ticket — compensation is not reduced because the fare was paid in points, though the refund is of points plus the cash portion (`disruptions.md`).
- Redeposit deadlines are hard. Put them in `## Due` at booking.

## Upgrades With Points

Almost always worse value than booking the premium cabin outright as an award, because upgrades require an eligible — usually expensive — cash fare underneath and separate upgrade inventory that rarely exists on the flights people want (`seats.md`). Run both numbers before recommending an upgrade: `cash fare + upgrade points` against `award in the premium cabin + its surcharges`.

**When a routing works — the programme, the partner metal, the points and cash paid, and where the space appeared** — write it to `~/Clawic/data/flight/artifacts/award-<route>.md` and add its `## Boxes` line in the same turn. Award routings are expensive to derive and identical the next year; this is the highest-value artifact this skill produces.
