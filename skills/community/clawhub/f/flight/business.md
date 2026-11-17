# Corporate And Business Travel

Scope: flying on someone else's money, under someone else's rules, with a receipt that has to survive an audit. Different constraints, different failure modes, and two clocks that quietly destroy value.

**Before booking a work trip**, read `config.yaml` for `booking_channel` (a corporate agency may be mandatory) and `## Boxes` for any `artifacts/policy-*.md` covering this employer's rules.

**Contents:** [Policy Is A Filter, Not A Price](#policy-is-a-filter-not-a-price) · [Channel: Agency, Direct, Or Self-Book](#channel-agency-direct-or-self-book) · [Unused Ticket Credits](#unused-ticket-credits) · [Invoices And VAT](#invoices-and-vat) · [Expensing](#expensing) · [Whose Points Are They](#whose-points-are-they) · [Duty Of Care](#duty-of-care) · [Frequent Traveller Economics](#frequent-traveller-economics)

## Policy Is A Filter, Not A Price

Corporate travel policy usually defines: an advance-purchase minimum, a cabin threshold by flight duration, a preferred-carrier list, a fare-type rule, and an approval step above a value. What follows:

- The cheapest compliant option is the goal, not the cheapest option. Presenting a non-compliant fare wastes an approval cycle.
- Advance-purchase rules are where most of the saving actually lives, and they are the rule most often broken.
- A refundable or flex fare is often mandated for trips that can move; the policy is buying optionality, and arguing against it with a headline price misses the point (`fares.md`).
- The cabin threshold is usually stated in flight hours, so a routing with a connection can cross it and change what may be booked.
- Where an employer's rules matter repeatedly, save them once as `~/Clawic/data/flight/artifacts/policy-<employer>.md` with its `## Boxes` line, rather than re-deriving them each trip.

## Channel: Agency, Direct, Or Self-Book

| Channel | Gains | Costs |
|---|---|---|
| Corporate travel agency / online booking tool | Negotiated fares, policy enforcement, duty-of-care tracking, one point of contact during a disruption | Transaction fees, a fare set that hides some options, and slower changes out of hours |
| Direct with a preferred carrier | Corporate discount codes still apply, better handling during disruption (Rule 4) | Does not feed the company's reporting unless recorded |
| Self-book and expense | Cheapest and fastest | May breach policy, and the company loses visibility of where its people are |

If a trip is booked outside the mandated channel, the reason should be stated at the time — the approval question is asked later, when nobody remembers.

## Unused Ticket Credits

The most reliably wasted asset in corporate travel.

- When a non-refundable ticket goes unused, the value usually survives as a credit — and it typically expires **twelve months from the date of issue, not from the travel date**, which means a ticket bought in January for a June trip may already be half-expired when the trip is cancelled in May.
- Credits are often locked to the original traveller, sometimes to the original route, and usually unusable for taxes and ancillaries.
- Agencies hold a pool of unused credits and will apply them if asked. Many are never asked.
- Ask, at every booking: *is there a credit on file for this traveller?*
- **Every credit gets a `## Due` row on the day it exists**, with value, currency, expiry and any restriction (`refunds.md`).

## Invoices And VAT

Recovering tax on air travel is jurisdiction-specific and time-limited, and the second condition is what breaks it.

- Domestic and intra-regional flights carry recoverable tax in several jurisdictions; international flights are commonly zero-rated, so there may be nothing to recover regardless of the invoice.
- The document needed for reclaim is a **proper invoice**, not the booking confirmation and not the card receipt: it must show the seller's tax registration, the buyer's details and the tax amount separately.
- Airlines issue invoices through a self-service portal, usually within a **finite window** after travel — often measured in weeks or a few months. After it closes, many simply will not issue one.
- Booking through an agency means the invoice comes from the agency for its fee and from the airline for the fare, and both are needed.
- The company's own tax details must be on the booking, or the invoice comes out in the traveller's name and is unusable.
- Set a `## Due` row at booking for retrieving the invoice after travel. This is a small task that expires.

## Expensing

- Capture at the moment: the itinerary with the ticket number, the card receipt, the invoice, and any ancillary receipts (bags, seats, lounge, ground transport at both ends).
- Ancillaries are charged separately and appear as separate card lines — the ones that get lost are the seat and bag charges bought weeks after the fare.
- Currency: record the amount in the charged currency and let the finance system convert. Recording a converted figure loses the audit trail.
- Where the personal card carries the travel insurance benefit but the company card is mandated, know which one you actually paid with before assuming coverage (`refunds.md`).
- Trip spend itself belongs in the company's system; what belongs in `~/Clawic/data/` is the booking row and its deadlines, never card numbers.

## Whose Points Are They

- Most employers let the traveller keep frequent-flyer points and status while the company pays. Some do not, and a few claim them.
- Points earned on a corporate-negotiated fare may be reduced or excluded by the fare class, whatever the policy says (`points.md`).
- Choosing a marginally dearer flight to earn status on a personal account is the compliance question most people get wrong: the honest framing is that the company is buying the itinerary, and the tie-break belongs to it.
- Record the crediting programme once in `## Loyalty` and stop deciding per trip.

## Duty Of Care

Employers have a legal obligation to know where their travelling employees are and to be able to reach them. Practical consequences for booking:

- A trip booked outside the mandated channel is invisible to that system, which is the real reason self-booking is discouraged.
- Itinerary changes made directly with the airline during a disruption should be reported back into the company's system the same day.
- Risk-rated destinations may require pre-approval, briefings or specific insurance, and that process has a lead time longer than the flight booking.

## Frequent Traveller Economics

For someone flying regularly on business, the levers that pay, in rough order:

1. **Concentrate flying in one alliance** to reach a tier that removes bag fees, seat fees and change friction (`points.md`).
2. **Use the same hub routing** where possible: the airline's recovery options for you are best where it has the most flights.
3. **Book flexible fares on genuinely movable trips**; the change fee avoided over a year exceeds the premium for anyone who moves one trip in four.
4. **Keep the credits ledger current** — the annual loss to expired credits typically exceeds anything gained by shopping fares harder.
5. **Choose the earlier flight** for anything unmissable: an early departure has same-day alternatives behind it, and the last flight of the day has none (`connections.md`).

**When a trip is booked for work**, the row goes in `~/Clawic/data/bookings/<year>.md` like any other, with the invoice-retrieval date and any credit expiry in `## Due`. **When an employer's policy or an airline's invoice procedure has been worked out once**, it becomes `~/Clawic/data/flight/artifacts/policy-<employer>.md` or `artifacts/invoice-<airline>.md`, with its `## Boxes` line added in the same turn.
