# AI Readiness File Specifications

Detailed spec for each of the 18 files. For each file, the spec covers:
- Purpose and audience
- Required structure / key fields
- Condensed example pattern
- Common mistakes to avoid

---

## 1. ai.txt

**Purpose:** The AI equivalent of robots.txt. Declares crawler permissions, brand identity,
product taxonomy, authoritative topics, and training data policy. Deployed at `/ai.txt`.

**Audience:** AI crawlers, LLM training pipelines, RAG indexers.

**Structure:**
```
# [COMPANY] AI Permissions and Identity File
# Version: 1.0 | Updated: [DATE] | Domain: [BASE_URL]

## AI CRAWLER PERMISSIONS
User-agent: *
Allow: /
Disallow: [private paths — login, admin, checkout, apply]

User-agent: GPTBot
Allow: /
Allow: /llms.txt
...

## BRAND IDENTITY
Name: [Full legal/brand name]
Domain: [baseURL]
Description: [2-3 sentence brand description]
Founded: [year if known]
Headquarters: [city, country if known]
Industry: [industry]

## PRODUCT/SERVICE TAXONOMY
[List all major categories with brief descriptions]

## AUTHORITATIVE TOPICS
[List 15-25 topics this site is authoritative on]

## TRAINING DATA POLICY
[Permission statement — default: allow retrieval/RAG, require license for commercial training]
```

**Common mistakes:** Don't include `Disallow: /wp-admin/` unless the site uses WordPress.
Don't list topics that aren't actually covered by the site.

---

## 2. llms.txt

**Purpose:** Concise LLM site index following the [llmstxt.org](https://llmstxt.org/) standard.
Structured markdown that fits in a single LLM context window. Deployed at `/llms.txt`.

**Audience:** LLMs, AI assistants, AI search engines.

**Structure:**
```markdown
# [Company Name]

> [One paragraph brand description — who they are, what they do, who they serve]

## [Section 1 — e.g., "Products" or "Programs" or "Destinations"]
- [Page Title]([URL]): [One-line description]
- [Page Title]([URL]): [One-line description]

## [Section 2]
...

## Resources
- [FAQ]([URL]): [description]
- [Blog]([URL]): [description]

## Company
- [About]([URL]): [description]
- [Contact]([URL]): [description]

## Key Questions This Site Answers
- [query 1 from research]
- [query 2 from research]
...
```

**Rules:**
- H1 = company name only
- Blockquote = one-paragraph description
- H2 sections = logical groupings of pages
- Each link = `[Title](URL): description`
- End with "Key Questions This Site Answers" listing 15-25 high-value queries
- Aim for 100-200 lines total — long enough to be useful, short enough to fit in context

---

## 3. llms-full.txt

**Purpose:** Extended version of llms.txt with rich descriptions, detailed Q&A, and deep
context for RAG pipelines and AI systems needing full detail. Deployed at `/llms-full.txt`.

**Audience:** LLMs, RAG pipelines, AI knowledge bases.

**Structure:**
```markdown
# [Company Name] — Complete LLM Context File
*As of [DATE]. For current pricing and availability, visit [baseURL].*

## Company Overview
[3-5 paragraphs: who they are, history, what makes them distinctive, who they serve]

## [Category 1 — e.g., "Products" or "Programs by Destination"]

### [Subcategory — e.g., specific product or city]
[2-4 paragraphs of rich description: what it is, key features/highlights, who it's for, URL]

### [Next subcategory]
...

## Financial Information / Pricing
[Pricing overview, scholarships, financial aid — whatever applies]

## Frequently Asked Questions

**Q: [High-value query]**
A: [Authoritative, specific answer with URL references]

**Q: [Next query]**
A: [Answer]
...
```

**Rules:**
- Must answer the key queries identified in research (the "Key Questions" from llms.txt)
- Q&A section should have at least 8 questions
- Each answer should cite specific URLs for where to learn more
- Include the "as of [date]" note so AI systems know to check for updates

---

## 4. ai-sitemap.xml

**Purpose:** AI-optimized XML sitemap with per-URL topic tags, content-type metadata,
and plain-English summaries. Extends the standard sitemap protocol. Deployed at `/ai-sitemap.xml`.

**Audience:** AI crawlers, semantic search indexers, RAG pipelines.

**Structure:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:ai="https://schema.org/AIContentMetadata">

  <url>
    <loc>[URL]</loc>
    <lastmod>[YYYY-MM-DD]</lastmod>
    <priority>[0.5–1.0]</priority>
    <changefreq>[always|daily|weekly|monthly|yearly]</changefreq>
    <ai:content-type>[homepage|product|service|program|blog|faq|about|contact|pricing|resource]</ai:content-type>
    <ai:topic>[comma, separated, keywords]</ai:topic>
    <ai:summary>[One plain-English sentence describing what's on this page]</ai:summary>
  </url>

  ...
</urlset>
```

**Priority tiers:**
- 1.0: Homepage
- 0.9: Top-level product/service/program hubs
- 0.8: Key product/service/program detail pages
- 0.7: Resources, blog, about, pricing
- 0.6: Support, careers, contact, legal

**Aim for 35-55 URLs.** Cover all confirmed pages from research.

---

## 5. sitemap.md

**Purpose:** Human-readable markdown sitemap organized by section. Easy for LLMs and
developers to parse. Deployed at `/sitemap.md`.

**Structure:**
```markdown
# [Company] Site Map

## [Section 1]
| Page | URL | Description |
|------|-----|-------------|
| [Title] | [URL] | [One-line description] |

## [Section 2]
...

## AI Readiness Files
| File | URL | Purpose |
|------|-----|---------|
| ai.txt | [baseURL]/ai.txt | AI crawler permissions and brand identity |
| llms.txt | [baseURL]/llms.txt | LLM site index |
...
```

Always end with an "AI Readiness Files" section linking to all 13 deployed files.

---

## 6. ai-entities.json

**Purpose:** Structured entity declarations for AI classification. Deployed at `/ai-entities.json`.

**Structure:**
```json
{
  "organization": {
    "name": "[Company Name]",
    "brand_names": ["[Name]", "[Alt Name]"],
    "domain": "[baseURL]",
    "industry": "[industry]",
    "founded": "[year]",
    "headquarters": "[city, country]",
    "description": "[one sentence]",
    "last_updated": "[YYYY-MM-DD]"
  },
  "[primary_taxonomy_key]": {
    "categories": ["[cat1]", "[cat2]"],
    "[subcategory_key]": ["[item1]", "[item2]"]
  },
  "priority_urls": {
    "[key]": "[URL]",
    "[key2]": "[URL2]"
  }
}
```

The `primary_taxonomy_key` depends on site type:
- Software: `"products"` with `"categories"` and `"named_products"`
- Education: `"programs"` with `"types"`, `"destinations"`, `"disciplines"`
- E-commerce: `"catalog"` with `"categories"`, `"collections"`

---

## 7. ai-intent.json

**Purpose:** Maps user query intents to the best landing URL. Helps AI assistants route
users to the right page. Deployed at `/ai-intent.json`.

**Structure:**
```json
{
  "intents": [
    {
      "query": "[natural language query]",
      "intent": "[category: informational|navigational|transactional]",
      "preferred_url": "[URL key from preferred_urls]",
      "confidence": "[high|medium]"
    }
  ],
  "preferred_urls": {
    "[key]": "[full URL]"
  }
}
```

**Aim for 30-50 intents.** Cover:
- General informational queries ("what is [company]", "what does [company] do")
- Product/service/program queries ("how to [use product]", "what is [program type]")
- Comparison queries ("best [category] software", "top [category] programs")
- How-to / decision queries (the key queries from llms.txt)
- Per-entity queries (one per major product, destination, or category)

---

## 8. ai-schema.json

**Purpose:** JSON-LD Schema.org structured data. Can be embedded in the site `<head>`
or served as a standalone reference. Deployed at `/ai-schema.json`.

**Structure:** Use the appropriate primary type from Phase 2 classification:

```json
{
  "@context": "https://schema.org",
  "@type": "[Organization|EducationalOrganization|SoftwareApplication|Store]",
  "name": "[Company Name]",
  "alternateName": ["[alt name]"],
  "url": "[baseURL]",
  "logo": "[baseURL]/logo.png",
  "description": "[2-3 sentence description]",
  "foundingDate": "[year]",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "[city]",
    "addressCountry": "[country code]"
  },
  "contactPoint": {
    "@type": "ContactPoint",
    "email": "[email]",
    "contactType": "customer support"
  },
  "sameAs": ["[LinkedIn URL]", "[Twitter URL]", "[Facebook URL]"],
  "knowsAbout": ["[topic1]", "[topic2]"],
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "[Products/Programs/Services]",
    "url": "[catalog URL]"
  }
}
```

For SaaS: add `"applicationCategory"`, `"operatingSystem"`, `"hasPart"` (one per major product).
For Education: use `EducationalOrganization`, add `"hasOfferCatalog"` with programs.

---

## 9. rag-index.json

**Purpose:** JSON array ready for ingestion into RAG pipelines and vector databases.
Deployed at `/rag-index.json`.

**Structure:**
```json
[
  {
    "url": "[full URL]",
    "title": "[Descriptive page title — not just the nav label]",
    "topics": ["[topic1]", "[topic2]", "[topic3]"]
  }
]
```

**Aim for 40-60 records.** Cover:
- Homepage
- All major product/service/program hub pages
- All individual product/destination/service pages
- Pricing, about, contact
- 5-10 blog/resource posts (if the site has them)
- Financial aid / scholarships (if applicable)
- FAQ, support, documentation

Topics should be 3-6 keywords per record, specific enough to be useful for semantic search.

---

## 10. rag-index.jsonl

Auto-generated from rag-index.json. Same records, one JSON object per line.
See SKILL.md for the generation command.

---

## 11. ai-disclosure.txt

**Purpose:** Transparent disclosure of AI usage on the website and in products/services.

**Structure:**
```
AI Usage Disclosure
[Company Name] | [baseURL]
Last Updated: [DATE]

## How We Use AI on This Website
[Describe: chatbots, personalization, content generation, recommendations]

## How We Use AI in Our Products/Services
[Describe AI features in the product/service if applicable]

## Accuracy Commitment
[State what the company does/doesn't guarantee about AI-generated content]

## Data and Privacy
[Brief statement on user data and AI]

## Contact
[contact email for AI-related questions]
```

**For sites where accuracy matters critically** (education, healthcare, finance):
include an explicit no-fabrication commitment for key details like pricing, dates,
eligibility, or medical advice.

---

## 12. training-data-policy.txt

**Purpose:** Granular policy governing use of site content for AI model training.

**Structure:**
```
AI Training Data Policy
[Company Name] | [baseURL]
Last Updated: [DATE]
Contact: [email]

## Permitted Uses
- Retrieval-Augmented Generation (RAG): PERMITTED
- Non-commercial academic research: PERMITTED
- AI-powered search indexing (Perplexity, etc.): PERMITTED

## Restricted Uses
- Commercial model training: REQUIRES LICENSE
- Republication of verbatim content: NOT PERMITTED
- Training on [sensitive content type]: NOT PERMITTED

## Content-Type Breakdown
[List key content types and their specific permissions]

## Attribution
When citing content: "[Company Name] ([baseURL])"

## Licensing
Contact [email] for commercial training licenses.
```

**For sites with time-sensitive data** (education pricing, healthcare, finance):
add a note that AI systems should link to source pages rather than caching values.

---

## 13. .well-known/ai-plugin.json

**Purpose:** AI plugin discovery metadata. Deployed at `/.well-known/ai-plugin.json`.

**Structure:**
```json
{
  "schema_version": "v1",
  "name_for_human": "[Company Name]",
  "name_for_model": "[lowercase_underscore_name]",
  "description_for_human": "[One sentence: what this plugin/integration does for users]",
  "description_for_model": "[2-3 sentences for AI: what data is available, what queries it can answer]",
  "auth": { "type": "none" },
  "api": {
    "type": "openapi",
    "url": "[baseURL]/openapi.yaml",
    "is_user_authenticated": false
  },
  "logo_url": "[baseURL]/logo.png",
  "contact_email": "[contact email]",
  "legal_info_url": "[baseURL]/privacy-policy",
  "topics": ["[topic1]", "[topic2]"],
  "key_urls": {
    "[key]": "[URL]"
  }
}
```

`key_urls` should map 8-15 logical names to the most important pages on the site.

---

## 14. structured-data-guide.md

**Purpose:** Developer guide for implementing JSON-LD Schema.org on the site.

**Structure:**
```markdown
# Structured Data Implementation Guide
[Company] | [baseURL]

## Overview
[Brief: why structured data matters, what schema types are used]

## Schema Types by Page Type
| Page Type | Schema Type | Priority |
|-----------|-------------|----------|
| Homepage | Organization + WebSite + SearchAction | Critical |
| [Product/Program page] | [Schema type] | High |
...

## Schema Implementations

### [Schema type 1]
[When to use it]
[Complete JSON-LD example]

### [Schema type 2]
...

## Validation
- Google Rich Results Test: https://search.google.com/test/rich-results
- Schema.org Validator: https://validator.schema.org/
```

Choose schemas appropriate for the site type. Minimum set:
- All sites: Organization, WebSite + SearchAction (homepage), BreadcrumbList, BlogPosting
- Education: EducationalOccupationalProgram, Place (for locations), Grant (for scholarships)
- Software: SoftwareApplication, FAQPage
- E-commerce: Product, Offer, ItemList

---

## 15. manifest.json

**Purpose:** Machine-readable inventory of all AI readiness files.

**Structure:**
```json
{
  "name": "[Company] AI Readiness File Set",
  "version": "1.0.0",
  "generated": "[YYYY-MM-DD]",
  "domain": "[baseURL]",
  "company": "[Company Name]",
  "industry": "[industry]",
  "contact": "[contact email]",
  "description": "[one sentence about the file set]",
  "files": [
    {
      "filename": "[filename]",
      "deploy_path": "/[path]",
      "url": "[baseURL]/[path]",
      "content_type": "[MIME type]",
      "purpose": "[one sentence]",
      "audience": ["[audience1]", "[audience2]"],
      "update_frequency": "[frequency]",
      "priority": "[critical|high|medium|low]"
    }
  ],
  "totals": {
    "total_files": 13,
    "critical": 3,
    "high": 6,
    "medium": 4,
    "low": 1
  },
  "related_urls": {
    "robots_txt": "[baseURL]/robots.txt",
    "standard_sitemap": "[baseURL]/sitemap.xml",
    "privacy_policy": "[baseURL]/privacy-policy"
  }
}
```

List all 13 *deployed* files (not the 5 internal docs). Priorities:
- Critical: ai.txt, llms.txt, llms-full.txt
- High: ai-sitemap.xml, ai-entities.json, ai-intent.json, ai-schema.json, rag-index.json, rag-index.jsonl
- Medium: sitemap.md, ai-disclosure.txt, training-data-policy.txt, ai-plugin.json
- Low: structured-data-guide.md

---

## 16. deployment-checklist.md

**Purpose:** Step-by-step deployment guide for the web/IT team.

**10 phases:**
1. Deploy critical text files (ai.txt, llms.txt, llms-full.txt) — verify each URL
2. Deploy sitemap and markdown (ai-sitemap.xml, sitemap.md)
3. Deploy JSON AI files (ai-entities.json, ai-intent.json, ai-schema.json, rag-index.json, rag-index.jsonl)
4. Deploy policy files (ai-disclosure.txt, training-data-policy.txt)
5. Deploy .well-known/ai-plugin.json
6. Update robots.txt — add AI crawler blocks + Sitemap: reference
7. Add structured data to site `<head>` (from structured-data-guide.md)
8. Register ai-sitemap.xml with Google Search Console and Bing
9. Final URL verification table + batch curl script
10. Announce and index (share llms.txt URL with SEO team, add `<link rel="ai-content-declaration">` to `<head>`)

Use checkboxes `- [ ]` for all action items. End with a maintenance schedule table.

---

## 17. README.md

**Purpose:** Human-readable documentation for the whole file set.

**Sections:**
1. **What Is This** — overview for someone who's never seen these files
2. **Why AI Readiness Matters** — 3-4 bullet business case (with stats if available)
3. **File Inventory** — table organized by tier (Critical / High / Medium / Supporting)
4. **Key Queries** — bulleted list of the 15-25 queries these files are optimized for
5. **Coverage** — at-a-glance stats (e.g., "22 destinations, 9 program types, 40 query intents")
6. **How Each File Works** — 2-4 sentence explanation per file
7. **Deployment** — quick-start `cp` commands + link to deployment-checklist.md
8. **Verification** — batch curl script
9. **Maintenance** — table of files and when to update them
10. **Standards Referenced** — table linking to llmstxt.org, Schema.org, etc.

---

## 18. robots.txt

**Purpose:** Example robots.txt showing how to add AI crawler blocks alongside the
standard sitemap reference. The real file must be *merged* into the live robots.txt —
this is a reference, not a replacement.

**AI crawlers to include:** GPTBot, ClaudeBot, Google-Extended, PerplexityBot, FacebookBot, CCBot

**For each crawler:**
```
User-agent: GPTBot
Allow: /
Allow: /llms.txt
Allow: /llms-full.txt
Allow: /ai.txt
Allow: /ai-sitemap.xml
Allow: /rag-index.json
Allow: /rag-index.jsonl
Allow: /ai-entities.json
Allow: /ai-intent.json
Disallow: [private paths specific to this site — login, admin, apply, checkout]
```

**Important:** Only include `Disallow` paths you can confirm are relevant to this site.
Do NOT include WordPress paths (`/wp-admin/`, `/wp-login.php`) unless you can confirm
the site uses WordPress. Do NOT include e-commerce paths (`/checkout/`) for non-commerce sites.

End with:
```
Sitemap: [baseURL]/sitemap.xml
Sitemap: [baseURL]/ai-sitemap.xml
```

And a comment block listing all AI readiness file URLs.
