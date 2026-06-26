# LTV Segmentation Campaign Output Template

**Campaign Name:** [e.g., "Q2 2026 LTV Optimization Launch"]
**Business Unit:** [e.g., "US DTC - Subscription"]
**Campaign Owner:** [Name]
**Data Refresh Date:** [YYYY-MM-DD]
**LTV Calculation Date:** [YYYY-MM-DD]
**Expected Launch Date:** [YYYY-MM-DD]

---

## Campaign Summary

| Metric | Value |
|---|---|
| Total Active Customers | [n] |
| Total Revenue (Last 12 Months) | [$$] |
| Average Customer LTV | [$$] |
| Revenue Concentration (Top 10% of customers) | [%] |
| Segments Included in Campaign | [n] |
| Estimated Incremental Revenue (30-day projection) | [$$] |
| Email Sends (30-day forecast) | [n] |
| SMS Sends (30-day forecast) | [n] |

---

## LTV Segment Overview

| Segment | Count | % of Base | Avg LTV | Total Revenue | Est. Monthly Spend (Email/SMS/Paid) | Key Metric |
|---|---|---|---|---|---|---|
| Champions (Top 1%) | [n] | [%] | [$$] | [$$] | [$$] | RPE Target: [$$] |
| VIP (Top 10%) | [n] | [%] | [$$] | [$$] | [$$] | RPE Target: [$$] |
| High-Value (Top 20%) | [n] | [%] | [$$] | [$$] | [$$] | RPE Target: [$$] |
| Mid-Tier (Mid 60%) | [n] | [%] | [$$] | [$$] | [$$] | RPE Target: [$$] |
| Low-Value (Bottom 20%) | [n] | [%] | [$$] | [$$] | [$$] | RPE Target: [$$] / Suppressed |
| Lapsed High-Value (180+ days inactive) | [n] | [%] | [$$] (peak) | [$$] | [$$] | Win-Back Priority |
| Lapsed Low-Value (180+ days inactive) | [n] | [%] | [$$] (peak) | [$$] | [$$] (minimal) | Suppress or single email |

**Notes:**
- Revenue concentration: Revenue from top [X]% of customers = [%] of total annual revenue
- Churn rate by segment (annualized): Champions [%] | VIP [%] | High-Value [%] | Mid-Tier [%] | Low-Value [%]
- Segment migration (last 90 days): [X] customers moved from Mid-Tier → High-Value; [X] from High-Value → VIP; [X] from VIP → Champions

---

## Champions (Top 1% LTV)

**Segment Definition:**
- LTV Threshold: >[threshold]
- Acquisition Cohorts Included: [e.g., "Jan 2023 forward, minimum 12 months post-purchase"]
- RFM Overlay: Active (0–30 days since purchase) or Warm (31–60 days)
- Size: [n] customers | [%] of base
- Avg LTV: [$$] | Total Revenue: [$$]

**Email Strategy:**
- Frequency: 2–3x per week + weekly SMS + monthly phone outreach (for top 5% by LTV)
- Content Mix: 60% exclusive/early access, 20% educational/thought leadership, 20% promotional
- Cadence: [Specific send dates/triggers]
  - Tuesday 10am ET: "Founder's Letter" or CEO insights (exclusive to Champions)
  - Thursday 2pm ET: Product launch pre-access (48-hour early window)
  - Sunday 6pm ET: Weekly curated picks or trend forecast
- Unsubscribe Rate Target: <0.2% | Open Rate Target: >45% | Click Rate Target: >15%

**Offer Strategy:**
- Primary: High-value, exclusive, non-discounted offers (limited edition early access, VIP experiences, personalization)
- Secondary: 20–30% off select premium products (only if engagement stalls for 45+ days)
- Incentive Example: "First 50 customers get exclusive [PRODUCT] + free priority shipping + $50 service credit" (vs. $50 discount)
- Never: Generic "20% off everything" broadcasts; treat these customers as partners, not transactional
- Upsell Logic: Category expansion (if purchased skincare, recommend wellness supplements or beauty tools); premium tier (if used product X, offer professional/subscription version)

**Reactivation Trigger & Rules:**
- Trigger: 45 days since last purchase (proactive, before true churn risk)
- Day 1 (Email): "We've reserved exclusive early access—just for you" — personalized re-engagement, emphasis on exclusivity
- Day 5 (Phone/SMS): Concierge outreach — "Hi [NAME], checking in on [PRODUCT]—how's it working? I'd like to share something new reserved for our best customers"
- Day 12 (Email): Product recommendation based on purchase history + offer (25–30% off premium item or exclusive experience)
- If No Response by Day 30: Escalate to [Account Manager/CEO] for personal outreach if LTV >$[threshold]
- Suppression: Never suppress from any channel unless explicitly unsubscribed

**Platform Setup:**
- Klaviyo: Segment = "Champions" (LTV >[threshold] AND active/warm RFM)
- Shopify Tags: "champion", "vip", "priority_support"
- Advertising: Include in Facebook Custom Audience "Champions—Retention & Upsell"; bid aggressively on engagement campaigns
- CRM/Zendesk: Create "VIP" tag; route inbound inquiries to senior support team
- Email List Cleanliness: Monthly review of bounce rates, hard bounces removed immediately

**Success Metrics (30-day window):**
- Revenue Per Email (RPE): [$$] (target: [$$])
- Unsubscribe Rate: <0.2%
- Win-back Conversion Rate: [%]
- Reactivation Revenue: [$$]
- NPS from Champions: [score target]

---

## VIP (Top 10% LTV)

**Segment Definition:**
- LTV Threshold: [threshold low] – [threshold high]
- Size: [n] customers | [%] of base
- Avg LTV: [$$] | Total Revenue: [$$]

**Email Strategy:**
- Frequency: 2–3x per week + bi-weekly SMS
- Content Mix: 50% exclusive offers, 30% early access, 20% community/social proof
- Cadence: [Specific dates]
  - Monday 10am ET: New arrival or exclusive collection
  - Wednesday 2pm ET: VIP-only discount (15–20% off select items)
  - Friday 6pm ET: Weekend feature or limited-time offer
- Unsubscribe Rate Target: <0.3% | Open Rate Target: >35% | Click Rate Target: >10%

**Offer Strategy:**
- Primary: 15–20% off exclusive or premium products; tiered loyalty discounts; exclusive access to new categories
- Secondary: Subscription incentives (10% off annual plan for VIPs); bundle offers combining complementary products
- Incentive Example: "VIP exclusive: 20% off + free gift with order over $[amount] + entry into monthly VIP giveaway"
- Upsell Logic: Frequency acceleration (if monthly purchaser, encourage twice-monthly via incentive); category expansion (if 1–2 categories, introduce 3rd category with discount)

**Reactivation Trigger & Rules:**
- Trigger: 60 days since last purchase
- Day 1 (Email): "VIP early access—new collection for members only"
- Day 8 (Email): "Your exclusive discount expires Friday" — scarcity/urgency
- Day 15 (SMS): Personal message from brand with discount code
- Day 22 (Email): Product recommendation + 15% off (stepped down from initial 20%)
- Suppression: Suppress from generic broadcast promotions after 90+ days inactivity; maintain SMS engagement

**Platform Setup:**
- Klaviyo: Segment = "VIP" (LTV [threshold low]–[high] AND active RFM OR active within 90 days)
- Shopify Tags: "vip"
- Advertising: Include in "VIP Retention" audience; test SMS retargeting for inactive 60+ days
- Email List: Clean monthly; maintain <2% bounce rate
- SMS Preference: Default to 2x per week unless customer manually adjusts

**Success Metrics (30-day window):**
- RPE: [$$] (target: [$$])
- Unsubscribe Rate: <0.3%
- Reactivation Rate: [%]
- Subscription Conversion Rate (if applicable): [%]

---

## High-Value (Top 20% LTV)

**Segment Definition:**
- LTV Threshold: [threshold low] – [threshold high]
- Size: [n] customers | [%] of base
- Avg LTV: [$$] | Total Revenue: [$$]

**Email Strategy:**
- Frequency: 2–3x per week
- Content Mix: 60% promotional/offers, 25% product education, 15% brand narrative
- Cadence: [Specific dates]
  - Tuesday 10am ET: Weekly deal or flash sale
  - Thursday 3pm ET: Featured product or category promotion
  - Saturday 9am ET: Weekend special or bundle offer
- Unsubscribe Rate Target: <0.4% | Open Rate Target: >28% | Click Rate Target: >8%

**Offer Strategy:**
- Primary: 20–30% off most products; bundle discounts (buy 2 get 15% off); loyalty tier enrollment incentive
- Secondary: Frequency acceleration rewards ("Buy 3 times this month, get $[amount] credit")
- Incentive Example: "High-Value Exclusive: 25% off + free shipping over $75 + earn 2x loyalty points this weekend"
- Upsell Logic: Bundle-driven (pair frequently purchased items at discount); frequency incentive (if 1x/month purchaser, incentivize 2x with offer)

**Reactivation Trigger & Rules:**
- Trigger: 90 days since last purchase
- Day 1 (Email): "We miss you—exclusive 25% off inside"
- Day 10 (Email): "Last chance—25% off expires tonight"
- Day 20 (Email): Stepped down offer (20% off) with product recommendation
- Suppression: Suppress from SMS and push after 120+ days inactivity

**Platform Setup:**
- Klaviyo: Segment = "High-Value" (LTV [low]–[high] AND activity status)
- Shopify Tags: "high_value", "frequent_buyer"
- Advertising: Include in "Frequency Acceleration" campaigns; test SMS for active customers
- Loyalty Program: Automatically enroll (if applicable); give bonus points for signup

**Success Metrics (30-day window):**
- RPE: [$$]
- Repeat Purchase Rate: [%] (goal: increase frequency)
- Loyalty Enrollment: [%] of segment
- Reactivation Rate: [%]

---

## Mid-Tier (Mid 60% LTV)

**Segment Definition:**
- LTV Threshold: [threshold low] – [threshold high]
- Size: [n] customers | [%] of base
- Avg LTV: [$$] | Total Revenue: [$$]

**Email Strategy:**
- Frequency: 1–2x per week
- Content Mix: 70% promotional/offers, 20% product highlights, 10% brand narrative
- Cadence: [Specific dates]
  - Wednesday 10am ET: Weekly promotion or sale
  - Sunday 6pm ET: Weekend deal or new arrivals
- Unsubscribe Rate Target: <0.5% | Open Rate Target: >22% | Click Rate Target: >6%

**Offer Strategy:**
- Primary: 25–35% off broad selection; second-purchase incentives ("Spend $[amount], save [%]"); bundle discounts
- Secondary: Free shipping thresholds; loyalty program enrollment with signup bonus
- Incentive Example: "New Customer Exclusive: 30% off your next order + free shipping when you buy 2+ items"
- Upsell Logic: Second-purchase conversion (if customer has only 1 order, incentivize second); cross-category (if purchased in one category, recommend complementary category at discount)

**Reactivation Trigger & Rules:**
- Trigger: 120 days since last purchase
- Day 1 (Email): "Special offer—35% off everything inside"
- Day 15 (Email): "Final call—35% off expires this week"
- Day 30 (Email): Stepped down offer (25% off) with curated product recommendations
- Suppression: Suppress from SMS/push and most broadcast campaigns after 150+ days inactivity

**Platform Setup:**
- Klaviyo: Segment = "Mid-Tier" (LTV [low]–[high])
- Shopify Tags: "mid_tier"
- Advertising: Lower priority for paid social; use in organic/owned channel campaigns
- Email Frequency: Cap at 2x/week to manage unsubscribe risk
- Cleanup: Monitor bounce rate; remove hard bounces monthly

**Success Metrics (30-day window):**
- RPE: [$$]
- Second Purchase Conversion: [%] of segment
- Reactivation Rate: [%]
- Cost per Acquisition of Repeat: [$$]

---

## Low-Value (Bottom 20% LTV)

**Segment Definition:**
- LTV Threshold: <[threshold]
- Size: [n] customers | [%] of base
- Avg LTV: [$$] | Total Revenue: [$$]

**Email Strategy (Minimal Engagement):**
- Frequency: 1x per week OR suppressed entirely (recommend suppression if LTV <$[threshold])
- Content Mix: 90% promotional, 10% brand narrative (keep messaging minimal)
- Cadence: [Specific date] or [Suppressed]
  - Thursday 10am ET: Single weekly deal email
- Unsubscribe Rate Target: <0.6% (expect higher; margin is thin)

**Offer Strategy:**
- Primary: 30–40% off broad selection; deep discounts to drive volume; free shipping thresholds; bundle discounts
- Secondary: Minimal—focus on volume, not margin
- Incentive Example: "Everything 30% off this week" or "Free shipping on any order"
- Suppress High-Cost Channels: NO SMS, NO paid social retargeting, NO push notifications
- Upsell Logic: Minimal; focus on conversion to mid-tier via volume discounts and low-friction checkout

**Reactivation Trigger & Rules:**
- Trigger: 180 days since last purchase OR suppressed from all communications
- Day 1 (Email): Single re-engagement offer (30–40% off) if LTV was not trivial (e.g., >$50 lifetime)
- If No Response: Suppress permanently from all channels except annual clearance or post-acquisition windows
- No Win-Back Campaigns: Do not execute high-touch win-back (margin cannot support it)
- Segment Logic: After 180+ days inactive, remove from all email/SMS/paid channels; maintain only for organic/search remarketing

**Platform Setup:**
- Klaviyo: Segment = "Low-Value" (LTV <[threshold])
- Suppression List: Create "Low-Value Suppressed" list; exclude from all broadcasts, SMS, push after 90+ days inactive
- Shopify Tags: "low_value", "suppress_paid"
- Advertising: Do NOT include in paid social retention campaigns; exclude from SMS audiences entirely
- Email Frequency Cap: 1x/week maximum; better to suppress than over-email
- List Cleanup: Aggressive list hygiene; remove hard bounces and unengaged weekly

**Platform Setup:**
- Data Trigger: Any customer in this segment >90 days inactive should be moved to "Suppressed—Low-Value" list
- Success Metrics: Primarily cost reduction (lower email volume = lower ESP cost), NOT revenue growth

---

## Lapsed High-Value (180+ Days Inactive, Previously Top 20% LTV)

**Segment Definition:**
- Previous LTV: >[threshold]
- Inactivity: 180+ days since last purchase
- Size: [n] customers | [%] of base
- Estimated Peak Annual Spend: [$$] per customer (when active)

**Reactivation Playbook (Priority: AGGRESSIVE WIN-BACK):**
- Trigger: Any previously high-value or champion customer hitting 180-day inactivity
- Channel Priority: Email + SMS + phone (for LTV >$[threshold])
- Offer Depth: 30–40% off (significantly higher than standard campaigns)
- Messaging Tone: Personal, care-focused, "we noticed you're gone"

**Sequence (45-day win-back):**

**Week 1:**
- Day 1 (Email): "We're sorry you're gone—here's 40% off your favorite category"
  - Subject: "[NAME], we want you back" or "You're missed—exclusive offer inside"
  - Copy: Reference past purchases; acknowledge absence; make offer urgent and clear
  - Offer: 40% off previously purchased category
  - CTA: "Shop Your Favorites"
- Day 3 (SMS): "Hi [NAME]—we set aside 40% off for you. Shop now: [LINK] or reply to chat"
  - High urgency, direct, personal
  - Response: SMS 2-way conversation option if set up
- Day 5 (Email): "Your 40% off expires in 2 days—[CATEGORY] refreshed while you were away"
  - Scarcity/urgency
  - Social proof: "Customers like you are loving [PRODUCT]"
  - CTA: "Redeem 40% Off"

**Week 2:**
- Day 10 (Phone Call, if LTV >$[threshold]): Personal outreach from account manager or concierge
  - Script: "Hi [NAME], I'm [NAME] from [BRAND]. We noticed you haven't visited in a while. I wanted to personally check in—are you still [PRODUCT] or would something new be helpful?"
  - Offer: Email to follow with exclusive incentive based on conversation
  - Log conversation in CRM
- Day 12 (Email if No Phone Response): "Personal note from [TEAM]—let's find what works for you"
  - Softer tone; less salesy
  - Offer: Same 40% off; add concierge consultation (20-min call)
  - CTA: "Let's Talk"

**Week 3:**
- Day 18 (Email): "Last chance—40% off + [PREMIUM BENEFIT] expires Sunday"
  - Final push before offer expires
  - Add time-based urgency: "2 days left"
  - Premium benefit: Free upgrade, extended warranty, priority shipping
- Day 21 (SMS if opted in): "Final notice—40% off [CATEGORY] ends tonight. [LINK]"
  - Short, direct, last-chance message

**Week 4+:**
- Day 30 (Email if still inactive): Stepped-down offer (30% off) + product recommendation
  - "We've picked [PRODUCT] based on what you loved"
  - Tone: Helpful, not salesy
- Day 45 (Email if still inactive): Final re-engagement attempt
  - Single offer (25% off) with feedback request: "What would bring you back?"
  - Post-45 day: Suppress from win-back campaigns if no engagement; move to suppression list or annual re-engagement only

**Platform Setup:**
- Segment Identification: Automated flag in Klaviyo: "Lapsed High-Value" (LTV >[threshold] AND last purchase >180 days ago)
- Workflow: Trigger email immediately upon 180-day mark
- SMS Integration: Enroll in SMS-enabled sequences (confirm SMS opt-in first)
- Phone Escalation: Flag for account manager if LTV >$[threshold]
- Tracking: Tag all win-back responses with "lapsed-reactivated" for attribution
- Control Group: Hold 20% control group; do not send any communications to measure lift

**Success Metrics (45-day window):**
- Win-Back Conversion Rate: [%] (industry benchmark: 20–40%)
- Revenue from Reactivations: [$$]
- ROI on Win-Back Campaign: [ratio] (account for email, SMS, phone costs)
- Average Order Value (reactivated customers): [$$] vs. baseline [$$]
- Repeat Rate (reactivated customers after 90 days): [%]

---

## Lapsed Low-Value (180+ Days Inactive, Previously Bottom 20% LTV)

**Segment Definition:**
- Previous LTV: <[threshold]
- Inactivity: 180+ days since last purchase
- Size: [n] customers | [%] of base
- Strategy: Minimal or suppressed intervention

**Reactivation Playbook (Priority: LOW—SUPPRESS OR MINIMAL TOUCH):**
- Strategy: Suppress from all channels OR single low-cost re-engagement email
- Rationale: Margin math does not support multi-touch win-back; cost of campaigns exceeds expected LTV recovery
- Approach: Suppress by default; only include in annual re-engagement or promotional event

**Option 1: Suppress (Recommended)**
- Segment Setup: Create "Suppressed—Lapsed Low-Value" list
- Exclusion Rules: Exclude from all email broadcasts, SMS, push, paid social after 180+ days inactivity
- Retention: Keep in database for reference; do not delete (potential future value)
- Annual Re-engagement: Once per year (e.g., January New Year offer or post-holiday), send single re-engagement email: "We're back with something new—20% off everything"

**Option 2: Single Touch (If Testing Reactivation)**
- Day 1 (Email only): "It's been a while—come back to [BRAND]"
  - Subject: Soft, non-promotional ("We've Missed You" vs. "50% Off Inside")
  - Copy: Brief, friendly, minimal sell
  - Offer: 20–25% off (lower than high-value, but competitive)
  - CTA: "Explore What's New"
- Post-Email: If no response within 14 days, suppress permanently; no follow-up sequences

**Platform Setup:**
- Suppression List: "Lapsed-Low-Value-Suppressed" — exclude from all broadcasts, SMS, paid social
- Annual Exception: Include in single annual re-engagement campaign
- Tagging: "suppress_low_value", "inactive_180+"
- Cleanup: Monitor for bounces; remove after 3 bounces

**Success Metrics:**
- Primary Metric: **Cost Savings** (reduced email/SMS volume = lower ESP spend)
- Secondary Metric: Annual re-engagement open rate [%], but do not expect high conversion
- Avoid: Do not expect significant win-back revenue; segment is optimized for margin protection, not recovery

---

## RFM Overlay & Composite Scoring

Apply RFM (Recency, Frequency, Monetary) scoring on top of LTV segmentation to identify at-risk or high-opportunity customers within each tier.

**Recency Scoring (0–100):**
- 0–30 days since last purchase: Score 100 (Active)
- 31–60 days: Score 75 (Warm)
- 61–90 days: Score 50 (Cool)
- 91–180 days: Score 25 (Cold)
- 180+ days: Score 0 (Lapsed)

**Frequency Scoring (0–100):**
- 5+ purchases in 12 months: Score 100
- 3–4 purchases: Score 75
- 2 purchases: Score 50
- 1 purchase in 12 months: Score 25
- 0 purchases (new): Score 0 (handle separately)

**Monetary Scoring (0–100):**
- Total 12-month spend >[90th percentile]: Score 100
- [70th–90th percentile]: Score 75
- [50th–70th percentile]: Score 50
- [30th–50th percentile]: Score 25
- <[30th percentile]: Score 0

**Composite Churn Risk Score:**
- Formula: 100 - ((Recency × 0.5) + (Frequency × 0.3) + (Monetary × 0.2))
- Interpretation:
  - 0–30: Very Low Risk (active, frequent, high spend)
  - 31–50: Low Risk (active or high frequency)
  - 51–70: Moderate Risk (cooling off or declining frequency)
  - 71–85: High Risk (cold and declining patterns)
  - 86–100: Critical Risk (lapsed or one-time buyers)

**Action Triggers by Segment & Risk Score:**
- **Champions + High Risk (>70):** Immediate phone outreach + premium win-back offer
- **VIP + Moderate Risk (51–70):** Email + SMS re-engagement sequence
- **High-Value + Moderate Risk (51–70):** Email re-engagement sequence
- **Mid-Tier + High Risk (71–85):** Single email re-engagement
- **Any Segment + Critical Risk (>85):** Suppress or single outreach depending on LTV
ngle email re-engagement; suppress after no response
- **Low-Value + Critical Risk (86–100):** Suppress from all channels

---

## Email Suppression Rules

Apply these rules to all segments to optimize list health and margin:

| Condition | Action |
|---|---|
| Hard bounce or permanently invalid email | Remove immediately from all sends |
| Multiple complaints/abuse reports | Suppress immediately; flag in CRM |
| Unsubscribed (any reason) | Honor immediately; do not send any communications |
| Low-Value + 90+ days inactive | Move to suppression list; suppress from all channels except annual campaign |
| Mid-Tier + 150+ days inactive | Suppress from SMS and push; retain on email quarterly |
| High-Value + 120+ days inactive | Suppress from SMS and push; retain on email at reduced frequency |
| VIP + 90+ days inactive | Suppress from paid social and push; maintain email + SMS |
| Champions + any inactivity | Never suppress; escalate for win-back |
| Complained about frequency (>3 unsubscribes from segment) | Reduce frequency by 50%; offer preference center |
| Do Not Mail list / legal suppression | Suppress globally; never override |
| Opted out of SMS | Exclude from all SMS sequences; retain email if opted in |

---

## Platform-Specific Setup Notes

### Klaviyo
- Create segment for each LTV tier using LTV custom attribute
- Build automation workflow: LTV re-calc monthly → segment assignment → trigger appropriate flow
- RFM overlay: Use Klaviyo's predictive analytics (if available) or manual scoring via custom property
- Suppression list: Create global suppression segment, exclude from all broadcasts
- Email list cleanup: Use Klaviyo's list validation; remove hard bounces after 1 bounce, soft bounces after 2
- SMS campaigns: Require explicit SMS opt-in; maintain separate SMS list per segment

### Shopify
- Create customer tags: "champion", "vip", "high_value", "mid_tier", "low_value"
- Automated tagging: Use Shopify Apps (e.g., Judgify, Judge.me) or manual script to assign tags based on LTV
- Segment isolation: Use tags to exclude/include customers in Shopify campaigns
- Note: Shopify's native email tool has limited segmentation; recommend connecting to Klaviyo for full LTV workflows

### Facebook/Instagram Ads
- Custom Audiences: Create Custom Audiences for "Champions," "VIP," "High-Value" (use email list upload)
- Lookalike Audiences: Build Lookalike Audiences from Champions and VIP for new customer acquisition
- Exclusion Audiences: Exclude Low-Value and Lapsed Low-Value from retention campaigns to reduce ad spend waste
- Bid Strategy: Bid aggressively on Champions/VIP retention campaigns; bid down on Mid-Tier and Low-Value
- Frequency Cap: Champions/VIP 3–5x/week; Mid-Tier 2–3x/week; Low-Value 1x/week or excluded

### SMS (Twilio, Attentive, or similar)
- Segment Routing: Create segment-specific SMS flows based on LTV and RFM
- Frequency: Champions 1–2x/week; VIP 1–2x/week; High-Value 1x/week; Mid-Tier 1x/week; Low-Value suppressed
- Opt-In Management: Require explicit SMS opt-in for VIP and Champions; optional for others
- Compliance: Honor SMS opt-out immediately; maintain DNC list and legal compliance

### Email Service Provider (e.g., Klaviyo, Iterable)
- List Segmentation: Create separate lists or segments for each LTV tier
- Unsubscribe Management: Segment-specific unsubscribe links and preference centers
- List Cleanliness: Remove hard bounces within 1 day; monitor spam complaints weekly
- Seed List Testing: Use segment-specific seed lists for QA before send

---

## Success Metrics & Reporting Dashboard

### Primary KPIs (Monthly Review)
| Metric | Target | Owners |
|---|---|---|
| Revenue Per Email (RPE) by Segment | Champions [$$] \| VIP [$$] \| High-Value [$$] \| Mid-Tier [$$] \| Low-Value [$$] | Marketing Manager |
| Unsubscribe Rate by Segment | <0.2% (Champions) \| <0.3% (VIP) \| <0.4% (High-Value) \| <0.5% (Mid-Tier) \| <0.6% (Low-Value) | Email Manager |
| Repeat Purchase Rate (30-day window) | Champions [%] \| VIP [%] \| High-Value [%] \| Mid-Tier [%] \| Low-Value [%] | Product Manager |
| Segment Migration (Month-over-Month) | [%] of Mid-Tier → High-Value; [%] of High-Value → VIP; [%] of VIP → Champions | Analyst |
| Win-Back Conversion Rate (Lapsed High-Value) | [%] reactivated within 45 days | Campaign Manager |
| Cost Per Acquisition (by segment) | Champion [$$] \| VIP [$$] \| High-Value [$$] | Finance |

### Secondary KPIs (Quarterly Review)
- Email Open Rates by Segment
- Click-Through Rates by Segment
- AOV (Average Order Value) by Segment
- Customer Lifetime Value Growth (quarter-over-quarter)
- Churn Rate by Segment (annualized)
- Net Promoter Score (NPS) by Segment
- Segment Stickiness (% of customers remaining in same segment after 90 days)

---

## Data Flags & Alerts

Flag these conditions for immediate investigation:

| Flag | Condition | Threshold | Action |
|---|---|---|---|
| LTV Calculation Error | Segment contains customers <[X] days post-acquisition | >5% of segment | Recalculate; exclude new cohorts |
| Bounce Rate Spike | Email list bounce rate increases >2% month-over-month | Per segment | Review data quality; clean bounces |
| Churn Acceleration | Segment churn rate increases >2% from trailing 3-month average | Per segment | Analyze for product/external issues; adjust campaign frequency |
| Segment Size Anomaly | Segment shrinks >15% month-over-month | Per segment | Investigate customer migration; validate LTV calculation |
| Unsubscribe Spike | Unsubscribe rate increases >0.5% from baseline | Per segment | Review email copy, frequency; test frequency reduction |
| RPE Decline | RPE declines >20% from trailing 3-month average | Per segment | Analyze offer effectiveness; test offer depth or product |
| Compliance Issue | Bounce rate >10% or SPAM complaint rate >0.3% | Per segment | Stop campaigns; audit list health; comply with CAN-SPAM |

---

## Approval & Sign-Off

**Campaign Approval:**
- [ ] LTV calculation validated by [Finance/Analytics]
- [ ] Segment definitions approved by [Product/CMO]
- [ ] Email templates approved by [Compliance/Brand]
- [ ] Offers approved by [Merchandising/Finance]
- [ ] Platform setup tested by [Marketing Ops]
- [ ] List cleanliness verified by [Data Quality]

**Campaign Launch Checklist:**
- [ ] Suppression lists finalized and loaded
- [ ] Automation workflows built and tested
- [ ] Email templates QA'd across devices
- [ ] Control groups defined and isolated
- [ ] Success metrics dashboard live and monitoring
- [ ] Team trained on segment strategy
- [ ] Launch communication sent to stakeholders

**Post-Launch Review:**
- Review performance metrics at [72 hours], [1 week], [2 weeks], [30 days]
- Document learnings and optimization recommendations
- Schedule quarterly segment recalibration
