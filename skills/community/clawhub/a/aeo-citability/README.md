# aeo-citability 🔎

An [OpenClaw](https://github.com/openclaw/openclaw) skill that makes a static
site **answer-engine-citable** — the work that gets your pages parsed and cited
by Perplexity, ChatGPT search and Google AI Overviews, not just ranked by classic
SEO.

It adds four things to plain HTML:

1. **Article / BlogPosting JSON-LD** — derived from each page's own head.
2. **FAQPage JSON-LD** — the block answer engines quote most directly.
3. **Clean `.md` siblings** — the readable text version many engines prefer.
4. **`llms.txt` + `sitemap.xml`** — the maps engines fetch to decide what to cite.

Python 3 standard library only. No build system, no framework, no network calls.
Every write is idempotent, so it is safe to run on a live site repeatedly.

## Quick start

```bash
# 1. See where you stand (0–100 per page)
python3 scripts/aeo.py audit ./site

# 2. Add structured data
python3 scripts/aeo.py schema ./site --author "Jane Doe" --publisher "Acme" \
  --base https://acme.example

# 3. Add an FAQ to a key page
python3 scripts/aeo.py faq ./site/pricing.html \
  --qa "How much does it cost?::Plans start at £9/month."

# 4. Clean text siblings + the maps
python3 scripts/aeo.py md ./site
python3 scripts/aeo.py llms ./site --base https://acme.example --site "Acme"
python3 scripts/aeo.py sitemap ./site --base https://acme.example

# 5. Confirm
python3 scripts/aeo.py audit ./site
```

Pass `--dry-run` to any write command to preview without touching files.

## What each command does

| Command   | Effect                                                            |
|-----------|-------------------------------------------------------------------|
| `audit`   | Scores pages across 7 checks, lists the biggest wins.             |
| `schema`  | Injects Article/BlogPosting/NewsArticle JSON-LD before `</head>`. |
| `faq`     | Injects FAQPage JSON-LD from `Question::Answer` pairs.            |
| `md`      | Writes a clean `page.md` next to each `page.html`.                |
| `llms`    | Generates `llms.txt` mapping every page.                          |
| `sitemap` | Generates a standard `sitemap.xml`.                               |

## Why "AEO" and not just SEO

Classic SEO optimises for a ranked link a human clicks. Answer-engine
optimisation (AEO) optimises for being **quoted inside the generated answer**.
That rewards machine-readability: a self-contained claim, extractable headings,
structured data, a clean text surface, and a map the engine can fetch. This skill
automates the mechanical parts of that.

## Notes

- `schema` and `faq` edit your HTML in place; `md`, `llms` and `sitemap` write new
  files. Use `--dry-run` first if you want to look before you leap.
- Idempotent: re-running skips work already done (use `--force` to redo).
- After publishing, submit the new `sitemap.xml` / `llms.txt` and ping IndexNow or
  Search Console so engines re-crawl.

## Credit

Built by [Workloft](https://workloft.ai). It packages the exact approach Workloft
runs on its own [Labs](https://workloft.ai/labs/) and [Ships](https://workloft.ai/ships)
pages. Licensed MIT-0.
