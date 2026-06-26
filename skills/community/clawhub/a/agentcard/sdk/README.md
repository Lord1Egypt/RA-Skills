# @asgcard/sdk

TypeScript SDK for [ASG Card](https://asgcard.dev) — instant virtual MasterCard cards for AI agents, paid via x402 on Stellar.

## Install

```bash
npm install @asgcard/sdk
```

## Quick Start

```typescript
import { ASGCardClient } from '@asgcard/sdk';

const client = new ASGCardClient({
  privateKey: 'S...', // Stellar secret key
});

// Create a $10 virtual card
const result = await client.createCard({
  amount: 10,
  nameOnCard: 'AI AGENT',
  email: 'agent@example.com',
});

console.log(result.card.cardId);          // card_xxxx
console.log(result.detailsEnvelope);      // { cardNumber, cvv, expiry, ... }
console.log(result.payment.txHash);       // Stellar tx hash
```

## How It Works

1. SDK calls `POST /cards/create/tier/10`
2. API returns `402` with x402 payment challenge
3. SDK builds a Soroban USDC transfer, signs it, and retries with `X-PAYMENT` header
4. API verifies + settles on Stellar mainnet → returns `201` with card details

## API

### `new ASGCardClient(config)`

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `privateKey` | `string` | — | Stellar secret key (`S...`) |
| `walletAdapter` | `WalletAdapter` | — | External wallet (browser extension) |
| `baseUrl` | `string` | `https://api.asgcard.dev` | API URL |
| `rpcUrl` | `string` | `https://mainnet.sorobanrpc.com` | Soroban RPC |
| `timeout` | `number` | `60000` | Request timeout (ms) |

### `client.createCard(params)`

```typescript
const card = await client.createCard({
  amount: 10,            // 10, 25, 50, 100, 200, or 500 USD
  nameOnCard: 'MY AGENT',
  email: 'agent@example.com',
});
```

### `client.fundCard(params)`

```typescript
const funded = await client.fundCard({
  amount: 25,
  cardId: 'card_xxxx',
});
```

### `client.getTiers()`

```typescript
const tiers = await client.getTiers();
// { creation: [...], funding: [...] }
```

### `client.health()`

```typescript
const health = await client.health();
// { status: 'ok', version: '0.3.1' }
```

## Low-Level Utilities

For custom integrations:

```typescript
import {
  parseChallenge,
  buildPaymentTransaction,
  buildPaymentPayload,
  handleX402Payment,
} from '@asgcard/sdk';
```

## Requirements

- Node.js 18+
- Stellar account with USDC balance
- USDC asset: `CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75` (Soroban SAC)

## Links

- [Documentation](https://asgcard.dev/docs)
- [OpenAPI Spec](https://asgcard.dev/openapi.json)
- [GitHub](https://github.com/ASGCompute/asgcard-public)
- [API Status](https://api.asgcard.dev/health)

## License

MIT
