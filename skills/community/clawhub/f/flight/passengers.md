# Who Is Travelling — Infants, Minors, Pets, Assistance, Groups

Scope: everything that must be arranged at booking because it cannot be arranged at the airport. Most of this domain's outright refusals happen here, and all of them were avoidable at purchase.

**Before booking for anyone but the user**, read `## Travellers` in `~/Clawic/data/flight/memory.md` for their documents and constraints, and `~/Clawic/data/contacts/contacts.md` for who they are.

**Contents:** [The Notice Windows](#the-notice-windows) · [Infants Under Two](#infants-under-two) · [Children](#children) · [Unaccompanied Minors](#unaccompanied-minors) · [Pets](#pets) · [Reduced Mobility And Assistance](#reduced-mobility-and-assistance) · [Medical Conditions](#medical-conditions) · [Pregnancy](#pregnancy) · [Groups](#groups) · [Meals](#meals)

## The Notice Windows

| Request | When it must be made | What happens if late |
|---|---|---|
| Special assistance (wheelchair, guide, boarding help) | At booking; **48 hours minimum** is the regulated floor in the EU and similar elsewhere | Assistance may be provided at the airport's discretion, or not |
| Medical oxygen, stretcher, medical clearance | Weeks — needs the airline's medical desk and a doctor's form | Refused at check-in |
| Pet in cabin or hold | At booking — capacity is capped per flight and per aircraft | Sold out, not a fee |
| Unaccompanied minor | At booking, with the service purchased | Cannot be added later on many carriers |
| Bassinet | At booking, reconfirm at T-48h | Allocated to whoever asked first |
| Special meal | Usually up to 24-48 hours before departure | The standard meal, or nothing |
| Sports and outsize equipment | At booking — capacity capped per flight | Refused at the desk (`baggage.md`) |

Every one of these that applies gets a `## Due` row for its reconfirmation date, because the request being in the system at booking and the request being honoured on the day are different things.

## Infants Under Two

- **Lap infant**: under two on the date of *each* flight. Typically free or a nominal amount domestically and a percentage of the adult fare plus taxes internationally. The infant has no seat and no baggage allowance beyond a small one, and usually gets a pushchair carried free.
- **Turning two mid-trip** means a full seat on the return. This is the single most common infant booking error — check the birthday against both flight dates.
- **Own seat**: buy a child fare and use an approved restraint. Safer, and the only option once they turn two. The restraint must be approved for aircraft use, which is not the same as approved for cars in every country.
- **Bassinets** are bulkhead-only, limited in number, and have weight and length limits — a large baby will be refused one even if it is booked (`seats.md`).
- Only one lap infant per adult, and rows with a single oxygen mask spare cannot take two infants — this constrains the seat map more than people expect.
- Pushchairs and car seats are usually carried free and gate-checked; confirm whether they are returned at the gate or the carousel.

## Children

- Child fares are often a small discount or none at all, and sometimes more expensive than a discounted adult fare — check both.
- Several regulators require or press carriers to seat young children beside an accompanying adult without a fee, and several carriers do so as policy. Verify the specific carrier's stated policy and use it; do not assume, and do not pay if it applies (`seats.md`).
- Book everyone on one reservation so a disruption moves the whole family together (`disruptions.md`).
- Children still need their own documents and authorisations, and sometimes a consent letter (`documents.md`).

## Unaccompanied Minors

- Age bands vary by carrier: the service is typically mandatory for a lower band, optional for a middle band, and unavailable below a minimum age. The fee is per direction and is charged on top of an adult-priced fare in most cases.
- Many carriers refuse unaccompanied minors on connections entirely, or on the last flight of the day, or on codeshares and interline itineraries — this rules out most cheap routings.
- The form names the adults dropping off and collecting, with their identification; the collecting adult must be there and must match.
- Non-stop, mid-day, on one carrier, with a buffer before the last flight of the day. That is the shape of a booking that works.

## Pets

The highest-refusal category in the domain, and almost entirely a matter of preparation.

- **In cabin** (small animal in a carrier under the seat): limited slots per flight, size and weight limits including the carrier, and forbidden by some carriers and on some routes.
- **In the hold** as checked or manifest cargo: temperature embargoes in summer and winter, breed restrictions (short-nosed breeds are refused by many carriers after fatalities), and crate specifications that are enforced to the centimetre.
- **Destination rules dominate**: microchip, rabies vaccination with a waiting period, antibody titre tests with multi-month lead times for rabies-free destinations, health certificates issued inside a narrow window before travel, and quarantine in the strictest cases.
- Some countries only accept animals as cargo, not as accompanied baggage, regardless of the airline's policy.
- Assistance animals are a separate legal category with their own documentation, and the rules diverged sharply between jurisdictions after emotional-support animals were removed from several.
- Start with the destination's import rules, then find the airlines that fit them. Doing it the other way round wastes the booking.

## Reduced Mobility And Assistance

- Assistance is a legal right on most major aviation markets and is free: help through the terminal, boarding, on-board transfer, and carriage of mobility equipment beyond the baggage allowance.
- Request at booking and confirm at 48 hours. The airport, not the airline, usually provides it, and the airline is the channel.
- Powered wheelchairs need the battery type declared; some battery types are refused, and dimensions matter for the hold door of small aircraft.
- Damage to a mobility device is treated more seriously than baggage damage in several jurisdictions — report before leaving the airport (`baggage.md`).
- Seat restrictions: exit rows are unavailable, and some carriers require a companion for passengers who cannot self-evacuate.

## Medical Conditions

- Medical clearance forms exist for recent surgery, recent cardiac events, unstable conditions, and anything requiring on-board oxygen or medical equipment. Lead time is weeks.
- Fitness-to-fly recency: airlines commonly require a doctor's assessment dated within a short window before departure.
- Medication in the cabin, in original packaging, with a prescription or letter; check the destination's controlled-substances list, because common prescriptions are illegal in some countries (`documents.md`).
- Cabin pressure and dehydration matter for some conditions; recent scuba diving has a documented no-fly interval.
- Allergies: airlines will not guarantee an allergen-free cabin. Some make a buffer-zone announcement on request, and pre-boarding to wipe down a seat is usually permitted if asked at the gate.

## Pregnancy

Carrier policies cluster around a cut-off in the late 30s of weeks for single pregnancies and earlier for multiples, with a medical letter required from a point before that — typically around 28 weeks. The letter states the due date and fitness to fly and must be recent. Policies differ enough between carriers that the cut-off must be read on the specific airline, and the return date is what governs.

## Groups

- Ten or more passengers is usually a group booking with its own desk: a deposit, a deadline to name passengers (often around a month out), and some name-change flexibility that individual tickets do not have.
- Group fares are frequently **above** the lowest published fare — the benefit is flexibility and guaranteed seats together, not price. Price both.
- For a group under ten, booking as several small reservations often prices better, because a single booking must find all seats in one fare bucket (`fares.md`). Never split anyone travelling with a child.
- Note the pairing between reservations in `~/Clawic/data/bookings/<year>.md` so a disruption does not surprise anyone.

## Meals

Special meals are ordered per passenger, per segment, and are silently dropped by a reissue or a change of aircraft. Reconfirm after any change. Codeshares often do not carry the request across to the operating carrier — re-enter it with them.

**When a new person travels**, add them to `~/Clawic/data/contacts/contacts.md` (identity is their email or handle; read before adding, update in place, never touch another skill's rows) and put their **name only** in `## Travellers` alongside the flight-specific facts: nationality, document expiry, assistance needs, meal, seat constraints, and the age band with the month it changes. The person belongs to the shared box; their flying constraints belong here.
