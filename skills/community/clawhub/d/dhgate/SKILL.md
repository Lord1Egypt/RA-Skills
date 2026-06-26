---
name: DHgate
slug: dhgate
version: 1.0.0
homepage: https://clawic.com/skills/dhgate
description: Buy, source, and dispute on DHgate with supplier vetting, landed-cost checks, tracking triage, and counterfeit-risk control.
changelog: Initial release with supplier vetting, cost checks, dispute prep, and safer sourcing workflows.
metadata: {"clawdbot":{"emoji":"🛒","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/dhgate/"]}}
---

## When to Use

User wants help buying, sourcing, comparing, or disputing products on DHgate.
Agent helps with seller screening, lot economics, shipping-risk triage, evidence prep, and safer category selection for personal buying or resale.

## Architecture

Memory lives in `~/dhgate/`. If `~/dhgate/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```text
~/dhgate/
├── memory.md        # Status, buying profile, active constraints
├── shortlist.md     # Candidate listings, rankings, next checks
├── sourcing.md      # Seller replies, negotiation points, MOQ notes
├── orders.md        # Tracking state, ETA assumptions, follow-ups
└── disputes.md      # Evidence checklist, timeline, decision log
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup and activation flow | `setup.md` |
| Memory structure and starter files | `memory-template.md` |
| Seller and listing scorecard | `supplier-vetting.md` |
| Real cost and margin math | `landed-cost.md` |
| Tracking and dispute triage | `shipping-disputes.md` |
| Seller message templates | `sourcing-messages.md` |
| Brand and counterfeit filters | `counterfeit-checks.md` |

## Scope

This skill ONLY:
- helps evaluate DHgate listings, stores, shipping states, dispute options, and sourcing messages.
- stores user-approved local notes in `~/dhgate/`.
- uses screenshots, order details, links, and facts the user provides.

This skill NEVER:
- places orders, confirms receipt, or opens disputes without explicit user confirmation.
- recommends off-platform payment, counterfeit sourcing, or customs evasion.
- stores payment credentials, identity documents, or card details.
- makes undeclared network requests or modifies its own core files.

## Data Storage

Local working notes live in `~/dhgate/`.
Before the first write in a session, explain the planned files in plain language and ask for confirmation.

## Core Rules

### 1. Classify the Buying Motion First
- Separate personal purchase, sample order, resale, and dropshipping before giving advice.
- The same listing can be acceptable for one-off personal use and unacceptable for repeat resale.

### 2. Never Call It Cheap Until Landed Cost Is Clear
- DHgate sticker price is only the opening number.
- Calculate unit cost with shipping, duties or VAT, payment friction, defect reserve, and downstream fulfillment before saying a deal is good.
- Use `landed-cost.md` whenever quantity, bundles, or resale margin matter.

### 3. Vet the Store, the Listing, and the Conversation Together
- A strong seller score with a vague listing is still a risk.
- A detailed listing with evasive replies is still a risk.
- Use `supplier-vetting.md` and keep a written pass or fail reason for every shortlisted option.

### 4. Start Narrow, Then Scale
- For unknown sellers or categories, prefer sample orders or the smallest sensible batch first.
- Do not recommend scaling until the user has seen real quality, real transit time, and real packaging from that seller.

### 5. Work the Timeline Before the Emotion
- Treat tracking, ETA drift, and buyer protection as a timeline problem, not a panic problem.
- If live order data is available, rely on the actual order page first.
- Use `shipping-disputes.md` to separate normal lag, seller failure, carrier handoff issues, and genuine dispute cases.

### 6. Evidence Beats Opinions in Disputes
- For damaged, wrong, incomplete, or suspicious deliveries, collect photos, package labels, quantity proof, and a short factual timeline before arguing.
- Keep seller communication concise and platform-native.
- If a dispute is needed, submit the claim with evidence and requested remedy already defined.

### 7. Counterfeit Risk Cancels Cheap Prices
- If branding, logos, packaging, or price signals point to counterfeit risk, advise away from the purchase.
- Prefer unbranded equivalents, compliant alternatives, or better-documented suppliers instead of rationalizing a risky listing.

## Common Traps

- Comparing only item price -> shipping, duties, and defect rates erase the apparent discount.
- Ordering a large first batch -> one bad seller can lock cash, time, and customer trust at the same time.
- Treating review count as proof -> recycled photos and shallow reviews can hide quality drift.
- Accepting vague seller replies -> unclear specs become impossible-to-win disputes later.
- Assuming "delivered" means solved -> carrier handoff, parcel lockers, and local post office issues still need verification.
- Chasing branded bargains -> counterfeit or seizure risk overwhelms any margin.
- Using one listing photo as truth -> DHgate catalog images are often reused across multiple sellers and factories.

## External Endpoints

This skill makes NO external network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Nothing by default. This is an instruction-only, local-first sourcing workflow.

**Data stored locally:**
- Buying profile, shortlisted sellers, cost assumptions, tracking notes, and dispute evidence planning.
- Stored in `~/dhgate/`.

**This skill does NOT:**
- store payment credentials, passports, tax IDs, or identity photos.
- recommend counterfeit sourcing or trademark infringement.
- advise customs evasion, under-declaration, or off-platform payments.
- make undeclared network calls.

## Trust

This is an instruction-only DHgate sourcing skill.
No third-party service access is required.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `shopping` - broader buying discipline for comparisons, timing, and post-purchase decisions.
- `marketplace` - cross-platform marketplace rules when DHgate should be compared against other channels.
- `amazon` - useful baseline when comparing local retail convenience against import risk and lead times.
- `price` - structured pricing logic for margin checks, bundle comparisons, and offer framing.

## Feedback

- If useful: `clawhub star dhgate`
- Stay updated: `clawhub sync`
