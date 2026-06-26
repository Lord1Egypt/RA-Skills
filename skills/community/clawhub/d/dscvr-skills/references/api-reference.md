# DSCVR Intelligence API Reference

Complete documentation for all available API endpoints.

## Base URL

```
https://dscvr.one
```

All endpoints are prefixed with `/developer/v1/product/`.

## Endpoint Pattern

```
/developer/v1/product/<module>/<endpoint>
```

---

## Module: News

### 1. Get Event Categories

Retrieve all available event categories.

**Endpoint:** `GET /developer/v1/product/news/event_category`

**Parameters:** None

**Response:**
```json
[
  {
    "id": 1,
    "name": "DeFi",
    "image_url": "https://example.com/defi.png"
  },
  {
    "id": 2,
    "name": "NFT",
    "image_url": "https://example.com/nft.png"
  }
]
```

**Example:**
```bash
python scripts/dscvr_api.py categories
```

---

### 2. Get Event List

Retrieve a paginated list of news events.

**Endpoint:** `GET /developer/v1/product/news/event_list`

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `category` | string | No | — | Filter by category name |
| `date` | string | No | — | Filter by date (YYYY-MM-DD format) |
| `page` | integer | No | 1 | Page number |
| `limit` | integer | No | 20 | Results per page |

**Response:**
```json
{
  "total": 150,
  "page": 1,
  "limit": 20,
  "events": [
    {
      "event_id": 42,
      "headline": "Major DeFi Protocol Reaches $10B TVL",
      "short_summary": "A leading DeFi protocol has crossed the $10 billion TVL milestone...",
      "event_time": "1774338406",
      "category": "DeFi",
      "sources": [
        {
          "url": "https://example.com/article",
          "title": "Source Article",
          "tag": "news"
        }
      ],
      "coins": [
        {
          "coin_id": 1,
          "name": "ETH",
          "image_url": "https://example.com/eth.png"
        }
      ]
    }
  ]
}
```

**Example:**
```bash
# Get all events
python scripts/dscvr_api.py events

# Filter by category and date
python scripts/dscvr_api.py events --category "DeFi" --date "2026-03-24"

# Paginate
python scripts/dscvr_api.py events --page 2 --limit 10
```

---

### 3. Get Event Detail

Retrieve detailed information about a specific event.

**Endpoint:** `GET /developer/v1/product/news/event_detail`

**Query Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `event_id` | string | Yes | The unique event identifier |

**Response:**
```json
{
  "event_id": 42,
  "headline": "Major DeFi Protocol Reaches $10B TVL",
  "short_summary": "A leading DeFi protocol has crossed the $10 billion TVL milestone...",
  "full_content": "Detailed analysis of the event...",
  "event_time": "1774338406",
  "category": "DeFi",
  "sources": [
    {
      "url": "https://example.com/article",
      "title": "Source Article",
      "tag": "news"
    }
  ],
  "coins": [
    {
      "coin_id": 1,
      "name": "ETH",
      "image_url": "https://example.com/eth.png"
    }
  ]
}
```

**Example:**
```bash
python scripts/dscvr_api.py event-detail --event-id 42
```

---

## Response Envelope

The upstream DSCVR backend wraps all responses in an envelope:

```json
{
  "code": 0,
  "msg": "Success",
  "data": { ... }
}
```

The proxy server strips this envelope and returns only the `data` field. If the upstream returns a non-zero `code`, the proxy returns HTTP 502.

---

## Rate Limiting

- Default: **100 requests per minute** per API key
- Exceeding the limit returns HTTP 429
- The counter resets on a sliding 1-minute window

---

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error description"
}
```

| HTTP Code | Meaning |
|---|---|
| 400 | Bad request (missing or invalid parameters) |
| 401 | Authentication failed |
| 403 | API key temporarily banned |
| 404 | Resource not found |
| 429 | Rate limit exceeded |
| 502 | Upstream service error |

---

## Module: Market (Smart Money & Prediction Markets)

### 4. Smart Money Trader List

List smart money traders with comprehensive filtering.

**Endpoint:** `POST /developer/v1/product/market/smart_money/list`

**Request Body (JSON):**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `search_keyword` | string | No | — | Fuzzy search by name or bio |
| `win_rate_range` | array[string] | No | — | `HOT`, `STEADY`, `REVERSE` |
| `position_state` | array[string] | No | — | `ACTIVE`, `STREAK`, `SAFE` |
| `transaction_size` | array[string] | No | — | `WHALE`, `MID`, `SMALL`, `SMALL_LOSS`, `MID_LOSS` |
| `position_style` | array[string] | No | — | `SWING`, `DIAMOND`, `HOT_ONLY` |
| `is_human` | array[string] | No | — | `BOT`, `HUMAN`, `INSIDER` |
| `category` | array[string] | No | — | `politics`, `sports`, `crypto`, `economy`, `elections`, `culture`, `finance`, `mentions`, `world`, `geopolitics`, `earnings`, `climate_science`, `tech` |
| `sort_by` | string | No | `TOTAL_PNL` | `TOTAL_PNL`, `WIN_RATE`, `TOTAL_TRADE_COUNT`, `TOTAL_TURNOVER`, `AVG_HOLD_TIME` |
| `is_ascending` | boolean | No | `false` | Sort direction |
| `limit` | integer | No | 20 | Results per page (1–100) |
| `page` | integer | No | 1 | Page number |

**Response (each item in `data` array):**

| Field | Description |
|---|---|
| `address` | Wallet address |
| `win_rate` | Win rate (0–1) |
| `consecutive_wins` | Current consecutive win streak |
| `max_consecutive_wins` | Historical max consecutive wins |
| `daily_avg_trades` | Average daily trade count |
| `insider_trades_count` | Insider trade count |
| `financial_trades_count` | Financial category trade count |
| `diamond_hands_count` | Long-term hold count |
| `tags` | Labels: `win_rate_range`, `position_state`, `transaction_size`, `position_style`, `categories`, `is_human` |
| `profile` | `name`, `nick`, `icon_url`, `created_at` |
| `total_pnl` | Cumulative PnL |
| `total_pnl_change_rate` | PnL change rate |
| `total_trade_count` | Total trades |
| `total_turnover` | Total turnover |
| `avg_hold_time` | Average hold time (hours) |
| `last_active_time` | Last active timestamp |
| `pnl_trend` | Daily PnL trend (last 30 days): `pnl_date`, `daily_total_pnl` |
| `grid_heatmap` | Recent 20 events heatmap: `event_id`, `slug`, `title`, `total_pnl`, `resolved_count`, `realized_pnl_cum` |
| `last_trades` | Last 2 trades: `event_id`, `slug`, `title`, `realized_pnl_cum` |

**Example:**
```bash
uv run scripts/dscvr_api.py smart-money --tx-size WHALE --category crypto --sort TOTAL_PNL --limit 10
```

---

### 5. Market Categories

List all prediction market categories.

**Endpoint:** `GET /developer/v1/product/market/market/category`

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `source` | string | No | `polymarket` | Data source |

**Response:**
```json
[
  { "category_id": 1, "category_name": "Politics" },
  { "category_id": 2, "category_name": "Crypto" }
]
```

**Example:**
```bash
uv run scripts/dscvr_api.py market-categories
```

---

### 6. Market Listings

Browse prediction markets with smart money signals.

**Endpoint:** `GET /developer/v1/product/market/market/list`

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `source` | string | No | `polymarket` | Data source |
| `category` | string | No | `all` | Category filter |
| `smart_filter` | string | No | `all` | `all` or `smart_money` |
| `sort_by` | string | No | `smart_money_activity` | Sort field (prefix `-` for asc) |
| `limit` | integer | No | 20 | Results per page (max 100) |
| `page` | integer | No | 1 | Page number |

**Sort options:** `smart_money_activity`, `volume_24h`, `liquidity`, `close_time` (prefix with `-` for ascending)

**Response (each item in `data` array):**

| Field | Description |
|---|---|
| `event_id` | Event ID |
| `img` | Event image URL |
| `title` | Event title |
| `liquidity` | Total liquidity |
| `volume_24h` | 24h trading volume |
| `close_time` | Event close time |
| `last_trade_time` | Last trade timestamp |
| `source` | Data source |
| `holders` | Smart money holder count |
| `smart_money_trader_count` | Total smart money traders |
| `insider_count` | Insider address count |
| `smart_money_trader_count_24h` | 24h smart money traders |
| `smart_money_position_amount` | Smart money position count |
| `smart_money_position_volume` | Smart money position value |
| `most_popular_market_choice` | Most popular outcome: `market_name`, `token`, `price`, `most_popular_choice_percent` |
| `outcome_data` | Outcome list: `token`, `tag`, `price`, `title` |

**Example:**
```bash
uv run scripts/dscvr_api.py markets --smart-filter smart_money --sort smart_money_activity --limit 10
```

---

### 7. Event Traders

Get smart money traders and their positions for a specific event.

**Endpoint:** `GET /developer/v1/product/market/market/event_trader`

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `event_id` | integer | Yes | — | Event ID |
| `limit` | integer | No | 5 | Results per page (max 10) |
| `page` | integer | No | 1 | Page number |

**Response:** Dictionary keyed by wallet address, each value is an array of positions:

| Field | Description |
|---|---|
| `event_id` | Event ID |
| `market_id` | Market ID |
| `title` | Market title |
| `token` | Direction (Yes/No) |
| `position_value` | Position value |
| `realized_pnl_cum` | Realized PnL |
| `unrealized_pnl_cum` | Unrealized PnL |
| `last_side` | Last trade direction (BUY/SELL) |
| `last_amount` | Last trade amount |
| `last_trade_time` | Last trade timestamp |

**Example:**
```bash
uv run scripts/dscvr_api.py event-traders --event-id 100989
```

---

## Module: AI Discovery

### 8. AI Categories

List all AI discovery event categories.

**Endpoint:** `GET /developer/v1/product/ai/category_list`

**Parameters:** None

**Example:**
```bash
uv run scripts/dscvr_api.py ai-categories
```

---

### 9. AI Event List

Browse AI-curated prediction market events.

**Endpoint:** `GET /developer/v1/product/ai/event_list`

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `category` | string | No | `All` | Category filter |
| `page` | integer | No | 1 | Page number |
| `limit` | integer | No | 10 | Results per page |
| `platform` | string | No | — | Platform filter |
| `is_active` | boolean | No | — | Only active events |

**Example:**
```bash
uv run scripts/dscvr_api.py ai-events --category crypto --active --limit 10
```

---

### 10. AI Event Search

Search AI discovery events by keyword.

**Endpoint:** `GET /developer/v1/product/ai/event_search`

**Query Parameters:**

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | Yes | — | Search keyword |
| `page` | integer | No | 1 | Page number |
| `limit` | integer | No | 10 | Results per page |

**Example:**
```bash
uv run scripts/dscvr_api.py ai-search --query "US election" --limit 10
```

---

### 11. AI Event Detail

Get detailed AI analysis for a specific event.

**Endpoint:** `GET /developer/v1/product/ai/event_detail`

**Query Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `provider` | string | Yes | Provider name |
| `event_id` | string | Yes | Event ID |

**Example:**
```bash
uv run scripts/dscvr_api.py ai-event-detail --provider polymarket --event-id 12345
```

---

### 12. Market Orderbook

Get orderbook depth data for a prediction market.

**Endpoint:** `GET /developer/v1/product/ai/market_orderbook`

**Query Parameters:**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `kalshi_market_id` | string | No | Kalshi market ID |
| `polymarket_market_id` | string | No | Polymarket market ID |

At least one market ID is required.

**Example:**
```bash
uv run scripts/dscvr_api.py ai-orderbook --polymarket-id 0x1234abcd
```

---

## Module: Social

### 13. GraphQL Query

Execute a GraphQL query against the DSCVR social API.

**Endpoint:** `POST /developer/v1/product/social/graphql`

**Request Body (JSON):**

| Parameter | Type | Required | Description |
|---|---|---|---|
| `query` | string | Yes | GraphQL query string |

**Available queries:**
- `user(id: DscvrId!)` — Lookup user by principal ID
- `userByName(name: String!)` — Lookup user by username
- `content(id: ContentId!)` — Lookup content by ID
- `portalBySlug(slug: String!)` — Lookup portal by slug
- `portalById(id: PortalId!)` — Lookup portal by ID
- `unpackFrameMessage(message: String!)` — Unpack frame message

**Example:**
```bash
uv run scripts/dscvr_api.py social-graphql --query '{ userByName(name: "PopularDude99") { id username followerCount } }'
```
