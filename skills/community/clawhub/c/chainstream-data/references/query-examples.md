# Query Examples

Real-world query patterns for ChainStream Data API using MCP tools, REST API, and SDK.

## Token Search

**"Find the PUMP token on Solana"**

```bash
# MCP
{"tool": "tokens/search", "arguments": {"query": "PUMP", "chain": "sol"}}

# REST
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/token/search?keyword=PUMP&chain=sol"
```

```typescript
const results = await client.token.search({ keyword: 'PUMP', chain: 'sol' });
console.log(results.data.map(t => `${t.name} (${t.symbol}): ${t.address}`));
```

```python
results = token_api.search(keyword="PUMP", chain="sol")
for t in results.data:
    print(f"{t.name} ({t.symbol}): {t.address}")
```

## Token Detail and Analysis

**"Analyze whether BONK is worth buying"**

```bash
# MCP — comprehensive analysis in one call
{"tool": "tokens/analyze", "arguments": {"chain": "sol", "address": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263", "sections": ["overview","metrics","holders","security"]}}

# REST — combine multiple endpoints
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/token/sol/DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263"
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/token/sol/DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263/security"
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/token/sol/DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263/topHolders"
```

```typescript
const [token, security, holders] = await Promise.all([
  client.token.getToken({ chain: 'sol', tokenAddress: 'DezXAZ...' }),
  client.token.getSecurity({ chain: 'sol', tokenAddress: 'DezXAZ...' }),
  client.token.getTopHolders({ chain: 'sol', tokenAddress: 'DezXAZ...' }),
]);
```

## Token Price History

**"Show me the 1-hour candles for SOL over the last 24 hours"**

```bash
{"tool": "tokens/price_history", "arguments": {"chain": "sol", "address": "So11111111111111111111111111111111111111112", "resolution": "1h", "limit": 24}}
```

```typescript
const candles = await client.token.getCandles({
  chain: 'sol',
  tokenAddress: 'So11111111111111111111111111111111111111112',
  resolution: '1h',
  limit: 24,
});
candles.data.forEach(c => console.log(`${c.time}: O=${c.open} H=${c.high} L=${c.low} C=${c.close} V=${c.volume}`));
```

## Token Discovery

**"Find high-volume tokens on BSC in the last 24 hours"**

```bash
{"tool": "tokens/discover", "arguments": {"chain": "bsc", "sort_by": "volume", "time_frame": "24h", "min_volume_usd": 100000, "limit": 10}}
```

```typescript
const hot = await client.ranking.getHotTokens({ chain: 'bsc', duration: '24h' });
```

## Token Comparison

**"Compare BONK, WIF, and POPCAT"**

```bash
{"tool": "tokens/compare", "arguments": {"tokens": [{"chain": "sol", "address": "DezXAZ..."}, {"chain": "sol", "address": "EKpQGS..."}, {"chain": "sol", "address": "7GCihg..."}]}}
```

## Wallet PnL

**"What's the PnL for this Solana wallet?"**

```bash
{"tool": "wallets/profile", "arguments": {"chain": "sol", "address": "5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1", "include": ["holdings","pnl","net_worth"]}}

# REST
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/wallet/sol/5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1/pnl"
```

```typescript
const pnl = await client.wallet.getPnl({ chain: 'sol', walletAddress: '5Q544f...' });
console.log(`Total PnL: $${pnl.totalPnlUsd}, Win Rate: ${pnl.winRate}%`);
```

```go
pnl, _ := client.Wallet.GetPnl(ctx, "sol", "5Q544f...")
fmt.Printf("Total PnL: $%s\n", pnl.TotalPnlUsd)
```

## Wallet Net Worth

**"Show portfolio breakdown for wallet 0xABC on BSC"**

```bash
# REST
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/wallet/bsc/0xABC.../net-worth-details"
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/wallet/bsc/0xABC.../tokens-balance"
```

```typescript
const [netWorth, balance] = await Promise.all([
  client.wallet.getNetWorthDetails({ chain: 'bsc', walletAddress: '0xABC...' }),
  client.wallet.getTokensBalance({ chain: 'bsc', walletAddress: '0xABC...' }),
]);
```

## Wallet Activity

**"Recent transfers for this wallet"**

```bash
{"tool": "wallets/activity", "arguments": {"chain": "sol", "address": "5Q544f...", "limit": 20}}
```

```typescript
const transfers = await client.wallet.getTransfers({
  chain: 'sol', walletAddress: '5Q544f...', limit: 20
});
```

## Market Trends

**"What are the hottest tokens right now?"**

```bash
{"tool": "market/trending", "arguments": {"chain": "sol", "category": "hot", "limit": 10}}
```

```typescript
const trending = await client.ranking.getHotTokens({ chain: 'sol', duration: '24h' });
```

**"Show me newly launched tokens on Solana"**

```bash
{"tool": "market/trending", "arguments": {"chain": "sol", "category": "new", "limit": 20}}
```

```typescript
const newTokens = await client.ranking.getNewTokens({ chain: 'sol' });
```

**"Which tokens are about to graduate from bonding curve?"**

```bash
{"tool": "market/trending", "arguments": {"chain": "sol", "category": "graduating"}}
```

## Recent Trades

**"Show latest trades for this token"**

```bash
{"tool": "trades/recent", "arguments": {"chain": "sol", "tokenAddress": "DezXAZ...", "limit": 20}}
```

```typescript
const trades = await client.trade.getTrades({ chain: 'sol', tokenAddress: 'DezXAZ...' });
```

## Top Traders (Smart Money)

**"Who are the most profitable traders on Solana?"**

```bash
# REST
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/trade/sol/top-traders"
```

```typescript
const topTraders = await client.trade.getTopTraders({ chain: 'sol' });
```

**"Which traders tagged as smart_money are trading this token?"**

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/token/sol/DezXAZ.../traders/smart_money"
```

## Webhook Setup

**"Notify me when whale wallets trade BONK"**

```bash
{"tool": "webhooks/manage", "arguments": {"action": "create", "url": "https://my-server.com/webhook", "events": ["trade.whale"]}}

# REST
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://my-server.com/webhook","filterTypes":["trade.whale"]}' \
  "https://api.chainstream.io/v2/webhook/endpoint"
```

## Batch Token Queries

**"Get market data for 5 tokens at once"**

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/token/sol/marketData/multi?addresses=ADDR1,ADDR2,ADDR3,ADDR4,ADDR5"
```

```typescript
const marketData = await client.token.getMarketDataMulti({
  chain: 'sol',
  addresses: ['ADDR1', 'ADDR2', 'ADDR3', 'ADDR4', 'ADDR5'],
});
```

## Token Security Check

**"Is this token safe to trade?"**

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/token/sol/TOKEN_ADDRESS/security"
```

```typescript
const security = await client.token.getSecurity({ chain: 'sol', tokenAddress: 'TOKEN_ADDRESS' });
// Check: isHoneypot, hasMintAuthority, hasFreezeAuthority, top10HolderPercent
```

## Developer Token History

**"What other tokens has this developer created?"**

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.chainstream.io/v2/token/sol/dev/DEV_ADDRESS/tokens"
```
