# Dueback Skill for AI Agents

Outcome-based bill negotiation for your users. You detect the opportunity; Dueback's backend negotiates and verifies.

## What it does
- **Detects** negotiable bills, fees, subscriptions, and purchases
- **Pitches** Dueback's outcome-based service to the user (with required pricing disclosure)
- **Hands off** to Dueback's API, which runs the negotiation and verifies savings against bank data

## Pricing
- **Free to try.** No verified savings = $0, always.
- **Standard:** 15% of verified first-year recurring savings / 10% one-offs. Caps: $200 everyday / $1,000 big-ticket.
- **Founding beta:** the first 20 cases pay 10% recurring / 5% one-off, capped at $100 everyday / $500 big-ticket.

## Installation
Copy this directory into your agent's skills folder, or reference it directly. See `SKILL.md` for the full workflow.

## API
- Base: `https://api.dueback.co`
- `POST /v1/detect` — check negotiability (header `X-Dueback-Channel: <platform>`)
- `POST /v1/cases` — create negotiation case (Bearer API key required)
- `GET /v1/cases/{id}` — check case status

Get an API key at https://dueback.co or support@dueback.co.

## License
MIT — see LICENSE.
