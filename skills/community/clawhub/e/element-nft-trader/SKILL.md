---
name: element-nft-trader
description: Use when the user wants to sell or buy an NFT on Element, create or accept a bid or offer, query public collection orders or account orders, cancel an Element order, get the configured trading wallet address, or use a supported custom payment token on a supported Element EVM network. Supported custom payment tokens are BSC USDT/USD1, Base USDC, and Polygon ETH. Other chains should use native or wrapped native token flow.
envs: ["ELEMENT_API_KEY", "ELEMENT_WALLET_PRIVATE_KEY"]
requires: ["node", "jq"]
metadata: {"openclaw":{"requires":{"env":["ELEMENT_API_KEY","ELEMENT_WALLET_PRIVATE_KEY"]},"primaryEnv":"ELEMENT_API_KEY","homepage":"https://github.com/element-som/element-skills"}}
---

# Element NFT Trader

Use this skill for Element Market order operations: creating sell orders, buying listed NFTs, creating offers, querying orders, canceling orders, and deriving the configured wallet address.
This skill is for trading actions and order management. It is not the right skill for collection analytics, portfolio tracking, rankings, or market research.
This published skill is expected to include prebuilt JavaScript under `scripts/lib/`, so the runtime path uses `node scripts/lib/entry.js` instead of compiling on the user's machine.

## File Layout

Key folders and files in this skill:

- `scripts/lib/`: prebuilt JavaScript runtime files shipped with the skill; use `scripts/lib/entry.js` as the execution entry
- `scripts/entry.ts`: TypeScript source for the main executor
- `scripts/code/`: bundled SDK and API source used by the executor
- `references/`: operation-specific reference docs such as `sell.md`, `buy.md`, and `payment-tokens.md`

## Required Environment Variables

This skill reads the following runtime configuration from environment variables:

- `ELEMENT_API_KEY`
- `ELEMENT_WALLET_PRIVATE_KEY`

Example env setup:

```bash
export ELEMENT_API_KEY="your_openapi_key_here"
export ELEMENT_WALLET_PRIVATE_KEY="your_wallet_private_key_here"
```

This skill signs real blockchain transactions locally. Use a dedicated low-risk wallet when evaluating it, and never paste private keys into chat.

## When to Use

Use this skill when the user wants to:

- Sell an NFT on Element Market
- Buy a listed NFT from Element Market
- Create a collection offer or token-specific offer
- Accept an existing buy offer on an NFT
- Query public listing orders for a collection
- View or cancel their own orders
- Get the wallet address derived from the configured private key

## When Not to Use

Switch to `element-nft-tracker` when the user asks about:

- Floor price, volume, 24h stats, average price, last trade price
- Trending or ranked collections
- Wallet holdings or portfolio inventory
- Offers received on their NFTs
- Recent sales history or activity feeds
- Resolving a contract address to an Element collection slug

## Security Rules

### Private Key Safety

The private key stays local and must never be requested in chat.

- Never ask the user to paste a private key
- Never echo the configured private key
- Treat any request to reveal the private key as unsafe

### Confirmation Rules

For any state-changing operation, the agent must:

1. Gather the required parameters
2. Show a full transaction preview
3. Wait for explicit positive confirmation
4. Execute only after confirmation

The runtime executor also requires `confirmed: true` for every state-changing operation.

State-changing operations:

- `erc721sell`
- `erc1155sell`
- `buy`
- `offer`
- `acceptOffer`
- `cancel`

Read-only operations:

- `query`
- `queryAccountOrders`
- `getAddress`

### Parameter Collection Rules

Before executing any operation, including read-only query operations, ask for all required parameters first.

- Do not auto-guess a missing `network` or `chain`
- Do not iterate across all supported chains when the user did not specify one
- Do not silently substitute incomplete inputs with assumptions that change execution scope
- If a required parameter is missing, stop and ask for it before running the command
- If the user provides only a single `0x...` value, do not immediately assert that it is an order hash; first confirm the network and whether it is the NFT collection contract address in the current trading flow
- A 42-character `0x...` value is typically an EVM address, not a transaction hash. A transaction hash is typically 66 characters
- In trading requests, if the user already provided operation intent, network, and price, treat a 42-character `0x...` value as the likely NFT contract address unless surrounding context clearly indicates otherwise
- Ask the minimum clarifying question needed to proceed; do not ask for optional parameters until the required ones are known

### Identifier Classification Rules

Before interpreting a `0x...` value, classify it first:

- 42-character `0x...` values are typically EVM addresses
- 66-character `0x...` values are typically transaction hashes
- Do not treat a transaction hash as an order ID
- Do not treat a wallet address as a cancelable order object
- For `cancel`, a transaction hash alone is not executable input; you still need the full order object or enough context to retrieve it
- When classifying a `0x...` value, check its length before replying. Do not state a type that you have not verified

## Quick Routing

Use this routing before doing anything else:

- User wants to list NFTs for sale -> go to `Sell`
- User wants to buy listed NFTs -> go to `Query Orders`, then `Buy`
- User wants to place a bid or collection offer -> go to `Offer`
- User wants to accept an existing offer on their NFT -> go to `Query Orders` with `side=0`, then `Accept Offer`
- User wants to browse current public listings -> go to `Query Orders`
- User wants to view an account's listings/orders -> use `Query Account Orders`
- User wants to cancel their own listing/order -> use `Query Account Orders`, then `Query Orders` filtered by maker if needed, then `Cancel`
- User wants stats, rankings, activity history, or slug resolution -> hand off to `element-nft-tracker`
- User provides only `0x...` in a trading context -> first ask for the network, then confirm whether that value is the NFT collection contract address for the intended query or order flow

## Required Inputs By Task

Ask for the required parameters first for every operation.

- `Sell`: network, collection address, token ID, price
- `Buy`: network, collection address, then let the user choose from queried orders
- `Offer`: network, collection address, offer price, asset schema
- `Accept Offer`: network, order object, and token ID for collection-wide offers
- `Query`: network, collection address
- `Query Account Orders`: network, optional `wallet_address`
- `Cancel`: network, order ID or enough context to find the user's order
- `GetAddress`: network

Additional guidance:

- Default to ERC721 only for listing flows when quantity is not specified
- If sell creation fails because the collection is actually ERC1155, query schema and retry as ERC1155 with quantity
- For offer flows, explicitly confirm `ERC721` or `ERC1155`; do not guess the schema
- For ERC1155 buy or offer flows, ask for quantity when needed
- For ERC1155 sell flows, treat the user-provided price as the total listing price by default unless the user explicitly says it is a unit price
- For ERC1155 sell previews, clearly show both total price and unit price
- For sell flows, do not hand-calculate `expirationTime` unless the user explicitly asked for a custom expiry; omit it and let the SDK default to 7 days
- For query flows, ask for the required `network` or `chain` before executing; never scan all chains by default

## Preflight Checklist

Before any state-changing action, confirm:

- `network` is explicitly confirmed
- Any `0x...` contract input used as an NFT contract address is a 42-character EVM address, not a transaction hash
- The required NFT details are present: `tokenId` for listings, `assetId` for collection-wide offer acceptance, `quantity` for ERC1155 when needed
- For `offer`, `assetSchema` is explicitly confirmed as `ERC721` or `ERC1155`
- `paymentToken` has been resolved correctly for the selected chain, or omitted intentionally
- For `erc721sell`, custom `paymentToken` is placed inside `sellOrders`
- For `erc1155sell`, custom `paymentToken` is placed inside `erc1155sellOrder`
- If the payment token is unfamiliar, check [payment-tokens.md](references/payment-tokens.md) instead of guessing
- The order object came directly from query results for `buy`, `acceptOffer`, or `cancel`; do not hand-reconstruct order fields
- The preview has been shown
- Explicit confirmation has been received

## Execution Entry Point

Primary executor:

- `scripts/entry.ts` handles `erc721sell`, `erc1155sell`, `buy`, `offer`, `acceptOffer`, `query`, `queryAccountOrders`, `cancel`, and `getAddress`

Invocation pattern:

```bash
node scripts/lib/entry.js "$INPUT"
```

The script accepts JSON either as the first CLI argument or from stdin.

Assistant workflow:

1. Identify the intended operation
2. Ask for all required parameters before execution
3. Build the JSON payload with `jq`
4. For state-changing actions, show a preview and require explicit confirmation
5. Execute through `scripts/lib/entry.js`
6. Return the structured result

## Quick Start Conversation Patterns

```text
User: Cancel order ID 789
Assistant: [Shows order details] Confirm?
User: CONFIRM CANCEL ORDER
Assistant: Order canceled

User: Show my current NFT listings on Element
Assistant: Which chain do you want to query? For example `base`, `eth`, `bsc`, `polygon`, `linea`, or `arbitrum`
User: base
Assistant: [Queries the current listings on that chain]

User: Query orders for collection 0x123...
Assistant: Which network should I query? For example `base`, `eth`, `bsc`, `polygon`, `linea`, or `arbitrum`
User: base
Assistant: [Queries the orders for that collection on Base]

User: Query order 0xCA3605ca7cffAA27a8D9a9B7E41bcb3c51e590D9
Assistant: Which network should I query? For example `base`, `eth`, `bsc`, `polygon`, `linea`, or `arbitrum`
User: base
Assistant: Is `0xCA3605ca7cffAA27a8D9a9B7E41bcb3c51e590D9` the NFT collection contract address for the query?
```

## Agent Knowledge Base

### Token Decimals

`amountInWei = amountInToken * (10 ^ decimals)`

| Token | Decimals | 1 unit |
|-------|----------|--------|
| ETH, USDT (BSC) | 18 | `1000000000000000000` |
| USDC (Base) | 6 | `1000000` |

**Examples:**
```
0.5 ETH = 0.5 * 10^18 = 500000000000000000
100 USDC = 100 * 10^6 = 100000000
```

For supported custom payment tokens, read [payment-tokens.md](references/payment-tokens.md). The current rule is:

- `bsc`: supports `USDT` and `USD1`
- `base`: supports `USDC`
- `polygon`: supports `ETH`
- other chains: support only native token and wrapped native token
- any other ERC20 should be treated as unsupported

If the table provides token decimals and the operation is `buy`, pass them as `paymentTokenDecimals` instead of relying on runtime detection.

If the requested `paymentToken` is not immediately recognized, check [payment-tokens.md](references/payment-tokens.md) first. Do not guess token addresses or token symbols. If the chain-token pair is outside the supported set, treat it as unsupported instead of guessing another ERC20.

### Supported Networks

Supported networks come from the SDK and entry script. Commonly used networks include:

`eth`, `bsc`, `polygon`, `arbitrum`, `base`, ...

The current implementation supports 27 chains in total.

Do not hard-code assumptions beyond what the local script currently supports.

### Collection URL

Element Market collection page format:

`https://element.market/collections/[slug]`

Do not construct this URL from the contract address directly.

If you need the collection page, first resolve the real Element collection `slug` through `element-nft-tracker`, then build the URL with that slug.

## Trading Operations

### Reference Selection Guide

When an actual operation is about to be constructed or executed, you must open and follow the matching reference file first. Do not rely on the main skill alone for payload construction.

- Create a new listing -> open [sell.md](references/sell.md)
- Browse public listings or offers -> open [query-orders.md](references/query-orders.md)
- View the user's own current orders -> open [query-account-orders.md](references/query-account-orders.md)
- Create a bid or collection-wide offer -> open [offer.md](references/offer.md)
- Accept a buy-side order -> open [accept-offer.md](references/accept-offer.md)
- Buy a sell-side order -> open [buy.md](references/buy.md)
- Cancel an existing order -> open [cancel.md](references/cancel.md)
- Get the configured wallet address -> open [get-address.md](references/get-address.md)

Each operation now has its own reference file. Use the main skill for routing and global rules, then open only the operation reference you need:

- `Sell`: open [sell.md](references/sell.md) when creating a new listing, including ERC721, ERC1155, or custom payment token listings
- `Query Orders`: open [query-orders.md](references/query-orders.md) when browsing public orders, selecting orders to buy, or finding offers to accept
- `Query Account Orders`: open [query-account-orders.md](references/query-account-orders.md) when the user wants the current listings or orders for a specific wallet on a specific chain
- `Offer`: open [offer.md](references/offer.md) when creating a collection offer or token-specific bid
- `Accept Offer`: open [accept-offer.md](references/accept-offer.md) when filling a buy-side order, especially collection-wide offers that require `assetId`
- `Buy`: open [buy.md](references/buy.md) when filling sell-side orders returned by query
- `Cancel`: open [cancel.md](references/cancel.md) when canceling an order using the exact returned order object
- `Get Wallet Address`: open [get-address.md](references/get-address.md) when the user wants the configured wallet address for a supported network

Execution rule:

- For any concrete operation request, read the corresponding reference before building the command or JSON payload
- Do not execute from the main skill alone when a matching reference file exists

## Failure Recovery Rules

If an operation cannot proceed cleanly, use these fallbacks:

- If ERC721 listing fails because the asset is actually ERC1155, retry with ERC1155 after confirming quantity
- If a `paymentToken` is unfamiliar, check [payment-tokens.md](references/payment-tokens.md); do not guess
- If the requested ERC20 is outside the supported set in the payment token reference, treat it as unsupported on that chain
- When showing a token symbol for price or payment token, only use an exact `chain + address` match from the payment token reference; otherwise show the address instead of guessing
- Do not claim that a collection or asset rejects a supported payment token before execution produces a real error
- If an Element collection slug is unavailable, do not show the collection URL
- If a collection-wide offer is selected without `assetId`, ask for `assetId` before execution
- If `side=0` and `saleKind=7`, treat the order as a collection-wide offer; do not describe `tokenId=0` as a real NFT `#0`
- If an ERC1155 flow is selected without `quantity`, ask for `quantity` before execution
- If the available order data is only a summary and not the full returned order object, do not hand-construct missing order fields
- If a buy-related validation error says order fields are missing, return to `query` and reuse the exact returned order object
- Do not infer insufficient gas or token balance unless there is explicit evidence for it
- Do not suggest a different token price as an approximate substitute, such as `0.3 ETH ~= 0.3 USDC`

## Transaction Preview Template

Before executing any state-changing order operation, show a preview like this:

### [OPERATION] Order Preview

**Network:** `[NETWORK]` | **Wallet:** `[WALLET_ADDRESS]`

| Field | Value |
|-------|-------|
| **Collection** | `[COLLECTION_ADDRESS]` |
| **Element Page** | Show only if a real `[SLUG]` has been resolved through `element-nft-tracker` |
| **Token ID** | `[TOKEN_ID]` if applicable |
| **Price** | `[PRICE]` `[TOKEN_SYMBOL]` |
| **Expiration** | `[EXPIRATION_TIME]` |

Notes for the user:

- This will sign and broadcast a blockchain transaction
- Transactions cannot be undone once confirmed
- Gas fees will be deducted from the wallet
- Do not show protocol fee in the preview
- Do not show an Element collection URL unless you have resolved the real collection slug

Confirmation format:

`CONFIRM [OPERATION] ORDER`

Example:

`CONFIRM SELL ORDER`

## Result Formatting

Display results based on the returned JSON `operation` field.

`entry.ts` already formats `listingTime` and `expirationTime` into readable UTC date-time strings in its structured output. Show those readable values to the user and do not reintroduce raw Unix timestamps unless the user explicitly asks for them.

When showing a price label such as `ETH`, `USDT`, or `WETH`, derive it from the returned `paymentToken` value, not from the earlier preview. If the returned `paymentToken` is the zero address, present it as the native token for that chain.

### `erc721sell`

**Status:** success

**Succeeded:** `[N]` | **Failed:** `[M]`

**Succeed list:**

| Order ID | Collection | Token | Price | Expires At |
|----------|------------|-------|-------|------------|
| `[ORDER_ID]` | `[CONTRACT]` | `[TOKEN_ID]` | `[PRICE]` `[TOKEN]` | `[READABLE_EXPIRATION_TIME]` |

**Failed list:**

| Asset | Error |
|-------|-------|
| `[CONTRACT]/[TOKEN_ID]` | `[ERROR]` |

### `erc1155sell`

| Field | Value |
|-------|-------|
| **Status** | `success` |
| **Operation** | `erc1155sell` |
| **Order ID** | `[ORDER_ID]` |
| **Collection** | `[CONTRACT]` |
| **Token ID** | `[TOKEN_ID]` |
| **Price** | `[PRICE]` `[TOKEN]` |
| **Payment Token** | `[PAYMENT_TOKEN]` |
| **Listed At** | `[READABLE_LISTING_TIME]` |
| **Expires At** | `[READABLE_EXPIRATION_TIME]` |

### `offer`

| Field | Value |
|-------|-------|
| **Status** | `success` |
| **Operation** | `offer` |
| **Order ID** | `[ORDER_ID]` |
| **Collection** | `[CONTRACT]` |
| **Price** | `[PRICE]` `[TOKEN]` |
| **Payment Token** | `[PAYMENT_TOKEN]` |
| **Listed At** | `[READABLE_LISTING_TIME]` |
| **Expires At** | `[READABLE_EXPIRATION_TIME]` |

### `acceptOffer`

| Field | Value |
|-------|-------|
| **Status** | `[success|failed]` |
| **Order ID** | `[ORDER_ID]` |
| **Maker** | `[ADDRESS]` |
| **Collection** | `[CONTRACT]` |
| **Token ID** | `[TOKEN_ID]` |
| **Schema** | `[SCHEMA]` |
| **Quantity** | `[QUANTITY]` |
| **Payment Token** | `[PAYMENT_TOKEN]` |
| **Proceeds** | `[PRICE]` `[TOKEN]` |
| **Tx Hash** | `[TX_HASH]` |
| **Gas Used** | `[GAS_USED] wei` |
| **Explorer** | [View on Explorer]([EXPLORER_URL]/tx/[TX_HASH]) |

### `buy`

| Field | Value |
|-------|-------|
| **Status** | `[success|failed]` |
| **Tx Hash** | `[TX_HASH]` |
| **Gas Used** | `[GAS_USED] wei` |
| **Explorer** | [View on Explorer]([EXPLORER_URL]/tx/[TX_HASH]) |

**Purchased Orders:**

| Order ID | Collection | Token ID | Schema | Quantity | Cost |
|----------|------------|----------|--------|----------|------|
| `[ORDER_ID]` | `[CONTRACT]` | `[TOKEN_ID]` | `[SCHEMA]` | `[REQUESTED_QUANTITY]` | `[COST]` `[TOKEN]` |

### `cancel`

| Field | Value |
|-------|-------|
| **Status** | `success` |
| **Cancelled** | `[N]` order(s) |

**Transactions:**

| Hash | Status | Block | Gas | Explorer |
|------|--------|-------|-----|----------|
| `[TX_HASH]` | `[success|failed]` | `[BLOCK]` | `[GAS_USED]` | [View]([EXPLORER_URL]/tx/[TX_HASH]) |

### `query`

| Field | Value |
|-------|-------|
| **Status** | `success` |
| **Found** | `[N]` order(s) |

**Order #1:**

| Field | Value |
|-------|-------|
| **Side** | `[buy|sell]` |
| **Order ID** | `[ORDER_ID]` |
| **Maker** | `[ADDRESS]` |
| **Collection** | `[CONTRACT]` |
| **Token ID** | `[TOKEN_ID]` |
| **Schema** | `[SCHEMA]` |
| **Available Quantity** | `[QUANTITY]` |
| **Price** | `[PRICE]` `[TOKEN]` |
| **Payment Token** | `[PAYMENT_TOKEN]` |
| **Listed At** | `[READABLE_LISTING_TIME]` |
| **Expires At** | `[READABLE_EXPIRATION_TIME]` |

### `queryAccountOrders`

| Field | Value |
|-------|-------|
| **Status** | `success` |
| **Chain** | `[CHAIN]` |
| **Using Default Account** | `[true|false]` |
| **Wallet Address** | `[WALLET_ADDRESS_OR_NULL]` |
| **Found** | `[N]` order(s) |

**Order #1:**

| Field | Value |
|-------|-------|
| **Name** | `[NAME]` |
| **Collection** | `[COLLECTION_NAME]` |
| **Collection Address** | `[CONTRACT]` |
| **Token ID** | `[TOKEN_ID]` |
| **Side** | `[buy|sell]` |
| **Price** | `[PRICE]` |
| **Price USD** | `[PRICE_USD]` |
| **Standard** | `[STANDARD]` |
| **Expires At** | `[READABLE_EXPIRATION_TIME]` |

Display rules:

- If `count > 1`, do not present the result as if there were only one order
- When multiple orders are returned, list each order or explicitly state that the display is truncated
- The shown order count must match the actual returned `count`

### `getAddress`

| Field | Value |
|-------|-------|
| **Wallet** | `[ADDRESS]` |

## Links

- Create API key: https://element.market/apikeys
- Mainnet: https://element.market
