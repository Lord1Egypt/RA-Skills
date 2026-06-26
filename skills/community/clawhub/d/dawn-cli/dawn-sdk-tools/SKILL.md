---
name: dawn-sdk-tools
description: Reference for all Dawn SDK tools. ALWAYS run `dawn tool docs <module>` before writing strategy code — it has complete signatures, return types, and working code examples for every tool. Use `dawn tool run <name> --input <json>` to call tools directly for research.
tags: [sdk, research, strategy]
metadata:
  openclaw:
    emoji: "🌅"
    homepage: https://dawn.ai
    requires:
      bins: [dawn]
    install:
      - kind: node
        package: "@dawnai/cli"
        bins: [dawn]
---

# Dawn SDK Tools Reference

## ALWAYS read the SDK docs before writing strategy code

**`dawn tool docs` is the single most important command when writing strategy code.** It returns the complete, up-to-date module reference with exact function signatures, return types, and working code patterns. Always run it before generating code for any module.

```bash
# ALWAYS read these before writing strategy code:
dawn tool docs overview      # SDK architecture + which modules to use
dawn tool docs directive     # Strategy coding rules and patterns (REQUIRED reading)
dawn tool docs prediction_market    # Full prediction market reference with code examples
dawn tool docs portfolio     # Portfolio, state management, termination
dawn tool docs web           # Browser search and URL extraction
dawn tool docs social        # Twitter/social tools
dawn tool docs sports        # Sports data + odds tools
dawn tool docs crypto        # Cryptocurrency OHLCV data
dawn tool docs utils         # classify_text and other helpers
```

**Do not guess tool signatures or parameters.** Run `dawn tool docs <module>` first — it has working code snippets for every tool, edge cases, and return type details that are not in this skill file.

---

## Overview

The Dawn SDK provides tools for trading on Polymarket prediction markets, monitoring the web and social media, accessing sports data and crypto prices, and managing portfolio state. SDK tools are imported via:

```python
from dawnai.strategy.tools import <tool_name>
```

The Dawn SDK is one toolbox among many. The Python standard library is always available, and any pip dependency you declare in `pyproject.toml` (`[project.dependencies]`) or `requirements.txt` is installed into the strategy's per-deps venv on launch — pandas, numpy, your own HTTP clients, ML libraries, anything pip can resolve.

## Tool Types

**Research tools** — read-only, safe to call any time, no wallet required:
`prediction_market_event_search`, `prediction_market_list_events`, `prediction_market_event_markets`, `get_prediction_market_details`, `get_prediction_market_prices`, `get_prediction_market_order_book`, `get_prediction_market_timeseries`, `get_prediction_market_market_trades`, `prediction_market_simulate_buy`, `prediction_market_simulate_sell`, `browser_search`, `extract_text_from_urls`, `search_tweets`, `get_user_tweets`, `get_tweet_info`, `get_sports`, `get_events`, `get_odds_as_probabilities`, `get_scores`, `get_cryptocurrency_ohlcv`, `get_exchanges`, `get_exchange_symbols`, `read_portfolio`, `classify_text`

**Execution tools** — execute real live trades, require wallet + **explicit user confirmation**:
`prediction_market_buy_token`, `prediction_market_sell_token`

## Cost-aware tool use

Some research tools are paid. Use them deliberately, and design strategy code so paid calls are triggered by likely decision points rather than blind high-frequency polling.

Before running tools:
- Tell the user the expected duration for the work. Focused research is often 3-5 minutes; research + code + launch is often 8-15 minutes; deep research/debugging may be 15-30+ minutes.
- Check `dawn tool settings` if tool availability matters, and respect disabled paid tools.
- Prefer cheap/free discovery first: prediction market search, market details, prices, order books, portfolio state, and cached config.
- Use paid tools only after cheap checks show a trade might be possible or more evidence is actually needed.

When writing monitoring strategies:
- Cache source results and `last_seen_*` markers to avoid re-processing unchanged data.
- Add `start_at_utc` / `active_after_utc` for future updates instead of polling before the relevant window.
- Use active windows, quiet hours, cooldowns, backoff, and daily caps for paid checks.
- For websites, avoid repeated `extract_text_from_url(s)` unless the page is likely to have changed, a cheap search/headline check suggests a change, or the user explicitly wants high-frequency monitoring.
- For social sources, adapt polling to the source's likely activity window and the market's urgency.

```bash
dawn tool settings
dawn tool toggle <tool_name>
```

---

## Direct Trade Workflow

Use this when the user asks to trade on a specific market **without** building a full strategy (e.g. "buy the yes token of this market", "sell my position on X").

**Prerequisite:** wallet must be configured — `dawn wallet use <address-or-name>`

**Workflow:**

```bash
# 1. Research — find the market and token IDs
dawn tool run prediction_market_event_search --input '{"query": "...", "limit": 5}'
dawn tool run get_prediction_market_details --input '{"market_id": "..."}'
dawn tool run get_prediction_market_prices --input '{"market_id": "..."}'

# 2. Simulate — preview price impact and tokens received
dawn tool run prediction_market_simulate_buy --input '{"token_id": "...", "usd_amount": "10"}'

# 3. ALWAYS ask for explicit confirmation before executing:
# "Market: [question]
#  Current ask: $0.62 per Yes token
#  $10 → ~16 Yes tokens (avg price $0.625, price impact 0.1%)
#  Shall I execute this buy?"

# 4. Only after user confirms — execute:
dawn tool run prediction_market_buy_token --input '{"token_id": "...", "amount": "10"}'
```

**Never execute a trade without first showing the user the market details and asking for confirmation.**

---

## Research Mode

Before writing strategy code, use `dawn tool run` to call any SDK tool and inspect real data. This is the primary way to discover markets, check prices, and validate your strategy logic.

```bash
# Find prediction market events
dawn tool run prediction_market_event_search --input '{"query": "Bitcoin price 2025", "limit": 5}'

# Get market details for a specific market
dawn tool run get_prediction_market_details --input '{"market_id": "123456"}'

# Check current market prices
dawn tool run get_prediction_market_prices --input '{"market_id": "123456"}'

# Search the web
dawn tool run browser_search --input '{"query": "US election prediction markets", "limit": 10}'

# Get in-season sports
dawn tool run get_sports --input '{}'

# Get NFL events
dawn tool run get_events --input '{"sport": "americanfootball_nfl"}'

# Search Twitter
dawn tool run search_tweets --input '{"query": "Bitcoin ETF approval", "query_type": "Latest"}'

# Check portfolio
dawn tool run read_portfolio --input '{}'
```

---

## Prediction Market Tools

### `prediction_market_event_search`

Search for active prediction market events by keyword. Use this first to discover relevant markets.

```python
prediction_market_event_search(
    query: str,              # Search query
    limit: int = 10,         # Max events to return
    events_status: str = 'active',  # 'active' or 'resolved'
    sort: str | None = None, # 'volume_24hr', 'volume', 'liquidity', 'start_date', 'end_date'
    ascending: bool = False,
    page: int = 1
) -> PolymarketEventSearchResponse
```

Returns: `PolymarketEventSearchResponse` with fields:
- `events: list[PolymarketEvent]` — each has `id`, `title`, `description`, `volume`, `volume24hr`, `liquidity`, `active`, `closed`, `start_date`, `end_date`, `tags`, `market_count`
- `tags: list[Tag]`
- `count: int`

**Research example:**
```bash
dawn tool run prediction_market_event_search --input '{"query": "Presidential election", "limit": 5, "sort": "volume_24hr"}'
```

---

### `prediction_market_list_events`

List events with advanced filters. Use for pagination or tag-based browsing.

```python
prediction_market_list_events(
    limit: int = 10,
    offset: int = 0,
    order: str | None = None,   # 'volume', 'volume_24hr', 'liquidity', 'start_date', 'end_date'
    ascending: bool = False,
    tag_id: int | None = None,
    featured: bool | None = None,
    closed: bool | None = None,
    end_date_min: str | None = None,  # ISO date-time
    end_date_max: str | None = None,
    # ... more filters
) -> PolymarketListEventsResponse
```

Returns: `PolymarketListEventsResponse` with `events: list[PolymarketEvent]`, `count: int`

---

### `prediction_market_event_markets`

Get all markets within a specific event. Use after finding an event to see tradeable outcomes.

```python
prediction_market_event_markets(
    event_id: int,
    limit: int = 10,
    offset: int = 0,
    order: str | None = None,  # 'volume24hr', 'volume', 'liquidity', 'startDate', 'endDate'
    ascending: bool = False,
    active: bool | None = None,
    closed: bool | None = None
) -> PolymarketEventMarketsResponse
```

Returns: `PolymarketEventMarketsResponse` with:
- `markets: list[PolymarketMarket]` — each has `id`, `question`, `slug`, `active`, `closed`, `tokens` (list of `TokenInfo`)
- `total_markets: int`
- `event_info: EventInfo` — has `id`, `title`, `description`, `slug`

**Research example:**
```bash
dawn tool run prediction_market_event_markets --input '{"event_id": 12345, "active": true, "limit": 10}'
```

---

### `get_prediction_market_details`

Get detailed information about a specific market, including token IDs needed for trading.

```python
get_prediction_market_details(
    market_id: str   # e.g. "123456"
) -> PolymarketMarket | None
```

Returns `PolymarketMarket` with:
- `id: str`
- `question: str`
- `tokens: list[TokenInfo]` — each has `id: str`, `outcome: str` (e.g. "Yes", "No")

**The token `id` is what you pass to `prediction_market_buy_token` / `prediction_market_sell_token`.**

**Research example:**
```bash
dawn tool run get_prediction_market_details --input '{"market_id": "123456"}'
```

**Code pattern:**
```python
market = get_prediction_market_details(market_id)
if market is None:
    print(f"Market {market_id} not found")
    return

yes_token = next((t for t in market.tokens if t.outcome.lower() == "yes"), None)
no_token = next((t for t in market.tokens if t.outcome.lower() == "no"), None)
print(f"Yes token: {yes_token.id}")
print(f"No token: {no_token.id}")
```

---

### `get_prediction_market_prices`

Get current bid/ask prices for all tokens in a market.

```python
get_prediction_market_prices(
    market_id: str
) -> GetPolymarketPricesResponse
```

Returns `GetPolymarketPricesResponse` with:
- `prices: dict[str, MarketPriceData]` — maps token_id → `MarketPriceData(BUY="0.55", SELL="0.54")`
  - `BUY` = best bid (what you receive selling), `SELL` = best ask (what you pay buying)
- `error: str | None`

Note: `prices` is empty if market is closed.

**Research example:**
```bash
dawn tool run get_prediction_market_prices --input '{"market_id": "123456"}'
```

---

### `get_prediction_market_timeseries`

Get historical price data for a market outcome.

```python
get_prediction_market_timeseries(
    market_id: str,
    side: str,             # "Yes", "No", etc. — matched case-insensitively
    interval: str = '1h',  # '1m', '1h', '6h', '1d', '1w', 'max'
    fidelity: int = 60     # resolution in seconds
) -> list[TimeseriesPoint]
```

Returns list of `TimeseriesPoint(t: int, p: Decimal)` where `t` = Unix timestamp, `p` = price.

---

### `get_prediction_market_order_book`

Get the order book for one side of a market.

```python
get_prediction_market_order_book(
    market_id: str,
    side: str   # "Yes", "No", "Up", "Down", etc.
) -> OrderBookResponse
```

Returns `OrderBookResponse` with `order_book: OrderBookData | None`:
- `bids: list[Order]` — each has `price: Decimal`, `size: Decimal`
- `asks: list[Order]`
- `tick_size: str`
- `min_order_size: str`

---

### `get_prediction_market_market_trades`

Fetch recent trades on a specific market (by condition ID). Good for market flow, spotting large prints, and taker vs maker mix.

```python
get_prediction_market_market_trades(
    market_id: str,                                   # 0x-prefixed condition ID
    limit: int = 100,                                 # max 10000
    offset: int = 0,
    side: Literal["BUY", "SELL"] | None = None,
    taker_only: bool = True,
    filter_type: Literal["CASH", "TOKENS"] | None = None,  # pair with filter_amount
    filter_amount: float | None = None,
) -> TradesResponse
```

Returns `TradesResponse`:
- `trades: list[Trade]` — each with `proxy_wallet`, `timestamp`, `side`, `size`, `price`, `asset`, `outcome`, `title`, etc.
- `count: int`
- `error: str | None`

```python
trades = get_prediction_market_market_trades(market_id="0x…", limit=20, filter_type="CASH", filter_amount=500)
for t in trades.trades:
    print(f"{t.side} {t.size:.2f} @ ${t.price:.3f} by {t.proxy_wallet[:8]}")
```

Also aliased as `get_polymarket_market_trades`.

---

### `prediction_market_simulate_buy`

Preview a buy order without executing it. Check price impact and slippage.

```python
prediction_market_simulate_buy(
    token_id: str,
    usd_amount: Decimal   # Amount of USDC to spend
) -> SimulateTradeResult
```

Returns `SimulateTradeResult` with:
- `average_price: Decimal`
- `tokens_traded: Decimal`
- `usd_amount: Decimal`
- `price_impact_percent: Decimal | None`
- `error: str | None`

---

### `prediction_market_simulate_sell`

Preview a sell order without executing it.

```python
prediction_market_simulate_sell(
    token_id: str,
    token_amount: Decimal   # Number of tokens to sell (NOT USD)
) -> SimulateTradeResult
```

---

### `prediction_market_buy_token`

> **EXECUTION TOOL** — executes a real live trade. Always research the market, simulate the trade, show the user the outcome, and ask for confirmation before calling this.

Spends USDC to purchase prediction market tokens. Requires a wallet configured via `dawn wallet use`.

```python
prediction_market_buy_token(
    token_id: str,
    amount: Decimal   # USDC to spend. Minimum $1.
) -> BuyTokenResult
```

Returns `BuyTokenResult` with:
- `result: OrderResult` — has `success: bool`, `order_id: str`, `executed_price: Decimal`, `executed_amount: Decimal`
- `error: str | None`

**Code pattern (in strategy):**
```python
buy_result = prediction_market_buy_token(yes_token_id, Decimal("100"))
if not buy_result.result.success:
    print(f"[Error] Buy failed: {buy_result.error}")
    return
print(f"Bought {buy_result.result.executed_amount} tokens at {buy_result.result.executed_price}")
```

---

### `prediction_market_sell_token`

> **EXECUTION TOOL** — executes a real live trade. Always research the market, simulate the trade, show the user the outcome, and ask for confirmation before calling this.

Sells prediction market tokens for USDC. **If the market has resolved, automatically redeems the tokens instead of selling on the order book** — users don't need to distinguish between selling and redeeming. Requires a wallet configured via `dawn wallet use`.

```python
prediction_market_sell_token(
    token_id: str,
    amount: Decimal   # Number of tokens to sell
) -> SellTokenResult
```

Returns `SellTokenResult` (same structure as `BuyTokenResult`).

---

### `get_prediction_market_leaderboard`

Get the top traders on prediction markets ranked by PnL or volume.

```python
get_prediction_market_leaderboard(
    category: str = "OVERALL",    # OVERALL, POLITICS, SPORTS, CRYPTO, CULTURE, ECONOMICS, etc.
    time_period: str = "DAY",     # DAY, WEEK, MONTH, ALL
    order_by: str = "PNL",        # PNL or VOL
    limit: int = 25,              # 1-50
    offset: int = 0,
    user: str | None = None,      # filter by wallet address
    user_name: str | None = None, # filter by username
) -> LeaderboardResponse
```

Returns `LeaderboardResponse` with `entries: list[LeaderboardEntry]`:
- `rank: str`, `user_name: str`, `pnl: float`, `volume: float`
- `proxy_wallet: str` — **use this as the `proxy_wallet` param in `get_prediction_market_user_activity`**

---

### `get_prediction_market_user_activity`

Get a specific user's trading activity. The `proxy_wallet` comes from leaderboard results.

```python
get_prediction_market_user_activity(
    proxy_wallet: str,             # from leaderboard's proxy_wallet field
    limit: int = 100,
    offset: int = 0,
    type: str | None = None,       # TRADE, REDEEM, SPLIT, MERGE, etc.
    side: str | None = None,       # BUY or SELL
    start: int | None = None,      # Unix timestamp
    end: int | None = None,        # Unix timestamp
    sort_by: str = "TIMESTAMP",    # TIMESTAMP, TOKENS, CASH
    sort_direction: str = "DESC",
) -> UserActivityResponse
```

Returns `UserActivityResponse` with `activities: list[UserActivity]`:
- `timestamp: int`, `type: str`, `side: str`, `size: float`, `usdc_size: float`, `price: float`
- `title: str`, `outcome: str`, `event_slug: str`, `transaction_hash: str`

**Typical workflow — copy-trade the top trader:**
```python
# 1. Find the top trader this week
lb = get_prediction_market_leaderboard(time_period="WEEK", limit=1)
whale = lb.entries[0]
print(f"Top trader: {whale.user_name} (PnL: ${whale.pnl:.0f})")

# 2. See what they're trading
trades = get_prediction_market_user_activity(whale.proxy_wallet, limit=5, type="TRADE")
for t in trades.activities:
    print(f"  {t.side} {t.size:.0f} tokens @ ${t.price} — {t.title} [{t.outcome}]")
```

---

## Portfolio Tools

### `read_portfolio`

Read current wallet balance and open positions (paper and live strategies, from internal DB).

```python
read_portfolio() -> PortfolioResponse
```

Returns `PortfolioResponse` with:
- `wallet: WalletData`:
  - `current_balance: Decimal`
  - `total_pnl: Decimal`
  - `positions: list[WalletPosition]` — each has `token_id`, `market_id`, `amount`, `cost_basis`, `current_value`, `pnl`, `pnl_percent`
- `strategy: StrategyData`:
  - `total_pnl: Decimal`, `total_pnl_percent: Decimal`
  - `transactions: list[StrategyTransaction]`

**Code pattern:**
```python
portfolio = read_portfolio()
print(f"Balance: ${portfolio.wallet.current_balance}")
print(f"Total PnL: ${portfolio.wallet.total_pnl}")

for position in portfolio.wallet.positions:
    print(f"Token {position.token_id}: {position.amount} tokens, PnL={position.pnl_percent:.1f}%")
```

---

### `terminate_strategy`

Called **from within strategy code** when the strategy decides it's done (e.g. take-profit hit, market resolved). Do not call this as a standalone tool — to stop a running strategy externally, use `dawn strategy stop <run_id>` instead.

```python
terminate_strategy(
    should_liquidate: bool = False  # if True, sells all open positions before stopping
) -> TerminateStrategyResult
```

```python
# After a successful exit trade:
terminate_strategy()
sys.exit(0)

# To liquidate all positions on exit:
terminate_strategy(should_liquidate=True)
sys.exit(0)
```

---

## Web Tools

### `browser_search`

Search the web via Brave Search. **Always verify results from specific APIs rather than relying blindly on search results.**

```python
browser_search(
    query: str,
    limit: int = 10,          # max 20
    category: str | None = None,  # 'news', 'company', 'research paper', 'github', 'tweet', etc.
    start_published_date: str | None = None,  # YYYY-MM-DD
    end_published_date: str | None = None,
    include_domains: list[str] | None = None,
    exclude_domains: list[str] | None = None
) -> BrowserSearchResponse
```

Returns `BrowserSearchResponse` with `results: list[BrowserSearchResult]` — each has `title`, `url`, `published_date`.

---

### `extract_text_from_urls`

Fetch plain text from one or more URLs. Simple but may not work for all sites.

```python
extract_text_from_urls(
    urls: list[str]   # 1-10 URLs
) -> ExtractTextResponse
```

Returns `ExtractTextResponse` with `contents: list[ExtractTextContent]` — each has `url`, `title`, `text`.

## Social Tools

### `search_tweets`

Search for tweets by keyword.

```python
search_tweets(
    query: str,
    query_type: str = 'Latest',  # 'Latest' or 'Top'
    cursor: str | None = None
) -> SearchTweetsResponse
```

Returns `SearchTweetsResponse` with `tweets: list[Tweet]`, `count: int`, `next_cursor: str | None`.

Each `Tweet` has: `id`, `text`, `created_at`, `author: TwitterUser`, `like_count`, `retweet_count`, `view_count`.

---

### `get_user_tweets`

Get recent tweets from a specific user.

```python
get_user_tweets(
    handle: str,   # Twitter handle without @
    cursor: str | None = None
) -> UserTweetsResponse
```

---

### `get_tweet_info`

Get detailed info about specific tweets by ID.

```python
get_tweet_info(
    tweet_ids: list[str]
) -> TweetInfoResponse
```

---

## Sports Tools

### `get_sports`

List available sports from The Odds API.

```python
get_sports(
    all: bool = False   # True = include out-of-season sports
) -> GetSportsResponse
```

Returns `GetSportsResponse` with `data: list[Sport]` — each has `key` (e.g. `"americanfootball_nfl"`), `title`, `active`.

**Always call this first** to get the correct `sport` key for other sports functions.

```bash
dawn tool run get_sports --input '{}'
```

---

### `get_events`

Get upcoming and live games for a sport.

```python
get_events(
    sport: str,                        # Sport key from get_sports()
    date_format: str | None = None,    # 'iso' or 'unix'
    commence_time_from: str | None = None,  # ISO 8601
    commence_time_to: str | None = None
) -> GetEventsResponse
```

Returns `GetEventsResponse` with `data: list[Event]` — each has `id`, `home_team`, `away_team`, `commence_time`.

---

### `get_odds_as_probabilities`

Get betting odds converted to implied probabilities (0–1 scale).

```python
get_odds_as_probabilities(
    sport: str,
    regions: str,          # 'us', 'uk', 'eu', 'au' (comma-separated)
    markets: str | None = None,  # 'h2h', 'spreads', 'totals' (comma-separated)
    event_ids: str | None = None
) -> GetOddsAsProbabilitiesResponse
```

Returns `GetOddsAsProbabilitiesResponse` with `data: list[OddsEvent]`.
Each `OddsEvent` has `bookmakers: list[Bookmaker]` → `markets: list[Market]` → `outcomes: list[Outcome]`.
Each `Outcome` has `name: str`, `probability: float` (implied probability 0–1).

**Code pattern:**
```python
odds = get_odds_as_probabilities("americanfootball_nfl", regions="us")
for event in odds.data:
    print(f"{event.away_team} @ {event.home_team}")
    for bookmaker in event.bookmakers:
        for market in bookmaker.markets:
            for outcome in market.outcomes:
                print(f"  {outcome.name}: {outcome.probability:.1%}")
```

---

### `get_scores`

Get live and recent game scores.

```python
get_scores(
    sport: str,
    days_from: int | None = None,   # Days in the past to include completed games (1-3)
    date_format: str | None = None
) -> GetScoresResponse
```

Returns `GetScoresResponse` with `data: list[ScoreEvent]` — each has `home_team`, `away_team`, `completed: bool`, `scores: list[Score] | None`.

---

## Crypto Tools

### `get_cryptocurrency_ohlcv`

Get historical OHLCV (open/high/low/close/volume) data.

```python
get_cryptocurrency_ohlcv(
    symbol_id: str,           # e.g. "COINBASE_SPOT_BTC_USD"
    period_id: str,           # '1SEC', '1MIN', '5MIN', '15MIN', '30MIN', '1HRS', '4HRS', '8HRS', '1DAY', '7DAY', '1MTH'
    limit: int | None = None,
    time_start: str | None = None,
    time_end: str | None = None,
    endpoint: str | None = None   # 'history' or 'latest'
) -> CryptocurrencyOhlcvResponse
```

---

### `get_exchanges`

List available cryptocurrency exchanges.

```python
get_exchanges() -> ExchangesResponse
```

---

### `get_exchange_symbols`

Get tradeable symbols for an exchange.

```python
get_exchange_symbols(
    exchange_id: str
) -> ExchangeSymbolsResponse
```

---

## Agent Tools

### `Agent` (class)

Persistent LLM agent with conversation history and Dawn SDK tool access. Uses litellm — supports Anthropic, OpenAI, Ollama, Gemini, and more. **The user's own API key is used, not Dawn's.**

```python
from dawnai.strategy.tools import Agent

agent = Agent(
    model: str,                    # e.g. 'claude-sonnet-4-6', 'gpt-4o', 'ollama/llama3'
    system_prompt: str = "",       # system prompt for the agent
    tools: list | None = None,     # tool functions or names; defaults to ALL SDK tools
)

response: str = agent.run(prompt: str)  # send message, get response (history preserved)
agent.clear_history()                    # reset conversation
```

**Stateful pattern — agent remembers across iterations:**
```python
from dawnai.strategy.tools import (
    Agent, get_prediction_market_prices, prediction_market_buy_token, read_portfolio,
)

agent = Agent(
    model="claude-sonnet-4-6",
    system_prompt="You are a prediction market trader. Track price trends across iterations and buy when momentum is strong.",
    tools=[get_prediction_market_prices, prediction_market_buy_token, read_portfolio],
)

for i in range(ITERATIONS):
    prices = get_prediction_market_prices(MARKET_ID)
    portfolio = read_portfolio()
    response = agent.run(f"Iteration {i}. Prices: {prices}. Portfolio: {portfolio}")
    print(response)
    time.sleep(INTERVAL)
```

### `run_agent` (function)

Stateless one-shot agent — creates a fresh Agent, runs once, discards history.

```python
run_agent(
    prompt: str,
    model: str,
    tools: list | None = None,
    system_prompt: str = "",
) -> str
```

```python
from dawnai.strategy.tools import run_agent

response = run_agent(
    "What NBA prediction markets have the most volume today?",
    model="claude-sonnet-4-6",
)
```

**Supported model formats:**
- Anthropic: `claude-sonnet-4-6`, `claude-opus-4-6`, `claude-haiku-4-5`
- OpenAI: `gpt-4o`, `gpt-4o-mini`, `o3`
- Ollama (local): `ollama/llama3`, `ollama/mistral`
- Google: `gemini/gemini-2.0-flash`
- Any provider supported by [litellm](https://docs.litellm.ai/docs/providers)

---

## Utility Tools

### `classify_text`

Classify text into one of the provided categories using AI. **Prefer this over hardcoded string matching.**

```python
classify_text(
    text: str,
    categories: list[str],
    question: str
) -> ClassifyTextResponse
```

Returns `ClassifyTextResponse(category: str)`.

**Code patterns:**
```python
# Sentiment analysis
result = classify_text(
    text=article_text,
    categories=["positive", "negative", "neutral"],
    question="What is the sentiment of this text regarding Bitcoin?"
)
sentiment = result.category  # "positive"

# Event outcome detection
result = classify_text(
    text=news_text,
    categories=["confirmed", "denied", "unclear"],
    question="Has the Bitcoin ETF been approved?"
)
```

---

### `get_state` / `set_state`

Per-strategy KV store backed by the server. Survives process restarts as long as the strategy name stays the same. Use it for caching token IDs, last-check timestamps, deduplication markers, and any small state you want to persist across iterations.

```python
from dawnai.strategy.tools import get_state, set_state
```

**Code pattern:**
```python
yes_token_id = get_state("yes_token_id")
if yes_token_id is None:
    market = get_prediction_market_details(market_id)
    yes_token_id = next(t.id for t in market.tokens if t.outcome.lower() == "yes")
    set_state("yes_token_id", yes_token_id)
```

### `read_budget`

Read the strategy's spend cap, cumulative BUY spend, and remaining headroom (server-computed). Use this only when you need to gate a decision on remaining headroom — every `polymarket_buy_token` is already server-enforced against the cap and rejects with `would_exceed_budget` if it would put you over.

```python
from dawnai.strategy.tools import read_budget

budget = read_budget()           # returns BudgetStatus(cap, spent, remaining) as Decimals
if budget.remaining < Decimal("5"):
    print("Out of room. Holding.")
    return
```

---

## Strategy Code Tips

### Import pattern

```python
from dawnai.strategy.tools import (
    prediction_market_event_search,
    get_prediction_market_details,
    get_prediction_market_prices,
    prediction_market_buy_token,
    prediction_market_sell_token,
    read_portfolio,
    read_budget,
    get_state,
    set_state,
    browser_search,
    classify_text,
)
```

### Market discovery workflow

```python
# 1. Search for events
events = prediction_market_event_search(query="Bitcoin price", limit=10)
for event in events.events:
    print(f"ID={event.id}, Title={event.title}, Markets={event.market_count}")

# 2. Get markets for an event
markets = prediction_market_event_markets(event_id=int(event.id), active=True)
for m in markets.markets:
    print(f"Market ID={m.id}, Q={m.question}")
    for token in (m.tokens or []):
        print(f"  Token {token.outcome}: {token.id}")

# 3. Get current price
prices = get_prediction_market_prices(market_id=m.id)
for token_id, price in prices.prices.items():
    print(f"  {token_id}: BUY={price.BUY}, SELL={price.SELL}")
```

### Reliable web monitoring

```python
# ALWAYS prefer specific APIs/URLs over browser_search alone
# If scraping a web page:
result = extract_text_from_urls(urls=[SPECIFIC_SOURCE_URL])

# Then classify the result — don't rely on exact string matching:
classification = classify_text(
    text=result.contents[0].text if result.contents else "",
    categories=["resolved_yes", "resolved_no", "still_pending"],
    question="What is the resolution status of this prediction market event?"
)
```

### Error handling

**Never raise exceptions in strategy code** — print the error and return or continue:

```python
def run_once():
    try:
        market = get_prediction_market_details(MARKET_ID)
        if market is None:
            print(f"[Error] Market not found: {MARKET_ID}")
            return
        # ... rest of logic
    except Exception as e:
        print(f"[Error] Unexpected error: {e}")
        return
```

### When a market resolves

When all relevant markets close, `prediction_market_sell_token` will automatically redeem tokens instead of selling on the order book. Call `terminate_strategy()` to stop the strategy:

```python
prices = get_prediction_market_prices(market_id=MARKET_ID)
if not prices.prices:
    print("Market closed. Terminating strategy.")
    terminate_strategy()
    return
```
