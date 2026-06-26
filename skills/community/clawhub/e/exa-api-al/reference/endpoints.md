# Exa Endpoints Reference

Base URL: `https://api.exa.ai`. Auth header on every request:
`x-api-key: <EXA_API_KEY>`. Every response includes `costDollars`.

> Cost note: keyword/fast search is cheaper than neural; requesting contents
> (text/highlights/summary) and `livecrawl` add cost. Exact dollar amounts vary.
> Verification needed: confirm current pricing with https://docs.exa.ai.

---

## search — `POST /search`

**Purpose:** Find relevant web pages for a query, by neural meaning, keyword, or
a fast/auto blend.

**Key params:** `query` (required), `type` (`auto|neural|keyword|fast`),
`category`, `numResults`, `includeDomains[]`, `excludeDomains[]`,
`startPublishedDate`, `endPublishedDate` (ISO 8601), optional inline
`contents:{text,highlights,summary,livecrawl}`.

**Response shape:**
```
{
  requestId,
  resolvedSearchType,
  results: [ { id, title, url, publishedDate, author, score, text?, highlights?, summary? } ],
  searchTime,
  costDollars
}
```
`id` equals `url`. `score` is 0–1 (relevance).

**Cost note:** lowest with `keyword`/`fast` and no inline contents; grows with
`neural`, larger `numResults`, and requested contents.

---

## contents — `POST /contents`

**Purpose:** Retrieve clean page content for known URLs.

**Key params:** `urls[]` (required), and any of `text`, `highlights`, `summary`;
optional `livecrawl` for fresh (non-cached) fetches.

**Response shape:** results keyed by URL, each with the requested `text`,
`highlights`, and/or `summary` fields, plus `costDollars`.

**Cost note:** `summary` < `highlights` < full `text`; `livecrawl` adds latency
and cost. Batch URLs in one call.

---

## findSimilar — `POST /findSimilar`

**Purpose:** Find pages semantically similar to a reference URL.

**Key params:** `url` (required), `numResults`; optional domain/date filters.

**Response shape:** `results[]` with the same fields as `search` results
(`id`, `title`, `url`, `publishedDate`, `author`, `score`, optional contents),
plus `costDollars`.

**Cost note:** similar to neural search; keep `numResults` small and avoid inline
contents unless needed.

---

## answer — `POST /answer`

**Purpose:** Produce a short, cited answer to a question, grounded in live
sources.

**Key params:** `query` (required), `text` (boolean; include supporting source
text).

**Response shape:**
```
{ answer, citations: [ { id, title, url, text? } ], costDollars }
```

**Cost note:** runs retrieval internally; cost depends on sources used and
whether `text` is requested.

---

## research — `POST /research` (beta)

**Purpose:** Run a multi-step research task over the web and return a synthesized
result.

**Status:** Beta. Treat output as preliminary and re-verify key claims.

> Verification needed: confirm exact request/response schema, parameters, and
> tool name for `research` with https://docs.exa.ai before relying on it.
