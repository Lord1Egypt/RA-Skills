# Apify AI-Friendly SEO Workflows

This file adds AI-friendly SEO workflows to the Apify-first Beyond SEO system.

Use this whenever a user asks for AI-friendly SEO, AEO, GEO, Entity SEO, Reputation SEO, or Conversation SEO.

---

## 1. Actor Categories to Use

Search Apify Store or use known actors for:

```text
Website content crawl
Custom web scrape
Google SERP
Google Trends
Google Maps / Places
Google reviews
PageSpeed / Lighthouse
Social profile scraping
YouTube scraping
News / article scraping
Backlink / authority checks
AI Overview / AI Mode checks where supported
Perplexity / answer engine checks where supported
GSC / GA4 connector or export actors where available
```

---

## 2. Credit-Safe AI-Friendly SEO Sequence

```text
1. Crawl own website: homepage + sitemap, max 50 pages.
2. Extract entity data from own site.
3. Run 5-10 SERP queries around money keywords.
4. Extract People Also Ask and related questions.
5. Crawl 3-5 competitors.
6. Check Google Maps/reviews if local.
7. Check social/reputation profiles.
8. Check PageSpeed/Lighthouse on homepage + money pages.
9. Check authority/backlink actors after page strategy is known.
10. Check AI Overview / answer engine visibility where supported.
```

---

## 3. Data to Extract

### AEO

```text
Questions
PAA
Related searches
FAQ sections
Answer snippets
Content gaps
```

### GEO

```text
Cited sources
Mentioned brands
Competitor cited pages
Authority pages
Media mentions
Balanced comparison content
```

### Entity SEO

```text
Brand name
Person name
Alternate names
Profiles
sameAs links
Reviews
Media
Certifications
Schema
```

### Reputation SEO

```text
Review platforms
Review count/rating
Review themes
Trustpilot/Google/LinkedIn proof
Media articles
Third-party authority pages
```

### Conversation SEO

```text
Human questions
Objections
Cost concerns
Trust concerns
Comparison questions
Action questions
```

---

## 4. Output

Apify findings should feed into:

```text
AI-friendly SEO report
Page creation plan
Answer block plan
Entity page plan
Reputation proof plan
Third-party authority article plan
Schema plan
90-day roadmap
```

---

## 5. Confidence Labels

```text
Confirmed: crawl/SERP/review data directly extracted.
Directional: community authority/backlink/AI visibility estimates.
Not verified: actor unavailable or data not collected.
```

## Research Anchors

Use these public guidance anchors when explaining or auditing AI-friendly SEO:

- Google Search Central: AI features and your website — https://developers.google.com/search/docs/appearance/ai-features
- Google Search Central: Google Search generative AI optimization guide — https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Google Search Central: Creating helpful, reliable, people-first content — https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google Search Central: Organization structured data — https://developers.google.com/search/docs/appearance/structured-data/organization
- Google Search Central: ProfilePage structured data — https://developers.google.com/search/docs/appearance/structured-data/profile-page
- Google Search Central: Review snippet structured data — https://developers.google.com/search/docs/appearance/structured-data/review-snippet
- Bing Webmaster Tools: AI Performance — https://www.bing.com/webmasters/help/ai-performance-9f8e7d6c
- Bing Webmaster Blog: AI Performance announcement — https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview
- Perplexity Hub — https://www.perplexity.ai/hub
