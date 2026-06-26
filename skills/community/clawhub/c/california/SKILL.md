---
name: California
slug: california
version: 1.0.0
homepage: https://clawic.com/skills/california
description: Navigate California for living, moving, working, and road trips with region fit, housing reality, hazard planning, and daily logistics.
changelog: "Initial release with resident-first California guidance, regional tradeoffs, and practical state-level logistics."
metadata: {"clawdbot":{"emoji":"🌊","requires":{"bins":[],"config":["~/california/"]},"os":["linux","darwin","win32"],"configPaths":["~/california/"]}}
---

## When to Use

User needs California-specific guidance that generic U.S. advice usually gets wrong: choosing a region, moving, licensing, housing, taxes, wildfire and earthquake readiness, healthcare, schools, commuting, or statewide trip planning.

This skill should activate for four modes: visiting, moving to California, living in California, and operating a California-based business.

## Architecture

This skill works statelessly for one-off California questions. If the user wants continuity across sessions, memory lives in `~/california/`. If `~/california/` does not exist, read `setup.md`, explain planned local storage in plain language, and ask for confirmation before creating files. See `memory-template.md` for structure.

```text
~/california/
└── memory.md     # User context, region, timelines, constraints, and open loops
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Regions, metros, and base-city tradeoffs | `regions.md` |
| Move-in sequence and relocation checklist | `moving-and-settling.md` |
| Driver license, registration, smog, and DMV flow | `california-dmv-and-vehicles.md` |
| Renting, buying, insurance pressure, and property fit | `housing-and-insurance.md` |
| Electricity, water, gas, internet, and recurring bills | `utilities-and-bills.md` |
| Taxes, salary reality, and total cost of life | `costs-and-taxes.md` |
| Wildfire, earthquake, flood, and outage readiness | `hazards-and-preparedness.md` |
| Laws, scams, and practical safety | `laws-and-safety.md` |
| Schools, childcare, and family-location logic | `family-and-schools.md` |
| Health insurance, care access, and plan selection | `healthcare-and-coverage.md` |
| Work, startups, LLCs, and statewide business tradeoffs | `work-and-business.md` |
| Transit, driving, and commute design | `transit-and-commutes.md` |
| Road trips, parks, and visiting strategy | `road-trips-and-visiting.md` |
| Official sources map | `sources.md` |

## Core Rules

### 1. Classify the User Before Giving Advice
- Decide which California mode applies first: visitor, future resident, current resident, or business operator.
- Then anchor the answer to the user's region, metro, county, ZIP, and school district when those variables change the recommendation.
- If that context is missing, ask for it before pretending California is one market.

### 2. Separate State Rules from Local California Reality
- California-level rules are only the first layer. City, county, utility territory, school district, coastal or inland climate, and insurance exposure often change the real answer.
- Always label which parts are statewide and which parts must be verified locally.
- For address-specific questions, prefer official portals over generic summaries.

### 3. California Is a Set of Distinct Operating Environments
- Bay Area, Los Angeles, Orange County, Inland Empire, San Diego, Sacramento, Central Coast, and mountain or desert regions do not solve the same problem.
- Never compare them as if only rent changes.
- The correct answer usually depends on housing cost, commute shape, hazard exposure, and job geography together.

### 4. Total Cost Beats Headline Rent or Salary
- Include state income tax, sales tax variation, car or transit cost, parking, utilities, insurance, and hazard-driven costs.
- For homeowners and renters, mention wildfire or earthquake readiness, deductible pressure, and availability problems when relevant.
- Use `costs-and-taxes.md` before saying a place is "worth it."

### 5. Hazard Planning Changes Good Advice
- Wildfire, smoke, earthquake, flood, mudslide, drought, heat, and outage risk are not side notes.
- Adjust home choice, commute, trip design, and insurance guidance around actual exposure.
- When hazard risk matters, lead with readiness and fallback plans, not scenery.

### 6. Deliver Sequence, Not Brochure Copy
- California users often need deadlines, documents, portals, and tradeoffs.
- For administrative topics, answer in the form "do this today / this week / later" whenever possible.
- For destination or relocation topics, show why one base region fits better than another.
- Before creating or changing local files in `~/california/`, explain the planned write and ask for confirmation.

### 7. Use Official Sources for Unstable Rules
- DMV steps, smog rules, tax rates, wildfire insurance issues, district boundaries, and health-coverage details can change.
- Verify current information from the official state or local source before giving precise compliance steps.
- If current verification is blocked, say so plainly and avoid false precision.

## Common Traps

- Treating California like one state experience instead of multiple different markets and risk zones.
- Recommending a neighborhood or suburb without checking commute shape, insurance stress, and district fit.
- Comparing salaries without subtracting state tax, parking, transit, utilities, and local cost pressure.
- Ignoring wildfire, smoke, earthquake, or flood exposure until after housing is narrowed.
- Mixing up DMV, CDTFA, FTB, Covered California, CPUC-regulated utilities, and local school or county systems.
- Planning California travel by map distance instead of traffic, mountain timing, permits, and seasonal hazard conditions.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.ca.gov | Page requests only unless user explicitly wants form guidance | State services and resident tasks |
| https://www.dmv.ca.gov | Page requests only unless user explicitly provides case details | Driver license, REAL ID, registration, and smog workflows |
| https://www.cdtfa.ca.gov | Page requests only unless user explicitly wants tax-specific guidance | Sales tax and local district tax guidance |
| https://www.ftb.ca.gov | Page requests only unless user explicitly wants income-tax guidance | State income tax references and resident tax workflows |
| https://www.calfire.ca.gov | ZIP, county, or region references if the user asks for wildfire-specific guidance | Wildfire preparedness and local fire-risk context |
| https://www.earthquake.ca.gov | Page requests only | Earthquake alerts and preparedness guidance |
| https://www.insurance.ca.gov | ZIP, county, or region references if the user asks for insurance or wildfire-loss guidance | Insurance help, wildfire consumer protections, and claims guidance |
| https://www.coveredca.com | County or ZIP if the user asks for marketplace coverage help | Health insurance marketplace and plan lookup |
| https://www.cde.ca.gov | ZIP, city, district, or school references if the user asks for school matching | Education and school district framework |

No other data is sent externally.

## Security & Privacy

**Data that may leave your machine:**
- Public page requests to official California agencies and official service portals
- ZIP, county, or district data only when the user asks for location-specific guidance

**Data that stays local:**
- Region preference, move timeline, family constraints, vehicle notes, and open tasks in `~/california/`

**This skill does NOT:**
- Submit government forms on the user's behalf without explicit instruction
- Store credentials, SSNs, or payment information in local memory
- Assume local rules when the answer depends on a city, county, district, or utility territory

## Trust

By using this skill, location details such as ZIP, county, or district may be checked against official California or local-government websites when the user asks for precise guidance.

Only install if you trust those public services with that lookup context.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` — General itinerary design and travel planning structure
- `car-rental` — Rental car, pickup, and handoff decisions for California trips
- `home-buying` — Deeper purchase workflow support after region and housing fit are narrowed
- `health-insurance` — More detailed insurance-plan comparison and terminology support
- `business` — Broader business operations guidance beyond California-specific rules

## Feedback

- If useful: `clawhub star california`
- Stay updated: `clawhub sync`
