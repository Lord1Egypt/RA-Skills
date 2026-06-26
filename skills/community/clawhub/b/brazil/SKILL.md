---
name: Brazil
slug: brazil
version: 1.0.0
homepage: https://clawic.com/skills/brazil
changelog: "Initial release with verified Brazil entry rules, money strategy, region playbooks, and practical travel logistics."
description: Plan Brazil trips with region-specific routing, visa and money clarity, season-aware logistics, and concrete city-nature playbooks.
metadata: {"clawdbot":{"emoji":"🇧🇷","requires":{"bins":[],"config":["~/brazil/"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/brazil/` does not exist or is empty, read `setup.md` and start naturally.

## When to Use

User is planning a Brazil trip and needs more than generic inspiration: nationality-specific entry checks, realistic routing across huge distances, city and beach tradeoffs, neighborhood-aware stays, money and payment strategy, and safer on-the-ground execution.

## Architecture

Memory lives in `~/brazil/`. See `memory-template.md` for structure.

```
~/brazil/
└── memory.md     # Trip context and evolving constraints
```

## Quick Reference

Use this map to enter the right decision module before building the route.

| Topic | File |
|-------|------|
| **Entry, Border, and Money** | |
| Tourist entry, visas, passport checks, vaccines | `entry-and-documents.md` |
| Customs, declarations, restricted goods, cash | `customs-and-border.md` |
| Cards, cash, PIX, exchange, CPF friction | `money-payments-and-exchange.md` |
| **Planning Backbone** | |
| Macro-regions and route architecture | `regions.md` |
| Sample itineraries for 7-21 days | `itineraries.md` |
| Accommodation and neighborhood logic | `accommodation.md` |
| Budget framing and hidden-cost traps | `budget-and-costs.md` |
| Flights, buses, ferries, airport buffers | `transport-domestic.md` |
| Self-drive loops, tolls, night-driving rules | `road-trips-and-driving.md` |
| Parks, islands, lodges, permits, nature logistics | `national-parks-and-nature.md` |
| Cross-border side trips and re-entry risk | `border-hops-and-neighbor-countries.md` |
| **Major Regions and Cities** | |
| Rio de Janeiro playbook | `rio-de-janeiro.md` |
| Sao Paulo playbook | `sao-paulo.md` |
| Salvador and Bahia coast playbook | `salvador-and-bahia-coast.md` |
| Foz do Iguacu playbook | `foz-do-iguacu.md` |
| Manaus and Amazon playbook | `manaus-and-amazon.md` |
| Pantanal and Bonito playbook | `pantanal-and-bonito.md` |
| Florianopolis and Santa Catarina coast playbook | `florianopolis-and-santa-catarina.md` |
| Fernando de Noronha and Recife playbook | `fernando-de-noronha-and-recife.md` |
| Minas Gerais and colonial cities playbook | `minas-gerais-and-colonial-cities.md` |
| Brasilia and Chapada dos Veadeiros playbook | `brasilia-and-chapada-dos-veadeiros.md` |
| **Lifestyle and Execution** | |
| Food strategy by region and city type | `food-guide.md` |
| Nightlife and late-return logic | `nightlife.md` |
| Families, mixed ages, and calmer routes | `family-travel.md` |
| Accessibility and low-mobility planning | `accessibility.md` |
| Safety, theft prevention, beach and heat risk | `safety-and-emergencies.md` |
| Climate, rain, heat, smoke, and events | `weather-and-seasonality.md` |
| Connectivity, eSIM, transport, and useful apps | `telecoms-and-apps.md` |
| Research sources map | `sources.md` |

## Core Rules

### 1. Build Brazil by Macro-Blocks, Not by Wish List
For short and medium trips, keep to one anchor block and one contrast block at most. Brazil punishes fantasy routing more than most countries because flights, ferries, and road transfers consume real daylight.

### 2. Lock Entry, Health, and Money Before Non-Refundables
Before buying flights, confirm the correct entry path in `entry-and-documents.md`, check vaccine recommendations for the planned ecosystems, and decide the payment model from `money-payments-and-exchange.md`.

### 3. Choose Cities by Profile, Not by Fame
Rio, Sao Paulo, Salvador, Florianopolis, Recife, and Brasilia solve different trips. Recommend the city and neighborhood that fits the user's pace, beach needs, food goals, and risk tolerance.

### 4. Always State the Transfer Cost of Every Dream Add-On
Each extra region must include the true price of adding it:
- Door-to-door travel time
- New baggage or transfer costs
- Lost beach, park, or city time
- New weather or logistics risk

### 5. Treat PIX and CPF as Friction, Not Assumptions
Cards work widely in major corridors, but local operators, event tickets, and some websites may prefer PIX or ask for CPF. Offer foreigner-safe booking channels and do not promise every local deal is accessible.

### 6. Give Safer Arrival and Return Plans
When users land late, move between neighborhoods, or return after nightlife, recommend the transport model explicitly and tell them what to avoid improvising.

### 7. Deliver Actionable Plans
Output should include:
- Best-fit base city and neighborhood
- Day-by-day flow with realistic transfer buffers
- What must be booked early
- Payment and connectivity setup
- Safety and weather fallback notes

## Common Traps

- Treating Brazil like one compact destination instead of several different trip products.
- Adding Amazon, Rio, Iguacu, and beach islands into one short holiday.
- Assuming "best time for Brazil" exists as one answer for all regions.
- Choosing accommodation by nightly rate only and losing hours in traffic or unsafe arrival patterns.
- Assuming every app, ticket site, or small operator will accept foreign cards without friction.
- Underestimating New Year, Carnival, and school-holiday price spikes.
- Treating security as a generic warning instead of a context-specific operating rule.

## Security & Privacy

**Data that stays local:** Trip preferences in `~/brazil/`

**This skill does NOT:** Access files outside `~/brazil/` or make network requests.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `travel` - General trip planning and itinerary structure
- `booking` - Reservation workflows and confirmation hygiene
- `car-rental` - Better self-drive strategy and handoff logistics
- `food` - Deeper restaurant and cuisine recommendations
- `portuguese` - Language support for bookings, transport, and service interactions

## Feedback

- If useful: `clawhub star brazil`
- Stay updated: `clawhub sync`
