# Native Agent Scraping Workflow

This file defines how Beyond SEO should work when Apify is not available but the AI-agent environment has browser, search, scraping, page-opening, screenshot, or HTML-reading tools.

Many agents already have scraping tools. Beyond SEO should use them before asking for a separate API.

---

## 1. When to Use

Use Native Agent Scraping Mode when:

```text
No APIFY_API_TOKEN is available
No Apify MCP access exists
The agent can still browse/search/open pages
The agent can inspect pages or scrape visible content
The user only gave a URL
The task needs first-pass SEO analysis
```

This mode is still useful. It is not a “weak mode” if used carefully.

---

## 2. Native Tool Examples

Depending on the host environment, native tools may include:

```text
Browser/open URL
Search engine access
HTML extraction
Screenshot analysis
Built-in crawler
Playwright/Puppeteer
Requests + BeautifulSoup
Sitemap fetcher
Robots.txt fetcher
File reader
CSV parser
Schema validator
PageSpeed tool
Custom scraper
MCP browser tools
```

Use whatever exists.

---

## 3. Native Scraping Priorities

Start with high-value checks:

```text
1. Homepage
2. Sitemap.xml
3. Robots.txt
4. Main service/product/course pages
5. Blog/resources page
6. Contact/conversion page
7. Competitor top pages
8. SERP top results for target keywords
9. Local/GBP public profiles where available
10. Backlink/prospect pages if relevant
```

Do not try to crawl the entire internet.

---

## 4. First-Pass Native Website Audit

### Step 1: Open Homepage

Extract:

```text
Title tag
Meta description
H1
Visible hero copy
Main navigation
Primary CTA
Internal links to service pages
Trust proof
Schema if visible/source accessible
```

Ask:

```text
Is the main business/entity clear?
Is the primary offer clear?
Is there a location if local?
Is the page crawlable?
Does the page target the right keyword?
```

### Step 2: Check Sitemap

Try:

```text
/domain.com/sitemap.xml
/domain.com/sitemap_index.xml
/domain.com/wp-sitemap.xml
robots.txt sitemap references
```

Extract:

```text
Total URLs
URL types
Priority routes
Old/irrelevant URLs
Missing service pages
Blog/article coverage
```

### Step 3: Check Robots

Try:

```text
/domain.com/robots.txt
```

Look for:

```text
Blocked important paths
Sitemap reference
Crawl traps
Staging paths
Admin/private paths properly blocked
```

### Step 4: Inspect Money Pages

For each main page:

```text
URL
Title
Meta
H1
H2
Content depth
Intent match
CTA
Trust proof
FAQ
Schema
Internal links
Conversion path
```

### Step 5: Check Blog/Support Content

Look for:

```text
Topical clusters
Internal links to money pages
Author/expert proof
Freshness
Long-tail intent coverage
```

---

## 5. Native SERP Research

When search tools exist, run small targeted SERP checks.

Use:

```text
Primary service + city
Service + near me
Best + service + city
Cost + service + city
Competitor brand terms
Course/product category terms
```

Extract manually:

```text
Top ranking domains
Ranking page type
Directory presence
Local pack presence
PAA questions
Featured snippets
AI answer/AI Overview presence if visible
Ads presence
Repeated competitors
```

Output:

```text
SERP intent
Competitor list
Page types Google rewards
Questions to answer
Content/page gaps
```

---

## 6. Native Competitor Research

Use SERP top results or user-provided competitors.

For each competitor, inspect:

```text
Homepage positioning
Main service pages
Location pages
Blog/resources
FAQ sections
Schema if visible
CTA style
Trust proof
Reviews/testimonials
Internal linking
Content depth
```

Create a competitor gap table:

```text
Competitor
Strong pages
Missing on client site
Content depth
Trust proof
Schema
CTA strength
Backlink/authority data if visible
Action for client
```

---

## 7. Native Backlink/Authority Research

Without Ahrefs/Semrush/Moz/API, do not pretend to know full backlink profile.

Possible checks:

```text
Search brand mentions
Search exact domain mentions
Search competitor "write for us" and directory opportunities
Check public profiles/directories
Check obvious citations
Inspect user-provided backlink URLs
Evaluate paid backlink placement pages
```

Use search queries:

```text
"brand name" -site:clientdomain.com
"clientdomain.com" -site:clientdomain.com
"competitor.com" -site:competitor.com
industry "write for us"
industry "guest post"
city "business directory"
industry association directory city
```

Output:

```text
Backlink opportunities
Brand mention opportunities
Citation gaps
Need official backlink export
```

Required label:

```text
Backlink profile not fully verified without official backlink data or a trusted backlink source.
```

---

## 8. Native Local SEO Checks

Use public information only.

Check:

```text
Business name consistency
Website NAP
Contact page
Footer NAP
Google map embed if present
Location/service pages
Review widgets/testimonials
Schema
Public GBP if search can show it
Competitor map/listing visibility if visible
```

Do not claim actual GBP performance unless data is provided.

Output:

```text
Local visibility gaps
GBP data needed
Review strategy
Local pages needed
Citation cleanup needs
```

---

## 9. Native AEO/GEO Checks

Inspect whether pages answer questions clearly.

Look for:

```text
Definitions
Direct answer blocks
Cost sections
Process/steps
Comparison tables
Risks/limitations
FAQs
Author/expert credentials
Sources/citations
Schema
Entity clarity
```

Search for:

```text
Who is [brand]?
Best [service] in [city]
How much does [service] cost in [city]?
[service] vs [alternative]
How to choose [provider type]
```

Output:

```text
Entity clarity gap
Answer block gaps
Source-worthiness gaps
Schema/entity recommendations
```

---

## 10. Native Technical Checks

Depending on available tools, check:

```text
HTTPS
www/non-www consistency
Redirects
404 pages
Canonical tags
Title/meta
H1/H2
Robots
Sitemap
Index/noindex
Mobile visible issues
Speed observations if PageSpeed available
Schema snippets
Broken navigation links
Thin/empty pages
```

If the tool cannot inspect HTML, say so.

---

## 11. Data Labels in Native Mode

Use:

```text
Observed
Likely
Estimated
Not verified
```

Examples:

```text
Observed: the homepage H1 is missing from visible content.
Likely: the site may have JavaScript-rendering SEO issues because direct HTML shows very little body content.
Not verified: exact rankings and backlinks require GSC/rank/backlink data.
```

---

## 12. Native Mode Output Structure

For a first-pass audit:

```text
Audit Mode: Native Agent Scraping Mode

Available:
- Website URL
- Browser/search/scraping tools

Missing:
- GSC
- GA4
- GBP
- Backlink export
- Apify

Findings:
1. Technical
2. On-page
3. Content
4. Keyword/SERP
5. Competitor
6. Local if relevant
7. Backlinks if relevant
8. AEO/GEO
9. Conversion
10. Next actions
```

---

## 13. When Native Mode Is Enough

Native mode can be enough for:

```text
Proposal preparation
First-pass audit
Page structure review
Content strategy
AEO/GEO recommendations
Service-page planning
Competitor page comparison
Client discovery
```

---

## 14. When Native Mode Is Not Enough

Need stronger data for:

```text
Exact keyword ranking report
Traffic performance
Query-level GSC data
Conversion analysis
GBP calls/directions
Complete backlink audit
Large site technical crawl
Historical trend analysis
```

Ask for:

```text
GSC export
GA4 export
GBP export
Ahrefs/Semrush/Moz export
Apify token
Crawl export
```

---

## 15. Common Mistakes to Avoid

Do not:

```text
Say “I crawled the whole site” if only a few pages were opened.
Say “site has no backlinks” without backlink data.
Say “not ranking” without SERP/GSC/rank data.
Say “technical SEO is fine” without checking source/crawl.
Rely only on homepage.
Ignore sitemap.
Ignore competitors.
Ignore conversion.
```

---

## 16. Bottom Line

Native scraping mode is practical and powerful when used honestly.

It should produce:

```text
A strong first-pass diagnosis
A clear list of verified findings
A clear list of missing data
A practical roadmap
```

Not fake certainty.
