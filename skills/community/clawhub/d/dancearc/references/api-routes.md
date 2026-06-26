# DanceArc API routes (quick map)

Base URL in dev: same origin as Vite with `/api` proxied to Express (default **8787**).

## Payment / monetization

| Method | Path | Interaction | Notes |
|--------|------|-------------|-------|
| POST | `/api/dance-extras/live/judge-score/testnet` | **h2a** | 402 + `X-Payment-Tx`; body: `battleId`, `roundId`, `judgeId`, `dancerId`, `score` |
| POST | `/api/judges/score` | **h2a** | Same payment gate; resource URL in challenge |
| POST | `/api/battle/intent` | **h2h** | Returns `requires_payment` + `recipient`, `amountDisplay` |
| POST | `/api/battle/verify` | **h2h** | `{ intentId, paymentTx }` |
| POST | `/api/coaching/start` | — | Open session |
| POST | `/api/coaching/tick` | — | Add seconds |
| POST | `/api/coaching/end` | **h2h** | Bill → `requires_payment` |
| POST | `/api/coaching/verify` | **h2h** | `{ sessionId, paymentTx }` |
| POST | `/api/beats/intent` | **h2h** | License intent |
| POST | `/api/beats/grant` | **h2h** | `{ licenseId, paymentTx }` |

## Config / ops

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/health` | `chainId`, `recipient`, `perActionUsdc` |
| GET | `/api/nanopayments/events` | In-memory events after successful Arc verify |

## Circle / wallets

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/dev-wallets/status` | DCW configured? |
| POST | `/api/dev-wallets/create` | Create Arc testnet wallet |
| POST | `/api/dev-wallets/faucet` | Programmatic faucet (may 403 by Circle policy) |
| POST | `/api/circle-modular` | JSON-RPC proxy to Modular SDK |

## Docs

| GET | `/openapi.json` | Stub OpenAPI 3.1 |
