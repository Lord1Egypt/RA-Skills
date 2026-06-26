# Apify-First Audit Mode Override

Beyond SEO should prefer Apify Intelligence Mode whenever Apify is available.

## New Default Mode Priority

```text
1. Apify Intelligence Mode
2. Apify + File Analysis Mode
3. Native Agent Scraping Mode
4. File Analysis Mode
5. Advisory Mode
```

Full Intelligence Mode now means:

```text
Apify Intelligence Mode + authenticated/export-based Apify data + optional uploaded files.
```

The skill should not ask for separate GSC/GA4/Ahrefs/Semrush/Moz/PageSpeed APIs at the start. It should search/use Apify actors first.


---

# Audit Modes

Beyond SEO works in five modes. The agent must choose the correct mode before starting an audit, strategy, competitor analysis, backlink plan, or AEO/GEO task.

The goal is to produce the best possible result without pretending that unavailable data was checked.

---

## Mode Summary

```text
Mode 1: Full Intelligence Mode
Mode 2: Apify Intelligence Mode
Mode 3: Native Agent Scraping Mode
Mode 4: File Analysis Mode
Mode 5: Advisory Mode
```

---

# Mode 1: Full Intelligence Mode

## When to Use

Use this mode when the agent has most of the following:

```text
Website URL
Target market/location
Competitor URLs
Apify token or advanced crawler
Native browser/search/scraping
GSC export/access
GA4 export/access
GBP export/access if local
Ahrefs/Semrush/Moz export or authority data
Ability to process CSV/PDF/JSON files
```

## What This Mode Can Produce

```text
Full technical SEO audit
Page inventory
Crawlability and indexability review
Keyword ranking and opportunity review
GSC query/page performance analysis
GA4 conversion/landing page analysis
Competitor SERP and content gap analysis
Local SEO and map pack analysis
Backlink/authority gap analysis
AEO/GEO readiness audit
Conversion SEO audit
30/60/90-day execution roadmap
Client-ready report
Developer task brief
Content and page brief plan
```

## Required Output Sections

```text
1. Data Sources Used
2. Executive Summary
3. Current SEO Health
4. Confirmed Technical Issues
5. Keyword and Page Opportunity
6. Competitor Gap
7. Local SEO Gap if relevant
8. Backlink/Authority Gap
9. AEO/GEO Gap
10. Conversion Gap
11. 30-Day Plan
12. 60-Day Plan
13. 90-Day Plan
14. KPIs
15. Remaining Data Gaps
```

## Confidence Level

High, if data is fresh and complete.

Still avoid guarantees.

---

# Mode 2: Apify Intelligence Mode

## When to Use

Use this mode when:

```text
APIFY_API_TOKEN is available
OR Apify MCP/tool access is available
```

but GSC/GA4/GBP/official backlink exports may be missing.

## What Apify Can Help With

Depending on actor availability:

```text
Website crawling
Competitor crawling
Sitemap crawling
SERP scraping
Google Trends checks
Google Maps/local scraping
Google reviews scraping
Ahrefs-style metrics via community actors
Semrush-style checks via community actors
Moz-style checks via community actors
Similarweb-style traffic checks
Social/content competitor scraping
Scheduled monitoring
```

## Important Caution

Apify is a marketplace. Actor quality varies.

Use labels:

```text
Confirmed: when actor output is reliable and directly observed.
Directional: when community actor data approximates third-party SEO metrics.
Not verified: when the actor does not support a needed metric.
```

Do not say “official Ahrefs data” unless the data came from an official export or authenticated official source.

## Required Process

```text
1. Identify needed actor categories.
2. Check actor availability.
3. Run/plan website crawl.
4. Run/plan SERP checks for target keywords.
5. Run/plan competitor crawls.
6. Run/plan local/maps checks if local business.
7. Run/plan authority-style checks if useful.
8. Normalize outputs.
9. Build audit and roadmap.
10. Mark missing GSC/GA4/GBP data.
```

## What This Mode Cannot Fully Confirm Without Other Data

```text
Actual GSC queries
Actual organic clicks/impressions
Actual GA4 conversions
Actual GBP calls/directions
Official Ahrefs/Semrush/Moz backlink counts
CRM lead quality
Revenue data
```

## Best Use Cases

```text
First serious SEO audit
Competitor research
SERP and content gap analysis
Local SEO scan
AI-search/AEO checks if actors support SERP/AI result scraping
Backlink/authority directional review
```

## Confidence Level

Medium to high for crawl/SERP/content findings.  
Medium or directional for third-party authority metrics unless verified.

---

# Mode 3: Native Agent Scraping Mode

## When to Use

Use this mode when no Apify token is available, but the agent has:

```text
Browser/search access
Page opening ability
Scraper/crawler tool
Screenshot or HTML inspection
Manual SERP research capability
```

## What This Mode Can Produce

```text
Visible website audit
Basic technical observations
Content and on-page audit
Competitor visible page comparison
Manual SERP observations
Schema presence checks if HTML/source can be viewed
Internal linking observations
Local SEO visible checks
AEO/GEO content readiness review
Strategic 90-day plan
```

## Limitations

Cannot reliably confirm without specific tools/files:

```text
Full site crawl for large sites
Complete backlink profile
Exact search volume
Exact ranking history
GSC clicks/impressions
GA4 conversions
GBP performance
Core Web Vitals field data
```

## Required Output Labels

Use:

```text
Observed from available pages
Likely
Not verified
Recommended next check
```

## Best Use Cases

```text
Fast first-pass audit
Client discovery review
Proposal preparation
Competitor page comparison
Service page gap discovery
AEO/GEO content improvement
```

## Example Output Note

```text
This audit is based on visible pages and available search/scraping access. It is strong for content, page structure, and strategy. It is limited for confirmed rankings, backlinks, traffic, and conversions because GSC, GA4, GBP, and backlink exports were not provided.
```

## Confidence Level

Medium for visible page findings.  
Low for exact rankings/backlinks unless directly checked.

---

# Mode 4: File Analysis Mode

## When to Use

Use this mode when live tools are unavailable, but the user provides:

```text
SEO PDF reports
GSC exports
GA4 exports
Screaming Frog exports
Sitebulb exports
Ahrefs exports
Semrush exports
Moz exports
Backlink sheets
Keyword sheets
Competitor reports
Client documents
Screenshots
```

## What This Mode Can Produce

```text
Report analysis
Findings summary
Prioritized action plan
Keyword map from exports
Backlink prospect review
Competitor strategy based on reports
90-day roadmap
Client proposal
Developer brief
```

## Required Process

```text
1. Identify file types.
2. Extract confirmed facts.
3. Separate data from recommendations.
4. Check for outdated data.
5. Build issue/opportunity summary.
6. Create roadmap.
7. List missing live checks.
```

## Important Caution

Files may be outdated. Metadata is not enough. Use document content and dates if available.

If the report says “current” but has old dates, label it:

```text
Potentially outdated. Needs live verification.
```

## Best Use Cases

```text
Turning existing audits into better plans
Upgrading client proposals
Building skill examples
Summarizing SEO exports
Creating execution briefs
Analyzing backlink lists
```

## Confidence Level

Depends on source freshness and completeness.

Use:

```text
Confirmed from uploaded file
Not independently verified live
```

---

# Mode 5: Advisory Mode

## When to Use

Use this mode when:

```text
No API
No browser/search
No scraping
No uploaded files
No exports
Only a general question or goal
```

## What This Mode Can Produce

```text
Manual audit checklist
Data request list
SEO strategy framework
Client intake form
Technical checklist
Backlink evaluation framework
AEO/GEO framework
Content plan template
90-day planning skeleton
```

## What This Mode Must Not Do

Do not claim:

```text
The site has X backlinks.
The site ranks for X keywords.
The site traffic is X.
Competitor has X pages.
Core Web Vitals are poor.
GBP is weak.
```

unless the user provided data.

## Best Use Cases

```text
Planning
Training
Prompt writing
Skill design
Client intake
SEO SOP creation
Manual checklist creation
```

## Confidence Level

Strategic only. Not an audit.

---

# Hybrid Modes

Sometimes the correct mode is a combination.

## Native + File Mode

Use when:

```text
Uploaded files exist
Browser/search/scraping exists
No Apify
```

Output:

```text
Audit Mode: Native Agent Scraping Mode + File Analysis
```

## Apify + File Mode

Use when:

```text
Apify exists
Uploaded exports/reports exist
```

Output:

```text
Audit Mode: Apify Intelligence Mode + File Analysis
```

## Advisory + Templates

Use when:

```text
No data exists but user needs deliverables
```

Output:

```text
Audit Mode: Advisory Mode
Deliverable: checklist/template/brief
```

---

# Audit Mode Selection Tree

Use this decision tree:

```text
START

Do I have enough data/tools for live verification?

IF Apify + GSC/GA4/backlink/GBP exports + competitor data:
    Full Intelligence Mode

ELSE IF Apify is available:
    Apify Intelligence Mode

ELSE IF browser/search/scraping is available:
    Native Agent Scraping Mode

ELSE IF uploaded files are available:
    File Analysis Mode

ELSE:
    Advisory Mode
```

If two sources exist, combine modes.

---

# Mode Announcement Template

For serious audits, include a short mode note:

```text
Audit Mode: [mode name]
Available: [data/tools]
Missing: [data/tools]
Confidence: [short note]
```

Example:

```text
Audit Mode: Apify Intelligence Mode
Available: website URL, target city, Apify token, competitor URLs
Missing: GSC, GA4, GBP, official backlink export
Confidence: strong for crawl/SERP/competitor checks; limited for actual traffic, conversions, and GBP call data.
```

---

# Mode-Specific Deliverables

## Full Intelligence Mode Deliverables

```text
Technical audit
Keyword audit
GSC opportunity report
GA4 conversion report
Competitor gap
Backlink gap
Local SEO audit
AEO/GEO audit
30/60/90-day plan
KPI dashboard outline
```

## Apify Intelligence Mode Deliverables

```text
Crawl report
SERP/competitor findings
Local/maps findings where actor supports it
Authority-style directional analysis
Keyword-to-page map
AEO/GEO recommendations
90-day plan
Missing-data list
```

## Native Agent Scraping Mode Deliverables

```text
Visible site audit
Manual competitor comparison
Content/page gap plan
Technical observations
AEO/GEO recommendations
Backlink/local next-check list
90-day strategy
```

## File Analysis Mode Deliverables

```text
Findings from files
Issue consolidation
Opportunity summary
Execution roadmap
Report rewrite/proposal
Missing live verification list
```

## Advisory Mode Deliverables

```text
Manual checklist
Data request list
Process guide
Templates
Strategic plan skeleton
```

---

# What to Do If the User Disagrees With Mode

If user says:

```text
No, do full audit without tools.
```

Respond:

```text
I can create a strategic audit framework and first-pass checklist, but I cannot honestly confirm rankings, backlinks, traffic, or technical crawl issues without live access, scraping, or exports.
```

Then continue in Advisory or File mode.

If user says:

```text
Use only my files.
```

Use File Analysis Mode and do not browse.

If user says:

```text
Do not use APIs.
```

Use Native Agent Scraping Mode or File Analysis Mode.

---

# Quality Gate Before Final Output

Before giving final output, check:

```text
Did I announce or internally select the correct mode?
Did I avoid inventing unavailable data?
Did I label estimates?
Did I include missing data?
Did I prioritize issues?
Did I connect actions to business impact?
Did I avoid guarantees?
```

If yes, proceed.

---

# Short Mode Reference

```text
Full Intelligence = best possible, complete data stack.
Apify Intelligence = strong crawl/SERP/data layer, missing first-party performance unless exports exist.
Native Scraping = good visible audit, limited hard metrics.
File Analysis = strong if exports/reports are good, needs live verification.
Advisory = strategy only, not verified audit.
```
