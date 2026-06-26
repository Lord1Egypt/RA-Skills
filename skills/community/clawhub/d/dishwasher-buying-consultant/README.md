# Dishwasher Buying Consultant

> Turns any AI agent into an expert dishwasher buying consultant.

## What it does

Guides dishwasher buyers through a structured consultation to identify exactly which specs they need for their specific household size, kitchen space, water hardness, noise situation, and region — without relying on biased sales advice. Delivers a prioritised spec list (non-negotiable → recommended → optional) and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user with targeted, research-backed question groups covering: household size and load frequency, installation space and form factor, plumbing and water supply, electrical infrastructure, water hardness, noise sensitivity, programme needs, and long-term intent
2. Applies verified industry standards — IEC 60436 place-setting definition and capacity sizing rules, EU A–G energy label per-cycle kWh and litre benchmarks, IEC 60704-2-3 noise test reference, water hardness °dH thresholds for softener requirement, drying method comparison, and programme duration ranges
3. Proactively flags common buyer mistakes: measuring only width and ignoring depth, selecting capacity by place-setting count without checking rack flexibility, skipping a built-in softener in hard-water areas, ignoring dB(A) rating for open-plan kitchens, integrated panel sourcing complexity, and off-grid peak wattage risk
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

- **Regions supported:** Europe (CE, EU energy label A–G), UK (UKCA), USA/Canada (UL/ETL, Energy Star), India (BIS, BEE), Saudi Arabia (SASO), Pakistan (PSQCA), and others via voltage/certification logic
- **Form factors covered:** Freestanding, semi-integrated, fully integrated, slimline (45 cm), countertop/tabletop
- **Standards applied:** IEC 60436 (capacity test), IEC 60704-2-3 (noise test), EU ErP Directive energy label, US EPA Energy Star, BEE star rating

## License

MIT

## Homepage

https://github.com/arbazex/home-appliance-buying-consultants/tree/master/dishwasher-buying-consultant
