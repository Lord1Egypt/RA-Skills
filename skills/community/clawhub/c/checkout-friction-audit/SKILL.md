---
name: checkout-friction-audit
description: Audit checkout friction points and prioritize fixes that improve completed purchases without increasing risk. Use when the user reports high add-to-cart but low purchase rate, checkout abandonment spikes, or repeated payment/shipping complaints.
---

# Checkout Friction Audit

## Skill Card

- **Category:** Conversion
- **Core problem:** Which checkout steps are leaking intent and killing purchase completion?
- **Best for:** Conversion rate recovery projects
- **Expected input:** Checkout flow notes, abandonment signals, user complaints, policy constraints
- **Expected output:** Friction map with severity, likely cause, and fix priority
- **Creatop handoff:** Push fixes into sprint board and rerun after implementation

## Browser-first guidance

If the checkout flow is accessible by URL or staging page, prefer **OpenClaw managed browser** for direct observation before producing recommendations.

Recommended order:
1. Use any funnel notes, complaints, or screenshots the user already has.
2. If live checkout pages are available, inspect them in **OpenClaw managed browser**.
3. Use Browser Relay only when the user explicitly wants to inspect their current Chrome session.

## Workflow

1. Clarify where the drop appears to happen.
   - cart?
   - shipping step?
   - payment step?
   - mobile-specific issue?
2. Map checkout path and identify complaint-linked touchpoints.
3. Score friction by impact on completion and fix complexity.
4. Separate UX friction from trust/compliance friction.
5. Output top quick wins and structural fixes.

## Output format

Return in this order:
1. Executive summary (max 5 lines)
2. Priority actions (P0/P1/P2)
3. Evidence table (signal, confidence, risk)
4. 7-day execution plan

## Quality and safety rules

- Tie each recommendation to observed evidence, not guesswork.
- Prioritize reversible low-risk fixes first.
- Avoid recommendations that violate platform/payment policies.
- If the observed flow is partial, state that clearly.

## License

Copyright (c) 2026 **Razestar**.

This skill is provided under **CC BY-NC-SA 4.0** for non-commercial use.
You may reuse and adapt it with attribution to Razestar, and share derivatives
under the same license.

Commercial use requires a separate paid commercial license from **Razestar**.
No trademark rights are granted.
