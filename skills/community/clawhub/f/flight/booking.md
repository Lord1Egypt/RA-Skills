# Buying The Ticket

Scope: the purchase itself and the first hour after it. What the fare is: `fares.md`. What happens when it breaks: `disruptions.md`.

**Before buying anything**, read `~/Clawic/data/bookings/<year>.md` for clashes with trips already held, and `## Travellers` in `memory.md` for the exact name spelling and document validity of everyone on the reservation.

**Contents:** [Where To Buy](#where-to-buy) · [Codeshares and Who Operates](#codeshares-and-who-operates) · [Names Must Match The Passport](#names-must-match-the-passport) · [Payment](#payment) · [The Post-Purchase Check](#the-post-purchase-check) · [Holds and 24-Hour Windows](#holds-and-24-hour-windows) · [Changing A Ticket](#changing-a-ticket) · [Check-In](#check-in) · [What To Record](#what-to-record)

## Where To Buy

| Channel | Buy here when | Cost of doing so |
|---|---|---|
| Operating airline, direct | Default (Rule 4). Anything with a connection, a fixed commitment, or a likely change | Occasionally a few percent dearer |
| Marketing airline of a codeshare | The itinerary is only sold as one ticket by that carrier | Check-in and irregularity handling split between two carriers |
| OTA / consolidator | Materially cheaper, or the only source of a multi-carrier single ticket | The airline generally will not reissue; the OTA must, on its own hours |
| Virtual-interlining platform | Two carriers that do not interline, and the user accepts the model | No airline is party to the connection; the platform's guarantee is the whole protection |
| Corporate travel agency | The trip is on company policy and needs to be | Policy filters may hide the cheapest option (`business.md`) |
| Anything else — a link, a broker, a social-media "deal" | Never without verifying the ticket number afterwards | Fraudulent ticketing exists and is usually discovered at check-in |

Standing test before choosing a channel: *if this flight is cancelled at 22:00 the night before, who has the authority to put me on another aircraft, and are they open?*

## Codeshares and Who Operates

A flight number belonging to one airline, flown by another, changes practical things:

- **Check-in and the airport desk** belong to the operating carrier. Turning up at the marketing carrier's terminal is a common and expensive mistake at multi-terminal airports.
- **Baggage allowance** on an interline itinerary follows the most significant carrier for the journey, not whoever sold the ticket (`baggage.md`).
- **Seat selection** often cannot be done on the marketing carrier's site; use the operating carrier's booking reference, which differs from the one on the confirmation email.
- **Points** credit according to the operating carrier's fare class as mapped by whichever programme you credit to (`points.md`).
- **Disruption handling** is done by the operating carrier at the airport and by the marketing carrier on the phone, and they will disagree. The operating carrier controls the aircraft.

## Names Must Match The Passport

- Given name and surname exactly as on the passport's machine-readable zone. Middle names may be omitted where the airline's field does not accept them; nothing may be invented.
- Composite Spanish and Portuguese surnames, hyphenated names, and suffixes cause the recurring mismatch. Enter both surnames where the passport shows both.
- A spelling correction of a few characters is normally free or cheap within 24-48 hours of purchase and is a reissue afterwards. **A wrong name found at check-in is a new ticket at the day's fare.**
- Titles and gender fields must match the document, because they are transmitted in the advance passenger data.
- Check every passenger against `## Travellers` before paying, and record the exact spelling there afterwards.

## Payment

- Pay with a card that carries travel protection, and know what triggers it: many benefits require the whole fare on that card, and cover delay, cancellation and baggage only above defined thresholds (`refunds.md`).
- A credit card gives a chargeback route that a debit card and most instant-transfer methods do not — this is what matters if the airline or the agency fails.
- Pay in the fare's own currency; decline dynamic currency conversion at checkout.
- Do not save card details in an OTA account for a single purchase. Never record any card number in `~/Clawic/data/`.
- Third-party "pay in instalments" offers at checkout complicate refunds — the refund goes back through the lender, not the card.

## The Post-Purchase Check

Run this in the same session as the purchase. Reservations that pass this are tickets; ones that do not are cancelled silently overnight.

- [ ] A **ticket number** exists (13 digits, airline prefix), not merely a "confirmed" reservation
- [ ] Names match the documents, character for character
- [ ] The itinerary shows the expected operating carriers and flight numbers, and the terminals for each
- [ ] Frequent-flyer numbers attached, one per passenger, to the programme they intend to credit
- [ ] Seats assigned or a plan for when they open (`seats.md`)
- [ ] Bags purchased if needed — cheaper now than later, and much cheaper than at the airport
- [ ] Special requests entered: meals, assistance, infant, pet, sports equipment (`passengers.md`)
- [ ] Fare rules saved as a screenshot or PDF, with the change and cancel terms visible
- [ ] Confirmation stored where it survives a dead phone

## Holds and 24-Hour Windows

- Some carriers sell a paid or free hold for 24-72 hours at the searched price. Worth it when a document check, a visa lead time or a companion's decision is outstanding.
- The statutory 24-hour free cancellation on US-anchored tickets bought at least 7 days out is a free hold in disguise: buy, verify everything, cancel without cost if anything fails.
- Award holds vary by programme; where they exist, they are the safe way to sequence a points transfer (`awards.md`).

## Changing A Ticket

- Compute the real cost before touching anything: `change fee + fare difference in the same fare family`. The fare difference is usually the larger half, and it is calculated against today's price for the new dates.
- Changing one leg of a return can reprice the entire ticket. Ask for the total, not the fee.
- On a voluntary change the airline chooses the rebooking rules; on an involuntary one (schedule change, cancellation) they do not, and much more is available for free (`refunds.md`).
- Same-day change and standby are separate cheaper products on several carriers, usually excluded from the lowest fares.
- Cancel before departure even when nothing is refundable: it preserves taxes and any residual value, while a no-show usually destroys the rest of the itinerary (`fares.md`).

## Check-In

- Opens typically at T-24h; some low-cost carriers charge for airport check-in, and some open earlier for higher fare families or elite tiers.
- Advance passenger information (document details) is entered here for international travel and is where a mismatched document surfaces — early enough to fix.
- Boarding passes: keep the airline's own app copy and one offline copy. Never store the barcode image in `~/Clawic/data/` — it decodes to the record.
- Put the check-in opening time in `## Due` for any carrier that charges for airport check-in, and for any flight where seats are assigned at check-in.

## What To Record

**The moment a ticket is issued**, write its row in `~/Clawic/data/bookings/<year>.md` — locator, `flight`, provider, route and cabin, dates, passengers, amount with currency, `ticketed`, and the change rule in a few words. Then add every clock it creates to `## Due` in `memory.md`: the end of the free-cancellation window, check-in opening, any document renewal the trip now depends on, and the date the fare stops being changeable. A booking recorded without its deadlines is half a record, and the deadlines are the expensive half.

**If the trip is being run as a project** — a relocation, a multi-city work tour, an event with its own plan — the itinerary summary also goes to the shared `~/Clawic/data/projects/<trip>.md`: dates, travellers, one line per flight with its locator, updated in that file in place and never duplicated into a second file. Fares, fare rules, seats, points and claims stay in this skill (`memory-template.md`, shared projects pointer).
