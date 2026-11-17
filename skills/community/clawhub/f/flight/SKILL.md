---
name: Flight
slug: flight
version: 1.0.3
description: 'Searches, compares, books, and fixes flights — fares and fare rules, connections, baggage, seats, miles, delays, and passenger rights. Use when someone needs a flight found or priced, asks whether a fare is a good deal or whether to book now, is choosing between cash and miles, or wants an award seat found. Use for everything after the ticket is issued: seat selection and upgrades, baggage allowance and fees, a tight connection, a schedule change, a delayed or cancelled flight, a missed connection, denied boarding, a lost or damaged bag, a refund, a voucher, or an EU261/UK261/US DOT compensation claim. Also for passport, visa, and ESTA/ETA rules tied to a specific itinerary, flying with infants, minors, pets or special assistance, corporate travel policy, elite status, and points expiry. Not for hotels and accommodation (`booking`), whole-trip itineraries and packing (`travel-planning`), car hire (`car-rental`), or Expedia-specific workflows (`expedia`).'
homepage: https://clawic.com/skills/flight
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: ✈️
    os:
    - linux
    - darwin
    - win32
    displayName: Flight
    configPaths:
    - ~/Clawic/data/flight/
    - ~/Clawic/data/bookings/
    - ~/Clawic/data/contacts/
    - ~/Clawic/data/finances/
    - ~/Clawic/data/projects/
    - ~/Clawic/profile.yaml
    - ~/flight/
    - ~/clawic/flight/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/flight/
      - ~/Clawic/data/bookings/
      - ~/Clawic/data/contacts/
      - ~/Clawic/data/finances/
      - ~/Clawic/data/projects/
      - ~/Clawic/profile.yaml
      - ~/flight/
      - ~/clawic/flight/
---

**Data.** At the start of every session, read `~/Clawic/data/flight/config.yaml` (what the user declared) and `~/Clawic/data/flight/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition written on its line applies — that index *is* the list of files; never work from a list of names carried in your head, because most boxes are created after this skill was written. Read `~/Clawic/data/bookings/<current year>.md` before answering anything about an existing trip, a date, a locator, or "what have I got booked". If none of it exists, work from defaults and say nothing about it. If data sits at an older location (`~/flights/`, `~/flight/`, `~/Clawic/flight/`), move it to `~/Clawic/data/flight/` and say so in one line. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens.

**Write before the session ends** whenever it produced something durable: a ticket issued, changed or cancelled; a flight actually flown; a price seen for a route being watched; a points balance, tier or requalification number; a passport, visa or ETA expiry; a claim opened, paid or refused; a voucher or credit with an expiry date; or something the user will want to read again — an entry-requirement procedure, an award routing that worked, a claim letter that got paid. `memory-template.md` lists every destination, format and threshold, and is the only file you open in order to write.

**Tickets go to the shared box `~/Clawic/data/bookings/<year>.md`**, not into this skill's folder: hotels, trains and car hire land in the same file, so "what do I have in October" answers itself. One row per booking, identified by its **record locator** — read the file and search for the locator before adding, update that row in place when it already exists, and never touch a row whose `Type` is not `flight`. Cancelled or flown rows are moved out, not left to rot (`memory-template.md`).

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. Store the pointer and drop the value: `keychain:ba-executive-club`, `1password:Travel/Iberia`, `env:DUFFEL_API_KEY`. Passport and ID numbers, boarding-pass barcodes and images, programme PINs and card numbers are never stored at all, in any file (`memory-template.md` has the two lists).

Flights are bought on a headline fare and paid for in fees, and the expensive mistakes happen after the ticket is issued, not during the search. Give the total, name the fare rule that will bite, and act on the clock. Work from defaults immediately: never open by asking about home airports, budget or how proactive to be. Two exceptions to silence, both statements rather than questions: while `home_airports` is unset, say which origin you are assuming before searching (Rule 1); while `passport_country` is unset, say that entry rules depend on nationality and ask for it only when an actual entry requirement is at stake. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: currency, locale, timezone) → the Configuration table default.

## When To Use

- Finding, comparing or pricing a flight: routes, dates, alternate airports, cash versus miles, "is this a good price", "should I book now"
- Deciding what to buy: fare families and fare rules, refundability, basic economy, direct versus OTA, one ticket versus two
- Anything after the ticket exists: seats, upgrades, baggage, name corrections, schedule changes, check-in, connections that look tight
- Something went wrong: delay, cancellation, missed connection, denied boarding, downgrade, delayed or damaged bag — including whether money is owed and how to claim it
- Loyalty economics: award searches, transfer partners, cents-per-point, elite status, requalification, expiring points and vouchers
- Trip-critical paperwork tied to a specific itinerary: passport validity, visas, ESTA/ETA, transit rules, minors, pets, assistance
- Mode: **advise by default** — present options with their total cost and let the user pick; act directly (search, monitor, draft the claim, fill the form) when the user asks for it. This skill never completes a payment on the user's behalf
- Not for accommodation (`booking`), the shape of the whole trip (`travel-planning`), ground transport (`car-rental`), or one platform's own workflow (`expedia`)

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| "Find me a flight to X" | Origin set from `home_airports`, ±3 days, alternate airports, then total cost per option — never the headline fare | `search.md` |
| "Is this a good price?" | Compare against the stored range for that route in `## Routes`, not against a feeling | `tracking.md` |
| "Should I book now or wait?" | Booking-window bands below, then set a target price and stop watching | `tracking.md` |
| Cheap fare, unclear what it includes | Read the fare family: bag, seat, change, refund, credit, no-show rule | `fares.md` |
| Choosing where to buy: airline, OTA, meta | Who controls the ticket during a disruption decides, not the €12 saving | `booking.md` |
| Connection looks tight, or it is two tickets | MCT + buffer formula; separate tickets are a different product | `connections.md` |
| Seats, upgrades, extra legroom, sitting together | Seat map source, upgrade mechanics, family-seating rules | `seats.md` |
| Bags: allowance, fees, sports gear, batteries, a bag that did not arrive | Whose allowance applies, the 21-day clock, the liability cap | `baggage.md` |
| Delayed, cancelled, misconnected, bumped, downgraded | Fix the routing first, then the money — the two are separate tracks | `disruptions.md` |
| Money back: refund, voucher, insurance, chargeback, airline collapse | Which of the five refund paths applies, and its deadline | `refunds.md` |
| Cash or miles for this ticket | cents-per-point against the real cash price, taxes deducted (Rule 7) | `points.md` |
| Finding award space, transfer partners, sweet spots | Availability first, transfer second — transfers are one-way | `awards.md` |
| Passport, visa, ESTA/ETA, transit, onward ticket | Document clock before price comparison (Rule 5) | `documents.md` |
| Infants, children, unaccompanied minors, pets, wheelchair, medical | Notice windows and the things that must be added at booking | `passengers.md` |
| Corporate trip, expense policy, VAT invoice, unused credits | Invoice window and credit expiry are the two things people lose | `business.md` |
| Building something that searches or tracks flights | Which APIs can actually book, which only redirect | `apis.md` |
| Anything else about flying | Answer directly, then state the total cost and the next deadline it creates | — |

Coverage map: `search.md` finding it · `fares.md` what the fare actually is · `booking.md` buying it · `connections.md` making the connection · `seats.md` where you sit · `baggage.md` what you carry · `disruptions.md` when it breaks · `refunds.md` getting money back · `points.md` earning and valuing · `awards.md` spending points · `documents.md` being allowed in · `passengers.md` who is travelling · `tracking.md` prices and status over time · `business.md` corporate and expensing · `apis.md` building on flight data.

## Core Rules

1. **Search from a stated origin, over a range.** Set origin from `home_airports`; while that is unset, name the origin you are assuming out loud before searching. Search ±3 days by default and include airports within a 2-hour surface journey — both routinely move the price by double digits on the same route, and neither costs anything to check. Cap the alternate-airport detour at the point where the ground cost and the extra hours exceed the saving; that comparison goes into the option table, not into your head.
2. **Price the trip, not the fare.** `total = fare + bags you will actually check or carry + seat selection + payment-method surcharge + surface transport at both ends + the cost of the change you might need`. A €9.99 headline with one cabin bag, one seat and an airport bus lands in the €60-90 band on European low-cost carriers; the comparison is only honest once every option carries the same line items (`search.md`).
3. **Three sources, chosen for different blind spots.** One metasearch for the shape of the market, one aggregator that actually lists low-cost carriers, and the operating airline's own site — which is the only place showing the fare rules you will be held to, and often the only place selling the fare family that includes a bag. A recommendation from a single source is a guess.
4. **Buy from the operating airline unless there is a reason not to.** When an OTA holds the ticket, the airline generally will not reissue it during a disruption: the agency has to, on its own queue, in its own hours. Escape hatch: buy elsewhere when it is the only way to combine carriers, or when the saving is material *and* the itinerary is a single non-stop with nothing to reroute. Never through an OTA on a tight connection or a trip with fixed onward commitments (`booking.md`).
5. **Check the document clock before the price.** Passport validity, visa or ETA lead time, transit rules and onward-ticket enforcement void the whole purchase, so they are cheaper to check first: the common two are the 6-months-beyond-arrival rule most of Asia and the Middle East apply, and Schengen's pair — valid at least 3 months beyond intended departure *and* issued within the previous 10 years. Every document expiry that touches a booked trip gets a `## Due` row (`documents.md`).
6. **A connection you cannot miss needs the airline's MCT plus a buffer.** On one ticket, take the published minimum connection time for that airport and add 30 minutes for a wide-body arrival or a terminal change, plus `connection_buffer_min`. On two tickets, the buffer starts at 3 hours, and the last departure of the day on the second leg must still exist after your first leg is 2 hours late — otherwise there is no plan B to buy (`connections.md`).
7. **Miles are only cheap when the cash fare is expensive.** `cpp = (cash price − taxes and fees payable on the award) ÷ points × 100`. A £480 fare against 25,000 points plus £180 in surcharges is (480−180)÷25000×100 = 1.2 cpp — a poor use of transferable points, a fine use of an expiring airline balance. Baselines to beat: roughly 1.2-1.5 cpp in economy, 2 cpp and up in a premium cabin. Never transfer points to a programme before the award seat is confirmed or held: transfers are one-way and almost never reversed (`points.md`).
8. **Never recommend a tactic that voids the ticket.** Hidden-city and throwaway ticketing breach nearly every carrier's conditions of carriage: skipping a segment cancels every later segment on that ticket, a checked bag travels to the ticketed destination, and the exposure is points clawback or account closure. If the user raises it, explain the mechanism and the risk, then give the legal shape that gets the same saving — one-ways, an open jaw, a positioning flight on a separate ticket (`fares.md`).
9. **A reservation is not a ticket.** Before treating anything as booked, confirm a ticket number exists, the name matches the passport exactly, the frequent-flyer number is attached, seats are assigned, and the fare rules are saved. Unticketed reservations are cancelled silently, and a name mismatch found at check-in is a reissue at full fare (`booking.md`).

## True Cost

The comparison table that makes the decision. Every option carries every line, even at zero, or the cheapest row is just the one that hid the most.

| Line item | Where it bites | How to price it |
|---|---|---|
| Base fare + carrier-imposed charges | Award tickets too: surcharges are levied on points bookings by several carriers | The number after taxes, in `currency` |
| Cabin bag | Low-cost carriers sell the overhead bin separately; a personal item under the seat is what "free" means | Priced at booking is cheaper than at the airport, which is cheaper than at the gate — often by 2-3× |
| Checked bag | Cheapest online pre-purchase, dearest at the desk | Per direction, per passenger; on separate tickets, per ticket |
| Seat | Basic fares assign at check-in, families get split | Price only what you would actually pay for (`seats.md`) |
| Payment surcharge | Card-type surcharges and currency conversion when the fare is not in your currency | Pay in the fare's own currency and let your card convert |
| Surface transport | The "same city" airport that is 90 minutes away | Both ends, both directions, at the actual hour of arrival |
| Change and cancel exposure | The fare's own rule, not the airline's brand | Fee + fare difference, or the value of the credit and its expiry |
| Time | A 21-hour two-stop against a 9-hour non-stop | State the elapsed hours next to the price; do not decide it for them |

## Deadlines That Expire Value

This domain loses more money to clocks than to bad prices. Every applicable row becomes a `## Due` line in `memory.md` the moment the booking exists.

| Clock | Typical window | Consequence of missing it |
|---|---|---|
| Free cancellation after purchase | 24 hours on tickets to/from the US bought at least 7 days out; varies elsewhere and by seller | The whole ticket becomes a change fee plus a fare difference |
| Special assistance, pets, extra oxygen, bassinet | 48 hours' notice minimum, and inventory runs out much earlier | Denied service at the gate, legally |
| Online check-in | Usually T-24h; some low-cost carriers charge for airport check-in | A three-figure fee on a two-figure fare |
| Delayed-bag claim | Report before leaving the airport; written claim within 21 days of the bag being returned, 7 days for damage | The carrier's liability ends |
| Compensation claim | 1 to 6 years depending on the country whose law applies | The claim is time-barred, whatever its merit |
| Voucher / travel credit | Commonly 12 months from *issue*, not from the flight | Silent expiry, no reminder |
| Points balance | Programme-specific; many reset the clock on any qualifying activity | Balance zeroed with no notice |
| Elite requalification | The programme's year end, which is often not December | Tier lost, then a full year to earn back |
| Passport / visa / ETA | The 6-month and Schengen rules, plus renewal lead time | Boarding refused at the departure gate |

## Booking Windows

Honest version: no public service predicts a specific route's price, and the "best day to book" studies contradict each other because the effect is small next to route-level variance. What survives:

- **Domestic:** the useful band is roughly 1-3 months out. **Long-haul:** roughly 2-6 months. **Peak dates** (Christmas, Lunar New Year, August in Europe, school holidays): earlier than feels reasonable, because the cheap fare buckets sell out rather than the price rising smoothly.
- **Departure day beats booking day.** Mid-week departures usually price below Friday and Sunday departures — Google Flights' own published analysis puts it in the low double digits for domestic trips — while the day of the week you buy on is worth a percent or two and is not a strategy.
- **The last 21 days are a different market.** Fares rise on business-travel demand; below 7 days out, expect the top of the historical range.
- **Set a target and stop looking.** Use the stored range in `## Routes`; book at 10-20% below the route's own typical price. Checking daily converts a stable market into anxiety and a worse decision.
- Prices seen while researching are worth recording either way — that stored range is the only thing that makes the next "is this good?" answerable (`tracking.md`).

## Rights At A Glance

Route into `disruptions.md` before quoting a number: the regimes below are amended, and the EU's has been under active revision. Verify the current threshold and amount before promising money.

| Where | What triggers money | Roughly how much | Care regardless of cause |
|---|---|---|---|
| EU261 — departing the EU on any airline, or arriving in the EU on an EU airline | Arrival 3+ hours late, cancellation with under 14 days' notice, denied boarding | €250 / €400 / €600 by distance band, halved when the rerouting lands close behind | Yes: meals, communication, hotel and transfers while you wait |
| UK261 — same shape, UK-anchored | As above | £220 / £350 / £520 | Yes |
| US DOT | No delay compensation exists. Cancellation or a significant change gives an automatic cash refund; involuntary denied boarding pays a multiple of the one-way fare up to a capped ceiling | Refund, or the denied-boarding multiple | No federal right to meals or hotel — it is airline policy |
| Canada APPR / Brazil ANAC and similar | Tiered by delay length and airline size; cause tests differ | Set by regulation | Yes, above defined delay lengths |
| Anywhere | Baggage loss, damage or delay on an international itinerary is capped by the Montreal Convention | A cap in SDR, revised every five years | — |
| Anything else | The carrier's conditions of carriage are the floor, and its schedule-change policy is usually more generous than the law | — | — |

Extraordinary circumstances (weather, air-traffic control, security) remove the compensation but never the duty of care or the refund.

## Output Gates

Before presenting an option, a booking, or a claim:

- Does every option in the comparison carry the same cost lines, including bags and surface transport (Rule 2)?
- Have I named the fare rule that decides what happens if this trip changes — change fee, credit, refund, or nothing?
- Does every connection in what I am recommending clear the MCT-plus-buffer test, and did I say what happens if it is missed (Rule 6)?
- Have I checked the document clock for this specific nationality and route before comparing prices (Rule 5)?
- Am I quoting a compensation amount or a deadline? Then I checked the current rule rather than reciting it.
- **Persistence:** did this session produce a ticket, a flown flight, a price for a watched route, a balance or tier, a document expiry, a claim, or a voucher? Each one has a destination in `memory-template.md`, and anything with an expiry also gets its `## Due` row — in this turn, not "later".

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/flight/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| home_airports | list (IATA codes, preferred first) | none | Origin for every search and price alert; while unset, name the assumed origin before searching (Rule 1) |
| passport_country | list (ISO country codes, one per traveller document) | none | Drives every visa, ETA, transit and entry answer in `documents.md`; while unset, entry requirements are stated as nationality-dependent |
| cabin | economy \| premium-economy \| business \| first | economy | Cabin searched and priced, and the cpp baseline applied in Rule 7 |
| currency | text (ISO 4217) | from `profile.yaml`, else USD | Currency of every quote, target price and stored amount |
| max_stops | number (0-2) | 1 | Filters itineraries before comparison; 0 turns non-stop into a hard requirement rather than a preference |
| connection_buffer_min | number (minutes) | 30 | Added on top of the published MCT in the Rule 6 test and in `connections.md` |
| carry_on_only | bool | false | Removes checked-bag cost from the True Cost table and changes the fare family recommended |
| separate_tickets_ok | bool | false | Whether self-transfer and virtual-interlining itineraries are offered at all (`connections.md`) |
| booking_channel | direct \| ota \| either | direct | Where options are sourced and bought (Rule 4) |
| loyalty_focus | text (programme or alliance) | none | Which programme's earning, routing and award charts are checked first (`points.md`, `awards.md`) |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — which metasearch, aggregator and award-search tools the user trusts, and which they refuse to buy through — affects the three sources of Rule 3
- **Comfort and timing** — red-eye tolerance, earliest departure and latest arrival, aircraft and cabin preferences, seat type, maximum elapsed journey time — affects ranking in `search.md` and `seats.md`
- **Restrictions** — airlines vetoed for any reason, no basic economy, no overnight layovers, dietary and special meals, accessibility needs, travelling with a companion who has their own constraints — affects filtering before options are shown
- **Risk posture** — appetite for non-refundable fares, self-transfer, tight connections and error fares; whether travel insurance is expected on every trip — affects Rule 4, Rule 6 and `refunds.md`
- **Payment ecosystem** — which points currency and cards the user actually holds, which airline programme credits their flying, whose lounge access matters — affects `points.md` and `awards.md`
- **Presentation** — how many options to show, whether to lead with cheapest or fastest, whether every answer carries the total-cost table — affects the shape of every recommendation
- **Cadence** — how often to check watched routes, when to audit points and tiers, when to re-check passport validity — affects the `## Due` table

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Comparing headline fares across carriers | The fares include different products; the cheapest headline is frequently the dearest trip | The True Cost table, every line filled for every option (Rule 2) |
| Booking two tickets to save money without saying so | The saving is real; the risk transfer is invisible until leg 1 is late and nobody owes anything | Price it as a different product, with the 3-hour rule and a named plan B (`connections.md`) |
| Trusting an aggregator's baggage figures | Aggregators infer allowances and get fare families wrong, especially on low-cost and basic fares | Confirm on the operating carrier's own fare page before quoting a total |
| Booking an award before the seat is confirmed | Transferred points are stranded in a programme the user does not use | Confirm or hold the seat, then transfer (Rule 7) |
| Treating a schedule change as bad luck | A significant change usually unlocks a free rebooking or a full refund, including on non-refundable fares | Read the carrier's schedule-change policy and ask for the rebooking you actually want (`refunds.md`) |
| Accepting a voucher at the desk during a disruption | Accepting a voucher can settle a statutory claim worth several times more | Refund or reroute first, compensation claimed separately afterwards (`disruptions.md`) |
| Leaving the airport without a bag report | The report reference is the entire claim; issuing one later is a negotiation | File before leaving, photograph the tag and the report, start the 21-day clock (`baggage.md`) |
| Adding the frequent-flyer number after flying | Retro-claims work but need boarding pass and receipt, and some fare classes earn nothing regardless | Attach at booking, verify it posted within a week (`points.md`) |
| Assuming the marketing carrier's baggage rules apply | On an interline itinerary the most significant carrier's allowance governs the whole trip | Identify the operating and most significant carrier before quoting bags (`baggage.md`) |
| Renewing a passport "when it expires" | Most refusals happen on valid passports that fail the 6-month or 10-year rule | Diary the renewal against the rule, not the expiry date (Rule 5) |
| Chasing a price daily | Attention is the cost, and it produces worse timing, not better | Target price, alert, stop looking (`tracking.md`) |
| Buying trip insurance without reading the card benefit already held | Double coverage, and the card benefit often requires paying with that card to apply at all | Check the card's own terms first, then buy only the gap (`refunds.md`) |

## Where Experts Disagree

- **Book early versus wait.** Both camps are right about different products: on a route with many carriers and daily frequencies, waiting for a target price wins; on a thin route, a peak date or a family-sized party, the cheap inventory sells out and waiting only buys a worse seat map. Frequency and party size decide, not the calendar.
- **Direct versus OTA.** Consolidator and OTA pricing on multi-carrier itineraries is genuinely cheaper and sometimes the only way to combine two airlines on one ticket. The disagreement is about disruption handling, and it is settled by who has to reissue the ticket at 6am (Rule 4).
- **Points maximizing versus cash simplicity.** Above roughly 2 cpp in a premium cabin the points game beats cash back by a wide margin; below ~1.2 cpp it is an unpaid hobby with devaluation risk. The frontier is how much flying is already happening — points optimization pays in proportion to volume.
- **Insurance versus card coverage.** Card benefits are free but conditional (paid with that card, specific delay lengths, secondary coverage). Standalone policies pay more reliably on medical and cancellation. The split most practitioners land on: card coverage for delay and baggage, a policy for medical and cancel-for-cause on expensive or long trips.
- **Self-transfer platforms.** Their own guarantees do rebook you, and the products have matured; what has not changed is that no airline is involved, so an immigration queue or a strike leaves you with a claim against a platform rather than a seat on the next flight.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/flight (install if the user confirms):
- `booking` — accommodation search and reservation, the other half of most trips
- `travel-planning` — itineraries, multi-city routing, packing, whole-trip budgets
- `car-rental` — ground transport at the far end
- `money` — where trip spend and card annual fees actually get tracked
- `expedia` — one platform's own search, package and booking workflow

## Feedback

- If useful, star it: https://clawic.com/skills/flight
- Latest version: https://clawic.com/skills/flight

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/flight.
