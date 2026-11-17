---
name: Detect & Refresh Ad Copy Fatigue with AI Analysis
description: "Detect ad copy fatigue and auto-suggest micro-pivot refreshes by analyzing CTR/CPC degradation across Facebook, Google, and LinkedIn campaigns. Use when the user needs performance recovery, creative rotation strategies, or real-time ad health monitoring."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["FACEBOOK_API_KEY","GOOGLE_ADS_API_KEY","LINKEDIN_API_KEY","OPENAI_API_KEY"],"bins":["python3","curl"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📊"}}
---

## Overview

**Ad Copy Fatigue Detector & Refresher** is an enterprise-grade creative intelligence tool that monitors advertising campaign performance across Facebook, Google Ads, and LinkedIn in real-time. It automatically identifies when ad copy variants are experiencing performance degradation (declining CTR, rising CPC, or stalling engagement), then generates micro-pivot suggestions—headline reframes, CTA redirects, benefit reshuffles—without requiring manual A/B test setup.

### Why This Matters

Ad fatigue costs businesses 15-40% of ad spend efficiency annually. Traditional solutions require marketers to:
1. Manually pull performance reports weekly
2. Visually inspect CTR/CPC trends
3. Guess at what to change
4. Set up new A/B tests and wait days for results

This skill automates steps 1-3 and jumpstarts step 4 with data-driven micro-pivot suggestions informed by 50+ years of combined advertising dynamics research (Facebook Feed Algorithm, Google Smart Bidding, LinkedIn Sponsored Content best practices).

### Key Integrations
- **Facebook Ads Manager API** (real-time campaign sync)
- **Google Ads API** (Search & Display network analysis)
- **LinkedIn Campaign Manager API** (B2B targeting insights)
- **Slack** (alert notifications on fatigue detection)
- **Zapier** (workflow automation for bulk creative rotation)
- **OpenAI GPT-4** (micro-pivot generation engine)

---

## Quick Start

### Example 1: Detect Fatigue Across All Active Campaigns
```
Analyze my Facebook and Google Ads accounts for copy fatigue. 
Flag any ad variations showing CTR drop >15% or CPC increase >20% 
in the last 14 days. Show me a fatigue risk score for each.
```

**What happens:** The skill connects to your ad accounts, pulls the last 14 days of performance data, calculates CTR/CPC degradation trends, and returns a dashboard with risk scores and flagged variations.

---

### Example 2: Generate Micro-Pivot Suggestions for Underperforming Copy
```
My Google Search campaign headline "Best Project Management Software" 
is showing fatigue (CTR down 18% week-over-week). 
Generate 5 alternative headlines using micro-pivots: reframe the benefit, 
swap CTA language, and add social proof triggers.
```

**What happens:** The skill analyzes the original copy structure, identifies the specific fatigue pattern, and generates variations targeting urgency, specificity, and authority signals.

**Sample output:**
```
Original: "Best Project Management Software"
Risk Score: 8.2/10 (High Fatigue)

Micro-Pivot Suggestions:
1. "Project Management That Cuts Admin Work 47%" (Specificity Pivot)
   Rationale: Adds quantified benefit; targets pain point efficiency
   Estimated CTR Lift: +8-12%

2. "Teams Are Shipping 3x Faster With [Tool]" (Social Proof Pivot)
   Rationale: Third-party validation; competitive differentiation
   Estimated CTR Lift: +6-10%

3. "Stop Wasting Time in Meetings—Try Our PM Tool Free" (CTA Reframe)
   Rationale: Negative-to-positive urgency; removes friction
   Estimated CTR Lift: +5-9%

4. "The #1 PM Tool For Remote Teams (5,000+ Companies Trust Us)" (Authority + Specificity)
   Rationale: Double-trigger (social proof + segment specificity)
   Estimated CTR Lift: +10-14%

5. "Manage Projects Like Top 1% Teams—See Why" (Aspiration + Curiosity)
   Rationale: Identity-based messaging; curiosity gap
   Estimated CTR Lift: +7-11%
```

---

### Example 3: Schedule Automatic Weekly Fatigue Audits & Slack Alerts
```
Set up automated fatigue detection on my Facebook and LinkedIn accounts. 
Run analysis every Monday at 9 AM. Alert me on Slack if any ad variant 
shows >15% CTR drop or >25% CPC increase. Include refresh suggestions 
in the Slack notification.
```

**What happens:** The skill configures a scheduled job that runs Monday mornings, compares performance against baseline, and sends actionable Slack messages with suggested pivots ready to A/B test.

---

## Capabilities

### 1. **Real-Time Fatigue Detection**
- Connects to Facebook Ads Manager, Google Ads, and LinkedIn Campaign Manager APIs
- Analyzes performance across: CTR, CPC, ROAS, Engagement Rate, Cost Per Lead
- Calculates week-over-week and month-over-month degradation rates
- Flags variations at risk using proprietary fatigue scoring (0-10 scale)
- Excludes seasonal/budget-related fluctuations from analysis

**Usage:**
```
Run fatigue detection on my top 10 Facebook campaigns. 
Show me which ad sets are underperforming, when the fatigue started, 
and the 7-day degradation trend.
```

### 2. **Micro-Pivot Suggestion Engine**
- Analyzes underperforming copy using NLP (OpenAI GPT-4 backbone)
- Identifies fatigue type: benefit erosion, CTA fatigue, audience saturation, creative wear
- Generates 3-7 alternative copy variations for each ad
- Each variation uses ONE micro-pivot: headline reframe, benefit reshuffle, CTA redirect, authority addition, urgency trigger
- Includes estimated CTR/CPC impact based on historical pattern matching

**Usage:**
```
My LinkedIn Sponsored Content ad "Join 10,000+ Professionals Learning AI" 
is showing 12% CTR decline. What micro-pivots should I test? 
Generate alternatives using: specificity, social proof, urgency, and curiosity.
```

### 3. **Copy Health Scoring**
- Assigns a Fatigue Risk Score (0-10) to each ad variation
- Tracks: age of copy, impression count, click decay rate, engagement velocity
- Predicts time-to-fatigue (when CTR will likely drop 20%+)
- Compares against industry benchmarks (by vertical, ad platform, device type)

**Usage:**
```
Score the copy health of all my Google Search ads. 
Show me which ads are healthy, which are at risk, and which are critically fatigued. 
Rank by days-until-predicted-fatigue.
```

### 4. **A/B Test Auto-Setup**
- Generates A/B test recommendations with control/variant pairs
- Suggests sample size and duration based on baseline performance
- Integrates with Zapier to automatically create test variants in your ad platform
- Tracks test performance and reports winner back to your dashboard

**Usage:**
```
Take my top 3 micro-pivot suggestions for this underperforming Facebook ad. 
Set up A/B tests: control vs. each variant. 
Run for 7 days or until statistical significance. Alert me when done.
```

### 5. **Historical Performance Trending**
- Pulls 90-day historical performance data across all platforms
- Identifies performance patterns by: time of day, day of week, audience segment, device type
- Detects seasonal fatigue vs. structural copy decay
- Highlights which micro-pivots worked best in the past for similar ads

**Usage:**
```
Show me a 90-day performance trend for my Google Display campaigns. 
Which ad copy variations recovered best from fatigue? 
Use those patterns to suggest refreshes for my current declining ads.
```

### 6. **Slack & Email Alerting**
- Real-time notifications when fatigue is detected
- Weekly digest summaries with top action items
- One-click approval to launch suggested A/B tests
- Tracks notification performance (how many alerts led to action)

**Usage:**
```
Configure Slack alerts for my team. Notify #marketing-ads 
whenever a Facebook ad shows >20% CTR decline. 
Include the fatigue risk score and top 2 micro-pivot suggestions.
```

---

## Configuration

### Required Environment Variables

```bash
# Facebook Ads
export FACEBOOK_API_KEY="your-facebook-ads-api-key"
export FACEBOOK_ACCOUNT_ID="act_1234567890"

# Google Ads
export GOOGLE_ADS_API_KEY="your-google-ads-api-key"
export GOOGLE_ADS_CUSTOMER_ID="1234567890"
export GOOGLE_ADS_DEVELOPER_TOKEN="your-dev-token"

# LinkedIn
export LINKEDIN_API_KEY="your-linkedin-api-key"
export LINKEDIN_AD_ACCOUNT_ID="123456789"

# AI Model
export OPENAI_API_KEY="sk-your-openai-key"

# Optional: Slack Integration
export SLACK_WEBHOOK_URL="REDACTED-SECRET"
```

### Setup Instructions

**Step 1: Authenticate Ad Accounts**
```bash
claw skill config ad-copy-fatigue-detector-refresher --setup
# Walks you through OAuth for each platform
```

**Step 2: Set Fatigue Thresholds**
```bash
claw skill config ad-copy-fatigue-detector-refresher \
  --ctr-drop-threshold 15 \
  --cpc-increase-threshold 20 \
  --analysis-window 14 \
  --fatigue-risk-score-threshold 7
```

**Step 3: (Optional) Enable Slack Alerts**
```bash
claw skill config ad-copy-fatigue-detector-refresher \
  --slack-enabled true \
  --slack-channel "#marketing-ads" \
  --slack-frequency weekly
```

**Step 4: (Optional) Schedule Automated Scans**
```bash
claw skill schedule ad-copy-fatigue-detector-refresher \
  --run "every Monday at 09:00 AM" \
  --platforms facebook,google,linkedin \
  --action "detect-and-alert"
```

### Platform-Specific Notes

**Facebook Ads Manager:**
- Requires `ads_read` permission
- Pulls data from all ad sets in connected accounts
- Supports Advantage+ and traditional campaign analysis
- Recognizes seasonal campaigns (excludes from fatigue flagging)

**Google Ads:**
- Requires `GOOGLE-ADWORDS-API-MARKETING-MANAGER` scope
- Analyzes Search, Display, and Performance Max campaigns
- Uses Smart Bidding signals in CPC trend analysis
- Supports multi-account view hierarchy

**LinkedIn Campaign Manager:**
- Requires `administer_organization` permission
- Analyzes Sponsored Content, Lead Gen Forms, and Conversation Ads
- Factors in audience expansion and saved audiences
- Recognizes B2B-specific fatigue patterns (longer sales cycle)

---

## Example Outputs

### Output Format 1: Fatigue Detection Report
```json
{
  "analysis_date": "2024-01-15T14:30:00Z",
  "platforms_analyzed": ["facebook", "google_ads", "linkedin"],
  "total_campaigns": 47,
  "fatigued_variations": 12,
  "campaigns_at_risk": [
    {
      "platform": "facebook",
      "campaign_name": "Q1 Lead Gen - SaaS",
      "ad_set_id": "120145789",
      "ad_variation": "Headline: 'Best Project Management Software'",
      "fatigue_risk_score": 8.2,
      "ctr_trend": {
        "current": 0.89,
        "14_days_ago": 1.08,
        "percent_change": -17.6
      },
      "cpc_trend": {
        "current": 1.42,
        "14_days_ago": 1.15,
        "percent_change": 23.5
      },
      "impression_count": 127400,
      "days_since_active": 34,
      "recommendation": "HIGH PRIORITY: Refresh with micro-pivot. Suggested: Specificity pivot or Authority addition.",
      "estimated_time_to_critical_fatigue": "4-6 days"
    },
    {
      "platform": "google_ads",
      "campaign_name": "Search - Branded Keywords",
      "ad_id": "456789123",
      "ad_variation": "Headline 1: 'Trusted by 5,000+ Teams Worldwide'",
      "fatigue_risk_score": 6.1,
      "ctr_trend": {
        "current": 3.24,
        "14_days_ago": 3.67,
        "percent_change": -11.7
      },
      "cpc_trend": {
        "current": 0.68,
        "14_days_ago": 0.71,
        "percent_change": 4.2
      },
      "impression_count": 89300,
      "days_since_active": 28,
      "recommendation": "MEDIUM PRIORITY: Monitor closely. Consider testing urgency or curiosity pivot.",
      "estimated_time_to_critical_fatigue": "9-12 days"
    }
  ],
  "healthy_campaigns": 35,
  "summary": "12 of 47 campaigns show fatigue signals. 2 are high-priority for refresh. 5 are medium-priority (monitor). 5 healthy campaigns can be scaled."
}
```

### Output Format 2: Micro-Pivot Suggestions
```markdown
## Copy Refresh Strategy for: "Best Project Management Software"

**Original Copy Analysis:**
- Platform: Facebook Ads
- Performance Age: 34 days active
- Fatigue Type: Benefit Erosion (audience has heard this generic benefit)
- CTR Decline Rate: 17.6% over 14 days
- CPC Increase Rate: 23.5% over 14 days

---

### Suggested Micro-Pivots (Ranked by Estimated Impact)

#### Pivot #1: SPECIFICITY ENHANCEMENT (Est. CTR Lift: +8-12%)
**New Copy:** "Project Management That Cuts Admin Work 47%"
**Rationale:** 
- Replaces generic "Best" with quantified result
- Targets the #1 pain point for your audience (time waste)
- Creates specificity urgency (the "47%" makes it credible and memorable)
**Change Type:** Headline Swap
**Estimated Impact:** High confidence lift; aligns with platform best practices

---

#### Pivot #2: SOCIAL PROOF INTEGRATION (Est. CTR Lift: +6-10%)
**New Copy:** "Teams Are Shipping 3x Faster With [YourTool]"
**Rationale:**
- Adds third-party validation signal (reduces skepticism)
- Competitive differentiation (faster outcomes vs. feature lists)
- Outcome-focused messaging (what users care about)
**Change Type:** Benefit Reshuffle + CTA Reframe
**Estimated Impact:** Medium-high confidence; proven for SaaS

---

#### Pivot #3: URGENCY + NEGATIVE-TO-POSITIVE (Est. CTR Lift: +5-9%)
**New Copy:** "Stop Wasting Time in Meetings—Try Our PM Tool Free"
**Rationale:**
- Opens with pain point acknowledgment (resonance trigger)
- Clear CTA ("Free trial") reduces friction
- Contrast structure (negative problem → positive solution) improves memorability
**Change Type:** CTA Reframe
**Estimated Impact:** Medium confidence; effective for B2B audiences

---

#### Pivot #4: AUTHORITY STACKING (Est. CTR Lift: +10-14%)
**New Copy:** "The #1 PM Tool For Remote Teams (5,000+ Companies Trust Us)"
**Rationale:**
- Double-trigger messaging (authority + social proof + segment specificity)
- Targets growing remote work demographic
- Parenthetical reinforcement adds credibility without feeling forced
**Change Type:** Authority Addition + Specificity Pivot
**Estimated Impact:** High confidence; highest estimated lift

---

#### Pivot #5: IDENTITY-BASED + CURIOSITY GAP (Est. CTR Lift: +7-11%)