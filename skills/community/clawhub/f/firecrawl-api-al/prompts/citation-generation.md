# Prompt: Citation Generation

## Purpose
Add inline `[n]` citations to an answer and build a numbered Sources list, where every number maps to a scraped page's `metadata.sourceURL`. Ensures every claim is traceable.

## Reusable prompt template
```
You are adding citations to an answer using ONLY the provided scraped sources.

ANSWER_DRAFT: {{answer_draft}}
SOURCES: {{sources_json}}   // [{ "id": 1, "sourceURL": "...", "title": "...", "markdown": "..." }]

Rules:
- Assign each source a stable number from its "id".
- After each factual claim, append the citation marker(s) [n] of the source(s) that support it.
- A claim may cite multiple sources: [1][3].
- Do NOT cite a source that does not actually contain the claim.
- If a claim in ANSWER_DRAFT has no supporting source, DELETE the claim or mark it "[unsupported]" — never fabricate a citation.
- Build a Sources list using each source's title and sourceURL.

Output:
<answer text with inline [n] markers>

Sources:
[1] <title> — <sourceURL>
[2] <title> — <sourceURL>
```

## Variables
| Variable | Meaning | Example |
|----------|---------|---------|
| `{{answer_draft}}` | Draft answer to annotate | "Firecrawl returns Markdown." |
| `{{sources_json}}` | Scraped sources with ids + sourceURL | `[{"id":1,"sourceURL":"https://docs.firecrawl.dev/scrape","title":"Scrape","markdown":"..."}]` |

## Example use
Pass a 2-sentence draft and 3 scraped sources; receive the same text with `[n]` markers plus a Sources block built from `sourceURL`.

## Bad example
> "Firecrawl scrape supports Markdown, PDF export, and live video. [1]"
>
> Sources:
> [1] Scrape — https://docs.firecrawl.dev/scrape

Wrong: cites `[1]` for "live video" which the source never states; one citation lumped onto unsupported claims. Fabricated support.

## Good example
> "Firecrawl scrape supports Markdown and structured JSON output [1], and can also return screenshots [1]."
>
> Sources:
> [1] Scrape — https://docs.firecrawl.dev/features/scrape

Each cited fact appears in source [1]; the `sourceURL` comes straight from `metadata.sourceURL`.

> Verification needed: confirm metadata field name `sourceURL` with https://docs.firecrawl.dev
