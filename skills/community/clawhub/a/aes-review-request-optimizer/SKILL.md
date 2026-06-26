---
name: Review Request Optimizer
description: Optimize review request timing, channel, and messaging to maximize review collection rates and star ratings. Use when an ecommerce seller wants to lift review velocity, improve star average, or fix a review program that is producing low response rates or compliance risk on Amazon, Shopify, eBay, or Etsy.
---

# Review Request Optimizer

Customer reviews are the single most influential conversion factor on marketplace product pages, yet most sellers either never ask for reviews or ask at the wrong time through the wrong channel with generic messaging. This skill designs a data-informed review request strategy that identifies the optimal moment to ask each customer segment for a review, selects the highest-performing channel for each request, and crafts messaging that encourages detailed, authentic feedback while staying compliant with platform review policies.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Request timing | Triggered by experience milestone (delivered + first-use window) per category, with separate timing for consumables vs durables | Fixed 7-14 days after delivery for all categories | Same-day or random ad-hoc requests |
| Request channel | Multi-touch: in-package insert + email + post-delivery SMS, sequenced to avoid overlap | Single email at delivery + 7 | A single platform-default request only |
| Segmentation | Split by first-time vs repeat buyer, AOV band, category, and SKU complexity | Split by repeat-buyer status only | One message for all customers |
| Messaging tone | Specific, low-pressure, asks one question, references the product purchased and the experience milestone | Generic "leave us a review" | "Please leave 5 stars" or any direct rating ask |
| Compliance posture | Platform-native request tools only; no incentives, no rating direction, no review gating | Some platform-tools + permitted insert language | Incentivized reviews, rating direction, or review filtering |
| Negative-feedback handling | Pre-emptive support route for unhappy buyers with separate, supportive language and a service offer | Generic "let us know" line at end of message | No alternative path; complaints land as 1-star reviews |
| Cadence | One reminder after 5-7 days if no response, then stop | Two reminders | Three or more reminders / weekly nagging |

## Problems this skill solves

This skill is for sellers who want more, better, faster reviews without crossing compliance lines:

1. A seller with a 2% review rate wants to understand whether to ask sooner, ask differently, or add a new channel.
2. A brand with 30 reviews vs a competitor with 500 needs a plan to close the gap in 90 days without buying reviews.
3. A new launch needs a sequenced program that generates the first 25 reviews before paid traffic ramps up.
4. A seller is getting reviews but stuck at 4.2 stars and needs to investigate timing, messaging, and SKU-level issues that suppress ratings.
5. A team has been warned by a platform about gated or incentivized reviews and needs a compliant replacement program.
6. A seasonal product needs a request sequence that fits short usage windows (e.g., Christmas decor, swimwear).
7. A subscription brand needs a separate program for first delivery vs ongoing renewals.

## Workflow

### Step 1: Audit the current state
Pull current review rate by SKU, by channel, by source (organic vs solicited), by 30 / 60 / 90 day window. Identify SKUs with no reviews, SKUs with declining stars, and SKUs with abnormally short or long lead time from purchase to review. See `references/audit-checklist.md`.

### Step 2: Map the customer experience timeline per category
Define the milestone moments: purchase, ship, deliver, first use, expected satisfaction, expected re-use. Categories vary dramatically — a t-shirt is judged in days, a mattress in weeks. Set the request trigger at the moment the customer has formed an opinion but before novelty fades.

### Step 3: Choose channels and sequence them
Decide which channels apply: in-package insert (always free), platform-native request (Amazon Request a Review, Shopify post-purchase, etc.), branded email, SMS, post-delivery WhatsApp. Sequence them so no customer receives more than two asks in a 7-day window. See `references/channel-playbook.md`.

### Step 4: Segment and personalize
At minimum split by first-time vs repeat buyer, AOV band, and category. Repeat buyers get a different opener ("thanks for coming back"). High-AOV buyers get a more individual touch. New-launch SKUs get a "you're an early customer" framing.

### Step 5: Write compliant messaging
Use the templates in `references/messaging-templates.md`. Never ask for a rating, never offer compensation tied to reviews, never review-gate. Reference the product by name, reference the experience milestone, ask one open question, and link to the platform-native review tool.

### Step 6: Add a negative-feedback safety route
Include a separate, supportive line that invites dissatisfied buyers to contact support before reviewing. This is not gating — it's good service. The link goes to support, not to a review filter.

### Step 7: Measure and iterate
Track review rate, response time from request, star average, and review length per cohort. A/B test timing first, then channel mix, then messaging. Refresh every 60 days.

## Worked Example 1: DTC kitchenware brand on Shopify + Amazon

**Inputs:** 800 orders/month, current review rate 1.8% on Amazon, 0.7% on Shopify, average rating 4.4. Two flagship SKUs (knife block, cast iron pan). Returns rate 5%.

**Audit findings:** Amazon program relies only on automated default tool. Shopify has no program at all. No in-package insert. Returns spike at day 14 suggests buyers form opinion ~day 10.

**New program:**
- In-package insert with QR code to a review landing page that explains how to leave reviews on whichever platform they bought from. No incentive offered.
- Amazon: Request a Review tool fired at day 11 post-delivery (window: day 11 ± 1 to stay inside Amazon's allowed window). No follow-up.
- Shopify: branded email at day 10, reminder at day 17 if no review, then stop.
- Negative path: insert says "if anything's off, email care@brand.com first."
- Segmentation: first-time buyer email mentions the unboxing; repeat buyer email says "your second knife block — let other cooks know how it's held up."

**Expected lift:** Review rate to 3.5-4.5% within 90 days. Star average held steady or +0.1 due to negative-path interception.

## Worked Example 2: Subscription skincare brand

**Inputs:** Subscription serum, 6-week supply per shipment. Goal: reviews of the initial product (not the brand). Current program asks for a review at day 30 — buyers have only used it twice.

**Audit findings:** Day-30 timing is too early for skincare results. Reviews are noncommittal. No separate program for renewals.

**New program:**
- First-shipment cohort: email at day 42 ("six weeks in — what are you seeing?"). Skin care benefits typically show by week 5-6.
- Renewal cohort: separate quarterly email celebrating consistency, asking "what's changed since your last review?"
- Channels: email primary; SMS reminder at day 49 if no review.
- Messaging asks an open question about a visible benefit ("How does your skin look this morning?") rather than star rating.
- Negative-path: pre-renewal pause + dermatologist Q&A link.

**Expected lift:** Review rate to 8-12% (subscription audiences over-index); review length up; first-week renewal churn reduced because unhappy buyers are routed to support.

## Common Mistakes

1. **Asking before the experience is formed.** A request at day 3 generates shallow or absent reviews.
2. **Asking too late.** After day 30 in fast-cycle categories, novelty has faded and reviews drop.
3. **Bundling all SKUs into one timing.** A consumable and a durable need different triggers.
4. **Using the same message for first-time and repeat buyers.** Repeat buyers know your brand; the opener should reflect that.
5. **Rating direction language.** "Help us hit 5 stars" or "if you loved it, leave 5 stars" violates most marketplace policies and skews data.
6. **Incentive entanglement.** Offering anything tied to reviews is a violation on Amazon and most marketplaces.
7. **Review gating.** Filtering unhappy buyers away from the review process is a policy violation; offering a support channel is not.
8. **Over-asking.** More than two requests inside two weeks irritates customers and depresses overall response.
9. **No SKU-level review-rate tracking.** Without per-SKU rates you can't tell whether messaging or product is the issue.
10. **Ignoring negative reviews after they post.** Failing to respond publicly to a 1-star is itself a signal to future shoppers.

## Resources

- `references/audit-checklist.md` — Full audit list to characterize current review performance.
- `references/channel-playbook.md` — Channel-by-channel rules including platform compliance notes.
- `references/messaging-templates.md` — Compliant first-buyer, repeat-buyer, and renewal templates.
- `references/output-template.md` — Program plan template with timeline, channels, and metrics.
- `assets/quality-checklist.md` — 40-point checklist to validate the program before launch.
