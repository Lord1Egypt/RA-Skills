---
name: cross-corpus-research
description: Run bounded research across Crawlora public-web, paper, and indexed developer-document sources, retaining source snapshots, evidence, and partial-coverage warnings. Use for focused cited briefs or structured research jobs, not exhaustive web coverage.
---

# Cross-corpus research

Use this skill when a question needs an evidence brief across more than one
public source type, a durable research job, or a bounded inventory of one site.
Choose the smallest source scope and credit budget that can answer the question.

## Access and source readiness

Set `CRAWLORA_API_KEY`. Use the bundled `scripts/crawlora.sh`, which sends it in
an `x-api-key` header to `https://api.crawlora.net/api/v1`; do not place the key
in a URL, shell argument, example, or report. Check both HTTP status and the
application `code`. Stop on authentication errors, back off on `429`, and retry
a transient upstream failure once. Successful calls may consume credits.

Before selecting sources, inspect the live registries and capabilities when the
request depends on source availability:

- `/research/sources` lists paper operations and the current registry revision.
  Paper keyword search is arXiv-based. Europe PMC adds MED-backed metadata,
  licensed full-text reads, and one-hop citation operations; it is not a
  universal paper search index.
- `/developer/sources` lists indexed documentation sources, supported filters,
  and index state. `/developer/search` searches only the index and never starts
  ingestion or contacts upstream sites. The source set can be narrow (the
  current ready source is Go documentation), so check before promising coverage.
- `/web/capabilities` reports which retrieval operations and limits are
  enabled for the current account.

## Run a durable research job

1. Frame one answerable query, the requested date/market, source preferences,
   and a credit ceiling. Choose `scope=web`, `papers`, `developer`, or `mixed`;
   `sources` can further restrict the registered source IDs. `seed_urls`,
   `include_domains`, and `exclude_domains` apply only to `web` or `mixed` jobs.
2. Submit `POST /research/jobs` with a 16–128 character `idempotency_key`, the
   query, and `limits.max_credits`. Bound `rounds`, `searches`, `sources`, and
   timeout for the task. Browser renders are fixed at zero. Reuse the same key
   and identical request after an uncertain submission; use a new key only for
   a materially changed investigation. A JSON output requires a strict object
   schema; otherwise use the report output.
3. Keep the returned `job_id`. Check `/research/jobs/{job_id}` for state,
   progress, warnings, and usage. Read `/research/jobs/{job_id}/events` with its
   `next_cursor` when the audit trail matters. A queued job can wait up to 30
   minutes before it times out without charge.
4. Read `/research/jobs/{job_id}/results` until a terminal state and a validated
   result are available. `ready:false`, `partial:true`, or any source warning
   must remain visible in the answer. Do not fill missing sources with guesses
   or describe retained evidence as a completed report.
5. Preserve `source_snapshot` revisions, result kind, source URLs, source dates,
   retrieval times, and usage. Search snippets are discovery leads, not citable
   evidence. A claim is `supported` only when its full text exactly quotes a
   retained passage; citation IDs alone do not establish support. Keep
   `conflicting` and `unverified` claims explicit.

```sh
scripts/crawlora.sh /research/sources
scripts/crawlora.sh /developer/sources
scripts/crawlora.sh /web/capabilities
scripts/crawlora.sh -X POST /research/jobs '{"idempotency_key":"brief-20261019-001","query":"Compare recent evidence on public EV charging reliability","scope":"mixed","output_format":"report","limits":{"max_credits":40,"rounds":2,"searches":4,"sources":8,"timeout_seconds":180}}'
# Use the returned job ID; this placeholder is for route shape only.
scripts/crawlora.sh /research/jobs/job-example123 | jq '.'
scripts/crawlora.sh /research/jobs/job-example123/results | jq '.'
```

## Read papers and indexed documentation directly

- Search papers with `/research/papers/search`, then inspect returned stable IDs
  with `/research/papers/metadata`. The arXiv search result window is frozen for
  cursor continuation; preserve the source and coverage warnings.
- Use `/research/papers/read` with a specific question. Europe PMC full text is
  returned only when the article license permits it; restricted records remain
  metadata-only. arXiv PDFs are not fetched. Keep passage locators, license,
  provenance, and exact source URLs with any extracted evidence.
- `/research/papers/related` returns one-hop Europe PMC references or citers.
  It is a bounded indexed graph, not a complete bibliography or a multi-hop
  literature review. Alias or seed failures and partial lists remain visible.
- For developer docs, call `/developer/search` only after selecting a source
  reported ready by `/developer/sources`. A search hit is indexed content, not a
  statement that the documentation is current for every software version.

## Map or crawl one site

Use `/web/search` for a bounded public-web discovery sample. Use `/web/map` when
the user needs an approximate URL inventory; it follows public sitemaps and
seed-page links, defaults to the seed host, and freezes its cursor snapshot for
30 minutes. It is not a complete site census.

Use `/web/crawl` for a bounded, resumable page crawl. Supply a stable
`idempotency_key`, the seed URL, and `limits.max_credits`; set reasonable page,
depth, byte, and timeout limits. Poll its status and read results until drained
or terminal. Failed/skipped URLs count toward the admitted page limit. Browser
rendering is not available on this job path; do not promise JavaScript-rendered
coverage. Preserve `partial`, warnings, stop reason, and accounting.

```sh
scripts/crawlora.sh -X POST /web/search '{"q":"site:example.org API rate limit","include_domains":["example.org"],"limit":5}'
scripts/crawlora.sh -X POST /web/map '{"url":"https://example.org/docs/","scope":{"include_paths":["/docs/**"]},"max_urls":100,"page_size":50}'
scripts/crawlora.sh -X POST /web/crawl '{"idempotency_key":"crawl-example-20261019","url":"https://example.org/docs/","scope":{"include_paths":["/docs/**"]},"limits":{"max_credits":20,"max_pages":10,"max_depth":1}}'
```

Return a concise finding summary with claim-level citations, source and query
scope, dates, successful and failed sources, and a clear stopping/coverage
statement. Do not imply exhaustive research, browser rendering, future
monitoring, or independent verification beyond the retained evidence. Do not
publish, contact sources, or create recurring jobs unless requested.
