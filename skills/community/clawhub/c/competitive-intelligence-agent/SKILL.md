---
name: competitive-intelligence-agent
description: Monitors competitors across pricing, social media, online reviews, and product changes — distills everything into a concise weekly briefing.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - curl
        - wget
    category: Automation
---

# Competitive Intelligence Agent

## Name & Purpose
Monitors competitors across pricing, social media, online reviews, and product changes — then distills everything into a concise weekly briefing. No more manual tab-switching across 20 competitor pages.

## Prerequisites

| Requirement | Version/Detail |
|---|---|
| OpenClaw | v2.4+ |
| Python 3 | v3.10+ |
| Playwright | v1.40+ (for JavaScript-rendered pages) |
| curl/wget | For API-based data sources |
| API key (opt.) | BrightData/ScrapingBee for blocked sites |

## Installation

### 1. Copy skill files

```bash
cp -r streams/01_ClawHub_Skills/03_Competitive_Intelligence_Agent/* ~/.openclaw/skills/
```

### 2. Install dependencies

```bash
cd ~/.openclaw/skills/competitive-intelligence
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure competitors

Edit `config/targets.yaml`:

```yaml
competitors:
  - name: "Competitor A"
    website: "https://competitor-a.com"
    pricing_url: "https://competitor-a.com/pricing"
    social:
      twitter: "@comp_a"
      linkedin: "competitor-a"
      facebook: "CompetitorAPage"
    review_sites:
      - "https://www.hellopeter.com/competitor-a"
      - "https://www.g2.com/products/competitor-a"
    monitoring:
      pricing_check: daily
      social_check: daily
      reviews_check: weekly
      product_check: weekly
```

### 4. Set up report delivery

Edit `config/delivery.yaml`:

```yaml
delivery:
  channel: "slack" # Options: slack, email, telegram, file
  slack_webhook: "https://hooks.slack.com/services/..."
  email:
    to: "team@yourcompany.com"
    from: "ci-agent@yourcompany.com"
  schedule:
    weekly_report: "0 9 * * 1"  # Monday 9 AM
    daily_alerts: "0 8 * * 1-5" # Weekdays 8 AM

  # What triggers a real-time alert (not just in the weekly report)
  alerts:
    - type: price_change
      threshold_percent: 10
    - type: new_product_launch
    - type: review_drop
      threshold_stars: 1.5
    - type: leadership_change
    - type: funding_round
```

## Usage

### Run a full intelligence sweep

```bash
# Immediate sweep of all configured competitors
openclaw skill run competitive-intelligence --full-sweep

# Specific competitor only
openclaw skill run competitive-intelligence --target "Competitor A"

# Specific data source only
openclaw skill run competitive-intelligence --source pricing
```

### Generate reports

```bash
# Weekly report (summary for all monitored metrics)
openclaw skill run competitive-intelligence --report weekly

# Pricing snapshot
openclaw skill run competitive-intelligence --report pricing

# Social media sentiment
openclaw skill run competitive-intelligence --report social

# Competitive landscape overview
openclaw skill run competitive-intelligence --report landscape

# Custom date range
openclaw skill run competitive-intelligence --report weekly --from "2025-01-01" --to "2025-01-07"
```

### Watch mode (continuous)

```bash
# Start continuous monitoring (uses configured schedule)
openclaw skill run competitive-intelligence --watch
```

## Workflow

```
Target Configuration (competitors + metrics + schedules)
  ├── Daily: Pricing Check → Compare → Alert on Δ > 10%
  ├── Daily: Social Monitor → Sentiment Analysis → Flag trends
  ├── Weekly: Review Scrape → Aggregate → Summary
  ├── Weekly: Product/Website Changes → Diff → Changelog
  └── Weekly: Generate Report → Deliver (Slack/Email/Telegram)
```

## Available Commands

| Command | Description |
|---|---|
| `/sweep` | Trigger full intelligence sweep now |
| `/report` | Generate weekly briefing immediately |
| `/alert <type>` | Show recent alerts (price, social, review, product) |
| `/competitors` | List all monitored competitors |
| `/add-competitor` | Interactive wizard to add a new competitor |
| `/remove <name>` | Stop monitoring a competitor |
| `/status` | Show monitor health, last sweep time, next scheduled sweep |
| `/export <format>` | Export data as CSV or JSON (format: csv, json) |
| /config | Show current monitoring configuration |

## Data Collection Methods

### Pricing Scraping
```yaml
# config/scraping.yaml extract
pricing:
  methods:
    - type: "css_selector"
      description: "Scrape pricing page with CSS selectors"
      example: "div.pricing-card span.price"
    - type: "api_endpoint"
      description: "Check for public pricing API"
      example: "https://api.competitor.com/v1/pricing"
    - type: "playwright"
      description: "Full browser render for JS-heavy pricing pages"
  comparison:
    price_fields:
      - plan_name
      - monthly_price
      - annual_price
      - features_included
      - user_limit
```
Prompt-Driven Analysis:
```yaml
# config/analysis.yaml extract
analysis:
  - name: pricing_analysis
    description: "Compare own pricing vs competitors"
    prompt: |
      Compare {{our_pricing}} to {{competitor_pricing}}.
      Identify:
      - Where we're more expensive
      - Where we're cheaper
      - Feature gaps at each price point
      - Recommended pricing adjustments
      - Market positioning suggestions
```

### Social Media Monitoring
```yaml
social:
  platforms:
    - twitter
    - linkedin
    - facebook
  monitoring:
    frequency: daily
    metrics:
      - follower_count
      - engagement_rate
      - sentiment_score
      - top_posts
      - response_time
  alert_rules:
    - metric: sentiment_score
      direction: drop
      threshold: 0.3
      action: alert
```

### Review Aggregation
```yaml
reviews:
  sites:
    - hellopeter
    - g2
    - trustpilot
    - cacx (South Africa)
    - google_reviews
  aggregation:
    metrics:
      - average_rating
      - review_count
      - sentiment_breakdown
      - common_complaints_cloud  # most common complaint keywords
      - common_praise_cloud      # most common praise keywords
  alert_rules:
    - metric: average_rating
      direction: drop
      threshold: 1.5
      window: 7d
      action: alert
```

## Weekly Report Template

The generated report follows this structure:

```
╔══════════════════════════════════════════╗
║  COMPETITIVE INTELLIGENCE BRIEFING      ║
║  Week 3 | Jan 13–19, 2025              ║
╚══════════════════════════════════════════╝

📊 EXECUTIVE SUMMARY
  - Key movements this week
  - Top 3 things to act on
  - Risk level: [Low/Medium/High]

💰 PRICING CHANGES
  Competitor A → Increased Enterprise by 15%
  Competitor B → Launched Freemium tier

📱 SOCIAL MEDIA
  Competitor A → Viral tweet about [topic]
  Competitor C → Follower growth +22% (attributed to campaign)

⭐ REVIEW CHANGES
  Competitor B → Hellopeter dropped 3.2 → 2.8
  Common complaints: [support wait time, uptime]

🚀 PRODUCT LAUNCHES
  Competitor A → New AI analytics feature
  Competitor C → Mobile app v2.0

📰 NEWS & HIRING
  Competitor B raised $5M Series A
  Competitor A hired new CMO from [company]

🎯 RECOMMENDATIONS
  1. Match dropdown on Enterprise tier pricing
  2. Highlight our 24/7 support (competitor weakness)
  3. Consider AI analytics feature for Q3 roadmap

────────────────────────────────────────
  Generated by Competitive Intelligence Agent
  Next report: Mon Jan 20, 2025
```

## Example Prompts for Human Operators

> "Hey Marvis, run a full competitive sweep and send me the briefing."
> "Add 'Competitor D' to monitoring — here's their website and social links."
> "Alert me if any competitor drops their price by more than 10%."
> "What are the common complaints about our competitors on Hellopeter?"
> "Show me the pricing comparison between us and Competitor A."
> "Send the weekly report to the #competitive-intel Slack channel."
> "Which competitor launched something new this week?"

## Directory Structure

```
competitive-intelligence/
├── SKILL.md
├── README.md
├── config/
│   ├── targets.yaml           # Competitor profiles (websites, social, review sites)
│   ├── scraping.yaml          # CSS selectors, API endpoints, playwright config
│   ├── analysis.yaml          # Analysis prompts and comparison rules
│   ├── delivery.yaml          # Report delivery channels and schedules
│   └── alerts.yaml            # Alert thresholds and notification rules
├── collectors/
│   ├── pricing.py             # Price scraping logic
│   ├── social.py              # Social media monitoring
│   ├── reviews.py             # Review aggregation
│   ├── product_changes.py     # Website/product diffing
│   └── news.py                # News and hiring monitoring
├── analyzers/
│   ├── pricing_comparison.py
│   ├── sentiment.py
│   ├── product_gap.py
│   └── trend_analysis.py
├── templates/
│   └── weekly_report.md       # Weekly briefing template
├── output/
│   ├── reports/               # Generated reports (archived by week)
│   ├── data/                  # Raw data dumps (rotated after 90 days)
│   └── screenshots/           # Evidence snapshots (when alerts trigger)
├── scripts/
│   ├── full-sweep.sh          # Complete intelligence sweep
│   ├── test-collectors.sh     # Verify all collectors work
│   └── setup-cron.sh          # Install cron jobs for schedules
├── requirements.txt
└── package.json
```

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Pricing page returns empty | CSS selector changed | Update `config/scraping.yaml` selectors |
| Social metrics stale | API rate limit hit | Increase `check_interval` in targets.yaml |
| Report not delivered | Slack webhook URL wrong | Check `config/delivery.yaml` |
| Playwright failing | Headless browser issue | Run `playwright install chromium` |
| "No data for competitor" | Target URL unreachable | Verify URL or add proxy in scraping config |
| Alerts not firing | Threshold too conservative | Lower `threshold_percent` in alerts.yaml |
| Reviews returning nothing | Review site blocks scraping | Add `user_agent` or rotate proxy |
| Memory grows over time | Data not rotated | Check output/data rotation schedule |
