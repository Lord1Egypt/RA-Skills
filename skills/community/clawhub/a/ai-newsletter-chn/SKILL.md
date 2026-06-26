---
name: ai-newsletter-daily
description: >
  Generate a daily AI news newsletter for a Chinese audience from fresh web
  sources, summarizing current AI/ML articles into Markdown and JSON with
  Simplified Chinese output.
version: 1.2.1
author: Jeff Yang (https://github.com/j3ffyang)
user-invocable: true
category: content
license: MIT
metadata:
  openclaw:
    skillKey: ai-newsletter-daily
    emoji: "🗞️"
    required-tools:
      - web_search
      - web_fetch
    requires:
      env:
        - BRAVE_API_KEY
        - FIRECRAWL_API_KEY
    commands:
      - name: ai-newsletter
        description: Generate a daily AI news digest in Markdown and JSON.
        arg-mode: raw
---

# AI Newsletter Daily

Generate a concise daily AI newsletter for a Chinese audience from fresh web sources.

Use this skill only when the request is about current AI/ML news, releases, research, funding, product launches, model updates, regulation, benchmarks, or practitioner-relevant developments.

Do not use this skill for:
- Evergreen explainers.
- Non-AI topics.
- Long-form research that is not intended to become a curated newsletter.

## Inputs

Expected inputs, with defaults if missing:
- `target_news_count` = 20
- `search_query` = `"latest AI news today"`
- `search_time_window_days` = 2
- `max_search_results` = 60
- `min_articles_required` = 10
- `include_domains` = `[]`
- `exclude_domains` = `["youtube.com", "reddit.com", "facebook.com", "x.com", "twitter.com"]`
- `summary_model` = `"host-default"`
- `max_scrape_retries` = 2

Rules:
- Clamp `target_news_count` to 1..50.
- Clamp `search_time_window_days` to 1..14.
- Clamp `max_search_results` to 20..120.
- Clamp `min_articles_required` to 1..50.
- Clamp `max_scrape_retries` to 0..5.
- If `min_articles_required > target_news_count`, set `min_articles_required = target_news_count`.

## Batch policy

Use a two-stage batch limit:

- Search batch: collect up to `max_search_results` candidates from search.
- Scrape batch: keep the top `target_news_count * 2` ranked candidates for fetch and summary attempts.
- Final batch: return only the top `target_news_count` verified items.

Do not summarize every search result. Over-collect, filter, verify, then reduce to the final batch.

## Required outputs

Return all of the following:

1. `newsletter_items` as a list of objects.
2. `markdown_newsletter` as a string.
3. `json_newsletter` as an object.

Each newsletter item must include:
- `title`
- `url`
- `domain`
- `published_at`
- `summary`
- `relevance_score`
- `source_query`

Use `"unknown"` for `published_at` when no date is available.

## Deterministic workflow

1. Resolve inputs.
   - Apply defaults and bounds.
   - Initialize `warnings = []`.
   - Initialize `seen_canonical_urls = set()`.
   - Initialize `processed_urls = set()`.

2. Search.
   - Run `web_search` with `search_query`.
   - If there are no usable results, retry once with:
     - `"{search_query} generative AI LLM model open source enterprise"`
   - If there are still no usable results, fail with a clear message.

3. Normalize and filter.
   - Keep only results with non-empty title and URL.
   - Canonicalize URLs by lowering the host, removing tracking parameters when possible, and normalizing safe trailing slashes.
   - Drop duplicates by canonical URL.
   - Apply `include_domains` and `exclude_domains`.
   - Prefer results likely within `search_time_window_days`.
   - Keep unknown dates, but score them lower.

4. Rank.
   - Score each candidate from 0 to 100:
     - AI-topic relevance: 0..50.
     - Freshness: 0..30.
     - Title/snippet clarity: 0..20.
   - Sort by:
     - `relevance_score` descending
     - `published_at` descending, unknown last
     - `url` ascending
   - Keep the top `target_news_count * 2` candidates.

5. Verify and summarize.
   - Process candidates in ranked order until `target_news_count` verified items are collected.
   - Skip candidates whose canonical URL is already in `processed_urls`.
   - Attempt `web_fetch` up to `max_scrape_retries + 1` times.
   - If fetch fails, add a warning with the URL and reason, then continue.
   - Cross-check search result vs fetched page using title similarity, domain consistency, topic alignment, and published date when available.
   - If the page appears materially inconsistent, skip it and warn.
   - Summarize each accepted article in one short plain-text paragraph, max about 80 words, focused on why it matters to AI practitioners.

6. Minimum quality gate.
   - If collected items are fewer than `min_articles_required`, run one fallback search with:
     - `"AI news today machine learning model release funding research"`
   - Process only new candidates not already seen or processed.
   - Repeat filtering, ranking, verification, and summarization.

7. Final integrity check.
   - Ensure every final item has non-empty `title`, `url`, `domain`, `summary`, `source_query`, and numeric `relevance_score`.
   - Ensure each URL appears once.
   - Ensure `markdown_newsletter` and `json_newsletter` match in item count.
   - Remove and warn on any invalid item.

8. Finalize.
   - Sort by `relevance_score` descending, then `published_at` descending.
   - Truncate to `target_news_count`.
   - Render `markdown_newsletter`.
   - Assemble `json_newsletter`.
   - Apply the language output rule below.
   - Return all outputs.

## Language output

- Translate the final `markdown_newsletter` body and each article `summary` in `newsletter_items` into Simplified Chinese.
- Keep `title`, `url`, `domain`, `published_at`, `relevance_score`, and `source_query` unchanged.
- If a source title is already in Chinese, preserve it as-is.
- Do not add extra commentary outside the newsletter content.

## Verification

Accept items only if:
- URL is valid and canonicalized.
- Search result and fetched page broadly match.
- Topic is actually AI/news relevant.
- Published date is present or safely unknown.
- Fetched content is not malformed or off-topic.

Record warnings for failed URLs, short reasons, and whether fallback search was used.

## Output Format

`markdown_newsletter`:
- H1 title with date.
- One H2 per article.
- One short summary paragraph per article.
- One source link per article.

`json_newsletter`:
- `date`
- `query`
- `count`
- `articles`
- `warnings`

## Safety rules

- Use only sanctioned tools.
- Do not request API keys from the user.
- Do not expose secrets.
- Do not include copyrighted full article text.
- Keep summaries neutral, concise, and factual.
- Preserve deterministic behavior wherever tool outputs allow.
