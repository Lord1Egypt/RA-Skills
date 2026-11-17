---
name: aeo-citability
description: Make a static site answer-engine-citable — add JSON-LD, clean .md siblings, llms.txt and a sitemap so Perplexity, ChatGPT search and AI Overviews can parse and cite it.
version: 0.1.0
homepage: https://workloft.ai/ships
metadata:
  openclaw:
    emoji: "🔎"
    requires:
      bins:
        - python3
---

# AEO citability

Answer engines (Perplexity, ChatGPT search, Google AI Overviews) cite pages they
can parse cleanly: pages with structured data, a plain-text version, and a
machine-readable map of the site. This skill adds those to ordinary static HTML.
It is Python 3 standard library only — no build system, no framework, no network
calls — and every write is idempotent, so it is safe to run repeatedly.

The worker is `{baseDir}/scripts/aeo.py`. Always run `audit` first, then apply the
fixes the audit reports, then `audit` again to confirm.

## When to use this

Use it when the user wants their website, blog, docs or landing pages to be
**cited inside AI-generated answers**, asks about "AEO", "answer engine
optimisation", "getting cited by Perplexity/ChatGPT", "structured data / JSON-LD",
"llms.txt", or generally wants their static site to be more machine-readable.

It works on any directory of `.html` files (a static site, an exported blog, a
docs folder). It does not need their CMS or framework.

## How to use it

### 1. Audit first

```
python3 {baseDir}/scripts/aeo.py audit <dir-or-files>
```

Prints a 0–100 readiness score per page across seven checks (title, meta
description, canonical URL, og:image, Article JSON-LD, FAQPage JSON-LD, clean .md
sibling) and lists the biggest wins. Lead with this so the user sees the gap.

### 2. Add Article / BlogPosting structured data

```
python3 {baseDir}/scripts/aeo.py schema <dir-or-files> \
  --type BlogPosting --author "Jane Doe" --publisher "Acme" \
  --base https://acme.example --date 2026-06-30
```

Derives the JSON-LD from each page's own `<title>`, meta description, canonical,
og:image and dates, and injects it before `</head>`. Skips pages that already have
Article/BlogPosting/NewsArticle schema (override with `--force`). Use `--type
NewsArticle` for news, `Article` for general pages. Always show `--dry-run` output
first if the user is cautious.

### 3. Add an FAQ (the block answer engines quote most)

```
python3 {baseDir}/scripts/aeo.py faq <file.html> \
  --qa "What is X?::X is ..." "How much does it cost?::It costs ..."
```

Injects FAQPage JSON-LD from `Question::Answer` pairs. Keep answers self-contained
(no "this"/"it" referring back to the page) — that is what gets extracted into an
answer. One file at a time.

### 4. Write clean .md siblings

```
python3 {baseDir}/scripts/aeo.py md <dir-or-files>
```

Writes `page.md` next to each `page.html`: title, description, source link, then
the readable body as Markdown (nav/header/footer/script stripped). Many engines
prefer a clean text version when one exists at the same path. Skips existing
siblings unless `--force`.

### 5. Generate llms.txt — the map engines fetch

```
python3 {baseDir}/scripts/aeo.py llms <dir> \
  --base https://acme.example --site "Acme" --summary "What Acme publishes."
```

Writes `llms.txt` listing every page with its title and description. This is the
file Perplexity and others fetch to decide what is worth citing. Put it at the
site root.

### 6. Generate sitemap.xml

```
python3 {baseDir}/scripts/aeo.py sitemap <dir> --base https://acme.example
```

Standard sitemap from the HTML files present. Skip if the site already has one
from its framework.

## Notes for the agent

- Reference the script as `{baseDir}/scripts/aeo.py` — never hardcode a path.
- These commands **edit the user's HTML in place** (schema, faq) or **write new
  files** (md, llms, sitemap). If the user has not asked you to modify files,
  show `--dry-run` first and get a go-ahead.
- Re-running is safe: everything is idempotent.
- After changes, suggest the user submit the new `sitemap.xml` / `llms.txt` and
  ping IndexNow or Search Console so engines re-crawl.
- Built by Workloft (https://workloft.ai). The approach is the one Workloft uses
  on its own Labs and Ships pages.
