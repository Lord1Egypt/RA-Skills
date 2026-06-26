# API Schema Reference

## Supported Chains

| Chain | Identifier | Data API | DeFi API | WebSocket |
|-------|-----------|----------|----------|-----------|
| Solana | `sol` | Yes | Yes | Yes |
| BSC | `bsc` | Yes | Yes | Yes |
| Ethereum | `eth` | Yes | Yes | Yes |
| Polygon | `polygon` | — | Bridge only | — |
| Arbitrum | `arbitrum` | — | Bridge only | — |
| Avalanche | `avalanche` | — | Bridge only | — |
| Optimism | `optimism` | — | Bridge only | — |
| zkSync | `zksync` | — | Bridge only | — |

## Base URLs

| Service | URL |
|---------|-----|
| Data API | `https://api.chainstream.io` |
| MCP Server (streamable-http) | `https://mcp.chainstream.io/mcp` |
| MCP Server (SSE) | `https://mcp.chainstream.io/sse` |
| WebSocket | `wss://realtime-dex.chainstream.io/connection/websocket` |
| OAuth Token | `https://dex.asia.auth.chainstream.io/oauth/token` |
| x402 Pricing | `https://mcp.chainstream.io/x402/pricing` |
| x402 Facilitator | `https://x402.org/facilitator` |

## Authentication

| Method | Header/Param | Description |
|--------|-------------|-------------|
| Bearer Token | `Authorization: Bearer <token>` | API Key or OAuth JWT |
| API Key | `X-API-KEY: <key>` | Alternative API key header |
| x402 Payment | `X-Payment: <base64>` | x402 payment proof |
| Wallet Signature | `X-Wallet-Address`, `X-Wallet-Chain`, `X-Wallet-Signature`, `X-Wallet-Timestamp`, `X-Wallet-Nonce` | Wallet-based auth |
| WebSocket | `?token=<access_token>` | URL query parameter |

## Response Formats

Control output verbosity with the `response_format` parameter:

| Format | Token Count | Records | Use Case |
|--------|------------|---------|----------|
| `concise` | ~500 | 5-10 | Default for AI agents |
| `detailed` | ~2000-5000 | Full | Top holders, recent trades, K-lines |
| `minimal` | ~100 | IDs only | Batch processing, pipelines |

## K-line Resolutions

| Value | Period |
|-------|--------|
| `1m` | 1 minute |
| `5m` | 5 minutes |
| `15m` | 15 minutes |
| `1h` | 1 hour |
| `4h` | 4 hours |
| `1d` | 1 day |

## Ranking Duration Values

Used with `/v2/ranking/{chain}/hotTokens/{duration}`:

| Value | Period |
|-------|--------|
| `1h` | Last 1 hour |
| `6h` | Last 6 hours |
| `24h` | Last 24 hours |

## Trader Tags

Used with `/v2/token/{chain}/{tokenAddress}/traders/{tag}`:

| Tag | Description |
|-----|-------------|
| `smart_money` | Historically profitable wallets |
| `whale` | Large-balance wallets |
| `sniper` | Early buyers of new tokens |
| `insider` | Developer or related wallets |

## Error Codes

| HTTP Code | Meaning |
|-----------|---------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (missing or invalid token) |
| 402 | Payment required (x402 — send payment to proceed) |
| 403 | Forbidden (insufficient scopes) |
| 404 | Resource not found |
| 429 | Rate limited (exceeded plan limit) |
| 500 | Internal server error |

## Rate Limits

| Plan | REST (req/s) | WebSocket Subscriptions |
|------|-------------|------------------------|
| Free | 10 | 10 |
| Starter | 50 | 50 |
| Pro | 200 | 100 |
| Enterprise | 1000 | 100 |

## Billing

### Unit-Based (API Key Plans)

Different endpoints consume different Units:

| Endpoint Type | Units |
|--------------|-------|
| Token price/search | 1 |
| Token detail/stats | 1 |
| Wallet PnL | 2 |
| Quote | 2 |
| Execute swap | 5 |

### WebSocket Billing

- Per byte of data pushed: 0.005 Unit/byte
- Connection and heartbeat: free

### x402 Per-Tool Pricing (USDC)

| Tool | Price |
|------|-------|
| tokens/search | $0.001 |
| tokens/analyze | $0.003 |
| tokens/price_history | $0.002 |
| tokens/discover | $0.002 |
| tokens/compare | $0.005 |
| wallets/profile | $0.005 |
| wallets/activity | $0.002 |
| market/trending | $0.001 |
| dex/quote | $0.001 |
| dex/swap | $0.005 |
| trading/backtest | $0.05 |
| Default (unlisted) | $0.001 |

## OAuth Scopes

| Scope | Description |
|-------|-------------|
| `webhook.read` | Read webhook endpoints |
| `webhook.write` | Create/update/delete webhooks |
