# Memory Template - Facebook Marketplace

Create `~/facebook-marketplace/memory.md` with this structure:

```markdown
# Facebook Marketplace Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Operating Profile
<!-- Buyer, casual seller, flipper, or recovery mode -->
<!-- Categories, city, radius, and urgency profile -->

## Search and Inventory Rules
<!-- Saved search specs, floor prices, fast-sale logic, stale listing rules -->

## Messaging Defaults
<!-- Offer bands, hold policy, pickup wording, no-show rules, and escalation style -->

## Shipping and Protection
<!-- Pickup vs shipping defaults, proof habits, payment boundaries, and dispute notes -->

## Risks and Account Health
<!-- Scam patterns, removed listing reasons, warning history, and stop conditions -->

## Notes
<!-- Durable observations worth reusing -->

---
*Updated: YYYY-MM-DD*
```

## saved-searches.md Template

Create `~/facebook-marketplace/saved-searches.md`:

```markdown
# Saved Searches

## [Category or Goal]
city:
radius:
budget:
must_have:
deal_breakers:
price_band:
next_check:
```

## inventory.md Template

Create `~/facebook-marketplace/inventory.md`:

```markdown
# Inventory

## [Item]
category:
ask_price:
floor_price:
fast_sale_price:
condition:
status: draft | live | stale | pending | sold
next_action:
```

## incident-log.md Template

Create `~/facebook-marketplace/incident-log.md`:

```markdown
# Incident Log

## YYYY-MM-DD - [Incident]
type: scam | dispute | no_show | removal | warning | payment_risk
actors:
evidence_saved:
status:
next_step:
lesson:
```

## account-health.md Template

Create `~/facebook-marketplace/account-health.md`:

```markdown
# Account Health

## Status
warning_level: none | low | medium | high
last_issue:
appeal_open: yes | no

## Recent Events
- date:
  issue:
  evidence:
  next_step:
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Default state | Keep learning durable Marketplace context |
| `complete` | Context is stable | Reuse defaults unless the user changes direction |
| `paused` | User wants lower overhead | Save only critical updates |
| `never_ask` | User opted out of persistence | Operate statelessly |
