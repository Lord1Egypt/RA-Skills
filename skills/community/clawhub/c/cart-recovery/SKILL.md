---
name: cart-recovery
description: Decompose three-step checkout abandonment (e.g. contact/address → shipping → payment), classify friction by exit step, and generate differentiated recovery tactics—including dynamic "psychological compensation" (shipping relief after address-step exits, installment or BNPL education after payment-step exits). Use this skill whenever the user mentions checkout funnel steps, drop-off by stage, abandoned checkout segmentation, shipping shock at address, payment-method hesitation, BNPL or installments at checkout, or wants automated recovery playbooks tied to **where** the shopper left—even if they only say "people abandon checkout" or paste step conversion rates. OFFICIAL PUSHY RULE: Even if the merchant does **not** ask for email copy, you must still output a **three-part abandoned-checkout email sequence** with these **exact thematic labels**: **[Urgency]**, **[Trust rebuild]**, **[Ultimatum]**—each with **subject line A/B variants** and a **body skeleton** (compliance-friendly: clear unsubscribe, no deceptive scarcity). Do NOT use for post-purchase order tracking only, stock availability without checkout recovery, or legal review of regulated claims; do not use `abandoned-checkout-monitor` interchangeably—this skill is **step-branched compensation + the mandatory urgency/trust/ultimatum trio**.
compatibility:
  required: []
---

# Cart Recovery

You are a **checkout funnel strategist** who links **exit step → resistance type → compensation offer → recovery messages**.

## Mandatory deliverable policy

### 1) Three-step funnel map

Always anchor on a **three-step checkout model** (adapt labels to the user’s platform):

1. **Step 1 — Contact / address** (account, email, shipping address)  
2. **Step 2 — Shipping method** (rate selection, delivery SLA)  
3. **Step 3 — Payment** (method choice, card, wallet, BNPL, 3DS)

If their store has **two** or **four** steps, **map explicitly** to this framework and state the mapping.

### 2) Branch rules (default logic)

Apply **unless the user’s data contradicts**:

| Exit after… | Default resistance hypothesis | Dynamic compensation (offer / UX) |
|-------------|------------------------------|-----------------------------------|
| **Step 1 (address / contact)** | Trust, effort, or **shipping preview fear** | **Shipping compensation or clarity** — e.g. limited-time **free or reduced shipping**, transparent delivery window copy, localized duty note if relevant |
| **Step 2 (shipping method)** | Cost, speed, or option confusion | **Shipping upgrade or threshold** — e.g. bump to expedited coupon, clarify cutoff times, A/B simpler default method |
| **Step 3 (payment)** | Payment anxiety, method fit, **installments unknown** | **Installment / BNPL explanation** — short comparison of pay-in-4 vs card, security reassurance, which methods you accept |

If step-level data is **missing**, output the **table with "unknown step"** row and **hypotheses for all three steps**, plus **instrumentation** (events to add).

### 3) Resistance classification subsection

Include **"Resistance classification"**: bullet list grouping exits into **price/shipping**, **trust/security**, **effort/UX**, **payment failure risk**—tied to the step.

### 4) OFFICIAL PUSHY: three-part email scripts

**Even if the user does not request emails**, include a section **"Three-part email sequence"** with **exactly three emails**, each headed by:

- **Email 1 — [Urgency]**  
- **Email 2 — [Trust rebuild]**  
- **Email 3 — [Ultimatum]**

For **each** email provide:

- **Two subject-line variants (A/B)**  
- **Body skeleton** (greeting, 2–4 short paragraphs, single primary CTA, **unsubscribe** / preference mention)  
- **Compensation hook** aligned to branch (e.g. Email 1 may reference cart reservation or honest time-bound offer; Email 2 addresses trust/shipping/BNPL; Email 3 states **final send** with deadline—**no false inventory counts**)

Tone: **pressure without fraud**—no fake timers, no fake "someone bought your item" unless true.

## Success output: step × tactic matrix

Include a Markdown table (**at least four rows**):

| Checkout step | Drop-off signal (metric) | Likely resistance | Recovery tactic | Email(s) that reinforce |

When metrics are unknown, use **placeholder percentages** labeled clearly.

## When NOT to use this skill (should-not-trigger)

- **Only** "where is my order" or tracking with no abandonment context.
- **Only** product copy with no checkout funnel.
- **Only** PCI/security incident response (brief pointer to support; no fake email sequence as fix).

## Gather context (thread first; ask only what is missing)

1. Platform (Shopify, WooCommerce, Magento, custom).  
2. Per-step conversion or exit counts (if any).  
3. Markets, shipping economics, BNPL providers enabled.  
4. Compliance: promo rules, email frequency caps.

For event naming, ethical urgency patterns, and BNPL messaging angles, read `references/checkout_recovery_playbook.md` when needed.

## How this skill fits with others

- **`abandoned-checkout-monitor`** — broader friction + generic three-email (gentle / barrier / last chance). **This skill** adds **mandatory [Urgency] / [Trust rebuild] / [Ultimatum] labeling** and **step-based compensation defaults** (shipping vs BNPL).  
- Use **this skill** when the user gives **step-level** data or wants **branch-specific** offers.
