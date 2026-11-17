---
name: Analyze Creator Financial Health with Automated Reporting
description: "Analyze creator revenue streams (Stripe, PayPal, affiliate, sponsorships) to calculate true profitability per content piece, identify unprofitable segments, forecast cash flow gaps, and recommend high-margin content verticals. Use when the user needs revenue analysis, margin reporting, content ROI, or cash flow forecasting."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["STRIPE_API_KEY","PAYPAL_CLIENT_ID","PAYPAL_CLIENT_SECRET"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"💰"}}
---

# Creator Financial Health Auditor

## Overview

The Creator Financial Health Auditor is a comprehensive financial intelligence tool designed for solopreneurs, content creators, and digital agencies who need to understand their true profitability beyond vanity metrics. This skill connects to your revenue sources (Stripe, PayPal, affiliate platforms, sponsorship networks, course sales) and delivers actionable financial insights that drive strategic decision-making.

**Why This Matters:**
Most creators optimize for audience size, engagement, or subscriber count—metrics that don't translate to actual profitability. This skill answers the critical questions:
- Which content pieces actually generate margin?
- Are you losing money on certain audience segments?
- When will cash flow dry up based on current trends?
- Which content verticals should you invest in?

**Integrated Platforms & APIs:**
- **Stripe** – payment processing, subscription data, transaction fees
- **PayPal** – international payments, invoice tracking
- **Google Analytics 4** – content-to-revenue attribution
- **Slack** – automated financial alerts and weekly reports
- **Airtable** – financial data storage and historical tracking
- **Zapier** – workflow automation triggers
- **WordPress** – content metadata (post type, category, publish date)

---

## Quick Start

### Example 1: Analyze Monthly Revenue & Identify Unprofitable Content
```
Audit my creator finances for the last 90 days. Connect to my Stripe account 
(test keys: sk_test_xxx), pull all transactions, categorize by content source 
(YouTube, email list, sponsorships), calculate total revenue, subtract payment 
processing fees and platform costs, and show me which content pieces lost money 
after accounting for time spent.
```

### Example 2: Cash Flow Forecast & Runway Warning
```
Forecast my cash flow for the next 6 months. I have recurring sponsorships 
($5k/month), course sales ($3-8k/month, inconsistent), and affiliate income 
($2-4k/month). My monthly burn rate is $6k. When will I hit a cash shortage? 
Alert me when runway drops below 30 days and recommend which revenue stream 
I should prioritize to fix it.
```

### Example 3: Content ROI Ranking & Vertical Recommendations
```
Calculate the true ROI for each of my content verticals. Link my WordPress 
blog, Google Analytics 4, and Stripe account. For each blog post published 
in the last 6 months, calculate time spent (estimate 8 hours per post), 
attributed revenue from that post's audience, and net margin. Rank verticals 
by profitability and recommend which 3 I should double down on.
```

### Example 4: Audience Segment Profitability Analysis
```
Break down my revenue by audience segment. Show me revenue per subscriber 
in my email list, per YouTube viewer, per social media follower, and per 
course student. Which audience segment generates the highest margin per 
hour of content creation? Which segments are unprofitable and should I 
consider sunsetting?
```

### Example 5: Automated Weekly Financial Health Report
```
Create a weekly Slack report that lands in #finances every Monday 9am. Include:
- Last week's total revenue (by source)
- Profitability vs. projections
- Cash runway (days remaining)
- Top-performing content pieces
- Any cash flow warnings
Send it to my Slack workspace at enterprise-ai.slack.com.
```

---

## Capabilities

### 1. **Multi-Source Revenue Aggregation**
Connects to all major creator revenue streams:
- **Stripe Dashboard API** – transactions, subscription MRR, churn, refunds, payment method breakdown
- **PayPal REST API** – international sales, invoice history, dispute tracking
- **Affiliate Networks** – Refersion, Impact, ShareASale API integrations
- **Sponsorship Platforms** – Captiv8, Influee, FameBit revenue tracking
- **Course Platforms** – Gumroad, Teachable, ConvertKit API for course sales & refunds
- **Ad Networks** – YouTube Analytics API, AdSense revenue, Google AdManager

**Example Usage:**
```
Aggregate all revenue from my 4 income streams: Stripe (primary products), 
PayPal (international clients), Affiliate links (Amazon Associates + ShareASale), 
and course sales (Gumroad). Show combined total and breakdown by source.
```

### 2. **True Profitability Calculation**
Automatically deducts all costs:
- Payment processing fees (2.9% + $0.30 for credit cards, 1.99% for PayPal, platform-specific rates)
- Platform commissions (course platform cuts, affiliate platform fees)
- Time cost (hourly rate × estimated creation hours per content piece)
- Infrastructure costs (hosting, tools, software subscriptions pro-rated)
- Taxes (estimated quarterly tax obligations based on jurisdiction)
- Refunds & chargebacks

**Example Output:**
```
CONTENT PIECE: "How to Build Landing Pages" (Blog Post)
Gross Revenue: $2,847 (affiliate links + sponsorship)
- Payment Fees: -$85
- Platform Commission: -$142
- Content Creation Time (8 hrs @ $50/hr): -$400
- Infrastructure (pro-rated): -$28
NET PROFIT: $1,792
Profit Margin: 63%
```

### 3. **Unprofitable Segment Detection**
Identifies audience segments or content types that lose money:
- Calculates revenue-per-hour for each content format
- Compares against your target hourly rate
- Flags segments operating below break-even
- Suggests 3 optimization paths: increase prices, reduce production time, sunset the segment

**Example Usage:**
```
Show me all content segments that generated less than $50/hour of creation time 
in the last 90 days. Highlight which ones I should consider sunsetting or 
repurposing to be profitable.
```

### 4. **Cash Flow Forecasting**
Projects cash position 3, 6, and 12 months forward:
- Uses historical revenue patterns to forecast by source
- Accounts for seasonality and trend direction
- Models multiple scenarios (pessimistic, realistic, optimistic)
- Sends alerts when runway drops below threshold

**Example Output:**
```
CASH FLOW FORECAST (6-Month Outlook)
Current Cash Position: $18,500
Monthly Burn Rate: $5,200

MONTH 1: +$8,300 revenue → $21,600 cash (Safe)
MONTH 2: +$6,400 revenue → $23,800 cash (Safe)
MONTH 3: +$3,100 revenue → $21,700 cash (Safe)
MONTH 4: +$2,800 revenue → $19,300 cash (Caution)
MONTH 5: +$4,200 revenue → $18,300 cash (Alert: 30-day runway)
MONTH 6: +$5,900 revenue → $19,000 cash (Recovery)

⚠️ ACTION: Revenue dips in Month 5. Prioritize sponsorship renewals and 
course launch for Jan-Mar timeframe.
```

### 5. **Content Vertical Ranking & Recommendations**
Ranks content categories by profitability and ROI:
- Calculates margin per hour for YouTube, blog, podcast, email, social
- Identifies your "profit-generating" vs. "traffic-driving" content
- Recommends which verticals to scale based on margin, not just reach
- Shows opportunity cost of low-margin content

**Example Usage:**
```
Rank my content verticals (YouTube, Blog, Newsletter, Affiliate) by true ROI 
over the last 6 months. Which 3 should I focus on? What's the opportunity 
cost of continuing my lowest-margin vertical?
```

### 6. **Audience Segment Profitability**
Breaks down revenue efficiency by audience type:
- Revenue per email subscriber
- Revenue per YouTube subscriber
- Revenue per social media follower
- Revenue per course student
- LTV (lifetime value) by segment

**Example Output:**
```
REVENUE PER 1,000 PEOPLE
Email Subscribers: $4.20/month (highest margin)
YouTube Subscribers: $0.18/month (declining)
Twitter Followers: $0.05/month (lowest)
Course Students: $12.50/month (highest absolute value)

Recommendation: Invest in email growth (20:1 ROI) and deprecate Twitter tactics.
```

### 7. **Automated Financial Reports**
Generates recurring reports in your preferred format:
- **Daily Slack alerts** – new high-value transactions, cash threshold warnings
- **Weekly summaries** – revenue, profitability, top performers
- **Monthly dashboards** – Airtable synced, sortable, filterable
- **Quarterly deep dives** – cohort analysis, trend analysis, forward guidance

---

## Configuration

### Required Environment Variables
```bash
# Stripe
export STRIPE_API_KEY="sk_live_YOUR_KEY_HERE"

# PayPal
export PAYPAL_CLIENT_ID="your_client_id"
export PAYPAL_CLIENT_SECRET="your_client_secret"

# Google (for Analytics & Gmail integration)
export GOOGLE_ANALYTICS_PROPERTY_ID="12345678"
export GOOGLE_SERVICE_ACCOUNT_JSON='{"type":"service_account"...}'

# Optional: Slack for automated reports
export SLACK_BOT_TOKEN="REDACTED-SECRET"
export SLACK_CHANNEL_ID="C123ABC456"

# Optional: Airtable for historical tracking
export AIRTABLE_API_KEY="your_airtable_key"
export AIRTABLE_BASE_ID="appXXXXX"
```

### Setup Instructions

**Step 1: Connect Your Payment Processors**
```
1. Log into your Stripe Dashboard → Settings → API Keys
2. Copy your Secret Key (starts with sk_live_)
3. Set STRIPE_API_KEY environment variable
4. Repeat for PayPal (Settings → Apps & Credentials → REST API Signature)
```

**Step 2: Enable Data Integrations**
```
Optional: Connect Google Analytics 4 for content attribution
- Go to GA4 → Admin → Service Accounts
- Create a service account and export JSON credentials
- Set GOOGLE_SERVICE_ACCOUNT_JSON

Optional: Connect WordPress for content metadata
- Install REST API enabled on WordPress
- Provide site URL and API credentials
```

**Step 3: Configure Alert Thresholds**
```
Set your preferences in the skill config:
- Cash runway alert threshold (default: 30 days)
- Minimum profitability target per hour (default: $35/hour)
- Revenue forecast confidence interval (default: 80%)
- Reporting frequency (daily/weekly/monthly)
- Slack/email destination
```

---

## Example Outputs

### Output 1: Profitability Dashboard
```
═══════════════════════════════════════════════════════════════
CREATOR FINANCIAL HEALTH REPORT | October 2024
═══════════════════════════════════════════════════════════════

REVENUE SUMMARY
Total Gross Revenue:           $14,282
Payment Processing Fees:       -$427
Platform Commissions:          -$562
Net Revenue (Before Labor):    $13,293

TIME INVESTMENT & COST
Content Creation Hours:        48 hours
Target Hourly Rate:            $50/hour
Imputed Time Cost:             -$2,400
Infrastructure (pro-rated):    -$340
Quarterly Tax Reserve (est.):  -$3,323

NET PROFIT:                    $7,230
Profit Margin:                 50.6%

═══════════════════════════════════════════════════════════════
REVENUE BREAKDOWN BY SOURCE
═══════════════════════════════════════════════════════════════

Source               Gross      Fees    Net    % of Total  Margin/Hour
─────────────────────────────────────────────────────────────────────
Stripe (Products):   $8,900    -$267   $8,633  60.4%      $65.12
PayPal (Services):   $3,200    -$64    $3,136  22.0%      $56.30
Affiliate Links:     $1,645    -$82    $1,563  11.6%      $42.18
Sponsorships:        $537      -$14    $523     3.7%      $74.71
─────────────────────────────────────────────────────────────────────
TOTAL:              $14,282   -$427   $13,855  100%       $59.07

═══════════════════════════════════════════════════════════════
CONTENT VERTICAL PROFITABILITY
═══════════════════════════════════════════════════════════════

Rank  Vertical           Revenue  Hours  Profit/Hour  Margin%
────  ──────────────────────────────────────────────────────
 1.   Email Campaigns    $6,200   8      $77.50      67%
 2.   Video Courses      $4,100   16     $25.63      45%
 3.   Blog Posts         $2,400   18     $13.33      38%
 4.   Affiliate Content  $1,582   6      $26.33      52%

⚠️ RECOMMENDATION: Blog posts are underperforming ($13.33/hour). 
Consider repurposing blog content into email or video formats.

═══════════════════════════════════════════════════════════════
CASH FLOW & RUNWAY
═══════════════════════════════════════════════════════════════

Current Cash Position:         $23,400
Monthly Average Burn Rate:     $5,200
Current Runway:                4.5 months (safe)

Forecasted Position (6 months): $18,200 (declining trend)

🔴 ACTION: Sponsorship pipeline is weak. Launch 2 new affiliate programs 
by end of Q4 to shore up Q1 revenue dip (historical seasonal low).
```

### Output 2: Unprofitable Segments Alert
```
PROFITABILITY WATCH | High-Risk Segments

You have 2 content segments operating BELOW your target hourly rate of $50/hour:

SEGMENT 1: Blog Content (Travel Niche)
- Gross Revenue (90 days): $1,240
- Creation Hours: 22 hours
- Actual Hourly Rate: $56.36 ✓ PROFITABLE
- Trend: Declining (-12% YoY)
- Recommendation: Consolidate into 2x/month (reduce hours), test premium gate

SEGMENT 2: Podcast Episodes
- Gross Revenue (90 days): $380
- Creation Hours: 18 hours  
- Actual Hourly Rate: $21.11 ✗ UNPROFITABLE
- Trend: Flat for 12 months
- Recommendation: 
  Option A - Sunset (save 18 hrs/month)
  Option B - Monetize: Add sponsorship tier, Patreon, course bundle
  Option C - Repurpose: Convert audio to newsletter + clips (reuse labor)

Opportunity Cost of Keeping Podcast: $720/month 
(18 hours × $40/hour opportunity cost to use on high-margin content)
```

### Output 3: Slack Daily Alert
```
💰 Creator Financial Alert | Nov 14, 2024

✅ STRONG DAY
- Revenue: $847 (+32% vs daily avg)
- Top performer: Email sequence (32 sales)
- Cash position: $24,100 (healthy)

⚠️ ATTENTION NEEDED
- PayPal dispute filed: $140 (customer chargeback)
- Stripe fee rate increased: Now 2.9% + $0.30 (notify support)

📊 RUNWAY STATUS
- Days of cash remaining: 127 days
- Next cash threshold alert: 89 days (will notify)
```

---

## Tips & Best Practices

### 1. **Categorize Your Revenue Correctly**
Tag every transaction with the content source or campaign:
```
Good: "