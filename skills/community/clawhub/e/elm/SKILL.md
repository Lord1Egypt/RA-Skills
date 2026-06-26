---
name: elm
slug: elm
version: 2.0.1
description: Assisted 饿了么 ordering skill that turns a natural-language request plus delivery address, item name, requirements, and budget into a ready-to-pay cart: resume from a user-authenticated Ele.me session, search nearby merchants by address, compare real payable totals with visible coupons and discounts, and add the best basket to cart before handing off for payment.
---

# elm

Use this skill when the user wants real Ele.me cart-building help, not just public promo analysis.

This is a consent-based assisted-ordering skill. It may access the user's Ele.me account, saved addresses, account-visible coupons or red packets, and cart state only after explicit user consent and only after the user has already authenticated in the official Ele.me surface. Never store or reuse addresses, account data, or session details outside the current session.

## Required Inputs

Before execution, collect the minimum blocking details:
- delivery address
- target item or basket
- specific requirements such as flavor, portion, no-onion, merchant preference, dietary limits, brand, or ETA preference
- budget ceiling

If one of these is missing and it blocks execution, ask only for the missing item.

## What This Skill Should Do

Default outcome:
- resume from the user's existing authenticated Ele.me session or wait while the user logs in themselves
- set or confirm the delivery address
- search nearby merchants that satisfy the request
- compare real payable totals after visible coupons, red packets, threshold discounts, delivery fee, and packaging fee
- build the best basket under the user's requirements and budget
- add the selected items to cart
- tell the user the cart is ready and they should review and pay

Do not stop at generic recommendations if the user asked to place the basket.

## Workflow

1. Normalize the request.
   - Extract item, address, must-have constraints, avoid rules, budget, and urgency.
   - Convert vague language into actionable search terms and merchant filters.

2. Access the authenticated session with consent.
   - If Ele.me is already signed in, continue.
   - If Ele.me is not signed in, open the official login surface and pause while the user logs in themselves.
   - Do not ask for, copy, store, or type login secrets or other authentication material on the user's behalf.
   - Never read out-of-band messages, inboxes, or notifications automatically.

3. Set location and account context.
   - Confirm the delivery address or map pin before comparing merchants.
   - If multiple saved addresses exist, confirm which one should drive search and delivery pricing.
   - Use the address that best matches the user's stated delivery location.

4. Search and shortlist nearby merchants.
   - Search the requested item using direct terms and useful synonyms.
   - Favor merchants that can actually deliver to the confirmed address.
   - Reject obvious poor fits on merchant quality, ETA, or impossible pricing.

5. Build candidate carts.
   - Compare exact items, quantities, add-ons, and substitutes against the user's requirements.
   - If an exact match is unavailable, identify the closest acceptable substitute and ask before adding it.
   - For multi-item requests, optimize the whole basket instead of each item in isolation.

6. Compare real checkout value.
   - Count food subtotal, visible coupons or red packets, store full-reduction offers, delivery fee, packaging fee, and any service fee shown in the UI.
   - Prefer discounts that apply naturally to the basket the user already wants.
   - If a small useful add-on unlocks a better threshold, it can be acceptable.
   - If the discount only works by padding the basket with low-value filler, call that out and avoid it.

7. Choose the winning basket.
   - Respect hard constraints before optimizing savings.
   - Stay within budget when possible.
   - If nothing fits, present the closest fallback baskets such as cheapest acceptable and best-value stretch.
   - Use merchant quality and ETA as tie-breakers when price differences are small.

8. Add to cart and hand off.
   - With explicit consent, add the chosen items to cart and select the best visible discount path.
   - Stop at cart or pre-payment review.
   - Tell the user exactly what is in the cart, the estimated payable total, the expected arrival time, and why this route won.

## Decision Rules

### Budget And Basket Fit

- Hard requirements beat discounts.
- If the budget is tight, keep the basket focused on the core item instead of chasing promo thresholds.
- If the user specifies merchant, brand, or taste preferences, honor them unless they make the request impossible.

### Real Savings

- Count savings only after threshold, delivery fee, packaging fee, and visible service charges.
- Prefer account-visible or automatically applicable coupons that genuinely lower the final payable amount.
- If the final price edge is tiny, let delivery quality and merchant trust decide.

### Merchant And Delivery Quality

Prefer:
- merchants with believable recent reviews
- stores with stable ETA and lower complaint risk
- offers that still make sense without gaming the cart
- baskets with lower downside if the order disappoints

Avoid:
- suspiciously deep discounts with weak store credibility
- high-fee baskets pretending to be low-price
- poor review patterns around delays, wrong items, spills, or refund arguments

### Search And Substitution

- If the exact item is missing nearby, offer the nearest acceptable substitute before adding it.
- For natural-language requests, translate soft intent into search heuristics instead of asking the user to restate everything in platform keywords.
- If the user asks for multiple items, optimize the basket as one delivery decision.

## Output

Use this structure unless the user asks for something shorter:

### Cart Ready Status
Say whether the cart has been prepared and what still blocks completion.

### Selected Merchant And Basket
List the chosen merchant, items, key constraints satisfied, and any approved substitutions.

### Savings Summary
Summarize the coupon, red-packet, threshold, and fee logic that made this cart the best one.

### Payment Handoff
Tell the user to review address, delivery notes, coupon selection, and then pay in the cart.

## Safety Boundary

Allowed with explicit user consent:
- using an already authenticated Ele.me session after the user logs in themselves
- opening the official Ele.me login page and waiting for the user to complete authentication
- choosing or confirming the delivery address
- reading account-visible coupon, red-packet, and cart state
- adding or removing cart items
- selecting the best visible discount path
- preparing checkout for the user's review

Not allowed:
- asking the user to paste login secrets into chat for account access
- typing or handling account authentication material on the user's behalf
- storing addresses or account data outside the session
- reading out-of-band messages, email, or notifications automatically
- changing payment methods or account security settings
- submitting payment
- placing irreversible orders without the user taking the final payment step
- inventing availability, ETA, or discount data that the UI does not show
