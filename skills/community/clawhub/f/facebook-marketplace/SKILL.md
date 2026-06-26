---
name: Facebook Marketplace
slug: facebook-marketplace
version: 1.0.0
homepage: https://clawic.com/skills/facebook-marketplace
description: Buy and sell on Facebook Marketplace with pricing discipline, safer messaging, shipping guardrails, scam detection, and account-safe workflows.
changelog: Initial release with buyer, seller, shipping, policy, and interface guidance for Facebook Marketplace.
metadata: {"clawdbot":{"emoji":"🛍️","requires":{"bins":[]},"os":["darwin","linux","win32"],"configPaths":["~/facebook-marketplace/"]}}
---

## When to Use

User needs practical Facebook Marketplace help in real time: finding good local deals, screening scammy listings, writing or fixing a listing, handling buyer messages, planning pickup, deciding on shipping, or recovering from account warnings.
Use this skill when the output must respect how Marketplace actually works across public web, signed-in web, and mobile, not generic ecommerce advice.

## Architecture

Memory lives in `~/facebook-marketplace/`. If `~/facebook-marketplace/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/facebook-marketplace/
|-- memory.md          # Core profile, area, goals, and durable operating rules
|-- saved-searches.md  # Buyer watchlists, search specs, and go/no-go filters
|-- inventory.md       # Seller inventory, ask prices, floor prices, and stale listing notes
|-- message-lab.md     # Reusable reply patterns, offer rules, and no-show handling
|-- incident-log.md    # Scams, disputes, cancellations, and blocked patterns
`-- account-health.md  # Warnings, listing removals, appeals, and stop conditions
```

## Quick Reference

Load only the file needed for the current bottleneck.

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory structure and status model | `memory-template.md` |
| Buyer search, screening, and pickup flow | `buyer-flow.md` |
| Listing quality, pricing, and sell-through discipline | `listing-and-pricing.md` |
| Buyer and seller messaging patterns | `messages-and-negotiation.md` |
| Shipping, proof, and transaction protection | `shipping-and-protection.md` |
| Policies, warnings, and account-health rules | `policy-and-account-health.md` |
| Surface map, API limits, and automation boundaries | `interface-and-automation.md` |

## Operating Coverage

This skill combines four layers in one execution model:
- buyer layer: search specs, value scoring, seller vetting, negotiation, and safe pickup planning
- seller layer: listing creation, pricing, buyer screening, hold policy, and time-to-sale decisions
- protection layer: scam detection, payment guardrails, proof discipline, and escalation steps
- account-health layer: policy checks, restriction avoidance, and evidence-first recovery when listings are removed or warnings appear

## Data Storage

Local notes in `~/facebook-marketplace/` may include:
- city, radius, categories, and budget patterns for buying
- inventory, floor prices, refresh rules, and pickup defaults for selling
- reusable message patterns, offer thresholds, and no-show rules
- scam indicators, removed-listing reasons, and appeal evidence timelines

## Core Rules

### 1. Lock the Operating Lane First
Identify the active lane before giving advice:
- buyer
- casual local seller
- flipper or repeat seller
- account-recovery or safety mode

Advice that ignores the lane usually breaks on price, urgency, or risk tolerance.

### 2. Treat Public Web, Signed-In Web, and Mobile as Different Surfaces
Marketplace behavior changes by surface:
- public web can expose browse, category, search, and public item pages
- signed-in web handles active account workflows
- mobile may carry features that are limited or unavailable on desktop

Never guess a feature is universal across all three.

### 3. Price From Local Reality, Not Aspirational Listings
Use nearby comps, item condition, completeness, seasonality, and pickup friction to set a realistic range.
For bulky or low-value items, distance and effort can matter more than list price.

### 4. Make Messaging Evidence-First
Before moving a deal forward, confirm the details that change the decision:
- condition
- completeness
- exact model or dimensions
- availability
- pickup or shipping constraints

Never treat vague seller or buyer replies as proof.

### 5. Choose Pickup Versus Shipping Deliberately
Local pickup is usually the default for bulky, fragile, urgent, or low-margin items.
Shipping only makes sense when margin, packaging risk, and platform protection still work after fees and effort.

### 6. Safety Mode Beats Speed
If scam signals, pressure, off-platform payment requests, fake urgency, or identity mismatches appear, stop optimizing for conversion.
Pause, summarize the risk, and recommend the safest next move.

### 7. No Unsupported Automation or Account Evasion
Do not invent a Marketplace API, CLI, or Graph endpoint for consumer buying and selling.
Do not recommend bots, scraping behind login, mass messaging, repost farms, or anti-detection tactics.

## Facebook Marketplace Traps

- Treating all listings as current inventory -> dead listings waste time and distort pricing.
- Using national comps for a local-only item -> price looks fine on paper but never sells nearby.
- Letting the buyer or seller move payment or proof off platform too early -> fraud exposure rises fast.
- Writing generic AI-sounding listings -> trust drops and serious buyers disengage.
- Accepting vague shipping assumptions -> margin disappears once packing, fees, and breakage risk show up.
- Reposting, duplicating, or editing recklessly after warnings -> account-health risk compounds.
- Assuming Meta offers a supported public Marketplace API or CLI for these actions -> automation plan becomes unusable.

## External Endpoints

Only these endpoints are allowed for this skill; block any non-listed domain unless user explicitly approves it.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| https://www.facebook.com | user-approved search terms, listing views, listing drafts, messages, and transaction-related actions | Marketplace browsing, listing management, and account workflows |
| https://www.messenger.com | user-approved Marketplace message content and thread context | Continue Marketplace conversations when they route through Messenger |
| https://www.facebook.com/help | user-approved article lookups and policy queries | Verify feature availability, policies, and support guidance |

No other data is sent externally.

## Security & Privacy

Data that leaves your machine:
- none by default from this instruction set
- only user-approved Facebook or Messenger traffic when the user requests live Marketplace work

Data that stays local:
- context and operating memory under `~/facebook-marketplace/`
- search specs, inventory notes, message defaults, incident logs, and account-health notes

This skill does NOT:
- ask for passwords, one-time codes, card details, or identity documents in plain text
- move payments, deposits, or dispute handling off platform for convenience
- automate high-risk account actions without explicit user approval
- provide restriction-bypass, anti-detection, or fake-account workflows

## Trust

By using this skill, data may be sent to Meta through Facebook Marketplace and Messenger.
Only install if you trust Meta with your listing, message, and transaction data.

## Scope

This skill ONLY:
- structures Facebook Marketplace buying and selling workflows into clear next actions
- helps price, message, screen, document, and escalate safely
- keeps continuity through local memory and focused operating playbooks

This skill NEVER:
- guarantees a sale, a deal, shipping eligibility, or policy outcomes
- claims unsupported API or CLI access exists for consumer Marketplace actions
- helps bypass restrictions, impersonate users, or move risky flows off platform

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `marketplace` - Compare Marketplace against other buyer, seller, and builder workflows.
- `buy` - Improve buyer-side decisions when the purchase needs tighter screening.
- `sell` - Strengthen listing, pricing, and closing discipline across channels.
- `pricing` - Set floors, negotiation bands, and margin-aware discount rules.
- `ecommerce` - Expand from local Marketplace execution into broader commerce systems.

## Feedback

- If useful: `clawhub star facebook-marketplace`
- Stay updated: `clawhub sync`
