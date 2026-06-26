# Competitive Intelligence Tracker

## Data Sources & Tools

### Free Tools

**Meta Ads Library**
- URL: https://www.facebook.com/ads/library
- API: https://www.facebook.com/ads/library/api/
- What you can see: All active ads, ad copy, creative preview, run start date, page name, countries targeted
- What you can't see: Spend, impressions, targeting, audience size, CPM (except political ads which show spend range)
- Best for: Competitor creative angles, offer types, messaging strategy, format preferences, ad longevity

**Google Ads Transparency Center**
- URL: https://adstransparency.google.com/
- Shows: Active search and display ads, advertiser name, ad format
- Best for: Competitor Search ad copy, Display creative, YouTube ads

**LinkedIn Ad Library** (for B2B)
- URL: https://www.linkedin.com/ad-library/
- Shows: Active Sponsored Content, copy, creative, CTA

### Paid/Pro Tools
- **SimilarWeb** — traffic sources, ad spend estimates, channel mix
- **SEMrush / SpyFu** — competitor keywords, PPC ad history, Google Ads
- **AdBeat / WhatRunsWhere** — Display ad intelligence
- **Minea / Dropispy / BigSpy** — Meta ad performance signals (engagement data)
- **Pathmatics / Sensor Tower** — digital ad spend estimates by brand

---

## Meta Ads Library API — Scraping Guide

**Get competitor ads programmatically:**

```python
import requests

ACCESS_TOKEN = "YOUR_GRAPH_API_TOKEN"
BASE = "https://graph.facebook.com/v21.0/ads_archive"

params = {
    "access_token": ACCESS_TOKEN,
    "ad_reached_countries": "US",          # or "IN", "GB", etc.
    "search_page_ids": "COMPETITOR_PAGE_ID", # or use search_terms
    "search_terms": "competitor brand name",
    "ad_type": "ALL",                       # ALL, POLITICAL_AND_ISSUE_ADS
    "fields": "id,ad_creation_time,ad_creative_bodies,ad_snapshot_url,page_name,publisher_platforms",
    "limit": 50,
}

resp = requests.get(BASE, params=params)
ads = resp.json().get("data", [])
next_cursor = resp.json().get("paging", {}).get("cursors", {}).get("after")

for ad in ads:
    print(ad.get("page_name"), ad.get("ad_creation_time"))
    print(ad.get("ad_creative_bodies", []))
    print(ad.get("ad_snapshot_url"))
```

**Alternative: Use Apify's Facebook Ads Scraper actor**
- Actor: `apify/facebook-ads-scraper`
- Input: `{ "searchTerms": ["competitor name"], "country": "US", "adTypes": ["ALL"] }`

---

## Competitive Analysis Framework

### What to Analyze

**1. Creative Strategy**
- What formats dominate? (video, static, carousel, UGC, founder-led?)
- What's the hook style? (problem/solution, testimonial, before/after, demo?)
- What visual aesthetic? (polished vs raw, lifestyle vs product, AI-generated vs authentic?)
- Are they using Reels/vertical video? (signal of platform investment)
- How long do winning ads run before rotation? (longevity = proof of performance)

**2. Messaging & Offer**
- What is the primary value proposition?
- What offer type? (discount %, free trial, bundle, BOGO, free shipping, consultation?)
- What urgency mechanism? (scarcity, deadline, social proof count?)
- What CTA? (Shop Now, Learn More, Get Quote, Sign Up — indicates funnel stage)
- Are they addressing objections in ads? (signals mature audience understanding)

**3. Campaign Structure Signals**
- Are they running multiple creatives with different angles? (Andromeda-aware)
- Are they testing UGC vs polished production? (creative diversification)
- Any Advantage+ Shopping Campaigns visible? (ASC = Meta's AI campaign type)
- Frequency of new ads launched? (high = active testing culture)

**4. Platform Mix**
- Meta only? Google only? Both?
- Are they on Threads, YouTube Shorts, TikTok, LinkedIn?
- Connected TV or Display ads visible?
- Any new platform experiments visible? (early mover advantage signals)

**5. Audience Targeting Signals (Inferred)**
- Who appears in their creative? (demographic signals)
- What pain points are addressed? (audience psychographic signals)
- B2B or B2C framing?
- Geographic focus? (pricing/offer localization visible?)

---

## Competitive Intelligence Output Template

### Weekly Competitive Brief

```
WEEK OF: [date]
COMPETITOR: [name]
PLATFORMS ACTIVE: [Meta / Google / LinkedIn / TikTok / etc.]

NEW ADS LAUNCHED THIS WEEK:
- [Ad #1]: Format, hook, offer, CTA
- [Ad #2]: ...

LONGEST-RUNNING ADS (Proof of Performance):
- [Ad]: Running since [date] — [why it likely works]

DOMINANT CREATIVE THEME: [e.g., "founder story" / "before-after" / "social proof montage"]

PRIMARY OFFER THIS WEEK: [e.g., "20% off + free shipping"]

NEW PLATFORM OR FORMAT TEST: [yes/no — describe if yes]

RECOMMENDATIONS FOR OUR CAMPAIGNS:
- Consider testing [angle X] inspired by [competitor]
- Their [format] approach is getting strong engagement → test similar concept
- They've abandoned [format] → we may have white space there
```

---

## Industry Benchmarks (2025 Data)

### Meta Ads Benchmarks (Average by Objective)
| Metric | E-commerce | Lead Gen | App Install |
|---|---|---|---|
| CTR | 1.5–2.5% | 1.0–2.0% | 0.8–1.5% |
| CPM | $8–$15 | $6–$12 | $5–$10 |
| CPC | $0.50–$1.50 | $0.75–$2.00 | $0.80–$2.50 |
| Conversion Rate | 2–5% (landing page) | 5–15% (lead form) | varies |

Note: These vary significantly by vertical, audience temperature, creative quality, and season.

### Google Ads Benchmarks
| Metric | Search | PMax | Display |
|---|---|---|---|
| CTR | 3–6% | N/A | 0.3–0.6% |
| Avg CPC | $1–$4 (varies by industry) | Blended | $0.30–$1.00 |
| Conversion Rate | 3–7% | Varies | 0.5–1% |

---

## Response to Platform Changes — Competitive Intelligence

Track how competitors respond to major platform changes:

**After Andromeda rollout:**
- Are competitors increasing creative volume? (yes = they're adapting)
- Are they switching to broader ad sets? (yes = aware of consolidation need)
- Are they testing new formats aggressively? (yes = creative-first strategy)

**After PMax updates:**
- Are competitors running PMax + Search? (yes = capturing both)
- Are they investing in video for YouTube channel in PMax?
- Do they appear on Demand Gen placements?

**Use this intel to:**
- Identify competitors who are *lagging* in adaptation → opportunity to outpace them
- Identify competitors who are *leading* → what can you learn and test faster?
