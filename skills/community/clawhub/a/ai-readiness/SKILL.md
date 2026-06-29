---
name: ai-readiness
description: >
  Generates a complete set of AI readiness files for any website from a single command.
  Invoke this skill whenever the user types `/ai-readiness [url]`, asks to "create AI readiness
  files for [site]", "make my site AI-ready", "generate llms.txt for [url]", "build AI files
  for [domain]", or any variation of wanting to optimize a website for AI systems (ChatGPT,
  Claude, Gemini, Perplexity, etc.). Also trigger when the user asks about AI crawlers,
  llmstxt.org, ai.txt, RAG indexing of a website, or improving a site's visibility in AI search.
  The output is a complete folder of 18 production-ready files — dropped into the workspace,
  ready to deploy to the web root.
created_by: Russ Wittmann
company: Silverback Marketing
version: 1.0.0
---

# AI Readiness File Generator

## What This Produces

A complete AI Readiness File Set for any website: 18 files that tell AI systems (ChatGPT,
Claude, Gemini, Perplexity, and others) exactly what the site is, what it offers, and where
to send users. When deployed to a web root, these files improve how the site appears in
AI-generated answers, summaries, and recommendations.

## Invocation

```
/ai-readiness [url]
```

Examples:
- `/ai-readiness shopify.com`
- `/ai-readiness https://www.acmecorp.com`
- `create AI readiness files for hubspot.com`

Normalize the input to a bare domain (e.g., `shopify.com`) and a canonical base URL
(e.g., `https://www.shopify.com`). If the user provides a path, strip it to the root domain.

---

## Phase 1 — Research (do this before writing a single file)

The quality of every file depends on the research. Do not skip or shortcut this phase.
Run **at minimum 10 targeted searches** using WebSearch and/or WebFetch. Save what you find —
you will use it throughout Phase 3.

### Required searches

Run all of these:

1. `site:[domain]` — discover indexed pages and site structure
2. `site:[domain] about` — company overview, founding, mission
3. `site:[domain] products OR services OR solutions` — what the site sells/offers
4. `site:[domain] pricing OR plans` — pricing pages
5. `site:[domain] blog OR resources OR insights` — content sections
6. `site:[domain] contact OR team OR careers` — company/org pages
7. `"[Company Name]" description OR overview` — how others describe this company
8. `[domain] site:linkedin.com` — often reveals employee count, HQ, founding year
9. *(Industry-specific)* For education: `site:[domain] programs OR courses OR destinations`
   For software: `site:[domain] integrations OR API OR documentation`
   For e-commerce: `site:[domain] categories OR collections`
10. `site:[domain] sitemap` or attempt `WebFetch` on `[baseURL]/sitemap.xml`

Also attempt `WebFetch` on:
- The homepage (`[baseURL]/`)
- 2-3 key product/service/program pages discovered in searches
- `[baseURL]/about` or `[baseURL]/about-us`

### What to extract and record

As you research, build up a working picture of the site. You need:

- **Company/org name** (exact legal/brand name)
- **Industry** (InsurTech, Education, E-commerce, SaaS, Healthcare, etc.)
- **What they sell/offer** — products, services, programs, courses, destinations
- **Key entity taxonomy** — categories, types, sub-types (e.g., for study abroad: program types, destinations, disciplines)
- **Confirmed URLs** — pages you've seen in search results or fetched that almost certainly return 200. Note: only include URLs you have reasonable confidence exist. Do NOT fabricate paths.
- **Brand differentiators** — what makes this org stand out vs competitors
- **Contact info** — email, phone, address if findable
- **Social links** — LinkedIn, Twitter/X, Facebook, YouTube, Instagram
- **Schema type** — what Schema.org type fits best: Organization, EducationalOrganization, SoftwareApplication, Store, etc.

---

## Phase 2 — Site Classification

Before writing files, classify the site. This determines defaults for schema types,
program taxonomies, and file emphasis.

| Site Type | Schema Type | Emphasis |
|-----------|-------------|----------|
| B2B Software / SaaS | SoftwareApplication + Organization | Product categories, integrations, use cases |
| Education / Study Abroad | EducationalOrganization + EducationalOccupationalProgram | Programs, locations, disciplines, financial aid |
| E-commerce / Retail | Store + Organization | Product categories, collections, shipping |
| Healthcare | MedicalOrganization + Organization | Services, specialties, locations |
| Professional Services | Organization | Service lines, industries served, team |
| Nonprofit | NGO + Organization | Mission, programs, impact, donate |
| Media / Publishing | Organization + WebSite | Topics, authors, sections |

Adapt all file content to the site type. An e-commerce site needs product taxonomies;
an education site needs program types and locations; a SaaS site needs product categories
and use cases.

---

## Phase 3 — File Generation

Generate all 18 files. Save to a folder named after the domain
(e.g., `shopify/` for shopify.com) in the workspace outputs directory.

**Order matters** — generate in this sequence, since later files reference earlier ones:

1. `ai.txt`
2. `llms.txt`
3. `llms-full.txt`
4. `ai-sitemap.xml`
5. `sitemap.md`
6. `ai-entities.json`
7. `ai-intent.json`
8. `ai-schema.json`
9. `rag-index.json`
10. `rag-index.jsonl` ← auto-generate via script (see below)
11. `ai-disclosure.txt`
12. `training-data-policy.txt`
13. `.well-known/ai-plugin.json`
14. `structured-data-guide.md`
15. `manifest.json`
16. `deployment-checklist.md`
17. `README.md`
18. `robots.txt`

See `references/file-specs.md` for the detailed specification of each file.
That file contains the required structure, key fields, and a condensed example for each.

### Generating rag-index.jsonl

After writing `rag-index.json`, auto-generate the JSONL version with this inline command
(substitute the actual output path for `[output_dir]`):

```bash
python3 -c "
import json
with open('[output_dir]/rag-index.json') as f:
    records = json.load(f)
with open('[output_dir]/rag-index.jsonl', 'w') as out:
    for r in records:
        out.write(json.dumps(r) + '\n')
print(f'Generated {len(records)} lines')
"
```

The `scripts/gen_jsonl.py` bundled with this skill does the same thing and accepts
two arguments: `python3 gen_jsonl.py <input.json> <output.jsonl>`.

---

## Quality Principles

**Only use real URLs.** Every URL in every file should be one you have strong reason to
believe returns a 200 response. If you're not sure a page exists, use a higher-level URL
that definitely does (e.g., use `/blog/` rather than `/blog/post-that-might-not-exist`).

**Be specific to this site.** Generic filler text defeats the purpose. Every file should
read as authoritative, first-person content about this specific company — not a template
with the name swapped in. Use the exact brand name, real product names, confirmed URLs.

**Match the industry.** Study abroad sites need program types and destinations. SaaS sites
need product categories and use cases. Don't apply a one-size-fits-all structure.

**Prioritize the llms files.** `ai.txt`, `llms.txt`, and `llms-full.txt` are the most
important — they're what AI systems actually read. Spend the most time making these rich,
accurate, and comprehensive.

**Keep robots.txt CMS-agnostic.** Do not include WordPress paths (`/wp-admin/`,
`/wp-login.php`) unless you have confirmed the site uses WordPress. Only add CMS-specific
disallow rules you can verify.

---

## Output

When all 18 files are written, tell the user:

1. How many files were created and where they are
2. A brief summary of what was found/generated (company, industry, key entities count)
3. Link to the folder so they can open it
4. Note any URLs or details you weren't able to confirm and how they handled it

Do NOT present a long recap of every file. One short paragraph + the file link is enough.
The user can read the README.md for the full picture.
