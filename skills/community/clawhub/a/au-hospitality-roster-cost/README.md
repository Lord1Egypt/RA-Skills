# au-hospitality-roster-cost

**Hospitality Roster & Labour Cost Optimiser for Australian venues.**

An instruction-only AI agent skill covering the Hospitality Industry (General) Award 2020 [MA000009 — HIGA]: pay rates, penalty rate multipliers, overtime, casual loading, junior rates, superannuation, allowances, and roster cost optimisation for hotels, pubs, bars, and accommodation venues.

---

## What this skill does

Turns an AI agent into an expert hospitality labour cost advisor that can:

- Look up base rates for all HIGA classification levels (Introductory through Level 6), effective 1 July 2025
- Calculate penalty rates for Saturday (125%/150%), Sunday (150%/175%), public holidays (225%/250%), and evening/night flat-dollar loadings (+$2.81/hr and +$4.22/hr)
- Calculate overtime (150% first 2hrs, 200% after) and rostered day off rates
- Apply junior rate percentages (40%–90% by age) and flag the liquor service adult-rate override
- Apply 25% casual loading and explain casual conversion rights (Closing Loopholes No.2 Act 2024)
- Calculate superannuation at 12% (from 1 July 2025) on ordinary time earnings
- Explain leave entitlements: 4 weeks annual leave + 17.5% loading, personal/carer's leave
- Identify award coverage issues (HIGA vs Restaurant Award vs Clubs Award vs Fast Food Award)
- Calculate weekly labour cost, labour cost percentage (LCP), and flag benchmark variances
- Give actionable roster optimisation strategies to reduce cost without breaching compliance
- Flag wage theft risk areas and compliance obligations (criminal penalties from 1 January 2025)

---

## Who it's for

Australian hospitality employers covered by HIGA MA000009 — hotels, motels, pubs, taverns, bars, resorts, casinos, caravan parks. Australian market only.

---

## How it works

The agent asks 1–3 targeted diagnostic questions (venue type, employee classification, employment type) before calculating any rate. All award data is embedded in the skill — no external API calls.

---

## Requirements

- No environment variables
- No external APIs
- No binaries
- Compatible with OpenClaw, Hermes Agent, Claude, and any instruction-following AI agent

---

## Important: Rate Update Cycle

HIGA base rates change every 1 July following the Fair Work Commission's Annual Wage Review. This skill contains rates effective from **1 July 2025**. Update the rate tables in Step 2 and the flat-dollar evening loadings in Step 4 each July.

Official source: [fairwork.gov.au/pay-guides](https://www.fairwork.gov.au/pay-and-wages/minimum-wages/pay-guides)

---

## Disclaimer

This skill provides general information only. It is not legal, payroll, or employment advice. Users should verify all rates against the current Fair Work pay guide and consult a registered employment lawyer or the Fair Work Ombudsman (1300 799 675) for complex or disputed situations.

---

## Version

1.0.0

---

## License

MIT
