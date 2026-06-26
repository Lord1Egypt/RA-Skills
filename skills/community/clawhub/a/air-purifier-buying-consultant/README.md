# Air Purifier Buying Consultant

> Turns any AI agent into an expert air purifier buying consultant.

## What it does

Guides air purifier buyers through a structured consultation to identify exactly which specs they need for their specific room size, pollutant type, health situation, and region — without relying on biased sales advice. Delivers a prioritised spec list (non-negotiable → recommended → optional) and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed question groups covering: room dimensions, primary pollutant concern (allergens, smoke, VOCs, bacteria), household context (pets, smokers, respiratory conditions), usage pattern, electrical infrastructure, and regional standards
2. Applies verified industry formulas — AHAM CADR sizing rule, ACH (Air Changes per Hour) calculation for target pollutant type, ceiling height correction, filter type matching by pollutant, noise dB(A) thresholds for sleeping environments
3. Proactively flags common buyer mistakes: HEPA-type vs True HEPA confusion, coverage area vs CADR discrepancy for sensitive users, ioniser misconceptions, inadequate carbon bed weight for VOCs, exhausted filter risk, filter availability in the user's region
4. Delivers a structured spec recommendation: non-negotiable → recommended → optional
5. Suggests up to 5 real products matching the user's confirmed specs, tailored to their country/region

## Requirements

- No external APIs or environment variables required
- No runtime dependencies
- Works with any AI agent that supports SKILL.md (OpenClaw, ClawHub, etc.)
- Pure instruction-based — agent reasoning does the work

## Installation

Add via ClawHub or reference the SKILL.md directly in your agent configuration.

## Coverage

- **Regions supported:** Europe (CE), UK (UKCA), USA/Canada (ETL/UL, Energy Star), India (BIS), Saudi Arabia (SASO), Pakistan (PSQCA), China (GB/T 18801), and others via voltage/certification logic
- **Pollutant types covered:** Dust, pollen, pet dander, cigarette/wildfire smoke, cooking odours, VOCs/chemical fumes, bacteria, viruses
- **Unit types:** Tower, tabletop, floor-standing; HEPA, activated carbon, UV-C, ioniser combinations
- **Standards applied:** AHAM CADR (CFM and m³/h), ACH methodology (EPA/AHAM), EN 1822 True HEPA (H13), US DOE HEPA definition, EPA ozone limits for ionisers

## License

MIT

## Homepage

https://github.com/arbazex/home-appliance-buying-consultants/tree/master/air-purifier-buying-consultant
