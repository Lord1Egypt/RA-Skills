# Beyond SEO Onboarding — Apify-First

This file controls the first interaction when a user asks for SEO, AEO/GEO, backlinks, local SEO, competitor research, or reporting.

The goal is simple: do not ask for too many things.

---

## 1. Default First Question

Ask only for the essentials:

```text
Send the website URL, target country/city, main goal, and make sure APIFY_API_TOKEN is configured. If Apify is available, I can fetch the rest through Apify actors wherever possible.
```

If the website URL and goal are already given, do not ask again. Start capability detection.

---

## 2. API Rule

The only default API/access request is:

```text
APIFY_API_TOKEN
```

Do not ask up front for:

```text
Google Search Console API
GA4 API
PageSpeed API key
Ahrefs API
Semrush API
Moz API
Firecrawl
DataForSEO
```

Reason: Beyond SEO is Apify-first. It should look for Apify actors, Apify MCP tools, Apify datasets, or Apify-hosted exports first.

---

## 3. When to Ask for Extra Access

Ask for extra access only when:

```text
Apify cannot fetch the data.
An authenticated first-party source is required.
A user wants exact GSC/GA4/GBP performance.
A paid SEO database actor requires the user's own account/export.
The user asks for official verification rather than directional data.
```

Even then, phrase it as:

```text
Apify can handle this if there is an authenticated connector/export actor. If not, upload the export or connect the account.
```

---

## 4. Minimal Audit Start

For most audits:

```text
1. Check APIFY_API_TOKEN or Apify MCP.
2. If present, enter Apify Intelligence Mode.
3. Ask only missing business context: website URL, target location, goal.
4. Run credit-safe crawl/SERP sample.
5. Expand only after findings justify it.
```

---

## 5. Good Opening Message

```text
I’ll use Apify as the main data layer. I need the website URL, target location if local, and your main goal. If APIFY_API_TOKEN is configured, I’ll start with a credit-safe crawl and SERP sample, then use Apify actors for competitors, maps, trends, PageSpeed/Lighthouse, and authority/backlink checks where needed.
```

---

## 6. Bad Opening Message

Do not say:

```text
Please provide GSC, GA4, Ahrefs, Semrush, Moz, PageSpeed API, Screaming Frog, GBP, DataForSEO, Firecrawl, and Apify.
```

That overwhelms the user and defeats the Apify-first design.

---

## 7. Token Handling

Never ask the user to paste tokens into normal content files.

Preferred:

```text
Environment variable: APIFY_API_TOKEN
Agent secret manager
Apify MCP configuration
Secure runtime secret
```

If a token appears in chat, do not repeat it and do not save it into the skill.
