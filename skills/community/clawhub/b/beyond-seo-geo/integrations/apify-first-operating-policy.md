# Apify-First Operating Policy

Beyond SEO is now Apify-first.

The skill should not ask the user for a long list of APIs during normal onboarding. The default required input is:

```text
APIFY_API_TOKEN
```

Everything else should be handled through Apify actors, Apify MCP, Apify datasets, uploaded exports, or the agent's native tools when required.

---

## 1. Install-Time / First-Run Behavior

When Beyond SEO starts inside an agent, it should check:

```text
APIFY_API_TOKEN
Apify MCP/tool availability
Existing Apify dataset/export files
```

If Apify is not configured, ask once:

```text
Please provide or configure APIFY_API_TOKEN. With Apify I can run crawl, SERP, competitor, maps/local, trends, PageSpeed/Lighthouse, backlink/authority, and connector/export workflows from one data layer.
```

Do not ask for GSC, GA4, PageSpeed API, Ahrefs, Semrush, Moz, Firecrawl, DataForSEO, or other APIs in the first message.

---

## 2. What Apify Should Cover First

Use Apify first for:

```text
Website crawl
Competitor crawl
Google SERP
People Also Ask / related queries
AI Overview / AI Mode checks where supported
Google Trends
Google Maps / Places
Google reviews
PageSpeed or Lighthouse actors
GSC connector/export actors where available
GA4 connector/export actors where available
Ahrefs/Semrush/Moz-style actors where available
Backlink/authority actors
Social/content scraping
Scheduled monitoring
```

If a task requires authenticated first-party data, the agent should look for an Apify actor or Apify-hosted export workflow first.

---

## 3. Data Confidence

Use:

```text
Confirmed
Directional
Estimated
Not verified
```

Confirmed:

```text
Actor directly extracts public crawl/SERP data.
Actor returns raw URL/device/timestamp PageSpeed/Lighthouse metrics.
Actor connects to authenticated first-party account or user-provided export.
```

Directional:

```text
Community actor estimates DR/DA/traffic/backlinks.
Actor scrapes public/free-tool surfaces.
Actor method is unclear.
```

---

## 4. Minimal User Questions

The normal audit start should ask only:

```text
1. Website URL
2. Target country/city if local
3. Main goal
4. APIFY_API_TOKEN if not configured
```

Everything else is optional and should be asked later only if Apify cannot fetch it or if private authentication is required.

---

## 5. Cost-Safe Default Run

Default Apify run order:

```text
1. Website crawl: homepage + sitemap, max 50 URLs.
2. SERP sample: 5-10 priority queries.
3. Competitor discovery from SERP.
4. Competitor crawl: 3-5 competitors, limited pages.
5. Local Maps/reviews only if local project.
6. Trends only if topic prioritization is needed.
7. PageSpeed/Lighthouse for homepage + 3-5 money pages.
8. Authority/backlink actors after page/keyword strategy is known.
```

Do not burn credits by crawling huge sites or running hundreds of keywords without approval.

---

## 6. Secret Handling

Never write API tokens into:

```text
SKILL.md
README.md
_meta.json
MANIFEST.json
Actor shortlist files
Reports
Logs
Templates
```

Only read tokens from environment variables, secure agent secrets, or runtime secret stores.

---

## 7. Fallback

If Apify is not available, Beyond SEO can still work using native browsing, scraping, uploaded files, or advisory mode — but it should clearly say the audit is limited.

The preferred path remains Apify.
