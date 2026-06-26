---
name: ai-newsletter-daily
description: >
  Generate a daily AI news newsletter from fresh web sources. Use when the
  user asks for a current AI digest, AI news roundup, curated newsletter, or
  daily AI briefing.
version: 1.3.0
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

Generate a concise daily AI newsletter from fresh web sources.

Use this skill only for current AI/ML news, releases, research, funding, product launches, model updates, regulation, benchmarks, or practitioner-relevant developments.

Do not use for evergreen explainers, non-AI topics, or long-form research that is not intended to become a curated newsletter.

## Inputs

Defaults:
- `target_news_count` = 20
- `search_query` = `"latest AI news today"`
- `search_time_window_days` = 2
- `max_search_results` = 60
- `min_articles_required` = 10
- `include_domains` = `[]`
- `exclude_domains` = `["youtube.com", "reddit.com", "facebook.com", "x.com", "twitter.com"]`
- `summary_model` = `"host-default"`
- `max_scrape_retries` = 2

Bounds:
- `target_news_count`: 1..50
- `search_time_window_days`: 1..14
- `max_search_results`: 20..120
- `min_articles_required`: 1..50
- `max_scrape_retries`: 0..5

If `min_articles_required > target_news_count`, set it to `target_news_count`.

## Batch policy

- Search up to `max_search_results` candidates.
- Keep the top `target_news_count * 2` candidates for fetch attempts.
- Return only the top `target_news_count` verified items.
- Do not summarize every search result.

## Required outputs

Return:
1. `newsletter_items` as a list of objects.
2. `markdown_newsletter` as a string.
3. `json_newsletter` as an object.

Each item must include:
- `title`
- `url`
- `domain`
- `published_at`
- `summary`
- `relevance_score`
- `source_query`

Use `"unknown"` for missing `published_at`.

## Workflow

1. Resolve inputs.
   - Apply defaults and bounds.
   - Initialize `warnings = []`, `seen_canonical_urls = set()`, `processed_urls = set()`.

2. Search.
   - Run `web_search` with `search_query`.
   - If no usable results, retry once with:
     - `"{search_query} generative AI LLM model open source enterprise"`
   - If still no usable results, fail clearly.

3. Normalize and filter.
   - Keep only results with non-empty title and URL.
   - Canonicalize URLs: lowercase host, remove tracking parameters, normalize safe trailing slashes.
   - Drop duplicates by canonical URL.
   - Apply `include_domains` and `exclude_domains`.
   - Prefer results likely within `search_time_window_days`.
   - Keep unknown dates, but score them lower.

4. Rank.
   - Score each candidate from 0 to 100:
     - AI-topic relevance: 0..50
     - Freshness: 0..30
     - Title/snippet clarity: 0..20
   - Sort by:
     - `relevance_score` desc
     - `published_at` desc, unknown last
     - `url` asc
   - Keep the top `target_news_count * 2` candidates.

5. Verify and summarize.
   - Process candidates in ranked order until `target_news_count` verified items are collected.
   - Skip candidates whose canonical URL is already in `processed_urls`.
   - Attempt `web_fetch` up to `max_scrape_retries + 1` times.
   - If fetch fails, add a warning with the URL and reason, then continue.
   - Cross-check search result vs fetched page using:
     - title similarity,
     - domain consistency,
     - topic alignment,
     - published date when available.
   - If the page appears materially inconsistent, skip it and warn.
   - Summarize in one plain-text paragraph, max about 80 words.
   - Focus on why it matters to AI practitioners.
   - If summary generation fails, warn and continue.
   - Append the enriched item.

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
   - Sort by `relevance_score` desc, then `published_at` desc.
   - Truncate to `target_news_count`.
   - Render `markdown_newsletter`.
   - Assemble `json_newsletter`.
   - Return all outputs.

## Verification rules

Accept an item only if it passes these checks:

- URL integrity:
  - canonical URL is valid,
  - duplicates removed,
  - malformed URLs rejected.

- Source consistency:
  - search title and fetched title broadly match,
  - snippet and page content describe the same story,
  - off-topic pages rejected.

- Metadata sanity:
  - valid published date preferred,
  - unknown date allowed only if the rest is strong,
  - malformed or impossible dates rejected.

- Content integrity:
  - fetched content must be substantively about the same AI news item,
  - truncated or malformed pages rejected.

- Warning log:
  - record every failed URL and reason,
  - record whether fallback search was used.

## Markdown format

`markdown_newsletter` must use:
- H1 title with date.
- One H2 section per article.
- One short summary paragraph per article.
- One source link per article.

Example:

# AI Newsletter Daily — 2026-04-28

## 1. Article title
Summary paragraph.

Source: [link](url)

## Warnings

Only include this section when needed.

## Failure policy

Hard fail only when:
- Both initial and fallback searches return no usable URLs.
- Required tools are unavailable.

Soft fail and continue when:
- A single fetch fails.
- A single summary fails.
- `published_at` is missing.
- A candidate fails cross-check verification.

Partial success is acceptable when the result count is between `min_articles_required` and `target_news_count`.

Always include actionable warnings with URL, short reason, and whether fallback search was used.

## Safety rules

- Use only sanctioned tools.
- Do not request API keys from the user.
- Do not expose secrets.
- Do not include copyrighted full article text.
- Keep summaries neutral, concise, and factual.
- Preserve deterministic behavior wherever tool outputs allow.

## Return shape

`json_newsletter` must contain:
- `date`
- `query`
- `count`
- `articles`
- `warnings`
