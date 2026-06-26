---
name: ad-intelligence
description: >
  Competitive ad intelligence skill for fetching, analyzing, and reporting on competitor ads
  across Meta (Facebook/Instagram), Google Ads Transparency Center, and LinkedIn Ad Library.
  Use this skill whenever a user asks about competitor ads, what ads a brand is running,
  ad creative analysis, ad copy research, campaign monitoring, ad library lookups, or
  marketing intelligence on any of these platforms. Also trigger for phrases like "what ads
  is [company] running", "spy on competitor ads", "find ads from [brand]", "check ad library",
  "pull ad data", "analyze competitor campaigns", or any request involving scraping or fetching
  public ad data from Meta, Google, or LinkedIn. This is a two-phase skill — Phase 1 uses web
  scraping (no API keys needed), Phase 2 unlocks deeper data via official and third-party APIs.
---

# Ad Intelligence Skill

A two-phase competitive ad intelligence skill for marketing companies and ecommerce owners
to research how competitors run ads across Meta, Google, and LinkedIn.

---

## Quick Reference: What Data Is Available

| Field | Meta (FB/IG) | Google Transparency | LinkedIn |
|---|---|---|---|
| Ad copy / headline | ✅ Both phases | ✅ Both phases | ✅ Both phases |
| Creative (image/video URL) | ✅ Both phases | ✅ Both phases | ✅ Both phases |
| Ad format type | ✅ Both phases | ✅ Both phases | ✅ Both phases |
| Date first/last shown | ✅ Both phases | ✅ Both phases | ✅ Both phases |
| Platform / placements | ✅ Both phases | ✅ (Google Search, YT, Display, etc.) | ✅ Both phases |
| Active / inactive status | ✅ Both phases | ✅ Both phases | ✅ Both phases |
| CTA button | ✅ Phase 1 scrape | ❌ | ✅ Both phases |
| Destination / landing URL | ✅ Both phases | ✅ Both phases | ✅ Both phases |
| Total ads running | ✅ Phase 2 | ✅ Phase 2 | ✅ Phase 2 |
| Impression range | ✅ Phase 2 (EU/political only) | ❌ | ✅ Phase 2 (some scrapers) |
| Spend range | ✅ Phase 2 (EU/political only) | ❌ | ❌ |
| Demographic breakdown | ✅ Phase 2 (EU only) | ❌ | ❌ |
| Targeting info | ❌ | ❌ | ✅ Phase 2 (partial — language, location) |
| Advertiser ID | ✅ Phase 2 | ✅ Phase 2 | ✅ Phase 2 |

> ⚠️ No platform exposes: exact spend, CTR, conversion rates, ROAS, or detailed audience targeting.

---

## Workflow

### Step 1: Understand the Request

Gather from the user (ask if not provided):
- **Competitor name or domain** (e.g., "Nike" or "nike.com")
- **Target platform(s)**: Meta / Google / LinkedIn (default: all three)
- **Phase**: Phase 1 (quick, no API keys) or Phase 2 (deeper, requires API keys)
- **Country/region** filter (optional, e.g., "US", "IN", "EU")
- **Date range** (optional, e.g., "last 30 days")
- **Ad format filter** (optional: image / video / carousel / text)

If the user hasn't said which phase they want, ask. If they're just exploring, start with Phase 1.

---

### Step 2: Execute the Right Phase

Read the platform reference files for code, endpoints, and examples:

- **Meta**: `references/meta.md`
- **Google**: `references/google.md`
- **LinkedIn**: `references/linkedin.md`

Each reference contains:
- Phase 1: Python scraping code (no API key needed)
- Phase 2a: Official/free API instructions
- Phase 2b: Third-party paid API options (SerpAPI, SearchAPI, Adyntel, Apify)
- Sample output JSON
- Known limitations

---

### Step 3: Format the Output

Always deliver **both**:

#### A. Human-Readable Summary Report

```
## Ad Intelligence Report: [Company Name]
**Platforms Searched:** Meta, Google, LinkedIn
**Date:** [today]
**Phase:** 1 (Scrape) / 2 (API)
**Country:** [region]

### 📊 Overview
- Total ads found: X
- Active ads: X | Inactive: X
- Formats: X% image, X% video, X% carousel

### 🎯 Platform Breakdown
[Per platform: count, date range, notable trends]

### ✍️ Creative Themes & Messaging Patterns
[Summarize recurring hooks, CTAs, offers, tone]

### 📅 Recency & Cadence
[How often they post new ads, seasonal patterns]

### ⚠️ Data Limitations
[Note what wasn't available and why]
```

#### B. Raw Structured Data (JSON)

Return normalized JSON with this schema for each ad:

```json
{
  "platform": "meta|google|linkedin",
  "ad_id": "string",
  "advertiser_name": "string",
  "advertiser_page_url": "string",
  "status": "active|inactive",
  "format": "image|video|carousel|text|document",
  "headline": "string|null",
  "body_text": "string|null",
  "cta_text": "string|null",
  "destination_url": "string|null",
  "creative_url": "string|null",
  "platforms_served": ["facebook", "instagram", "messenger"],
  "date_first_shown": "YYYY-MM-DD|null",
  "date_last_shown": "YYYY-MM-DD|null",
  "country": "string|null",
  "spend_range": "string|null",
  "impression_range": "string|null",
  "targeting_summary": "string|null",
  "source_phase": 1
}
```

---

### Step 4: Provide Next Steps

After presenting results, always suggest:
- Which Phase 2 option would give more depth for this use case
- What API keys/accounts are needed to upgrade
- Whether the data is sufficient or the user should broaden/narrow their search

---

## Important Limitations to Always Communicate

1. **No private performance data**: CTR, conversions, ROAS, exact spend — these are never public.
2. **Meta API geographic restriction**: The official Meta Ad Library API only returns impression/spend data for EU-delivered ads and political/social cause ads globally. For general ecommerce ads in non-EU regions, Phase 1 scraping often gives broader coverage.
3. **Google has no official public API**: All Google Transparency Center data is accessed via scraping (Phase 1) or third-party wrappers like SerpAPI/SearchAPI (Phase 2).
4. **LinkedIn targeting data is partial**: Only language and location hints are sometimes visible — not job title, seniority, or company size targeting.
5. **Rate limits apply**: All platforms rate-limit requests. Use pagination and add delays (1–2s between calls).

---

## Phase Decision Guide

| Situation | Recommended Phase |
|---|---|
| Quick competitive overview | Phase 1 |
| No API keys available | Phase 1 |
| Need date-range filtering | Phase 2 |
| EU market + want spend/impressions | Phase 2 (official Meta API) |
| Need 500+ ads at scale | Phase 2 (paid third-party API) |
| B2B competitor research on LinkedIn | Phase 2 |
| Need creative image/video downloads | Phase 2 |

---

## Reference Files

- `references/meta.md` — Meta (Facebook/Instagram) scraping + API code
- `references/google.md` — Google Ads Transparency scraping + SerpAPI/SearchAPI
- `references/linkedin.md` — LinkedIn Ad Library scraping + third-party APIs
