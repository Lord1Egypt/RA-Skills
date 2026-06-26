# Bitquery Trading.Tokens — GraphQL Field Reference

Full reference for the fields available in the `Trading.Tokens` **query** and **subscription** on the Bitquery streaming API. For real-time streaming, use a `subscription` with the same structure (no `limit`/`orderBy`); the skill uses the subscription for the live Bitcoin price feed.

## Query / Subscription Structure

```graphql
{
  Trading {
    Tokens(
      where: <FilterInput>
      limit: <LimitInput>
      orderBy: <OrderByInput>
    ) {
      Token { ... }
      Block { ... }
      Interval { ... }
      Volume { ... }
      Price { ... }
    }
  }
}
```

---

## Filters (`where`)

### Currency / Token Filters

| Filter | Description | Example |
|--------|-------------|---------|
| `Currency.Id.is` | Match a specific token by Bitquery ID | `"bid:bitcoin"` |
| `Currency.SmartContract.is` | Match by contract address | `"0xabc...def"` |
| `Currency.Symbol.is` | Match by ticker symbol | `"BTC"` |

**Common `bid:` token IDs:**
- `bid:bitcoin` — Bitcoin

### Time / Interval Filters

| Filter | Description | Example |
|--------|-------------|---------|
| `Interval.Time.Duration.eq` | Candle duration: 1 = 1 second (tick); 5, 60, 1440 = minutes | `1`, `5`, `60`, `1440` |
| `Block.Time.after` | Filter data after this ISO timestamp | `"2025-01-01T00:00:00Z"` |
| `Block.Time.before` | Filter data before this ISO timestamp | `"2025-12-31T23:59:59Z"` |
| `Block.Time.between` | Array of [start, end] ISO timestamps | `["2025-01-01", "2025-02-01"]` |

---

## Sorting (`orderBy`)

```graphql
orderBy: { descending: Block_Time }   # Newest first
orderBy: { ascending: Block_Time }    # Oldest first
```

---

## Limit (`limit`)

```graphql
limit: { count: 1 }      # Latest single candle
limit: { count: 100 }    # Up to 100 candles
limit: { count: 1000 }   # Up to 1000 candles
```

---

## Output Fields

### `Token`

| Field | Type | Description |
|-------|------|-------------|
| `Address` | String | Token contract address (null for native) |
| `Id` | String | Bitquery token ID (e.g., `bid:bitcoin`) |
| `IsNative` | Boolean | True if native coin (BTC, ETH, etc.) |
| `Name` | String | Token full name |
| `Network` | String | Blockchain network (e.g., `ethereum`, `solana`) |
| `Symbol` | String | Ticker symbol (e.g., `BTC`) |
| `TokenId` | String | Internal Bitquery token ID |

### `Block`

| Field | Type | Description |
|-------|------|-------------|
| `Date` | String | Date in `YYYY-MM-DD` format |
| `Time` | String | ISO timestamp of the block |
| `Timestamp` | Integer | Unix timestamp |

### `Interval`

| Field | Type | Description |
|-------|------|-------------|
| `Time.Start` | String | Interval start ISO timestamp |
| `Time.End` | String | Interval end ISO timestamp |
| `Time.Duration` | Integer | Interval duration: 1 = 1 second (tick); other values in minutes |

### `Volume`

| Field | Type | Description |
|-------|------|-------------|
| `Base` | Float | Volume in the base token |
| `Quote` | Float | Volume in the quote token |
| `Usd` | Float | Volume in USD |

### `Price`

| Field | Type | Description |
|-------|------|-------------|
| `IsQuotedInUsd` | Boolean | Whether price is quoted in USD |
| `Ohlc.Open` | Float | Opening price |
| `Ohlc.High` | Float | Highest price in the interval |
| `Ohlc.Low` | Float | Lowest price in the interval |
| `Ohlc.Close` | Float | Closing price |
| `Average.Mean` | Float | Simple arithmetic mean price |
| `Average.SimpleMoving` | Float | Simple moving average |
| `Average.ExponentialMoving` | Float | Exponential moving average |
| `Average.WeightedSimpleMoving` | Float | Weighted simple moving average |

---

## Example: Multiple Candles for Ethereum

```graphql
{
  Trading {
    Tokens(
      where: {
        Currency: { Id: { is: "bid:ethereum" } }
        Interval: { Time: { Duration: { eq: 60 } } }
        Block: { Time: { after: "2025-01-01T00:00:00Z" } }
      }
      limit: { count: 24 }
      orderBy: { descending: Block_Time }
    ) {
      Block { Time }
      Volume { Usd }
      Price {
        Ohlc { Open High Low Close }
      }
    }
  }
}
```

## Example: Token by Contract Address

```graphql
{
  Trading {
    Tokens(
      where: {
        Currency: { SmartContract: { is: "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2" } }
        Interval: { Time: { Duration: { eq: 1440 } } }
      }
      limit: { count: 1 }
      orderBy: { descending: Block_Time }
    ) {
      Token { Name Symbol }
      Price { Ohlc { Close } }
      Volume { Usd }
    }
  }
}
```
