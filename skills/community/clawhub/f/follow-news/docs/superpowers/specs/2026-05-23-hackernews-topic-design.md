# Hacker News Topic Design

## Goal

Add a first-class `hackernews` topic so Hacker News stories appear only in a dedicated Hacker News section instead of being mixed into `frontier-tech`.

The default digest should keep Hacker News visible as its own topic, preserve HN-specific context such as score and comment count, and avoid duplicate rendering in generic topic sections or fixed fallback sections.

## Current Behavior

The default Hacker News source is `hn-rss` in `config/defaults/sources.json`.

It currently uses:

```json
"topics": ["frontier-tech"]
```

During merge, articles are grouped by their configured topics. Because `hn-rss` only declares `frontier-tech`, Hacker News stories are assigned to `frontier-tech` and rendered under `Tech Industry / 产业动态`.

The renderer also has fixed Hacker News section logic, but topic sections render first and register visible articles. By the time the fixed Hacker News section runs, those HN stories have already been marked visible and are filtered as duplicates.

## Proposed Approach

Use the existing config-driven topic model.

1. Add a default topic with id `hackernews`.
2. Change `hn-rss.topics` from `["frontier-tech"]` to `["hackernews"]`.
3. Render `hackernews` as a normal topic section, with HN-specific metadata display.
4. Keep the fixed Hacker News renderer as a compatibility fallback for old merged fixtures or custom configs, but do not duplicate articles already rendered by the `hackernews` topic.

This keeps routing explicit in config instead of hiding source-specific behavior inside merge code.

## Topic Definition

Add this topic to `config/defaults/topics.json`:

```json
{
  "id": "hackernews",
  "emoji": "📰",
  "label": "Hacker News / 热榜",
  "description": "Top stories from Hacker News frontpage with HN score, comments, and discussion links",
  "search": {
    "queries": [],
    "twitter_queries": [],
    "must_include": [],
    "exclude": []
  },
  "display": {
    "max_items": 10,
    "style": "compact"
  }
}
```

Place it before `frontier-tech` in the default topic order so the digest shows Hacker News before broader industry news.

## Data Flow

The pipeline remains structurally unchanged:

1. `fetch-rss.py` fetches `hnrss.org/frontpage` and preserves HN metadata such as `hn_url`, `score`, `num_comments`, and `hn_rank`.
2. `merge-sources.py` assigns source context and groups articles using topic definitions.
3. Because `hn-rss` now declares only `hackernews`, HN articles enter only the `hackernews` group.
4. `render-acceptance-digest.py` renders the `hackernews` topic as a dedicated section.

No special-case merge routing is required.

## Rendering Behavior

For the `hackernews` topic, render exactly the top 10 eligible HN stories when 10 or more are available. The topic ordering should follow Hacker News frontpage rank (`hn_rank` ascending) because the product requirement is to show Hacker News Top 10, not the highest local quality-score items. If an item lacks `hn_rank`, fall back after ranked items using HN score descending, then title.

For each `hackernews` topic item, render:

- Title.
- HN score and comment count when available.
- HN discussion URL as the primary link when available.
- External article URL as a secondary link when it differs from the HN discussion URL.

For other topics, keep existing rendering behavior.

The fixed Hacker News section remains useful when merged input contains HN articles outside the `hackernews` topic, but it should not create duplicates after the new topic has already rendered those articles. Dedupe must cover both duplicate articles inside the `hackernews` topic and cross-section duplicates between `hackernews`, generic topic sections, and the fixed Hacker News fallback.

## Documentation Updates

Update public docs that describe default topic counts or topic names:

- `README.md`
- `README_CN.md`
- `SKILL.md`
- `scripts/test-pipeline.sh`

The built-in source count does not change. The default topic count changes from 5 to 6.

## Tests

Update or add tests for these contracts:

1. `tests/test_config.py`
   - `REQUIRED_TOPICS` includes `hackernews`.
   - documentation examples include the current topic count and topic id.

2. `tests/test_acceptance_digest.py`
   - HN articles from `hn-rss` group into `hackernews`.
   - HN articles do not group into `frontier-tech` when only the default source config is used.
   - Chat output renders `## 📰 Hacker News / 热榜`.
   - Discord output renders the same dedicated topic label.
   - HN topic items include score/comment metadata when present.
   - HN topic renders at most 10 items.
   - Duplicate HN stories render once, even when they share a normalized title or URL across topic/fallback candidates.

3. Golden files
   - Update digest golden files only after reviewing the rendered diff.

## Risks

The main risk is changing expected digest ordering. Putting `hackernews` before `frontier-tech` intentionally makes HN more visible and reduces noise in `frontier-tech`.

Another risk is duplicate HN sections if the fixed Hacker News fallback and the new topic both render the same articles. Existing visible dedupe should prevent this, and tests should cover the intended behavior.

## Out of Scope

This change does not add more Hacker News feeds such as `best`, `newest`, `show`, or `ask`.

This change does not alter HN ranking selection beyond making HN a first-class topic.

This change does not modify source health behavior or pipeline concurrency.
