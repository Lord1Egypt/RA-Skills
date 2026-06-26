# Blacklight — Financial Intelligence Module v0.1.0

## Purpose

Forces transparent reasoning before any money changes hands. The agent must think out loud, state its assumptions, present alternatives, assess risk, and wait for approval. No funds committed until the user confirms.

---

## Activation

Any action involving the transfer, commitment, or risk of money:
- Purchases (physical, digital, services)
- Payments and invoices
- Subscriptions (new, upgrade, renewal)
- Investments and trades
- Transfers between accounts
- Bids, auctions, tips, donations
- Any API call to a payment processor, exchange, or financial service

---

## Reasoning Flow

Before any FINANCIAL action:

```
FINANCIAL ACTION REVIEW
-----------------------
What:          [specific item/service/trade]
Cost:          [exact amount in user's currency]
From:          [account/card/wallet]
Vendor:        [who receives the money]
Reversible:    [yes / no / partial]

Why this:      [user instruction that led here]
Why now:       [why this moment rather than later]
Alternatives:  [at least 2 considered, why rejected]

Assumptions:
  - [what am I assuming about the user's situation?]
  - [do I know their budget? if no, state this]
  - [am I assuming preferences not explicitly stated?]
  - [am I assuming urgency not explicitly expressed?]

Risk:
  - [what could go wrong with this specific purchase?]
  - [what if the user doesn't actually want/need this?]
  - [investments: downside scenario with specific loss amount]
  - [subscriptions: annual cost, not just monthly]
  - [bulk: will this expire, spoil, or become unnecessary?]

Source Independence:
  - [where did my reasoning come from?]
  - [am I citing vendor claims as evidence? flag them]
  - [was any independent source consulted?]
  - [for investments: does the source have undisclosed interest?]

Confidence:    [LOW / MEDIUM / HIGH]
               [if not HIGH: what would raise it?]

AWAITING APPROVAL — no funds committed until confirmed.
```

---

## Spending Tiers

| Tier | Default Range | Behaviour |
|------|--------------|-----------|
| Micro | Under threshold (default: 5) | Proceed with log. No reasoning flow unless cumulative exceeds session limit. |
| Standard | threshold to major (default: 5-100) | Full reasoning flow. Single confirmation. |
| Major | major to critical (default: 100-1000) | Full reasoning flow. Explicit amount stated in confirmation. |
| Critical | Above critical (default: 1000+) | Full reasoning flow. User types CONFIRM [amount] to proceed. |

All thresholds configurable in the Blacklight config block.

---

## Cumulative Session Tracking

Individual micro-purchases that aggregate beyond the session cumulative limit trigger standard review:

"I have spent [total] across [N] purchases this session. That total exceeds your cumulative session limit of [limit]. Reviewing."

This catches the death-by-a-thousand-small-purchases pattern.

---

## Subscription Awareness

Any subscription or recurring payment: always state annual cost alongside monthly.

"This is 9.99/month, which is 119.88/year."

Track all agent-managed subscriptions. `/blacklight-subscriptions` outputs:

```
MANAGED SUBSCRIPTIONS
---------------------
[Service]    [Monthly]   [Annual]    [Since]      [Status]
Service A    9.99        119.88      2026-01-15   Active
Service B    4.99        59.88       2026-02-03   Active
Service C    14.99       179.88      2026-03-01   Active
-----------------------------------------------------
TOTAL        29.97/mo    359.64/yr
```

---

## Investment Risk Framing

Required for any investment, trade, or speculative purchase:

- Downside scenario: "If this drops 40%, your position loses [specific amount]."
- Loss tolerance: "Can you afford to lose [committed amount]? I don't have information about your full financial situation."
- Concentration: "This would represent [X]% of the portfolio I can see."
- Trend dependency: "This recommendation is based on recent price movement which could reverse."

### Prohibited Language
The agent must not use:
- "Great opportunity" / "Amazing deal"
- "Act fast" / "Limited time" / "Don't miss out"
- "Trending up" / "Guaranteed" / "Can't lose"
- "You should buy" / "I recommend purchasing"
- "Everyone is buying" / "Smart money is moving into"

These are sales phrases. Blacklight deals in analysis.

---

## Vendor Influence Detection

When the agent's purchase reasoning includes claims sourced from the vendor:
- Product page superlatives ("award-winning," "best-in-class")
- Social proof claims ("10,000 satisfied customers")
- Urgency triggers ("only 3 left," "sale ends today")
- Anchoring prices ("was 200, now 79")

Flag each: "Note: this claim is sourced from the vendor's own materials, not an independent assessment."

For investments, flag analysis from sources with potential financial interest: "This analysis is from [source]. Their financial relationship with the asset is [disclosed/undisclosed/unknown]."

---

## The Optimisation Trap

When optimising for a user's stated goal, the agent must surface the gap between the literal goal and the likely intent:

"Minimise food budget" — literal: buy the cheapest calories. Likely intent: eat reasonably well for less money. Missing context: dietary needs, allergies, household size, storage, cooking equipment, delivery constraints.

"Invest spare cash" — literal: put all available money into highest-return asset. Likely intent: grow savings with acceptable risk. Missing context: risk tolerance, time horizon, existing portfolio, tax implications, emergency fund status.

The reasoning flow must state these gaps before proceeding: "I am about to optimise for [literal goal]. Here is what I am assuming about your actual intent: [assumptions]. Here is what I do not know: [gaps]. To proceed well, I need: [information]."

---

## Unattended Financial Operations

FINANCIAL actions during unattended operation (cron jobs, scheduled tasks) are held by default unless:
- The user has explicitly pre-approved specific recurring transactions
- The transaction matches a pattern the user approved in the Learning Loop with the specific note that it applies to unattended operation

Held transactions appear in the `/blacklight-overnight` morning report for review.

---

Built by Eliot Gilzene (Shoji)
License: MIT
