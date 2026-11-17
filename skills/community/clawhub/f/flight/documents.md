# Passports, Visas, and Being Allowed To Board

Scope: the constraint that voids the whole purchase, which is why it is checked before prices (Rule 5). Everything here depends on **the passport held**, not on where the traveller lives.

**Before answering**, read `## Travellers` in `~/Clawic/data/flight/memory.md` — or `travellers.md` if the `## Boxes` index points there — for each traveller's nationality and document expiry, and `config.yaml` for `passport_country`. If nationality is unknown, say that entry rules depend on it and ask once; every answer given without it is a guess.

**Entry rules change with no notice and are enforced by the airline at check-in.** Everything below is the shape of the problem and the questions to ask; the current answer comes from the destination's own official source and the airline's document checker, on the day.

**Contents:** [The Airline Is The Enforcer](#the-airline-is-the-enforcer) · [Passport Validity](#passport-validity) · [Visas And Pre-Travel Authorisations](#visas-and-pre-travel-authorisations) · [Transit](#transit) · [Onward And Proof Of Funds](#onward-and-proof-of-funds) · [Dual Nationality](#dual-nationality) · [Children And Consent](#children-and-consent) · [Health Documents](#health-documents) · [Practical Habits](#practical-habits)

## The Airline Is The Enforcer

Immigration decides at the border, but the airline decides at the gate, because carriers are fined for bringing inadmissible passengers and must repatriate them. Consequences:

- Check-in staff apply a conservative reading of a rule database, and being right about the law at the desk does not get you on the aircraft.
- Denied boarding for missing documents is **not compensable** — it is the passenger's obligation (`disruptions.md`).
- The airline's own online document checker is the practical test to pass, and it is free to run before booking.
- The check happens again at the boarding gate on many routes, and sometimes at a transit point.

## Passport Validity

Three separate rules, and travellers meet the wrong one:

1. **Six months beyond arrival** — the most widely applied rule, across much of Asia, the Middle East, Africa and Latin America. Measured from the date of *entry*, and some states measure from the date of *departure* from their territory.
2. **Three months beyond intended departure** — the Schengen area, plus a second condition that catches people: the passport must have been **issued within the previous ten years**. A passport with extra months added at renewal can be simultaneously valid and unacceptable.
3. **Valid for the duration of the stay** — the most permissive, used by a minority, including some near-neighbour arrangements.

Also required in practice: at least one or two blank pages for stamping, and a passport that is not damaged — water damage and a detached lamination are refusals.

Renewal lead times run from days to months depending on the country and the season. Diary the renewal against the applicable rule and the lead time, not against the expiry date: put it in `## Due` with the date the passport becomes unusable for the trips already booked.

## Visas And Pre-Travel Authorisations

| Type | What it is | Lead time to assume |
|---|---|---|
| Visa-free entry | Nothing to obtain, a stay limit and conditions still apply | — |
| Electronic travel authorisation | An online pre-clearance tied to the passport, valid for multiple entries over a period | Days, but apply weeks ahead; approval is not instant for everyone |
| E-visa | An online visa with a document to carry | Days to weeks |
| Visa on arrival | Obtained at the border, with fee, photo and queue | Confirm it exists for that nationality and that entry point |
| Consular visa | Appointment, biometrics, documents, waiting | Weeks to months — book the appointment before the flight |

Rules to state every time:

- Pre-travel authorisations are tied to the passport, so a renewed passport usually invalidates one and it must be re-obtained.
- **Only ever use the official government site.** Look-alike sites charge multiples of the real fee for the same form and are the most common travel scam in the domain. Never recommend a third-party portal.
- Stay limits are usually counted as days within a rolling window rather than per entry, and overstaying by even a day produces re-entry bans.
- Entry systems are being introduced and postponed continually in Europe and elsewhere — biometric entry-exit registration and new authorisation schemes have had repeatedly moving start dates. Check whether the scheme is actually in force for the travel date before telling anyone they need it, and before telling them they do not.

## Transit

The category that produces the most surprises, because a ticket can be sold that cannot legally be flown.

- **Airside transit without entering the country** is fine for most nationalities at most hubs — but a number of countries require a transit visa for airside transit for specific nationalities. This is a per-nationality, per-airport question with a real answer.
- **Any connection that requires entering the country** — bag reclaim, terminal change through immigration, most US and Canadian connections — needs the full entry requirement of that country, including its authorisation scheme (`connections.md`).
- **Separate tickets** almost always mean entering the country, because the bag must be collected.
- Overnight connections where the airside area closes force entry, and therefore a visa.
- Some countries' transit rules changed recently in both directions; verify rather than recalling.

## Onward And Proof Of Funds

- **Onward or return ticket** requirements are enforced by airlines at check-in in Southeast Asia, parts of Latin America and elsewhere. A one-way traveller must be able to show something.
- Legitimate answers: a genuine refundable ticket, a cheap real bus or train reservation, or an actual onward flight. A cancelled or forged reservation fails a live check and is a documents offence (`fares.md`).
- **Proof of funds and accommodation** is asked for at some borders — a card, a booking confirmation, an address. Rarely enforced, occasionally decisive.
- Some destinations require travel insurance with a minimum medical cover as a condition of entry.

## Dual Nationality

- Some states require their own citizens to enter and leave on their own passport, and the airline's system may need the other passport to satisfy the destination's rules. Both facts can apply on the same trip.
- The name on the ticket must match the passport that will be presented at check-in for that flight. Two passports with different name formats is a recurring cause of a mismatch (`booking.md`).
- Record which passport is used for which destination in `## Travellers` — nationality and expiry only, never document numbers.

## Children And Consent

- Children need their own passport and their own authorisation almost everywhere; some countries require a consent letter when a child travels with one parent or with neither, and a few require it certified.
- Differing surnames between parent and child attract questions. A birth certificate copy resolves them.
- Infant and child age bands are calculated **on the date of each flight**, so a child who turns two mid-trip needs a seat on the return (`passengers.md`).

## Health Documents

- Vaccination certificates are required for entry to some countries, and by some countries when arriving *from* a listed country — the second condition catches people connecting through a hub.
- Where required, the certificate has a validity start delay after vaccination, which is a lead time like any other.
- Medication: carry it in original packaging with a prescription, and check the destination's controlled-substances rules — common prescriptions are banned in some countries (`passengers.md`).

## Practical Habits

- Run the airline's document checker before buying, not after (Rule 5).
- Keep a photograph of the passport data page somewhere reachable without the passport — and never inside `~/Clawic/data/`.
- Register with the home country's consular service for high-risk destinations.
- Re-check requirements roughly a month out and again a week out; the rule that applied at booking is not necessarily the rule at departure.

**Whenever a document fact is learned** — nationality, passport expiry, an authorisation obtained and its validity, a consent letter held — write it into `## Travellers` in `memory.md`, and put every renewal and expiry in `## Due` against the rule that governs it. **When a destination's entry procedure took real work to assemble and the user goes there repeatedly**, save it as `~/Clawic/data/flight/artifacts/entry-<country>.md` with a written-on date and a "re-verify before booking" line, and add its `## Boxes` line in the same turn.
