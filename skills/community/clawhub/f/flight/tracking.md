# Prices Over Time, And Flights In The Air

Scope: two kinds of watching. Before the ticket, watching a price until it hits a target. After the ticket, watching the operation until the aircraft is on the ground.

**Before setting any alert or answering "is this a good price"**, read `## Routes` in `~/Clawic/data/flight/memory.md` — or `routes.md` if the `## Boxes` index points there. The stored range is what makes the answer a fact rather than an opinion.

**Contents:** [What Prediction Can And Cannot Do](#what-prediction-can-and-cannot-do) · [Building The Reference Range](#building-the-reference-range) · [Setting Alerts That Work](#setting-alerts-that-work) · [Buying Decision](#buying-decision) · [Price Drops After Purchase](#price-drops-after-purchase) · [Watching The Operation](#watching-the-operation) · [The Day Of Travel](#the-day-of-travel) · [What To Record](#what-to-record)

## What Prediction Can And Cannot Do

Say this plainly whenever a user asks whether prices will go up:

- **No public service predicts a specific route's future price.** Consumer prediction features are directional summaries of history, and their accuracy is not published in a form anyone can check.
- Historical patterns are real and usable: seasonality, day-of-week of departure, and the shape of the last three weeks before departure.
- What is *not* usable: any claim about the best day of the week to buy, any single "book N days ahead" number applied across routes, and any percentage saving quoted without the route it came from.
- The reliable edge is not prediction. It is knowing **this route's own price distribution** and having a target set before emotion arrives.

## Building The Reference Range

A range is worth more than a prediction, and it takes four observations to have one.

- Record the price in `## Routes` each time the route is searched: the price with its currency, the date seen, the dates searched, and the cabin. Four to six observations across a couple of months bound the route.
- The comparison must be like for like: same cabin, same bag inclusion, same number of stops. A cheaper number that is Basic economy with no bag is not a lower price.
- Note the **shape**, not just the low: a route that sits at 430-700 with occasional 380s behaves differently from one that never moves off 500.
- Peak dates have their own range. Christmas on the same route is a different distribution, and mixing them makes both useless.
- One row per route in `## Routes`, overwritten on each check — never a second row for the same route.

## Setting Alerts That Work

- **Set the alert on the range, not on hope.** A target 10-20% below the route's typical price fires occasionally; a target at the historical minimum never fires and the trip gets booked in a panic.
- Alert on **flexible dates** (±3 days) as well as the exact dates: the flexible alert is what finds the outlier.
- Two alerts on the same route with different targets is a reasonable setup: one at "good", one at "book immediately".
- Alert fatigue is real. Any alert that fires weekly is set wrong and will be ignored when it matters.
- Record where each alert lives in the `Alert` column of `## Routes` — an alert nobody can find later is an alert nobody can cancel.
- Cadence for manual checks: weekly is enough outside the last three weeks, and daily checking is a cost, not a strategy (`SKILL.md`, Booking Windows).

## Buying Decision

Book when any of these is true, and say which one:

- The price is at or below the target derived from the stored range.
- The trip is inside the last three weeks, where the distribution shifts upward and waiting has negative expected value.
- The itinerary is scarce: thin route, few frequencies, peak date, or a party of three or more needing seats from one bucket (`fares.md`).
- The fare includes a free-cancellation window that makes the decision reversible (`refunds.md`).

Do not book because a site says "only 2 seats left at this price" — that is a bucket count, and it is displayed to create urgency as much as to inform.

## Price Drops After Purchase

- A few carriers and some jurisdictions allow rebooking at the lower price, usually as a credit rather than cash, and typically only within a defined window.
- The statutory 24-hour cancellation window on US-anchored tickets makes an immediate rebook free (`fares.md`).
- Card price-protection benefits have largely disappeared for travel; check the current benefits guide rather than the folklore.
- Otherwise the correct answer is: the price paid was a decision made with the information available, and re-checking after purchase only buys regret. Say it once and stop watching the route — and delete its `## Routes` row.

## Watching The Operation

From about T-24h, and earlier for a trip with no slack:

- **The inbound aircraft is the best available predictor.** Find the aircraft's previous flight; if it is two hours late arriving, your departure is two hours late, whatever the departure board says.
- Airline apps notify earlier than departure boards and usually earlier than email.
- Independent tracking services show the aircraft's position, its actual airborne time and its historical on-time record for that flight number — the last of these is worth checking *before* booking a tight connection.
- Weather at the destination and at the hub matters more than at the origin, and air-traffic control programmes are published in some markets hours before airlines announce anything.
- Gate changes are common and are announced late. Terminal changes are rarer and more expensive to miss.
- A cancellation is often visible as an aircraft that has not moved when it should have. Acting on that ten minutes before everyone else is the entire advantage (`disruptions.md`).

## The Day Of Travel

- Check in at the opening of the window when seats are assigned then, or when the carrier charges for airport check-in.
- Re-verify the terminal for a codeshare — it belongs to the operating carrier, not the one on the ticket (`booking.md`).
- Arrive against the airport's own published security wait, not a habit. Some airports publish live queue times.
- Keep the boarding pass in the airline app and one offline copy; never store the barcode image in `~/Clawic/data/`.
- If a delay is building, start looking at alternatives before it is announced (`disruptions.md`).

## What To Record

**Every price seen for a route being watched goes into its `## Routes` row** — best seen with the date, and the range if it moved. **When an alert is set, record where.** **When the ticket is bought, the row's job is done**: delete it and let `~/Clawic/data/bookings/<year>.md` carry the trip. **After the flight is flown**, add the line to `flown/<year>.md` with its fare class, and if it was delayed enough to matter, open the `## Claims` row the same day (`disruptions.md`).
