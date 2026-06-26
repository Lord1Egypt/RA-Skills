# ESP Platform Guide — Klaviyo, Mailchimp, Omnisend, ActiveCampaign

## Overview

Email service platforms differ significantly in how they handle flow triggers, segmentation logic, A/B testing, and suppression. This guide covers platform-specific configuration for the four most common ecommerce ESPs. Always verify current platform behavior — interfaces and feature sets change with product updates.

---

## Klaviyo

### Flow Configuration

**Abandoned cart trigger:**
- Use the "Started Checkout" metric (not "Added to Cart") for highest intent signal
- Alternative: "Added to Cart" with no "Started Checkout" within 30 minutes for broader capture
- Smart Sending: Keep enabled — prevents sending if subscriber received any Klaviyo email in the past 16 hours

**Flow filters (apply at flow level, not email level):**
- "What someone has done → Placed Order → zero times since starting this flow" — removes purchasers from entire flow
- Set this as a trigger filter, not a mid-flow conditional, to prevent race conditions

**Smart Sending:**
- Default 16-hour quiet period — increase to 24 hours for lower-frequency senders
- Disable Smart Sending on transactional flows (order confirmation, shipping updates) only

**A/B Testing:**
- Subject line A/B: Available at the individual email level within flows
- Flow-level A/B (testing full sequence variants): Requires Klaviyo's "Flow A/B Test" feature — test 2 complete flow variants, split by percentage
- Winner determination: Set based on "Open Rate" for subject line tests; "Revenue per Recipient" for flow structure tests

**Segmentation and Conditional Splits:**
- Use "Conditional Split" nodes to branch by segment (VIP vs. standard, new vs. repeat)
- Define VIP as: "Has placed order → at least 3 times" or custom property synced from your store
- Time delay filters: Add "Time Delay" + "Trigger Split" combinations for advanced timing logic

**Deliverability notes:**
- Klaviyo uses shared sending IPs for accounts under ~50K contacts; dedicated IPs available above that threshold
- Ensure your Klaviyo account has a custom sending domain configured — shared domains reduce deliverability
- Monitor "Flow Analytics" → "Deliverability" tab for spam rates per flow

---

## Mailchimp

### Flow Configuration (Customer Journeys)

**Abandoned cart:**
- Available via "Customer Journeys" → Journey point: "Abandoned cart"
- Requires Mailchimp's ecommerce integration (Shopify, WooCommerce, or API)
- Limitation: Mailchimp's abandoned cart trigger fires on "cart created" + no order within X hours — less sophisticated than Klaviyo's "Started Checkout" event

**Timing:**
- Journey delays are set in whole hours or days — 1-hour minimum delay
- "Send at subscriber's local time" available on Standard plan and above

**Suppression:**
- Add a "If/Else" condition after each journey step: "Has ordered since journey start → Yes → End journey"
- Mailchimp does not auto-suppress on purchase at the journey level — manual conditional branching required

**A/B Testing:**
- A/B campaigns: Available for broadcast sends; tests subject line, content, or send time
- Multivariate testing: Available on Standard plan and above
- Journeys A/B: Limited compared to Klaviyo — use "If/Else" branches as a workaround for flow-level tests

**Segments:**
- Build segments via "Audience" → "Segments" using purchase history, engagement, and signup source
- Tag-based segmentation: Add tags via API or integration for custom segment signals
- Limitations: Mailchimp segment logic is less granular than Klaviyo for complex behavioral targeting

**Transactional emails:**
- Use Mailchimp Transactional (formerly Mandrill) for order confirmations and shipping updates — separate from marketing automation
- Do not send transactional messages through marketing journey builder

---

## Omnisend

### Flow Configuration (Automations)

**Abandoned cart:**
- Pre-built "Abandoned Cart" automation template available
- Trigger: Cart abandoned for X minutes/hours (configurable)
- Supports SMS + email + push notification in a single automation — useful for omnichannel sequences

**Multi-channel sequences:**
- Omnisend's primary advantage over Klaviyo for smaller stores: native SMS, push, and email in one flow
- Recommended order: Email (1h) → SMS (6h, if subscriber has SMS consent) → Email (22h) — mixes channels to reduce email fatigue

**Segmentation:**
- "Segment" filter available at automation level and at individual message level
- "Shopping activity" segment: filter by purchase count, purchase value, product category purchased
- "Campaign activity" segment: filter by open rate, click rate, last engagement date

**Suppression:**
- Built-in: Orders suppress cart abandonment automatically if integration is connected
- Frequency cap: Set via "Global Frequency Settings" → max X messages per Y days across all automations

**A/B Testing:**
- A/B testing available at the message level within automations (subject line, content)
- Not available at the full automation flow level (use separate automations for flow-level tests)

**Platform-specific notes:**
- Omnisend's "Product Picker" allows inserting dynamic product blocks directly in email — use for cart contents in abandonment emails
- "Discount Code" block: Generate unique one-time codes per subscriber directly in Omnisend (no external coupon system needed)
- TCPA compliance: Omnisend handles SMS opt-in separately — ensure SMS subscribers have opted in via Omnisend's keyword flow or embedded form

---

## ActiveCampaign

### Flow Configuration (Automations)

**Abandoned cart:**
- Requires ecommerce integration (Shopify, WooCommerce, BigCommerce, or custom via API)
- Trigger: "Makes a purchase" → Condition: "Wait 1 hour" → "If/Else: Has made a purchase in last 1 hour → No → Send Email 1"
- More complex to set up than Klaviyo but highly customizable via conditional logic

**CRM integration advantage:**
- ActiveCampaign's native CRM allows sales follow-up for high-value abandoned carts — assign to a sales rep if cart value exceeds threshold
- B2B ecommerce use case: "If cart value > $500 → Assign deal to sales rep → Send internal notification" within automation

**Segmentation:**
- Tag-based segmentation: Apply tags via automation actions; segment lists by tag combinations
- Custom fields: Store any customer attribute as a custom field; use in segment conditions and personalization
- Predictive sending: ActiveCampaign's "Send based on contact's timezone" and "Predictive Sending" (machine-learning send time) available on Plus plan and above

**Suppression:**
- Add "Goal" step at flow level: "Has made a purchase → Yes → End automation" — works as a continuous exit condition checking at each email step
- "Unsubscribe" automation trigger: Build a separate automation that fires on unsubscribe and removes contacts from all active automations

**A/B Testing:**
- Split testing available within automations: "Go to [Version A]" vs. "Go to [Version B]" branches
- Configure 50/50 split at branch node; winner can be selected manually or automatically after reaching statistical threshold

**Deliverability:**
- ActiveCampaign offers a dedicated IP on Enterprise plan; shared IPs on lower tiers
- Spam score check: Available in email builder — review before activating any new automation
- Engagement-based sending: Use segment conditions to suppress low-engagement contacts (no open in 180 days) from promotional sequences

---

## Cross-Platform Deliverability Basics

Regardless of ESP, these fundamentals apply to all ecommerce email programs:

| Practice | Implementation |
|---|---|
| Custom sending domain | Configure DKIM, SPF, and DMARC records for your sending domain — required for Google/Yahoo bulk sender compliance (2024+) |
| List hygiene | Remove hard bounces immediately; suppress soft bounces after 3 failed sends |
| Engagement segmentation | Do not send promotional sequences to subscribers who have not opened any email in 180+ days — suppress them first |
| Unsubscribe handling | Honor all unsubscribes within 10 business days (CAN-SPAM) or 10 days (CASL); most ESPs process immediately |
| One-click unsubscribe | Required for bulk senders per Google/Yahoo 2024 requirements — ensure your ESP has this configured |
| Seed list testing | Before launching a new sequence, send to a seed list across Gmail, Outlook, and Apple Mail to check rendering and inbox placement |
