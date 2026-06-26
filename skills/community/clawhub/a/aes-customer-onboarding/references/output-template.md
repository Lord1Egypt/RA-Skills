# Customer Onboarding Playbook — Output Template

Use this template to structure the final onboarding playbook deliverable. Each section should be completed with specific details from the client's product, customer, and channel context.

---

## 1. Executive Summary

**Brand:** [Brand name]
**Product category:** [e.g., Premium skincare, Home fitness equipment, Specialty food]
**Average order value:** $[amount]
**Current metrics:**
- Return rate: [X]%
- 30-day repurchase rate: [X]%
- Average days to second purchase: [X]
- Current post-purchase emails: [List existing automations]

**Onboarding objectives:**
- Primary: [e.g., Reduce return rate from 18% to 12%]
- Secondary: [e.g., Increase 30-day repurchase rate from 22% to 35%]
- Tertiary: [e.g., Achieve 15% review submission rate]

---

## 2. Customer Segmentation

### Segment A: [Name — e.g., "First-Time Buyer, Simple Product"]
- **Profile:** [Description]
- **Sequence length:** [X] touchpoints over [X] days
- **Primary channel:** [Email / SMS / Push]
- **Key education needs:** [List]

### Segment B: [Name — e.g., "First-Time Buyer, Complex Product"]
- **Profile:** [Description]
- **Sequence length:** [X] touchpoints over [X] days
- **Primary channel:** [Email / SMS / Push]
- **Key education needs:** [List]

### Segment C: [Name — e.g., "Returning Customer, New Category"]
- **Profile:** [Description]
- **Sequence length:** [X] touchpoints over [X] days
- **Primary channel:** [Email / SMS / Push]
- **Key education needs:** [List]

---

## 3. Sequence Timeline

### Master Timeline (Default Segment)

| # | Day | Trigger Event | Channel | Subject / Headline | Content Summary | Primary CTA | Success Metric |
|---|-----|---------------|---------|-------------------|-----------------|-------------|----------------|
| 1 | 0 | Order placed | Email | [Subject line] | [2-3 sentence summary] | [CTA text] | [Metric + target] |
| 2 | 0 | Order placed | SMS | [Message preview] | [Content summary] | [CTA text] | [Metric + target] |
| 3 | 1-2 | Processing | Email | [Subject line] | [Content summary] | [CTA text] | [Metric + target] |
| 4 | [var] | Shipped | Email + SMS | [Subject line] | [Content summary] | [CTA text] | [Metric + target] |
| 5 | [var] | Delivered | SMS | [Message preview] | [Content summary] | [CTA text] | [Metric + target] |
| 6 | D+1 | Delivered +1 | Email | [Subject line] | [Content summary] | [CTA text] | [Metric + target] |
| 7 | D+5 | Delivered +5 | Email/SMS | [Subject line] | [Content summary] | [CTA text] | [Metric + target] |
| 8 | D+12 | Delivered +12 | Email | [Subject line] | [Content summary] | [CTA text] | [Metric + target] |
| 9 | D+21 | Delivered +21 | Email | [Subject line] | [Content summary] | [CTA text] | [Metric + target] |
| 10 | D+30 | Delivered +30 | Email | [Subject line] | [Content summary] | [CTA text] | [Metric + target] |

*D = Delivery day. All post-delivery touchpoints are relative to confirmed delivery date.*

---

## 4. Content Briefs

### Touchpoint 1: Order Confirmation

**Channel:** Email
**Trigger:** Order placed (immediate)
**Subject line options:**
- Option A: [Subject]
- Option B: [Subject]

**Content structure:**
1. **Header:** Thank you + order summary
2. **Body section 1:** What happens next (timeline visual)
3. **Body section 2:** Expectation setting (what to prepare, when to expect delivery)
4. **Body section 3:** Brand story snippet (why this product matters)
5. **Footer CTA:** [Primary action]

**Tone guidance:** [e.g., Warm, excited, reassuring — emphasize they made a great choice]
**Visual requirements:** [e.g., Product hero image, shipping timeline graphic]
**Personalization tokens:** [e.g., {{first_name}}, {{product_name}}, {{estimated_delivery}}]

---

*[Repeat Content Brief structure for each touchpoint in the sequence]*

---

## 5. Metrics Dashboard

### Per-Touchpoint Metrics

| Touchpoint | Open Rate Target | CTR Target | Conversion Target | Current Baseline |
|------------|-----------------|------------|-------------------|-----------------|
| Order confirmation | 75%+ | 25%+ | N/A | [Current] |
| Shipping notification | 80%+ | 15%+ | N/A | [Current] |
| Product education | 45%+ | 12%+ | Guide completion 30%+ | [Current] |
| Review request | 35%+ | 8%+ | Review submission 12%+ | [Current] |
| Cross-sell | 30%+ | 5%+ | Purchase 4%+ | [Current] |

### Sequence-Level KPIs

| Metric | Current | Target (30 days) | Target (90 days) | Measurement Method |
|--------|---------|-------------------|-------------------|--------------------|
| Return rate | [X]% | [Y]% | [Z]% | [Platform/method] |
| 30-day repurchase rate | [X]% | [Y]% | [Z]% | [Platform/method] |
| Review submission rate | [X]% | [Y]% | [Z]% | [Platform/method] |
| NPS / CSAT | [X] | [Y] | [Z] | [Platform/method] |
| Avg. days to 2nd purchase | [X] | [Y] | [Z] | [Platform/method] |

---

## 6. A/B Testing Roadmap

### Month 1: Foundation Tests

| Test | Touchpoint | Variable | Variant A | Variant B | Success Metric | Duration |
|------|-----------|----------|-----------|-----------|----------------|----------|
| 1 | [Touchpoint] | Subject line | [Version A] | [Version B] | Open rate | 2 weeks |
| 2 | [Touchpoint] | Send time | [Time A] | [Time B] | Open rate | 2 weeks |
| 3 | [Touchpoint] | CTA copy | [Version A] | [Version B] | Click rate | 2 weeks |

### Month 2-3: Optimization Tests

| Test | Touchpoint | Variable | Hypothesis | Success Metric | Duration |
|------|-----------|----------|------------|----------------|----------|
| 4 | [Touchpoint] | Content format | [Hypothesis] | [Metric] | 3 weeks |
| 5 | [Touchpoint] | Channel swap | [Hypothesis] | [Metric] | 3 weeks |

---

## 7. Technical Implementation Notes

**Email platform:** [e.g., Klaviyo, Mailchimp, Omnisend]
**SMS provider:** [e.g., Postscript, Attentive, Klaviyo SMS]
**Shipping webhook source:** [e.g., Shopify, ShipStation, AfterShip]
**Key integration requirements:**
- [e.g., Delivery confirmation webhook to trigger post-delivery sequence]
- [e.g., Product category tag to select correct content template]
- [e.g., SMS consent status check before sending SMS touchpoints]

**Suppression rules:**
- Suppress cross-sell if customer already made second purchase
- Suppress review request if customer already submitted review
- Suppress all onboarding if customer initiated return
- Respect SMS quiet hours (9am-9pm local time)
