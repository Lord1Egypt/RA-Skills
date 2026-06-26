# Apify-First Capability Detection Override

Before using any other data/API path, check Apify first.

## Default Detection Order

```text
1. APIFY_API_TOKEN or Apify MCP
2. Apify actor shortlist
3. Website URL
4. Target country/city
5. Main goal
6. Apify datasets/exports already available
7. Native browser/search only if Apify is missing or unsuitable
8. Uploaded files only if provided or needed
```

## API Asking Rule

Do not ask for many APIs. Ask for `APIFY_API_TOKEN` only.

If GSC, GA4, PageSpeed, Ahrefs, Semrush, Moz, or backlink data is needed, first search/use Apify actor categories or Apify-hosted export workflows.

## Mode Selection

```text
IF APIFY_API_TOKEN or Apify MCP exists:
    Use Apify Intelligence Mode

ELSE IF native browser/search/scraping exists:
    Use Native Agent Scraping Mode and ask once for APIFY_API_TOKEN to upgrade

ELSE IF uploaded files exist:
    Use File Analysis Mode and ask once for APIFY_API_TOKEN to upgrade

ELSE:
    Use Advisory Mode and ask once for APIFY_API_TOKEN
```


---

# Capability Detection

Before any SEO task, Beyond SEO must detect available capabilities and choose the correct audit mode.

This prevents fake audits and helps the agent work properly across Codex, Claude, OpenClaw, Cursor, custom agents, and no-tool environments.

---

## 1. Detection Goal

The agent must answer:

```text
What can I actually access right now?
What can I verify?
What must be estimated?
What must be requested from the user?
Which audit mode should I use?
```

---

## 2. Detection Order

Check in this order:

```text
1. User-provided website URL
2. User-provided competitors
3. User-provided target location/market
4. Uploaded files or exports
5. Native browser/search access
6. Native scraping/crawling access
7. Apify API token or Apify MCP access
8. PageSpeed API access
9. GSC/GA4 exports or access
10. Ahrefs/Semrush/Moz exports or screenshots
11. Google Business Profile data
12. Ability to run scripts/tools
```

---

## 3. Environment Variable Checks

If the agent can inspect environment variables, check:

```text
APIFY_API_TOKEN
PAGESPEED_API_KEY
GSC_EXPORT_PATH
GA4_EXPORT_PATH
AHREFS_EXPORT_PATH
SEMRUSH_EXPORT_PATH
MOZ_EXPORT_PATH
SCREAMING_FROG_EXPORT_PATH
SITEBULB_EXPORT_PATH
CUSTOM_SCRAPER_API_KEY
CUSTOM_SCRAPER_BASE_URL
```

Do not reveal secret values. Only state whether they are present.

Correct:

```text
APIFY_API_TOKEN detected.
```

Wrong:

```text
Your API token is apify_api_xxxxx.
```

---

## 4. Tool Capability Checklist

### Browser/Search

Can the agent search the web or open URLs?

If yes, it can:

```text
Check live pages
Inspect visible content
Find competitors
Check SERP manually
Find backlink opportunities
Check public profiles/directories
```

### Scraper/Crawler

Can the agent scrape or crawl multiple pages?

If yes, it can:

```text
Create page inventory
Extract titles/meta/H1/H2
Find thin pages
Find internal links
Classify URLs
Check schema snippets
Compare competitor pages
```

### Apify

Is `APIFY_API_TOKEN` or Apify MCP/tool access available?

If yes, it can potentially:

```text
Run website crawlers
Run SERP scrapers
Run Google Maps/local actors
Run Google Trends actors
Run authority-style actors
Run social/content scrapers
Schedule monitoring actors
Export structured datasets
```

Actor availability and quality must still be verified.

### File Access

Can the agent read uploaded files?

If yes, it can analyze:

```text
PDF reports
CSV keyword exports
GSC exports
GA4 exports
Ahrefs exports
Semrush exports
Moz exports
Crawl exports
Backlink sheets
Competitor documents
```

### Code Execution

Can the agent run Python/Node/shell?

If yes, it can:

```text
Normalize CSVs
Merge keyword data
Score issues
Classify URLs
Build reports
Validate JSON/schema syntax
Generate templates
```

### No Tools

If no tools are available, the agent can still:

```text
Ask for data
Provide manual audit process
Create strategy templates
Prepare client/developer briefs
Explain what to check
```

---

## 5. Input Data Quality Labels

Use these labels in reports.

### Confirmed

Use when data was directly verified from a reliable source or file.

Example:

```text
Confirmed: GSC export shows 1,240 clicks from the target country in the last 90 days.
```

### Likely

Use when evidence strongly suggests something but full verification is missing.

Example:

```text
Likely: the page is thin because the visible crawlable content is under 500 words, but a full crawl export would confirm all templates.
```

### Directional

Use for third-party/community actor data or approximate tools.

Example:

```text
Directional: Apify Ahrefs-style actor suggests low authority, but this should be confirmed with Ahrefs/Moz/Semrush export.
```

### Estimated

Use for calculations based on assumptions.

Example:

```text
Estimated: at 10% visitor-to-query conversion, 500 monthly queries require around 5,000 qualified visits/interactions.
```

### Not Verified

Use when a key data source was unavailable.

Example:

```text
Not verified: Google Business Profile performance was not available in this audit.
```

---

## 6. Capability Detection Output

Before a full audit, briefly state:

```text
Audit Mode:
Available Data:
Available Tools:
Missing Data:
How this affects confidence:
```

Example:

```text
Audit Mode: Native Agent Scraping Mode
Available Data: website URL, target city, 3 competitors
Available Tools: browser/search, page scraping
Missing Data: GSC, GA4, GBP, backlink export, Apify token
Confidence: strong for visible on-page and competitor content; limited for exact rankings, backlinks, and traffic.
```

For client-facing reports, include this as “Data Sources Used” and “Data Not Available.”

---

## 7. Mode Selection Logic

Use this decision tree:

```text
IF Apify + native browser/scraping + GSC/GA4/backlink exports are available:
    Use Full Intelligence Mode

ELSE IF Apify is available:
    Use Apify Intelligence Mode

ELSE IF native browser/search/scraping is available:
    Use Native Agent Scraping Mode

ELSE IF uploaded files/exports are available:
    Use File Analysis Mode

ELSE:
    Use Advisory Mode
```

If both files and native browser are available but no Apify exists, use:

```text
Native Agent Scraping Mode + File Analysis
```

If Apify exists but no live browser exists, use:

```text
Apify Intelligence Mode + File Analysis if files exist
```

---

## 8. What Each Capability Enables

### Website URL Only

Possible:

```text
First-pass audit
Visible content review
Basic technical checks if browser/scraper exists
Manual competitor discovery if search exists
```

Not possible without tools:

```text
Confirmed keyword rankings
Confirmed traffic
Confirmed backlinks
Confirmed GSC queries
Confirmed GBP performance
```

### Website URL + Apify

Possible:

```text
Structured crawl
SERP checks
Competitor crawl
Google Trends
Local/maps checks depending on actors
Authority-style directional checks depending on actors
```

Still may need:

```text
GSC/GA4 for actual performance
GBP access for actual calls/directions
Official Ahrefs/Semrush/Moz for verified authority/backlink metrics
```

### Website URL + GSC

Possible:

```text
Actual queries
Actual clicks/impressions
CTR issues
Pages with opportunity
Keyword cannibalization signals
Pages near ranking improvement
```

Need other tools for:

```text
Competitor gaps
Backlinks
Technical crawl
Local/map performance
```

### Website URL + GA4

Possible:

```text
Landing page performance
Engagement
Conversions if configured
Traffic source behavior
```

Need GSC for:

```text
Query-level SEO performance
```

### Website URL + GBP

Possible:

```text
Local calls
Direction requests
Profile views
Review strategy
Local conversion behavior
```

Need SERP/map scraping for:

```text
Competitor map pack comparison
```

### Ahrefs/Semrush/Moz Exports

Possible:

```text
Backlink audit
Authority gap
Competitor authority comparison
Top pages
Ranking footprint
Keyword gaps
```

Caution:

```text
Different tools have different databases. Do not treat one tool as absolute truth.
```

---

## 9. Missing Data Request Rules

Only request missing data when it materially changes the output.

High-value asks:

```text
GSC export
GA4 conversion report
GBP performance data
Competitor URLs
Ahrefs/Semrush/Moz backlink export
Apify token
Target city/service list
```

Low-value asks:

```text
Brand colors
Logo
Full company history
Every social link
```

Unless the task is a proposal or brand audit.

---

## 10. Confidence Notes

Every audit should include a confidence note if data is incomplete.

Example:

```text
This audit is strong for on-page structure, content gaps, and strategic planning. It is limited for confirmed rankings, backlinks, and conversion data because GSC, GA4, GBP, and authority exports were not provided.
```

---

## 11. Capability Detection Examples

### Example A: User Gives URL Only

Input:

```text
Audit https://example.com
```

If browser/search/scraping exists:

```text
Mode: Native Agent Scraping Mode
Proceed with visible crawl/search checks.
```

If no tools:

```text
Mode: Advisory Mode
Provide manual audit framework and request exports.
```

### Example B: User Gives URL + Apify Token

Input:

```text
Audit https://example.com. APIFY_API_TOKEN is available.
```

Output:

```text
Mode: Apify Intelligence Mode
Use Apify for crawl, SERP, competitor, and local/authority-style checks where actors exist.
```

### Example C: User Gives PDF Reports

Input:

```text
Use these SEO PDFs and make a plan.
```

Output:

```text
Mode: File Analysis Mode
Extract confirmed facts from PDFs, create recommendations, and label what needs live verification.
```

### Example D: User Gives Everything

Input:

```text
Website, competitors, GSC, GA4, GBP, Ahrefs export, Apify token.
```

Output:

```text
Mode: Full Intelligence Mode
Run complete technical, performance, keyword, competitor, local, backlink, AEO/GEO, and conversion audit.
```

---

## 12. Common Mistakes to Avoid

Do not:

```text
Choose Full Intelligence Mode just because a website URL was provided.
Claim backlink analysis without backlink data.
Claim rankings without SERP/GSC/rank data.
Treat Apify community actors as official Ahrefs/Semrush truth.
Ignore uploaded files.
Ask for APIs again after user already said they do not have them.
Stop working because one tool is missing.
```

---

## 13. Completion Rule

Capability detection is complete when the agent can clearly say:

```text
I know what data is available.
I know what tools are available.
I know what cannot be verified.
I know which audit mode to use.
I know how to proceed.
```
