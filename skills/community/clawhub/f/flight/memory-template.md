# Working File Templates — Flight

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — table keys and preference areas alike | `~/Clawic/data/flight/config.yaml` | Key by key, read-modify-write |
| Travellers, watched routes, loyalty, open claims, how they fly, due dates, box index | `~/Clawic/data/flight/memory.md` | Rewritten in place; stays small |
| Tickets and reservations, current and future | `~/Clawic/data/bookings/<year>.md` (**shared**) | One row per booking, every travel type in one file |
| Flights actually flown | `~/Clawic/data/flight/flown/<year>.md` | Append-only, cut by year, from the first flight |
| People flown with, and who they are | `~/Clawic/data/contacts/contacts.md` (**shared**) — name only as pointer from `## Travellers` | One row per person |
| Airline card annual fees and travel credits | `~/Clawic/data/finances/subscriptions.md` (**shared**) | One row per card, with its currency |
| Itinerary summary for a trip run as a project or a larger plan | `~/Clawic/data/projects/<trip>.md` (**shared**) — summary only; fares, locators, seats and claims stay here | One file per project, updated in place, never deleted |
| Things you produced that get re-read — an entry procedure for a country they keep visiting, an award routing that worked, a claim letter that got paid, an itinerary brief, a seat-map note for an aircraft they fly often | `~/Clawic/data/flight/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| **Anything durable this table does not name** | `~/Clawic/data/flight/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Passport numbers, barcodes, PINs, card numbers, any credential | Nowhere under `~/Clawic/data/` | Pointer only, or not at all — see Secrets |

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A ticket was issued, changed, cancelled or refunded | Its row in `~/Clawic/data/bookings/<year>.md`, plus every deadline it creates in `## Due` |
| A flight was flown | A line in `flown/<year>.md`, and the booking row moves out of `bookings/` |
| A price was seen for a route being watched, or a new route came up twice | `## Routes` |
| A points balance, tier, requalification figure or expiry date was seen | `## Loyalty`, and the expiry in `## Due` |
| A passport, visa, ETA or trusted-traveller membership expiry was learned | `## Travellers`, and the renewal date in `## Due` |
| A disruption happened that may be compensable, or a bag went missing | `## Claims`, with its deadline in `## Due` |
| A claim was paid, refused, or a voucher was issued | `## Claims` status, and the voucher expiry in `## Due` |
| Someone new travelled with them | Their name in `~/Clawic/data/contacts/contacts.md`, their travel constraints in `## Travellers` |
| An airline card was opened, closed, or its fee or credit changed | `~/Clawic/data/finances/subscriptions.md` |
| A trip is being run as a project or a larger plan, or its dates or flights changed | Its itinerary summary in `~/Clawic/data/projects/<trip>.md`, flight detail referenced by name |
| A procedure, routing or letter came out of the session that would be re-derived otherwise | `artifacts/` |
| The user declared a preference | Its key in `config.yaml` |
| A recurring check was scheduled or run | `## Due` |

## Start flat, split only when it hurts

Everything except flown logs, artifacts and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. You, the agent about to write, run this — not a later cleanup pass. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/flight/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite. `## Travellers` → `travellers.md`, `## Routes` → `routes.md`, `## Loyalty` → `loyalty.md`, `## Claims` → `claims.md`.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts and the flown log are the exception: they are born as their own file whatever their size, because they are read whole and only when their subject comes up.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`keychain:ba-executive-club` · `1password:Travel/Iberia` · `bitwarden:Travel/AAdvantage` · `env:DUFFEL_API_KEY` · `env:AMADEUS_CLIENT_SECRET` · `file:~/Documents/passport-scan.pdf`

When the user pastes an itinerary, a confirmation email or a screenshot to be saved, strip the secret values before writing and leave the pointer visible: `programme login: <keychain:ba-executive-club>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: airport and airline IATA codes, flight numbers, dates and times, cabin and fare basis codes, record locators, ticket numbers, seat numbers, aircraft types, frequent-flyer numbers and tiers, points balances, prices with their currency, passport *nationality* and *expiry date*, visa and ETA *validity dates*, baggage report references, claim reference numbers.

**Secrets, strip them**: passport, national ID and visa document numbers; boarding-pass barcodes, QR codes and boarding-pass images (the barcode decodes to the record and the passenger record); loyalty programme passwords and PINs; airline and OTA account credentials; payment card numbers, expiry and CVV; the bank details given for a compensation payout; API keys and client secrets from `apis.md`; Known Traveler, Global Entry and Redress numbers — record that the membership exists and when it expires, never the digits. Full dates of birth are not stored either: where an age band matters, store the band and the month it changes ("infant, turns 2 in 2026-11").

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared bookings box](#shared-bookings-box) · [flown/](#flown) · [artifacts/](#artifacts) · [shared contacts pointer](#shared-contacts-pointer) · [shared finances pointer](#shared-finances-pointer) · [shared projects pointer](#shared-projects-pointer) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/flight/` if it does not exist.

```yaml
home_airports: [MAD, BCN]
passport_country: [ES]
cabin: economy
currency: EUR
max_stops: 1
connection_buffer_min: 45
carry_on_only: false
separate_tickets_ok: false
booking_channel: direct
loyalty_focus: oneworld

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
comfort:
  earliest_departure: "07:00"
  red_eye: avoid
  seat: aisle
restrictions:
  no_basic_economy: true
  meals: vegetarian
presentation:
  options_shown: 3
  lead_with: total-cost
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Flight Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Flights flown (2026, 14) → `flown/2026.md`; read before any status, requalification or points-earning question
- Japan entry procedure (1 page) → `artifacts/entry-japan.md`; read whenever a trip to Japan is on the table
- Claim letter that got paid (IB, EU261; 1 page) → `artifacts/claim-letter-eu261.md`; read when drafting any new compensation claim
- Tickets and reservations (2026, 2 rows) → `~/Clawic/data/bookings/2026.md` (shared); read before anything about an existing trip
- Tokyo trip, Sep 2026 (1 project file) → `~/Clawic/data/projects/tokyo-2026-09.md` (shared); read when that trip's dates, scope or budget come up

## Due
| What | Every | Last run | Next due |
|---|---|---|---|
| Passport validity check against booked trips | 6 months | 2026-06-01 | 2026-12-01 |
| Points audit (balances, expiry, orphan amounts) | quarter | 2026-07-01 | 2026-10-01 |
| Tier requalification check | month | 2026-07-20 | 2026-08-20 |
| MAD-JFK price check | week | 2026-07-22 | 2026-07-29 |
| Voucher IB 180 EUR expires | once | — | 2026-11-04 |
| EU261 claim FR1234 time-barred | once | — | 2031-03-02 |

## Travellers
| Name | Relation | Passport | Passport expires | Held | Constraints |
|---|---|---|---|---|---|
| (user) | self | ES | 2029-04-11 | ESTA to 2027-05, Global Entry (expiry 2028-02) | — |
| Marta | partner (see contacts) | ES | 2027-01-30 | ESTA to 2027-05 | aisle, no red-eye |
| Leo | child, turns 2 in 2026-11 | ES | 2030-08-02 | — | bassinet while under weight limit |

## Routes
| Route | Why | Target | Best seen | Typical range | Alert |
|---|---|---|---|---|---|
| MAD-JFK | annual, flexible ±5 days | 420 EUR | 388 EUR (2026-02-11) | 430-700 EUR | Google Flights, ±3 days |
| BCN-LHR | work, fixed dates | 120 EUR | 89 EUR (2026-05-03) | 110-260 EUR | — |

## Loyalty
| Programme | Number | Tier | Tier expires | Progress | Balance | As of | Points expire |
|---|---|---|---|---|---|---|---|
| Iberia Plus | IB1234567 | Plata | 2027-03-31 | 4 of 8 tier segments | 46,300 Avios | 2026-07-20 | no expiry with activity |
| Flying Blue | FB9876543 | Explorer | — | — | 12,100 miles | 2026-07-20 | 2027-01-14 |

## Claims
| Opened | Flight | What happened | Basis | Claimed | Reference | Status | Deadline |
|---|---|---|---|---|---|---|---|
| 2026-03-04 | IB6253 2026-03-02 | Arrived 4h20 late | EU261, 600 EUR band | 600 EUR | CLM-88213 | airline refused, NEB filed | 2031-03-02 |
| 2026-05-19 | BA506 2026-05-18 | Bag delivered 3 days late | Montreal, receipts 214 EUR | 214 EUR | PIR MADBA12345 | paid 2026-06-30 | closed |

## How They Fly
Books late and regrets it. Will not connect through LHR after the 2026 missed connection. Cares about arrival time more than price on work trips, the reverse on holidays.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. Every deadline in the SKILL.md "Deadlines That Expire Value" table that applies to this user belongs here, plus every recurring check they asked for. One-off deadlines use `once` in the `Every` column and are deleted once the thing they guarded has passed.
- **`## Travellers`**: nationality and expiry date only, never document numbers. A companion who is a real person also gets a row in the shared contacts box, and is referenced here by name; their travel constraints stay here, because they are flight-specific.
- **`## Routes`**: `Target` and `Best seen` always carry their currency and, for `Best seen`, the date it was seen — a price with no date is not a comparison. Re-checking a route **overwrites** its row; never a second row for the same route. Delete the row once the trip is booked or abandoned.
- **`## Loyalty`**: `Balance` carries its `As of` date. Programme numbers are working identifiers and stay; PINs and passwords never appear.
- **`## Claims`**: a claim stays here until it is paid, refused and dropped, or time-barred. `Deadline` is the date the claim expires under the applicable law, not the airline's internal target. Closed claims older than a year are deleted after their outcome is reflected in `flown/<year>.md`.
- These headings are exactly the ones the split-out files inherit, so each split stays a copy-paste.

| Status | Meaning |
|---|---|
| `ongoing` | Still learning how they travel |
| `complete` | Know their routes, programmes, documents and tolerances |

## Shared bookings box

Lives at `~/Clawic/data/bookings/<year>.md` and is shared with every other travel skill — hotels, trains, car hire and packages land in the same file, and the user may not have any of those skills installed, so the format travels with this one.

```markdown
# Bookings — 2026

| Locator | Type | Provider | What | Start | End | Passengers | Paid | Status | Changeable until |
|---|---|---|---|---|---|---|---|---|---|
| ABC123 | flight | Iberia | MAD-JFK-MAD, economy, 1 checked bag | 2026-09-14 | 2026-09-28 | 2 | 812 EUR | ticketed | fee 90 EUR + fare diff |
| XY9K2L | flight | Ryanair | BCN-STN one way, cabin bag only | 2026-10-02 | 2026-10-02 | 1 | 41 EUR | ticketed | non-changeable |
```

- **Identity is the record locator.** Read the file and search for the locator before adding anything. If it is already there, update that row in place — it is yours. Never modify or delete a row whose `Type` is not `flight`: hotel and car rows belong to other skills.
- **Two tickets are two rows**, one locator each, with the pairing noted in `What` ("self-transfer, paired with XY9K2L"). Recording them as one booking is how the connection risk disappears from the record.
- **Retirement is part of the inventory.** When a flight has been flown, move it to `flown/<year>.md` and delete the row. When it is cancelled or refunded, delete the row and record the outcome in `## Claims` if money is outstanding. A bookings file that only grows stops being an answer to "what have I got booked".
- **Amounts carry their currency in the value** (`812 EUR`), because rows from other providers and other skills sit next to yours and someone will add the column up. Award tickets record both: `55,000 Avios + 180 EUR`.
- **Year file by departure date.** A trip that crosses New Year lives in the file of its first departure.
- **Foreign columns win.** If `bookings/<year>.md` already exists with a different column set, match its columns and add anything missing as a trailing note. Never rewrite its header.
- Locators are working identifiers and stay. Boarding-pass barcodes and images never go in this file.

## flown/

`~/Clawic/data/flight/flown/<year>.md`, append-only, created with the first flight recorded. This is what makes status questions, requalification maths and "have we flown this route before" answerable without asking.

```markdown
# Flights Flown — 2026

| Date | Flight | Route | Cabin | Fare class | Distance | Credited to | Points earned | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-03-02 | IB6253 | MAD-JFK | economy | N | 3,590 mi | Iberia Plus | 1,240 Avios | 4h20 late, claim CLM-88213 |
| 2026-05-18 | BA506 | LHR-MAD | economy | O | 785 mi | Iberia Plus | 310 Avios | bag delayed 3 days |
```

Fare class is recorded because earning and upgrade eligibility depend on it, not on the cabin, and it is unrecoverable once the boarding pass is gone.

## artifacts/

One file per thing, at `~/Clawic/data/flight/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **an entry-and-transit procedure for a country they keep visiting**, **an award routing that worked** (programme, partner, chart band, where the space appeared), **a claim letter that got paid**, **an itinerary brief for a complex trip**, **a seat-map note for an aircraft they fly often**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Entry procedure — Japan (ES passport)
*Read whenever a trip to Japan is on the table. Written 2026-07-26; entry rules change, re-verify before booking.*

Visa: not required for ES up to 90 days · Pre-arrival: Visit Japan Web, QR per traveller
Transit: airside transit at HND/NRT does not enter immigration
Onward ticket: asked for on arrival, not at check-in
```

```markdown
# Award routing that worked — MAD to Tokyo in business
*Read before any long-haul award search in this direction. 2026-07-26.*

Programme: ... · Partner metal: ... · Points + cash paid: 90,000 + 240 EUR
Where the space appeared: T-330 days at schedule load, and again inside T-14
Rejected: the direct programme's own chart — dynamic pricing, 3.4× the points
```

If the trip is being tracked as a project or a larger plan, the itinerary summary also belongs in the shared `~/Clawic/data/projects/<trip>.md` — summary only, with fares, locators, seats and claims staying here and referenced by name (protocol below, [shared projects pointer](#shared-projects-pointer)).

## Shared contacts pointer

People are not stored twice. A companion, a colleague or a client whose flights are being booked goes in `~/Clawic/data/contacts/contacts.md` — identity is their email or handle — as `name | role | preferred channel | context`. Read the file and search for that identity before adding; if the person is there, update the row in place and never touch rows written by other skills. Scale cut: a table while there are 15 people or fewer, then one `~/Clawic/data/contacts/<name>.md` per person with the same fields, `contacts.md` left as the index — and if the folder already looks like that on arrival, follow it rather than starting a parallel table. If the file exists with a different column set, match its columns and never rewrite its header. Delete only rows this skill added, and only when the person is genuinely gone.

Only their **name** appears in `## Travellers`, alongside the flight-specific facts (nationality, document expiry, seat and meal constraints) that no other skill needs. Duplicating the person is the fastest way for two skills to contradict each other.

## Shared finances pointer

Airline and travel credit cards are recurring costs, so they belong with the rest of them: `~/Clawic/data/finances/subscriptions.md`, one row per card, identity is the card name. Record `name | provider | annual fee with currency | renews | benefits that expire`. Read before adding, update in place, delete the row when the card is closed, and never rewrite a header written by another skill. What stays in `## Loyalty` here is the programme and its balance; what goes there is the money — the annual fee, the renewal date, and any travel credit that expires unused. Card numbers never appear in either place.

## Shared projects pointer

A trip that is being run as a project — a relocation, a multi-city work tour, a wedding, a conference season — has its home outside this skill, at `~/Clawic/data/projects/<trip>.md`, one file per project, shared with every planning and work skill. Only the **itinerary summary** goes there: origin and destination, dates, who is travelling, and one line per flight (`2026-09-14 IB6253 MAD-JFK, ABC123`). Fares, fare rules, seat maps, points and claims stay in this skill's boxes and are referenced by name.

- **Identity is the project name, and the file slug *is* that name** in kebab-case: `tokyo-2026-09.md`, `berlin-relocation.md`. List `~/Clawic/data/projects/` and look for that file before writing anything.
- **The file exists → update it in place.** Write only the itinerary lines under an `## Itinerary` heading and leave every other section byte for byte. A second file for the same trip is how two skills end up holding two different departure dates.
- **Foreign structure wins.** If the file already uses different headings or a different table shape, match what is there and add anything missing as a trailing note. Never rewrite its headings, and never delete a section another skill wrote.
- **Retirement is a status line, never a deletion.** When the trip is over or called off, write `status: done — <date>` or `status: cancelled — <date>` inside the file. The file is the record of what happened and stays.
- **Scale cut: at roughly 20 closed projects**, move the closed ones to `~/Clawic/data/projects/archive/<project>.md` without renaming them. Open projects stay in the folder root.
- Amounts carry their currency inside the value (`812 EUR`), dates are ISO. Record locators are working identifiers and are fine here; passport numbers, barcodes and credentials are not — the Secrets rule covers this folder too.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact headings it had inside `memory.md`.

`travellers.md` — `## Travellers`, one row per person, for households and anyone who books for others.
`routes.md` — `## Routes`, the price history that makes "is this a good price" answerable. This is the file that stops the same route being researched from zero every year.
`loyalty.md` — `## Loyalty`, moved across unchanged; once it lives on its own, a `## Programme Rules` heading may be added for the per-programme details worth not re-deriving: expiry policy, retro-claim window, household pooling, transfer partners the user actually holds.
`claims.md` — `## Claims`, with closed claims kept for one year as precedent — the same airline, the same argument, the second time.
