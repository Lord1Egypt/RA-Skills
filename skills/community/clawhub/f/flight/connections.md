# Connections, Layovers, and Two-Ticket Itineraries

Scope: will this connection work, and what happens if it does not. The single question where a wrong answer strands someone.

**Contents:** [The Two Regimes](#the-two-regimes) · [Minimum Connection Time](#minimum-connection-time) · [The Buffer Formula](#the-buffer-formula) · [What Eats The Buffer](#what-eats-the-buffer) · [Two Tickets](#two-tickets) · [Virtual Interlining](#virtual-interlining) · [Immigration, Recheck and Preclearance](#immigration-recheck-and-preclearance) · [Long Layovers](#long-layovers) · [When It Is Already Going Wrong](#when-it-is-already-going-wrong)

## The Two Regimes

Everything about a connection follows from which of these applies. Establish it before any other analysis.

| | One ticket (single locator, or interlined) | Two tickets |
|---|---|---|
| If leg 1 is late | The carrier rebooks you, free, and owes duty of care | Leg 2 is a no-show you paid for |
| Bags | Checked through to the final destination | Collected and rechecked, unless the carriers interline and the agent agrees |
| Minimum time | Airline-published MCT, enforced by the booking engine | None — the platform will sell you 35 minutes |
| Compensation | The delay is measured to the final destination | Measured per ticket, so usually nothing |
| Cost | Sometimes higher | Often the reason the trip is affordable |

## Minimum Connection Time

Airlines publish an MCT per airport, per terminal pair, per domestic/international combination. Any itinerary a carrier or GDS sells on one ticket respects it — that is the guarantee, and it is a legal-ish minimum rather than a comfortable one.

Rough shape of published MCTs, to sanity-check what you are shown: domestic-to-domestic at a small airport can be under 45 minutes; the same-terminal international-to-international case is usually in the 60-90 minute band; anything crossing terminals, or entering a country's immigration, runs longer and is airport-specific. Treat the published number as a floor, never a plan.

## The Buffer Formula

```
one ticket:   safe = published MCT + 30 min if wide-body arrival or terminal change + connection_buffer_min
two tickets:  safe = 180 min minimum, + 60 min if bags are checked, + 60 min if immigration is crossed
```

And the two-ticket survivability test, which matters more than the number: **after leg 1 arrives 2 hours late, does a later departure on leg 2's route still exist that day?** If the answer is no, the itinerary has no plan B at any price, and that should be said out loud before it is booked.

`connection_buffer_min` defaults to 30 and is whatever the user has declared. Users with children, mobility needs or a hard commitment at the far end should be assumed to want more until they say otherwise (`passengers.md`).

## What Eats The Buffer

- Arriving at a remote stand and bussing to the terminal: 10-25 minutes before you are anywhere.
- Wide-body deplaning: the last rows leave 15-20 minutes after the doors open, and a tight connection assumes you are near the front.
- Terminal transfers with a train, and terminals that require re-clearing security.
- Immigration queues at peak banks, which are the reason published MCTs are long at hub airports.
- Gate-checked cabin bags returned at the aircraft door — a few minutes, but at the wrong moment.
- The inbound aircraft: the strongest available predictor of your departure delay is where the aircraft flying your flight is right now (`tracking.md`).

## Two Tickets

Legitimate, frequently the only affordable shape, and the risk must be stated rather than absorbed:

- Only offer them at all when `separate_tickets_ok` is true, or when the user asks and accepts the trade after hearing it.
- Book the second leg on a carrier and fare that can be changed cheaply, or on a route with many daily frequencies. The saving evaporates the first time a same-day rebooking is bought at the airport.
- Prefer an overnight break over a tight same-day connection when the fare gap is large: a cheap hotel is less than one walk-up ticket.
- Bags must usually be collected and rechecked. Some carriers will through-check on separate tickets when an interline agreement exists and the agent is willing — it is a courtesy, never a plan.
- Record the pairing in the `What` field of both rows in `~/Clawic/data/bookings/<year>.md`, so the risk is visible next time the trip is looked at.

## Virtual Interlining

Platforms that combine non-interlining carriers on one purchase and offer their own guarantee to rebook if a connection is missed.

- The guarantee is a commercial promise from the platform, not an airline obligation: rebooking happens on the platform's clock, on flights the platform buys, and reimbursement rules cap what is covered.
- No airline is party to the connection, so no airline owes duty of care between the two legs.
- Works best where the platform's own transfer product includes a buffer and the destination has frequent alternatives. Works worst on the last flight of the day, at airports needing immigration, and with checked bags.
- If the user has been burned by one, record that in `## How They Fly` and stop offering them.

## Immigration, Recheck and Preclearance

- **Entering the country of the hub** — most connections in the US, Canada and several others — means immigration, baggage reclaim, customs and re-drop, even when both legs are on one ticket. Budget hours, not minutes.
- **Airside transit** — most of Europe, the Gulf and East Asian hubs — means you never enter the country and the published MCT is realistic. Some nationalities still need a transit visa for airside transit (`documents.md`).
- **US preclearance** at certain foreign airports means you clear US immigration before departure and arrive as a domestic passenger: the connection at the US end is easy, the departure airport needs an extra 60-90 minutes.
- **Schengen boundary crossings** inside one airport add a passport control that the terminal map does not make obvious.

## Long Layovers

- 6-12 hours can be a mini-trip. Confirm the transit visa rule for the passport first, then whether bags can be left, then the real round-trip time to the city at that hour.
- Several hubs run free or subsidised city tours and stopover hotel programmes for long connections — check before booking a lounge day pass (`search.md`).
- Overnight in the terminal is a different proposition per airport: some close airside entirely.
- A long layover is also a buffer: on a two-ticket itinerary it is the cheapest insurance available.

## When It Is Already Going Wrong

Sequence, in order, while still in the air or on the ground:

1. Check whether the connection is still legally possible against the published MCT, using actual arrival time rather than scheduled.
2. On one ticket: you are already protected — find the next flights before landing so you can name the one you want when you reach an agent, and get on the app's rebooking screen, which is usually faster than the queue.
3. On two tickets: contact the second carrier before the departure time. A pre-departure change is a fee; a no-show is the whole fare.
4. Missed anyway: `disruptions.md` for rerouting and rights, then open the row in `## Claims` in `~/Clawic/data/flight/memory.md` if anything is owed, with its deadline in `## Due`.

**What gets written here**: a two-ticket pairing goes in the `What` field of both rows in `~/Clawic/data/bookings/<year>.md` ("self-transfer, paired with `<locator>`"), because the risk is invisible once the two rows look independent. A connection that failed, or an airport the user now refuses to connect through, goes in `## How They Fly` in `memory.md` — it changes every future search, and nobody wants to explain it twice.
