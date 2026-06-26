# Fallback Without APIs

This file defines how Beyond SEO should work when Apify, DataForSEO, Ahrefs API, Semrush API, Moz API, Firecrawl, and other paid APIs are unavailable.

The skill must not become useless without APIs.

---

## 1. Core Principle

No API does not mean no SEO work.

It means:

```text
Use native browser/search/scraping if available.
Use uploaded files if available.
Use manual audit frameworks if no live tools exist.
Label anything unverified.
Ask for exports only when necessary.
```

---

## 2. Fallback Levels

### Level 1: Native Tools Available

Use:

```text
Browser
Search
Page scraping
HTML inspection
Sitemap/robots fetch
Screenshots
Manual competitor review
```

Mode:

```text
Native Agent Scraping Mode
```

### Level 2: Files Available

Use:

```text
GSC export
GA4 export
Crawl export
SEO PDF
Backlink sheet
Ahrefs/Semrush/Moz screenshots
Keyword CSV
Competitor report
```

Mode:

```text
File Analysis Mode
```

### Level 3: No Tools, No Files

Use:

```text
Advisory Mode
```

Output:

```text
Manual audit checklist
Data request list
Strategy template
Client intake questions
Implementation plan skeleton
```

---

## 3. What Can Still Be Done Without APIs

### With Website URL + Browser

```text
Homepage SEO review
Main service/page review
Navigation/internal linking review
Visible content depth check
Title/meta/H1 if accessible
Sitemap/robots check
Competitor discovery via search
Manual SERP intent review
Local visibility observations
AEO/GEO content readiness
Conversion path review
```

### With Uploaded GSC Export

```text
Actual queries
Clicks
Impressions
CTR
Average position
Pages with opportunity
Queries near top 3/top 10
CTR improvement opportunities
Content refresh priorities
Cannibalization hints
```

### With Uploaded GA4 Export

```text
Organic landing pages
Engagement
Conversion paths
Traffic channels
Assisted conversion hints
Pages with traffic but no conversion
```

### With Uploaded Crawl Export

```text
Technical SEO issues
Titles/meta
H1/H2
Status codes
Canonicals
Indexability
Word count
Internal links
Broken links
Redirects
Schema if included
```

### With Uploaded Backlink Export

```text
Referring domains
Anchor text
Dofollow/nofollow
Link relevance
Spam risk
Competitor link gap if included
Link cleanup priorities
```

---

## 4. What Cannot Be Confirmed Without APIs or Exports

Do not confirm:

```text
Exact search volume
Full keyword universe
Full ranking history
Full backlink profile
Complete technical crawl of large site
Actual GSC performance
Actual GA4 conversions
Actual GBP calls/directions
Complete local map rank tracking
AI Overview citation history
```

Use:

```text
Not verified from available data.
Recommended check:
```

---

## 5. Manual Research Methods

### Manual SERP Check

Use search queries:

```text
primary service + city
service + near me
best service + city
service cost + city
service provider + city
competitor service pages
```

Record:

```text
Top 10 domains
Ranking page type
SERP features
PAA questions
Local pack presence
Ads
Directories
Repeated competitors
```

### Manual Competitor Check

Open competitor pages and record:

```text
Title
H1
Sections
Content depth
FAQs
CTA
Reviews/trust proof
Location proof
Schema if visible
Internal links
```

### Manual Backlink Prospecting

Search:

```text
industry "write for us"
industry "guest post"
industry "submit article"
city "business directory"
city "chamber of commerce"
industry association directory
competitor brand mentions
```

Evaluate:

```text
Relevance
Indexability
Organic footprint if visible
Outbound link quality
Paid/free status
Risk
```

---

## 6. File-Based Audit Procedure

When uploaded files are available:

```text
1. Identify file type.
2. Extract metrics and findings.
3. Check date/freshness.
4. Separate facts from recommendations.
5. Consolidate issues.
6. Remove duplicate findings.
7. Prioritize by impact.
8. Build action plan.
9. List missing live checks.
```

Example:

```text
Confirmed from file: The report shows 36 ranking keywords.
Not verified live: Current rankings may have changed since report date.
Action: Use the keyword footprint as baseline, then verify with fresh SERP/GSC data.
```

---

## 7. Advisory Mode Output

When no data exists, output:

```text
1. What data is needed
2. How to collect it
3. What to check manually
4. What the SEO strategy should include
5. What templates to use
6. What not to claim yet
```

Advisory output is not an audit. Say that clearly.

---

## 8. Data Request List

If deeper audit is needed, ask for:

```text
Website URL
Target city/country
Main services/products/courses
Top competitors
GSC export last 3-6 months
GA4 landing page + conversion export
GBP insights export/screenshots
Ahrefs/Semrush/Moz export
Screaming Frog/Sitebulb crawl export
Backlink prospect sheet
Apify token if available
```

Do not ask for everything if the task is small.

---

## 9. Fallback Report Language

Use honest phrasing.

Good:

```text
Based on the visible pages and provided files, the main likely issue is shallow service-page depth. Exact rankings and backlinks were not verified because GSC and backlink exports were not provided.
```

Bad:

```text
Your rankings are low because backlinks are bad.
```

unless verified.

Good:

```text
The current report suggests authority is low. Verify with Ahrefs/Semrush/Moz before buying backlinks.
```

Bad:

```text
Buy 100 backlinks.
```

---

## 10. No-API SEO Plan Template

When user wants a plan without tools, structure it:

```text
Goal
Assumptions
Data needed
Manual checks
Technical SEO checklist
Keyword/page architecture
Competitor research method
Content plan
Local SEO plan
Backlink plan
AEO/GEO plan
Conversion plan
30/60/90-day roadmap
KPIs
Risks
```

---

## 11. Fallback for Backlinks

Without backlink APIs:

```text
Do not claim full profile.
Evaluate provided backlink URLs.
Use public search for brand mentions.
Use competitor visible links where discoverable.
Build safe prospect categories.
Ask for Ahrefs/Semrush/Moz export for full profile.
```

Safe categories:

```text
Local directories
Industry associations
Partner/vendor pages
Guest articles on relevant sites
Digital PR
Founder/expert interviews
Resource pages
Free publishing platforms used carefully
```

Unsafe categories:

```text
Bulk link packages
PBNs
Irrelevant high-DA sites
Exact-match anchor abuse
Sites with obvious paid-link farms
```

---

## 12. Fallback for AEO/GEO

Without AI-search scraping:

```text
Audit content structure.
Check entity clarity.
Check answer blocks.
Check schema.
Check expert proof.
Check direct question coverage.
Check citations/sources.
Recommend pages and sections likely to improve AI answer eligibility.
```

Do not claim:

```text
ChatGPT cites your site
Google AI Overview uses your page
```

unless checked.

---

## 13. Fallback for Local SEO

Without GBP access:

```text
Audit website NAP.
Check location/service pages.
Check visible reviews/testimonials.
Check public listings if available.
Recommend GBP audit.
Recommend review strategy.
Recommend citation cleanup.
```

Do not claim:

```text
GBP calls are low
Directions are down
Map rankings are X
```

unless provided.

---

## 14. Fallback for Technical SEO

Without a full crawl:

```text
Check sample pages.
Check sitemap.
Check robots.
Check source if available.
Check visible metadata.
Look for pattern issues.
Recommend full crawl for confirmation.
```

Use language:

```text
Sampled pages show...
Likely pattern...
Needs full crawl verification...
```

---

## 15. Bottom Line

Beyond SEO should never say:

```text
I cannot help because there is no API.
```

It should say:

```text
I can produce a first-pass or strategic audit with current access. For confirmed rankings, backlinks, traffic, and conversion data, we need GSC/GA4/GBP/backlink exports or an Apify/API data layer.
```

No excuses. No fake certainty. Just useful work.
