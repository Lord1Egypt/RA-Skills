---
name: coin-news-openclaw
description: Collect and summarize cryptocurrency and coin market news with OpenClaw-friendly workflows. Use when users request coin news, crypto news, token-specific news, daily market briefings, or a replacement for Dify-based news aggregation. Supports configurable sources, keyword scoring, source weighting, deduplication, and structured JSON output for downstream tuning.
---

# Coin News OpenClaw

Collect cryptocurrency news from configurable sources, normalize the articles, score relevance, and return a structured digest that can be tuned over time.

## Use This Skill When

- The user wants a daily or on-demand crypto news digest
- The user wants news for a specific token or narrative
- The user wants to replace or compare against an existing Dify news workflow
- The user wants a configurable pipeline that PA can tune later

## Workflow

1. Read `references/sources.yaml` to determine enabled sources and source weights.
2. Read `references/scoring.yaml` to determine token aliases, topic keywords, negative keywords, and ranking logic.
3. If deterministic collection is needed, run `scripts/fetch_coin_news.py`.
4. Filter the normalized article list to the user’s requested scope.
5. Rank articles using source weight, keyword matches, recency, and duplicate suppression.
6. Return a short digest or a structured JSON array for downstream workflow use.

## CLI Usage

```bash
# Basic usage - JSON output (default)
python3 scripts/fetch_coin_news.py --days 1

# ⭐ Markdown output with clickable links (recommended for reading)
python3 scripts/fetch_coin_news.py --days 1 --format markdown

# Limit number of articles
python3 scripts/fetch_coin_news.py --days 1 --limit 10 --format markdown

# Filter by specific tokens
python3 scripts/fetch_coin_news.py --days 1 --token BTC --token ETH

# Filter by specific topics
python3 scripts/fetch_coin_news.py --days 1 --topic etf --topic regulation

# Adjust token fetch limit (default: 100, max: 250)
python3 scripts/fetch_coin_news.py --days 1 --token-limit 50

# Disable dynamic token fetching (use only YAML config)
python3 scripts/fetch_coin_news.py --days 1 --no-dynamic-tokens
```

## Output Formats

### JSON (default)
```bash
python3 scripts/fetch_coin_news.py --days 1
```
Returns structured JSON for programmatic use.

### Markdown (recommended for reading)
```bash
python3 scripts/fetch_coin_news.py --days 1 --format markdown
```
Returns formatted markdown with **clickable links** for each article:

```markdown
## 1. [Article Title](https://example.com/article)
**来源**: CoinDesk | **时间**: 2026-03-25 | **分数**: 78
**Token**: BTC, ETH
**主题**: etf

Summary text here...
---
```

## Time Range

- Default: last 24 hours
- Support explicit day windows such as:
  - recent 2 days
  - recent 3 days
  - recent 7 days
- Support common Chinese requests such as:
  - 最近2天
  - 最近3天
  - 最近一周
  - 过去7天
- For deterministic runs, prefer `--days <n>` over manually converting to hours.
- If both `--days` and `--hours` are provided, `--days` takes precedence.
- Recommended mapping:
  - 最近2天 -> `--days 2`
  - 最近3天 -> `--days 3`
  - 最近一周 -> `--days 7`
  - 过去7天 -> `--days 7`

## Dynamic Token Fetching

The skill automatically fetches the top 100 tokens (by market cap) from CoinGecko API and merges them with the YAML config:

- **Source**: CoinGecko API (free, no API key required)
- **Cache TTL**: 24 hours (stored in `scoring.yaml` under `dynamic_tokens`)
- **Merge logic**: YAML `token_aliases` overrides dynamic tokens (for manual tuning)
- **Disable**: Use `--no-dynamic-tokens` to use only YAML config

## Output Contract

Prefer this JSON structure for workflow handoff:

```json
[
  {
    “title”: “Example headline”,
    “url”: “https://example.com/article”,
    “source”: “CoinDesk”,
    “published_at”: “2026-03-20T09:00:00Z”,
    “summary”: “One paragraph summary.”,
    “score”: 78,
    “matched_topics”: [“bitcoin”, “etf”],
    “matched_tokens”: [“BTC”],
    “duplicate_group_key”: “normalized-title-key”
  }
]
```

## Tuning Rules

- Do not hardcode source lists in prompts. Update `references/sources.yaml`.
- Do not hardcode scoring logic in prompts. Update `references/scoring.yaml`.
- Prefer established publications before secondary aggregators.
- If the user asks for “latest” or “today”, prioritize the last 24 hours and show exact dates.

## References

- `references/sources.yaml`: source registry and weights
- `references/scoring.yaml`: token aliases, topic keywords, penalties, thresholds
- `scripts/fetch_coin_news.py`: deterministic RSS collector and scorer
