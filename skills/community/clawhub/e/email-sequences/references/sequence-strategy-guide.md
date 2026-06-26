# Email Sequence Strategy Guide — Timing, Segmentation, and Architecture

## Overview

Email sequence architecture determines whether automation feels helpful or annoying. The decisions made before writing a single word — who receives this sequence, when each email sends, and what event exits the subscriber — have more impact on performance than copy quality alone. This guide covers the strategic frameworks for each ecommerce sequence type.

---

## Abandoned Cart Sequences

### Timing Benchmarks

| Email | Send time | Rationale |
|---|---|---|
| Email 1 | 1 hour post-abandonment | Catches still-deciding shoppers while intent is fresh; no offer preserves margin |
| Email 2 | 6–8 hours post-abandonment | Secondary reminder after work/day distractions; optional low-stock urgency |
| Email 3 | 22–24 hours post-abandonment | Last chance with incentive if needed; matches a full purchase consideration cycle |

**Why not sooner?** Emails sent within 15–30 minutes feel intrusive and increase opt-outs. A 1-hour delay converts nearly as well as immediate sends with significantly lower complaint rates.

**Why not later?** Beyond 48 hours, purchase intent for most product categories drops significantly. A 3-day sequence extending to 72 hours works for high-AOV items (furniture, jewelry) but not for impulse categories.

### Discount Logic

The most common mistake in abandoned cart sequences is offering a discount in Email 1. This:
- Trains subscribers to abandon carts intentionally to wait for coupons
- Reduces perceived product value
- Conditions repeat customers to expect discounts on every order

**Recommended escalation:**
- Email 1: No offer — product + social proof
- Email 2: No offer — urgency (low stock, session expiry) or additional social proof
- Email 3: Offer only if cart value justifies margin cost; set 24-hour expiry on discount

**High-AOV exception (>$200 avg cart):** Consider offering free shipping (lower cost to you) in Email 2 rather than a percentage discount.

### Segmentation Variants

| Segment | Sequence adjustment |
|---|---|
| First-time visitor | Email 1 adds brand trust signals (return policy, reviews) |
| Repeat customer | Email 1 skips trust signals; lead with "welcome back" |
| VIP / high LTV | Email 2 can offer larger incentive (loyalty points or free gift) |
| Wholesale / B2B | Different copy; consider phone follow-up instead of Email 3 |

---

## Post-Purchase Sequences

### New Customer Onboarding Architecture

Post-purchase is the highest-leverage sequence in ecommerce — it has the highest open rates (60–70% for order confirmations) and determines whether a one-time buyer becomes a repeat customer.

**3-email new customer onboarding structure:**

| Email | Timing | Goal |
|---|---|---|
| Email 1 | Immediately on order | Confirm order, set delivery expectations, introduce brand |
| Email 2 | 2–3 days (pre-delivery) | Product education, usage tips, anticipation building |
| Email 3 | 7 days (post-delivery) | Review request, community invitation, cross-sell |

**Key principle:** Never put promotional content in the order confirmation email. It is transactional and requires only implied consent. Adding "while you wait, check out our sale" converts a transactional email into a promotional one — separate them.

### Review Request Timing

| Product type | Optimal review request timing |
|---|---|
| Consumable (skincare, food, supplements) | 7–10 days post-delivery |
| Physical goods (clothing, home goods) | 5–7 days post-delivery |
| Digital / software | 3–5 days post-activation |
| High-consideration (furniture, appliances) | 14–21 days post-delivery |

Send review requests too early (day 1–2) and the customer has not formed an opinion. Send too late and the window of goodwill has passed.

### Cross-Sell Logic

Post-purchase cross-sell should be category-adjacent, not random catalog browsing. Examples:
- Bought coffee beans → suggest grinder, filters, or complementary roast
- Bought running shoes → suggest insoles, socks, or hydration
- Bought a gift → suggest gift wrapping add-on for future orders or gift cards

Do not cross-sell competing products (a customer who bought Product A should not receive an ad for Product B that serves the same function).

---

## Win-Back Campaigns

### Lapsed Threshold by Category

| Category | Define "lapsed" as |
|---|---|
| Consumable (30–60 day reorder cycle) | No purchase in 90 days |
| Fashion / apparel (seasonal) | No purchase in 180 days |
| High-consideration / furniture | No purchase in 365 days |
| Subscription boxes | Churned for 60 days |

Do not run win-back campaigns on subscribers who have been inactive for only 30–45 days. That is normal purchase cadence variation, not lapse.

### Win-Back Sequence Architecture

| Email | Timing | Angle |
|---|---|---|
| Email 1 | Day 0 of win-back trigger | "Here's what you've missed" — new arrivals or improvements |
| Email 2 | Day 7 (no open) | Soft offer — loyalty points or small discount |
| Email 3 | Day 14 (no open) | Final offer + "stay or go" opt-down option |

**Email 3 best practice:** Offer an opt-down (reduce email frequency) in addition to an unsubscribe option. Some subscribers want fewer emails, not zero emails. Capturing opt-downs preserves list size while respecting preferences.

**Sunset policy:** If a subscriber does not open any of the 3 win-back emails, suppress them from future marketing sends. Continuing to send to confirmed non-engagers damages your sender reputation with every ISP.

---

## Welcome Sequences

### Architecture for Ecommerce Welcome Series

| Email | Timing | Goal |
|---|---|---|
| Email 1 | Immediately on opt-in | Welcome + deliver incentive (if offered at opt-in) |
| Email 2 | Day 2 | Brand story + bestsellers |
| Email 3 | Day 5 | Social proof + community |
| Email 4 | Day 8 (no purchase) | Soft nudge with urgency on their welcome offer |

**Welcome offer timing:** If you offered a discount at opt-in (e.g., "sign up for 15% off"), deliver it immediately in Email 1. Delaying it — even by one hour — reduces conversion significantly.

**Transition to main list:** After the welcome series ends, move subscribers into your standard promotional cadence. Do not leave them in limbo between segments.

---

## Seasonal Promotion Sequences

### Segmentation Matrix for Seasonal Sends

| Segment | Messaging angle |
|---|---|
| Active buyers (purchase in 90 days) | VIP early access framing; no discount needed |
| Engaged non-buyers (opens/clicks, no purchase) | Category-specific offer matching browse behavior |
| Lapsed buyers (90–365 days) | "Come back for [season]" + incentive |
| New subscribers | Brand-appropriate seasonal intro; lighter selling |

**Never send one seasonal email to all segments.** The messaging that converts a loyal VIP ("exclusive early access") is different from what converts a deal-seeker ("biggest sale of the year").

### Seasonal Send Cadence

| Phase | Timing | Content |
|---|---|---|
| Teaser | 7–10 days before event | Build anticipation; no full offer reveal |
| Launch | Sale start day | Full offer + urgency |
| Mid-sale | 2–3 days in (for 7+ day sales) | New arrivals, bestsellers, social proof |
| Last chance | 24 hours before end | Explicit deadline; strongest urgency |
| Post-sale | 1–2 days after | Full-price "if you missed it" positioning or waitlist |

---

## Suppression Framework

Every sequence must define suppression conditions before any copy is written. Unconfigured suppression is the primary driver of subscriber complaints and spam folder placement.

### Minimum Required Suppressions

| Condition | Action |
|---|---|
| Purchase during sequence | Exit all remaining emails in sequence immediately |
| Unsubscribe / opt-out | Exit sequence; add to permanent suppression list; never re-add without explicit re-consent |
| Hard bounce | Remove from all lists permanently |
| Spam complaint | Remove from all lists; flag for review |
| Currently in another promotional sequence | Apply frequency cap — suppress overlap |

### Frequency Caps by Sequence Type

| Sequence type | Recommended frequency cap |
|---|---|
| Abandoned cart | 1 active cart sequence per subscriber at a time |
| Post-purchase onboarding | Do not send additional promotional emails for 3–5 days |
| Win-back | 1 win-back sequence per quarter maximum |
| Welcome | Suppress from broadcast emails until welcome series ends |
| Seasonal | Maximum 4–6 promotional campaign emails per month total |
