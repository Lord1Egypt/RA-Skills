# Example 06 — RAG Ingestion: Crawl/Scrape into Grounded, Cited Context

## User request

> "Ingest our help center at https://help.example.com and then answer support questions using only that content — no guessing. First question: 'How do I rotate my API key?'"

## Agent reasoning summary

- Build a retrievable corpus from the site, then answer strictly from retrieved chunks → crawl to ingest, scrape for one-offs.
- Clean markdown with `onlyMainContent` is ideal RAG input: less boilerplate, better chunk quality.
- Ground every sentence in retrieved chunks and cite their `sourceURL`; if retrieval returns nothing relevant, say so instead of hallucinating.

## Firecrawl operation to use

- **Ingestion**: `crawl` (async) over the help center to collect many pages as markdown. Bound with `limit` + `includePaths`; cost scales per page (see Example 04 for the polling/pagination mechanics).
- **Targeted top-up**: `scrape` (sync) for a single page you discover you're missing.

Markdown output is the key choice — it preserves headings and lists that make clean chunk boundaries, and strips nav/ads that pollute embeddings.

## Request shape

Crawl to ingest:

```json
POST https://api.firecrawl.dev/v2/crawl
Authorization: Bearer $FIRECRAWL_API_KEY

{
  "url": "https://help.example.com",
  "limit": 200,
  "includePaths": ["^/articles/.*", "^/faq/.*"],
  "scrapeOptions": { "formats": ["markdown"], "onlyMainContent": true }
}
```

Poll to completion and collect all `data` (paginate via `next`), as in Example 04.

## Response handling

For each completed document `{ markdown, metadata: { sourceURL, statusCode } }`:
1. Drop non-2xx pages and empty markdown.
2. **Dedup by `sourceURL`**.
3. **Chunk** the markdown: split on headings, then cap chunk size (e.g. ~800–1200 tokens) with small overlap. Keep heading context in each chunk.
4. Attach metadata to every chunk: `{ text, sourceURL, title, headingPath }`. The `sourceURL` is the citation anchor that survives into the answer.
5. Index chunks (embeddings / keyword) for retrieval.

At query time ("How do I rotate my API key?"):
6. Retrieve top-k chunks.
7. **Relevance gate**: if no chunk clears a minimum relevance bar, answer "I couldn't find this in the help center" — do **not** fall back to general knowledge.
8. Generate the answer using only the retrieved chunk text, attaching each chunk's `sourceURL` as a citation.

## Citation behavior

Each answer sentence cites the `sourceURL` of the chunk(s) it was generated from. Because chunks carry their source metadata from ingestion, citations are exact and verifiable. Never cite a page that wasn't actually retrieved for this query.

## Final answer pattern

```
To rotate your API key:

1. Open Settings -> API Keys [1].
2. Click "Rotate" next to the active key; the old key stays valid for 24h [1].
3. Update the key in your integrations before the grace period ends [2].

Sources
[1] Rotating API keys — https://help.example.com/articles/rotate-api-key
[2] Migrating integrations — https://help.example.com/articles/update-integrations

(Answer grounded in retrieved help-center content only.)
```

If retrieval finds nothing relevant:

```
I couldn't find anything about rotating API keys in the ingested help center.
I won't guess. Want me to scrape a specific page or broaden the crawl?
```

## Common failure mode

The model blends retrieved content with its own training-data guesses (hallucination), or chunks lose their `sourceURL` during ingestion so citations are missing/wrong. Worst case: confidently citing a help-center URL that doesn't actually contain the claimed steps. Also: ingesting full HTML/boilerplate instead of `onlyMainContent` markdown, which dilutes retrieval quality.

## Improved version

```
INGEST:
  crawl (markdown, onlyMainContent) -> dedup by sourceURL -> drop empties/non-2xx
  -> chunk on headings with overlap -> store {text, sourceURL, title, headingPath}

ANSWER:
  retrieve top-k -> relevance gate
     if nothing passes: say "not found", offer to scrape more (NO general-knowledge fallback)
     else: generate using ONLY retrieved chunk text; cite each chunk's sourceURL
  refuse any claim not supported by a retrieved chunk
```

This produces answers that are fully grounded, precisely cited, and explicitly admit ignorance instead of fabricating.
