---
name: Map Customer Micromoments Across Web Analytics & CRM Platforms
description: "Analyze customer journey touchpoints to identify micro-moments of intent, frustration, and buying readiness. Use when the user needs audience behavior maps, emotional trigger extraction, or optimal intervention windows for targeted nurture sequences."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["OPENAI_API_KEY","ANTHROPIC_API_KEY"],"bins":["python3","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"🎯"}}
---

## Overview

The **Audience Micromoment Mapper** is an AI-powered intelligence tool that transforms raw customer interaction data into actionable behavioral insights. It analyzes support tickets, email replies, social comments, product feedback, and chat logs to detect critical decision-making moments—when customers are frustrated, curious, or ready to purchase.

Unlike generic analytics, this skill identifies the **emotional context** behind customer behaviors, extracts **pain point keywords** that signal readiness for intervention, and maps **optimal timing windows** for personalized content delivery. The output is a structured audience behavior map that feeds directly into marketing automation platforms, CRM nurture sequences, and content strategy.

**Why it matters:** 80% of sales are won in micro-moments—the 5-second windows when customers have high intent. This skill finds those moments and tells you exactly how to respond.

**Integration Ready:** Works with Slack (real-time alerts), HubSpot (contact enrichment), WordPress (comment analysis), Intercom (support ticket mining), Google Sheets (data import/export), Zapier, and Make.

---

## Quick Start

Try these prompts immediately to see the skill in action:

### Example 1: Support Ticket Analysis
```
Analyze this support ticket for micro-moments:
"Hi, I've been using your tool for 2 weeks and I love the dashboard, 
but I'm frustrated that I can't bulk export my data. I'm comparing you 
with Competitor X right now because they offer that feature. My team 
is growing and I need this before month-end or we'll have to switch."

Identify: emotional state, pain points, buying readiness score (1-10), 
and recommended intervention.
```

### Example 2: Email Thread Mining
```
Extract micro-moments from this email conversation thread:

[User]: "Your pricing seems high for our startup."
[Sales]: "What's your monthly usage?"
[User]: "About 100K events. But honestly, we're also looking at alternatives."
[Sales]: "Let me show you our startup plan..."
[User]: "Interesting! Can you show me a demo this week? We're deciding Friday."

Output: customer intent signals, objection patterns, timing window, 
and next-best-action recommendations.
```

### Example 3: Social Media & Product Feedback
```
Batch analyze these customer comments for behavior insights:

1. "Finally switched from [old tool]! The onboarding is SO much better."
2. "Anyone else have issues with the API rate limits on the free plan?"
3. "Just upgraded to Pro. Best decision for our analytics. Worth every penny."
4. "The documentation is outdated. I'm stuck on step 3 of the tutorial."
5. "Is there a Slack integration? That would be the last thing we need."

Create a micromoment map with: emotional segments, feature requests 
that signal upgrade readiness, friction points, and cohort recommendations.
```

---

## Capabilities

### 1. Micro-Moment Detection
The skill automatically identifies **7 critical decision moments**:
- **Frustration peaks**: Customer pain points reaching a tipping point
- **Comparison signals**: Active evaluation of competitors (highest-intent moment)
- **Feature requests**: Indirect buying signals ("if only you had X...")
- **Social proof moments**: Success celebrations and positive sentiment
- **Urgency triggers**: Time-bound commitments ("deciding Friday," "before month-end")
- **Objection patterns**: Price sensitivity, feature gaps, integration needs
- **Readiness-to-upgrade indicators**: Outgrowing current plan, team expansion, budget allocated

*Example output:*
```json
{
  "micromoment_type": "competitor_comparison",
  "intensity_score": 9.2,
  "emotional_state": "frustrated_but_exploratory",
  "pain_points": ["data_export", "bulk_operations"],
  "urgency_window": "7_days",
  "recommended_intervention": "demo_of_advanced_export_features"
}
```

### 2. Emotional Trigger Extraction
Analyzes sentiment, subtext, and linguistic patterns to reveal what's driving behavior:
- **Explicit emotions**: frustration, excitement, confusion, hesitation
- **Implicit signals**: sarcasm, false agreement, question patterns suggesting doubt
- **Urgency indicators**: words like "asap," "before," "deadline," "switching"
- **Authority signals**: decision-maker language vs. evaluator vs. influencer

### 3. Pain Point Keyword Mapping
Automatically extracts and clusters pain points by:
- **Functional gaps** (missing features)
- **Usability friction** (unclear UI, poor documentation)
- **Workflow inefficiencies** (manual steps, integrations)
- **Cost concerns** (budget overruns, price sensitivity)
- **Support gaps** (response time, knowledge base quality)

### 4. Intervention Window Timing
Calculates optimal timing for outreach:
- When to send nurture content (emotional state receptivity)
- When to escalate to sales (buying readiness window)
- When to gather feedback (frustration resolution moments)
- When to hold back (customer satisfaction peaks)

### 5. Audience Behavior Cohorts
Groups customers into actionable segments:
- **At-risk churners** (high frustration, competitor comparison)
- **Ready-to-upgrade** (feature requests, team growth signals)
- **Feature-seekers** (specific capability gaps)
- **New advocates** (recent positive experiences, high satisfaction)
- **Stalled evaluators** (stuck on onboarding, confusion signals)

### 6. Structured Audience Map Output
Generates exportable JSON/CSV behavior maps with:
- Customer ID / email
- Current micro-moment type & intensity
- Emotional profile
- Top 3 pain points
- Recommended nurture content type
- Suggested intervention channel (email, Slack, in-app, sales call)
- Optimal timing (day/time to contact)
- Readiness-to-buy score (1-10)
- Cohort assignment

---

## Configuration

### Required Environment Variables
```bash
# OpenAI for advanced language analysis and semantic understanding
export OPENAI_API_KEY="sk-..."

# Anthropic for multi-turn context analysis and nuance detection
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Optional Environment Variables (for integrations)
```bash
# For Slack alerts on high-intent micro-moments
export SLACK_WEBHOOK_URL="https://hooks.slack.com/..."

# For HubSpot contact enrichment
export HUBSPOT_API_KEY="pat-..."

# For WordPress comment analysis
export WORDPRESS_API_TOKEN="..."

# For Google Sheets export (audience maps)
export GOOGLE_SHEETS_CREDENTIALS="path/to/credentials.json"
export TARGET_SPREADSHEET_ID="..."

# For Intercom support ticket mining
export INTERCOM_ACCESS_TOKEN="..."
```

### Setup Instructions

1. **Prepare your data source**:
   - Export support tickets (Intercom, Zendesk, Help Scout)
   - Export email threads (Gmail, Mailchimp, ConvertKit)
   - Export social comments (Twitter/X, LinkedIn, Facebook, product reviews)
   - Export product feedback (Canny, UserVoice, in-app surveys)

2. **Format data** (JSON or CSV):
   ```json
   [
     {
       "customer_id": "cust_12345",
       "email": "user@company.com",
       "source": "support_ticket",
       "timestamp": "2025-01-15T10:30:00Z",
       "content": "I love the dashboard but need bulk export...",
       "metadata": {"user_since": "2024-11-20", "plan": "starter"}
     }
   ]
   ```

3. **Run the skill**:
   ```bash
   openclaw exec audience-micromoment-mapper \
     --input data.json \
     --output audience-behavior-map.json \
     --cohort-analysis true \
     --include-timing-windows true
   ```

---

## Example Outputs

### Audience Behavior Map (JSON)
```json
{
  "analysis_date": "2025-01-15T14:22:00Z",
  "customers_analyzed": 156,
  "micromoments_detected": 47,
  "audience_segments": {
    "at_risk_churners": {
      "count": 8,
      "avg_frustration_score": 8.1,
      "primary_pain_points": ["data_export", "integrations", "support_response_time"],
      "recommended_intervention": "executive_outreach_with_roadmap_review",
      "sample_customers": [
        {
          "email": "manager@acme.com",
          "micromoment_type": "competitor_comparison",
          "pain_points": ["bulk_export", "api_rate_limits"],
          "urgency_window": "7_days",
          "emotional_state": "frustrated_but_still_evaluating",
          "intervention_channel": "sales_call",
          "optimal_contact_time": "tuesday_10am_est",
          "readiness_score": 8.7,
          "talking_points": ["New bulk export feature (roadmap)", "Pro plan tier available", "Dedicated support option"]
        }
      ]
    },
    "ready_to_upgrade": {
      "count": 19,
      "avg_readiness_score": 7.8,
      "primary_triggers": ["team_growth", "feature_requests", "usage_growth"],
      "recommended_nurture_sequence": "upgrade_benefits_3_email_series",
      "sample_customers": [
        {
          "email": "growth@startup.io",
          "current_plan": "starter",
          "micro_signals": ["We're hiring 3 people next month", "Need API access", "Budget approved for tools"],
          "feature_requests": ["advanced_analytics", "team_collaboration"],
          "optimal_content": "case_study_of_similar_team_scaling",
          "suggested_contact": "in_app_offer_this_week",
          "conversion_probability": 0.72
        }
      ]
    },
    "feature_seekers": {
      "count": 15,
      "primary_feature_gaps": ["slack_integration", "custom_reports", "webhook_support"],
      "recommended_action": "feature_release_notification_campaign",
      "impact_if_addressed": "likely_to_upgrade_or_increase_usage"
    },
    "new_advocates": {
      "count": 12,
      "sentiment_score": 9.1,
      "recommended_action": "nurture_for_referrals_and_testimonials",
      "potential_csat_improvement": "15-20%"
    }
  },
  "timing_insights": {
    "highest_intent_window": "tuesday_through_thursday_9am_to_12pm",
    "post_frustration_resolution_optimal_reach": "48_hours_after_support_resolution",
    "weekend_engagement_patterns": "minimal_business_decision_activity"
  },
  "recommended_next_actions": [
    {
      "priority": 1,
      "action": "Execute executive outreach to 8 at-risk accounts",
      "expected_impact": "60-70% prevent churn, 30% upgrade"
    },
    {
      "priority": 2,
      "action": "Launch upgrade nurture sequence for 19 ready-to-upgrade customers",
      "expected_impact": "$48K-72K ARR potential"
    },
    {
      "priority": 3,
      "action": "Publish Slack integration announcement (19 feature-seekers waiting)",
      "expected_impact": "increased activation, higher NPS"
    }
  ]
}
```

### Email Nurture Sequence Recommendation
```json
{
  "customer_email": "manager@acme.com",
  "cohort": "at_risk_churners",
  "micro_moment_type": "competitor_comparison",
  "recommended_sequence": {
    "email_1": {
      "send_time": "wednesday_10am_est",
      "subject": "We heard you need bulk export—here's what's coming",
      "content_angle": "acknowledge_pain_point_plus_roadmap",
      "cta": "schedule_20_min_product_walkthrough"
    },
    "email_2": {
      "days_after_first": 3,
      "subject": "How [Competitor] customers are switching to us (and saving $X)",
      "content_angle": "competitive_comparison_social_proof",
      "cta": "view_case_study"
    },
    "email_3": {
      "days_after_second": 4,
      "subject": "Your team, your timeline: Pro plan flexibility",
      "content_angle": "remove_objections_pricing_packaging",
      "cta": "explore_pro_tier_pricing"
    }
  },
  "alternate_channel_if_no_email_open": "sales_call_scheduled_thursday_3pm"
}
```

---

## Tips & Best Practices

### 1. Data Quality Maximizes Insight
- **Include context metadata**: customer lifetime value, current plan, company size, industry
- **Date-stamp everything**: micro-moments are time-dependent; recency matters
- **Batch consistently**: analyze weekly or bi-weekly for trend detection
- **Source diversity**: mix support, sales, product, and social data for complete picture

### 2. Act on High-Intensity Micro-Moments Within 24 Hours
Micro-moments decay quickly. If the skill flags a customer as "comparing competitors" with intensity 9+, personalized outreach within 24 hours can convert—after 3 days, the moment often passes.

### 3. Segment Your Nurture by Emotional State, Not Just Behavior
A frustrated customer needs empathy + fast solutions. A curious evaluator needs education + comparison. The skill detects both; use it to tailor messaging tone.

### 4. Use Timing Windows for Channel Selection
- **High urgency + low tech-savviness** → Phone call
- **High urgency + self-directed** → In-app notification
- **Medium urgency** → Personalized email sequence
- **Low urgency but high value** → Invite to exclusive webinar/community

### 5. Monitor Cohort Shifts
If 3 customers move from "happy user" to "competitor comparison" in one week, there's likely a systemic issue (competitor feature launch, pricing change, support problem). Investigate root cause.

### 6. Cross-Reference with Win/Loss Data
Tag wins and losses in your CRM. Over time, correlate which micro-moments and interventions actually drive conversion. Refine your playbooks monthly.

### 7. Create Playbooks for Each Micro-Moment Type
```markdown
## Competitor Comparison Playbook
- Within 4 hours: Sales team alert (Slack notification)
- Within 24 hours: CMO review of email + custom demo offer
- Content: competitive comparison guide + customer testimonial
- Goal: schedule demo within 72 hours
- Success metric: 60%+ demo completion rate

## Frustration Peak Playbook
- Within 2 hours: Support team automatic escalation
- Content: empathy message + fast resolution path
- Follow-up: "product improvement survey" to capture UX feedback
- Goal: resolve within SLA, then pitch advanced tier that solves problem
```

### 8. Export & Integrate with Marketing Automation
Push audience maps directly into HubSpot workflows, Klaviyo segments, or ActiveCampaign:
```bash
openclaw exec audience-micromoment-mapper \
  --input tickets.json \
  --export-to hubspot \
  --sync-segment "at_risk_churners" \
  --assign-workflow "save_my_subscription"
```

---

## Safety & Guardrails

### What This Skill Will NOT Do

❌ **Does not make automated decisions**: The skill recommends interventions; human judgment must approve all outreach.

❌ **Does not collect new personal data**: Analyzes only data you've already collected (with appropriate consent). GDPR, CCPA, and privacy-law compliant.

❌ **Does not manipulate or deceive**: Av