# Prompt: Target Planning (scrape vs crawl vs map vs search)

## Purpose
Decide which Firecrawl operation to use for a task, and define scope (paths, limits, formats) BEFORE spending any credits. Prevents the most common waste: crawling when a single scrape would do, or scraping when only a URL list is needed.

## Reusable prompt template
```
You are planning a Firecrawl data-retrieval task. Choose exactly one primary
operation and define its scope. Do not write code; output a plan.

TASK: {{task_description}}
KNOWN_URLS: {{known_urls_or_none}}
NEED: {{content | url_list_only | structured_fields | answer_to_question}}
EXPECTED_SCALE: {{one_page | a_few_pages | a_section | whole_site}}
BUDGET_HINT: {{max_credits_or_pages_if_any}}

Decision rules (apply in order):
1. If NEED is "answer_to_question" and KNOWN_URLS is none -> use SEARCH (then scrape selected results).
2. If NEED is "url_list_only" -> use MAP (cheapest; returns links only).
3. If KNOWN_URLS has exactly one (or few) URLs and NEED is content/fields -> use SCRAPE per URL.
4. If you must DISCOVER many pages under a root and NEED their content -> use CRAWL (async; always set limit).
5. For structured_fields -> use SCRAPE with the json format (prompt+schema).

Output the plan as:
- Operation: <scrape|crawl|map|search>
- Reason: <one sentence tied to the rules>
- Scope: { url(s), includePaths, excludePaths, limit }
- Formats: <markdown | json | other; justify any extra format>
- Estimated cost: <credits or "pages x ~1 credit; confirm via creditsUsed">
- Async?: <yes only for crawl; note polling required>
```

## Variables
| Variable | Meaning | Example |
|----------|---------|---------|
| `{{task_description}}` | What the user wants | "Get all guide pages from docs.example.com" |
| `{{known_urls_or_none}}` | URLs already in hand | "https://example.com/a" or "none" |
| `{{NEED}}` | Output type required | "content" |
| `{{EXPECTED_SCALE}}` | Rough page count | "a_section" |
| `{{BUDGET_HINT}}` | Cost ceiling if any | "<= 50 pages" |

## Example use
Fill the template for: "Summarize the Firecrawl blog post at URL X." → KNOWN_URLS = X, NEED = content, scale = one_page.

## Bad example
> "I'll crawl the whole site to be safe and then find the page I need."

Wrong: crawling an entire site to read one known URL wastes many credits and is async/slow. Rule 3 says use a single `scrape`.

## Good example
> Operation: scrape
> Reason: exactly one known URL and we need its content (rule 3).
> Scope: { url: "https://example.com/blog/post-x" }
> Formats: markdown (no extra formats needed).
> Estimated cost: ~1 credit; confirm via creditsUsed.
> Async?: no.

> Verification needed: confirm operation semantics with https://docs.firecrawl.dev
