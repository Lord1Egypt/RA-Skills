---
name: fomo-app-data-api
title: Fomo App Public Data
description: Read-only Fomo App API for public market-research data through ReplyNodes prepaid credits with one long-lived Bearer fetcher key; per-operation credit cost follows the authoritative catalog.
version: 2.0.1
mode: readonly
auth: Authorization: Bearer YOUR_FETCHER_KEY
---

# Fomo App Public Data

Read-only Fomo App API for public market-research data through ReplyNodes prepaid credits with one long-lived Bearer fetcher key; per-operation credit cost follows the authoritative catalog.

## Setup

1. Create a free ReplyNodes account at https://app.replynodes.com/auth.
2. The Free plan includes 500 one-time credits and does not require payment setup.
3. Open https://app.replynodes.com/developers and create the single long-lived ReplyNodes fetcher API key.
4. Store the secret as REPLYNODES_API_KEY in the agent secret store. Never paste it into chat, commit it, or put it in a URL.
5. Send it on API calls as Authorization: Bearer YOUR_FETCHER_KEY.

Gateway: https://api.replynodes.com

## Authentication

Use one long-lived ReplyNodes fetcher key. Send it on every request as:

```http
Authorization: Bearer YOUR_FETCHER_KEY
```

Store the real key in the agent's secret configuration. Never put it in prompts, source files, logs, URLs, or returned data. The gateway performs shared control-plane scope and entitlement checks.

## Plans and prepaid credits

- Payment mode: `prepaid_credit` only.
- Free: 500 one-time credits.
- Developer: 10,000 credits/month at $19/month.
- Pro: 100,000 credits/month at $99/month.
- Failed or provider-error requests cost zero; monthly credits do not roll over; paid overage requires an explicit cap.

- Fomo operation pricing is intentionally deferred to the authoritative catalog; this package does not quote a numeric Fomo price.

## Read-only operations

Every operation is an HTTP GET and reads public data only:

- `leaderboard` — `GET https://api.replynodes.com/v1/fomo/leaderboard/{window}`. Read public Fomo leaderboard data Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `tokens_trending` — `GET https://api.replynodes.com/v1/fomo/tokens/trending`. Read public trending-token data Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `tokens_most_held` — `GET https://api.replynodes.com/v1/fomo/tokens/most-held`. Read public most-held-token data Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `tokens_graduated` — `GET https://api.replynodes.com/v1/fomo/tokens/graduated`. Read public graduated-token data Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `token_holders` — `GET https://api.replynodes.com/v1/fomo/tokens/{address}/holders`. Read public token-holder data Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `user_profile` — `GET https://api.replynodes.com/v1/fomo/users/{handle}`. Read a public Fomo user profile Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `user_trades` — `GET https://api.replynodes.com/v1/fomo/users/{handle}/trades`. Read public user trade history Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `user_balances` — `GET https://api.replynodes.com/v1/fomo/users/{handle}/balances`. Read public user balance data Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `trade` — `GET https://api.replynodes.com/v1/fomo/trades/{trade_id}`. Read one public trade Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `thesis` — `GET https://api.replynodes.com/v1/fomo/thesis`. Read public Fomo theses Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `thesis_by_token` — `GET https://api.replynodes.com/v1/fomo/thesis/token/{mint}`. Read public theses for a token Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `thesis_by_user` — `GET https://api.replynodes.com/v1/fomo/thesis/user/{id}`. Read public theses by a user Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `thesis_by_user_token` — `GET https://api.replynodes.com/v1/fomo/thesis/user/{id}/token/{address}`. Read public user-token theses Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `search` — `GET https://api.replynodes.com/v1/fomo/search`. Search public Fomo data Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `alerts` — `GET https://api.replynodes.com/v1/fomo/alerts`. Read public Fomo alerts Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.
- `notifications` — `GET https://api.replynodes.com/v1/fomo/notifications`. Read public Fomo notifications Cost is determined by the authoritative Fomo catalog; do not infer or quote a number.

## Request and response behavior

- Use `https://api.replynodes.com` as the gateway origin.
- Encode path parameters and query values; do not put credentials in query strings.
- Preserve the gateway response envelope and request ID when reporting results.
- Treat unavailable upstream data as unavailable; do not fabricate fields or success.
- Do not retry non-idempotent methods: this package has no non-GET methods.

## Example

```bash
curl -sS https://api.replynodes.com/v1/fomo/capabilities
curl -sS -H "Authorization: Bearer YOUR_FETCHER_KEY" \
  "https://api.replynodes.com/v1/fomo/leaderboard/{window}"
```

## Safety boundaries

This skill has no write, publish, account, follow, or credential-management operation. It must not be used to claim private data access, unauthenticated access, guaranteed availability, or unsupported pricing.

## Source and validation

The operation list is generated from `services/replynodes-fetcher/internal/billing/catalog.go and the live Fomo capability catalog`. `manifest.json`, `references/operations.json`, and `CHECKSUMS.sha256` are generated artifacts; change the catalog or source capability contract and regenerate them together.
