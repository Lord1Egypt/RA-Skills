---
name: search
description: "Content search and synthesis primitive using Kaito MCP tools. Use this skill to search for and synthesize content from Twitter (X) and News sources. Triggers on phrases like 'search for tweets about X', 'what's being said about Y', 'find content about Z', 'any news on X', 'what are people saying about Y on Twitter'. This is a primitive skill — it searches content via kaito_advanced_search and synthesizes results. It can be called standalone or composed into higher-level workflow skills. Do NOT use for mindshare tracking (mindshare skill), sentiment analysis (sentiment skill), or user profiling (user-profile skill)."
---

# Search Skill (Content Search Primitive)

Search for and synthesize content from Twitter and News using `kaito_advanced_search`.

## Parameters

- **entity** *(required)*: What to search for. One of:
  - `tokens`: Ticker symbol (e.g. `HYPE`, `SOL`, `ETH`) — exact Kaito entity match
  - `keyword`: Project name or free-text (e.g. `HYPERLIQUID`, `liquid staking`) — broader match
  - `topics`: Kaito-indexed topic (e.g. `DeFi`, `AI`, `L2`) — built-in query expansion
  - `usernames`: Twitter handle(s) to search posts from (e.g. `HyperliquidX`)
- **time_horizon** *(required)*: Time window (e.g. 24h, 48h, 7d, 30d). Sets `min_created_at` / `max_created_at`.
- **sources** *(optional)*: `Twitter`, `News`, or both (default: both)
- **sort_by** *(optional)*: Ranking method (default: `relevance`)

When called standalone, confirm parameters with the user first. When called by a workflow skill, parameters are passed directly.

### Critical: Kaito Search Behavior (AND Logic + Exact Match)

Kaito's search uses **AND** across all fields and **exact string matching** (not semantic). This means:
- If you set `tokens: HYPE` **and** `keyword: liquid staking`, a result must contain **both** — drastically reducing matches.
- The more fields you fill, the **fewer** results you get. Adding parameters narrows, never broadens.
- There is no fuzzy/semantic matching — `liquid staking` won't match "staked liquidity" or "LST".

**Strategy: Use ONE entity field per call. Never combine `tokens` + `keyword` + `topics` in a single request.**

**Default query strategy: AND-narrow with boolean expansion.**

The optimal query pattern is: pick ONE entity term and ONE topic/context term, AND them together, and OR-expand each with spelling variants, plurals, and handles.

```
keyword: "EntityA" OR "EntityA_variant" "TopicB" OR "TopicB_variant"
```

Spaces between OR-groups act as AND. This is the `(A OR A') AND (B OR B')` pattern.

**Step-by-step:**
1. **Identify the most distinctive proper noun** — prefer unique names over common ones (e.g. "Wyoming" > "Kraken" when searching for Kraken's Fed master account, because "Kraken" matches many unrelated posts).
2. **AND-narrow with a topic term** — combine entity + distinctive topic/context term in the keyword field (e.g. `"Hyperliquid" "buyback"`). This filters down to relevant content.
3. **OR-expand each AND-group** with:
   - **Plurals**: `"agent" OR "agents"`, `"buyback" OR "buybacks"`
   - **Spelling variants**: `"memecoin" OR "memecoins" OR "meme coin" OR "meme coins"`, `"crypto" OR "cryptocurrency"`
   - **Handles**: `"SUI" OR "@SuiNetwork"`, `"Kraken" OR "@krakenfx"` — Twitter handles are powerful OR-variants that improve recall
   - **Ticker variants**: `"hyperliquid" OR "$HYPE" OR "HYPE" OR "@HyperliquidX"`
4. **If a ticker exists and differs from the keyword**, make a **parallel** `tokens` call and merge results. This provides redundancy — some content is only findable via ticker, some only via name.
5. **Do NOT use `tokens` alone for major tickers** (BTC, ETH, SOL) — the result set is too broad to surface specific content. Always pair with a keyword call.
6. **Do NOT use `topics` for targeted search** — topics return category-level firehose results. Only use for broad discovery/scanning.
7. **`usernames` param** — use for searching posts from official project accounts or known authors (e.g. `usernames: jespow`). Also add handles as OR-variants in keyword searches for better recall.

### Proximity Matching (automatic `~15` slop)

Simple keywords — those without `AND`, `OR`, `-`, or quoted phrases — automatically get **proximity matching with slop 15**. This means the words just need to appear within 15 tokens of each other in the document, not adjacent. For example, `liquid staking` (unquoted) matches text where "liquid" and "staking" appear near each other, even with other words in between. To require an **exact adjacent phrase**, wrap in quotes: `"liquid staking"`.

### Text Field Modifiers (`#...#` and `[...]`)

The keyword field supports special syntax to target different text analyzers:

- **`#keyword#`** → **case-sensitive** match (field: `text.case_sensitive`). Useful for ambiguous tickers: `#SOL#` avoids matching "solution", `#AI#` avoids matching "said".
- **`[keyword]`** → **English-stemmed** match (field: `text.english_analyzed`). Matches morphological variants: `[staking]` matches "staked", "stakes", "staking".
- **Default (no modifier)** → **standard analyzer** (field: `text.standard`). Balanced tokenization without stemming.

These can be combined with boolean operators: `#SOL# "liquid staking"` means case-sensitive SOL AND exact phrase "liquid staking".

### Keyword Search Syntax (Boolean Operators)

The `keyword` field supports boolean operators. Understanding precedence is critical:

- **Exact phrase**: Wrap in quotes — `"liquid staking"` matches the exact phrase only.
- **OR operator**: Use capitalized `OR` between terms — `"liquid staking" OR "LST"` matches either phrase.
- **AND (implicit)**: Spaces between OR-groups act as AND — `"A" OR "B" "C" OR "D"` means `(A OR B) AND (C OR D)`.

**Precedence: AND binds tighter than OR.** The query `"Lighter" "Hyperliquid" OR "perp DEX"` parses as `("Lighter" AND "Hyperliquid") OR "perp DEX"`, flooding results with generic perp DEX content. To get the intended meaning, structure OR-groups carefully.

**OR must only broaden variants of the same concept — never mix in a different concept.**
- Good: `"Hyperliquid" OR "$HYPE" OR "@HyperliquidX"` — same entity, different representations.
- Good: `"buyback" OR "buybacks"` — same concept, plural variant.
- Bad: `"Hyperliquid" OR "perp DEX"` — different concepts; floods results with unrelated content.

**Use the simplest, most natural term — don't guess at multi-word phrases.**
- Good: `"Lighter"` — how people actually refer to the project.
- Bad: `"Lighter DEX" OR "Lighter exchange" OR "Lighter protocol"` — nobody writes these; returns very few results.

**Comparison queries: use multiple quoted terms in a single keyword field.**
- To find posts comparing two projects, put both names as separate quoted terms: `"Hyperliquid" "Lighter"`. Kaito ANDs them, surfacing only posts that mention both — exactly what you want for comparisons.

**Beware common-word project names (e.g. "Lighter", "Drift", "Pump").**
- These match as English adjectives/nouns in the `keyword` field (e.g. "lighter volume" = lower volume). For common-word projects, **prefer the `tokens` param** (e.g. `tokens: LIT`) — Kaito pre-runs entity linking (mapping various keywords, Twitter handles, and ticker variants to the canonical token) and relevance tagging, so results are already disambiguated. Only fall back to `keyword` with a disambiguating term (e.g. `"Lighter" "perps"`) if the token isn't indexed.

### Kaito-Indexed Topics (prefer `topics` param — built-in query expansion)

AI, Robotics, DeFi, Stablecoin, Prediction Markets, Perp DEX, NFT, Gaming, L2, ZK, RWA, Restaking, Liquid Staking, DEX, Lending, Yield, Bridge, Privacy, Wallet, Infrastructure

If the topic isn't indexed, use the `keyword` parameter instead and note that query expansion won't apply.

---

## Workflow

### Step 1 — Call `kaito_advanced_search` (with pagination)

Retrieve multiple pages of results to ensure broad coverage.

**Scale pagination to query specificity:**

| Query type | Example | Twitter pages | Rationale |
|---|---|---|---|
| Broad single-entity | `tokens: HYPE` | 10 (200 results) | Large result set; need depth |
| Moderate / themed | `keyword: "liquid staking"` | 5–7 (100–140 results) | Medium result set |
| Narrow comparison | `"Hyperliquid" "Lighter"` | 2–3 (40–60 results) | AND of two names is inherently narrow; pages 3+ are mostly SE ≤ 2 tangential mentions |

For each Twitter page, call `kaito_advanced_search` with:
- The appropriate entity parameter (`tokens`, `keyword`, `topics`, or `usernames`)
- sources: Twitter
- min_created_at: `<window_start>`
- max_created_at: `<window_end>` (if applicable)
- size: 20
- sort_by: relevance
- from: `<0, 20, 40, ...>`

**For News (always 1 page → 20 results):**

Call `kaito_advanced_search` with:
- The appropriate entity parameter
- sources: News
- min_created_at: `<window_start>`
- max_created_at: `<window_end>` (if applicable)
- size: 20

News is high-efficiency: one call typically returns all relevant long-form articles.

Make all calls in parallel (Twitter pages + News page) when both sources are requested.

### Step 2 — Synthesize Results

Merge paginated results, deduplicate, then categorize content into:
- **Positive** — bullish narratives, partnerships, product launches, KOL endorsements
- **Negative** — FUD, exploits, regulatory risks, criticism
- **Neutral/Notable** — major events worth knowing regardless of sentiment

For each item include:
- Author and their `smart_engagement` score
- 1-2 sentence summary
- Source link (tweet URL or news URL)

Highlight any post with `smart_engagement` > 50 as high-signal.

---

## Output Format

When used standalone:

```
Content Search: [ENTITY] | [TIME WINDOW] | [SOURCES]
Ranked by: relevance (desc)

--- TWITTER (sorted by relevance) ---
Positive
- @author (SE: N): [summary — only claims present in retrieved data] [URL]
...

Negative
- @author (SE: N): [summary — only claims present in retrieved data] [URL]
...

Notable
- @author (SE: N): [summary — only claims present in retrieved data] [URL]
...

--- NEWS ---
- [headline] (SE: N) [URL]
...
```

When called by a workflow skill, return the structured results for the workflow to integrate into its own output format.

---

## Key Rules

- **Default to `sort_by: relevance`** unless the user explicitly requests a different ranking. Relevance ranking surfaces the most topically relevant content. Use `smart_engagement` only when specifically requested.
- **Scale pagination to query specificity** — broad single-entity searches warrant 10 pages; narrow comparison queries (AND of two names) only need 2–3 pages since pages 3+ are mostly low-SE tangential mentions. Always fetch 1 page for News.
- **Never combine multiple entity fields in one call** — Kaito ANDs all fields together, so combining `tokens` + `keyword` narrows results severely. Use separate calls and merge.
- **AND-narrow + boolean expansion is the default strategy** — always combine entity + topic term in keyword, then OR-expand each group with plurals, spelling variants, and handles. Pattern: `"EntityA" OR "@EntityHandle" "topic" OR "topics"`. This achieves highest recall while keeping results relevant.
- **Prefer `keyword` over `tokens` as the primary search** — keyword has 3.5x higher recall than token-only searches. Major tickers (BTC, ETH, SOL) return firehose results where specific content drowns.
- **If a ticker exists, run a parallel `tokens` call as supplementary** — merge with keyword results. Some content is only findable via one or the other.
- **If `tokens` returns empty**, the token may not be indexed. Fall back to keyword immediately.
- **OR-expand aggressively within each AND-group** — always include plurals (`"agent" OR "agents"`), common abbreviations, handles (`"SUI" OR "@SuiNetwork"`), and ticker variants (`"HYPE" OR "$HYPE"`). OR across variants of the same concept improves recall without diluting relevance.
- **Pick the most distinctive proper noun for AND-narrowing** — when multiple terms could identify a topic, use the rarest one. Example: for "Kraken's Fed master account", use `"Wyoming"` not `"Kraken"` as the primary entity, since Wyoming is more distinctive for this specific topic.
- **`smart_engagement` is an integer** (e.g. 124) representing how many smart accounts engaged — do NOT confuse with `sentiment_score` (a volume-weighted float indicating tone × volume).
- **Indexed topics use the `topics` parameter; unindexed topics use `keyword`** — using `topics` for indexed terms gives Kaito's built-in query expansion. Using it for unindexed terms returns empty results.
- **Make separate calls for Twitter and News** — they are different source types and the separation makes synthesis cleaner.
- **NEVER fabricate or embellish details beyond what the API returns** — only include claims, quotes, figures, wallet addresses, and engagement numbers that appear verbatim in the search results. If the retrieved data is thin, say so honestly rather than filling gaps with plausible-sounding specifics. Attribute every factual claim to a specific search result with its URL. If you cannot link a claim to a retrieved result, do not include it.
- **Always show smart_engagement counts in output** — every cited tweet or article MUST include its `smart_engagement` integer from the API response (displayed as `SE: N`). This is critical for transparency and for demonstrating that results were ranked by smart_engagement.
- **For comparison queries, use dual-quoted terms in keyword** — e.g. `"Hyperliquid" "Lighter"` forces AND between the two names, surfacing only posts that discuss both. This is the most effective strategy for "X vs Y" searches. Supplement with a `tokens`-based search for each entity separately if one-sided context is also needed.
- **Use the simplest natural term, not guessed multi-word phrases** — people write "Lighter" not "Lighter DEX" or "Lighter protocol". Overly specific exact phrases return very few results because they don't match how people actually talk.
- **Beware common-word project names** — names like "Lighter", "Drift", "Pump" match as English words in the `keyword` field. **Prefer `tokens` param** (e.g. `tokens: LIT`) — Kaito pre-runs entity linking and relevance tagging, so results are already disambiguated. Only fall back to `keyword` with a disambiguating term if the token isn't indexed.
