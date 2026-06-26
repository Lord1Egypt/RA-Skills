# Journey Mapping Methodology Guide

Deep-dive reference on journey mapping methodology for ecommerce contexts. Use alongside the main SKILL.md workflow.

---

## Data Collection Approaches

### Quantitative Data Sources

**Web and App Analytics:** Collect at minimum 90 days of data. Key extracts: traffic by source/medium (new vs. returning), page-level metrics (views, bounce rate, time on page, exit rate), event tracking (add to cart, begin checkout, purchase, search queries), funnel step-by-step drop-off, device/browser breakdown, geographic data.

**Ecommerce Platform Analytics:** Prioritize platform-specific reports:
- Shopify: conversion rate funnel, returning customer rate, AOV trends, product views-to-purchase ratio, cart analysis
- Amazon: Brand Analytics (search query performance, repeat purchase behavior, market basket), Business Reports (detail page views, unit session percentage, Buy Box %), advertising search term reports
- TikTok Shop: video views to product clicks, shop tab traffic, live shopping metrics, creator affiliate performance

**Advertising Data:** Campaign and ad-level performance across all paid channels: impressions, reach, frequency, CTR, CPC, CPA, audience segment performance, creative performance, landing page performance tied to campaigns, view-through and assisted conversions.

**Email/SMS Analytics:** Performance for every automated flow and campaign: delivery rate, open rate, click rate, conversion rate, revenue per email, unsubscribe rate, list growth rate, segment-level performance, flow completion rates.

### Qualitative Data Sources

**Customer Reviews:** Categorize by theme (product quality, shipping, service, value, packaging, ease of use). Track sentiment over time. Focus on 2-3 star reviews for balanced detail. Note recurring language customers use.

**Support Ticket Analysis:** Categorize by journey stage. Identify top 10 inquiry types. Calculate resolution time by category. Track repeat contacts as severe friction indicators.

**Session Recordings:** Watch 20-30 recordings per key page across device types. Note rage clicks, u-turns, dead zones. Compare heatmaps between converting and non-converting sessions. Document scroll depth drop-off and form field hesitation.

**Customer Interviews:** Recruit 5-10 across outcomes (completed purchase, abandoned cart, one-time, repeat). Use open-ended prompts: "Walk me through how you first heard about us." Probe emotional states and alternatives considered. Capture verbatim quotes.

---

## Touchpoint Identification Techniques

### Channel Mapping Matrix

Create a matrix of every active channel at each stage:

| Channel | Awareness | Consideration | Evaluation | Purchase | Onboarding | Retention | Advocacy |
|---|---|---|---|---|---|---|---|
| Paid Search | X | X | | | | | |
| Paid Social | X | X | | | | X | |
| Organic Search | X | X | X | | | | |
| Email | | X | X | | X | X | X |
| SMS | | | | X | X | X | |
| Website | | X | X | X | | X | X |
| Marketplace | X | X | X | X | | X | X |
| Physical Product | | | | | X | X | X |
| Customer Service | | | X | X | X | X | |

### Micro-Touchpoint Identification

Within major touchpoints, identify specific interactions: hero image, headline, price display, reviews widget, trust badges, CTA button, navigation, pop-ups, chat widget, promo code field, shipping options, payment selection, order confirmation elements, product insert contents.

### Cross-Device Journey Tracking

Document device-switching patterns (e.g., mobile discovery, desktop purchase). Map where handoffs create friction (carts not syncing, login required). Note platform device biases (TikTok nearly all mobile). Check whether analytics properly attribute cross-device journeys.

---

## Emotion Mapping

### Emotion Categories

**Positive:** Curiosity (compelling creative), Excitement (product discovery, deal finding), Confidence (social proof, clear info), Delight (exceeding expectations), Pride (smart decisions, brand association)

**Negative:** Confusion (unclear navigation, complex processes), Skepticism (unsubstantiated claims, few reviews), Anxiety (high prices, unclear returns, data security), Frustration (errors, slow loads, poor support), Disappointment (product mismatch, slow delivery)

### Emotion Intensity Scoring

Rate each touchpoint from -5 to +5:
- **-5 to -3:** Severe/moderate negative, likely causes abandonment
- **-2 to -1:** Mild negative, creates friction
- **0:** Neutral, functional interaction
- **+1 to +2:** Mild/moderate positive, builds momentum
- **+3 to +5:** Strong positive, creates memorable moments and advocacy

Plot chronologically to create an emotional curve. Consistent negative slope signals deteriorating experience. Peaks followed by valleys indicate expectation failures.

### Emotion-to-Action Mapping

| Emotion | Likely Behavior | Intervention |
|---|---|---|
| Confusion | Bounce, back button, support contact | Clearer UX, better info hierarchy |
| Skepticism | Competitor comparison, review seeking | Social proof, trust signals, guarantees |
| Anxiety | Cart abandonment, hesitation | Risk reversal, reassurance, support access |
| Frustration | Rage clicks, site exit, negative review | Technical fixes, process simplification |
| Excitement | Quick progression, add-ons, sharing | Cross-sell, sharing prompts |
| Confidence | Steady progression, larger basket | Upsell, subscription offers |

---

## Friction Diagnosis Framework

### The STOP Framework

**S - Spot:** Where exactly? Specific page, element, step, and moment in the timeline.

**T - Type:** What category?
- Technical: load speed, broken links, payment failures, device compatibility
- Informational: missing details, unclear copy, confusing navigation
- Emotional: trust gaps, price shock, decision fatigue, commitment anxiety
- Procedural: too many steps, forced account creation, complex returns

**O - Outcome:** What happens? Complete abandonment, temporary delay, channel switch, support escalation, or reduced satisfaction.

**P - Priority:** How to rank? Calculate frequency x severity x revenue at stake. Classify as must-fix (blocking revenue), should-fix (impacting experience), or could-fix (nice improvement).

### Friction Heat Map

Plot friction severity across stages and channels in a grid. Patterns reveal: a column of red across one stage = stage-level problem; a row of red across one channel = channel-level problem; scattered points = individual issues; friction at transitions = handoff problems.

---

## Cross-Channel Analysis

### Consistency Audit

For each channel pair, evaluate: messaging consistency (do promises match?), visual consistency (same brand feel?), pricing consistency (same prices/promos?), information consistency (same specs/availability?), experience quality consistency.

### Handoff Quality Assessment

Evaluate every channel transition: ad to landing page (does it deliver on the promise?), social to website (same tone?), email to product page (matches offer?), website to marketplace (consistent presentation?), digital to physical (unboxing matches online brand?), support to self-service (seamless transition?).

---

## Persona-Based Journey Variations

### When to Create Separate Maps

Create separate maps when segments differ significantly by: acquisition channel (TikTok vs. Google search), purchase intent (gift vs. self-buyer), lifecycle stage (first-time vs. returning), platform (Amazon vs. Shopify), or price sensitivity (deal-hunter vs. premium buyer).

### Persona Template

For each persona document: name and description, primary acquisition channel, decision-making style (impulsive vs. research-intensive), key criteria (price, quality, reviews, convenience), typical device journey, emotional baseline (confident vs. skeptical), post-purchase behavior (one-time vs. repeat vs. advocate), and journey duration (hours to months).

---

## Advanced Techniques

**Cohort Analysis:** Compare journeys by acquisition cohort (month), channel cohort (paid vs. organic), product cohort (entry product), and value cohort (high vs. low AOV).

**Journey Velocity:** Measure time from first visit to add-to-cart, add-to-cart to purchase, and purchase to second purchase. Also track sessions and touchpoints before conversion. Slow velocity at a stage indicates friction.

**Competitive Benchmarking:** Map simplified competitor journeys to identify stages where they provide superior experience, touchpoints they offer that you lack, and post-purchase programs driving higher retention.
