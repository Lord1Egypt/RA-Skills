---
name: Europe
slug: europe
version: 1.0.0
homepage: https://clawic.com/skills/europe
description: Navigate Europe for travel, relocation, study, remote work, and cross-border life with bloc logic, country fit, rights, timing, and practical execution.
changelog: "Initial release with a Europe-wide framework for travel, moving, work, study, and cross-border planning."
metadata: {"clawdbot":{"emoji":"🌍","requires":{"bins":[],"config":["~/europe/"]},"os":["linux","darwin","win32"],"configPaths":["~/europe/"]}}
---

## When to Use

User needs Europe-specific guidance that generic travel or relocation advice usually gets wrong: choosing the right country or city, understanding EU vs Schengen vs eurozone rules, planning multi-country trips, moving, studying, working remotely, handling healthcare, or operating across borders.

This skill should activate for seven modes: visiting Europe, choosing a base in Europe, moving to Europe, living in Europe, studying in Europe, working remotely across Europe, and operating a Europe-facing business or freelance setup.

## Architecture

This skill works statelessly for one-off Europe questions. If the user wants continuity across sessions, memory lives in `~/europe/`. If `~/europe/` does not exist, read `setup.md`, explain planned local storage in plain language, and ask for confirmation before creating files. See `memory-template.md` for structure.

```text
~/europe/
└── memory.md     # Nationality, mobility rights, target countries, timelines, constraints, and open loops
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Europe blocs, rights layers, and country-group logic | `europe-basics-and-blocs.md` |
| Macroregions, corridors, and cluster tradeoffs | `regional-corridors-and-country-clusters.md` |
| Choosing countries, cities, and base strategy | `choosing-countries-and-cities.md` |
| Entry, visas, residence pathways, and right-to-stay logic | `entry-visas-and-right-to-stay.md` |
| Schengen math, borders, and 90/180 traps | `schengen-border-and-90-180.md` |
| Move-in sequence and settling checklist | `moving-and-settling.md` |
| Housing, banking, SIMs, utilities, and local admin | `housing-banking-phone-and-admin.md` |
| Jobs, universities, qualifications, and business setup | `work-study-and-qualifications.md` |
| Tax residence, social security, and cross-border paperwork | `taxes-social-security-and-residency.md` |
| Public healthcare, EHIC/GHIC logic, and private cover | `healthcare-and-insurance.md` |
| Rail, flights, ferries, buses, and passenger rights | `transport-and-passenger-rights.md` |
| Multi-country routing, road trips, and Europe pace design | `rail-flights-and-road-trips.md` |
| Eurozone reality, cards, cash, and everyday payments | `money-payments-and-eurozone.md` |
| Remote work, digital nomads, and split-country life | `remote-work-and-digital-nomads.md` |
| Seasonal stays, second homes, and part-year Europe life | `seasonal-living-and-second-homes.md` |
| Families, children, schools, and student tradeoffs | `family-students-and-children.md` |
| Scams, emergencies, 112, and consumer protection | `safety-scams-and-consumer-rights.md` |
| Climate, shoulder seasons, and event timing | `weather-seasons-and-trip-timing.md` |
| Weekend trips, interrail-style loops, and short-break logic | `weekend-trips-and-multicountry-routes.md` |
| Official sources map | `sources.md` |

## Core Rules

### 1. Europe Is Not One Operating System
- Separate Europe the continent from the EU, Schengen Area, eurozone, EEA, UK, Switzerland, Balkans, and microstates.
- Never answer a Europe question as if all countries share the same visa, tax, bank, health, or border rules.
- Start by identifying which legal bloc and which country or corridor actually controls the answer.

### 2. Classify the User Before Giving Advice
- Decide which Europe mode applies first: visitor, future resident, current resident, student, worker, remote worker, family household, or operator.
- Then anchor the answer to nationality, passport, visa status, target country, intended length of stay, and whether the user is moving between countries or just visiting.
- If that context is missing, ask before pretending Europe is interchangeable.

### 3. Separate Stable Framework from Volatile Execution
- Bloc definitions, 90/180 math, passenger-right concepts, and broad routing logic are stable enough to explain.
- Visa thresholds, local registration steps, fees, opening-hour quirks, health enrollment steps, and tax details can change.
- For volatile topics, explain the framework first and then verify with official current sources before giving precise compliance steps.

### 4. Country Fit Beats Bucket Lists
- Europe planning fails when users pick countries from aesthetics alone.
- Compare countries and cities using legal access, language load, weather, housing stress, healthcare depth, transport quality, salary reality, and social fit together.
- Use `choosing-countries-and-cities.md` before endorsing a base.

### 5. Cross-Border Friction Is the Real Difficulty
- Border rights, tax residence, social security, roaming, banking, school systems, driving rules, and healthcare access can all change when the user crosses countries.
- Treat Europe as a network of connected but non-identical systems.
- When the user is splitting time across countries, lead with what breaks at the boundary.

### 6. Deliver Sequences, Not Vibes
- Europe users often need a path like "choose country -> confirm right to stay -> secure housing -> register locally -> fix bank/SIM/health -> then optimize lifestyle."
- For trips, answer with transfer logic, reservation deadlines, and fallback routes.
- For moves, answer in the form "do this before arrival / in week one / in month one / after stabilizing."

### 7. Respect the Difference Between Tourist and Resident Advice
- A city that is great for a 4-day trip can be bad for long-term housing, bureaucracy, or income fit.
- Do not use tourist-season impressions to answer residency, schooling, or work questions.
- Do not use residency-oriented cost assumptions to answer short-break or interrail questions.

### 8. Use Official Europe-Level Sources Before Blogs
- Prefer Your Europe, the EU Immigration Portal, EURES, Europass, national government portals, Eurostat, and passenger-rights pages.
- Use private guides only as secondary context, never as the final authority for legal or rights-sensitive topics.
- If a country-specific official page is required, say so clearly instead of improvising.

### 9. Before Writing Local Memory, Ask
- If continuity would help, explain exactly what would be stored in `~/europe/`.
- Ask for confirmation before creating or changing local files.
- Do not save passport numbers, tax IDs, banking credentials, or full street addresses unless the user explicitly asks for that behavior.

## Common Traps

- Treating Europe as if EU membership, Schengen membership, and euro use are the same thing.
- Recommending a move path without checking the user's nationality and right to stay.
- Suggesting multi-country trips that look short on a map but waste time in transfers.
- Mixing tourist affordability with long-term housing and tax reality.
- Assuming roaming, healthcare, or consumer rights apply equally in every European country.
- Giving digital-nomad or residency advice without asking whether the user wants legal residence, tax residence, or just a long visit.
- Ignoring language load, local admin friction, and housing inventory until too late.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://europa.eu/youreurope/ | Page requests only unless user explicitly wants country-specific rights guidance | EU citizen rights, travel, residence, work, health, consumer protection |
| https://immigration-portal.ec.europa.eu/ | Nationality and target-country context only if user asks for non-EU residence or work guidance | Non-EU migration pathways by country |
| https://eures.europa.eu/ | Country, language, and profession context only if user asks for job-market guidance | Jobs, living and working conditions |
| https://europass.europa.eu/ | Qualification or CV context only if user asks for recognition or study/work prep | Skills, qualifications, and CV framework |
| https://eur-lex.europa.eu/ | Page requests only | EU law and regulation reference |
| https://ec.europa.eu/eurostat | Page requests only unless user asks for comparative data pulls | Europe-wide comparative statistics |
| https://europa.eu/112 | Country or location only if user asks for emergency readiness | Europe emergency-number framework |
| https://www.eccnet.eu/ | Country and consumer-case context only if user asks for purchase or travel-rights help | Consumer protection and dispute support |
| https://europa.eu/solvit/ | Country and rights-problem context only if user asks for EU-rights problem solving | Cross-border rights assistance |

No other data is sent externally.

## Security & Privacy

**Data that may leave your machine:**
- Public page requests to official EU and national portals
- Country, nationality, residency, profession, or route context only when the user asks for location-specific guidance

**Data that stays local:**
- Mobility goals, target countries, trip or move timelines, family constraints, and open tasks in `~/europe/`

**This skill does NOT:**
- Submit visa, tax, residency, or university forms on the user's behalf without explicit instruction
- Store passport numbers, tax IDs, bank credentials, or payment information in local memory by default
- Assume country-specific rules when the answer depends on nationality, right-to-stay, or local registration

## Trust

By using this skill, details such as nationality, target country, and cross-border route context may be checked against official European or national-government websites when the user asks for precise guidance.

Only install if you trust those public services with that lookup context.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General trip planning and itinerary structure
- `booking` — Reservation workflows and confirmation hygiene
- `car-rental` — Better cross-border rental and handoff planning
- `health-insurance` — Deeper insurance-plan comparison support
- `english` — Language support for bookings, admin, and fallback communication

## Feedback

- If useful: `clawhub star europe`
- Stay updated: `clawhub sync`
