---
name: customer-churn-prediction-analyst
description: "Analyze customer behavior patterns and predict churn risk across Stripe, Shopify, and SaaS platforms. Identify at-risk accounts, generate personalized intervention recommendations, and track win-back success. Use when the user needs to prevent customer attrition, prioritize retention efforts, or create targeted recovery campaigns."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["STRIPE_API_KEY","SHOPIFY_API_TOKEN","OPENAI_API_KEY"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📊"}}
---

# Customer Churn Prediction Analyst

## Overview

The **Customer Churn Prediction Analyst** is a production-grade intelligence tool that identifies at-risk customers before they leave. By analyzing multi-dimensional behavioral signals—purchase frequency trends, support ticket sentiment, feature adoption rates, engagement decay, and payment friction—this skill surfaces customers most likely to churn within 30/60/90 days.

Beyond prediction, it generates **actionable intervention playbooks**: personalized discount strategies, feature education campaigns, re-engagement email templates, and VIP outreach scripts. The skill integrates with **Stripe** (payment history, subscription metrics), **Shopify** (order patterns, product affinity), **SaaS platforms** (API usage logs, login frequency), and **Slack** (automated alerts for high-risk segments).

**Why it matters:** Research shows that acquiring a new customer costs 5-25x more than retaining an existing one. A 5% improvement in retention can increase profitability by 25-95%. This skill automates the intelligence layer that turns data into revenue protection.

---

## Quick Start

Try these prompts immediately:

### Example 1: Analyze Stripe Subscription Churn Risk
```
Analyze my Stripe customer base for churn risk. 
I have 1,200 active subscriptions ranging from $29-$299/month.
Look at: payment failures in the last 90 days, 
declining MRR trends, and customers who haven't logged in for 30+ days.
Generate a risk-ranked list of my top 50 at-risk accounts 
with specific intervention recommendations for each.
```

### Example 2: Shopify E-commerce Customer Retention
```
I run a Shopify store with 8,500 customers. 
Identify customers at risk of not returning.
Analyze: purchase frequency decline, 
average order value trends, cart abandonment patterns, 
and email engagement (bounces/unsubscribes).
Create win-back campaign templates for three risk tiers: 
High (80%+ churn probability), Medium (50-79%), Low (25-49%).
Include personalized discount offers and subject lines.
```

### Example 3: SaaS Feature Adoption & Engagement Churn
```
Analyze our SaaS platform for churn signals.
Our customers are: 120 paid accounts, 
avg contract value $5,000/month.
Track: API call volume (declining usage = risk), 
feature adoption (low-feature users churn 3x faster), 
support ticket sentiment (negative = escalation risk), 
and last login recency.
Flag accounts with <10 API calls/week or 
no logins in 14+ days as critical intervention targets.
Generate retention playbooks for each.
```

---

## Capabilities

### 1. **Multi-Source Behavioral Analysis**
Aggregates signals from multiple platforms into a unified churn risk model:

- **Stripe Integration:** Payment decline frequency, subscription downgrades, MRR trajectory, failed payment recovery attempts, dunning email effectiveness
- **Shopify Integration:** Purchase frequency (RFM: Recency, Frequency, Monetary), product category affinity, cart abandonment rate, average order value trends, customer lifetime value (CLV) projections
- **SaaS/API Platforms:** Daily active users (DAU), feature adoption rates, API call volume patterns, session duration trends, support ticket volume/sentiment, last-activity timestamps
- **Email/CRM Data:** Open rates, click-through rates, unsubscribe trends, email bounce rates, campaign engagement decay
- **Support Systems:** Ticket volume, resolution time, sentiment analysis (negative sentiment = 4x higher churn risk), escalation frequency

### 2. **Predictive Risk Scoring**
Generates 30/60/90-day churn probability scores using:

- **Recency Decay:** How long since last transaction/login (exponential weighting)
- **Frequency Trends:** Purchase/usage slope analysis (declining = risk signal)
- **Monetary Value:** Revenue-at-risk calculations; high-value customers flagged separately
- **Engagement Velocity:** Rate of engagement decline vs. historical baseline
- **Cohort Benchmarking:** Compare customer behavior to cohort norms (e.g., customers acquired in same month)
- **Seasonal Adjustment:** Account for industry seasonality (e.g., retail Q4 spikes)

**Output:** Risk tiers (Critical, High, Medium, Low) with confidence intervals.

### 3. **Personalized Intervention Recommendations**
Generates tailored win-back strategies:

- **Segment-Specific Offers:** High-value customers get VIP treatment (white-glove support, exclusive features); price-sensitive get discounts; feature-poor get education
- **Email Campaign Templates:** Pre-written re-engagement sequences with A/B test variants, personalized product recommendations, and dynamic subject lines
- **Feature Education Playbooks:** For SaaS: identify underutilized features that correlate with churn; generate feature demo videos, webinar invites, or one-on-one training offers
- **Support Escalation Triggers:** Route customers with 3+ negative support interactions to dedicated success managers
- **Win-Back Incentive Suggestions:** Recommend discount depth (5%, 10%, 20%) based on customer LTV, willingness-to-pay analysis, and competitive benchmarking

### 4. **Retention Campaign Orchestration**
Generates ready-to-deploy campaigns:

- **Multi-Channel Sequences:** Email → SMS → In-App Push → Slack notification → Phone outreach (for high-value accounts)
- **Timing Optimization:** Send interventions at peak engagement windows (e.g., Tuesday 10am for B2B SaaS)
- **Dynamic Content:** Personalized product recommendations, usage statistics, and social proof ("3 customers like you upgraded to Pro this month")
- **A/B Test Frameworks:** Generate variant subject lines, offer amounts, and CTA copy for testing

### 5. **Win-Back Success Tracking**
Monitors intervention effectiveness:

- **Conversion Metrics:** % of at-risk customers who re-engage, upgrade, or extend contracts post-intervention
- **ROI Calculation:** Cost per intervention vs. revenue recovered; payback period
- **Cohort Analysis:** Which intervention types work best for which customer segments?
- **Feedback Loop:** Continuous model refinement based on what interventions actually prevent churn

---

## Configuration

### Environment Variables (Required)
```bash
# Stripe integration
export STRIPE_API_KEY="sk_live_..."

# Shopify integration
export SHOPIFY_API_TOKEN="shppa_..."
export SHOPIFY_STORE_NAME="your-store.myshopify.com"

# SaaS/custom platform
export SAAS_API_KEY="your_saas_api_key"
export SAAS_API_ENDPOINT="https://api.yourplatform.com/v1"

# OpenAI (for recommendation generation)
export OPENAI_API_KEY="sk-..."

# Slack notifications (optional)
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."

# Database (for tracking historical interventions)
export DATABASE_URL="postgresql://user:pass@localhost/churn_db"
```

### Setup Instructions

1. **Authenticate with data sources:**
   ```bash
   # Stripe: Generate API key from Dashboard > Developers > API Keys
   # Shopify: Admin > Apps and Integrations > Develop Apps > Create API credentials
   # SaaS: Use your platform's API documentation
   ```

2. **Initialize the analysis:**
   ```bash
   # First run: full historical analysis (may take 5-10 minutes for large datasets)
   openclaw run customer-churn-prediction-analyst \
     --mode=full-analysis \
     --lookback-days=180 \
     --data-sources=stripe,shopify,saas
   ```

3. **Set up recurring analysis:**
   ```bash
   # Schedule weekly churn analysis
   openclaw schedule customer-churn-prediction-analyst \
     --frequency=weekly \
     --day=monday \
     --time=08:00 \
     --notify-slack=true
   ```

### Configuration Options
- `risk-threshold`: Churn probability threshold (default: 0.5 = 50%)
- `lookback-days`: Historical analysis window (default: 180 days)
- `prediction-horizon`: Predict churn within X days (default: 30, 60, 90)
- `high-value-threshold`: Revenue amount that triggers VIP intervention (default: $5,000 MRR)
- `intervention-budget`: Maximum discount/incentive per customer (default: 15% of CLV)

---

## Example Outputs

### Output 1: Churn Risk Report (JSON)
```json
{
  "analysis_date": "2025-01-15T10:30:00Z",
  "total_customers_analyzed": 1247,
  "churn_risk_distribution": {
    "critical": 23,
    "high": 87,
    "medium": 156,
    "low": 981
  },
  "at_risk_accounts": [
    {
      "customer_id": "cust_8x9y2z",
      "name": "Acme Corp",
      "mrr": 12500,
      "churn_probability_30d": 0.89,
      "churn_probability_60d": 0.76,
      "primary_risk_signals": [
        "API usage declined 65% in last 30 days",
        "Payment failed 2x (recovered 1x)",
        "Support ticket sentiment: negative (3 tickets)",
        "No login in 18 days"
      ],
      "recommended_intervention": {
        "type": "VIP_SAVE",
        "tactics": [
          "Schedule executive business review call",
          "Offer 20% discount + feature unlock for 3 months",
          "Assign dedicated success manager"
        ],
        "estimated_recovery_probability": 0.72,
        "estimated_clv_at_risk": 150000
      },
      "suggested_email_subject": "We miss you, Acme—here's what's new in Q1"
    }
  ],
  "revenue_at_risk": 487500,
  "recommended_intervention_budget": 73125,
  "estimated_roi": 5.7
}
```

### Output 2: Intervention Campaign Template
```markdown
## Re-Engagement Campaign: "Win Back Acme Corp"

**Target Segment:** High-value SaaS customers with 60%+ churn risk
**Timing:** Send Monday 9am PT
**Duration:** 3-week sequence

### Email 1: "We noticed you've been quiet"
Subject: Acme, we want to help—here's what's new [A/B variant: "Your exclusive preview inside"]

Hi [FirstName],

We noticed your team's API usage has dropped. That's usually a sign we haven't delivered enough value—and that's on us.

**Here's what we've shipped since you last logged in:**
- Real-time collaboration (your #1 feature request)
- 40% faster query performance
- New integrations: Salesforce, HubSpot, Slack

**Offer:** Upgrade to Pro free for 90 days + 1:1 onboarding session ($0 cost to you).

[Claim Offer Button]

Questions? Reply to this email or book time with Sarah, your success manager: [Calendly Link]

---

### Email 2: "Social Proof" (Day 5)
Subject: 3 customers like you switched to Pro this month—here's why

[Testimonials, case study, usage stats]

---

### Email 3: "Final Offer" (Day 14)
Subject: Last chance: 25% off Pro + dedicated support [Expires Friday]

[Time-limited offer, scarcity messaging]
```

### Output 3: Win-Back Success Dashboard
```
Churn Prevention Dashboard (Last 30 Days)

At-Risk Customers Identified:     156
Interventions Deployed:            143 (92%)
Re-Engaged (logged in post-email): 89 (62%)
Converted to Upgrade:              34 (24%)
Revenue Recovered:                 $47,300
Intervention Cost:                 $3,200
ROI:                               14.8x

Top Performing Interventions:
1. VIP Phone Call (67% re-engagement rate)
2. Feature Education Webinar (58%)
3. Discount Offer (35%)
4. Email Sequence (28%)
```

---

## Tips & Best Practices

### 1. **Segment Before Intervening**
Don't use one-size-fits-all offers. High-value customers respond better to white-glove service; price-sensitive segments respond to discounts. This skill auto-segments—use it.

### 2. **Timing is Everything**
Send interventions during peak engagement windows. For B2B SaaS, that's usually Tuesday-Thursday, 9-11am. For e-commerce, Friday evening often works best. Test and adjust.

### 3. **Feature Education Beats Discounts**
Customers who adopt 3+ core features have 10x lower churn. Before offering discounts, try feature education. It's cheaper and builds stronger retention.

### 4. **Track the Tracking**
Set up UTM parameters and unique promo codes for each intervention so you can measure ROI. Example: `utm_source=churn_email&utm_medium=reengagement&utm_campaign=acme_save`

### 5. **Weekly Monitoring Over Batch Processing**
Run churn analysis weekly, not monthly. Early intervention (when churn probability hits 40%) is 3x more effective than waiting until it hits 80%.

### 6. **Validate Risk Signals Manually**
If the skill flags a high-value customer as high-risk, spot-check the data manually before sending a "we're losing you" message. False positives damage trust.

### 7. **Personalize at Scale**
Use dynamic content blocks in emails. Instead of "Here's a discount," say "We noticed you use our Reports feature heavily—here's a 20% upgrade to Pro Reports."

### 8. **Combine with Product Changes**
If the skill identifies that low feature adoption = churn, talk to product. Maybe the feature is hard to discover. Fix the product, not just the customer.

---

## Safety & Guardrails

### What This Skill Will NOT Do

1. **Discriminatory Targeting:** This skill will NOT use protected characteristics (age, race, gender, location) as churn risk factors. All recommendations are based on behavioral and transactional signals only.

2. **Aggressive Dark Patterns:** This skill will NOT generate deceptive subject lines, fake urgency ("Only 2 left!"), or manipulative CTAs. All messaging is honest and customer-centric.

3. **Unlimited Discounting:** Intervention budgets are capped per customer (default: 15% of CLV). The skill will NOT recommend discounts that would make the customer unprofitable.

4. **Automatic Execution:** This skill generates recommendations; **you must approve all interventions before sending**. It will not auto-send emails or modify customer accounts without explicit approval.

5. **Privacy Violations:** This skill respects GDPR, CCPA, and CAN-SPAM regulations. It will NOT:
   - Segment based on sensitive personal data
   - Send emails to unsubscribed users
   - Retain PII longer than necessary
   - Share customer data with third parties

6. **Over-Reliance on Predictions:** Churn prediction models are probabilistic, not deterministic. A 89% churn probability doesn't mean the customer *will* churn. Use it as a signal, not gospel.

### Limitations

- **Data Quality Dependency:** Garbage in, garbage out. If your data is incomplete or inaccurate, predictions suffer. Ensure Stripe/Shopify/SaaS data is clean and current.
- **Cold Start Problem:** New customers (< 30 days) don't have enough historical data for reliable churn prediction. The skill will flag these as "insufficient data."
- **Industry Variance:** Churn models are trained on general patterns. Your industry may have unique dynamics. Validate predictions against your domain knowledge.
- **External Factors:** Skill can't account for macroeconomic shocks, competitor actions, or