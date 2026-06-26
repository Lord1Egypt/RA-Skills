# ChainStream GraphQL Schema Guide

Complete reference for constructing valid ChainStream GraphQL queries.

## Schema Structure

The schema uses **chain group wrappers** as the top-level entry point. All cubes are nested under one of three wrappers:

```
type Query {
  EVM(network: EVMNetwork!, dataset: Dataset, aggregates: Aggregates): EVM!
  Solana(dataset: Dataset, aggregates: Aggregates): Solana!
  Trading(dataset: Dataset, aggregates: Aggregates): Trading!
}
```

## Query Format

### Solana — No network parameter

```graphql
query {
  Solana {
    DEXTrades(limit: {count: 25}, orderBy: {descending: Block_Time}) {
      Block { Time }
      Trade { Buy { Currency { MintAddress Symbol } Amount PriceInUSD } }
    }
  }
}
```

### EVM — network required (eth | bsc | polygon)

```graphql
query {
  EVM(network: eth) {
    DEXTrades(limit: {count: 25}, orderBy: {descending: Block_Time}) {
      Block { Time }
      Trade { Buy { Currency { MintAddress Symbol } Amount PriceInUSD } }
    }
  }
}
```

### Trading — Cross-chain pre-aggregated, no network parameter

```graphql
query {
  Trading {
    Pairs(tokenAddress: {is: "TOKEN_ADDRESS"}, limit: {count: 24}) {
      TimeMinute
      Token { Address }
      Price { Open High Low Close }
      VolumeUSD
    }
  }
}
```

### With GraphQL Variables

```graphql
query ($token: String!, $since: String) {
  Solana {
    DEXTradeByTokens(
      where: {Trade: {Currency: {MintAddress: {is: $token}}}, Block: {Time: {since: $since}}}
      limit: {count: 50}
      orderBy: {descending: Block_Time}
    ) {
      Block { Time }
      Trade { Currency { Symbol } Amount AmountInUSD Side { Type } }
    }
  }
}
```

Variables JSON: `{"token": "So11111111111111111111111111111111111111112", "since": "2026-04-01 00:00:00"}`

## Wrapper Parameters

### network (EVM only, required)

| Value | Chain |
|-------|-------|
| `eth` | Ethereum |
| `bsc` | BSC / BNB Chain |
| `polygon` | Polygon (required for Prediction Market cubes) |

Solana and Trading wrappers have no network parameter.

### dataset (optional, all wrappers)

| Value | Meaning |
|-------|---------|
| `realtime` | Recent data only (~last 1 day) |
| `archive` | Historical data (up to TTL) |
| `combined` | Full range (default) |

### aggregates (optional, all wrappers)

| Value | Meaning |
|-------|---------|
| `yes` | Prefer pre-aggregated tables when available |
| `no` | Use raw tables only |
| `only` | Only use pre-aggregated tables |

## Cube Parameters

### limit

```graphql
limit: {count: 25, offset: 0}
```

Default count is 25. Max varies by cube (check `graphql schema --type <cube>`). Absolute max is 10000.

### orderBy

Input object with four mutually exclusive fields:

```graphql
orderBy: {descending: Block_Time}
orderBy: {ascending: Block_Time}
orderBy: {descendingByField: "count"}
orderBy: {ascendingByField: "Trade_Buy_AmountInUSD_sum"}
```

- `descending` / `ascending`: enum value matching a dimension path (e.g. `Block_Time`, `Trade_Buy_Amount`)
- `descendingByField` / `ascendingByField`: string referencing a computed/aggregated field name

### where

Nested filter object following the dimension hierarchy:

```graphql
where: {
  Block: {Time: {since: "2026-04-01 00:00:00"}}
  Trade: {Buy: {Currency: {MintAddress: {is: "TOKEN_ADDRESS"}}}}
}
```

### limitBy (per-group row limit, ClickHouse LIMIT BY)

```graphql
limitBy: {by: Trade_Buy_Currency_MintAddress, count: 1}
```

Returns top N rows per group value.

## Filter Operators

| Type | Operators | Example |
|------|-----------|---------|
| **StringFilter** | `is`, `not`, `in`, `notIn`, `like`, `notLike`, `includes`, `notIncludes`, `startsWith`, `endsWith`, `includesCaseInsensitive`, `startsWithCaseInsensitive`, `likeCaseInsensitive`, `notLikeCaseInsensitive` | `{is: "0xabc..."}` |
| **IntFilter** | `eq`, `ne`, `gt`, `ge`, `lt`, `le`, `in`, `notIn` | `{gt: 1000}` |
| **FloatFilter** | `eq`, `ne`, `gt`, `ge`, `lt`, `le` | `{ge: 0.5}` |
| **DecimalFilter** | `eq`, `ne`, `gt`, `ge`, `lt`, `le` | `{gt: "1000000"}` (string value) |
| **DateTimeFilter** | `is`, `not`, `since`, `till`, `after`, `before`, `in`, `notIn` | `{since: "2026-03-24 00:00:00"}` |
| **BoolFilter** | `is` | `{is: true}` |

### OR Conditions (any)

Wrap multiple filter objects in `any: [...]` to combine with OR logic:

```graphql
where: {
  any: [
    {Transfer: {Sender: {Address: {is: "WALLET"}}}}
    {Transfer: {Receiver: {Address: {is: "WALLET"}}}}
  ]
}
```

### CRITICAL: DateTime Filters

DateTime fields (e.g. `Block.Time`) use **DateTimeFilter** — NOT IntFilter!

```
WRONG: Block: {Time: {gt: "2026-03-24 00:00:00"}}     <- gt does NOT exist on DateTimeFilter
RIGHT: Block: {Time: {since: "2026-03-24 00:00:00"}}   <- use since/after/before/till
```

## Date/Time Format

The database uses ClickHouse DateTime64. You MUST use this format:

```
"2026-03-31 00:00:00"   <- CORRECT (space-separated, no T, no Z)
"2026-03-31T00:00:00Z"  <- WRONG — causes ClickHouse TYPE_MISMATCH error
"2026-03-31"             <- WRONG — must include time portion
```

For relative time queries, compute the actual date string:
- "last 7 days" -> `since: "2026-03-31 00:00:00"`
- "last 24 hours" -> `since: "2026-04-06 00:00:00"`

## Metrics (Aggregation)

Available metrics: `count`, `sum`, `avg`, `min`, `max`, `uniq`

| Usage | SQL Equivalent |
|-------|---------------|
| `count` | `COUNT(*)`  |
| `count(of: Field)` | `COUNT(DISTINCT field)` |
| `sum(of: Field)` | `SUM(field)` |
| `avg(of: Field)` | `AVG(field)` |
| `uniq(of: Field)` | `uniqExact(field)` |

**Key rule**: For a total aggregate (single number), select ONLY the metric — do NOT include dimension fields. If you include dimension fields alongside a metric, results are grouped by those dimensions.

```graphql
# Total count (no grouping)
query { Solana { DEXTrades(where: {...}) { count } } }

# Count grouped by Dex
query { Solana { DEXTrades(where: {...}) { Trade { Dex { ProtocolName } } count } } }
```

### Conditional Aggregation (if)

Add a WHERE condition to individual metrics using `if`:

```graphql
buys: count(if: {Trade: {Side: {Type: {is: "buy"}}}})
sells: count(if: {Trade: {Side: {Type: {is: "sell"}}}})
buy_volume: sum(of: Trade_Amount, if: {Trade: {Side: {Type: {is: "buy"}}}})
```

### selectWhere (HAVING)

Filter on the aggregated result value:

```graphql
volume: sum(of: Trade_Side_AmountInUSD, selectWhere: {gt: "0"})
```

### calculate (Computed Expressions)

Reference other aliased metrics/fields with `$` prefix:

```graphql
buy_vol: sum(of: Trade_Amount, if: {Trade: {Side: {Type: {is: "buy"}}}})
sell_vol: sum(of: Trade_Amount, if: {Trade: {Side: {Type: {is: "sell"}}}})
RealizedPnL: calculate(expression: "$sell_vol - $buy_vol")
avg_price: calculate(expression: "$buy_volume_usd / $buy_volume")
```

### quantile

```graphql
median_price: quantile(of: Trade_PriceInUSD, level: 0.5)
p99_price: quantile(of: Trade_PriceInUSD, level: 0.99)
```

## Dimension-Level Aggregation (argMax / argMin)

Select a dimension's value at the row where another column is maximum or minimum:

```graphql
# Get the PostBalance at the maximum Block_Slot (latest balance)
BalanceUpdate {
  Balance: PostBalance(maximum: Block_Slot)
}

# OHLCV via DEXTradeByTokens — open price at min slot, close price at max slot
Trade {
  open: Price(minimum: Block_Slot)
  close: Price(maximum: Block_Slot)
  high: Price(maximum: Trade_Price)
  low: Price(minimum: Trade_Price)
}
```

## Time Interval Bucketing

Group timestamps into fixed intervals using the `interval` argument:

```graphql
Block {
  Timefield: Time(interval: {in: minutes, count: 5})
}
```

Supported units: `seconds`, `minutes`, `hours`, `days`, `weeks`, `months`.

Combined with dimension aggregation, this enables OHLCV candle construction from raw trades.

## Cross-Cube JOIN (joinXxx)

**ALWAYS prefer joinXxx over multiple separate queries.** When a user wants data from related cubes, generate ONE query with joinXxx fields.

joinXxx adds a LEFT JOIN to the target cube, returning related fields inline.

### Available Joins

| Source Cube | Join Field | Target Cube |
|-------------|-----------|-------------|
| **DEXTrades** | `joinTransfers` | Transfers |
| **DEXTrades** | `joinBalanceUpdates` | BalanceUpdates |
| **DEXTrades** | `joinDEXPoolEvents` | DEXPoolEvents |
| **Transactions** | `joinEvents` | Events (EVM only) |
| **Transactions** | `joinCalls` | Calls (EVM only) |
| **Transactions** | `joinDEXTrades` | DEXTrades |
| **Transactions** | `joinTransfers` | Transfers |
| **Transactions** | `joinInstructions` | Instructions (Solana only) |
| **Transactions** | `joinRewards` | Rewards (Solana only) |
| **BalanceUpdates** | `joinDEXTrades` | DEXTrades |
| **BalanceUpdates** | `joinTransfers` | Transfers |
| **DEXPoolEvents** | `joinDEXTrades` | DEXTrades |
| **Transfers** | `joinDEXTrades` | DEXTrades |
| **Transfers** | `joinBalanceUpdates` | BalanceUpdates |

### Example: Solana Transaction with Full Details

```graphql
query {
  Solana {
    Transactions(limit: {count: 1}, orderBy: {descending: Block_Time}) {
      Block { Time Slot Height Hash }
      Transaction { Signature Fee FeePayer Signer }
      joinInstructions {
        Instruction { Program { Id Name Method } }
      }
      joinDEXTrades {
        Trade { Buy { Currency { MintAddress } Amount PriceInUSD } }
      }
      joinTransfers {
        Transfer { Currency { MintAddress } Amount AmountInUSD }
      }
    }
  }
}
```

### Example: EVM Transaction with Logs and Traces

```graphql
query {
  EVM(network: eth) {
    Transactions(limit: {count: 1}, orderBy: {descending: Block_Time}) {
      Block { Time Number Hash }
      Transaction { Hash From To Value }
      joinEvents {
        Log { Address EventName Topics { Topic0 Topic1 } Data }
      }
      joinCalls {
        Call { CallType FromAddress ToAddress ValueInNative GasUsed }
      }
    }
  }
}
```

### Constraints

- Max 1 level of join (no nested joins)
- LEFT JOIN only

## DEXTradeByTokens — Token-Centric Trade View

`DEXTradeByTokens` provides a **token-centric** view of DEX trades by performing a `UNION ALL` of buy and sell sides from `DEXTrades`. Each row has the queried token as the primary `Currency`, with `Trade.Side.Type` (`buy` or `sell`) indicating the trade direction.

### When to Use

| Scenario | Cube |
|----------|------|
| Analyze a specific token's all trades (buy + sell) in one query | **DEXTradeByTokens** |
| See buy/sell ratio, volume breakdown by direction | **DEXTradeByTokens** (group by `Trade.Side.Type`) |
| Construct OHLCV candles from raw trades | **DEXTradeByTokens** (with time interval + dim agg) |
| Analyze a specific trade pair (buy token vs sell token) | DEXTrades |

## Common Mistakes

| WRONG | CORRECT | Note |
|-------|---------|------|
| `CubeName(network: sol)` | `Solana { CubeName(...) }` | Must use chain group wrapper |
| `network: sol` on cube | `EVM(network: eth)` or `Solana(network: solana)` on wrapper | network is a wrapper-level param on EVM (required) and Solana (optional, defaults to `solana`) |
| `orderBy: Block_Time_DESC` | `orderBy: {descending: Block_Time}` | orderBy is an InputObject, not an enum |
| `Block: {Time: {gt: "..."}}` | `Block: {Time: {since: "..."}}` | DateTimeFilter, not IntFilter |
| `"2026-03-31T00:00:00Z"` | `"2026-03-31 00:00:00"` | ClickHouse format, no T/Z |
| `Block { Number }` (Solana) | `Block { Slot }` or `Block { Height }` | Solana uses Slot/Height, not Number |
| Two queries for related data | One query with `joinXxx` | Single query principle |
| `{eq: true}` for Bool filter | `{is: true}` | BoolFilter uses `is`, not `eq` |

## Rules Summary

1. **MUST** use a chain group wrapper (`Solana`, `EVM`, or `Trading`) as the top-level field.
2. **MUST** include `network` parameter on `EVM` wrapper (not needed for Solana/Trading).
3. **STRICTLY** use only field names from the schema. NEVER invent fields.
4. Field names are **CASE-SENSITIVE** and must match exactly.
5. Date/time values **MUST** use `"YYYY-MM-DD HH:MM:SS"` format.
6. DateTime filters **MUST** use `since`/`after`/`before`/`till`.
7. **SINGLE QUERY PRINCIPLE**: Use joinXxx to combine related data.
8. Default limit 25. Use `{descending: Block_Time}` as default orderBy.
