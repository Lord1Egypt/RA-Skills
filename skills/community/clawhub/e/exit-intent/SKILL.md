---
name: Exit Intent
description: Design exit-intent popup strategies for ecommerce sites including trigger rules, offer types, copy variants, and A/B testing plans that recover leaving visitors without degrading UX or brand perception.
---

# Exit Intent

This skill designs end-to-end exit-intent popup strategies for ecommerce stores — deciding when to fire, what to offer, what copy and creative to show, and how to measure lift — so that recovery offers catch abandoning visitors without interrupting the ones who are still shopping or ready to check out.

## Quick Reference

| Decision | Strong | Acceptable | Weak|
|---|---|---|---|
| Trigger timing | Fire only after 15s+ on page AND cursor leaves viewport toward browser chrome | Fire on scroll-up past 60% of page | Fire immediately on page load or after < 5s |
| Offer type | Tiered by cart value (% off high carts, free shipping low carts) | Single universal discount code | Generic "Don't leave!" with no incentive |
| Copy length | Headline ≥ 8 words + 1-line value prop + single CTA | Headline + short paragraph + CTA | Wall of text with multiple competing CTAs |
| Mobile handling | Slide-up drawer triggered by back-button or tab-switch, respects scroll | Smaller modal with close button at top | Full-screen overlay blocking content, no close affordance |
| Frequency cap | 1 show per session, s-day cookie cooldown | 1 show per session, no cross-session memory | Shows on every page, no cap |
| A/B test design | Sequential test: trigger → offer → copy → creative, 1 variable at a time | Multivariate test with interaction analysis | Change everything at once with no control |
| SEO / CWV safety | Lazy-load popup JS, < 20 KB, no layout shift, defer until after LCP | Popup JS in main bundle but < 50 KB | Large third-party script blocking render, CLS > 0.1 |
| Close behavior | Visible X button + click-outside-to-close + Esc key | Visible X button only | No close mechanism or hidden close button |

## Solves

1. **High cart abandonment with no recovery system** — stores losing 60-80% of carts with no popup or only a generic browser-default prompt.
2. **Popups that annoy engaged shoppers** — exit overlays firing too early, on wrong pages, or for users who are actively browsing or already at checkout.
3. **Weak or generic popup copy** —  "Wait! Don't leave!" headlines that fail to provide a compelling reason to stay or convert.
4. **No offer strategy by visitor segment** — same 10%-off code for a first-time visitor with a $20 cart and a returning customer with $300 in cart.
5. **Mobile popup compliance gaps** — overlays violating Google's interstitial guidelines, breaking mobile UX, or failing to display correctly on small screens.
6. **Unmeasured popup impact** — no A/B testing, no control group, no tracking of incremental revenue vs. margin erosion from discounts.
7. **Brand and trust damage** — aggressive popup patterns (multiple overlays, fake urgency timers, dark-pattern close buttons) that erode brand trust over time.

## Workflow

### Step 1 — Audit Current State

Collect baseline metrics before designing the strategy:

- Current desktop and mobile bounce rates by page type (home, collection, product, cart, checkout)
- Cart abandonment rate (carts created vs. orders completed)
- Existing popup tools in use (Privy, Justuno, OptinMonster, Klaviyo forms, native Shopify)
- Google Search Console Core Web Vitals status (especially CLS and INP)
- Current popup frequency and trigger rules if any exist
- Revenue per session and average order value for context on offer sizing

Deliverable: Baseline metrics snapshot with annotated problem areas.

### Step 2 — Define Trigger Rules

Design trigger conditions that balance recovery rate with UX:

**Desktop triggers (use AND logic):**
- Time on page ≥ 15 seconds (proves engagement before interrupting)
- Cursor exits viewport toward top of screen (true exit signal)
- Page type is product or cart (highest-intent pages)
- User has NOT already seen popup this session
- User has NOT completed a purchase in the last 30 days

**Mobile triggers (use OR logic since no cursor):**
- Back button or navigation-away gesture detected
- Browser tab switch after 30s+ on site
- Scroll-to-top after reaching 70%+ page depth (intent reversal signal)

**Exclusions (never show):**
- User is mid-checkout (past shipping step)
- User arrived via email campaign with existing discount
- User has active discount code in cart
- User dismissed popup within last 72 hours

Deliverable: Trigger rules matrix with conditions, logic operators, and exclusion list.

### Step 3 — Design Offer Tiers

Create segmented offers based on cart value and visitor type:

| Segment | Cart Value | Visitor Type | Offer | Rationale |
|---|---|---|---|---|
| High-value abandoner | > $150 | Any | 10% off or free express shipping | Protect margin, high motivation to convert |
| Mid-value abandoner | $50-150 | Returning | Free standard shipping | Familiar with brand, shipping cost is friction |
| Mid-value abandoner | $50-150 | New | 15% off first order | Acquisition cost justifies deeper discount |
| Low-value browser | < $50 | Any | Email signup for 10% future discount | Build list, don't discount low-margin orders |
| Cart page abandoner | Any | Any | Cart reminder + urgency (stock/price) | No discount needed — just remove friction |

Deliverable: Offer tier matrix with segment definitions, offer values, and margin impact estimates.

### Step 4 — Write Copy Variants

Create 3 copy variants per offer tier for A/B testing:

**Structure for each variant:**
- Headline (≤ 8 words, benefit-led or curiosity-driven)
- Subheadline (1 line, specifics of the offer)
- CTA button text (action verb + benefit)
- Dismissal text (low-pressure, no guilt)

**Copy principles:**
- Lead with what they GET, not what they're LOSING
- Use specific numbers ("15% off" not "a special discount")
- CTA should complete the sentence "I want to..."
- Dismissal text should be neutral ("No thanks, I'll pay full price" not "No, I hate saving money")

Deliverable: Copy matrix with 3 variants per tier, each with headline, subheadline, CTA, and dismiss text.

### Step 5 — Specify Creative and Layout

Define visual specifications for the popup:

- **Format:** Centered modal on desktop (max 500px wide), bottom slide-up drawer on mobile (max 40% viewport height)
- **Visual hierarchy:** Headline → product image or lifestyle shot → offer details → CTA button → dismiss link
- **Colors:** CTA button uses brand primary, background uses white or light neutral, text uses brand dark
- **Animation:** Fade-in with subtle scale (200ms ease-out), no bounce or shake effects
- **Close affordance:** X button top-right (min 44px touch target), click-outside-to-close, Esc key support
- **Accessibility:** Focus trap within modal, aria-modal="true", role="dialog", aria-labelledby pointing to headline

Deliverable: Creative spec document with wireframe, color tokens, animation timing, and accessibility requirements.

### Step 6 — Build A/B Testing Plan

Design sequential tests to isolate each variable:

**Test 1 — Trigger sensitivity (Week 1-2):**
- Control: No popup
- Variant A: Trigger at 15s + cursor exit
- Variant B: Trigger at 30s + cursor exit
- Primary metric: Incremental revenue per session
- Guardrail: Bounce rate increase < 2pp

**Test 2 — Offer type (Week 3-4):**
- Use winning trigger from Test 1
- Control: Free shipping
- Variant A: Percentage discount
- Variant B: Dollar-off discount
- Primary metric: Popup conversion rate
- Guardrail: Gross margin per converted session

**Test 3 — Copy and creative (Week 5-6):**
- Use winning trigger + offer
- Test 3 headline/CTA combinations
- Primary metric: Popup click-through rate
- Guardrail: Overall site conversion rate

**Statistical requirements:**
- Minimum 1,000 popup impressions per variant
- 95% confidence level, 80% power
- Run each test for minimum 2 full business cycles (14 days)

Deliverable: A/B test roadmap with timeline, variants, metrics, sample sizes, and decision criteria.

### Step 7 — Monitor and Iterate

Set up ongoing monitoring dashboards and iteration cycles:

- **Daily:** Popup impression count, CTR, conversion rate, revenue attributed
- **Weekly:** Compare test variant performance, check guardrail metrics
- **Monthly:** Review offer margin impact, update copy for seasonal relevance, check CWV scores
- **Quarterly:** Full strategy review — retire underperforming variants, test new offer structures

Deliverable: Monitoring dashboard spec with KPIs, alert thresholds, and review cadence.

## Examples

### Example 1 — DTC Skincare Brand ($85 AOV, 72% Cart Abandonment)

**Input:** "We sell premium skincare DTC on Shopify. AOV is $85, cart abandonment is 72%. We have no exit popups. Our margins are 65%. We get 40K monthly sessions, 60% mobile."

**Audit findings:**
- No existing popup infrastructure
- Desktop bounce rate: 48% (acceptable), Mobile: 61% (high)
- Cart page drop-off: 38% of users who add to cart never reach checkout
- CWV scores: All green (LCP 1.8s, CLS 0.02, INP 120ms)
- No existing email popup or discount system

**Trigger rules designed:**
- Desktop: Time on page ≥ 20s AND cursor exit toward top AND page is product or cart AND no popup shown this session AND no purchase in 30 days
- Mobile: Back-button gesture after 25s+ on product page OR tab-switch from cart page
- Exclusions: Checkout pages, users with active promo code, users who dismissed within 72h, users arriving from Klaviyo email links

**Offer tiers:**
| Segment | Trigger Page | Offer | Expected Margin Impact |
|---|---|---|---|
| Cart > $100 | Cart page | Free express upgrade (normally $12) | -$12/order, ~14% conversion lift |
| Cart $50-100 | Cart page | 10% off | -$7.25/order avg, ~18% conversion lift |
| No cart, browsing | Product page | Join VIP list → 15% first order | $0 immediate, builds email list |

**Copy variant A (winning):**
- Headline: "Your cart is waiting"
- Subheadline: "Complete your order in the next 15 minutes and get free express shipping"
- CTA: "Upgrade My Shipping — Free"
- Dismiss: "No thanks, standard shipping is fine"

**Results after 6 weeks:**
- Popup impression rate: 12% of sessions (correctly filtered)
- Popup CTR: 8.4%
- Incremental revenue: $18,200/month
- Cart abandonment: 72% → 64%
- CWV impact: None (popup JS: 14KB, lazy-loaded)

### Example 2 — Electronics Accessories Store ($42 AOV, High Mobile Traffic)

**Input:** "We sell phone cases and accessories on WooCommerce. AOV is $42, margins are 45%. 78% mobile traffic. We tried a popup before but it hurt our Google rankings."

**Audit findings:**
- Previous popup was a full-screen interstitial on mobile (violates Google guidelines)
- CLS jumped to 0.18 when popup was active (failing CWV threshold)
- Desktop bounce: 52%, Mobile bounce: 67%
- Cart abandonment: 68%
- Previous popup had no frequency cap — showed on every page load

**Trigger rules designed:**
- Desktop: Time ≥ 15s AND cursor exit AND product or cart page AND session popup count = 0
- Mobile: NO full-screen overlay. Instead: sticky bottom bar (non-intrusive) that appears after 30s on product page, collapses to icon after 5s if not engaged
- Exclusions: Checkout, returning purchasers within 14 days, users who clicked dismiss, search-engine bot user agents

**Mobile-specific design:**
- Format: Bottom sheet, 30% viewport height, slides up with 250ms ease
- Does NOT cover main content — user can continue scrolling
- Complies with Google's mobile interstitial guidelines (not penalized)
- Touch target: 48px minimum for CTA and close

**Offer strategy (low margins require caution):**
| Segment | Offer | Margin Impact |
|---|---|---|
| Cart > $60 | Free shipping ($5.99 value) | -$5.99/order, justified by higher AOV |
| Cart $25-60 | "Add $X more for free shipping" progress bar | $0 cost, increases AOV |
| Browsing, no cart | "Get notified when this drops in price" email capture | $0 cost, builds list |

**Copy variant B (winning):**
- Headline: "Free shipping unlocked"
- Subheadline: "Your cart qualifies — checkout now to lock it in"
- CTA: "Checkout with Free Shipping"
- Dismiss: "Maybe later"

**Results after 4 weeks:**
- Mobile bounce rate: 67% → 63%
- CWV: CLS back to 0.03 (green), no ranking impact
- Popup engagement: 6.2% CTR
- Incremental revenue: $4,800/month
- AOV lift: $42 → $47 (from "add more for free shipping" bar)

## Common Mistakes

1. **Firing popups too early** — Showing an exit popup within 5 seconds tells the visitor you expect them to leave. Wait at least 15 seconds to ensure they've had time to engage with the page content.

2. **Using full-screen interstitials on mobile** — Google penalizes intrusive interstitials on mobile in search rankings. Use bottom sheets, slide-up drawers, or sticky bars instead of overlays that cover the main content.

3. **Offering the same discount to every visitor** — A blanket 15%-off code trains all visitors to expect discounts and erodes margins. Segment offers by cart value, visitor type, and page context.

4. **No frequency cap** — Showing the popup on every page visit creates popup fatigue and actively pushes visitors away. Cap to 1 impression per session with a 72-hour cross-session cooldown.

5. **Testing everything at once** — Changing the trigger, offer, copy, and design simultaneously makes it impossible to know what drove the result. Test one variable at a time in sequential experiments.

6. **Ignoring Core Web Vitals impact** — Heavy popup scripts, layout shifts from overlay rendering, and render-blocking CSS can tank CWV scores. Lazy-load popup code, keep the bundle under 20KB, and ensure zero CLS.

7. **Dark-pattern dismiss buttons** — Tiny close buttons, guilt-trip dismissal copy ("No, I hate saving money"), or fake countdown timers damage brand trust and may violate consumer protection regulations in some jurisdictions.

8. **Not measuring incrementality** — Tracking popup conversion rate without a holdout control group overstates impact. Many popup converters would have purchased anyway. Always run with a no-popup control to measure true incremental revenue.

9. **Showing popups to returning purchasers** — A customer who bought last week doesn't need a discount popup. Exclude recent purchasers and let loyalty programs handle retention offers.

10. **Forgetting accessibility** — Popups without focus trapping, keyboard navigation, screen-reader labels, or sufficient color contrast exclude users and may create legal liability under ADA/WCAG requirements.

## Resources

- [Output Template](references/output-template.md) — Structured template for the complete exit-intent strategy deliverable
- [Trigger Rules Guide](references/trigger-rules-guide.md) — Deep-dive into trigger logic, device-specific patterns, and exclusion rules
- [Offer Strategy Guide](references/offer-strategy-guide.md) — Frameworks for segmenting offers by visitor behavior and cart context
- [Quality Checklist](assets/quality-checklist.md) — Pre-launch checklist covering UX, compliance, performance, and measurement
