---
name: brand-mention-research
description: Build a sourced brand-mention and reputation brief from bounded Reddit, TikTok, and YouTube searches and comment samples through Crawlora. Use to resolve brand aliases, deduplicate mentions, compare discussion themes, or inspect a product issue with explicit sampling limits.
---

# Brand mention research

## Access and scope

Set `CRAWLORA_API_KEY` to your Crawlora key. Prefer the listed Crawlora MCP tools
when connected; otherwise use the bundled `scripts/crawlora.sh`, which sends
`x-api-key` to `https://api.crawlora.net/api/v1`. Read
[reference/endpoints.md](reference/endpoints.md) for exact methods and parameters.
Check application `code` as well as HTTP status; payloads are inside `data`.
Stop on authentication errors, back off on `429`, and retry a transient upstream
failure once. Bound pages and calls by the requested scope and credit budget.
Preserve source IDs, URLs, retrieval times, and source dates where supplied.

Produce a bounded mention brief for a brand, product, or campaign. Define the
entity and aliases, competitors when requested, date window, languages/markets,
platforms, and page budget before collecting. Common names need corroborating
product, domain, handle, or contextual evidence to avoid false matches. Start
with a small sample for each query. If broad Reddit or platform search results
are mostly unrelated, tighten the exact terms or select a relevant community;
do not treat returned-result counts as mention volume or continue paging through
a low-precision query.

## Collect and classify attributable mentions

- Search Reddit, TikTok, or YouTube according to the requested sources. Retain
  query/alias, filters, result order, pages/cursors, and retrieval time. Reddit's
  `time` filter applies to `top`/`comments` sorts; do not claim `sort=new time=week`
  enforces a week. TikTok has no date-filter argument here: filter returned dates
  locally and mark unknown dates rather than inventing a backend filter. YouTube
  uses its documented `upload_date` and locale/region fields.
- Resolve selected results into post/video detail. Canonical post IDs are the
  within-platform deduplication key. Cross-posted or quoted content can be linked
  as related observations, but identical text does not prove the same author.
- Fetch comments only for selected relevant posts. Preserve parent post, comment
  identity when available, ordering, and pagination. Keep comment counts/sample
  size separate from top-level post counts. Reddit's metrics mode costs more;
  request it only when engagement data is needed. Missing engagement remains unknown.
- Label each observation as a confirmed mention, ambiguous match, promotional
  mention, quotation, or excluded false positive with a reason. Interpret sentiment
  from available text/context; use mixed or unknown for sarcasm, missing content,
  or uncertain intent. Do not invent video dialogue from a caption alone.

```sh
scripts/crawlora.sh /reddit/search q="Crawlora" sort=top time=month limit=25
scripts/crawlora.sh /tiktok/search keyword="Crawlora" count=10
scripts/crawlora.sh /youtube/search q="Crawlora" type=video upload_date=this_month
# Resolve returned IDs before requesting selected details/comments:
# scripts/crawlora.sh "/reddit/comments/$POST_ID" limit=25
```

## Deliver a reproducible brief

Return a coverage ledger and evidence table with platform, source URL/ID,
publication time if available, alias/query, short excerpt, theme, sentiment,
and explicit selection reason. Show unique confirmed posts, excluded/ambiguous
matches, sampled comments, and denominators for each reported proportion.
Compare competitors only under equivalent windows and sampling budgets, and
still describe unequal platform/search coverage. Do not sum follower counts or
views into unique audience reach, infer market share from mention counts, or
call a sampled issue widespread without corroborating evidence. Repeated runs
need the same saved query/scope to support change claims. Do not contact authors,
post responses, or schedule monitoring unless the user requests those actions.
