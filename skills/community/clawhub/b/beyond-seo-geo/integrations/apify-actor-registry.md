# Apify Actor Registry for Beyond SEO

This file defines which categories of Apify actors Beyond SEO should look for and how to use them.

Actor availability, pricing, and quality can change. Therefore, this registry uses categories and preferred examples rather than treating any single actor as permanent truth.

---

## 1. Registry Philosophy

Do not hardcode one actor forever.

For each SEO job, the agent should:

```text
1. Identify needed data.
2. Choose the best actor category.
3. Prefer official/maintained actors when available.
4. Check actor rating, users, last modified date, pricing, and output examples.
5. Use community actors carefully.
6. Label low-confidence outputs as directional.
```

---

## 2. Actor Quality Checklist

Before using an actor, check:

```text
Actor name
Actor ID
Developer/maintainer
Rating
Number of users
Last modified date
Pricing model
Input schema clarity
Output schema clarity
Reviews/issues
Whether it supports API/MCP
Whether it exports JSON/CSV/Excel
Whether it has enough fields for SEO use
```

### Actor Confidence Levels

```text
High: maintained by Apify or reputable developer, strong usage, clear output, recent updates.
Medium: community actor with decent rating/usage and clear output.
Low: few users, unclear output, no recent updates, poor reviews, or unverifiable claims.
```

---

## 3. Primary Actor Categories

### 3.1 Website Crawling

Purpose:

```text
Own-site crawl
Competitor crawl
Content extraction
Page inventory
AEO/GEO content extraction
RAG/LLM-ready Markdown output
```

Preferred actor examples:

```text
apify/website-content-crawler
apify/web-scraper
custom Crawlee actor
```

Use for:

```text
URL discovery
Markdown/text extraction
HTML cleanup
JS-rendered page crawling
Sitemap crawling
File download if needed
Competitor page analysis
```

Standard output fields needed:

```text
url
title
description/meta
h1
h2_list
text/markdown
links
canonical
schema snippets if available
files
```

Caution:

```text
Website Content Crawler is excellent for content extraction, but may not provide every technical SEO field by default. For technical audits, combine with raw HTML extraction, custom Web Scraper logic, or native tools.
```

---

### 3.2 SERP Scraping

Purpose:

```text
Keyword ranking checks
Competitor discovery
SERP intent analysis
People Also Ask extraction
Related queries
AI Overview / AI Mode visibility where supported
Ads and SERP feature checks
```

Preferred actor examples:

```text
apify/google-search-scraper
other high-quality Google SERP scraper actors
Bing SERP actors where needed
```

Use for:

```text
Top 10/20/30 organic results
Local keyword checks
Country/language/device SERPs
PAA questions
Related searches
AI-search visibility checks where actor supports it
```

Standard output fields needed:

```text
query
country
language
location/city
device
rank
url
domain
title
snippet
serp_feature
paa_questions
related_queries
ai_overview_presence
ai_cited_sources
ads
```

Caution:

```text
SERP results vary by location, device, personalization, and time. Always record query, country, city/geolocation, language, device, and date.
```

---

### 3.3 Google Trends / Topic Demand

Purpose:

```text
Validate topic demand
Find rising queries
Compare keyword interest
Identify seasonality
Find regional interest
Support content calendar planning
```

Preferred actor examples:

```text
apify/google-trends-scraper
high-quality Google Trends community actors
```

Use for:

```text
Interest over time
Interest by country/city/subregion
Rising queries
Top related queries
Related topics
Topic comparison
```

Standard output fields needed:

```text
keyword/topic
time_range
region
interest_over_time
interest_by_region
rising_queries
top_queries
related_topics
```

Caution:

```text
Google Trends is relative interest, not exact search volume. Do not present it as keyword volume.
```

---

### 3.4 Google Maps / Local SEO

Purpose:

```text
Local competitor discovery
Map pack competitor analysis
Google Business Profile comparison
Review/rating analysis
Local category comparison
Service area discovery
```

Actor examples to look for:

```text
Google Maps Scraper actors
Google Places Scraper actors
Google Reviews Scraper actors
Competitive intelligence actors using Google Maps data
```

Use for:

```text
Business names
Categories
Ratings
Review counts
Address
Phone
Website
Hours
Services
Photos
Review text snippets
Map position where available
```

Standard output fields needed:

```text
query
city
business_name
category
rating
review_count
address
phone
website
hours
map_position
review_snippets
profile_url
```

Caution:

```text
Do not scrape or store unnecessary personal data. For SEO, business-level data and review themes are usually enough.
```

---

### 3.5 Authority / Backlink / SEO Metrics

Purpose:

```text
Directional domain authority checks
Backlink profile review
Competitor authority gap
Traffic estimate
Organic keyword footprint estimate
```

Actor categories to look for:

```text
Ahrefs-style scraper
Semrush-style scraper
Moz DA checker
Similarweb-style traffic checker
Ubersuggest-style scraper
Domain authority checker
Backlink checker
```

Use for:

```text
DR/DA/Authority Score
Referring domains
Backlinks
Dofollow/nofollow ratio
Top pages
Organic keywords
Organic traffic estimate
Anchors
Competitor comparison
```

Critical caution:

```text
Most Ahrefs/Semrush/Moz-style Apify actors are community-maintained or scrape public/limited data. Treat as directional unless the user provides an official export or authenticated official source.
```

Never write:

```text
Ahrefs confirms...
```

unless it truly came from Ahrefs export/access.

Write:

```text
Directional authority check suggests...
```

---

### 3.6 Social and Brand Authority

Purpose:

```text
Competitor content analysis
Brand demand signals
Social proof scan
Topic/format discovery
Content velocity comparison
```

Actor categories to look for:

```text
Instagram scraper
Facebook pages/posts scraper
Facebook reviews scraper
YouTube scraper
TikTok scraper
LinkedIn public data actors where allowed
Reddit scraper where relevant
```

Use for:

```text
Post topics
Engagement
Content frequency
Follower count
Video topics
Review themes
Competitor campaigns
Brand mentions
```

Caution:

```text
Social scraping must respect platform rules and privacy. Use public business/content data only.
```

---

### 3.7 Lead / Contact Enrichment

Purpose:

```text
SEO outreach prospecting
Local citation prospecting
Partnership link building
Digital PR prospecting
```

Actor categories to look for:

```text
Business leads enrichment
Google Maps lead extraction
Company website contact extraction
Social profile enrichment
```

Use for:

```text
Prospect name
Business URL
Email if legally and ethically appropriate
Phone
Category
Location
Website
Social profile
```

Caution:

```text
Follow email/privacy laws. Do not scrape personal data unnecessarily. Do not spam.
```

---

## 4. Preferred SEO Actor Stack

For most Beyond SEO audits, use this order:

```text
1. Website crawler
2. Google SERP scraper
3. Google Trends scraper
4. Google Maps/local actor if local business
5. Authority/backlink actor if needed
6. Social/content actor if brand/content strategy matters
```

---

## 5. Actor Selection by Task

### Website Technical + Content Audit

Use:

```text
Website Content Crawler
Web Scraper
Custom Crawlee actor
Native browser/source inspection
```

### Keyword Ranking Snapshot

Use:

```text
Google Search Results Scraper
GSC export if available
Rank tracking export if available
```

### Competitor Discovery

Use:

```text
Google SERP scraper
Google Maps scraper for local
Competitive Intelligence actors
Native search
```

### AEO/GEO Visibility

Use:

```text
Google Search scraper with AI Overview/AI Mode fields where supported
AI-search add-ons where available
Perplexity/ChatGPT/Copilot/Gemini search actors where available
Native AI-search testing if available
```

### Local SEO

Use:

```text
Google Maps scraper
Google Reviews scraper
Competitive intelligence actor using maps data
GBP export if available
```

### Backlink/Authority

Use:

```text
Ahrefs-style actor
Semrush-style actor
Moz DA actor
Similarweb-style actor
Official exports when available
```

### Content Calendar / Trends

Use:

```text
Google Trends scraper
SERP scraper
Social scrapers
Competitor blogs crawl
```

### Free/Paid Backlink Prospecting

Use:

```text
SERP scraper with queries like "write for us" + niche
Google Maps for local associations/business directories
Web scraper for prospect pages
Authority-style actor for prospect evaluation
```

---

## 6. Actor Discovery Queries

When the host agent can search Apify Store, use queries like:

```text
website crawler
website content crawler
google search scraper
serp scraper
google trends scraper
google maps scraper
google reviews scraper
ahrefs scraper
semrush scraper
moz domain authority
similarweb scraper
backlink checker
instagram scraper
facebook pages scraper
youtube scraper
tiktok scraper
competitive intelligence agent
```

---

## 7. Actor Approval Rules

Approve actor use if:

```text
The actor directly supports the task.
Output fields match the needed SEO fields.
Cost is reasonable for the task.
It has acceptable reliability.
The task is compliant and public-data based.
```

Reject or avoid actor if:

```text
It promises unrealistic data.
It has unclear output.
It is too expensive for the current question.
It has poor reviews/issues.
It collects unnecessary personal data.
It requires credentials the user does not have.
It violates task boundaries.
```

---

## 8. Actor Result Documentation

Every Apify-based report should include:

```text
Actor/category used
Purpose
Input scope
Date/time if available
Confidence label
Limitations
```

Example:

```text
Data Source: Google SERP scraper
Purpose: Local keyword SERP analysis
Input: 12 keywords, country US, location Arlington Heights, desktop
Confidence: Confirmed for sampled SERPs, not a full rank-tracking history
```

---

## 9. Actor Output to SEO Action Mapping

### If SERP shows competitors dominate with service pages

Action:

```text
Create or improve dedicated service landing pages.
```

### If PAA questions repeat cost/risk/process intent

Action:

```text
Add answer blocks, FAQs, cost sections, risk/process sections.
```

### If Trends shows rising query

Action:

```text
Prioritize content/page creation earlier in roadmap.
```

### If Maps shows competitors have more reviews

Action:

```text
Build review velocity and GBP content strategy.
```

### If authority actors show low referring domains

Action:

```text
Build niche/local/PR backlink plan, verify with official export if budget depends on it.
```

### If social scrapers show competitor content themes

Action:

```text
Create SEO-supporting content cluster and social proof loop.
```

---

## 10. Registry Maintenance

Because actors change, this registry should be reviewed regularly.

Update when:

```text
A better official actor appears.
Actor pricing changes significantly.
Actor output schema changes.
An actor becomes unreliable.
A new AI-search/AEO actor becomes available.
A better local SEO/maps actor appears.
```

---

## 11. Bottom Line

The registry exists to prevent tool chaos.

Beyond SEO should not ask, “Which random actor should I run?”

It should ask:

```text
What SEO question am I answering?
What data do I need?
Which actor category provides it?
How reliable is that actor?
How should I label the output?
What action does the data support?
```
