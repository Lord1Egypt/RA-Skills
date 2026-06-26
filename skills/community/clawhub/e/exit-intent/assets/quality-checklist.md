# Exit Intent — Quality Checklist

## Trigger Rules (8 items)
- [ ] Desktop trigger uses cursor-exit-top detection, not just time-on-page alone
- [ ] Minimum time-on-page threshold is ≥ 15 seconds
- [ ] Popup is restricted to high-intent pages (product, cart) not site-wide
- [ ] Session frequency cap: maximum 1 popup shown per session
- [ ] Cross-session cooldown: 72+ hours between popup impressions via cookie/localStorage
- [ ] Checkout pages are excluded from all popup triggers
- [ ] Recent purchasers (within 30 days) are excluded
- [ ] Users with active promo codes in cart are excluded

## Mobile Compliance (7 items)
- [ ] No full-screen interstitials on mobile (violates Google guidelines)
- [ ] Mobile popup format is bottom sheet, sticky bar, or slide-up drawer
- [ ] Mobile popup covers ≤ 40% of viewport height
- [ ] Close button touch target is ≥ 44px × 44px
- [ ] Popup does not block page content or navigation
- [ ] Back-button/gesture triggers tested on iOS Safari and Chrome Android
- [ ] Popup degrades gracefully if JavaScript is delayed or blocked

## Offer Strategy (7 items)
- [ ] Offers are segmented by cart value (not one-size-fits-all)
- [ ] New vs. returning visitors receive different offer types
- [ ] Browsing visitors without cart items get email capture, not discounts
- [ ] Discount levels are calibrated against gross margin (≤ 1/3 of margin)
- [ ] Dollar impact per order is calculated for each offer tier
- [ ] Auto-apply discount codes are used where platform supports it
- [ ] No fake urgency mechanisms (countdown timers, false scarcity)

## Copy and Creative (8 items)
- [ ] Headline is ≤ 8 words and benefit-led
- [ ] Subheadline specifies the exact offer (not vague)
- [ ] CTA button text uses action verb + benefit ("Get Free Shipping")
- [ ] Dismiss text is neutral and guilt-free
- [ ] At least 3 copy variants created per offer tier for A/B testing
- [ ] Copy avoids dark patterns and manipulative language
- [ ] Visual hierarchy follows: Headline → Image → Offer → CTA → Dismiss
- [ ] Brand colors and typography are consistent with site design

## Accessibility (6 items)
- [ ] Modal has role="dialog" and aria-modal="true"
- [ ] Headline is referenced by aria-labelledby
- [ ] Focus is trapped within modal when open
- [ ] Keyboard navigation works (Tab to cycle, Esc to close)
- [ ] Color contrast meets WCAG 2.1 AA (≥ 4.5:1 for text)
- [ ] Screen reader announces popup opening and content

## Performance (6 items)
- [ ] Popup JavaScript bundle is < 20 KB gzipped
- [ ] Popup JS is lazy-loaded after page load event
- [ ] Popup rendering causes zero Cumulative Layout Shift (CLS)
- [ ] Event listeners use passive flag for scroll tracking
- [ ] Popup assets (images) are optimized and lazy-loaded
- [ ] CWV scores tested with popup active — all metrics remain green

## A/B Testing (5 items)
- [ ] Sequential test plan isolates one variable at a time
- [ ] Control group (no popup) is included to measure incrementality
- [ ] Minimum sample size calculated per variant (≥ 1,000 impressions)
- [ ] Test duration spans at least 2 full business cycles (14 days)
- [ ] Guardrail metrics defined (bounce rate, margin, CWV)

## Analytics and Monitoring (5 items)
- [ ] Popup impressions tracked and reported daily
- [ ] Click-through rate tracked per variant
- [ ] Conversion rate tracked with attribution to popup interaction
- [ ] Incremental revenue calculated vs. control group
- [ ] Alert thresholds set for anomalies (sudden CTR drop, CWV spike)
