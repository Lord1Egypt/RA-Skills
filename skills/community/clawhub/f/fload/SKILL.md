---
name: fload
description: Use when the user has Fload MCP tools available and asks about mobile app analytics, reviews, growth metrics, ad performance, anomalies, or app store optimization. Teaches effective use of Fload's 18 MCP tools for mobile app publishers.
license: MIT
metadata:
  author: fload-ai
  version: "1.0.0"
---

# Fload — Mobile App Analytics via MCP

You have access to Fload MCP tools for mobile app analytics. Use them to help the user understand their app performance, manage reviews, track growth, and optimize their mobile app business.

## What Is Fload?

Fload is a SaaS platform for mobile app publishers. It aggregates data from App Store Connect, Google Play Console, ad platforms (Apple Search Ads, Google Ads, Meta, TikTok), Stripe, RevenueCat, and more. It provides AI-powered review management, anomaly detection, growth scoring, and app valuations.

## Available Tools

### App Data
- **list_apps** — List all apps in the user's organization. Use first to discover what apps are available.
- **get_app_details** — Get detailed app info (metadata, valuation, platform). Accepts assetId or bundleId.

### Reviews
- **get_reviews** — Get app reviews with filtering (rating, date range, replied status, platform). Essential for sentiment analysis and support workflows.

### Metrics & Analytics
- **discover_metrics** — Discover what metrics are available for an app. Always call this first before querying data.
- **get_metrics** — Query metric timeseries (supports 30+ metrics: proceeds, totalDownloads, activeSubs, sessions, crashes, adSpend, etc.). Can query multiple metrics at once and break down by dimension.
- **discover_dimensions** — Discover available breakdown dimensions (country, platform, app version, campaign) and their values.

### AI Agents
- **list_agents** — List Fload's AI agents (review, monitoring, forecasting, growth, ASO, ads, product, submission review).
- **get_agent_details** — Get agent configuration for a specific app.
- **get_agent_run_history** — Get execution history for an agent.

### Anomalies
- **get_anomalies** — Get detected metric anomalies (surges/declines). Filter by severity, type, status, date range.

### Ads
- **get_ads_performance** — Get ad campaign data across Apple Search Ads, Google Ads, Meta, TikTok.

### Growth
- **get_growth_audit** — Comprehensive growth assessment synthesizing reviews, anomalies, valuations, and connector health.
- **get_growth_score** — Calculated 0-100 growth score with letter grade and factor breakdown.

### Forecasting
- **get_forecasts** — Valuation-based forecasts with trend analysis and projections.

### Dashboard
- **get_dashboard_overview** — Organization-wide portfolio overview with revenue, downloads, and connector health.

### Actions
- **list_pending_actions** — List AI-generated review replies awaiting approval.
- **approve_action** — Approve a pending review reply (optionally edit first).
- **reject_action** — Reject and delete a pending review reply.

## Common Workflows

### "How is my app doing?"
1. `list_apps` to find the app
2. `get_growth_score` for a quick health check
3. `discover_metrics` to see what data exists, then `get_metrics` for revenue/downloads trends
4. `get_anomalies` for any recent issues

### "Show me my reviews"
1. `get_reviews` with appropriate filters
2. For negative reviews: filter by rating 1-2
3. For unreplied: filter by replied=false
4. `list_pending_actions` to see AI-drafted replies

### "What's happening with my ads?"
1. `get_ads_performance` — optionally filter by platform
2. Combine with `get_metrics` for downloads to calculate organic vs paid

### "Give me a full business overview"
1. `get_dashboard_overview` for portfolio-level metrics
2. `list_apps` then `get_growth_score` for each app
3. `get_anomalies` for anything needing attention

### "Help me understand this metric change"
1. `get_metrics` for the affected metric
2. `get_anomalies` to see if Fload detected it
3. `get_growth_audit` for broader context

## Tips

- Always start with `list_apps` if you don't know the user's app IDs
- Use `get_growth_score` for a quick pulse check — it synthesizes multiple signals
- The `get_growth_audit` tool is the most comprehensive single-call assessment
- Review tools work across platforms (iOS + Android) simultaneously
- Anomaly detection covers: revenue, downloads, active subscriptions, trials, and more
- When presenting data, format numbers nicely (currency for revenue, comma separators for counts)
- Use `discover_metrics` before `get_metrics` to know what metrics are available for an app
- Use `discover_dimensions` to find breakdown options (country, platform, etc.) before using dimensional queries
