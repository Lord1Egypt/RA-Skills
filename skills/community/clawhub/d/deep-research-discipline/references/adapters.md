# Optional adapters

Read this only if you want richer coverage than the required search/fetch pair. Nothing here is required for the workflow to run.

## Abstract interface

Any tool that satisfies these shapes can be used. Map your environment's tools to them; do not change the shapes.

```
search(query, {recency?, site?, language?}) -> [
  { title, url, snippet, published_at? }
]

fetch(url) -> {
  text, published_at?, author?, is_primary?
}

extract_document(file_or_url) -> { text, page_count?, tables? }

list_social(topic, {platform?, date_range?}) -> [
  { platform, text, url, posted_at, engagement? }
]
```

## Mapping guidance

- If your search tool returns answer summaries instead of result lists, treat the summary as a lead only and fetch the cited URLs.
- If your fetch tool returns raw HTML, strip navigation before quoting.
- If a tool requires credentials, that is an environment capability, not a workflow requirement — record it as `social=no` when absent.
- If two tools serve the same shape, prefer the one with explicit publication dates.

## Degradation table

| Missing capability | Effect on the report |
|---|---|
| recency filter | state that time-bounded freshness is not guaranteed |
| document extraction | mark documents as unread; summarize only from accessible text |
| social sources | state that community sentiment is not covered |
| code execution | report only figures stated by sources; do not compute derived numbers |

## What not to put here

- Vendor names, install commands, local filesystem paths, or account setup.
- “Recommended tool” claims. This file describes shapes, not products.
