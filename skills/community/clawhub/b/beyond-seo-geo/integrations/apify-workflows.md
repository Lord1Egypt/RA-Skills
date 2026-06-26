# Apify Workflows for Beyond SEO

This file defines practical Apify workflows for SEO, AEO/GEO, local SEO, competitor research, backlinks, and reporting.

The goal is not to run actors blindly. The goal is to collect exactly the data needed to make better SEO decisions.

---

## 1. Workflow Rules

Before running Apify:

```text
1. Define the business goal.
2. Define the SEO question.
3. Choose the smallest useful data pull.
4. Select actor/category.
5. Run test input first.
6. Inspect output quality.
7. Expand only if useful.
8. Normalize results.
9. Convert findings into actions.
```

Bad:

```text
Run every actor and see what happens.
```

Good:

```text
Run a 20-page crawl and 10-keyword SERP sample to identify page and competitor patterns.
```

---

## 2. Workflow A: First-Pass Website Crawl

### Use When

```text
User provides a website URL.
Need technical/content/on-page overview.
No crawl export exists.
Apify token is available.
```

### Actor Category

```text
Website crawler
Website content crawler
Web scraper
Custom Crawlee actor
```

### Input

```text
start_url: website homepage
include_sitemap: true if supported
max_pages: 50-200 for first pass
same_domain_only: true
exclude_patterns:
  - /wp-admin/
  - /cart/
  - /checkout/
  - /login/
  - /account/
  - ?replytocom=
  - tracking/query parameters
render_js: true only if needed
```

### Extract

```text
URL
status/final URL if available
title
meta description
H1
H2s
body text/Markdown
word count
links
canonical
schema snippets if available
page type
```

### Analyze

```text
Missing/duplicate titles
Missing/duplicate meta descriptions
Missing/multiple H1s
Thin pages
Empty JS-rendered pages
Orphan-like pages
Weak CTAs
Missing schema
Weak internal links
Service pages vs blog/support pages
```

### Output

```text
Page inventory
Issue summary
Priority technical/content fixes
Pages to improve first
Need for deeper crawl if required
```

---

## 3. Workflow B: JavaScript Rendering Check

### Use When

```text
Site appears modern React/Next/Lovable/SPA.
Crawl output has little body text.
Important pages show empty HTML or missing H1/H2.
```

### Actor Category

```text
Website crawler with headless browser
Web scraper with JS rendering
Native browser/source inspection
```

### Test

Compare:

```text
Raw HTML content
Rendered page content
Crawl-extracted Markdown/text
Visible browser content
```

### Red Flags

```text
No server-rendered H1/H2
Meta tags missing in source
Content only appears after JS
Course/product/service pages not crawlable
Canonical missing on dynamic routes
Duplicate title/meta across routes
```

### Output

```text
Rendering risk:
Critical / High / Medium / Low

Required fix:
SSR / pre-rendering / dynamic metadata / schema injection / static landing pages
```

---

## 4. Workflow C: SERP and Keyword Sample

### Use When

```text
Need keyword opportunities.
Need competitor discovery.
Need ranking snapshot.
Need SERP intent analysis.
```

### Actor Category

```text
Google SERP scraper
```

### Input

```text
queries:
  - 5 existing money keywords
  - 5 missing money keywords
  - 5 competitor-owned keywords
country
city/location/geocode if local
language
device: desktop/mobile if supported
max_pages_per_query: 1-3
```

### Extract

```text
Organic top 10/20/30
Titles
URLs
Domains
Snippets
PAA questions
Related queries
Ads
Local pack presence
AI Overview/AI Mode presence if available
```

### Analyze

```text
Who ranks repeatedly?
What page types rank?
Are directories dominating?
Are competitors using dedicated service pages?
Are pages local pages, category pages, blogs, homepages, or GBP-heavy results?
Are PAA questions cost/risk/process/comparison focused?
Are AI answers citing competitor or authority sources?
```

### Output

```text
Keyword-to-page map
Competitor list
SERP intent summary
PAA/AEO questions
Page creation/improvement priorities
```

---

## 5. Workflow D: Competitor Crawl

### Use When

```text
SERPs reveal top competitors.
User provides competitors.
Need content/service-page gap.
```

### Actor Category

```text
Website crawler
Website content crawler
Web scraper
```

### Input

```text
competitor_domains: 3-10
max_pages_per_domain: 50-150
include_sitemap: true
focus_patterns:
  - /services/
  - /service/
  - /treatments/
  - /courses/
  - /blog/
  - /resources/
  - location/city pages
```

### Extract

```text
Top service/product/course pages
Title/H1/H2
Content depth
FAQ sections
Schema
CTA patterns
Trust proof
Internal links
Blog/support clusters
Location pages
```

### Analyze

```text
Pages competitors have that client lacks
Service pages with stronger depth
Keyword clusters competitors cover
FAQ/PAA coverage
Schema usage
Conversion paths
Internal linking patterns
Local proof
Content freshness
```

### Output

```text
Competitor matrix
Missing page list
Service-page gap
Content gap
Internal linking recommendations
90-day build priority
```

---

## 6. Workflow E: Local SEO / Maps Scan

### Use When

```text
Business serves a local city/region.
User wants calls, appointments, map pack, or local queries.
```

### Actor Category

```text
Google Maps scraper
Google Places scraper
Google Reviews scraper
Competitive intelligence actor with Maps data
```

### Input

```text
queries:
  - main service + city
  - near me intent if useful
  - emergency/service-specific terms
location/city
radius if supported
max_results: 10-30 per query
```

### Extract

```text
Business name
Category
Rating
Review count
Address
Phone
Website
Hours
Services
Profile URL
Review snippets/themes if available
Map position if supported
```

### Analyze

```text
Who dominates map results?
What categories are competitors using?
How many reviews do winners have?
What review keywords appear?
Is client category/service coverage weak?
Does client need review velocity?
Does client need local landing pages?
Does client need citation cleanup?
```

### Output

```text
Map competitor summary
GBP optimization checklist
Review strategy
Local page plan
Citation/local backlink plan
```

---

## 7. Workflow F: Trends and Content Demand

### Use When

```text
Need content calendar.
Need topic prioritization.
Need seasonal/regional demand check.
Need to compare multiple service/course topics.
```

### Actor Category

```text
Google Trends scraper
```

### Input

```text
terms:
  - target service/course/product keywords
region
time_range: 12 months / 5 years / 90 days
category if relevant
```

### Extract

```text
Interest over time
Interest by region/city
Rising queries
Top queries
Related topics
```

### Analyze

```text
Which topic has rising demand?
Which city/region shows strongest demand?
Is this seasonal?
Which related queries should become support articles?
Which topics are low-volume but high-conversion?
```

### Output

```text
Topic priority
Content calendar input
Regional targeting
Support article ideas
Warnings where Trends is not enough
```

Important:

```text
Trends is relative interest, not exact keyword volume.
```

---

## 8. Workflow G: Authority / Backlink Directional Scan

### Use When

```text
Need backlink gap.
Need authority comparison.
User does not have official Ahrefs/Semrush/Moz export.
Apify community actor exists.
```

### Actor Category

```text
Ahrefs-style scraper
Semrush-style scraper
Moz DA checker
Similarweb-style checker
Backlink checker
```

### Input

```text
client_domain
competitor_domains: 3-10
```

### Extract

```text
Authority score/DR/DA if available
Referring domains
Backlinks
Organic keywords
Traffic estimate
Top pages
Anchor examples if available
```

### Analyze

```text
Authority gap
Competitor link advantage
Whether site needs local/niche links
Whether current authority is enough for target keywords
Whether paid backlink options need evaluation
```

### Output

```text
Directional authority comparison
Backlink priority
Need official export?
Safe link categories
Risk notes
```

Required disclaimer:

```text
This authority scan is directional unless verified with official Ahrefs/Semrush/Moz exports.
```

---

## 9. Workflow H: AEO/GEO Visibility Check

### Use When

```text
User wants AI search visibility.
SERP actor supports AI Overview/AI Mode or AI search add-ons.
Task involves AEO/GEO.
```

### Actor Category

```text
Google SERP scraper with AI Overview/AI Mode
AI-search actors/add-ons where available
Perplexity/ChatGPT/Copilot/Gemini search actors where available
Native AI-search testing if available
```

### Input

```text
Brand/entity questions
Service-intent questions
Comparison questions
Best/top provider questions
Cost/process questions
Problem-solution questions
```

Examples:

```text
best AI automation course in Pakistan
who offers AI agents course in Pakistan
best dental implants dentist in Arlington Heights
how much do dental implants cost in Arlington Heights
```

### Extract

```text
AI answer presence
Cited sources
Mentioned brands
Mentioned competitors
Narrative gaps
Questions generated/fan-out if available
```

### Analyze

```text
Does the brand appear?
Are competitors cited?
Which sources are cited?
What content format is being cited?
What entity information is missing?
What pages need answer blocks?
What proof/citations/schema are missing?
```

### Output

```text
AI-search visibility status
Mention/citation gap
Source-worthiness plan
AEO/GEO content blocks
Entity/schema recommendations
```

---

## 10. Workflow I: Free Backlink Prospecting

### Use When

```text
User wants free backlink posting ideas.
User has a backlink sheet/list.
Need entity-building support articles.
Need safe support backlinks.
```

### Actor Category

```text
SERP scraper
Website crawler
Manual/native scraping
Authority actor for prospect quality if needed
```

### Prospect Query Examples

```text
site:medium.com "write for us" niche
niche "guest post"
niche "submit article"
niche "contribute"
niche "community"
niche "forum"
niche "directory"
city business directory
industry association directory
```

### Analyze Prospects

```text
Indexability
Relevance
Traffic estimate if available
Outbound link behavior
Spam risk
Niche fit
Free/paid status
Anchor policy
Editorial quality
```

### Output

```text
Prospect URL
Type
Free/Paid
Relevance
Risk
Suggested article topic
Suggested anchor
Suggested target page
Priority
```

---

## 11. Workflow J: Paid Backlink Evaluation

### Use When

```text
User has a paid backlink offer.
Need decide buy/avoid/negotiate.
```

### Actor Category

```text
Website crawler
SERP scraper
Authority actor
Similarweb-style actor
Native browser inspection
```

### Input

```text
placement_domain
placement_page if known
price
target_page
proposed_anchor
niche
country
```

### Extract

```text
Indexation
Organic keywords estimate
Traffic estimate
Authority estimate
Outbound links
Recent posts
Niche relevance
Country relevance
Link selling pattern
Content quality
```

### Output Verdict

```text
Buy
Avoid
Negotiate
Use only branded anchor
Use nofollow/sponsored
Need more data
```

### Required Reasoning

```text
Relevance
Traffic
Authority
Spam risk
Anchor risk
Price fairness
Best target page
Best anchor
```

---

## 12. Workflow K: Scheduled Monitoring

### Use When

```text
Client has ongoing SEO campaign.
Need weekly/monthly tracking.
Apify schedules/webhooks are available.
```

### Monitoring Jobs

```text
Weekly SERP sample for priority keywords
Weekly competitor page change crawl
Monthly own-site crawl
Monthly backlink/authority directional scan
Weekly Google Trends/rising query scan
Monthly local/maps competitor review count scan
Monthly AEO/GEO visibility check
```

### Output

```text
Change summary
New issues
Ranking movement
Competitor movement
New content opportunities
Backlink opportunities
Local review movement
Next actions
```

---

## 13. Apify Workflow Output Standard

Every Apify workflow should produce:

```text
Workflow name
Actor/category used
Input scope
Date
Records collected
Confidence label
Key findings
Recommended actions
Missing data
Next run suggestion
```

Example:

```text
Workflow: SERP and Keyword Sample
Actor: Google SERP scraper
Input: 12 local service keywords, US, Arlington Heights, desktop
Records: 120 organic results + PAA data
Confidence: Confirmed for sampled SERPs
Finding: Competitors rank using dedicated service pages; client relies too heavily on homepage.
Action: Build service pages for family dentist, emergency dentist, Invisalign, cosmetic, veneers.
```

---

## 14. Mistakes to Avoid

Do not:

```text
Run large crawls without scope.
Treat scraped keyword appearances as rankings.
Treat Trends as search volume.
Treat community authority actors as official Ahrefs data.
Ignore failed or partial runs.
Give raw Apify output as the final report.
Forget to normalize fields.
Forget to label confidence.
```

---

## 15. Bottom Line

Apify workflows should help Beyond SEO move from opinion to evidence.

But the final deliverable must still be:

```text
What is wrong
Why it matters
What to fix first
What to build next
What to measure
What data is missing
```
