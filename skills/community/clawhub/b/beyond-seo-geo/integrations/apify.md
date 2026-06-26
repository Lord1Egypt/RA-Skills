# Apify Integration for Beyond SEO

Apify is the preferred external data layer for Beyond SEO.

The skill must remain useful without Apify, but when `APIFY_API_TOKEN` or Apify MCP access exists, Beyond SEO should use Apify as the primary collection layer for crawling, SERP checks, local SEO checks, trend research, competitor research, PageSpeed/Lighthouse-style checks, GSC/GA4-style connector or export workflows, social/content scans, and authority/backlink checks.

---

## 1. Purpose

Apify gives Beyond SEO a flexible marketplace-style data engine.

Use it for:

```text
Own-site crawling
Competitor crawling
Sitemap-based discovery
Google SERP scraping
People Also Ask / related queries extraction
AI Overview / AI Mode visibility checks where supported
Google Trends analysis
Google Maps/local competitor discovery
Review and ratings extraction where supported
Social profile/content scraping
Authority-style checks using Ahrefs/Semrush/Moz-like community actors
Google Search Console connector/export actors where available
GA4 connector/export actors where available
PageSpeed Insights or Lighthouse actors
Custom Crawlee actors
Scheduled SEO monitoring
Structured datasets for reporting
```

Apify should not replace human SEO judgment. It should provide raw data that Beyond SEO interprets. If Apify can collect the data, use Apify first. If an Apify actor is only scraping a third-party surface or estimating proprietary metrics, label the result as directional unless the actor is backed by authenticated first-party access or a user-provided export.

---

## 2. Required Access

Preferred environment variable:

```text
APIFY_API_TOKEN
```

Alternative access:

```text
Apify MCP server
Apify API client already configured by the host agent
Manual Apify dataset export uploaded by the user
CSV/JSON output from a previous Apify run
Authenticated Apify actor outputs for GSC, GA4, PageSpeed, Ahrefs, Semrush, Moz, or similar providers
```

If no Apify access exists, switch to Native Agent Scraping Mode or File Analysis Mode.

---

## 3. Apify Detection

Before using Apify, check:

```text
Is APIFY_API_TOKEN present?
Can the agent call Apify through MCP?
Can the agent run actors?
Can the agent read Apify datasets?
Can the agent export JSON/CSV?
```

Do not expose token values.

Correct:

```text
APIFY_API_TOKEN detected. I can use Apify Intelligence Mode.
```

Wrong:

```text
Your Apify token is apify_api_...
```

---

## 4. Apify Role in Beyond SEO

Apify should be used as a data collector, not as the strategist.

### Apify collects:

```text
URLs
HTML/text/Markdown
SERP results
AI-search answers where supported
People Also Ask
Related queries
Local business profiles
Reviews/ratings
Trends data
Social content
Public competitor data
Directional authority data
Authenticated first-party exports when an Apify actor connects to GSC, GA4, GBP, or another owned account
PageSpeed/Lighthouse measurements collected through Apify actors
```

### Beyond SEO decides:

```text
Which issues matter
Which pages need to be created
Which keywords are worth targeting
Which competitors are strongest
Which backlinks are safe or risky
Which actions should happen in 30/60/90 days
Which claims are confirmed vs directional
```

---

## 5. Data Quality Rules

Apify has official and community actors. Quality varies by actor.

Use these labels:

```text
Confirmed
Directional
Estimated
Not verified
```

### Use Confirmed When

```text
The actor directly extracted visible public page data.
The crawl output contains the exact title/H1/meta/schema/page text.
The SERP output directly shows the result position for the query/region used.
The output includes raw URLs, snippets, dates, or visible text.
The Apify actor uses authenticated first-party access or an uploaded export for GSC, GA4, GBP, Ahrefs, Semrush, Moz, or similar data.
The Apify actor returns raw PageSpeed/Lighthouse measurements with URL, device, timestamp, and metric fields.
```

### Use Directional When

```text
A community actor estimates DR/DA/traffic/backlinks.
A third-party-style actor scrapes public Ahrefs/Semrush/Moz-like data.
A GSC/GA4/backlink actor does not clearly document whether data is authenticated/export-based or scraped/estimated.
An actor has low rating, few users, or unclear methodology.
The output conflicts with official exports.
```

### Use Not Verified When

```text
No actor was run.
Actor failed.
Actor output is incomplete.
User did not provide official export/access.
The metric requires first-party data such as GSC, GA4, or GBP.
```

---

## 6. Apify Cost Awareness

Beyond SEO must not waste credits.

Use Apify intelligently:

```text
Start small.
Limit crawl depth for discovery.
Use sitemap where possible.
Test 5-10 URLs before full crawl.
Test 5-10 keywords before large SERP run.
Avoid crawling irrelevant assets.
Avoid duplicate competitor runs.
Use raw HTTP crawler when enough.
Use browser/headless mode only when JS rendering is needed.
Export only needed fields when possible.
```

Recommended credit-safe order:

```text
1. Crawl homepage + sitemap.
2. Crawl top money pages only.
3. Run SERP checks for 5-10 priority keywords.
4. Crawl 3-5 strongest competitors.
5. Add Trends/Maps/authority checks only when needed.
6. Expand only after findings justify it.
```

Never run a huge crawl without purpose.

---

## 7. Legal and Ethical Scraping Rules

Only scrape public data that is necessary for the SEO task.

Respect:

```text
robots.txt where applicable
site terms
privacy boundaries
personal data rules
rate limits
copyright boundaries
client confidentiality
```

Do not recommend scraping private user data, login-protected pages, or personal data unless the user has a legitimate right and the task is compliant.

Do not republish scraped content. Use it for analysis, summaries, and strategy.

---

## 8. Primary Apify Use Cases

### 8.1 Own-Site Crawl

Use to extract:

```text
URL
Title
Meta description
H1/H2
Text content
Markdown
Internal links
Canonical
Schema snippets if available
Status/code if actor supports it
Detected language
Content depth
```

Goal:

```text
Build page inventory and find SEO blockers.
```

### 8.2 Competitor Crawl

Use to extract:

```text
Competitor service pages
Page titles
H1/H2 structures
Content depth
FAQs
Schema
Internal links
CTA structure
Trust proof
Pricing/cost sections
Review/testimonial usage
```

Goal:

```text
Find what competitors rank with and what the client site lacks.
```

### 8.3 SERP Checks

Use to extract:

```text
Top organic results
Local pack/map results if supported
Ads
People Also Ask
Related queries
AI Overviews / AI Mode where supported
Result titles/snippets
Ranking URLs
Competitor domains
Search intent patterns
```

Goal:

```text
Understand what Google rewards for the target keyword and region.
```

### 8.4 Trends Research

Use to extract:

```text
Interest over time
Interest by region/city
Rising queries
Top related queries
Related topics
Seasonality
```

Goal:

```text
Prioritize topics by rising demand and regional relevance.
```

### 8.5 Local SEO / Maps

Use to extract:

```text
Competitor business names
Categories
Ratings
Review count
Address/service area
Opening hours
Website link
Phone
Photos if available
Review snippets if available
Map ranking patterns
```

Goal:

```text
Assess Google Business Profile and map-pack competition.
```

### 8.6 Backlink / Authority Directional Checks

Use only when actor exists and quality is acceptable.

Extract:

```text
DR/DA/Authority Score if available
Referring domains
Backlinks
Dofollow/nofollow if available
Organic traffic estimate
Top pages
Anchor data if available
```

Goal:

```text
Estimate authority gap and decide whether official exports are needed.
```

Always label as directional unless verified by official exports.

### 8.7 Social / Brand Authority Checks

Use when relevant.

Extract:

```text
YouTube posts/videos
Instagram content
Facebook pages/posts/reviews
TikTok content
Engagement patterns
Content topics
Brand mentions
Competitor content velocity
```

Goal:

```text
Understand brand demand, topical authority, and content ecosystem.
```

---

## 9. Standard Apify Workflow

When Apify is available:

```text
1. Define audit goal.
2. Select actor category.
3. Choose smallest useful input set.
4. Run actor or ask host agent to run it.
5. Retrieve dataset.
6. Normalize output.
7. Remove duplicates.
8. Label data confidence.
9. Convert data into SEO findings.
10. Prioritize actions.
11. Include missing data list.
```

---

## 10. Recommended Apify Data Normalization

Convert actor outputs into standard Beyond SEO fields.

### Crawl Output Standard

```text
source_actor
run_id
url
final_url
status_code
title
meta_description
h1
h2_list
word_count
text
markdown
canonical
robots_meta
schema_types
internal_links
external_links
images
page_type
seo_issue_flags
```

### SERP Output Standard

```text
source_actor
run_id
query
country
city_or_geo
language
device
date
organic_position
url
domain
title
snippet
serp_feature
paa_questions
related_queries
ai_answer_presence
ai_cited_sources
ads_presence
local_pack_presence
```

### Local Output Standard

```text
source_actor
run_id
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
photos_count
profile_url
```

### Authority Output Standard

```text
source_actor
run_id
domain
metric_name
metric_value
referring_domains
backlinks
organic_keywords
organic_traffic_estimate
top_pages
anchor_examples
confidence_label
```

---

## 11. When Not to Use Apify

Do not use Apify when:

```text
User explicitly says not to use it.
Task can be answered from uploaded verified exports.
The crawl would be too expensive for a small request.
The target website prohibits the intended scraping.
The data requested is private or sensitive.
The actor is low quality and a manual/browser check is better.
```

---

## 12. Apify Failure Handling

If an actor fails:

```text
1. Do not apologize dramatically.
2. Note the failure.
3. Try a smaller input.
4. Try a simpler actor/category.
5. Switch to native scraping or file analysis.
6. Label unavailable data.
```

Example:

```text
The Apify crawl did not return enough body content. I will switch to a smaller crawl and also inspect the live pages manually. If the site is JS-heavy, we may need a headless-browser crawler or SSR check.
```

---

## 13. Best Practices for SEO Agents

Use Apify to build proof, not noise.

Bad:

```text
Crawl 10,000 pages and dump all issues.
```

Good:

```text
Crawl priority pages, classify issue patterns, then recommend fixes by impact.
```

Bad:

```text
Run 500 keywords randomly.
```

Good:

```text
Run 10 seed money keywords, identify SERP patterns, expand only into high-intent clusters.
```

Bad:

```text
Use community Ahrefs actor and present numbers as official.
```

Good:

```text
Use community Ahrefs-style actor as directional and ask for official Ahrefs/Semrush/Moz export for final authority confirmation.
```

---

## 14. Apify Output in Client Reports

In final reports, list Apify under data sources:

```text
Data Sources Used:
- Apify Website Content Crawler for page extraction
- Apify Google SERP scraper for keyword SERP checks
- Apify Google Trends scraper for topic trend validation
- Apify/third-party community actors for directional authority data
```

If community actors were used, add:

```text
Authority metrics from community actors are directional and should be verified with official Ahrefs, Semrush, or Moz exports before final budgeting.
```

---

## 15. Bottom Line

Apify gives Beyond SEO the hands and eyes.

The agent still needs the brain:

```text
Crawl
Compare
Classify
Prioritize
Explain
Plan
Measure
```

Never let raw data become the report. The report is the decision layer.


---

## AI-Friendly SEO Add-On Workflows

When a user asks for AI-friendly SEO, AEO, GEO, Entity SEO, Reputation SEO, or Conversation SEO, use Apify as the main collection layer.

Use Apify to collect:

```text
Website crawl data
Competitor crawl data
SERP/PAA/related-query data
Google Trends demand signals
Google Maps / Places data
Google reviews
Social profile and content data
Third-party mentions
Media/article sources
Backlink/authority signals
PageSpeed/Lighthouse data
AI Overview / AI Mode visibility where supported
GSC/GA4 connector or export actors where available
```

Then map collected data into:

```text
AEO answer block plan
GEO citation/source-worthiness plan
Entity SEO knowledge graph plan
Reputation SEO proof stack plan
Conversation SEO question map
AI-friendly SEO report
30/60/90-day roadmap
```

For detailed instructions, use:

```text
integrations/apify-ai-friendly-seo-workflows.md
aeo-geo/ai-friendly-seo-master-workflow.md
```
