---
name: Florida
slug: florida
version: 1.0.0
homepage: https://clawic.com/skills/florida
description: Navigate Florida for living, moving, working, seasonal stays, and road trips with region fit, storm planning, insurance reality, and daily logistics.
changelog: "Initial release with resident-first Florida guidance, seasonal-living support, and practical statewide logistics."
metadata: {"clawdbot":{"emoji":"🌴","requires":{"bins":[],"config":["~/florida/"]},"os":["linux","darwin","win32"],"configPaths":["~/florida/"]}}
---

## When to Use

User needs Florida-specific guidance that generic U.S. advice usually gets wrong: choosing a region, moving, licensing, insurance, hurricane prep, HOA or condo reality, healthcare access, seasonal living, or statewide trip planning.

This skill should activate for five modes: visiting, moving to Florida, living in Florida, operating a Florida-based business, and managing a seasonal or snowbird setup.

## Architecture

This skill works statelessly for one-off Florida questions. If the user wants continuity across sessions, memory lives in `~/florida/`. If `~/florida/` does not exist, read `setup.md`, explain planned local storage in plain language, and ask for confirmation before creating files. See `memory-template.md` for structure.

```text
~/florida/
└── memory.md     # User context, regions, timelines, insurance concerns, and open loops
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Region fit and metro tradeoffs | `regions.md` |
| Move-in sequence and resident checklist | `moving-and-settling.md` |
| License, registration, tolls, and vehicles | `florida-dmv-and-vehicles.md` |
| Renting, buying, condo rules, and insurance pressure | `housing-and-insurance.md` |
| Utilities, internet, storm outages, and recurring bills | `utilities-and-bills.md` |
| Taxes, wages, insurance costs, and total budget reality | `costs-and-taxes.md` |
| Hurricanes, flooding, heat, and preparedness | `storms-and-preparedness.md` |
| Laws, scams, and practical safety | `laws-and-safety.md` |
| Schools, childcare, and family planning | `family-and-schools.md` |
| Health insurance, providers, Medicare, and care access | `healthcare-and-coverage.md` |
| Jobs, LLC setup, tourism exposure, and business tradeoffs | `work-and-business.md` |
| Driving, airports, transit, and corridor planning | `transit-and-driving.md` |
| Part-time residency, snowbirds, and dual-state logistics | `seasonal-living-and-snowbirds.md` |
| Beaches, parks, theme parks, and road-trip strategy | `road-trips-and-visiting.md` |
| Official sources map | `sources.md` |

## Core Rules

### 1. Classify the User Before Giving Advice
- Decide which Florida mode applies first: visitor, future resident, current resident, business operator, or seasonal resident.
- Then anchor the answer to the user's region, metro, county, ZIP, flood zone, and school district when those variables change the recommendation.
- If that context is missing, ask for it before pretending Florida is one market.

### 2. Separate State Rules from Local Execution
- Florida-level rules are only the first layer. County tax collectors, cities, flood zones, evacuation zones, condo associations, school districts, and utility territories often change the real answer.
- Always label which parts are statewide and which parts must be verified locally.
- For address-specific questions, prefer official portals over generic summaries.

### 3. Florida Is Multiple Operating Environments
- South Florida, Central Florida, Tampa Bay, Southwest Florida, the Panhandle, the First Coast, and the Keys do not solve the same problem.
- Never compare them only on beach access or rent.
- The correct answer usually depends on storm exposure, insurance availability, commute style, age mix, healthcare access, and how seasonal the area feels.

### 4. No State Income Tax Does Not Mean Low Cost
- Include homeowners or condo insurance, flood insurance, car insurance, tolls, HOA dues, utility spikes, and storm-prep costs.
- For condo or coastal housing, mention reserves, assessments, wind mitigation, and coverage exclusions when relevant.
- Use `costs-and-taxes.md` before saying a place is "cheap."

### 5. Storm and Heat Planning Change Good Advice
- Hurricanes, storm surge, inland flooding, lightning, heat, humidity, algae events, and outage risk are not side notes.
- Adjust home choice, seasonal timing, trip design, and evacuation guidance around actual exposure.
- When weather is part of the problem, lead with readiness and fallback plans, not brochure copy.

### 6. Seasonal Residents Need Different Guidance
- Snowbirds, second-home owners, and split-year residents care about mail, insurance, vehicles, healthcare continuity, taxes, and storm readiness when away.
- Do not give full-time resident advice to a part-time household without checking how long they stay, where they vote, insure, and receive medical care.
- Use `seasonal-living-and-snowbirds.md` whenever the user splits time across states.

### 7. Deliver Sequence, Not Vacation Copy
- Florida users often need deadlines, documents, portals, and tradeoffs.
- For administrative topics, answer in the form "do this today / this week / later" whenever possible.
- For relocation or seasonal topics, show why one base region fits better than another.
- Before creating or changing local files in `~/florida/`, explain the planned write and ask for confirmation.

### 8. Use Official Sources for Unstable Rules
- Licensing, registration, homestead, evacuation, school boundaries, insurance programs, Medicare options, and park rules can change.
- Verify current information from the official state or local source before giving precise compliance steps.
- If current verification is blocked, say so plainly and avoid false precision.

## Common Traps

- Treating Florida like one market instead of a mix of metros, retiree corridors, inland towns, and high-risk coastal zones.
- Recommending a home or condo without checking flood zone, evacuation zone, reserves, assessments, and insurance fit.
- Saying "Florida is affordable because there is no state income tax" while ignoring property insurance, HOA dues, tolls, and car costs.
- Giving resident advice without asking whether the user is full-time, seasonal, retired, or theme-park or hospitality adjacent.
- Planning trips by map distance instead of I-4 traffic, heat, afternoon storms, cruise timing, and airport spread.
- Mixing up FLHSMV, county tax collectors, property appraisers, insurance offices, and local emergency management.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.myflorida.gov | Page requests only unless user explicitly wants form guidance | State service portal and resident tasks |
| https://www.flhsmv.gov | Page requests only unless user explicitly provides personal case details | Driver license, ID, registration, and vehicle workflow guidance |
| https://floridarevenue.com | Page requests only unless user explicitly wants tax-specific guidance | Tax, reemployment tax, and business references |
| https://www.myfloridacfo.com/division/consumers | ZIP, county, or region references if the user asks for insurance help | Insurance consumer help, claims, and insurer complaints |
| https://www.floridadisaster.org | County, ZIP, or evacuation context if the user asks for hazard-specific help | Emergency readiness, hurricanes, shelters, and evacuation guidance |
| https://www.fldoe.org | ZIP, city, district, or school references if the user asks for school matching | Education and district framework |
| https://www.floridahealth.gov | County references if the user asks for public-health or local-care guidance | Health department and care navigation |
| https://www.visitflorida.com | Page requests only | Official trip-planning and regional travel references |

No other data is sent externally.

## Security & Privacy

**Data that may leave your machine:**
- Public page requests to official Florida agencies and official service portals
- ZIP, county, flood-zone, or district data only when the user asks for location-specific guidance

**Data that stays local:**
- Region preference, move timeline, seasonal-living setup, insurance concerns, and open tasks in `~/florida/`

**This skill does NOT:**
- Submit government forms on the user's behalf without explicit instruction
- Store credentials, SSNs, Medicare numbers, or payment information in local memory
- Assume local rules when the answer depends on a county, municipality, condo association, or flood zone

## Trust

By using this skill, location details such as ZIP, county, district, or flood-zone context may be checked against official Florida or local-government websites when the user asks for precise guidance.

Only install if you trust those public services with that lookup context.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General itinerary design and trip planning structure
- `car-rental` — Rental car, airport pickup, and highway planning for Florida trips
- `booking` — Reservation workflows for flights, cruises, resorts, and schedule holds
- `business` — Broader business operations guidance beyond Florida-specific rules
- `health-insurance` — Deeper plan-comparison support beyond Florida-specific access questions

## Feedback

- If useful: `clawhub star florida`
- Stay updated: `clawhub sync`
