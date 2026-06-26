# Generator Buying Consultant

> Turns any AI agent into an expert generator buying consultant.

## What it does

Guides buyers through a structured consultation to calculate exactly which generator specs they need — rated wattage, surge wattage, fuel type, output voltage and frequency, and generator type — based on their specific appliances, outage situation, operating environment, and region. Delivers a prioritised spec list with an explicit load calculation table and up to 5 matched product suggestions.

## How it works

1. Agent interviews the user across eight areas: use case and location, appliances and loads, motor-start surge loads, operating environment and noise, fuel type and supply, usage pattern, transfer switch and panel connection, and user profile
2. Applies verified load-sizing formulas: running watt summation, surge/starting watt calculation per appliance (2–3× running for motors), 1.25 safety margin, and altitude derating (3–4% per 300 m / 1,000 ft)
3. Flags critical safety issues proactively — CO indoor operation risk, backfeed without a transfer switch, frequency mismatch, and high-THD damage to sensitive electronics
4. Delivers a structured spec recommendation: non-negotiable → recommended → optional, with load calculations shown
5. Suggests up to 5 real generators matching the user's confirmed specs, tailored to their region and certifications

## Key formulas applied

| What                      | Formula                                                                            |
| ------------------------- | ---------------------------------------------------------------------------------- |
| Total running watts       | Sum of all simultaneously needed appliance running watts                           |
| Required surge watts      | (Running watts of all other loads) + (Highest-surge appliance running watts × 2–3) |
| Recommended rated wattage | Total running watts × 1.25                                                         |
| Altitude derating         | Rated watts × (1 − 0.035 × altitude in 300 m increments)                           |

## Safety warnings built in

- **CO poisoning**: Flags indoor/garage operation as life-threatening in every relevant context
- **Backfeed**: Flags illegal/dangerous direct panel connection without a transfer switch
- **Frequency mismatch**: Flags 50Hz/60Hz errors that damage motors
- **THD damage**: Flags high-THD conventional generators connected to sensitive electronics

## Regional certification coverage

EPA + CARB (USA/California), CE (EU/UK), RCM (Australia/NZ), CPCB II (India), CSA (Canada).

## Requirements

- No external APIs or environment variables required
- No runtime dependencies
- Works with any AI agent that supports SKILL.md (OpenClaw, ClawHub, etc.)
- Pure instruction-based — agent reasoning does the work

## Installation

Add via ClawHub or reference the SKILL.md directly in your agent configuration.

## License

MIT

## Homepage

https://github.com/arbazex/power-energy-buying-consultants/tree/master/generator-buying-consultant
