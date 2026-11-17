---
name: Analyze Competitor Wins & Losses — Win/Loss Analysis Automation
description: "Analyze win/loss data and customer churn interviews to extract competitive positioning insights, battle cards, and messaging frameworks. Use when the user needs competitive intelligence, sales battlecards, or market positioning strategies."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": [
          "HUBSPOT_API_KEY",
          "SALESFORCE_API_KEY",
          "SLACK_WEBHOOK_URL",
          "OPENAI_API_KEY"
        ],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "⚔️"
    }
  }
---

# Competitor Win/Loss Analysis Specialist

## Overview

The Competitor Win/Loss Analysis Specialist automates competitive intelligence extraction from your sales pipeline, customer churn data, and support interactions. This skill transforms unstructured win/loss survey responses, exit interview notes, and CRM deal loss reasons into actionable competitive battle cards, weak spot profiles, and positioning frameworks—all updated weekly from live data feeds.

**Why this matters:** Sales teams waste hours manually analyzing lost deals. Marketing struggles to articulate differentiation. Product managers don't know which competitor features are actually driving churn. This skill bridges that gap by synthesizing competitive signals from your existing CRM, support tickets, and survey tools into intelligence your entire go-to-market team can act on immediately.

**Integrations:** HubSpot, Salesforce, Slack, Google Sheets, Intercom, Zendesk, SurveyMonkey, Typeform, Gmail, and custom REST APIs.

---

## Quick Start

### Example 1: Analyze HubSpot Lost Deals

```
Analyze all lost deals from the past 60 days in HubSpot where the reason 
includes "competitor." Extract:
- Which competitor names appear most frequently
- Top 3 objection patterns
- Customer segments most vulnerable to each competitor
- Recommended messaging counters for our sales team

Return as a prioritized competitive battle card CSV.
```

### Example 2: Process Customer Churn Exit Interviews

```
I have 15 exit interview transcripts from churned customers (attached as 
a Slack thread). Analyze them for:
- Which competitor features they switched to
- Pricing objection patterns
- Feature gaps in our product that drove the decision
- Estimated revenue impact by competitor

Output a summary with actionable product feedback for our PM team.
```

### Example 3: Weekly Win/Loss Intelligence Report

```
Pull this week's win/loss survey responses from Typeform (form_id: xyz123), 
combine with lost deals from Salesforce, and generate:
- Top 5 competitive threats by deal volume
- Weak spot profile for each top competitor
- Messaging framework with specific counter-arguments
- Slack notification to #sales-leadership with top findings

Schedule this to run every Monday at 9 AM and post to Slack.
```

### Example 4: Identify Product Positioning Gaps

```
Analyze our last 90 days of lost deals in HubSpot. Cross-reference with 
competitor pricing pages and feature comparison. Identify:
- Features competitors highlight that we don't mention in sales materials
- Pricing positioning blind spots
- Market segments where we're losing consistently
- Recommended messaging updates for sales collateral

Export as JSON for use in our sales enablement platform.
```

---

## Capabilities

### 1. **Automated Win/Loss Data Ingestion**
- **HubSpot Integration:** Pull lost deal records, deal loss reasons, custom fields, deal notes, and associated contact data via HubSpot's REST API
- **Salesforce Integration:** Query Opportunity records filtered by StageName = "Closed Lost," extract close reasons, opportunity notes, and account team data
- **Zendesk/Intercom Integration:** Monitor support conversations tagged with "churn," "competitor," or "product feedback" to capture unstructured customer sentiment
- **Survey Tools:** Connect Typeform, SurveyMonkey, or Google Forms to automatically capture win/loss survey responses with participant metadata
- **Email Analysis:** Parse forwarded Slack threads, Gmail labels, or Outlook folders containing exit interview transcripts and feedback emails

### 2. **Competitive Mention Extraction & Normalization**
- **Named Entity Recognition (NER):** Automatically detect competitor names using AI-powered NLP, even in misspelled or abbreviated forms ("Salesforce" vs "SFDC" vs "Salesforce Clouds")
- **Context Awareness:** Distinguish between mentions of competitors as threats vs. integrations vs. comparisons
- **Historical Deduplication:** Track competitor mentions over time to identify emerging vs. established threats
- **Taxonomy Mapping:** Automatically normalize competitor names to a master competitor list you define

### 3. **Objection & Churn Pattern Analysis**
- **Unsupervised Clustering:** Group similar objections and churn reasons into thematic patterns (e.g., "price too high," "can't afford," "ROI doesn't justify cost" → **Pricing Objection**)
- **Sentiment & Intensity Scoring:** Rate how strong each objection was (deal-killer vs. nice-to-have) based on language signals
- **Temporal Trending:** Track whether specific objections are increasing or decreasing week-over-week
- **Segment Cohort Analysis:** Show which customer segments (SMB vs. Enterprise, by industry, by geography) are vulnerable to each competitor and objection type

### 4. **Battle Card Generation**
- **Automated Competitor Profiles:** Create one-page competitive battle cards that include:
  - Competitor overview (market positioning, target segments)
  - Top 3-5 reasons customers choose them over you
  - Your recommended counter-messaging with specific talking points
  - Feature comparison matrix (auto-populated from your product DB)
  - Price positioning analysis
  - Suggested discovery questions to uncover deal risk early
  - Win/loss metrics (deals lost to this competitor, frequency, average deal size)
- **Sales-Ready Format:** Export as Markdown, PDF, or native Salesforce records (via API)
- **Personalization by Role:** Customize messaging for sales, product, and marketing audiences

### 5. **Weak Spot & Positioning Gap Identification**
- **Feature Gap Analysis:** Compare features you DON'T mention in marketing materials vs. features competitors highlight—flags blind spots
- **Pricing Positioning Review:** Identify if competitors are positioned as premium, budget, or value leaders; show where you're positioned and objection patterns by segment
- **Customer Quote Mining:** Extract verbatim customer quotes from win/loss data that support specific competitive weaknesses (e.g., "Their UI is outdated," "They don't have X feature")
- **Market Positioning Gaps:** Analyze which market segments or use cases you're losing in disproportionately, suggesting repositioning opportunities

### 6. **Messaging Framework Generation**
- **Objection Counters:** AI-generated talking points and discovery questions for each top objection pattern
- **Positioning Statements:** Recommended messaging that explicitly differentiates you from top competitors
- **Case Study Mapping:** Link win stories to specific competitive threats (helps sales choose relevant proof points)
- **Sales Playbook Output:** Structured playbook format ready for import into Seismic, Highspot, or Veeva

### 7. **Automated Reporting & Alerting**
- **Weekly Intelligence Briefings:** Auto-generate and email summaries of top competitive threats
- **Slack Integration:** Post real-time alerts when a new high-value deal is lost to a specific competitor (allows sales leadership to debrief while deal is fresh)
- **Dashboards:** Embed win/loss metrics into your existing BI tool (Tableau, Looker, Power BI) for ongoing visibility
- **Scheduled Reports:** Set up recurring reports for sales leadership, product, and marketing (daily, weekly, monthly)

### 8. **Competitor Intelligence Aggregation**
- **Website Pricing Monitoring:** Auto-scrape and track competitor pricing page changes week-over-week
- **Feature Release Tracking:** Monitor competitor release notes and product changelogs for new feature launches
- **Cross-Reference Analysis:** Match customer churn reasons ("switched for better collaboration tools") against actual competitor feature releases to validate timing

---

## Configuration

### Required Environment Variables

```
HUBSPOT_API_KEY=hc_xxxxxxxxxxxx              # Private App key from HubSpot
SALESFORCE_API_KEY=xxxxxxxxxxxxx              # OAuth token or API key
OPENAI_API_KEY=sk-xxxxxxxxxxxx               # For AI analysis and NLP
SLACK_WEBHOOK_URL=https://hooks.slack.com... # For notifications
TYPEFORM_API_TOKEN=tfp_xxxxxxxx              # Optional: for Typeform surveys
ZENDESK_SUBDOMAIN=yourcompany                # Optional: for support ticket analysis
```

### Configuration File (Optional)

Create a `config.json` in your skill directory to customize behavior:

```json
{
  "competitors": [
    "Competitor A",
    "Competitor B",
    "Competitor C"
  ],
  "timeframe_days": 60,
  "min_deal_size_usd": 10000,
  "churn_tags": ["churn", "competitor", "pricing_concern"],
  "slack_channel": "#sales-leadership",
  "report_schedule": "weekly_monday_9am",
  "feature_gap_sources": ["competitor_websites", "g2_reviews", "user_surveys"]
}
```

### Setup Instructions

1. **HubSpot:** Create a Private App with scopes: `crm.objects.deals.read`, `crm.objects.contacts.read`
2. **Salesforce:** Create a Connected App; use OAuth flow or API key authentication
3. **OpenAI:** Use GPT-4 or GPT-3.5-turbo for analysis; budget ~$50-200/month depending on data volume
4. **Slack:** Create an Incoming Webhook for your sales leadership channel
5. **Data Retention:** By default, analysis is not stored permanently. Configure a Google Sheets or S3 bucket if you need historical archival

---

## Example Outputs

### Battle Card Output (Markdown)

```markdown
# Competitor: TechRival Pro

## Win/Loss Metrics (Last 60 Days)
- Deals Lost to This Competitor: 8
- Average Deal Size: $125,000
- Win Rate vs. Us: 62% (when head-to-head)
- Most Vulnerable Segment: Mid-market SaaS

## Top Reasons Customers Choose Them
1. **Lower Price** (37% of objections): $8K/month vs. our $12K/month
2. **Better Mobile Experience** (25%): "Their app is faster"
3. **AI-Powered Automation** (19%): Customers want hands-free workflows

## Your Counter-Messaging
- **On Price:** "Our 24/7 enterprise support and custom integrations save you 40+ hours/month—ROI in 3 months vs. their DIY model"
- **On Mobile:** "We invested 2024 in rebuilding our mobile platform; 10x faster than their legacy app"
- **On AI:** "Our AI trained on your specific workflows; theirs is generic. See Case Study: Acme Corp saved 200 hrs/year"

## Recommended Discovery Questions
- "What's your team's skill level with no-code tools?"
- "How critical is mobile-first workflow for your team?"
- "What integrations are absolutely non-negotiable?"

## Feature Comparison
| Feature | Us | Them |
|---------|----|----|
| Mobile App | ✅ | ✅ |
| Custom Integrations | ✅ | Limited |
| 24/7 Support | ✅ | 9-5 PT |
| AI Automation | ✅ | ✅ |
| Compliance (SOC2) | ✅ | ❌ |
```

### Win/Loss Summary Report (JSON)

```json
{
  "report_date": "2024-01-15",
  "timeframe": "last_60_days",
  "total_deals_analyzed": 127,
  "deals_lost": 23,
  "top_competitors": [
    {
      "name": "TechRival Pro",
      "deals_lost": 8,
      "avg_deal_size": 125000,
      "top_objections": [
        {
          "objection": "Lower pricing",
          "frequency": 6,
          "talking_point": "ROI-focused positioning; emphasize support & customization"
        },
        {
          "objection": "Better mobile UX",
          "frequency": 3,
          "talking_point": "Updated mobile platform; faster than competitor"
        }
      ]
    },
    {
      "name": "Legacy Enterprise Vendor",
      "deals_lost": 5,
      "avg_deal_size": 87000,
      "top_objections": [
        {
          "objection": "Existing ecosystem lock-in",
          "frequency": 4,
          "talking_point": "Seamless migration; we integrate with their current stack"
        }
      ]
    }
  ],
  "market_positioning_gaps": [
    "Competitors heavily promote AI/automation; we under-emphasize this in website",
    "Enterprise segment vulnerable to 'legacy vendor' positioning; consider partnership strategy"
  ],
  "recommended_actions": [
    "Update homepage messaging to lead with AI capabilities",
    "Create battle card for TechRival Pro sales team",
    "Schedule product roadmap review: mobile UX and custom integrations top priorities"
  ]
}
```

### Slack Alert Example

```
🚨 High-Value Deal Lost to Competitor

Deal: Acme Corp (Enterprise)
Deal Size: $425,000 (Annual Contract Value)
Lost To: TechRival Pro
Reason: "Better mobile experience, lower price"
Sales Rep: Sarah Johnson

Top Talking Points for Next Similar Opportunity:
• ROI calculation: Our support saves 40+ hours/month
• Mobile platform: Rebuilt in 2024; 10x faster than competitor
• Custom integrations: They're limited; we're flexible

⚔️ View Full Battle Card: [link]
📧 Schedule debrief with product? (Reply in thread)
```

---

## Tips & Best Practices

### 1. **Data Quality Matters**
- Standardize your "Deal Loss Reason" field in HubSpot/Salesforce. Enforce dropdown values rather than free text; this massively improves analysis accuracy
- Add a "Competitor Name" field to your CRM explicitly; don't rely solely on extraction from deal notes
- Tag churn-related support tickets consistently (e.g., with a "competitor_mention" label in Zendesk)

### 2. **Use Deal Frequency AND Deal Size**
- A competitor might lose 20 small deals ($5K each) but win 1 enterprise deal ($500K). By deal count, they look like a threat; by revenue, they're not. Always segment your analysis

### 3. **Combine CRM + Support + Survey Data**
- Lost deals tell you what happened. Exit interviews tell you *why*. Support tickets tell you *when customers started considering leaving*. Use all three
- Customers are most candid in Zendesk tickets and exit interviews, less candid in sales conversations. Cross-validate findings

### 4. **Create Competitor Personas, Not Just Battle Cards**
- Go beyond "Competitor X took deal Y." Understand: Which *customer segments* are most vulnerable to Competitor A vs. B? By industry? By company size? Use this to target sales outreach

### 5. **Feedback Loop: Share Findings with Product**
- Marketing owns messaging; sales owns conversations. But *product* needs to know which features are actually causing churn vs. which are nice-to-haves
- Export weak spot analysis as a structured input to your product roadmap process

### 6. **Objection Tracking Over Time**
- Track whether "pricing" objections are increasing or decreasing. If increasing, it may signal a pricing change by a competitor or shift in your market positioning
- Use this to decide: Do we need to adjust *price*, improve *ROI messaging*, or both?

### 7. **Integrate with Your Sales Enablement Platform**
- Export battle cards to Seismic, Highspot, or Veeva so sales reps see them in-context (during calls, in their CRM)
- Add battle card recommendations to your Slack sales channel so learnings are discoverable in real-time

### 8. **Validate with Sales Leadership**
- AI-generated insights are accurate ~85-90% of the time. Review top battle cards with your VP of Sales or sales leaders before publishing
- Use the first 2-3 weeks as a "calibration" period; refine the analysis based on sales team feedback

---

## Safety & Guardrails

### What This Skill Will NOT Do

1. **No Unethical Competitive Intelligence