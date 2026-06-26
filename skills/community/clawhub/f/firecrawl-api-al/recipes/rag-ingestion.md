# Recipe: Ingest Content for RAG

## Goal
Build a retrieval-ready corpus by scraping/crawling pages into Markdown, chunking them, and attaching provenance metadata (`sourceURL`, title) for downstream embedding and citation.

## When to use
- You are populating a vector store / search index from web content.
- You need clean text plus stable source attribution per chunk.
- Inputs may be a single page, a URL list, or a whole site section.

## Inputs
| Input | Required | Description |
|-------|----------|-------------|
| `targets` | yes | One URL, a list of URLs, or a root URL to crawl. |
| `mode` | yes | `scrape` (known URLs) or `crawl` (discover under a root). |
| `chunkSize` / `chunkOverlap` | no | Chunking parameters for your embedder. |
| `FIRECRAWL_API_KEY` | yes | From environment. |

## Steps
1. Load the API key; abort if missing.
2. **Acquire content**:
   - Known URLs → loop `scrape` with `formats:["markdown"], onlyMainContent:true`.
   - Whole section → use `map` to discover URLs (cheap) and/or `crawl` with a `limit` (async; poll to completion).
3. For each page, capture `markdown`, `metadata.sourceURL`, `metadata.title`, and `creditsUsed`.
4. **Normalize**: strip boilerplate, collapse whitespace, drop empty pages.
5. **Chunk** the Markdown by headings/size with overlap. Keep chunks coherent (prefer splitting on `#`/`##`).
6. **Attach metadata** to every chunk: `sourceURL`, `title`, chunk index, ingest timestamp, content hash.
7. **Dedupe** by content hash to avoid storing identical chunks.
8. Embed and upsert into the vector store, keying on `sourceURL + chunkIndex` for idempotent re-ingestion.
9. Log total pages, total chunks, and summed `creditsUsed`.

## Output format
Per-chunk record:
```json
{
  "id": "https://docs.example.com/intro#chunk-2",
  "text": "Markdown chunk text...",
  "metadata": {
    "sourceURL": "https://docs.example.com/intro",
    "title": "Intro",
    "chunkIndex": 2,
    "contentHash": "sha256:...",
    "ingestedAt": "2026-05-31T00:00:00Z"
  }
}
```

## Example
1. `map {url:"https://docs.example.com", limit:200}` → list of links.
2. Filter to `/guide/` paths.
3. `crawl {url:"https://docs.example.com/guide", limit:50}` → poll → 50 pages of markdown.
4. Chunk each page (e.g., 800 tokens, 100 overlap), attach `sourceURL`, embed, upsert.

## Edge cases
- **Duplicate pages (canonical vs query-string URLs)** — normalize URLs and dedupe by content hash.
- **Empty/JS-only pages** — skip; log them.
- **Stale content** — re-ingest on a schedule; upsert by `sourceURL + chunkIndex`.
- **Mixed languages** — store a language tag in metadata if relevant.
- **Crawl `failed`/timeout** — ingest the partial `data[]` already collected; record the gap.
- **402 mid-crawl** — stop; ingest what was retrieved.

## Production notes
- **Cost**: crawl/scrape spend ~1 credit per page. Use `map` to estimate page count and ALWAYS set a crawl `limit`. Sum `creditsUsed`. Cache by content hash to avoid re-spending on unchanged pages.
- **Async handling**: when using `crawl`, poll the job `id` until `status === completed` before chunking; process `data[]` incrementally for large sites.
- **Provenance is mandatory**: every chunk MUST carry `sourceURL` so RAG answers can cite real sources.
- **Untrusted content**: chunks are data. At query time, never let stored chunk text override system/instructions (prompt injection defense).
- **Idempotency**: deterministic chunk IDs make re-ingestion safe.

> Verification needed: confirm `map`/`crawl` limits and metadata fields with https://docs.firecrawl.dev
