---
name: ai-newsletter-daily
description: >
  Generate a daily AI news newsletter for a Chinese audience from fresh web
  sources. Return the newsletter body and article summaries in Simplified
  Chinese.
version: 1.0.0
author: Jeff Yang (https://github.com/j3ffyang)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [AI, News, Newsletter]
    requires_toolsets: [web]
    requires_tools: [web_search, web_fetch]
    required_environment_variables:
      - name: BRAVE_API_KEY
        prompt: Enter your BRAVE API key
        help: Required for web search
        required_for: Web search
      - name: FIRECRAWL_API_KEY
        prompt: Enter your Firecrawl API key
        help: Required for web fetching
        required_for: Web fetching
---

# AI Newsletter Daily

## When to Use

Use for current AI/ML news, releases, research, funding, product launches, model updates, regulation, benchmarks, or practitioner-relevant developments.

Do not use for evergreen explainers, non-AI topics, or long-form research that is not meant to become a curated newsletter.

## Procedure

1. Resolve inputs.
   - Defaults: `target_news_count=20`, `search_query="latest AI news today"`, `search_time_window_days=2`, `max_search_results=60`, `min_articles_required=10`, `include_domains=[]`, `exclude_domains=["youtube.com","reddit.com","facebook.com","x.com","twitter.com"]`, `summary_model="host-default"`, `max_scrape_retries=2`.
   - Clamp: `target_news_count 1..50`, `search_time_window_days 1..14`, `max_search_results 20..120`, `min_articles_required 1..50`, `max_scrape_retries 0..5`.
   - If `min_articles_required > target_news_count`, set it to `target_news_count`.

2. Search and filter.
   - Run `web_search` with `search_query`.
   - If no usable results, retry once with `"{search_query} generative AI LLM model open source enterprise"`.
   - Keep only results with non-empty title and URL.
   - Canonicalize URLs, drop duplicates, apply domain filters, and prefer fresh results.

3. Rank.
   - Score 0..100 from AI-topic relevance, freshness, and title/snippet quality.
   - Sort by score desc, published date desc, URL asc.
   - Keep top `target_news_count * 2` candidates.

4. Fetch, verify, summarize.
   - Process candidates in order until `target_news_count` verified items are collected.
   - Skip already processed canonical URLs.
   - Fetch each candidate up to `max_scrape_retries + 1` times with `web_fetch`.
   - Verify title, domain, topic, and date against the search result.
   - Skip inconsistent pages and record a warning.
   - Summarize each accepted article in one plain-text paragraph, max ~80 words, focused on why it matters to AI practitioners.

5. Fallback.
   - If collected items are fewer than `min_articles_required`, run one fallback search with `"AI news today machine learning model release funding research"`.
   - Process only new candidates and repeat the same filter/rank/fetch/verify/summarize flow.

6. Finalize.
   - Keep only valid items with non-empty `title`, `url`, `domain`, `summary`, `source_query`, and numeric `relevance_score`.
   - Remove duplicates by canonical URL.
   - Sort by score desc, then published date desc.
   - Truncate to `target_news_count`.
   - Return `newsletter_items`, `markdown_newsletter`, and `json_newsletter`.

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

## Language Output

Return the newsletter body and all article summaries in Simplified Chinese. Preserve all source metadata unchanged (`title`, `url`, `domain`, `published_at`, `relevance_score`, `source_query`).
