---
name: ad-platform-tracker
description: >
  Use this skill whenever the user needs to track, analyze, or respond to advertising platform
  changes across Meta (Facebook/Instagram), Google Ads, or competitor intelligence.
  Trigger for any of these requests: Meta algorithm updates, Andromeda implications, Google Ads
  policy changes, Performance Max updates, privacy/compliance tracking (GDPR, CCPA, iOS),
  competitor ad analysis, campaign impact assessment, ad policy audits, regulatory compliance
  checks, platform feature rollouts, algorithm behavior changes, creative strategy updates from
  platform shifts, competitor ad library scraping, or any question like "what changed on Meta/Google?",
  "how does X update affect my campaigns?", "is my account compliant?", "what are competitors running?".
  Always use this skill — do not rely on training memory for fast-changing platform details.
---

# Ad Platform Tracker Skill

A comprehensive skill for tracking algorithm changes, policy updates, compliance requirements,
and competitive intelligence across Meta and Google Ads platforms.

---

## Four Tracking Modules

| Module | File | Purpose |
|--------|------|---------|
| Meta Algorithm & Policy | `references/meta-tracker.md` | Meta ad system changes, Andromeda, features |
| Google Ads Algorithm & Policy | `references/google-tracker.md` | PMax, Smart Bidding, AI Max, policy changes |
| Regulatory & Compliance | `references/compliance-tracker.md` | GDPR, CCPA, iOS privacy, ad policies |
| Competitive Intelligence | `references/competitive-tracker.md` | Competitor ads, benchmarks, best practices |

**When to load each file:**
- Meta question → load `meta-tracker.md`
- Google Ads question → load `google-tracker.md`
- Compliance/privacy/policy question → load `compliance-tracker.md`
- Competitor/benchmarking question → load `competitive-tracker.md`
- General audit or "check everything" → load all four

---

## Quick Assessment Framework

When a user reports a campaign issue or asks "why did X change?", run through this:

1. **Platform Change?** → Check the relevant tracker file for recent algorithm/feature updates
2. **Compliance Risk?** → Check if account/vertical is in a sensitive category (health, finance, political)
3. **Creative Fatigue?** → For Meta: check creative diversity, similarity scores, refresh cycle
4. **Structural Issue?** → For Google PMax: check channel reporting, negative keywords, asset quality
5. **Competitive Shift?** → Check if competitors changed messaging, offers, or formats

---

## Output Templates

### Daily Update Digest
```
DATE: [date]
PLATFORM: Meta / Google / Both
CHANGE: [what changed]
SEVERITY: Critical / High / Medium / Low
IMPACT DATE: [when it takes effect]
AFFECTED: [all accounts / specific verticals / regions]
RECOMMENDED ACTION: [what to do]
```

### Campaign Impact Assessment
```
UPDATE: [name of update]
CURRENT CAMPAIGN STATUS: [affected / not affected]
METRICS AT RISK: [ROAS, CPM, CPA, reach, etc.]
URGENCY: [act now / act within 30 days / monitor]
SPECIFIC CHANGES NEEDED: [list]
```

### Compliance Alert
```
REGULATION: [GDPR / CCPA / Meta Policy / Google Policy]
RISK LEVEL: High / Medium / Low
DEADLINE: [compliance required by]
AFFECTED CAMPAIGNS: [list]
REMEDIATION STEPS: [numbered list]
```

---

## Data Sources to Monitor

**Meta Official:**
- Meta for Business blog: https://www.facebook.com/business/news
- Meta Transparency Center: https://transparency.fb.com/
- Meta Ads Library: https://www.facebook.com/ads/library
- Meta Graph API changelog: https://developers.facebook.com/docs/graph-api/changelog

**Google Official:**
- Google Ads blog: https://blog.google/products/ads-commerce/
- Google Ads Help Center: https://support.google.com/google-ads
- Google Ads Developer Blog: https://ads-developers.googleblog.com/
- Google Marketing Live announcements (annual, May)

**Industry Sources (fast-track updates):**
- Jon Loomer Digital (Meta expert): https://jonloomer.com
- Social Media Examiner: https://socialmediaexaminer.com
- Search Engine Journal (Google Ads): https://searchenginejournal.com
- WordStream / Search Engine Land: https://wordstream.com
- Foxwell Digital (Meta policy specialist): https://foxwelldigital.com

**Competitive Intelligence:**
- Meta Ads Library API: https://www.facebook.com/ads/library/api/
- Google Ads Transparency Center: https://adstransparency.google.com/

---

## Scraping Strategy

When asked to monitor or scrape platform updates, use the **web-scraper skill** (Firecrawl or Apify) to:

1. **Official blogs** → Firecrawl `/crawl` on Meta/Google blog URLs, filter for last 7 days
2. **Meta Ads Library** → Apify actor `apify/facebook-ads-scraper` for competitor ads
3. **Google Ads Transparency** → Firecrawl `/scrape` on specific advertiser pages
4. **Industry blogs** → Firecrawl `/search` for recent updates ("Meta algorithm update 2025")
5. **RSS feeds** → Firecrawl `/scrape` on RSS feed URLs for real-time monitoring

```python
# Example: Monitor Meta blog for updates in last 7 days
firecrawl_payload = {
    "url": "https://www.facebook.com/business/news",
    "formats": ["markdown"],
    "onlyMainContent": True,
}

# Example: Search for recent Google Ads changes
firecrawl_search = {
    "query": "Google Ads Performance Max update 2025",
    "limit": 10,
    "scrapeOptions": { "formats": ["markdown"] }
}
```

---

## Current State of Knowledge (as of early 2026)

### Meta — Critical Facts
- **Andromeda** fully rolled out globally October 2025 — creative is now the primary targeting mechanism
- Andromeda uses NVIDIA Grace Hopper Superchip, 10,000x increase in model capacity vs. predecessor
- **Engaged-view window** changed from 10s → 5s in 2025
- **Value Rules** expanded to Leads objective
- **Threads Feed** placement added — test for scaling
- **Lookalike restrictions** on health/finance data (Sept 2025)
- **Creative similarity scoring** active — too-similar ads punished with higher CPMs
- Sensitive category blocking (health, finance) started January 2025 — blocks mid/lower funnel events
- Meta AI chatbot personalization rolled out Dec 16, 2025 (excluding EU/UK/South Korea)

### Google Ads — Critical Facts
- **PMax channel-level reporting** went live November 2025 for all accounts
- **Full Search Terms Reporting** in PMax added in 2025
- **Campaign-level negative keywords** (10k limit) added January 2025
- **Search themes** expanded from 25 → 50 per asset group
- **AI Max** launched at Google Marketing Live May 2025 (new search campaign type)
- **Power Pack** = PMax + Demand Gen + AI Max (Google's new recommended setup)
- **Demand Gen** showed 26% conversion increase in tests
- **Waze ads** inventory added to PMax store goals (US only, Nov 2025)
- First-party audience exclusions added to PMax (2026 rollout)
- Budget projection report added to PMax

### Compliance — Critical Facts
- 19 US state privacy laws in effect by 2025
- Meta blocks custom audiences with sensitive attributes (health/finance) as of Sept 2025
- GDPR: requires opt-in, up to €20M or 4% global revenue fines
- CCPA/CPRA: opt-out model; requires "Do Not Sell" link
- Health/wellness brands: Add to Cart and Purchase events blocked for optimization (Jan 2025)
- Financial services: new mandatory Special Ad Category (Jan 14, 2025)
- Political ads: "Paid for by" disclaimer required, tighter targeting restrictions

For full deep-dive detail on any module, load the relevant reference file.
