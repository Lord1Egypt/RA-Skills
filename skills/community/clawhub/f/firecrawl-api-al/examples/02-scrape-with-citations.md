# Example 02 — Scrape Several URLs and Answer with Inline Citations

## User request

> "Compare how these three frameworks describe their streaming support. Here are the docs pages: https://a.example/docs/streaming , https://b.example/guide/stream , https://c.example/reference/streaming"

## Agent reasoning summary

- Three known URLs, comparative synthesis goal → scrape each page, then write a grounded comparison.
- Each claim in the answer must trace to a specific source, so I'll keep a numbered map of `sourceURL → [n]`.
- Dedup by resolved `sourceURL` in case two inputs redirect to the same canonical page.

## Firecrawl operation to use

`scrape` (synchronous), called once per URL. Three independent pages, no traversal needed, so three scrapes are cheaper and more predictable than a crawl. Cost: ~1 credit per page; sum the per-response `metadata.creditsUsed`. Each call is independent and can be issued in parallel.

## Request shape

One call per URL (parallelizable):

```json
POST https://api.firecrawl.dev/v2/scrape
Authorization: Bearer $FIRECRAWL_API_KEY

{ "url": "https://a.example/docs/streaming", "formats": ["markdown"], "onlyMainContent": true }
```

```json
{ "url": "https://b.example/guide/stream",      "formats": ["markdown"], "onlyMainContent": true }
{ "url": "https://c.example/reference/streaming","formats": ["markdown"], "onlyMainContent": true }
```

## Response handling

For each response:
1. Skip any with `success !== true` or non-2xx `metadata.statusCode`; note which inputs failed so the final answer can disclose gaps.
2. Build a citation table keyed by `metadata.sourceURL` (the resolved URL):

   | n | sourceURL | title |
   |---|-----------|-------|
   | 1 | https://a.example/docs/streaming | A streaming |
   | 2 | https://b.example/guide/stream   | B streaming |
   | 3 | https://c.example/reference/streaming | C streaming |

3. **Dedup by `sourceURL`**: if two inputs resolve to the same `sourceURL`, keep one citation number and don't double-count credits.
4. Synthesize only from the collected `markdown`. Attach the matching `[n]` to each factual sentence.
5. Sum `creditsUsed` across the surviving responses for the cost footer.

## Citation behavior

Every comparative claim carries an inline `[n]` whose number maps to a `metadata.sourceURL` in the sources list. Do not assert anything you can't pin to one of the scraped documents. If only two of three pages scraped successfully, say so and cite only the two.

## Final answer pattern

```
Streaming support, compared:

- Framework A streams token-by-token over SSE and requires no extra config [1].
- Framework B streams but needs an explicit `stream: true` flag [2].
- Framework C exposes a lower-level chunk iterator and leaves transport to the caller [3].

Bottom line: A is the most turnkey; C is the most flexible [1][3].

Sources
[1] A streaming — https://a.example/docs/streaming
[2] B streaming — https://b.example/guide/stream
[3] C streaming — https://c.example/reference/streaming

(3 pages scraped via Firecrawl, 3 credits total.)
```

## Common failure mode

Writing one merged paragraph with a single trailing "[1][2][3]" dump, or citing the user's pasted URLs instead of the resolved `sourceURL`s. The reader can't tell which framework's behavior came from which doc, and a redirected page yields a broken citation link.

## Improved version

- Attach `[n]` at the **claim** level, not the paragraph level.
- Key the citation table on resolved `metadata.sourceURL`, deduped.
- Explicitly disclose any URL that failed to scrape rather than silently dropping it:

```
Note: https://c.example/reference/streaming returned statusCode 403 and was excluded;
the comparison below covers A and B only.
```

This makes every sentence independently verifiable and makes coverage gaps honest.
