---
name: dscvr-skills
description: >
  Query DSCVR crypto intelligence APIs for market news, event tracking, smart money analysis,
  prediction market data, AI-powered event discovery, market orderbooks, and social graph data.
  Use this skill when the user asks about crypto news events, market event categories, event
  details, smart money traders, prediction market listings, whale wallet tracking, AI discovery
  events, market orderbook depth, DSCVR social profiles, or wants to retrieve intelligence
  data from DSCVR. Also use when the user mentions DSCVR API, subscription data, or needs to
  fetch crypto/blockchain event information, smart money flows, prediction market positions,
  or DSCVR user/portal data via GraphQL.
  Handles HMAC-SHA256 authenticated API calls automatically.
license: Proprietary
compatibility: Requires uv (https://docs.astral.sh/uv/) and Python 3.10+. Requires network access to the DSCVR API server.
metadata:
  author: dscvr.one
  version: "1.0.0"
---

# DSCVR Intelligence Skill

Query DSCVR's crypto intelligence APIs to retrieve market news events, event categories, and detailed event analysis. All API calls are authenticated via HMAC-SHA256 signing.

## Prerequisites

Before using this skill, ensure:

1. **uv** is installed — see [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/)
2. **Python 3.10+** is available (uv can install it for you: `uv python install 3.10`)
3. **API credentials** are configured — you need an `api_key` and `secret_key` obtained from a DSCVR subscription at [dscvr.one/subscription](https://dscvr.one/subscription).

No manual `pip install` needed — scripts declare their dependencies inline via [PEP 723](https://packaging.python.org/en/latest/specifications/inline-script-metadata/), and `uv run` resolves them automatically.

## Configuration

The skill needs two environment variables (or they can be passed as arguments to scripts):

| Variable | Description |
|---|---|
| `DSCVR_API_KEY` | Your 16-character public API key |
| `DSCVR_SECRET_KEY` | Your 32-character secret key |
| `DSCVR_API_BASE_URL` | API server base URL (default: `https://dscvr.one`) |

## Available Tools

### 1. Get Event Categories

Retrieve all available news event categories.

```bash
uv run scripts/dscvr_api.py categories
```

Returns a list of event categories with `id`, `name`, and `image_url`.

### 2. Get Event List

Retrieve paginated news events, optionally filtered by category and date.

```bash
uv run scripts/dscvr_api.py events [--category CATEGORY] [--date YYYY-MM-DD] [--page N] [--limit N]
```

**Parameters:**
- `--category`: Filter by category name (optional)
- `--date`: Filter by date in YYYY-MM-DD format (optional)
- `--page`: Page number, starting from 1 (default: 1)
- `--limit`: Results per page (default: 10)

### 3. Get Event Detail

Retrieve detailed information about a specific event.

```bash
uv run scripts/dscvr_api.py event-detail --event-id EVENT_ID
```

**Parameters:**
- `--event-id`: The event ID (required)

### 4. Smart Money Traders

List smart money traders with rich filtering options.

```bash
uv run scripts/dscvr_api.py smart-money [--keyword KW] [--win-rate HOT,STEADY,REVERSE] [--position-state ACTIVE,STREAK,SAFE] [--tx-size WHALE,MID,SMALL] [--style SWING,DIAMOND,HOT_ONLY] [--identity BOT,HUMAN,INSIDER] [--category politics,crypto,...] [--sort FIELD] [--ascending] [--page N] [--limit N]
```

**Parameters:**
- `--keyword`: Fuzzy search by name or bio (optional)
- `--win-rate`: Win rate filter, comma-separated: `HOT`, `STEADY`, `REVERSE` (optional)
- `--position-state`: Position state, comma-separated: `ACTIVE`, `STREAK`, `SAFE` (optional)
- `--tx-size`: Transaction size, comma-separated: `WHALE`, `MID`, `SMALL`, `SMALL_LOSS`, `MID_LOSS` (optional)
- `--style`: Position style, comma-separated: `SWING`, `DIAMOND`, `HOT_ONLY` (optional)
- `--identity`: Identity type, comma-separated: `BOT`, `HUMAN`, `INSIDER` (optional)
- `--category`: Domain category, comma-separated: `politics`, `sports`, `crypto`, `economy`, `elections`, `culture`, `finance`, `mentions`, `world`, `geopolitics`, `earnings`, `climate_science`, `tech` (optional)
- `--sort`: Sort field: `TOTAL_PNL`, `WIN_RATE`, `TOTAL_TRADE_COUNT`, `TOTAL_TURNOVER`, `AVG_HOLD_TIME` (default: `TOTAL_PNL`)
- `--ascending`: Sort ascending instead of descending (optional)
- `--page`: Page number (default: 1)
- `--limit`: Results per page (default: 20, max: 100)

### 5. Prediction Market Categories

List all available prediction market categories.

```bash
uv run scripts/dscvr_api.py market-categories [--source polymarket]
```

**Parameters:**
- `--source`: Data source (default: `polymarket`)

### 6. Prediction Market Listings

Browse prediction markets with filtering and smart money signals.

```bash
uv run scripts/dscvr_api.py markets [--source SRC] [--category CAT] [--smart-filter all|smart_money] [--sort FIELD] [--page N] [--limit N]
```

**Parameters:**
- `--source`: Data source (default: `polymarket`)
- `--category`: Category filter (default: `all`)
- `--smart-filter`: `all` or `smart_money` — filter to only show events with smart money activity (default: `all`)
- `--sort`: Sort field (prefix with `-` for ascending): `smart_money_activity`, `volume_24h`, `liquidity`, `close_time`
- `--page`: Page number (default: 1)
- `--limit`: Results per page (default: 20, max: 100)

### 7. Event Traders

Get smart money traders and their positions for a specific prediction market event.

```bash
uv run scripts/dscvr_api.py event-traders --event-id EVENT_ID [--page N] [--limit N]
```

**Parameters:**
- `--event-id`: The event ID (required)
- `--page`: Page number (default: 1)
- `--limit`: Results per page (default: 5, max: 10)

### 8. AI Discovery Categories

List all AI discovery event categories.

```bash
uv run scripts/dscvr_api.py ai-categories
```

### 9. AI Discovery Events

Browse AI-curated prediction market events with filters.

```bash
uv run scripts/dscvr_api.py ai-events [--category CAT] [--platform PLAT] [--active] [--page N] [--limit N]
```

**Parameters:**
- `--category`: Category filter (default: `All`)
- `--platform`: Platform filter (optional)
- `--active`: Only show active events (optional)
- `--page`: Page number (default: 1)
- `--limit`: Results per page (default: 10)

### 10. AI Event Search

Search AI discovery events by keyword.

```bash
uv run scripts/dscvr_api.py ai-search --query KEYWORD [--page N] [--limit N]
```

**Parameters:**
- `--query`: Search keyword (required)
- `--page`: Page number (default: 1)
- `--limit`: Results per page (default: 10)

### 11. AI Event Detail

Get detailed AI analysis for a specific event.

```bash
uv run scripts/dscvr_api.py ai-event-detail --provider PROVIDER --event-id EVENT_ID
```

**Parameters:**
- `--provider`: Provider name (required)
- `--event-id`: Event ID (required)

### 12. Market Orderbook

Get orderbook depth data for a prediction market.

```bash
uv run scripts/dscvr_api.py ai-orderbook [--kalshi-id ID] [--polymarket-id ID]
```

**Parameters:**
- `--kalshi-id`: Kalshi market ID (optional)
- `--polymarket-id`: Polymarket market ID (optional)
- At least one ID is required.

### 13. Social GraphQL

Query the DSCVR social graph via GraphQL. Supports user lookup, content lookup, portal lookup, and more.

```bash
uv run scripts/dscvr_api.py social-graphql --query '{ userByName(name: "alice") { id username followerCount } }'
```

**Parameters:**
- `--query`: GraphQL query string (required)

**Available queries:**
- `user(id: DscvrId!)` — Lookup user by principal ID
- `userByName(name: String!)` — Lookup user by username
- `content(id: ContentId!)` — Lookup content by ID
- `portalBySlug(slug: String!)` — Lookup portal by slug
- `portalById(id: PortalId!)` — Lookup portal by ID

## Authentication

All API calls use HMAC-SHA256 request signing. The skill handles this automatically via `scripts/auth.py`. Three headers are sent with every request:

| Header | Value |
|---|---|
| `X-API-Key` | Your public API key |
| `X-Timestamp` | Current Unix timestamp (seconds) |
| `X-Signature` | `HMAC-SHA256(secret_key, "{api_key}:{timestamp}")` hex digest |

The timestamp must be within 5 minutes of the server's time. See [references/auth-reference.md](references/auth-reference.md) for the full signing specification.

## Usage Examples

### Example 1: Browse event categories

**User prompt:** "What crypto event categories does DSCVR track?"

**Steps:**
1. Run `uv run scripts/dscvr_api.py categories`
2. Present the category list to the user in a readable format

### Example 2: Get recent events for a category

**User prompt:** "Show me the latest DeFi news events"

**Steps:**
1. First run `uv run scripts/dscvr_api.py categories` to find the matching category
2. Run `uv run scripts/dscvr_api.py events --category "DeFi"` to get events
3. Summarize the events for the user, highlighting key headlines and related coins

### Example 3: Deep dive into a specific event

**User prompt:** "Tell me more about event #42"

**Steps:**
1. Run `uv run scripts/dscvr_api.py event-detail --event-id 42`
2. Present the full event details including sources, related coins, and analysis

### Example 4: Daily market briefing

**User prompt:** "Give me today's crypto market briefing"

**Steps:**
1. Run `uv run scripts/dscvr_api.py categories` to get all categories
2. Run `uv run scripts/dscvr_api.py events --date $(date +%Y-%m-%d) --limit 10` for today's top events
3. Synthesize the events into a coherent market briefing

### Example 5: Find top smart money traders

**User prompt:** "Show me the top whale traders in crypto with the highest PnL"

**Steps:**
1. Run `uv run scripts/dscvr_api.py smart-money --tx-size WHALE --category crypto --sort TOTAL_PNL --limit 10`
2. Present the traders with their win rates, PnL, and recent activity

### Example 6: Explore prediction markets

**User prompt:** "What prediction markets are trending with smart money?"

**Steps:**
1. Run `uv run scripts/dscvr_api.py markets --smart-filter smart_money --sort smart_money_activity --limit 10`
2. Summarize the top markets, highlighting smart money positions and popular outcomes

### Example 7: Analyze smart money positions on an event

**User prompt:** "Who are the smart money traders betting on the Fed decision event?"

**Steps:**
1. Run `uv run scripts/dscvr_api.py markets --category all --limit 50` to find the Fed decision event
2. Run `uv run scripts/dscvr_api.py event-traders --event-id <EVENT_ID>` with the found event ID
3. Present each trader's positions, realized/unrealized PnL, and trade direction

### Example 8: Search AI discovery events

**User prompt:** "Find prediction market events about the US election"

**Steps:**
1. Run `uv run scripts/dscvr_api.py ai-search --query "US election" --limit 10`
2. Present the matching events with their categories and status

### Example 9: Get market orderbook

**User prompt:** "Show me the orderbook for this Polymarket event"

**Steps:**
1. Run `uv run scripts/dscvr_api.py ai-orderbook --polymarket-id <MARKET_ID>`
2. Present the bid/ask depth and current prices

### Example 10: Look up a DSCVR user

**User prompt:** "Find the DSCVR profile for user PopularDude99"

**Steps:**
1. Run `uv run scripts/dscvr_api.py social-graphql --query '{ userByName(name: "PopularDude99") { id username followerCount } }'`
2. Present the user's profile information

## Error Handling

| Error | Meaning | Action |
|---|---|---|
| `401 Unauthorized` | Invalid API key, bad signature, or expired timestamp | Check credentials and system clock |
| `403 Forbidden` | API key is temporarily banned (1-min cooldown after auth failure) | Wait 60 seconds and retry |
| `404 Not Found` | Endpoint or resource doesn't exist | Verify the endpoint path |
| `429 Too Many Requests` | Rate limit exceeded (100 req/min default) | Wait and retry with backoff |
| `502 Bad Gateway` | Upstream DSCVR service unavailable | Retry after a short delay |

## API Endpoint Pattern

All product endpoints follow the pattern:
```
/developer/v1/product/<module>/<endpoint>
```

Currently available modules:
- `news` — Crypto news and event intelligence
- `market` — Smart money analytics and prediction market data
- `ai` — AI-powered event discovery, search, and market orderbooks
- `social` — DSCVR social graph (GraphQL)

See [references/api-reference.md](references/api-reference.md) for the complete API documentation.
