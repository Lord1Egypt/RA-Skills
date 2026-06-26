# WebSocket Streams Reference

Real-time data streaming via WebSocket. All channels push incremental updates.

## Connection

**URL**: `wss://realtime-dex.chainstream.io/connection/websocket?token=YOUR_ACCESS_TOKEN`

**Limits**:
- Max 100 subscriptions per connection
- Max 100KB per message
- Connection timeout: 60s without messages
- Heartbeat: send ping every 30s

**Heartbeat**:

```json
// Send
{"method": "ping"}

// Receive
{"channel": "pong"}
```

**Billing**: 0.005 Unit per byte of data pushed. Connection and heartbeat are free.

## SDK Connection

```typescript
import { ChainStreamClient } from '@chainstream-io/sdk';

const client = new ChainStreamClient('YOUR_TOKEN', {
  autoConnectWebSocket: true,
  streamUrl: 'wss://realtime-dex.chainstream.io/connection/websocket',
});

await client.stream.connect();

// Batch subscribe for efficiency
client.stream.batchSubscribe((batch) => {
  batch.subscribeTokenCandles({ chain: 'sol', token: 'ADDR', resolution: '1m' }, handler);
  batch.subscribeTokenStats({ chain: 'sol', token: 'ADDR' }, handler);
});
```

## Channels

### Token Candles

Channel: `dex-candle:{chain}_{token}_{resolution}`

Resolution: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`

```typescript
client.stream.subscribeTokenCandles(
  { chain: 'sol', token: 'TOKEN_ADDR', resolution: '1m' },
  (candle) => {
    // { o: open, c: close, h: high, l: low, v: volume, r: resolution, t: timestamp }
  }
);
```

### Pool Candles

Channel: `dex-pool-candle:{chain}_{pool}_{resolution}`

```typescript
client.stream.subscribePoolCandles(
  { chain: 'sol', poolAddress: 'POOL_ADDR', resolution: '5m' },
  handler
);
```

### Pair Candles

Channel: `dex-pair-candle:{chain}_{pair}_{resolution}`

```typescript
client.stream.subscribePairCandles(
  { chain: 'sol', pair: 'PAIR', resolution: '1h' },
  handler
);
```

### Token Stats

Channel: `dex-token-stats:{chain}_{token}`

Includes buy/sell counts, volumes, price changes across time windows.

```typescript
client.stream.subscribeTokenStats(
  { chain: 'sol', token: 'TOKEN_ADDR' },
  (stats) => {
    // { a: address, t: timestamp, b1m: buys_1m, s1m: sells_1m, bviu1m: buy_vol_usd_1m, ... }
  }
);
```

### Token Holders

Channel: `dex-token-holding:{chain}_{token}`

```typescript
client.stream.subscribeTokenHolders(
  { chain: 'sol', token: 'TOKEN_ADDR' },
  (holding) => {
    // { a: address, h: holders, t100a: top100_added, t10a: top10_added, ... }
  }
);
```

### New Token (single)

Channel: `dex-new-token:{chain}`

```typescript
client.stream.subscribeNewToken(
  { chain: 'sol' },
  (token) => {
    // { a: address, n: name, s: symbol, dec: decimals, cts: created_ts, lf: launchpad_flag }
  }
);
```

### New Tokens (batch metadata)

Channel: `dex-new-tokens-metadata:{chain}`

```typescript
client.stream.subscribeNewTokensMetadata(
  { chain: 'sol' },
  (tokens) => {
    // [{ a: address, n: name, s: symbol, iu: image_url, de: description, sm: social_media, cts: created_ts }]
  }
);
```

### Token Supply

Channel: `dex-token-supply:{chain}_{token}`

```typescript
client.stream.subscribeTokenSupply(
  { chain: 'sol', token: 'TOKEN_ADDR' },
  (supply) => {
    // { a: address, s: supply, mc: market_cap, ts: timestamp }
  }
);
```

### Token Liquidity

Channel: `dex-token-liquidity:{chain}_{token}`

```typescript
client.stream.subscribeTokenMaxLiquidity(
  { chain: 'sol', token: 'TOKEN_ADDR' },
  (liq) => {
    // { a: address, p: pool, liu: liquidity_usd, lin: liquidity_native, ts }
  }
);
```

### Token Total Liquidity

Channel: `dex-token-total-liquidity:{chain}_{token}`

```typescript
client.stream.subscribeTokenTotalLiquidity(
  { chain: 'sol', token: 'TOKEN_ADDR' },
  (liq) => {
    // { a: address, liu: total_liquidity_usd, lin: total_liquidity_native, pc: pool_count, ts }
  }
);
```

### Token Trades

Channel: `dex-trade:{chain}_{token}`

```typescript
client.stream.subscribeTokenTrade(
  { chain: 'sol', token: 'TOKEN_ADDR' },
  (trade) => {
    // { a: token, t: timestamp, k: kind, ba: buy_amount, baiu: buy_amount_usd, bwa: buyer_wallet, ... }
  }
);
```

### Wallet Balance

Channel: `dex-wallet-balance:{chain}_{wallet}`

```typescript
client.stream.subscribeWalletBalance(
  { chain: 'sol', wallet: 'WALLET_ADDR' },
  (balance) => {
    // { a: wallet, ta: token_address, tpiu: token_price_usd, b: balance, t: timestamp }
  }
);
```

### Wallet PnL

Channel: `dex-wallet-token-pnl:{chain}_{wallet}`

```typescript
client.stream.subscribeWalletPnl(
  { chain: 'sol', wallet: 'WALLET_ADDR' },
  (pnl) => {
    // { a: wallet, ta: token_address, tpiu: token_price_usd, ba: buy_amount, sa: sell_amount, piu: pnl_usd, ... }
  }
);
```

### Wallet Trades

Channel: `dex-wallet-trade:{chain}_{wallet}`

```typescript
client.stream.subscribeWalletTrade(
  { chain: 'sol', wallet: 'WALLET_ADDR' },
  handler
);
```

### Ranking Lists

Channel: `dex-ranking-list:{chain}_{type}` or `dex-ranking-list:{chain}_{type}_{dex}`

Types: `new`, `trending`, `us_stocks`, `completed`, `graduated`

```typescript
client.stream.subscribeRankingTokensList(
  { chain: 'sol', rankingType: 'trending' },
  (list) => {
    // [{ t: token, bc: bonding_curve, h: holders, s: symbol, ts: timestamp }]
  }
);
```

### Ranking Token Stats

Channel: `dex-ranking-token-stats-list:{chain}_{type}`

```typescript
client.stream.subscribeRankingTokensStats(
  { chain: 'sol', rankingType: 'new' },
  handler
);
```

### Ranking Holders

Channel: `dex-ranking-token-holding-list:{chain}_{type}`

```typescript
client.stream.subscribeRankingTokensHolders(
  { chain: 'sol', rankingType: 'trending' },
  handler
);
```

### Ranking Supply

Channel: `dex-ranking-token-supply-list:{chain}_{type}`

```typescript
client.stream.subscribeRankingTokensSupply(
  { chain: 'sol', rankingType: 'new' },
  handler
);
```

### Ranking Bonding Curve

Channel: `dex-ranking-token-bounding-curve-list:{chain}_new`

```typescript
client.stream.subscribeRankingTokensBondingCurve(
  { chain: 'sol' },
  (list) => {
    // [{ a: address, pr: progress_percent }]
  }
);
```

### DEX Pool Balance

Channel: `dex-pool-balance:{chain}_{pool}`

```typescript
client.stream.subscribeDexPoolBalance(
  { chain: 'sol', poolAddress: 'POOL_ADDR' },
  (balance) => {
    // { a: pool, taa: token_a_amount, taliu: token_a_liquidity_usd, tba: token_b_amount, tbliu: token_b_liquidity_usd }
  }
);
```
