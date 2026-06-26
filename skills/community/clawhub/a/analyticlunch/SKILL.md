---
name: analyticlunch
description: Query live traffic data, tracking links, and weekly reports from AnalyticLunch
metadata:
  openclaw:
    requires:
      config:
        - skills.entries.analyticlunch.apiKey
---

# AnalyticLunch — Traffic & Competitive Intelligence

You have access to the AnalyticLunch API for querying website traffic data, managing tracking links, and pulling competitive intelligence reports.

## Authentication

Every request must include the header `x-api-key` with the value from your config (`skills.entries.analyticlunch.apiKey`).

Base URL: `https://analyticlunch.com`

## Available Actions

### 1. List tracked websites

Returns all websites the user is tracking with their site IDs, domains, and status.

```
GET /api/traffic/sites
```

Use this first to discover site IDs needed for other calls.

### 2. Get traffic summary

Returns traffic overview for a specific site: total visitors, top sources, top pages, device split, daily visitor data, and conversion funnel.

```
GET /api/traffic/dashboard/{siteId}?period={period}
```

Parameters:
- `siteId` (required): The traffic site ID from list_traffic_sites
- `period` (optional): `7d`, `30d`, `6m`, or `1y`. Default: `7d`

When reporting traffic data:
- Lead with unique visitors (more meaningful than raw pageviews)
- Highlight the top 3 traffic sources
- Note any significant trends (pageviewsTrend, visitorsTrend are percentages vs previous period)
- If dailyData is present, mention any notable spikes or dips

### 3. List tracking links

Returns all tracking links for a site with their URLs, labels, and click data.

```
GET /api/traffic/links?siteId={siteId}
```

### 4. Create a tracking link

Creates a new tracking link to measure traffic from a specific source (Instagram bio, email footer, Google ad, etc.).

```
POST /api/traffic/links
Content-Type: application/json

{
  "trafficSiteId": "{siteId}",
  "destinationUrl": "https://example.com/page",
  "label": "Instagram Bio",
  "suggestedPlacement": "instagram_bio"
}
```

After creating, return the tracking URL to the user so they can place it.

### 5. Get latest weekly report

Returns the most recent weekly competitive intelligence report for the user, including ranking changes, new competitors, review trends, and visibility summaries.

```
GET /api/weekly-report
```

## How to call

Use `exec` with curl. Always include the API key header.

Example:
```bash
curl -s -H "x-api-key: $ANALYTICLUNCH_API_KEY" "https://analyticlunch.com/api/traffic/sites"
```

Example with POST:
```bash
curl -s -X POST -H "x-api-key: $ANALYTICLUNCH_API_KEY" -H "Content-Type: application/json" -d '{"trafficSiteId":"SITE_ID","destinationUrl":"https://example.com","label":"My Link"}' "https://analyticlunch.com/api/traffic/links"
```

## When to use this skill

- User asks about website traffic, visitors, page views, or traffic sources
- User asks "how's my website doing" or "how's traffic"
- User wants to create a tracking link for marketing
- User asks about competitors, rankings, or visibility
- User asks for their weekly report
- User mentions AnalyticLunch, traffic dashboard, or tracking links

## Response style

Be conversational. Don't dump raw JSON. Summarize the key numbers and insights. For example:

"danstvmounting.com had 171 unique visitors this week. Top sources: Google Search (100), Facebook (65), Direct (24). Your most visited page after the homepage is the flush mount service page. Mobile traffic dominates at 85%."
