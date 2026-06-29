---
name: Analyze Customer Sentiment & Intent with AI Classification
description: "Analyze comments, DMs, and replies across YouTube, TikTok, Instagram, and email to extract buying intent, pain points, and churn signals. Use when the user needs audience sentiment tracking, content gap analysis, or early warning systems for brand reputation."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {"openclaw":{"requires":{"env":["YOUTUBE_API_KEY","TIKTOK_API_KEY","INSTAGRAM_BUSINESS_ACCOUNT_ID","ANTHROPIC_API_KEY"],"bins":["python3","jq"]},"os":["macos","linux","win32"],"files":["SKILL.md"],"emoji":"📊"}}
---

## Overview

The **Audience Sentiment & Intent Analyzer** transforms raw social engagement into strategic intelligence. Instead of manually scrolling through thousands of comments, this skill automatically ingests comments, DMs, and replies from YouTube, TikTok, Instagram, and email—then applies advanced NLP analysis to extract:

- **Intent signals**: Buying intent, pain points, feature requests, unmet needs
- **Sentiment velocity trends**: Identify whether audience sentiment is accelerating positive or negative over time
- **Emerging topics**: Flag discussion patterns before they trend publicly
- **Churn indicators**: Early warning signs of audience dissatisfaction or drift
- **Audience persona shifts**: Detect changes in who's engaging and why

The skill returns **structured JSON** with audience persona evolution, content gaps based on actual user requests, and actionable recommendations for content pivots. Perfect for content creators, agencies, product teams, and marketing leaders who want to lead audience needs instead of react to them.

**Integrations**: Connects with YouTube Data API v3, TikTok Business API, Instagram Graph API, Gmail/Google Workspace, Slack (for alert notifications), and supports CSV/JSON imports from manual data collection.

---

## Quick Start

### Example 1: Analyze YouTube Comments for Buying Intent

```
Analyze the last 500 comments on my YouTube channel for buying intent signals.
Extract pain points, feature requests, and sentiment trends. Flag any negative
sentiment spikes. Return as JSON with persona shifts and content gap analysis.
Channel ID: UC_example123
```

**What happens:**
- Fetches recent comments via YouTube Data API
- Segments by intent type (buying, support, feature request, complaint)
- Tracks sentiment velocity over the last 30 days
- Returns actionable content recommendations

### Example 2: Monitor TikTok DMs for Churn Signals

```
Scan my TikTok DMs from the last 2 weeks for any signs of audience dissatisfaction,
complaints about product quality, or requests to unsubscribe. Highlight sentiment
changes and calculate churn risk score (0-100). Show me the top 5 emerging complaints.
```

**What happens:**
- Analyzes direct messages for negative sentiment patterns
- Calculates churn risk using behavioral linguistics
- Groups complaints by category
- Recommends response templates

### Example 3: Cross-Platform Sentiment Velocity Report

```
Compare sentiment trends across YouTube, TikTok, and Instagram from the last 60 days.
Show me which platforms have accelerating positive/negative sentiment. Flag any
emerging topics that appear on 2+ platforms. Create an audience persona update
showing how my audience has evolved.
```

**What happens:**
- Aggregates data from all platforms
- Calculates sentiment velocity (rate of change)
- Identifies cross-platform consensus topics
- Generates persona evolution report

---

## Capabilities

### 1. Multi-Platform Data Ingestion
- **YouTube**: Comments, replies, Community posts, Shorts comments (via YouTube Data API v3)
- **TikTok**: Comments, DM content, video engagement (TikTok Business API)
- **Instagram**: Comments, DMs, Story replies, Reels comments (Instagram Graph API)
- **Email**: Gmail/Google Workspace thread analysis
- **Manual input**: Upload CSV or JSON files with user feedback

### 2. Intent Classification Engine
Automatically categorizes engagement by intent type:
- **Buying intent**: Language patterns indicating purchase readiness ("How much?", "Where to buy?", "Does it come in...?")
- **Support requests**: Questions, troubleshooting, how-to queries
- **Feature requests**: "Can you add...", "I wish...", "It would be great if..."
- **Complaints/pain points**: Negative sentiment with specific problems
- **Compliments/positive feedback**: Satisfaction signals, testimonials
- **Churn indicators**: "Unsubscribing", "Moving to competitor", "Disappointed"

### 3. Sentiment Velocity Analysis
- Tracks sentiment change over time windows (daily, weekly, monthly)
- Calculates acceleration/deceleration rates
- Identifies turning points in audience mood
- Alerts on sentiment spikes (>15% change in 7 days)

### 4. Topic Extraction & Emerging Trends
- Uses topic modeling to identify most-discussed themes
- Flags emerging topics (appearing in 5%+ of recent engagement but <2% historically)
- Cross-references with broader social trends via optional web search integration
- Segments topics by urgency and audience size

### 5. Audience Persona Evolution
- Builds demographic/psychographic profiles from language patterns
- Tracks persona shifts over time (age approximation, interests, pain points)
- Identifies audience segment expansion or contraction
- Shows content preferences implied by engagement patterns

### 6. Content Gap Analysis
- Analyzes feature requests and pain points not addressed in current content
- Recommends 5-10 content ideas based on actual audience demand
- Prioritizes recommendations by request frequency and intent strength
- Shows which content topics have highest engagement potential

### 7. Early Warning System
- Monitors for reputation threats (product complaints, service issues)
- Flags coordinated negative campaigns or review bombing
- Alerts on competitor mentions and market shift signals
- Calculates NPS-style sentiment score trends

---

## Configuration

### Required Environment Variables

```bash
# YouTube API (for comments analysis)
export YOUTUBE_API_KEY="your-youtube-api-key"

# TikTok Business API (for comment/DM data)
export TIKTOK_ACCESS_TOKEN="your-tiktok-access-token"
export TIKTOK_BUSINESS_ACCOUNT_ID="your-account-id"

# Instagram Graph API (for comments and DMs)
export INSTAGRAM_BUSINESS_ACCOUNT_ID="your-instagram-business-id"
export INSTAGRAM_ACCESS_TOKEN="your-instagram-access-token"

# Anthropic Claude for NLP analysis
export ANTHROPIC_API_KEY="your-claude-api-key"

# Optional: Gmail for email feedback analysis
export GOOGLE_SERVICE_ACCOUNT_JSON="/path/to/service-account.json"

# Optional: Slack notifications for alerts
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK"
```

### Configuration Options

```yaml
analysis:
  sentiment_window_days: 60           # Historical window for velocity analysis
  emerging_topic_threshold: 5         # % of recent comments to flag as emerging
  churn_risk_threshold: 75            # Score (0-100) to trigger alerts
  languages: ["en", "es", "fr"]       # Supported languages for analysis
  
data_sources:
  youtube:
    enabled: true
    max_comments_per_run: 500
    channels: ["UC_example1", "UC_example2"]
  
  tiktok:
    enabled: true
    include_dms: true
  
  instagram:
    enabled: true
    include_dms: true
  
  email:
    enabled: false
    gmail_label: "Customer Feedback"

output:
  format: "json"                      # Options: json, csv, markdown
  include_samples: true               # Include example comments in output
  slack_alerts: true
  notification_threshold: "medium"    # Only alert on medium+ priority findings
```

---

## Example Outputs

### Output 1: Sentiment Velocity Report

```json
{
  "analysis_period": "2024-01-01 to 2024-02-29",
  "platforms": ["youtube", "tiktok", "instagram"],
  "overall_sentiment_score": 7.2,
  "sentiment_velocity": 0.15,
  "velocity_interpretation": "Accelerating positive (15% improvement over 30 days)",
  "sentiment_trends": {
    "youtube": {
      "score": 7.5,
      "velocity": 0.12,
      "comment_volume": 2847,
      "top_sentiment_driver": "New product feature announcement"
    },
    "tiktok": {
      "score": 7.8,
      "velocity": 0.22,
      "comment_volume": 5432,
      "top_sentiment_driver": "Viral collaboration content"
    },
    "instagram": {
      "score": 6.5,
      "velocity": 0.08,
      "comment_volume": 1203,
      "top_sentiment_driver": "Community engagement initiatives"
    }
  },
  "sentiment_spikes": [
    {
      "date": "2024-02-15",
      "platform": "youtube",
      "change": "+24%",
      "trigger": "Product launch announcement",
      "affected_audience": "Early adopters, premium segment"
    }
  ]
}
```

### Output 2: Intent Classification & Content Gaps

```json
{
  "intent_breakdown": {
    "buying_intent": {
      "count": 342,
      "percentage": 22,
      "confidence": 0.94,
      "signals": ["pricing questions", "availability checks", "comparison with competitors"],
      "sample_comments": [
        "How much does the pro version cost?",
        "Is it available in Europe yet?"
      ]
    },
    "feature_requests": {
      "count": 198,
      "percentage": 13,
      "confidence": 0.91,
      "top_requests": [
        {"feature": "Dark mode support", "mentions": 47, "priority": "high"},
        {"feature": "API documentation", "mentions": 31, "priority": "high"},
        {"feature": "Mobile app", "mentions": 28, "priority": "medium"}
      ]
    },
    "pain_points": {
      "count": 156,
      "percentage": 10,
      "confidence": 0.87,
      "top_issues": [
        {"issue": "Slow onboarding process", "mentions": 34, "urgency": "high"},
        {"issue": "Documentation gaps", "mentions": 28, "urgency": "high"},
        {"issue": "Export limitations", "mentions": 19, "urgency": "medium"}
      ]
    },
    "churn_indicators": {
      "count": 23,
      "percentage": 1.5,
      "churn_risk_score": 34,
      "risk_level": "low",
      "concerns": ["Competitors offering better pricing", "Feature parity with alternatives"]
    }
  },
  "content_gaps": [
    {
      "gap": "Dark mode implementation",
      "audience_demand": "high",
      "demand_signals": 47,
      "estimated_reach": "2,340 engaged users",
      "recommended_content": "Tutorial: Enabling dark mode + settings guide"
    },
    {
      "gap": "API integration guides",
      "audience_demand": "high",
      "demand_signals": 31,
      "estimated_reach": "1,890 engaged users",
      "recommended_content": "Step-by-step API integration walkthrough, code examples"
    }
  ],
  "recommended_content_calendar": [
    {"topic": "Dark mode tutorial", "priority": 1, "format": "Video + docs", "urgency": "1 week"},
    {"topic": "API documentation overhaul", "priority": 2, "format": "Blog series + video", "urgency": "2 weeks"},
    {"topic": "Competitive positioning guide", "priority": 3, "format": "Blog post", "urgency": "3 weeks"}
  ]
}
```

### Output 3: Audience Persona Evolution

```json
{
  "persona_updates": {
    "primary_persona": {
      "name": "Early Adopter Elena",
      "evolution": "Stable with moderate shift toward feature complexity focus",
      "profile": {
        "estimated_age_range": "25-34",
        "primary_interests": ["product innovation", "API capabilities", "automation"],
        "pain_point_focus_shift": "From onboarding → technical depth",
        "engagement_style": "High-frequency, technical questions, feature requests"
      },
      "signals": {
        "language_shift": "Increased technical jargon usage (+18% this month)",
        "request_complexity": "Escalating from basic to advanced features",
        "sentiment_trend": "Stable positive with occasional frustration on documentation"
      },
      "recommendations": "Create advanced tutorials, API documentation, technical blog content"
    },
    "secondary_persona": {
      "name": "SMB Business Owner",
      "evolution": "Growing segment (+23% engagement month-over-month)",
      "profile": {
        "estimated_age_range": "35-50",
        "primary_interests": ["ROI metrics", "integration with existing tools", "cost-effectiveness"],
        "pain_point_focus": "Integration complexity, total cost of ownership",
        "engagement_style": "Infrequent but high-intent, specific use-case questions"
      },
      "signals": {
        "emergence_trend": "New segment gaining presence",
        "sentiment": "Positive with caution, needs ROI proof",
        "content_requests": "Case studies, ROI calculators, integration guides"
      },
      "recommendations": "Create ROI-focused case studies, integration partnerships, calculator tools"
    },
    "emerging_persona": {
      "name": "Enterprise Decision-Maker",
      "emergence_score": 4.2,
      "signals": {
        "first_detected": "2 weeks ago",
        "mention_volume": "Growing, now ~15 comments/week",
        "key_questions": "Security compliance, SLA guarantees, dedicated support",
        "sentiment": "Neutral-positive, highly analytical"
      },
      "recommendations": "Develop enterprise security documentation, create dedicated sales materials"
    }
  }
}
```

---

## Tips & Best Practices

### 1. Maximize Data Quality
- **Connect all platforms**: The more data sources, the more accurate the persona analysis. YouTube alone gives 60% accuracy; adding TikTok + Instagram boosts it to 85%+.
- **Regular syncs**: Run analysis weekly or bi-weekly, not monthly. Emerging trends surface fastest in 7-day windows.
- **Include historical context**: Analyze at least 60 days of history to establish baseline sentiment and detect true velocity shifts.

### 2. Act on Insights Within 48 Hours
- **Content gaps** lose value if addressed weeks later. When you see a feature request from 30+ people, create content within 48 hours.
- **Set Slack alerts** for churn indicators so your team responds to complaints before they escalate.
- **Publish response content** the same week you identify a pain point—audience memory is short.

### 3. Segment by Audience Size
- Focus on themes mentioned by 5%+ of engaged audience (not just high engagement single comments).
- Emerging topics should hit 15+ mentions in 7 days before you prioritize them.
- Validate against actual traffic/revenue impact, not just comment frequency.

### 4. Track Persona Shifts Monthly
- Set up monthly persona reports and compare quarter-over-quarter.
- When a new persona emerges (like "Enterprise Decision-Maker"), shift your messaging immediately—don't wait.
- Create audience segment-specific content once a persona reaches 10%+ of total engagement.

### 5. Combine with Other Metrics
- Cross-reference sentiment trends with revenue, signups, or email unsubscribe rates.
- Churn signals in comments often precede actual churn by 2-4 weeks.
- Feature requests should be weighted by audience segment value, not just frequency.

### 6. Use for Competitive Intelligence
- Track when competitors are mentioned and in what context (positive, negative, neutral).
- Monitor emerging alternatives in your space through audience language patterns.
- Identify feature parity gaps before customers complain.

---

## Safety & Guardrails

### What This Skill Will NOT Do

- **No automated responses**: This skill analyzes sentiment and intent but does NOT auto-reply to comments or DMs. All response recommendations require human approval.
- **No deletion or moderation without approval**: The skill flags problematic content but requires explicit human authorization before any comment removal.
- **No private data extraction**: Will not extract email addresses, phone numbers,