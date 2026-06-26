---
name: Email Sequences
description: Create segmented email sequences for abandoned carts, post-purchase follow-up, win-back campaigns, and seasonal promotions for online stores.
---

# Email Sequences

Ecommerce email sequences are the highest-ROI channel in most stores' marketing stack — but most brands send undifferentiated blasts that treat a first-time buyer and a lapsed VIP the same way. Email Sequences generates complete, segmented email flows with subject lines, preview text, body copy, CTAs, send timing, and suppression logic tailored to each campaign type and ESP.

## Solves

1. **Generic copy that ignores lifecycle stage** — sending the same welcome email to a wholesale buyer and a first-time gift shopper destroys relevance and trains subscribers to ignore your emails
2. **Abandoned cart sequences that annoy instead of convert** — sequences with no discount logic, wrong send cadence, or missing suppression that keep emailing after purchase
3. **Post-purchase flows that leave revenue on the table** — order confirmation emails with no cross-sell, no review request, and no onboarding that fail to build the second purchase
4. **Win-back campaigns that just say "we miss you"** — generic re-engagement copy with no segment-specific angle and no escalating offer logic
5. **Seasonal promotions with no segmentation** — blasting the entire list with the same sale email when VIPs, deal-seekers, and new subscribers all need different messaging
6. **Missing suppression logic** — sending cart abandonment after purchase, or win-back to someone who bought last week, driving opt-outs and deliverability damage
7. **Subject line and preview text mismatches** — weak subject lines that don't match preview text, no A/B test coverage, and no curiosity or urgency hooks calibrated to mobile inboxes

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| **Abandoned cart — Email 1 timing** | 1 hour post-abandonment, reminder only, no discount | 2–3 hours, soft urgency | Same-day discount offer in Email 1 (trains discount-seeking) |
| **Discount escalation logic** | Email 1 no offer → Email 2 soft offer (10%) → Email 3 stronger (15%) or FOMO | Email 2 only with incentive | Discount in every email or discount in Email 1 only |
| **Subject line structure** | Behavior-triggered or benefit-first; under 50 characters | Generic product mention | Brand name first with no hook; over 60 characters |
| **Preview text** | Extends subject line with new information; 85–100 characters | Restates subject | Blank (inbox shows body text or "View in browser") |
| **Segmentation** | Separate flows for new vs. repeat vs. VIP subscribers | Single flow with conditional blocks | No segmentation — one flow for all subscribers |
| **Post-purchase Email 1 timing** | Immediately triggered by order confirmation | Within 30 minutes | Hours after purchase (feels disconnected) |
| **Win-back angle** | Specific re-engagement hook (new arrival, exclusive, or "what changed") | Generic "we miss you" + offer | Guilt-based copy or no offer |
| **Suppression logic** | Purchase suppresses cart sequence; opt-out suppresses all; frequency cap per segment | Purchase suppression only | No suppression — sends regardless of purchase or engagement status |

## Workflow

### Step 1 — Gather campaign inputs
Before writing a single subject line, collect: campaign type (abandoned cart / post-purchase / win-back / welcome / seasonal / loyalty), ESP platform, product category, brand voice, offer details (if any), and target segment. Missing inputs produce generic copy that requires full rewrites.

### Step 2 — Map the sequence structure
Define the number of emails, send timing for each, and the behavioral trigger or delay. For multi-email sequences, map suppression conditions at each step. For seasonal campaigns, confirm send window and list segment before drafting.

### Step 3 — Draft subject lines and preview text first
Write subject line + preview text pairs before body copy. Subject line and preview text together form the 90-character "envelope" that determines open rate — weak envelope copy makes strong body copy irrelevant. Aim for under 50 characters for subject lines on mobile.

### Step 4 — Write body copy for each email
Follow the structure: hook (first sentence makes the reason to open obvious), context (short), offer or action (specific, not vague), CTA (single, present-tense verb). Keep emails under 200 words for promotional sequences; post-purchase and onboarding emails may run longer if value justifies it.

### Step 5 — Apply segmentation and personalization flags
Note where merge tags should be used (first name, product name, cart contents, order number). Flag any conditional content blocks (e.g., "show this block to VIP segment only"). Identify which segments should receive this sequence vs. be suppressed.

### Step 6 — Specify suppression and exit logic
For every sequence, define: what event exits the subscriber early (purchase, reply, opt-out), frequency cap interactions with other active sequences, and re-entry conditions. Unclear suppression logic is the most common cause of subscriber complaints.

### Step 7 — Deliver complete output package
Present the full sequence with: sequence overview table, individual email blocks (subject, preview, body, CTA, timing), suppression logic summary, and platform-specific setup notes. For sequences with A/B tests, label variants and state the variable being tested.

## Examples

### Example 1 — 3-email abandoned cart sequence

**Inputs:**
- Campaign type: Abandoned cart
- Product: Mid-range skincare (avg order $65)
- Platform: Klaviyo
- Brand voice: Warm, slightly witty, not pushy
- Offer: 10% off code COMEBACK10, valid 24 hours, available for Email 3 only
- Segment: All subscribers with express consent

**Sequence Overview:**

| Email | Timing | Angle | Offer |
|---|---|---|---|
| Email 1 | 1 hour post-abandonment | Helpful reminder — your cart is saved | None |
| Email 2 | 6 hours post-abandonment | Social proof / urgency (low stock) | None |
| Email 3 | 22 hours post-abandonment | Final nudge + discount expires midnight | 10% off, expires midnight |

**Suppression:** Stop sequence immediately on purchase. Stop on opt-out. Do not re-enter for 14 days after sequence completes without purchase.

---

**Email 1 of 3**

**Subject:** Your cart is still here (and so is your skin)
**Preview text:** You left some good stuff behind — no pressure, just saving it for you.

Hi [First Name],

Looks like life got in the way. Your cart is still here with everything you picked — we'll hold it for you.

No rush. If you want to pick up where you left off:

[View your cart →]

— [Brand Name] Team

---

**Email 2 of 3**

**Subject:** A few people have been eyeing your cart
**Preview text:** We can't hold it forever — here's what's in yours.

Hi [First Name],

Just a heads up: a couple of items in your cart are running low. We can't guarantee they'll still be available tomorrow.

Your cart is still saved, but popular items go fast.

[Grab it before it's gone →]

---

**Email 3 of 3**

**Subject:** Last call — 10% off, expires midnight
**Preview text:** COMEBACK10 takes 10% off your cart. Offer ends at midnight tonight.

Hi [First Name],

This is your last nudge, we promise. Your cart is still waiting, and today only, use COMEBACK10 for 10% off your order.

**COMEBACK10 — 10% off, expires midnight**

[Claim your discount →]

After midnight, this offer disappears. Your items may too.

---

**Klaviyo setup notes:**
- Trigger: "Added to cart" event → "Checkout started" event not completed within 60 minutes
- Configure active on-site suppression to prevent Email 1 firing while user is still browsing
- Set "Placed Order" metric as flow exit condition for all 3 emails
- Frequency filter: Do not send if subscriber received any Klaviyo flow or campaign in past 12 hours

---

### Example 2 — Post-purchase onboarding sequence (new customer)

**Inputs:**
- Campaign type: Post-purchase (new customer onboarding)
- Product: Specialty coffee subscription
- Platform: Mailchimp
- Brand voice: Enthusiastic but educational
- Segment: First-time buyers only

**Sequence Overview:**

| Email | Timing | Angle |
|---|---|---|
| Email 1 | Immediately on order confirmation | Welcome + what to expect |
| Email 2 | Day 3 (before first delivery) | Product education + brewing tips |
| Email 3 | Day 7 (after first delivery expected) | Review request + community |

**Email 1 — Immediately post-purchase**

**Subject:** Your first bag is on its way ☕
**Preview text:** Here's everything you need to know about your order and what comes next.

Welcome to [Brand Name], [First Name].

Your order #[ORDER_NUMBER] is confirmed and roasting now. You'll get a shipping notification within 48 hours.

**What to expect:**
- Delivery in 3–5 business days
- Freshly roasted within 24 hours of shipping
- Grind size: [GRIND_SELECTION] (you chose this — you can change it anytime)

Questions? Reply to this email — we read every one.

[Manage your subscription →]

---

## Common Mistakes

1. **Discounting too early** — but most brands write great subject lines and leave preview text blank or let it auto-populate with "View in browser." Preview text is free real estate that extends your subject line. Use it.

2. **No suppression after purchase** — the most complained-about email in ecommerce is a cart abandonment or "you left something behind" message that arrives after the customer already bought. Always configure "Placed Order" as a flow exit event.

3. **Weak preview text** — offering 10% off in the first abandonment email trains your entire subscriber base to abandon carts intentionally to wait for a coupon. Reserve incentives for Email 3 only, or omit entirely for high-AOV products.

4. **Same angle for every win-back email** — the first win-back email should test the re-engagement angle; only escalate to a discount in Email 2 or 3. Offering a discount immediately in win-back signals low brand confidence and attracts deal-seekers.

5. **Post-purchase emails that only confirm the order** — transactional order confirmations have 70%+ open rates. That's your highest-engagement touchpoint. Use it to set expectations, introduce your brand story, and plant the seed for the next purchase.

6. **Subject lines over 60 characters** — on mobile, subject lines over 50–55 characters get truncated. Most ecommerce email opens happen on phones. Write the hook in the first 40 characters, put the detail after.

7. **Sending win-back to recently active subscribers** — if a subscriber opened an email 3 weeks ago, they are not lapsed. Win-back flows should target 90–180 day+ non-openers, not anyone who didn't buy last month.

8. **No A/B testing on subject lines** — open rate is almost entirely determined by subject line + preview text + sender name. Not testing at least two subject line variants on every major send wastes the statistical value of your list size.

9. **Ignoring transactional vs. promotional consent** — shipping updates are transactional and can be sent without marketing consent; promotional emails in post-purchase flows require express marketing consent. Keep flows clean.

10. **Flow re-entry loops** — if a subscriber abandons a cart, completes the 3-email sequence without buying, and immediately gets re-entered into the same flow, you will generate complaints. Set minimum re-entry delays of 14–30 days.

## Resources

- `references/output-template.md` — Standard output format for all Email Sequences deliverables
- `references/sequence-strategy-guide.md` — Sequence architecture, timing benchmarks, and segmentation frameworks by campaign type
- `references/esp-platform-guide.md` — Platform-specific setup instructions for Klaviyz, Mailchimp, Omnisend, and ActiveCampaign
- `assets/email-sequence-checklist.md` — 45-point quality checklist covering copy, segmentation, suppression, and deliverability
