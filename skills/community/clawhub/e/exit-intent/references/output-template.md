# Exit Intent Strategy — Output Template

## 1. Executive Summary

**Store:** [Store name and platform]
**Current cart abandonment rate:** [X%]
**Current recovery mechanism:** [None / Basic popup / Email only]
**Projected incremental monthly revenue:** [$X,XXX]

---

## 2. Baseline Metrics

| Metric | Desktop | Mobile | Combined |
|---|---|---|---|
| Monthly sessions | | | |
| Bounce rate | | | |
| Cart abandonment rate | | | |
| Average order value | | | |
| Gross margin | | | |
| Revenue per session | | | |
| Core Web Vitals (LCP) | | | |
| Core Web Vitals (CLS) | | | |
| Core Web Vitals (INP) | | | |

---

## 3. Trigger Rules

### Desktop Triggers
| Condition | Operator | Value | Rationale |
|---|---|---|---|
| Time on page | ≥ | [X] seconds | |
| Cursor position | = | Exited viewport top | |
| Page type | IN | [product, cart] | |
| Session popup count | = | 0 | |
| Days since last purchase | > | [X] days | |

### Mobile Triggers
| Condition | Value | Rationale |
|---|---|---|
| Gesture detected | [back-button / tab-switch / scroll-reversal] | |
| Minimum time on page | [X] seconds | |
| Page type | [product / cart] | |

### Global Exclusions
- [ ] User is past checkout shipping step
- [ ] User arrived via campaign with existing discount
- [ ] User has active promo code in cart
- [ ] User dismissed popup within [X] hours
- [ ] User is identified as bot/crawler
- [ ] User completed purchase within [X] days

---

## 4. Offer Tiers

| Tier | Segment Definition | Cart Value | Visitor Type | Offer | Est. Margin Impact | Est. Conversion Lift |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |

---

## 5. Copy Variants

### Tier 1 — [Tier Name]

**Variant A:**
- Headline: 
- Subheadline: 
- CTA: 
- Dismiss text: 

**Variant B:**
- Headline: 
- Subheadline: 
- CTA: 
- Dismiss text: 

**Variant C:**
- Headline: 
- Subheadline: 
- CTA: 
- Dismiss text: 

*(Repeat for each tier)*

---

## 6. Creative Specifications

### Desktop Layout
- Format: [Centered modal / Slide-in / Banner]
- Max width: [X]px
- Background: [Color]
- Visual hierarchy: [Headline → Image → Offer → CTA → Dismiss]

### Mobile Layout
- Format: [Bottom sheet / Sticky bar / Slide-up drawer]
- Max height: [X]% viewport
- Animation: [Type, duration, easing]

### Accessibility Requirements
- [ ] Focus trap within modal
- [ ] aria-modal="true"
- [ ] role="dialog"
- [ ] aria-labelledby pointing to headline
- [ ] Keyboard navigation (Tab, Esc to close)
- [ ] Color contrast ≥ 4.5:1
- [ ] Touch targets ≥ 44px

---

## 7. A/B Testing Roadmap

### Test 1 — [Variable]
| Parameter | Value |
|---|---|
| Duration | Week [X] to [Y] |
| Control | |
| Variant A | |
| Variant B | |
| Primary metric | |
| Guardrail metric | |
| Min sample size | |
| Confidence level | |

*(Repeat for each test)*

---

## 8. Implementation Checklist

- [ ] Popup tool selected and installed
- [ ] Trigger rules configured per spec
- [ ] Offer codes created in ecommerce platform
- [ ] Copy loaded for all variants
- [ ] Creative assets designed and uploaded
- [ ] A/B test configured with proper traffic split
- [ ] Analytics tracking verified (impressions, clicks, conversions)
- [ ] CWV impact tested in staging
- [ ] Mobile compliance verified
- [ ] Accessibility audit passed

---

## 9. Monitoring Dashboard

| KPI | Frequency | Alert Threshold |
|---|---|---|
| Popup impression rate | Daily | < [X]% or > [Y]% of sessions |
| Popup CTR | Daily | < [X]% |
| Popup conversion rate | Daily | < [X]% |
| Incremental revenue | Weekly | Negative vs. control |
| Cart abandonment rate | Weekly | Increase > [X]pp |
| CLS score | Weekly | > 0.1 |
| Bounce rate change | Weekly | Increase > [X]pp |

---

## 10. Results Summary (Post-Test)

| Metric | Before | After | Change |
|---|---|---|---|
| Cart abandonment rate | | | |
| Revenue per session | | | |
| Incremental monthly revenue | | | |
| AOV | | | |
| CWV impact | | | |
| Email list growth (if applicable) | | | |
