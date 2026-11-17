---
name: freeland-x402-esim
description: Discover, compare, buy, and retrieve Freeland prepaid travel eSIMs through x402 with native USDC on Base. Use when an agent needs travel connectivity, an eSIM plan or quote, an x402 eSIM purchase, a live catalog lookup, purchase readiness, order recovery, or private owner delivery of eSIM installation credentials.
---

# Freeland x402 eSIM

Use the live service contract at `https://api.x402card.org/api/esim/discovery`. Use the remote MCP at `https://api.x402card.org/mcp` only for read-only discovery; never give it wallet authority.

## Discover and select

1. Read `https://api.x402card.org/api/esim/ready`. Stop if it is not green.
2. List plans with the MCP tool `x402card.list_esim_plans` or `GET /api/esim/plans`. Filter by destination, allowance, duration, and the user's price cap.
3. Treat the live plan and its returned price as authoritative. Do not use cached plan ids, counts, or prices.
4. State the selected plan, destination coverage, allowance, duration, and exact USDC amount before payment.

## Buy directly

1. Generate one stable idempotency key for the purchase attempt.
2. Send `POST https://api.x402card.org/api/esim/purchase` with `{ "planId": "<live-plan-id>", "idempotencyKey": "<stable-key>" }` and no payment header.
3. Require HTTP `402` and decode `PAYMENT-REQUIRED`. Verify all of the following:
   - x402 version `2` and scheme `exact`;
   - network `eip155:8453`;
   - native Base USDC asset `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`;
   - resource `https://api.x402card.org/api/esim/purchase`;
   - amount equals the selected live plan price;
   - service name is `Freeland eSIM`.
4. Sign the exact challenge with the user-owned payer wallet. Never request or expose a seed phrase or private key.
5. Repeat the same POST once with the same body and `PAYMENT-SIGNATURE`. The payer becomes the eSIM owner.
6. Preserve the returned `orderId` and `delivery.token` in private local state. Never print, log, publish, or send the token to another user.
7. If the paid response is lost, repeat the same purchase body with the same idempotency key. The service facilitator-verifies the fresh payer authorization and replays the settled order without settling a second transfer. Require `replayed: true`; never change the key to recover.

## Continue and retrieve

1. Poll `GET /api/esim/orders/:orderId` with `X-Esim-Delivery-Token: <delivery.token>` from the paid response. This is the primary path for payment-only x402 wallets.
2. Wallet authentication through `POST /api/auth/challenge` and `POST /api/auth/verify` remains an optional fallback for signers that support EIP-191 or EIP-712.
3. Continue polling while fulfillment is pending. Never create a replacement order to recover an unclear payment.
4. After status `fulfilled`, call `GET /api/esim/orders/:orderId/credentials` with the same delivery header.
5. Deliver QR, LPA activation data, ICCID, and installation links only to the capability holder or authenticated owner through a private, non-cacheable channel. Never place them in public artifacts, shared logs, analytics, or another user's context.

## Failure policy

- Reuse the original idempotency key, delivery token, and order id for reads and recovery.
- Treat timeouts as unknown state, not proof that payment failed.
- Do not replay payment, compensate, refund, reorder, or retry provider fulfillment without a new explicit owner decision.
- Stop on a changed plan price or payment requirement and show the new quote before requesting a new authorization.
- Keep supplier identity, wholesale cost, provider credentials, and installation secrets private.
