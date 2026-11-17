---
name: Bangkok
slug: bangkok
version: 1.0.4
description: >-
  Plans Bangkok trips, relocations, and nomad stays: neighborhoods, visas, costs, transport,
  street food, and Thai law. Use when choosing where to stay or live in Bangkok, building an
  itinerary, comparing rents or cost of living, picking a visa (exemption, DTV, retirement, LTR),
  riding BTS/MRT/Grab or driving, handling Thai taxes on foreign income, avoiding scams and
  overstay fines, teaching English, finding tech work, setting up a company, buying a condo,
  choosing schools for kids, or navigating etiquette, festivals, healthcare, nightlife, and
  shopping. Covers day trips from Bangkok; not for beaches, islands, or other Thai bases — use
  the thailand skill for those.
homepage: https://clawic.com/skills/bangkok
changelog: "Full coverage pass: deeper guides, situation-named files, and per-user configuration"
metadata:
  clawdbot:
    emoji: 🏯
    requires:
      bins: []
    os:
    - linux
    - darwin
    - win32
    displayName: Bangkok
    configPaths:
    - ~/Clawic/data/bangkok/
---

User preferences and memory live in `~/Clawic/data/bangkok/` (`config.yaml` for declared preferences — see Configuration; `memory.md` for what the agent observes). If you have data at an old location (`~/bangkok/` or `~/clawic/bangkok/`), move it to `~/Clawic/data/bangkok/`.

## When To Use

- Planning a Bangkok trip: itinerary, lodging, attractions, day trips, festivals
- Choosing a neighborhood or relocating: rent, contracts, schools, settling in
- Working remotely from Bangkok: visa strategy, coworking, legality, taxes
- Estimating cost of living or comparing against another base
- Teaching, tech jobs, company setup, retiring, or buying property in Bangkok
- Not for beaches/islands/Chiang Mai specifics — only day trips from Bangkok are covered here

## Quick Reference

| Topic | File |
|-------|------|
| **Visitors** | |
| Attractions (must-see vs skip) | `visitor-attractions.md` |
| Itineraries (1/3/7 days) | `visitor-itineraries.md` |
| Where to stay | `visitor-lodging.md` |
| Tips & day trips | `visitor-tips.md` |
| **Neighborhoods** | |
| Quick comparison | `neighborhoods-index.md` |
| Sukhumvit (Asok, Thonglor, Ekkamai) | `neighborhoods-sukhumvit.md` |
| Silom, Sathorn, Riverside | `neighborhoods-silom.md` |
| Ratchathewi, Ari, Phaya Thai | `neighborhoods-ari.md` |
| Old Town, Chinatown, Rattanakosin | `neighborhoods-oldtown.md` |
| Choosing guide | `neighborhoods-choosing.md` |
| **Food** | |
| Overview & street food culture | `food-overview.md` |
| Street food guide | `food-street.md` |
| Thai cuisine essentials | `food-thai.md` |
| International & fine dining | `food-international.md` |
| Best areas for dining | `food-areas.md` |
| Dietary & practical | `food-practical.md` |
| **Practical** | |
| Moving & settling | `resident.md` |
| Transport (BTS, MRT, taxis, Grab) | `transport.md` |
| Driving, licenses, buying vehicles | `driving.md` |
| Cost of living | `cost.md` |
| Thai taxes (180-day rule, remittance) | `taxes.md` |
| Safety & scams | `safety.md` |
| Weather & seasons | `climate.md` |
| Local services (banking, SIM) | `local.md` |
| Shopping, malls, tailors, VAT refund | `shopping.md` |
| **Career & Life Stages** | |
| Digital nomad guide | `nomad.md` |
| Teaching English | `teaching.md` |
| Tech industry & startups | `tech.md` |
| Business setup | `business.md` |
| Retiring in Bangkok | `retirement.md` |
| Buying property (condo quota, FET) | `property.md` |
| Visas (exemption, DTV, retirement, LTR) | `visas.md` |
| **Lifestyle** | |
| Culture & customs | `culture.md` |
| Festivals & annual calendar (Songkran) | `festivals.md` |
| Kids, schools & family life | `families.md` |
| Healthcare & hospitals | `healthcare.md` |
| Nightlife & entertainment | `nightlife.md` |
| Expat lifestyle & social | `lifestyle.md` |
| Thai language basics | `language.md` |
| **Anything else** | Ask role + timeline first (Rule 1), then route to nearest file; short visit defaults to `visitor-tips.md`, staying defaults to `resident.md` |

## Core Rules

### 1. Identify User Context First
The same question has opposite answers by role. "Where should I stay?" for a 4-day tourist = hotel near a BTS interchange (`visitor-lodging.md`); for a 6-month nomad = condo contract in On Nut or Ari (`neighborhoods-choosing.md`).
- **Role**: tourist, digital nomad, teacher, retiree (`retirement.md`), family with kids (`families.md`), entrepreneur
- **Timeline**: days, months, or relocation
- If either is unknown, check `config.yaml` first (Configuration), then ask — don't average the answers.

### 2. Visa Reality
Thailand rewrites visa rules several times a year. Ranges below held as of early 2026 — always verify before the user commits money:
- **Visa exemption**: 60 days for 93 nationalities (air and land, since Jul 2024) + 30-day extension at immigration (฿1,900). Government has floated reverting to 30 days — check current status.
- **DTV (Destination Thailand Visa)**: since Jul 2024 the default nomad answer — 5-year multi-entry, 180 days per entry (+180 extension), ฿10,000 fee, proof of ฿500,000 funds. Covers remote workers with foreign employers/clients; it is not a Thai work permit.
- **ED visa**: study Thai or Muay Thai; renewable, but under crackdown — schools with real attendance only.
- **Retirement (Non-O)**: 50+, ฿800,000 seasoned in a Thai bank OR ฿65,000/month income.
- **Thailand Privilege** (rebranded from "Elite" in 2023): from ~฿900,000 for 5 years; tiers up to 15-20 years.
- **LTR**: 10-year for remote workers around $80K/year income — criteria relaxed in 2025, verify current thresholds.
- Heuristic: if the user plans >90 days/year in Thailand on exempt entries, immigration will eventually flag them — route to a real visa in `visas.md`.

### 3. Tax Residency (the 2024 change)
Compliance framing: everything below exists so the user meets Thai obligations and is not caught out by them. Thresholds and rules change; for a filing, a visa application, or anything with legal consequence, confirm with Thai immigration, the Revenue Department, or a licensed professional.
- **≥180 days in Thailand in a calendar year = Thai tax resident** — automatic, on any visa, including chained tourist entries.
- Since 1 Jan 2024, foreign income remitted by a resident is assessable whenever remitted (pre-2024 savings grandfathered). The DTV gives zero tax shelter; LTR is the exemption route.
- Trigger: any plan crossing ~6 months/year → raise the 180-day rule once and route to `taxes.md`. The user who learns this at filing time learns it as back taxes.

### 4. Cultural Context
- **Royal family**: never criticize — this carries severe prison time, including for social-media shares and likes (-> Legal Awareness).
- **Temples**: shoes off, shoulders and knees covered; women never touch monks or hand them objects directly.
- **Head & feet**: head sacred, feet lowest — never point feet at Buddha images or people.
- **Wai**: return a wai when given; don't initiate to children or service staff (it embarrasses them).
- **Face**: raising your voice loses the argument. Calm + smile gets problems fixed; anger gets stonewalled.
See `culture.md`.

### 5. Weather Reality
- **Hot season (Mar-May)**: 35-40°C, heat index can pass 45°C in April — schedule temples 7:30-10 AM only.
- **Rainy season (Jun-Oct)**: afternoon downpours, heaviest Sep-Oct; rain means BTS, not Grab (surge pricing + gridlock).
- **Cool season (Nov-Feb)**: 25-32°C, peak tourist season and peak prices.
- **Burning/pollution season (Dec-Mar, worst Jan-Feb)**: PM2.5 spikes, AQI 150+ days — N95 masks, check AQI before outdoor plans.
See `climate.md` for monthly breakdown.

### 6. Current Data (early 2026 — ranges drift, direction holds)

| Item | Range |
|------|-------|
| 1BR condo (Sukhumvit) | ฿15,000-35,000/month (~$425-1,000) |
| 1BR condo (Silom) | ฿25,000-50,000/month (~$715-1,430) |
| Coworking (monthly) | ฿1,200-8,000/month (~$35-230) |
| Street food meal | ฿40-80 (~$1.15-2.30) |
| Mid-range restaurant | ฿200-500/person (~$6-14) |
| BTS/MRT single ride | ฿17-62 (~$0.50-1.80) |
| Private hospital visit | ฿1,000-3,000 (~$29-85) |

Rough conversion used across all files: 35 THB ≈ $1. Quote ranges, never a single "the price is" number.

### 7. Cost Reality
Build budgets bottom-up from components, not from a single headline number:
- rent ฿15,000-35,000 + food ฿8,000-15,000 + transport ฿2,000-4,000 + utilities/SIM/internet ฿3,000-5,000 = **฿28,000-59,000/month (~$800-1,700) for a comfortable single**.
- Worked example (budget nomad, On Nut): rent 15k + food 9k + transport 2.5k + utilities 3.5k ≈ ฿30,000 (~$860/month).
- Western-format life (imported groceries, wine, Thonglor rents) doubles the food and housing lines — warn users who anchor on "Bangkok is cheap".
- Healthcare: world-class private hospitals at roughly 20-30% of US prices (`healthcare.md`).

### 8. Transit Reality
Rail network (2026): BTS Sukhumvit + Silom + Gold lines, MRT Blue + Purple, Yellow and Pink monorails (opened 2023), SRT Red lines, Airport Rail Link. Decision rules:
- If a rail route exists, take it — rush hour (7-9 AM, 5-8 PM) Grab can be 3-6× the rail time (On Nut→Siam: 20 min BTS vs 45-90 min car).
- Raining → rail. Grab surges and roads gridlock simultaneously.
- Short hop inside a soi (<2 km) → motorbike taxi, orange vest, ฿20-50, agree price first.
- Metered taxi flag fall ฿35; refusal to use the meter = walk away, open Grab.
- BTS and MRT still use separate stored-value cards; contactless bank cards work on MRT.

### 9. Neighborhood Matching

| Profile | Best Areas |
|---------|------------|
| Young professionals/nomads | Thonglor, Ekkamai, Ari, On Nut |
| Budget digital nomads | On Nut, Phra Khanong, Bang Na |
| Families | School catchment first (`families.md`), else Sukhumvit (Asok-Thonglor), Ari |
| Nightlife seekers | Sukhumvit Soi 11, Khao San, RCA |
| Culture & temples | Rattanakosin, Chinatown, Riverside |
| Business/finance | Silom, Sathorn, Asok |
| Luxury living | Thonglor, Sathorn, Riverside |
| Budget travelers | Khao San, Rambuttri, Chinatown |
| Anything else / unsure | Asok as base — BTS+MRT interchange, test other areas from there |

## Legal Awareness

- **Lèse-majesté**: 3-15 years per count. No exceptions, no irony, includes online activity.
- **Drugs**: death penalty possible for trafficking hard drugs (heroin, meth); possession = prison. Cannabis is the only carve-out and its rules changed twice since 2022 — verify current status.
- **Criminal defamation**: truth is not always a defense; up to 2 years, more under the Computer Crime Act. Tourists have been sued over negative online reviews — advise users to phrase complaints factually and privately first.
- **Gambling**: illegal except state lottery; private poker games get raided.
- **Vaping**: import/sale banned (up to 10 years); possession can draw fines. Don't bring vapes in.
- **Overstay ladder**: ฿500/day fine (cap ฿20,000). Voluntary departure: >90 days → 1-year ban; >1 year → 3-year; >3 years → 5-year; >5 years → 10-year. Caught while overstaying: bans double in severity (5-10 years).
- **Work permit**: any work performed inside Thailand — even unpaid or volunteer — technically requires one.

See `safety.md` for scams and emergencies.

## Digital Nomad Context

- **The DTV changed the game (Jul 2024)**: most nomads with foreign clients now have a clean answer (full terms -> Core Rule 2: Visa Reality). Before recommending workarounds, check DTV eligibility first.
- **Still gray**: DTV is not a work permit; working for Thai companies or clients remains illegal without one.
- **Infrastructure**: 100 Mbps fiber standard in condos (฿400-600/month; 1 Gbps ฿1,000-1,500); dozens of coworking spaces ฿1,200-8,000/month; work-friendly cafés everywhere.
- **Community**: large and liquid — Facebook groups and weekly meetups make Bangkok one of the easiest cities to land in solo.
- **LTR** for high earners (~$80K/year): 10-year visa, 17% flat tax for eligible categories, legal remote work.
- **Taxes are the blind spot**: the DTV solves immigration, not tax (Rule 3) — `taxes.md` before any >6-month plan.

See `nomad.md` for coworking, communities, and visa strategy.

## Output Gates

Before emitting an answer, verify:

- Role and timeline known — read from `config.yaml` or asked (Rule 1), never averaged across audiences?
- Every price a range in ฿ with ~USD at 35 (Rule 6), never a single point number?
- Anything volatile (visa terms, tax rules, cannabis, alcohol regulations) flagged verify-before-committing-money?
- Stated `dietary`, `monthly_budget`, and `home_area` respected when set?
- Legal red lines touched by the plan (lèse-majesté, drugs, work without permit, overstay) surfaced?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/bangkok/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| role | visitor \| nomad \| resident \| teacher \| retiree \| family \| entrepreneur | none | Pre-answers Rule 1; selects the default routing branch (visitor→`visitor-*.md`, retiree→`retirement.md`, family→`families.md`) |
| home_area | text (neighborhood) | none | Anchors food, nightlife, gym, and transport picks to BTS/walking distance from this base |
| monthly_budget | number (THB/month) | none | Filters neighborhood and lodging suggestions; recommendations above it get flagged, not hidden |
| currency_display | THB \| THB+USD \| THB+EUR | THB+USD | Which currencies prices are quoted in; conversion baseline is Rule 6's 35 THB ≈ $1 |
| dietary | list (vegetarian, vegan, halal, gluten-free, allergy:item) | none | Routes every food recommendation through the `food-practical.md` filters first |
| spice_tolerance | none \| mild \| thai | mild | Ordering guidance in food files ("pet nit noi" caveats vs none) |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied:

- **Transport posture**: rail-first vs comfort-first Grab, motorbike-taxi willingness — reorders routing suggestions in `transport.md`
- **Lodging style**: hotel vs serviced apartment vs condo contract — shifts answers between `visitor-lodging.md` and `resident.md`
- **Risk appetite**: street-stall adventurousness, motorbike rental, nightlife zones — tunes `food-street.md` and `safety.md` framing
- **Visa/legal posture**: conservative (real visa early, file taxes) vs minimal-compliance — tunes `visas.md` and `taxes.md` recommendations
- **Climate sensitivity**: heat tolerance, personal AQI threshold — paces itineraries and outdoor plans (`climate.md`)
- **Family context**: kids' ages, curriculum preference — drives `families.md` and neighborhood choice
- **Work setup**: coworking vs café vs home fiber — orders `nomad.md` recommendations

## Traps

| Trap | Why it fails | Do instead |
|------|--------------|------------|
| Chaining visa-exempt entries | Immigration tracks entries; back-to-back stamps → questioning or denial | Real visa (DTV, ED, Non-O) — `visas.md` |
| Assuming cannabis is simply legal | Decriminalized 2022, then re-restricted toward medical-only in 2025; rules in flux | Treat as regulated; never carry across borders |
| Trains "from Hua Lamphong" | Long-distance services moved to Krung Thep Aphiwat (Bang Sue) in 2023; only some ordinary trains still use Hua Lamphong | Check departure terminal per train before heading out |
| Taxi meter refusal at tourist spots | Driver quotes 3-5× meter price | Walk away; use Grab or hail a moving cab |
| Tuk-tuk "temple is closed" | Detour ends at commission gem/tailor shop | Temples rarely close; verify yourself, ignore touts |
| Booking "near BTS" listings | "Near" can mean an 800 m walk in 35°C heat | Check Google Maps walking time before booking |
| Renting in apartment buildings without checking electric rate | Buildings bill ฿7-8/unit vs government ~฿4-5 — doubles the AC bill | Ask the per-unit rate before signing |
| Ignoring 90-day reporting | ฿2,000 fine, compounds visa problems | Calendar it; online reporting when the site works |
| Working on a tourist stamp for Thai clients | Any work for Thai sources without permit = deportation risk | Foreign income only; DTV/LTR for legality — `nomad.md` |
| Jet ski and motorbike rentals with passport deposit | Damage-claim scam holds your passport hostage | Never leave passport as deposit; skip jet skis entirely |
| ATM habit withdrawals | ฿220 fee per withdrawal, every bank | Withdraw the max per transaction; bring a fee-reimbursing card |
| Renting sight-unseen in rainy season | Some sois flood ankle-deep every storm | Visit after heavy rain or ask in building's LINE group |
| Assuming the DTV shelters you from Thai tax | 180 days = tax resident; remitted income assessable since 2024 | Read `taxes.md` before any >6-month plan; LTR is the shelter route |
| Buying a condo in the first months | Oversupply + illiquid resale + unseen micro-location flaws | Rent 12 months in the target building/area first — `property.md` |
| Renting a scooter on a car license | Motorbike is a separate class: insurance void + checkpoint fines | Thai motorbike license first, or skip the scooter — `driving.md` |
| Visa deadline falling in Songkran week | Immigration closes ~Apr 12-16 | Extend before April 10 — `festivals.md` |

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/bangkok (install if the user confirms):

- **[travel](https://clawic.com/skills/travel)** — General travel planning, itineraries, packing
- **[tokyo](https://clawic.com/skills/tokyo)** — Another major Asian city guide
- **[seoul](https://clawic.com/skills/seoul)** — Korea's capital, similar nomad appeal
- **[singapore](https://clawic.com/skills/singapore)** — Southeast Asian hub comparison
- **[thailand](https://clawic.com/skills/thailand)** — Choosing a Thai base beyond Bangkok: islands, Chiang Mai, beaches

## Feedback

- If useful, star it: https://clawic.com/skills/bangkok
- Latest version: https://clawic.com/skills/bangkok

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/bangkok.
