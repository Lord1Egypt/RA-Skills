# ASG Card — Technical Overview

## Platform

ASG Card is an agent-focused virtual card platform built on the Stellar network. It uses the [x402 payment protocol](https://www.x402.org/) to enable AI agents to autonomously create and fund virtual cards using USDC.

## Stack

| Layer | Technology |
|---|---|
| **Network** | Stellar mainnet (pubnet) |
| **Asset** | USDC (Centre/Stellar) |
| **Payment Protocol** | x402 v2 (`X-PAYMENT` header, `PaymentPayload`) |
| **Facilitator** | OpenZeppelin Channels (hosted verify + settle) |
| **API** | Express.js on Vercel Serverless |
| **Auth** | Ed25519 wallet signature |
| **Database** | PostgreSQL (Supabase) |
| **SDK** | `@asgcard/sdk` (TypeScript) |

## Security

- HMAC webhook signature verification
- Anti-replay with idempotency keys + DB deduplication
- Kill-switch (`ROLLOUT_ENABLED`) for instant rollback
- Rate limiting on sensitive endpoints
- Gitleaks CI on every push

## API

- **Base URL:** `https://api.asgcard.dev`
- **OpenAPI:** [asgcard.dev/openapi.json](https://asgcard.dev/openapi.json)
- **Docs:** [asgcard.dev/docs](https://asgcard.dev/docs)

See [SECURITY.md](./SECURITY.md) for vulnerability reporting.
