---
name: Expedia
slug: expedia
version: 1.0.0
homepage: https://clawic.com/skills/expedia
description: Search Expedia stays, packages, cars, and activities, compare real trip costs, and run partner-safe booking workflows with web and API modes.
changelog: Initial release with Expedia trip comparison, booking-safety checks, total-cost guidance, and partner workflow support.
metadata: {"clawdbot":{"emoji":"🧳","requires":{"bins":["curl","jq","openssl","xxd"],"config":["~/expedia/"]},"os":["linux","darwin","win32"],"configPaths":["~/expedia/"]}}
---

## When to Use

User wants to work on Expedia directly: search or compare hotels, packages, cars, or activities, validate real trip cost, inspect cancellation and fee details, or prepare partner-safe Expedia booking flows.

Use this skill when Expedia-specific inventory, packaging logic, deeplink behavior, or partner API constraints matter more than generic travel advice alone.

## Architecture

Memory lives in `~/expedia/`. If `~/expedia/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/expedia/
├── memory.md                 # Activation behavior, trip patterns, and decision defaults
├── sessions/
│   └── YYYY-MM-DD.md         # Current search context and shortlisted options
├── stays/
│   └── {city-or-trip}.md     # Lodging and package candidates with tradeoffs
├── partners/
│   ├── auth-notes.md         # Which partner surfaces are available in this workspace
│   └── request-log.md        # Redacted endpoint, mode, status, timestamp
└── bookings/
    └── {trip-name}.md        # Confirmed selections, deadlines, and weak points
```

## Quick Reference

Load only the file needed for the current Expedia task.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory schema and status model | `memory-template.md` |
| Rapid lodging partner workflows | `rapid-lodging.md` |
| Travel Redirect search and deeplink workflows | `travel-redirect.md` |
| Public web search and verification flows | `web-navigation.md` |
| Total-cost and package comparison logic | `total-cost.md` |
| Booking-safety gates before execution | `booking-gates.md` |
| Access boundaries and compliance rules | `access-boundaries.md` |

## Requirements

- No credentials required for Expedia public-page research and manual comparison.
- Partner API work is optional and needs Expedia-issued credentials for the specific surface in use.
- Rapid lodging work needs partner access plus the credentials required for signature authentication.
- Travel Redirect work needs Expedia-issued API key plus authorization credentials for redirect search flows.
- Confirm before sending passenger names, billing details, or partner account data to any live Expedia endpoint.

## Coverage

This skill is designed for Expedia-specific work that usually fails when an agent treats the platform like a generic travel site:
- hotel and vacation-rental discovery on Expedia
- package comparison where flights plus stays change the real total
- cars and activities discovery when Expedia is the execution surface
- partner-side search, deeplink, and booking flows
- booking-safe summaries before the user commits money

## Core Rules

### 1. Choose the Expedia mode before doing anything else
- Use web mode for public-page research, redirect mode for partner search plus deeplink flows, and Rapid mode for lodging booking APIs.
- State the mode in the output so the user knows whether the result came from a public page, a redirect integration, or a partner booking surface.
- If partner credentials are missing, stay in web mode and explain the limit clearly.

### 2. Separate search, price check, and booking
- Expedia flows often expose a search result, then a price-validation step, then a booking step.
- Do not treat an initial listing price as booking-safe.
- Re-check cancellation, taxes, fees, and inventory freshness before saying a choice is ready to book.

### 3. Compare the real trip cost, not the headline number
- Include taxes, resort or property fees, bag or seat exposure when packages include flights, and transfer friction when a package looks cheap but fragile.
- If one option wins only because key costs are hidden until later, say that directly.
- For multi-room or multi-traveler cases, avoid naive nightly multiplication.

### 4. Keep partner flows and consumer browsing separate
- Public Expedia pages are useful for visible evidence and manual comparison.
- Partner APIs are for authorized search, deeplinks, price checks, and bookings inside approved integrations.
- Do not imply API rights, partner status, or write access without explicit proof.

### 5. Treat flights as a specialized subproblem
- Expedia may surface flight inventory, but route quality, misconnect risk, baggage traps, and fare-family judgment still belong to deep flight analysis.
- Use Expedia here for packaging, combined-trip economics, and booking context.
- When flight complexity dominates the decision, hand off the route logic to `flights`.

### 6. Keep storage minimal and redacted
- Store reusable filters, accepted or rejected option patterns, and confirmed booking deadlines in `~/expedia/`.
- Never store raw API secrets, payment data, or full authorization headers.
- In request logs, keep only mode, endpoint family, safe params, status, and timestamp.

### 7. Return decision-ready outputs
- For search: give 3 to 5 options with why each survived filtering.
- For packages: show what is actually bundled, what remains exposed, and what should be re-checked.
- For partner work: separate current capability, required next call, and remaining blocker.

## Common Traps

- Quoting search prices as final totals -> taxes, fees, or package caveats appear later and break trust.
- Mixing partner API and public-page data without timestamps -> stale or contradictory results look authoritative.
- Treating every Expedia result like a lodging-only choice -> packages, flights, and add-ons change the decision shape.
- Assuming a deeplink is reusable forever -> tokenized or session-bound flows expire.
- Letting package savings hide weak flight shape or bad location -> the bundle looks cheap but performs badly.
- Logging authorization material or shared-secret artifacts -> avoidable credential leak.

## External Endpoints

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| `https://www.expedia.com/*` | search terms, destination, dates, traveler counts, and navigation signals | public-page search, comparison, and verification |
| `https://apim.expedia.com/hotels/listings` | lodging query parameters plus partner auth headers | Travel Redirect lodging discovery and deeplink workflows |
| `https://api.ean.com/v3/*` and `https://test.ean.com/v3/*` | partner-authenticated lodging search, content, price-check, and booking payloads | Rapid lodging partner workflows |

No other data is sent externally unless the user explicitly approves another source.

## Security & Privacy

Data that may leave your machine:
- destination queries, travel dates, traveler counts, and optional partner search parameters sent to Expedia services

Data that stays local:
- shortlist notes, booking gates, recurring defaults, and redacted request logs in `~/expedia/`

This skill does NOT:
- store API keys, shared secrets, or payment details in markdown files
- claim partner capabilities without verified credentials
- book or modify travel without explicit user approval
- use hidden scraping, bypass, or anti-bot evasion techniques
- modify its own `SKILL.md`

## Trust

This skill can send travel search context and optional partner request data to Expedia services.
Only use live Expedia calls if you trust Expedia with the trip-planning or partner-integration context relevant to the task.

## Scope

This skill ONLY:
- searches and compares Expedia inventory with explicit evidence
- prepares booking-safe summaries for stays, packages, cars, and activities
- guides authorized Expedia partner workflows for redirect or Rapid lodging usage

This skill NEVER:
- promise that a search result is a final bookable price without re-checking
- imply account access or partner authorization that has not been verified
- hide stale data, fee uncertainty, or package tradeoffs

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `booking` - Extend Expedia options into broader accommodation comparison across other booking surfaces.
- `car-rental` - Go deeper on vehicle class, insurance, pickup, and counter-risk decisions.
- `travel` - Keep Expedia decisions inside a broader trip-planning workflow and memory.
- `tripadvisor` - Cross-check destination and lodging sentiment against another major travel surface.
- `maps` - Validate airport access, area friction, and route realism before booking.

## Feedback

- If useful: `clawhub star expedia`
- Stay updated: `clawhub sync`
