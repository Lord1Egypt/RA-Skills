---
name: canopy-deposits
description: Create crypto deposit intents, retrieve funding options and addresses, and track settlement through Canopy's remote MCP server. Use when a user wants to accept or check a crypto deposit through Canopy. Free to integrate.
metadata:
  openclaw:
    homepage: https://www.canopypay.io/agents/mcp
---

# Canopy deposits

Use Canopy's MCP tools to prepare a crypto deposit for a merchant account and report its funding or settlement state. The human funds the deposit from their wallet or through Canopy checkout. MCP tools do not sign or submit blockchain transactions.

## Connection

Use an MCP client connected to **https://www.canopypay.io/api/mcp** with Streamable HTTP. Keep the `www.` hostname: the apex redirects across hosts, which can drop the authorization header. The endpoint accepts POST and JSON responses; it does not support legacy SSE. GET/DELETE returning 405 is expected.

Authenticate using the client's OAuth flow or a server-side Canopy secret key supplied securely through the client's environment/credential configuration. OAuth uses authorization code with PKCE and supports dynamic registration. Every tool requires the `payment_intents:create` scope. A publishable key cannot authenticate MCP.

Do not request secrets in chat or embed them in committed configuration. If the connection is absent, explain the endpoint and scope and let the account owner connect it through their MCP client. Do not invent a credential or access another merchant account.

Documentation: https://www.canopypay.io/agents/mcp
Plain-text contract: https://www.canopypay.io/agents/mcp/raw

## Tools and decisions

Confirm the connected server exposes these five tools:

| Tool | Purpose | Inputs |
| --- | --- | --- |
| `create_deposit` | Create or reuse a payment intent | Optional `priceUnits`, `oneTime`, `merchantReference`, `metadata`, and destination fields |
| `list_deposit_options` | Read this intent's funding options, minimums and settlement rails | `intentId` |
| `get_deposit_address` | Issue or return an address and start detection for this option | `intentId`, exact returned `caip19` |
| `get_deposit_status` | Read deposit detection and transfer/settlement state | `intentId` |
| `list_deposits` | List the authenticated account's intents | Optional `limit`, `cursor` |

Read results from `structuredContent`; clients may expose equivalent JSON in the text content. Inputs are strict: unknown fields are rejected. Do not add fee or treasury inputs.

Creating an intent or issuing an address changes Canopy account state. Do it only when the user's request calls for preparing a deposit. For a status question, use read tools and an existing intent.

## Prepare a deposit

1. Establish the intended destination from the user/app. Set `payoutWallet`, `payoutNamespace` and `payoutChainReference` only when provided; omit them to use the merchant's account default. `payoutTokenAddress` is optional with a destination wallet. Never guess a recipient wallet.
2. For an open-amount deposit, omit `priceUnits`. For a fixed amount, determine the default settlement asset and its decimals from `settleRails` returned by `list_deposit_options` for an existing intent (`list_deposits` can locate one). Use the rail with `default: true`, not the first rail. Convert decimal input with integer arithmetic into a positive base-unit string. Do not assume decimals or silently convert currencies. If no existing rail is available, request the settlement configuration rather than guessing an amount.
3. Call `create_deposit` with the authorized inputs. `oneTime: true` requires `priceUnits`. Retain the returned `intentId` and `hostedPageUrl`.
4. Offer the hosted checkout link as the simplest human funding flow. If the user wants a direct address, call `list_deposit_options` for this intent, show chain/token/minimum, and let the user choose an available option. Use only options with `depositIssuable: true`.
5. Call `get_deposit_address` with the chosen option's exact `caip19`. Present the full returned address **together with the returned chain name, token symbol and minimum**. Tell the human to send that token on that network. Do not show a bare address or reuse one from another intent/option.
6. Read `get_deposit_status` when the user asks for progress. Report the actual detection and per-transfer stage; `depositDetected` alone is not settlement. Include returned fee/net information when relevant. `belowMinimum: true` means top-ups on the same network are needed to reach the minimum.

Supported assets are whatever the tools return for this intent, including native assets. Do not call Canopy stablecoin-only or list networks/tokens from memory. Delivery may bridge or convert, so the received asset can differ from the sent asset.

## Reuse and failures

An active intent is reused for the same account, destination chain, wallet and token with matching terms. A reused result has `created: false`; new `merchantReference` and `metadata` are not applied. Different amount/one-time terms cause `idempotency_key_reuse`.

Without destination fields, each create makes a new intent. After a timeout, check `list_deposits` before retrying creation. Repeating `get_deposit_address` for the same intent/option returns the same address.

Branch on the returned error code. Fix rejected inputs; do not retry `not_found` as another account. Authentication failures require correcting the hostname or credential/scope, not repeated calls. Respect HTTP 429/`Retry-After` and avoid automatic tight status polling.

## Pricing

Canopy is free to integrate. Do not infer that funding, conversion, blockchain fees or settlement are free; report the actual tool results and current Canopy pricing when those costs matter.
