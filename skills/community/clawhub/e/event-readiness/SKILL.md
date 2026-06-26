---
name: event-readiness
description: Check whether a seller is actually ready for a marketplace event, promo spike, or campaign window before traffic is pushed. Use when the user wants to know if inventory, pricing, creator support, content, service, and fulfillment are ready enough to participate without wasting the event.
---

# Event Readiness

Check readiness before the team burns an event with weak preparation.

## Skill Card

- **Category:** Operations
- **Core problem:** Are we ready enough to enter this event window?
- **Best for:** Marketplace promos, brand events, seasonal pushes, and campaign spikes
- **Expected input:** Event timing + hero SKUs + inventory + pricing + support readiness
- **Expected output:** Readiness verdict + gap list + must-fix priorities
- **Creatop handoff:** Push critical gaps into launch and campaign prep workflows

## Before you run

Ask the user to clarify:
- event type
- event date range
- hero products
- current inventory situation
- pricing plan
- creator / affiliate support
- content volume readiness
- customer support coverage
- fulfillment readiness

If the event is near and the inputs are incomplete, say so explicitly.

## Optional tools / APIs

Useful but not required:
- inventory export
- SKU list
- promo plan sheet
- creator list
- content calendar
- fulfillment SLA sheet
- Google Sheets / CSV

If the user has no exports, continue with checklist mode and mark blind spots.

## Workflow

1. Confirm the event scope.
2. Review readiness across six areas:
   - inventory
   - pricing
   - traffic support
   - content support
   - customer support
   - fulfillment
3. Flag critical gaps.
4. Decide:
   - ready
   - ready with fixes
   - not ready
5. Produce a must-fix sequence.

## Output format

Return in this order:
1. Readiness verdict
2. Critical gaps
3. Must-fix before launch
4. Nice-to-fix if time allows
5. Final go / no-go note

## Fallback mode

If the user only has partial information:
- run checklist mode
- call out unknowns as risk
- do not mark the event “ready” unless the critical path is reasonably covered

## Quality rules

- Focus on launch failure points first.
- Distinguish critical gaps from nice-to-have polish.
- Do not confuse “some assets exist” with true event readiness.
- Keep the verdict decision-oriented.

## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
