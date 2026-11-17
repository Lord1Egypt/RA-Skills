# Getting Money Back

Scope: the five routes by which money returns, which one applies, and its deadline. Statutory compensation for a disrupted flight is a different track (`disruptions.md`); this is about the fare itself.

**Before starting**, read the ticket's row in `~/Clawic/data/bookings/<year>.md` for the fare rule and the amount paid with its currency, and `## Claims` for anything already open on the same booking.

**Contents:** [Which Route Applies](#which-route-applies) · [Refund From The Airline](#refund-from-the-airline) · [Taxes On Unused Tickets](#taxes-on-unused-tickets) · [Vouchers And Credits](#vouchers-and-credits) · [Travel Insurance](#travel-insurance) · [Card Benefits](#card-benefits) · [Chargeback](#chargeback) · [When The Airline Fails](#when-the-airline-fails) · [Recording It](#recording-it)

## Which Route Applies

Work down this table; the first row that matches is the cheapest and fastest route, and the ones below it are fallbacks, not alternatives.

| What happened | Route | Typical window |
|---|---|---|
| Bought minutes or hours ago, US-anchored, 7+ days before departure | Statutory 24-hour cancellation | 24 hours |
| Airline cancelled, or changed the schedule beyond its significance threshold | Refund of the unused portion, in cash, even on a non-refundable fare | No fixed limit, but claim promptly |
| You cancelled a refundable or flex fare | Fare rule refund | Fare-rule dependent |
| You cancelled a non-refundable fare | Taxes only, plus any credit the rule gives | Before departure, always |
| Reason is illness, bereavement, jury service, visa refusal | Insurance, or the airline's own compassionate policy with documentation | Policy-dependent, usually days |
| Paid-for service not delivered — seat, bag, lounge, meal | Ancillary refund from the airline with the receipt | Weeks, carrier-dependent |
| Airline or agency ceased trading | Chargeback, then any statutory protection or insolvency cover | Card-scheme deadline |
| Anything else | Ask the airline in writing first; every other route asks whether you did | — |

## Refund From The Airline

- **Involuntary** (they cancelled or significantly changed) means cash back to the original payment method, and in the US that is now automatic and cannot be substituted with a voucher unless you choose one. Choosing a voucher is a decision to accept less liquidity for a bonus; take it only if the user flies that airline regularly.
- **Voluntary** means the fare rule governs, and the fare rule is what you screenshotted at purchase (`fares.md`).
- Refunds go back to the card used, not to the traveller, which matters for company-paid and gift bookings.
- Timelines are regulated in several jurisdictions (commonly 7 days to the card, longer for other methods) and routinely missed. A polite reminder quoting the timeline is more effective than a second claim.
- Bought through an agency: the agency refunds you, the airline refunds the agency, and the agency's own service fee is usually not refundable. This is the tax on the OTA saving (Rule 4).

## Taxes On Unused Tickets

Government taxes and most airport charges are levied on passengers who fly. If you do not fly, they were never earned and are refundable **even on the strictest non-refundable fare** — but only on request, and often through a specific form rather than the normal refund flow.

On long-haul tickets this can be a meaningful share of the total. Two conditions: cancel the booking rather than no-showing, and ask within the airline's stated window, which is finite. It is worth doing on any unused international ticket.

## Vouchers And Credits

The single largest silent loss in this domain.

- Expiry is commonly measured from the **date of issue**, not from the original travel date, and typically about a year. Read the expiry, not the assumption.
- Many are: single-use (residual value lost), name-locked, unusable for taxes or ancillaries, unusable through agencies, or excluded on sale fares.
- Some can be extended once by asking. Ask before expiry, not after.
- An open ticket (the original ticket held for reissue) is usually more valuable than a voucher: it retains the fare's own rules and its taxes.
- **Every voucher gets a `## Due` row on the day it is issued**, with its expiry date and its value with currency. This is the box that pays for itself.

## Travel Insurance

- Buy for the named causes that actually bankrupt a trip: medical treatment abroad and repatriation, then cancellation for illness or bereavement. Delay and baggage cover are add-ons that a good card already provides.
- Cancellation cover pays for **named reasons** only. "Changed my mind" needs a cancel-for-any-reason product, which is materially more expensive and usually pays a percentage.
- Buy early: cancellation cover only works for events that occur after purchase, and pre-existing conditions must be declared or they void the medical section.
- Annual multi-trip policies beat per-trip cover from roughly the third trip a year, with per-trip day limits to check.
- Claim from the airline first. Insurers deduct anything the airline owed you whether or not you claimed it.

## Card Benefits

Free, conditional, and routinely forgotten.

- Common conditions: the whole fare (or a defined portion) paid with that card, the traveller being the cardholder or a named beneficiary, and a minimum delay length before delay cover triggers.
- Typical coverage shapes: trip delay above a threshold of hours, trip cancellation for named reasons, baggage delay and loss, and rental excess — plus, on some cards, a genuinely useful secondary medical layer.
- **Secondary** coverage pays only what other insurance and the airline did not. **Primary** pays first. Know which, before deciding not to buy a policy.
- Keep the benefits guide, not the marketing page — the conditions are in the guide.
- Record which card carries which benefit, and its annual fee, in `~/Clawic/data/finances/subscriptions.md`; that is where the "is this card worth keeping" question gets answered (`points.md`).

## Chargeback

The tool for **services not delivered**, not for dissatisfaction and not for statutory compensation.

- Use when the airline or agency has ceased trading, has taken payment for something never provided, or has agreed a refund and not paid it after a reasonable period.
- Card-scheme deadlines run from the expected service date and are finite — commonly around 120 days, with longer limits in specific circumstances. Do not sit on it while an airline stalls.
- Some jurisdictions add statutory joint liability for card purchases within a value band, which is stronger than a chargeback and survives longer.
- Debit cards have weaker equivalents; some instant transfer methods have none. This is the practical argument for paying for flights with a credit card (`booking.md`).
- Warn about the side effect: a chargeback against an airline can get the frequent-flyer account suspended and the ticket cancelled if it is still live. Use it after the ticket is dead, not during a negotiation.

## When The Airline Fails

Airlines stop flying with little notice, and the sequence is:

1. Do not buy a replacement through the failing carrier's own channels or credits.
2. Chargeback or the equivalent statutory card protection is the primary route for the fare.
3. Package and tour protection schemes cover flights sold as part of a package; a flight bought on its own is usually outside them, which is exactly why the card route matters.
4. Scheduled-airline-failure cover exists as an insurance add-on and is one of the few add-ons worth buying for a long-haul ticket on a thin carrier.
5. Other airlines sometimes offer rescue fares to stranded passengers. They are a commercial gesture and priced accordingly.

## Recording It

**Every refund route opened becomes a row in `## Claims` in `memory.md`** — date, flight, what happened, basis (fare rule, statutory, insurance, card, chargeback), amount with currency, reference, status, deadline — and **every deadline it creates becomes a `## Due` row**: the card-scheme window, the insurer's notification period, the voucher expiry. When the money lands, update the status and the amount actually received; when a voucher is used, delete its `## Due` row. An unclosed claim row is the only reminder that will exist six months from now.
