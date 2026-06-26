---
name: aurex
description: Issue virtual crypto-funded cards and manage payments with the Aurex API. Use when users want to create virtual Visa/Mastercard cards, handle crypto deposits in SOL/USDT/USDC, manage user accounts, top up cards, or retrieve transaction history. Get your API key at aurex.cash → Dashboard → API Keys.
primaryEnv: AUREX_API_KEY
credentials:
  - name: AUREX_API_KEY
    description: Your Aurex API key from aurex.cash dashboard. Never log or expose this value.
    required: true
---

# Aurex

Issue virtual crypto-funded cards and manage payments programmatically using the Aurex API.

## Setup

Get your API key at [aurex.cash](https://aurex.cash) → Dashboard → API Keys.

```bash
export AUREX_API_KEY="your-api-key"
```

**Base URL:** `https://aurex.cash/api/dashboard`
**Auth:** `Authorization: Bearer $AUREX_API_KEY`
**Rate limit:** 60 requests/minute

## Security

- Store `AUREX_API_KEY` in environment variables only — never hardcode or log it
- Card details (number, CVV, expiry, OTP) are sensitive — never log or store them in plaintext
- Only request card details when strictly necessary for the user's task
- Treat CVV and OTP as single-use secrets — discard after use

## Users

### Create a user
```http
POST /users
Authorization: Bearer $AUREX_API_KEY
Content-Type: application/json

{ "name": "John Doe", "email": "john@example.com" }
```

### Get a user
```http
GET /users/:userId
Authorization: Bearer $AUREX_API_KEY
```

### Get wallet address for deposits
```http
GET /users/:userId/wallet
Authorization: Bearer $AUREX_API_KEY
```
Returns a deposit address. Send SOL, USDT, or USDC to fund the wallet.

## Cards

### Issue a card
```http
POST /cards
Authorization: Bearer $AUREX_API_KEY
Content-Type: application/json

{ "userId": "user_123", "name": "Shopping Card", "amount": 50 }
```

### Get card details
```http
GET /cards/:cardId
Authorization: Bearer $AUREX_API_KEY
```
Returns card number, CVV, expiry, OTP. Handle with care — never log these values.

### Top up a card
```http
POST /cards/:cardId/topup
Authorization: Bearer $AUREX_API_KEY
Content-Type: application/json

{ "amount": 25 }
```

### List cards
```http
GET /cards?userId=user_123
Authorization: Bearer $AUREX_API_KEY
```

### Get transactions
```http
GET /cards/:cardId/transactions
Authorization: Bearer $AUREX_API_KEY
```

## Commission

### Set partner markup
```http
POST /partner/markup
Authorization: Bearer $AUREX_API_KEY
Content-Type: application/json

{ "markup": 5 }
```

### Get commission earnings
```http
GET /partner/commission
Authorization: Bearer $AUREX_API_KEY
```

## Common Workflows

### Issue a card end-to-end
1. Create user: `POST /users`
2. Get deposit address: `GET /users/:id/wallet`
3. User sends crypto to that address
4. Issue card: `POST /cards`
5. Return card details to user securely

### Top up an existing card
1. Check wallet balance: `GET /users/:id/wallet`
2. Top up: `POST /cards/:id/topup`
3. Confirm balance: `GET /cards/:id`

## Error Codes

| Status | Meaning |
|--------|---------|
| 401 | Invalid or missing API key |
| 404 | User or card not found |
| 422 | Insufficient wallet balance |
| 429 | Rate limit exceeded |

## TypeScript SDK

```bash
npm install @aurexcash/agent
```

```typescript
import { createAurexTools } from '@aurexcash/agent'

const tools = createAurexTools({ apiKey: process.env.AUREX_API_KEY })
// Works with Claude, OpenAI, Vercel AI SDK
```

## Resources

- Website: [aurex.cash](https://aurex.cash)
- Docs: [docs.aurex.cash](https://docs.aurex.cash)
- Support: [support@aurex.cash](mailto:support@aurex.cash)
