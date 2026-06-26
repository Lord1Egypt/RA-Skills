---
name: browser-e-commerce
description: "Browser shopping assistant. Input a product link or keyword; compare browser-visible prices, seller type, reviews, promotions, delivery/return signals, and after-sales risk across shopping sites, then output buy/wait/switch-platform advice. Safe boundary: no login, no order submission, no checkout, and no payment."
---

# Browser E-Commerce Assistant

Use this skill when the user wants browser-visible shopping research across ecommerce sites without account access.

## Workflow

1. Clarify product, budget, required specs, delivery urgency, and risk tolerance.
2. Search or inspect user-provided links using visible page information.
3. Compare candidates by visible price, seller trust, reviews, delivery, return policy, promotions, and hidden caveats.
4. Return one action: buy, wait, compare another platform, or avoid.

## Safety Boundaries

- Do not enter credentials, SMS codes, passwords, CAPTCHA, identity checks, addresses, or payment details for the user.
- Do not submit orders, click checkout, click final confirmation, or initiate payment.
- Use browser-visible or user-provided information only.
- Final price, stock, delivery, coupons, and after-sales terms must be rechecked by the user before purchase.

## Example Prompts

1. `Compare this product link with the same item on JD and PDD.`
2. `Search for a reliable 27-inch monitor under 1500 RMB and tell me what to avoid.`
3. `Check whether this cheap listing looks risky based on visible reviews and seller signals.`
4. `Find the best place to buy this appliance and explain the tradeoffs.`
5. `Summarize visible promotion conditions before I decide manually.`
