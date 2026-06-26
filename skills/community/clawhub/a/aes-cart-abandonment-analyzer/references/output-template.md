# Cart Abandonment Analysis Report

## 1. Store Overview

| Field | Details |
|---|---|
| Store Platform | [Shopify / WooCommerce / BigCommerce / Custom] |
| Average Order Value (AOV) | $[X.XX] |
| Monthly Visitors | [X,XXX] |
| Monthly Add-to-Carts | [X,XXX] |
| Monthly Cart Abandonments | [X,XXX] |
| Cart Abandonment Rate | [XX%] |
| Current Recovery Method | [None / Single email / Multi-touch / etc.] |
| Current Recovery Rate | [X%] (or N/A if none) |

### Product Mix
| Category | Avg Price | % of Carts | Margin Profile |
|---|---|---|---|
| [Category 1] | $[X.XX] | [XX%] | [High / Medium / Low] |
| [Category 2] | $[X.XX] | [XX%] | [High / Medium / Low] |
| [Category 3] | $[X.XX] | [XX%] | [High / Medium / Low] |

---

## 2. Funnel Drop-off Analysis

### Checkout Funnel Stages

| Stage | Visitors Entering | Drop-off Rate | Primary Device | Key Observation |
|---|---|---|---|---|
| Product Page → Cart | [X,XXX] | [XX%] | [Desktop/Mobile split] | [Observation] |
| Cart → Checkout Start | [X,XXX] | [XX%] | [Desktop/Mobile split] | [Observation] |
| Checkout → Shipping Info | [X,XXX] | [XX%] | [Desktop/Mobile split] | [Observation] |
| Shipping → Payment | [X,XXX] | [XX%] | [Desktop/Mobile split] | [Observation] |
| Payment → Order Review | [X,XXX] | [XX%] | [Desktop/Mobile split] | [Observation] |
| Order Review → Purchase | [X,XXX] | [XX%] | [Desktop/Mobile split] | [Observation] |

### Abandonment by Segment

| Segment | Abandonment Rate | vs. Average | Notable Pattern |
|---|---|---|---|
| New visitors | [XX%] | [+/-X%] | [Pattern] |
| Returning visitors | [XX%] | [+/-X%] | [Pattern] |
| Mobile users | [XX%] | [+/-X%] | [Pattern] |
| Desktop users | [XX%] | [+/-X%] | [Pattern] |
| Paid traffic | [XX%] | [+/-X%] | [Pattern] |
| Organic traffic | [XX%] | [+/-X%] | [Pattern] |

---

## 3. Root Cause Diagnosis

### Ranked Abandonment Causes

| Rank | Cause | Estimated Impact | Evidence | Confidence |
|---|---|---|---|---|
| 1 | [Primary cause] | [XX% of abandonments] | [Data supporting this] | [High/Medium/Low] |
| 2 | [Secondary cause] | [XX% of abandonments] | [Data supporting this] | [High/Medium/Low] |
| 3 | [Tertiary cause] | [XX% of abandonments] | [Data supporting this] | [High/Medium/Low] |
| 4 | [Fourth cause] | [XX% of abandonments] | [Data supporting this] | [High/Medium/Low] |
| 5 | [Fifth cause] | [XX% of abandonments] | [Data supporting this] | [High/Medium/Low] |

### Checkout Friction Fixes (Pre-Recovery)
Before building recovery sequences, address these checkout issues:

| Issue | Fix | Expected Impact | Implementation Effort |
|---|---|---|---|
| [Issue 1] | [Solution] | [High/Medium/Low] | [Easy/Medium/Hard] |
| [Issue 2] | [Solution] | [High/Medium/Low] | [Easy/Medium/Hard] |
| [Issue 3] | [Solution] | [High/Medium/Low] | [Easy/Medium/Hard] |

---

## 4. Recovery Sequence Design

### Sequence Architecture

| Touch # | Channel | Timing After Abandonment | Purpose | Content Type | Incentive |
|---|---|---|---|---|---|
| 1 | [Email/SMS/Push] | [X min/hours] | [Reminder/Social proof/Urgency] | [Description] | [None/Free shipping/X% off] |
| 2 | [Email/SMS/Push] | [X hours] | [Purpose] | [Description] | [Incentive] |
| 3 | [Email/SMS/Push] | [X hours] | [Purpose] | [Description] | [Incentive] |
| 4 | [Email/SMS/Push] | [X hours] | [Purpose] | [Description] | [Incentive] |
| 5 | [Email/SMS/Push] | [X hours] | [Purpose] | [Description] | [Incentive] |

### Segmentation Rules

| Segment | Definition | Sequence Modification | Rationale |
|---|---|---|---|
| [Segment 1] | [Criteria] | [How sequence changes] | [Why] |
| [Segment 2] | [Criteria] | [How sequence changes] | [Why] |
| [Segment 3] | [Criteria] | [How sequence changes] | [Why] |
| [Segment 4] | [Criteria] | [How sequence changes] | [Why] |

### Suppression Rules
- [ ] Remove from sequence when purchase is completed (any channel/device)
- [ ] Remove when customer starts a new cart (restart sequence for new cart)
- [ ] Exclude customers who have unsubscribed from marketing
- [ ] Exclude customers who have abandoned 3+ times in 30 days (deal-seekers)
- [ ] Exclude orders with already-discounted items from discount offers
- [ ] Respect quiet hours (no SMS between 9pm-9am recipient local time)

---

## 5. Incentive Strategy

### Incentive Escalation Ladder

| Cart Value Tier | Touch 1 | Touch 2 | Touch 3 | Touch 4+ | Max Discount |
|---|---|---|---|---|---|
| Under $[X] | [Incentive] | [Incentive] | [Incentive] | [Incentive] | [Cap] |
| $[X]-$[Y] | [Incentive] | [Incentive] | [Incentive] | [Incentive] | [Cap] |
| $[Y]-$[Z] | [Incentive] | [Incentive] | [Incentive] | [Incentive] | [Cap] |
| Over $[Z] | [Incentive] | [Incentive] | [Incentive] | [Incentive] | [Cap] |

### Discount Code Rules
- Code type: [Unique single-use / Shared with expiration]
- Expiration: [X hours after generation]
- Minimum order value: $[X.XX]
- Exclusions: [Product categories or conditions excluded]
- Stacking: [Can/cannot combine with other promotions]

---

## 6. Message Copy (Per Touch)

### Touch 1: [Channel] — [Purpose]
**Send time:** [X minutes/hours after abandonment]

**Subject line A:** "[Subject]"
**Subject line B:** "[A/B variant]"
**Preview text:** "[Preview text]"

**Body copy:**
[Full email body copy or SMS text]

**CTA:** "[Button text]"

### Touch 2: [Channel] — [Purpose]
[Same structure]

### Touch 3: [Channel] — [Purpose]
[Same structure]

[Continue for all touches]

---

## 7. Measurement Framework

### Primary KPIs

| Metric | Definition | Target | Current |
|---|---|---|---|
| Recovery Rate | Abandoned carts recovered / Total abandoned carts | [X%] | [X%] |
| Revenue Recovered | Total revenue from recovered carts | $[X,XXX]/month | $[X,XXX]/month |
| Incremental Revenue | Revenue recovered minus baseline return rate | $[X,XXX]/month | N/A |
| Recovery Cost | Cost per recovered cart (email/SMS send costs + discounts given) | $[X.XX] | N/A |
| ROI | (Revenue Recovered - Costs) / Costs | [X:1] | N/A |

### Per-Touch Metrics

| Touch | Delivery Rate | Open Rate | Click Rate | Conversion Rate | Revenue |
|---|---|---|---|---|---|
| Touch 1 | [XX%] | [XX%] | [XX%] | [XX%] | $[X,XXX] |
| Touch 2 | [XX%] | [XX%] | [XX%] | [XX%] | $[X,XXX] |
| Touch 3 | [XX%] | [XX%] | [XX%] | [XX%] | $[X,XXX] |
| Touch 4 | [XX%] | [XX%] | [XX%] | [XX%] | $[X,XXX] |

### Incrementality Testing Plan
- **Holdout group:** [X%] of abandoners receive no recovery messages
- **Test duration:** [X weeks] minimum for statistical significance
- **Expected baseline return rate:** [X%] (customers who return without any nudge)
- **True incremental lift calculation:** Recovery rate - Holdout conversion rate

---

## 8. Optimization Roadmap

### 90-Day Testing Calendar

| Week | Test | Hypothesis | Success Metric | Min Sample |
|---|---|---|---|---|
| 1-2 | [Test 1] | [Hypothesis] | [Metric] | [N per variant] |
| 3-4 | [Test 2] | [Hypothesis] | [Metric] | [N per variant] |
| 5-6 | [Test 3] | [Hypothesis] | [Metric] | [N per variant] |
| 7-8 | [Test 4] | [Hypothesis] | [Metric] | [N per variant] |
| 9-12 | [Test 5] | [Hypothesis] | [Metric] | [N per variant] |

---

## 9. Revenue Impact Projection

| Scenario | Recovery Rate | Monthly Recoveries | Monthly Revenue | vs. Current |
|---|---|---|---|---|
| Current state | [X%] | [X,XXX] | $[X,XXX] | Baseline |
| Conservative (sequence only) | [X%] | [X,XXX] | $[X,XXX] | +$[X,XXX] |
| Moderate (sequence + checkout fixes) | [X%] | [X,XXX] | $[X,XXX] | +$[X,XXX] |
| Aggressive (fully optimized) | [X%] | [X,XXX] | $[X,XXX] | +$[X,XXX] |

**Annual revenue opportunity:** $[XXX,XXX]
