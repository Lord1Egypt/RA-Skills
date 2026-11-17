---
name: elfa-ai
description: >
  Use this skill for Elfa API crypto social intelligence and Auto condition-engine workflows:
  trending tokens, narratives, mentions, smart account stats, token news, trending contract
  addresses, AI market chat, integration examples, curl/code snippets, automated alerts,
  EQL queries, trigger pipelines, and agent workflows that react to market conditions.
  Auto can also place live perp trades on Hyperliquid and GMX (market/limit orders with
  TP/SL) when a condition fires, trigger on Kalshi and Polymarket prediction markets,
  trigger on funding rates, liquidation cascades, and the Fear & Greed index, re-fire
  recurring plans via `repeat` (including trade actions), run calendar schedules via
  `cron.schedule`, and trade crypto plus HIP-3 assets (equities, indices, commodities, FX,
  pre-IPO — 24/7). Supports API-key calls and x402 pay-per-request USDC on Base, Arbitrum,
  Polygon, or Avalanche.
metadata:
  openclaw:
    requires:
      bins:
        - curl
    anyBins:
      - jq
      - python3
    primaryEnv: ELFA_API_KEY
    envVars:
      - name: ELFA_API_KEY
        required: false
        description: >-
          Elfa API key for API-key auth mode. Optional — x402 keyless USDC
          payments work without any key. Free key (1,000 credits) at
          https://go.elfa.ai/claude-skills.
      - name: ELFA_HMAC_SECRET
        required: false
        description: >-
          HMAC secret (used with openssl) to sign Auto trade-action mutations
          and exchange linking. Not needed for notification-only queries.
      - name: ELFA_AGENT_SECRET
        required: false
        description: >-
          Agent identity secret sent as x-elfa-agent-secret for x402 Auto
          requests.
    homepage: https://docs.elfa.ai
    emoji: "\U0001F4E1"
---

# Elfa API Skill

This skill enables agents to work with the [Elfa API](https://api.elfa.ai) — a social listening,
market context layer, and automated condition engine for crypto. Elfa ingests real-time data
from Twitter/X, Telegram, and other sources, then structures sentiment, narratives, and
attention shifts into actionable trading insights. The **Auto** subsystem adds a managed
condition engine and trigger pipeline — describe what to watch for, and Auto evaluates
continuously and fires actions when conditions are met. The **Trade** subsystem adds
direct, synchronous order execution — place and manage perp orders on Hyperliquid and GMX
immediately, without a condition or query.

Full documentation: [docs.elfa.ai](https://docs.elfa.ai)

> **Staying current — check weekly.** This skill is updated on a **weekly** cadence to track
> Elfa API and Auto changes. Before relying on it, check whether your copy may be stale: if it
> has been **more than 7 days** since this skill was last fetched/installed (or you are unsure),
> re-fetch the latest version before acting —
> - **Skill package & changelog:** <https://go.elfa.ai/claude-skills> (and the
>   [`elfa-ai/skills`](https://github.com/elfa-ai/skills) repo).
> - **Live source of truth:** [docs.elfa.ai](https://docs.elfa.ai) — when this skill and the
>   docs disagree, the docs win; prefer the docs and flag the mismatch to the user.
>
> When in doubt about a specific endpoint, parameter, or price, verify against
> [docs.elfa.ai](https://docs.elfa.ai) at call time rather than trusting a possibly-stale copy.

## Environment and credentials

Elfa supports API-key auth and x402 keyless payments. API keys are optional when using x402.

| Variable | Required | Use |
|---|---:|---|
| `ELFA_API_KEY` | No | API-key authenticated requests. Get a free key at <https://go.elfa.ai/claude-skills>. |
| `ELFA_HMAC_SECRET` | No | HMAC secret for Auto trade-action mutations (`market_order`, `limit_order`, or `llm` callbacks to those) and exchange linking, **and for all Trade (`/v2/trade/*`) write routes** (place / cancel / modify / close / tpsl). Auto notification-only mutations (`notify`, `telegram_bot`, `webhook`, or `llm` callbacks to those) and Trade previews accept unsigned requests; the HMAC requirement on trade actions reflects current documented policy and is subject to change. Always-signing remains compatible if you prefer to avoid edge cases. |
| `ELFA_AGENT_SECRET` | No | Persistent agent identity secret for x402 Auto. Generate once with `openssl rand -hex 32` and reuse for query lifecycle calls. |

x402 wallet signing is handled client-side by `@x402/fetch` or `@x402/axios`.

## When to use this skill

- User asks about **trending tokens, narratives, or contract addresses** in crypto
- User wants **social mentions** for a specific ticker or keyword
- User wants **smart stats** (smart followers, engagement) for a Twitter/X account
- User wants an **AI-generated market summary, macro overview, or token analysis**
- User asks how to **integrate, call, or use the Elfa API**
- User wants **code examples** (curl, Python, JavaScript/TypeScript) for Elfa endpoints
- User mentions "elfa" in a crypto or trading data context
- User wants to **set up automated alerts or monitoring** on price, indicators, or narratives
- User wants to **build condition-based triggers** (e.g., "alert me when BTC crosses 100k")
- User mentions **Auto**, **EQL**, **condition engine**, or **trigger pipeline** in a crypto context
- User wants **agent workflows** that react to market conditions automatically
- User wants to **build queries with Builder Chat** using natural language

## API Overview

**Base URL:** `https://api.elfa.ai`
**Version:** v2 (current)
**Docs:** [docs.elfa.ai](https://docs.elfa.ai)

### Two access modes

Elfa supports two independent ways to authenticate requests:

| Mode | Endpoint prefix | Auth header | Best for |
|---|---|---|---|
| **API key** | `/v2/` | `x-elfa-api-key: YOUR_KEY` | Humans & apps with a registered key |
| **x402 (keyless)** | `/x402/v2/` | `PAYMENT-SIGNATURE: <signed-payload>` | Agents & wallets — no signup needed |

Both modes access the same data. The only difference is how you authenticate:
- **API key** — register at https://go.elfa.ai/claude-skills, get 1,000 free credits.
- **x402** — pay per request with USDC on Base, Arbitrum, Polygon, or Avalanche. No
  registration, no API key. Currently in beta with a 70% discount on Auto endpoints.

### Endpoints at a glance

#### Data endpoints

All endpoints below work with both `/v2/` (API key) and `/x402/v2/` (keyless) prefixes,
except `key-status` which is API key mode only.

| Endpoint | Method | Description | Credits |
|---|---|---|---|
| `/v2/key-status` | GET | API key usage & limits (API key only) | Free |
| `/v2/aggregations/trending-tokens` | GET | Trending tokens by mention count | 1 |
| `/v2/account/smart-stats` | GET | Smart follower & engagement stats | 1 |
| `/v2/data/top-mentions` | GET | Top mentions for a ticker symbol | 1 |
| `/v2/data/keyword-mentions` | GET | Search mentions by keywords or account | 1 |
| `/v2/data/event-summary` | GET | AI event summaries from keyword mentions | 5 |
| `/v2/data/trending-narratives` | GET | Trending narrative clusters | 5 |
| `/v2/data/token-news` | GET | Token-related news mentions | 1 |
| `/v2/aggregations/trending-cas/twitter` | GET | Trending contract addresses (Twitter) | 1 |
| `/v2/aggregations/trending-cas/telegram` | GET | Trending contract addresses (Telegram) | 1 |
| `/v2/chat` | POST | AI chat with multiple analysis modes | Speed-based |

#### Auto endpoints (Condition Engine)

Auto endpoints are available under `/v2/auto/` (API key, HMAC for trade/exchange routes) and
`/x402/v2/auto/` (keyless). See [Auto docs](https://docs.elfa.ai/auto/overview) for full details.

> **Auth column legend (tables below).** `API key` = `x-elfa-api-key` only (no HMAC).
> `Conditional` = HMAC required only when the EQL action is trade-flavoured
> (`market_order`, `limit_order`, or `llm` callback to those); notification-only actions
> (`notify`, `telegram_bot`, `webhook`, `llm` callback to those) skip HMAC. `HMAC` = HMAC
> always required. See [HMAC Bypass for Notification-Only Mutations](#hmac-bypass-for-notification-only-mutations).

**API key mode (`/v2/auto/*`):**

_Query lifecycle:_

| Endpoint | Method | Description | Auth |
|---|---|---|---|
| `/v2/auto/chat` | POST | Builder Chat — AI-assisted query building (produces drafts only) | API key |
| `/v2/auto/queries/validate` | POST | Validate EQL and preview cost | API key |
| `/v2/auto/queries` | POST | Create and activate a query | Conditional |
| `/v2/auto/queries` | GET | List queries | API key |
| `/v2/auto/queries/:queryId` | GET | Poll query status and executions (resolves query or draft) | API key |
| `/v2/auto/queries/:queryId/cancel` | POST | Cancel an `active` query (returns `409` if status is terminal) | Conditional |
| `/v2/auto/queries/:queryId` | DELETE | Delete a terminal query — only when status is `triggered` / `expired` / `cancelled` / `failed` (returns `409` otherwise; active queries must be cancelled first) | Conditional |
| `/v2/auto/queries/:queryId/stream` | GET | Stream notifications via SSE | API key |

_Query drafts (editable, not yet active):_

| Endpoint | Method | Description | Auth |
|---|---|---|---|
| `/v2/auto/queries/drafts` | POST | Create or update (upsert) a query draft | Conditional |
| `/v2/auto/queries/drafts` | GET | List editable query drafts | API key |
| `/v2/auto/queries/drafts/:draftId` | GET | Get a specific draft (legacy — prefer `GET /queries/{queryId}`) | API key |
| `/v2/auto/queries/drafts/:draftId` | DELETE | Delete a query draft | API key |
| `/v2/auto/queries/drafts/:draftId/validate` | POST | Validate a stored draft | API key |
| `/v2/auto/queries/drafts/:draftId/convert` | POST | Convert a draft into an active query | Conditional |

_LLM sessions (for `action.type: "llm"` queries):_

| Endpoint | Method | Description | Auth |
|---|---|---|---|
| `/v2/auto/queries/:queryId/sessions` | GET | List LLM sessions | API key |
| `/v2/auto/queries/:queryId/sessions/:sessionId` | GET | Get full LLM session details | API key |

_Executions (trigger fire records):_

| Endpoint | Method | Description | Auth |
|---|---|---|---|
| `/v2/auto/executions` | GET | List execution records | API key |
| `/v2/auto/executions/:executionId` | GET | Get a single execution record | API key |

_Exchange connections (for live trade actions):_

| Endpoint | Method | Description | Auth |
|---|---|---|---|
| `/v2/auto/exchanges` | POST | Connect an exchange integration | HMAC |
| `/v2/auto/exchanges` | GET | List connected exchanges | API key |
| `/v2/auto/exchanges/:exchange` | DELETE | Disconnect an exchange | HMAC |

_Other:_

| Endpoint | Method | Description | Auth |
|---|---|---|---|
| `/v2/auto/validate-symbol/:exchange/:symbol` | GET | Check whether a symbol is supported on a venue (`exchange` = `hyperliquid` / `gmx`) — pre-flight for trade actions **and for `price`/`ta` data sources** | API key |

**x402 mode (`/x402/v2/auto/*`)** — note: some routes use POST instead of GET:

| Endpoint | Method | Description |
|---|---|---|
| `/x402/v2/auto/chat` | POST | Builder Chat |
| `/x402/v2/auto/queries/validate` | POST | Validate EQL and preview cost |
| `/x402/v2/auto/queries` | POST | Create and activate a query |
| `/x402/v2/auto/queries/:queryId` | POST | Poll query status (POST, not GET) |
| `/x402/v2/auto/queries/:queryId/cancel` | POST | Cancel an `active` query |
| `/x402/v2/auto/queries/:queryId/stream` | GET | Stream notifications via SSE |
| `/x402/v2/auto/queries/:queryId/sessions` | POST | List LLM sessions (POST, not GET) |
| `/x402/v2/auto/queries/:queryId/sessions/:sessionId` | POST | Get LLM session details (POST, not GET) |

> **Note on x402 Auto scope.** Trade execution actions are not available via x402. Exchange connections, drafts, executions, and the terminal-query DELETE endpoint are API-key-mode only. x402 Auto covers the core monitoring lifecycle (chat, validate, create, poll, cancel, stream, sessions).

#### Trade endpoints (Direct Execution)

Trade is **direct, synchronous** order execution — one request, one order, no condition
engine. Same `x-elfa-api-key` + HMAC auth and same venues (`hyperliquid`, `gmx`) as Auto;
they differ only in _when_ the order fires. Trade is **API-key mode only** (no x402). See
[Trade docs](https://docs.elfa.ai/trade/overview) for full details.

All endpoints are `POST` under `/v2/trade`. HMAC is required on every **write**; previews
are free and unsigned.

| Endpoint | Method | Description | HMAC | Credits |
|---|---|---|---|---|
| `/v2/trade/orders` | POST | Place a market or limit order | Yes | 1 |
| `/v2/trade/orders/preview` | POST | Dry-run an order (`wouldExecute`) | No | Free |
| `/v2/trade/orders/cancel` | POST | Cancel a resting order | Yes | Free |
| `/v2/trade/orders/modify` | POST | Modify size / price / trigger price | Yes | Free |
| `/v2/trade/positions/close` | POST | Close a position (full or partial) | Yes | 1 |
| `/v2/trade/positions/close/preview` | POST | Dry-run a close | No | Free |
| `/v2/trade/positions/tpsl` | POST | Set take-profit / stop-loss | Yes | 1 |
| `/v2/trade/positions/tpsl/preview` | POST | Dry-run a TP/SL update | No | Free |

> **Credits & billing.** 1 credit per executed order (place / close / tpsl), charged only
> on a `2xx`; failed fills (`422`/`502`) are never billed. Previews, cancels, and modifies
> are free. Trade bypasses the monthly spend-cap hard-stop (a key over its limit still trades
> and bills overage).

For full parameter details, see the [Elfa API documentation](https://docs.elfa.ai).

**Machine-readable manifest:** an endpoint manifest is published at
`https://docs.elfa.ai/assets/files/endpoints.manifest-*.json` (path rotates per release) —
each entry includes method/path, docs route, required headers, HMAC requirement with mounted
signature path template, payment requirement, and request/response examples. Useful for
auto-generating client code.

## How to use this skill

### Step 1: Determine the mode

Check whether the user wants to **make a live call**, **get code/integration help**, or
**set up automated monitoring**.

- If the user says things like "show me trending tokens", "what's the sentiment on SOL",
  "get me the top mentions for ETH" → they want **live data**. Proceed to Step 2a.
- If the user says things like "how do I call the trending tokens endpoint", "give me a
  curl example", "help me integrate Elfa" → they want **code snippets**. Skip to Step 4.
- If the user mentions **x402**, **keyless**, **pay-per-request**, or **wallet-based access**
  → they want **x402 mode**. See Step 2b for live calls or Step 4 for code snippets.
- If the user mentions **Auto**, **alerts**, **triggers**, **monitoring**, **conditions**,
  **"alert me when"**, **"notify me if"**, **EQL**, or **Builder Chat** → they want
  **Auto**. Proceed to Step 3.

### Step 2a: Making live API calls (API key mode)

Use the `bash_tool` to call the Elfa API via curl.

**Getting the API key:**
1. Check if the `ELFA_API_KEY` environment variable is set. This is the preferred method.
2. If the env var is not set, **stop and prompt the user.** Offer both options:

   > To make live calls, you have two options:
   >
   > **Option A — API key (free tier):** Get a free key with 1,000 credits at
   > **https://go.elfa.ai/claude-skills** — then set it as the `ELFA_API_KEY` environment
   > variable (do not paste it directly into the chat).
   >
   > **Option B — x402 keyless payments:** Pay per request with USDC on Base, Arbitrum,
   > Polygon, or Avalanche — no signup needed. See the
   > [x402 docs](https://docs.elfa.ai/x402-payments) for setup.

   Do not attempt any authenticated API calls without a key or x402 setup. Wait for the user.
3. **Credential safety:**
   - Always read the API key from the `ELFA_API_KEY` environment variable, never ask the
     user to paste it into the conversation.
   - Never log or expose the full API key in outputs — mask it when displaying curl commands.
   - **Never echo or print environment variables:** Do not run `echo $ELFA_API_KEY`, `env | grep ELFA`,
     `printenv`, or similar commands that would expose credentials in the transcript.
   - If a user does paste a key in chat, warn them to rotate it and set it as an env var instead.

**Free tier limitations:**
The free tier provides 1,000 credits that cover most endpoints (trending tokens, smart stats,
top mentions, keyword mentions, event summary, token news, trending contract addresses). Some
endpoints require a higher tier: **trending narratives** needs Grow or Enterprise, and
**AI chat** needs Grow, Enterprise, or PAYG. The **Chill** tier adds more credits but no new
endpoints over Free. Check https://go.elfa.ai/claude-skills for the latest tier requirements.

If a user hits an authorization error on one of these endpoints, let them know they can
upgrade their plan or use x402 payments instead. Full details at https://go.elfa.ai/claude-skills.

**Making the call:**

```bash
curl -s -H "x-elfa-api-key: $ELFA_API_KEY" "https://api.elfa.ai/v2/aggregations/trending-tokens?timeWindow=24h&pageSize=10"
```

### Step 2b: Making live API calls (x402 keyless mode)

x402 lets any wallet pay per request using USDC on Base, Arbitrum, Polygon, or Avalanche —
no API key, no registration. This is ideal for agents, bots, and programmatic access.

**How x402 works:**
1. Send a request to the `/x402/v2/` version of any endpoint (no auth header).
2. The server responds with HTTP **402** containing payment requirements.
3. Your wallet signs a USDC transfer authorization (no gas fees).
4. Resend the request with the signed payment in the `PAYMENT-SIGNATURE` header.
5. Server verifies payment, serves the response, and settles on-chain.

**x402 signing and security:**
- Signing happens **entirely client-side** using the `@x402/fetch` or `@x402/axios`
  libraries. The agent never handles, stores, or transmits private keys.
- The user's wallet private key is used only locally by the x402 library to sign
  EIP-712 typed data authorizing a specific USDC amount for a specific request.
- Never ask the user to share their wallet private key or seed phrase in the conversation.
- When generating x402 code examples, use `"0xYOUR_PRIVATE_KEY"` as a placeholder and
  advise the user to load it from an environment variable (e.g., `process.env.PRIVATE_KEY`).

**x402 details:**
- **Networks:** the server offers every supported network in the 402 response; your client
  signs on the first one it's registered for. Register the network(s) you hold USDC on.
- **Scheme:** `exact` (fixed price per request); asset is native Circle USDC (6 decimals).
- **Status:** Currently in beta.

| Network | Chain ID | USDC Address | Facilitator |
|---|---|---|---|
| Base | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | [xpay.sh](https://xpay.sh), [payai.network](https://facilitator.payai.network) |
| Arbitrum | `eip155:42161` | `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` | [payai.network](https://facilitator.payai.network) |
| Polygon | `eip155:137` | `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359` | [payai.network](https://facilitator.payai.network) |
| Avalanche | `eip155:43114` | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` | [payai.network](https://facilitator.payai.network) |

**x402 pricing (data endpoints):**

| Tier | Credits | USDC Cost | Endpoints |
|---|---|---|---|
| Standard | 1 | $0.009 | trending-tokens, smart-stats, keyword-mentions, token-news, top-mentions, trending-cas |
| Extended | 5 | $0.045 | event-summary, trending-narratives |
| Chat — fast | 5 | $0.045 | chat (speed: "fast") |
| Chat — expert | 18 | $0.162 | chat (speed: "expert", default) |

**Making an x402 call with curl (manual flow):**

```bash
# Step 1: Send request without payment — get 402 with payment requirements
curl -s https://api.elfa.ai/x402/v2/aggregations/trending-tokens?timeWindow=24h

# Step 2: After signing the payment payload with your wallet, resend with payment header
curl -s -H "PAYMENT-SIGNATURE: <base64-encoded-payment-payload>" \
  "https://api.elfa.ai/x402/v2/aggregations/trending-tokens?timeWindow=24h"
```

**Recommended: use the `@x402/fetch` library** which handles payment automatically:

```javascript
import { wrapFetchWithPayment } from "@x402/fetch";
import { ExactEvmScheme, toClientEvmSigner } from "@x402/evm";
import { x402Client } from "@x402/core/client";
import { createPublicClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const account = privateKeyToAccount("0xYOUR_PRIVATE_KEY");
const publicClient = createPublicClient({ chain: base, transport: http() });
const signer = toClientEvmSigner(account, publicClient);

const client = new x402Client().register(
  "eip155:8453",
  new ExactEvmScheme(signer));

const x402Fetch = wrapFetchWithPayment(fetch, client);

// Use x402Fetch exactly like regular fetch — payment is handled automatically on 402 responses
const response = await x402Fetch(
  "https://api.elfa.ai/x402/v2/aggregations/trending-tokens?timeWindow=24h");
const data = await response.json();
```

To pay on another network, swap the `base` chain import and register that scheme instead —
e.g. Arbitrum (`arbitrum` from `viem/chains`, `eip155:42161`). Register a scheme for each
network you want to pay from; the client uses the first one the server also accepts.

**x402 with the Chat endpoint (POST):**

```javascript
const response = await x402Fetch(
  "https://api.elfa.ai/x402/v2/chat",
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message: "What is the current sentiment on BTC?",
      analysisType: "chat",
      speed: "fast", // "fast" = 5 credits ($0.045), "expert" = 18 credits ($0.162)
    }),
  });
const data = await response.json();
console.log(data.data.message);
```

**Presenting results:**
- Parse the JSON response and present it in a clean, readable format.
- For trending tokens: show a ranked table with token name, mention count, and change %.
- For mentions: show tweet links, engagement metrics, and account info.
  Note: Elfa returns tweet IDs but not tweet text content — let the user know they'll
  need their own X (Twitter) API key to fetch the actual tweet content.
- For narratives/summaries: present the narrative text with source links.
- For the chat endpoint: display the AI response cleanly.
- If the response contains an error, explain what went wrong and suggest fixes.

### Step 3: Auto — Condition Engine and Trigger Pipeline

Auto is a managed **condition engine + trigger pipeline** for agents. You describe what to
watch for (price, technical indicators, LLM-evaluated conditions, scheduled checks,
prediction-market activity, funding rates, liquidation cascades, market sentiment), and Auto
evaluates continuously and fires actions when conditions resolve to true. Assets are not
crypto-only — HIP-3 perps cover equities, indices, commodities, FX, and pre-IPO names, 24/7.

Full Auto docs: [docs.elfa.ai/auto/overview](https://docs.elfa.ai/auto/overview)

#### Lifecycle Sequence (Enforced)

For API key lifecycle/cleanup calls, preserve this order when each operation applies:

1. `POST /v2/auto/queries/validate` — validate EQL and preview cost
2. `POST /v2/auto/queries` — create and activate
3. `POST /v2/auto/queries/{queryId}/cancel` — only if stopping an `active` query before it reaches terminal status (returns `409` once terminal)
4. `DELETE /v2/auto/queries/{queryId}` — only after status is terminal (`triggered` / `expired` / `cancelled` / `failed`); active queries must be cancelled first

> **Cancel and delete are distinct operations.** `POST /cancel` flips an active query to `cancelled` (terminal). `DELETE` removes the record entirely and only works on terminal queries. Sending `DELETE` on an active query returns `409 Conflict`.

**Important — Exchange preflight for trade actions:**
For trade actions (`market_order`, `limit_order`, or `llm` with a trade callback), **always call `GET /v2/auto/exchanges` before creating the query** to verify the target exchange is connected. Without an active exchange connection, query creation may succeed but the trade action fails at execution time with `AGENT_WALLET_REQUIRED`. If the exchange is not connected, inform the user they need to link it via the Elfa dashboard before the trade trigger can work.

x402 mode supports the same lifecycle except: x402 has no `DELETE` endpoint (cancel-only), and trade actions are not available via x402.

#### Intent Routing (Strict)

Pick the condition source by user intent **before** writing condition args:

| Intent | Required source | Minimum required fields |
|---|---|---|
| Account-anchored post intent (`@user posts ...`) | `source: "tweet"` | `args.username` (no `@`), `args.text`, `args.minConfidence` (use `80` if user gives no threshold) |
| World event intent (ETF approval, exploit, sanctions, etc.) | `source: "news"` | `args.text`, `args.minConfidence` (use `80` if user gives no threshold) |
| Prediction-market move/lifecycle on a named open Kalshi market | `source: "kalshi"` | `method` (e.g. `yes_price`, `status`, `result`), `args.ticker` (a currently-open Kalshi market), `operator`/`value` per the per-method allowlists |
| Prediction-market price/trade on a Polymarket outcome token | `source: "polymarket"` | `method` (`price`, `bid`, `ask`, `size`, `side`), `args.ticker` (outcome-token `asset_id`), `operator`/`value` per the per-method allowlists |
| Perp funding-rate intent (overheated funding, funding flips negative) | `source: "funding"` | `method` (prefer `annualized_rate`), `args.ticker` as `SYMBOL:EXCHANGE` (e.g. `BTC:BINANCE`) |
| Liquidation-flow intent (cascade, long/short flush) | `source: "liquidation"` | `method` (e.g. `total_usd_5m`, `total_pct_oi_1h`), `args.ticker` as `SYMBOL:EXCHANGE` |
| Market-wide sentiment (fear/greed regime) | `source: "fear_greed"` | `method` (`value` or `classification`), empty `args: {}` |
| Real-world catalyst moving an equity/index/commodity (rate decision, CPI, earnings) | the catalyst's own source (`kalshi` / `polymarket` / `news` / `price`) + a HIP-3 `symbol` in the action | Pick the catalyst source, then bridge to the asset class it moves — see [Catalyst Triggers](https://docs.elfa.ai/auto/catalyst-triggers) |
| Fuzzy world-state predicate not naturally expressible as a post or event | `source: "llm"` | `method: "athena_condition"`, `args.query`, `args.period` (`>= 1h`) |

When the prompt is account-anchored, **start with `tweet`** — do not route to `news` or `llm` first. When the prompt is event-anchored without a specific account, start with `news`. When the trigger maps to a concrete prediction market you can name (a Kalshi ticker or a Polymarket outcome-token id), use `kalshi` / `polymarket` (prefer them over `llm` for supported methods). Use `llm` (`athena_condition`) only when the predicate cannot reasonably be matched against a post, event, or named prediction market.

#### When to suggest Auto

- User wants alerts based on **price thresholds** ("alert me when BTC crosses 100k")
- User wants alerts based on **technical indicators** ("notify when RSI drops below 30")
- User wants **scheduled checks** ("check every 4 hours") or **calendar schedules** ("every weekday at 9am New York time" — use `cron.schedule`)
- User wants the **same alert to keep firing on its own condition** ("notify me every time BTC dips below 60k") — add the top-level `repeat` object (`cooldown` + `maxTriggers`)
- User wants **narrative/sentiment monitoring** ("alert when AI token narrative shifts")
- User wants **multi-condition triggers** ("BTC above 100k AND ETH above 3500")
- User wants to **compare live metrics** ("alert when price crosses above Bollinger Band")
- User wants **LLM analysis on trigger** ("when it triggers, run a full analysis")
- User wants **account-anchored social triggers** ("notify me when @cz_binance posts that Binance Alpha is listing a new token") — use **Signal: X/Twitter Post** (`source: "tweet"`)
- User wants **event-driven triggers** ("alert me when SEC approves a spot ETH ETF") — use **Signal: Event** (`source: "news"`)
- User wants **prediction-market triggers** ("alert when this Kalshi market's YES probability crosses 60%", "notify when the market settles YES", "alert when this Polymarket outcome trades above 60c") — use **Prediction Markets** (`source: "kalshi"` or `source: "polymarket"`)
- User wants **funding / liquidation / sentiment triggers** ("alert when BTC funding flips negative", "notify on an ETH liquidation cascade", "alert when Fear & Greed drops below 20") — use `source: "funding"` / `"liquidation"` / `"fear_greed"`
- User wants to **trade a macro catalyst on stocks/indices/commodities** ("go long the S&P when the market prices a Fed cut", "buy gold if CPI runs hot") — fire on the catalyst source and execute on a HIP-3 perp (24/7). See [Catalyst Triggers](https://docs.elfa.ai/auto/catalyst-triggers)

#### Auto access models

| Mode | Route prefix | Auth | Best for |
|---|---|---|---|
| API key + HMAC | `/v2/auto/*` | `x-elfa-api-key` on all + HMAC on trade mutations and exchange linking (notification-only mutations skip HMAC) | Apps, dashboards |
| x402 keyless | `/x402/v2/auto/*` | x402 payment + `x-elfa-agent-secret` | AI agents, bots |

#### HMAC signing (API key mode — trade mutations and exchange linking)

Trade-action mutations and exchange linking under `/v2/auto/*` require HMAC signing in
addition to `x-elfa-api-key`. **Notification-only mutations skip HMAC** so agents can
onboard without provisioning a secret — see
[HMAC Bypass for Notification-Only Mutations](#hmac-bypass-for-notification-only-mutations)
below for the per-route decision rule. Read-only endpoints (GET) only need the API key.
`POST /v2/auto/chat` is fully ungated and never needs HMAC.

> **Always-signing remains safe.** If your client signs every mutation, you do not need
> to opt into the bypass. Signed requests are accepted on every route. The bypass is
> purely an optimization for clients that want to skip the HMAC setup step.

**Required headers for signed mutations:**

```
x-elfa-api-key: <api_key>
x-elfa-timestamp: <unix_seconds>
x-elfa-signature: <hex_hmac_sha256>
```

**Signing payload:**

```
timestamp + method + mounted_path + body
```

**CRITICAL:** `mounted_path` is the path **inside** `/v2/auto`, NOT the full URL path.
- Request URL: `/v2/auto/queries` → signed path: `/queries`
- Request URL: `/v2/auto/chat` → signed path: `/chat`
- Request URL: `/v2/auto/queries/q_123` → signed path: `/queries/q_123`

**Replay protection:** timestamp must be within 30 seconds.

**TypeScript signing example:**

```typescript
import crypto from "crypto";

const hmacSecret = process.env.ELFA_HMAC_SECRET!;
const apiKey = process.env.ELFA_API_KEY!;

function signAutoRequest(method: string, mountedPath: string, body: string = "") {
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const payload = `${timestamp}${method}${mountedPath}${body}`;
  const signature = crypto
    .createHmac("sha256", hmacSecret)
    .update(payload)
    .digest("hex");
  return { timestamp, signature };
}

// Example: Create a query
const body = JSON.stringify({
  title: "BTC breakout alert",
  description: "Notify when BTC trades above 100k.",
  query: {
    conditions: {
      AND: [{ source: "price", method: "current", args: { symbol: "BTC", exchange: "hyperliquid" }, operator: ">", value: 100000 }]
    },
    actions: [{ stepId: "step_1", type: "notify", params: { message: "BTC crossed 100k" } }],
    expiresIn: "24h"
  }
});

const { timestamp, signature } = signAutoRequest("POST", "/queries", body);

const response = await fetch("https://api.elfa.ai/v2/auto/queries", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "x-elfa-api-key": apiKey,
    "x-elfa-timestamp": timestamp,
    "x-elfa-signature": signature,
  },
  body,
});
```

**Bash signing example:**

```bash
TIMESTAMP=$(date +%s)
METHOD="POST"
PATH_SIGN="/queries"
BODY='{"title":"BTC alert","query":{"conditions":{"AND":[{"source":"price","method":"current","args":{"symbol":"BTC","exchange":"hyperliquid"},"operator":">","value":100000}]},"actions":[{"stepId":"step_1","type":"notify","params":{"message":"BTC crossed 100k"}}],"expiresIn":"24h"}}'
SIGNATURE=$(echo -n "${TIMESTAMP}${METHOD}${PATH_SIGN}${BODY}" | openssl dgst -sha256 -hmac "$ELFA_HMAC_SECRET" | cut -d' ' -f2)

curl -s -X POST "https://api.elfa.ai/v2/auto/queries" \
  -H "Content-Type: application/json" \
  -H "x-elfa-api-key: $ELFA_API_KEY" \
  -H "x-elfa-timestamp: $TIMESTAMP" \
  -H "x-elfa-signature: $SIGNATURE" \
  -d "$BODY"
```

#### HMAC Bypass for Notification-Only Mutations

Mutations whose EQL action is a pure notification skip the HMAC requirement. Trade
execution and exchange linking continue to require HMAC unconditionally.

**Notification action types (HMAC bypassed):**

- `notify`
- `telegram_bot`
- `webhook`
- `llm` whose `params.callback.action.type` is one of the above

**Trade action types (HMAC required):**

- `market_order`
- `limit_order`
- `llm` whose `params.callback.action.type` is `market_order` or `limit_order`

**Decision is per-route:**

| Route | Decision input |
|---|---|
| `POST /v2/auto/queries`, `POST /v2/auto/queries/drafts` | Request body's `query.actions[*].type` |
| `POST /v2/auto/queries/drafts/:id/convert` | Stored draft's actions |
| `POST /v2/auto/queries/:id/cancel` (cancel active query) | Stored query's actions |
| `DELETE /v2/auto/queries/:id` (delete terminal query) | Stored query's actions |

If the lookup fails or the action type is unknown, HMAC is enforced (fail-safe). Unknown
action types added in future API versions default to requiring HMAC, so always-signing
clients keep working.

`POST /v2/auto/chat` is fully ungated regardless of content because it produces drafts
only — activation flows through `convert`, which is still gated when the draft is
trade-flavoured.

`POST /v2/auto/exchanges` and `DELETE /v2/auto/exchanges/:exchange` always require
HMAC — linking an exchange is the gateway to trade execution.

**Why this matters for agents.** An agent that only ever sends `notify` / `telegram_bot` /
`webhook` actions can call `POST /v2/auto/queries`, `POST /v2/auto/queries/:id/cancel`,
`DELETE /v2/auto/queries/:id`, etc. with just `x-elfa-api-key` — no HMAC secret
provisioning required. Agents that need trade execution must still configure
`ELFA_HMAC_SECRET` for the trade-flavoured calls and for exchange linking.

#### x402 Auto (keyless agent mode)

For x402 Auto, no API key or HMAC is needed. Instead:
- Send x402 payment headers (`PAYMENT-SIGNATURE` preferred, `X-PAYMENT` legacy)
- Include `x-elfa-agent-secret` on all query lifecycle routes

**Agent secret management:**
Generate a strong secret once and reuse it for all calls:

```bash
openssl rand -hex 32
# or: node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

Persist as `ELFA_AGENT_SECRET`. **Do not rotate per request** — x402 session ownership is
derived from `SHA256(secret)`. If you change secrets, your agent identity changes and
existing queries/sessions may become inaccessible.

#### Auto pricing (both modes)

**API-key mode (`/v2/auto/*`) — charged against your credit balance:**

| Operation | Credits | Notes |
|---|---|---|
| `POST /v2/auto/chat` (Builder Chat) | `1 + dynamic` | Base 1 credit + `ceil(request_cost * 750)` dynamic charge based on LLM usage |
| `POST /v2/auto/queries` (Create) | Simulation-driven | Baseline `5` + per simulated LLM call: fast `+5`, expert `+18` |
| `POST /v2/auto/queries/validate` | Free | Returns cost estimate — always call before Create |
| `GET /v2/auto/queries/*` (list, poll, stream, sessions) | Free | |
| `POST /v2/auto/queries/:queryId/cancel` (Cancel active query) | Free | |
| `DELETE /v2/auto/queries/:queryId` (Delete terminal query) | Free | |
| `GET /v2/auto/validate-symbol/:exchange/:symbol` | Free | |

> Reference USD values for Create: baseline `$0.045`, fast call `+$0.045`, expert call `+$0.162`. Use `/queries/validate` to preview exact cost before committing.

**x402 mode (`/x402/v2/auto/*`) — 70% discount, limited-time, pay-per-request in USDC on Base, Arbitrum, Polygon, or Avalanche:**

| Operation | Credits | USDC Cost |
|---|---|---|
| Builder Chat — fast | 5 | $0.045 |
| Builder Chat — expert | 18 | $0.162 |
| Query creation — baseline | 5 | $0.045 |
| Per fast LLM call | +5 | +$0.045 |
| Per expert LLM call | +18 | +$0.162 |
| Validate, poll, cancel, sessions, stream | Free | Free |

**x402 Auto example:**

```javascript
// Validate a query (x402 Auto)
const response = await x402Fetch(
  "https://api.elfa.ai/x402/v2/auto/queries/validate",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-elfa-agent-secret": process.env.ELFA_AGENT_SECRET,
    },
    body: JSON.stringify({
      query: {
        conditions: { AND: [{ source: "price", method: "current", args: { symbol: "BTC", exchange: "hyperliquid" }, operator: ">", value: 100000 }] },
        actions: [{ stepId: "step_1", type: "notify", params: { message: "BTC crossed 100k" } }],
        expiresIn: "24h"
      }
    }),
  });
```

#### Recommended call sequence (deterministic agent path)

**API key mode (`/v2/auto/*`):**

1. `POST /v2/auto/chat` — Ask Builder Chat to draft a query
2. `POST /v2/auto/queries/validate` — Validate EQL and preview cost
3. (Trade actions only) `GET /v2/auto/exchanges` — Confirm an active exchange connection
4. `POST /v2/auto/queries` — Create and activate
5. `GET /v2/auto/queries/{queryId}/stream` — Stream notifications (or poll)
6. `GET /v2/auto/queries/{queryId}/sessions` + `/sessions/{sessionId}` — Fetch LLM output (if using `llm` action)
7. (Optional cleanup) `POST /v2/auto/queries/{queryId}/cancel` — Cancel only while `active` (returns `409` if already terminal)
8. (Optional cleanup) `DELETE /v2/auto/queries/{queryId}` — Delete only after terminal (`triggered` / `expired` / `cancelled` / `failed`); rejects active queries with `409`

**x402 mode (`/x402/v2/auto/*`):**

1. `POST /x402/v2/auto/chat` — Ask Builder Chat to draft a query
2. `POST /x402/v2/auto/queries/validate` — Validate EQL and preview cost
3. `POST /x402/v2/auto/queries` — Create and activate
4. `GET /x402/v2/auto/queries/{queryId}/stream` — Stream notifications (or poll via POST)
5. `POST /x402/v2/auto/queries/{queryId}/sessions` + `/sessions/{sessionId}` — Fetch LLM output
6. (Optional cleanup) `POST /x402/v2/auto/queries/{queryId}/cancel` — Cancel only while `active`. (x402 has no terminal-delete endpoint.)

**Always validate before create.** Validate returns structured errors you can iterate on
without spending credits.

**Failure handling order** (apply in sequence):

1. Retry transient network errors with exponential backoff.
2. On `400` / `422` validation failure → repair query using [Validation Errors table](#validation-errors--next-action-table), re-validate.
3. On `401` / `403` auth failure → refresh credentials or verify Auto is enabled for the API key.
4. On `402` x402 payment failure → re-price and retry with valid payment payload.
5. On `410` (SSE stream closed) → re-open stream or fall back to polling.

**Common agent flows:**

_Poll-based LLM flow:_
```
POST /v2/auto/queries                               → create query with action.type = "llm"
GET  /v2/auto/queries/{queryId}                     → poll until execution with sessionId appears
GET  /v2/auto/queries/{queryId}/sessions/{sessionId} → fetch full analysis
```

_Webhook-based LLM flow:_
```
POST /v2/auto/queries                               → create with action.type = "llm" and params.objective
(wait for webhook)                                  → receive session reference / output
(optional) GET session fetch                        → /v2/auto/queries/{queryId}/sessions/{sessionId}
```

#### Builder Chat

Builder Chat (`POST /v2/auto/chat` or `POST /x402/v2/auto/chat`) uses AI to translate
natural language into EQL queries. Use `sessionId` for multi-turn conversations.

```json
{
  "message": "Alert me when BTC breaks 100k with RSI confirmation above 55",
  "speed": "expert",
  "sessionId": "optional-session-id"
}
```

Response (API-key mode):

```json
{
  "sessionId": "session-uuid",
  "response": "I can help with that... (markdown + EQL JSON code block)",
  "title": "BTC Breakout Alert",
  "reasoning": null,
  "planIds": []
}
```

The response message contains the AI's reply in Markdown. When it generates EQL, it will be
in a JSON code block — extract, validate via `/queries/validate`, then submit via `/queries`.

**Prompting tips for Builder Chat:**
- Include `title` and `description` (shown in notifications so recipients know what fired hours/days later)
- Specify symbols, timeframe, trigger behavior (one-time — the default — vs recurring), delivery target. For recurring on the **same condition**, ask for the `repeat` object (`cooldown` + `maxTriggers`); for a fixed schedule, use a `cron` condition
- For Signal triggers, give a **factual** match description (avoid vague phrasing like "bullish vibes")
- Append `"If anything is unsupported, return the closest supported query and list substitutions"` to handle edge cases gracefully
- Prefer `expiresIn` of `24h`–`3d` for fresh signals
- Persist `sessionId` and reuse it for follow-up prompts so the model keeps context across turns

**High-impact prompt pack** — drop these into `POST /v2/auto/chat` as the `message` field:

_1) Complex TA breakout with direction filter:_

```
Build an Auto query:
- title + description: short human-readable summary and 1-2 sentence thesis
- symbols: BTC, ETH, SOL
- timeframe: 5m
- trigger when price breaks previous 1h range high or low
- confirm direction with RSI(14): >55 for upside, <45 for downside
- actions: telegram alert + webhook to https://your-runner.example/auto/events
- one-time trigger, expires in 48h
If anything is unsupported, return the closest supported query and list substitutions.
```

_2) CEX + DEX monitoring pack:_

```
Build an Auto query pack for supported CEX + DEX symbols:
- title + description per query: short summary and thesis sentence
- watchlist: WBTC, ETH, SOL, HYPE
- trigger when 15m volume surge aligns with price momentum
- action: webhook to https://your-runner.example/auto/events
- include symbol and trigger summary in payload
- expires in 24h
If any symbol/source is unsupported, skip it and report skipped items.
```

_3) News + X sentiment context on trigger:_

```
Build an Auto query:
- title + description: short summary and the thesis behind watching this
- monitor BTC and ETH for abnormal 1h move + volume confirmation
- on trigger run llm action that adds:
  - latest market news context
  - X sentiment summary
  - risk note
- also send telegram alert with a short summary
- expires in 24h
```

_4) Prediction-market thesis watcher (Kalshi):_

```
Build an Auto query:
- title + description: name the market thesis and the move you're watching for
- source: kalshi
- ticker: <a confirmed-open Kalshi market ticker, e.g. KXBTC-26APR0803-T77799.99>
- trigger when the YES implied probability crosses above 0.6
- action: llm to produce a catalyst hypothesis + invalidation level
- deliver to webhook: https://your-runner.example/auto/events
- include decision priority: high/medium/low
- expires in 2d
If the ticker is not open or anything is unsupported, return the closest supported query and list substitutions.
```

_5) Portfolio risk guardrail:_

```
Build an Auto query:
- title + description: portfolio guardrail label and the risk scenario it covers
- watch my portfolio symbols: BTC, ETH, SOL, HYPE
- trigger on downside acceleration and momentum weakness
- action: telegram alert with severity and suggested next check
- recurring checks, expires in 3d
```

_6) Agent handoff with strict execution contract:_

```
Build an Auto query:
- title + description: breakout playbook name and the execution intent
- trigger on breakout + trend-confirmation conditions
- action: webhook to https://your-runner.example/auto/events
- include fields: eventId, symbol, triggerReason, priority, queryId
- objective: downstream agent decides next action under policy constraints
- expires in 24h
```

_7) Signal — account-anchored X/Twitter Post watcher:_

```
Build an Auto query:
- title + description: short summary anchored to the account + intent
- use Signal category:
  - condition source: tweet
  - username: cz_binance (no leading @)
  - match description: "Binance Alpha is listing a new token"
  - minConfidence: 80
- action: notify (or telegram_bot) with a concise message
- expires in 24h
If unsupported, return closest supported query and list substitutions.
```

_8) Signal — event-first catalyst watcher:_

```
Build an Auto query:
- title + description: catalyst name and why it matters now
- use Signal category:
  - condition source: news
  - match description: "SEC approves a spot ETH ETF"
  - minConfidence: 80
- action: webhook to https://your-runner.example/auto/events
- include queryId, eventId, and short trigger reason in payload
- expires in 24h
```

#### Query model (EQL)

A query contains `conditions`, `actions`, and `expiresIn` (plus an optional `repeat`
sibling — by default a plan is one-shot; see **Repeat** below):

```json
{
  "title": "BTC RSI oversold on 1h",
  "description": "Mean-reversion entry: if BTC 1h RSI dips under 30, consider scaling in.",
  "conditions": {
    "AND": [
      {
        "source": "ta",
        "method": "rsi",
        "args": { "symbol": "BTC", "timeframe": "1h", "period": 14, "exchange": "hyperliquid" },
        "operator": "<",
        "value": 30
      }
    ]
  },
  "actions": [
    { "stepId": "step_1", "type": "webhook", "params": { "url": "https://your-endpoint.example/events" } }
  ],
  "expiresIn": "24h"
}
```

**Condition rules:**
- Root group must be `AND` or `OR`
- Nest groups up to depth 3, max 10 leaf conditions
- Multi-symbol: a single query can require BTC AND ETH AND SOL conditions jointly

**Allowed `expiresIn` values:** `1h`, `2h`, `4h`, `8h`, `12h`, `24h`, `48h` (2d), `72h` (3d),
`120h` (5d), `168h` (7d), `240h` (10d), `336h` (14d), `504h` (21d), `720h` (30d — hard max).
**Prefer `24h`–`72h`** — signals decay and short windows force re-evaluation. Only reach for
`240h`–`720h` on slow structural theses (token unlocks, options expiries, monthly
copy-trading), never on short-timeframe TA/scalps.

**Plan limits (active plans per account):** an account can only hold so many **active** plans
at once, by API key tier — Free `2`, Chill `10`, Grow `50`, PAYG/Enterprise unlimited. A hard
ceiling of **100 active plans** applies regardless of tier; exceeding either cap returns
`409`. Only *active* plans count — expired/cancelled/terminal plans free capacity, so
cancelling stale plans (or choosing a shorter `expiresIn`) is the fastest way to make room.

**Repeat (`repeat`) — recurring plans on their own conditions:**

By default a plan is **one-shot**: it fires once and moves to a terminal state. The optional
top-level `repeat` object (a sibling of `expiresIn`) keeps a plan active and makes it re-fire
on **its own** conditions — the right tool for "notify me *every time* BTC dips below 60k"
without a fixed cron cadence.

```json
{
  "conditions": { "AND": ["..."] },
  "actions": ["..."],
  "expiresIn": "7d",
  "repeat": { "cooldown": "1h", "maxTriggers": 10 }
}
```

Both fields are **mandatory** when `repeat` is present:

| Field | Type | Meaning |
|---|---|---|
| `cooldown` | string | Minimum time between fires. `"0"` disables the rate limit. |
| `maxTriggers` | number | Lifetime cap on fires (`1`–`1000`); reaching it makes the plan terminal. |

- **`cooldown` allowed values** (its own set — sub-hour is permitted, unlike the cron/llm 1h minimum): `1m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `8h`, `12h`, `24h`, `1d`, `7d`, plus `"0"`. Use `"0"` for "fire on every distinct event" (e.g. every matching tweet).
- **`maxTriggers`** counts how many times the plan **fires** over its lifetime (distinct from the number of action steps). Sanity-check `cooldown × maxTriggers` against `expiresIn` — if there isn't enough runway, the plan expires before reaching the cap. A longer `expiresIn` buys patience through quiet periods; it does **not** raise the fire cap.
- **Single reset rule.** A `repeat` plan re-fires only once its triggering signal has cleared. **Level** conditions (`price` / `ta` / `llm`-boolean) disarm on fire and re-arm when the whole condition tree next evaluates false; **event** conditions (`tweet.semantic` / `news.semantic`) consume the matched mention and re-fire on the **next distinct** mention.

> **`repeat` on trade actions places a NEW order every fire.** `repeat` composes with **every**
> action type, including `market_order` / `limit_order`. On an order action, **each fire opens a
> new position** — Auto does not net, reconcile, or cancel earlier fires. Three fires = three
> positions. So `cooldown` and `maxTriggers` are your **position-count controls**, not just an
> alert rate-limit. `positionSizePercent` recomputes against the then-current account value
> (it compounds), and `tp` / `sl` / `leverage` attach per order. **Never use `cooldown: "0"`
> on order actions** — a redelivered trigger could place a second order; any non-zero cooldown
> closes that window. A failed fire notifies you (`order_failed`), still consumes one
> `maxTriggers`, and leaves the plan live.
>
> **Still rejected:** `repeat` combined with a recurring cron condition (`cron.every` /
> `cron.schedule`) — both provide recurrence, so combining them fails validation as
> `EQL_INVALID_REPEAT`. For a fixed-cadence recurring plan, use the cron condition on its own;
> for a condition-driven recurring plan, use `repeat`.

**Avoiding over-triggering:** the main risk is a condition that keeps flipping true — a
metric flapping around its threshold, or a chatty account. `cooldown` is your rate-limit
floor (never use `"0"` on level/metric conditions); `maxTriggers` is your hard circuit
breaker (set it conservatively so a runaway condition self-limits). A **level** condition
like `price < 60000` fires on *every* re-crossing, so prefer transition operators
(`crosses_below` / `crosses_above` over `<` / `>`), give the threshold room from the current
value, match `cooldown` to the signal's timeframe, and start conservative then loosen.

Recommended starting points:

| Condition type | `cooldown` | `maxTriggers` | Notes |
|---|---|---|---|
| Price / TA level (`price`, `ta`) | `1h`–`4h` (≥ your timeframe) | `3`–`10` | Prefer `crosses_*` operators; avoid `"0"` here. |
| LLM predicate (`llm.athena_condition`) | `≥ period` (min `1h`) | `3`–`5` | The LLM already re-checks on `period` — don't re-alert faster than it re-evaluates. |
| Event — single / quiet account (`tweet`) | `0`–`15m` | `10`–`20` | Each distinct post is a discrete event; `"0"` is fine unless the account is chatty. |
| Event — noisy account / broad `news` | `15m`–`1h` | `10`–`20` | A small cooldown collapses a burst of mentions into one alert. |
| Liquidation cascade (`liquidation`) | `1h`+ | `5`–`10` | Windows decay to zero, so the plan re-arms per cascade; the cooldown stops one long cascade re-alerting. |
| **Trade / order action** (`market_order`, `limit_order`) | non-zero, `1h`+ | `2`–`5` | These are **positions, not alerts** — `maxTriggers` is the number of orders the plan may place. Never `"0"`. |

**Allowed action types:** `webhook`, `notify`, `telegram_bot`, `llm`, `market_order`, `limit_order`. The `actions` array is **exactly one step** per query — run standalone LLM work with `params.objective`; chain follow-up work via `llm` action with `params.callback.action`, or have your runner fan out from the trigger event.

**Action params shape (key fields):**

| `type` | Required `params` | Optional `params` |
|---|---|---|
| `notify` | `message` (1–1000 chars) | — |
| `webhook` | `url` (https only, allowlisted host) | `allNotifications` (default `false`) |
| `telegram_bot` | `botToken`, `chatId` | `allNotifications` (default `false`) |
| `market_order` / `limit_order` | `exchange` (`hyperliquid` / `gmx`), `symbol`, `side` (`buy` / `sell`), and exactly one of `size` / `amount` / `positionSizePercent` (+ `price` for limit) | `reduceOnly`, `leverage`, `marginType` (`cross` / `isolated`), `tp`, `sl` |
| `llm` | `objective` for standalone LLM work, or `action` + `callback.action` for chained follow-up | `action` ∈ `chat` / `summary` / `macro` / `accountAnalysis` / `tokenDiscovery` / `tokenAnalysis`; `speed` (`fast` / `expert`), per-action extras |

`telegram_bot` does **not** take a `message` field — the message body is auto-composed from the query `title` + `description` + trigger context. Use `notify` (in-app push) when you want to specify the message text yourself. `allNotifications: true` on `webhook` / `telegram_bot` opts the destination into lifecycle notifications (failed/expired/run-failed) in addition to the trigger fire.

#### Triggers — condition sources

**Market-data venue (`exchange`) — REQUIRED on every `price` and `ta` condition:**

Every `price` and `ta` condition must include an `exchange` arg that selects which venue's
market data backs the condition. Allowed values: `hyperliquid`, `gmx` (exact lowercase
enum). This arg **only affects the data source** of the condition — it is independent of
where `market_order` / `limit_order` actions execute. A `price`/`ta` condition without
`exchange` fails validation.

```json
{ "source": "price", "method": "current", "args": { "symbol": "BTC", "exchange": "hyperliquid" }, "operator": ">", "value": 100000 }
```

**Price source (`price`):**

| Method | Args | Returns | Description |
|---|---|---|---|
| `current` | `symbol`, `exchange` | number | Current price |
| `change` | `symbol`, `exchange`, `period` | number | % change over period |
| `high` | `symbol`, `exchange`, `period` | number | High in period |
| `low` | `symbol`, `exchange`, `period` | number | Low in period |
| `volume` | `symbol`, `exchange`, `period` | number | Volume (USD) over period |

**TA source (`ta`) — technical indicators:** every method also requires `symbol`, `timeframe`, **and `exchange`**.

| Method | Required args | Optional args | Returns |
|---|---|---|---|
| `rsi` | `symbol`, `timeframe`, `exchange` | `period` (default 14) | RSI (0-100) |
| `macd_value` | `symbol`, `timeframe`, `exchange` | — | MACD line |
| `macd_signal` | `symbol`, `timeframe`, `exchange` | — | MACD signal line |
| `macd_histogram` | `symbol`, `timeframe`, `exchange` | — | MACD histogram |
| `bbands_upper` | `symbol`, `timeframe`, `exchange` | `period` (default 20) | Upper Bollinger Band |
| `bbands_middle` | `symbol`, `timeframe`, `exchange` | `period` (default 20) | Middle Bollinger Band |
| `bbands_lower` | `symbol`, `timeframe`, `exchange` | `period` (default 20) | Lower Bollinger Band |
| `ema` | `symbol`, `timeframe`, `exchange`, `period` | — | Exponential MA |
| `sma` | `symbol`, `timeframe`, `exchange`, `period` | — | Simple MA |
| `atr` | `symbol`, `timeframe`, `exchange` | `period` (default 14) | Average True Range |
| `stoch_k` | `symbol`, `timeframe`, `exchange` | — | Stochastic %K |
| `stoch_d` | `symbol`, `timeframe`, `exchange` | — | Stochastic %D |
| `cci` | `symbol`, `timeframe`, `exchange` | `period` (default 20) | CCI |
| `willr` | `symbol`, `timeframe`, `exchange` | `period` (default 14) | Williams %R |

**TA critical rules:**
- Every `ta` (and `price`) condition **requires `exchange`** (`hyperliquid` or `gmx`)
- `ema` and `sma` **require** `period` — it is NOT optional
- `rsi`, `bbands_*`, `atr`, `cci`, and `willr` accept optional `period` with documented defaults above
- `period` must be a JSON number (`14`), not a string (`"14"`)
- Use `period` not `length` — `length` is not a recognized alias
- `timeframe` values: `1m`, `5m`, `15m`, `30m`, `1h`, `2h`, `4h`, `8h`, `12h`, `1d`

**Cron source (`cron`):**

| Method | Args | Description |
|---|---|---|
| `once` | `period` | True on first due evaluation at/after creation + period |
| `onceRemainTrue` | `period` | True on first due evaluation and stays true |
| `every` | `period` | True at each period interval |
| `schedule` | `expression`, `timezone?` | True whenever the 5-field cron `expression` matches in `timezone` |

`once`, `onceRemainTrue`, and `every` are **interval** methods measured from query creation.
`schedule` is a **calendar/wall-clock** method:

- `expression` is a classic **5-field** cron string (`minute hour day-of-month month day-of-week`) — e.g. `0 9 * * 1-5` (weekdays at 09:00).
- `timezone` is optional and defaults to `UTC`. When set it must be a valid **IANA** name (e.g. `America/New_York`, `Asia/Singapore`) so daylight-saving transitions are handled correctly. Fixed-offset strings like `+02:00` are **not** accepted.
- `schedule` enforces the same **1h-minimum cadence** as the other cron methods: the minute field must be a single fixed value (`0`–`59`). Wildcards, steps, lists, or ranges in the minute field are rejected.
  - Allowed: `7 * * * *` (hourly at minute 7), `0 9 * * 1-5` (weekdays 09:00), `30 8 * * *` (daily 08:30).
  - Not allowed: `* * * * *` (every minute), `*/15 * * * *` (every 15 min), `0,30 * * * *` (twice per hour).
- `schedule` takes **no** `period` arg.

> **Builder Chat support pending:** `cron.schedule` is available on the direct EQL/API path
> (Validate / Create). Builder Chat does not yet reliably generate `cron.schedule` — author
> calendar schedules directly and confirm with `/v2/auto/queries/validate`.

**LLM source (`llm`):**

| Method | Args | Description |
|---|---|---|
| `athena_condition` | `query`, `period`, `speed?` | LLM-evaluated condition (natural language) |

**Signal source — X/Twitter Post (`tweet`):**

In the Builder Chat catalog this is the `Signal` category, **X/Twitter Post**.

| Method | Required args | Returns | Description |
|---|---|---|---|
| `semantic` | `username`, `text`, `minConfidence` | boolean | Matches posts from a specific X/Twitter account when semantic confidence meets threshold |

Rules:
- `username` must be passed **without** `@` (e.g. `cz_binance`, not `@cz_binance`).
- `username` must resolve to an active monitored account at create-time, otherwise validation/create fails.
- `minConfidence` must be a JSON integer between `0` and `100`; use `80` when the user gives no threshold.
- `method`, `operator`, and `value` are auto-filled defaults (`semantic`, `==`, `true`) — do **not** include them in the condition JSON.

```json
{
  "source": "tweet",
  "args": {
    "username": "cz_binance",
    "text": "Binance Alpha is listing a new token",
    "minConfidence": 80
  }
}
```

**Signal source — Event (`news`):**

In the Builder Chat catalog this is the `Signal` category, **Event**.

| Method | Required args | Returns | Description |
|---|---|---|---|
| `semantic` | `text`, `minConfidence` | boolean | Matches event-style mentions from news-tagged sources when semantic confidence meets threshold |

Rules:
- `minConfidence` must be a JSON integer between `0` and `100`; use `80` when the user gives no threshold.
- `method`, `operator`, and `value` are auto-filled defaults — do **not** include them.
- Use `news` for world events not anchored to a specific account; use `tweet` when the trigger is anchored to a specific handle.

```json
{
  "source": "news",
  "args": {
    "text": "SEC approves a spot ETH ETF",
    "minConfidence": 80
  }
}
```

**Signal selection policy** (which source to pick):

- Account-anchored intent (handle in the prompt) → `tweet`.
- World-event intent (no specific account) → `news`.
- Prefer `tweet`/`news` over `llm` when the trigger is plausibly expressed as a post or event.
- Fall back to `llm` (`athena_condition`) only for predicates that are not naturally a post/event match.

**Signal `args.text` authoring rubric** — match quality is dominated by `text` quality. Write a short factual claim, not a monitoring command.

| Weak phrasing (bad) | Actionable phrasing (good) |
|---|---|
| `Bearish vibes` | `Opens a short position on oil` |
| `Something bullish` | `Announces a new stake in TSLA` |
| `Bullish on a coin` | `Posts that they're bullish on $HYPE and $SOL` |
| `Market crash` | `Major DeFi protocol suffers a $200M exploit` |
| `War conflict` | `US imposes new sanctions on Russia` |
| `Big news` | `SEC approves a spot ETH ETF` |

Additional constraints:
- Keep `text` atomic — one event/theme per condition.
- For `tweet`, do not restate account identity in `text` — `username` already scopes that.
- Split `A or B` intents into multiple Signal conditions joined by `OR`; split `A and B` into multiple conditions joined by `AND`.
- Prefer separate queries for event-driven Signal intents (`tweet`/`news`) and recurring schedule intents (`cron.every`) for clearer runtime semantics.

**`minConfidence` tuning:** default `80`; raise to `85`–`90` for fewer false positives; lower to `70`–`75` if you need higher recall.

**Scheduling period (cron / llm):** for `cron` **interval** methods (`once`,
`onceRemainTrue`, `every`) and `llm` sources, `period` is a scheduling interval with a
minimum of `1h`. Allowed: `1h`, `2h`, `4h`, `8h`, `12h`, `24h`, `1d`, `7d`. `cron.schedule`
does **not** take a `period` — it is driven by its 5-field cron `expression` and follows the
same 1h-minimum cadence (at most one fire per hour).

**Signal sources are event-driven**, not schedule-driven — they evaluate when relevant mention events arrive, not on a polling interval. They can still be combined with other condition types via `AND`/`OR`.

**Prediction Markets source (`kalshi`):**

Trigger on Kalshi prediction-market activity — live trade prints and market lifecycle. Each
`kalshi` condition takes exactly one arg, `ticker`: a full open Kalshi market ticker
(e.g. `KXBTC-26APR0803-T77799.99` = series + event + strike). Prefer `kalshi` over `llm` when
the trigger is a supported Kalshi method, and over `price`/`ta` when you care about an event's
*implied probability* rather than an asset's spot price.

_Trade-backed methods_ — evaluate on the latest executed trade print:

| Method | Returns | Description |
|---|---|---|
| `yes_price` | number `0`–`1` | Executed YES price = live implied probability of YES |
| `no_price` | number `0`–`1` | Executed NO price (implied probability of NO) |
| `trade_size` | number ≥ 0 | Contracts on that print |
| `taker_outcome_side` | enum `yes` / `no` | Which outcome the aggressor (taker) positioned for |
| `taker_book_side` | enum `bid` / `ask` | `bid` = YES-side pressure, `ask` = NO-side pressure |
| `is_block_trade` | boolean | `true` for large off-book negotiated block trades |

_Market-backed methods_ — evaluate on market lifecycle updates:

| Method | Returns | Description |
|---|---|---|
| `status` | enum `active` / `closed` / `determined` / `settled` / `finalized` | Lifecycle state (`active` = only tradeable state) |
| `result` | enum `yes` / `no` | Settlement outcome (empty until the market resolves) |
| `settlement_value` | number ≥ 0 | Final settlement value in dollars (populated on settlement) |

**Operators by method** (restricted per method):

| Method(s) | Allowed operators |
|---|---|
| `yes_price`, `no_price` | `>` `<` `>=` `<=` `==` `!=` `crosses_above` `crosses_below` |
| `trade_size`, `settlement_value` | `>` `<` `>=` `<=` `==` `!=` |
| `taker_outcome_side`, `taker_book_side`, `status`, `result`, `is_block_trade` | `==` `!=` |

Only the price methods (`yes_price` / `no_price`) support the transition operators
`crosses_above` / `crosses_below`; enum and boolean methods are equality-only. `value` must be
a **literal** matching the method's type (no dynamic field-vs-field values), and
`is_block_trade` takes a JSON boolean `true` / `false` (not the strings `"true"` / `"false"`).

**Open markets only:** at create/validate time `args.ticker` is checked against the catalog of
**currently-open** Kalshi markets. A `closed` / `determined` / `settled` / `finalized` ticker
is rejected with `EQL_INVALID_ARG_VALUE` ("was not found or is not open"). Resolve a real,
currently-open ticker first — never invent or guess tickers. Lifecycle conditions are still
useful on a market you already watch: a plan created while a market is `active` can fire as it
later moves to `settled` (`status`) or resolves (`result` / `settlement_value`) within its
`expiresIn` window.

```json
{
  "source": "kalshi",
  "method": "yes_price",
  "args": { "ticker": "KXBTC-26APR0803-T77799.99" },
  "operator": "crosses_below",
  "value": 0.4
}
```

Full method tables, value enums, and example automations:
[Prediction Markets → Kalshi](https://docs.elfa.ai/auto/prediction-markets#kalshi).

**Prediction Markets source (`polymarket`):**

Trigger on live Polymarket outcome-token activity: last traded price, best bid/ask, and the
size and aggressor side of the most recent trade. Unlike Kalshi, Polymarket exposes **price
and trade methods only** — there are **no** market-lifecycle (`status` / `result`) methods.

**Ticker = outcome-token `asset_id`.** For Polymarket, `args.ticker` is the **outcome token
`asset_id`** — the long numeric id of a single outcome (e.g. the YES token), **not** the
top-level Polymarket market id (which is shared by both sides of a binary market). At create
time the token is validated against Polymarket's live markets; an unknown or inactive token
is rejected ("was not found or is not active"). Resolve a real, currently-active
outcome-token id first — never invent or guess ids.

Each method takes exactly one arg, `ticker`:

| Method | Returns | Description |
|---|---|---|
| `price` | number in `[0, 1]` | Last traded probability / price for the outcome token |
| `bid` | number in `[0, 1]` | Best bid for the outcome token (when present on the event) |
| `ask` | number in `[0, 1]` | Best ask for the outcome token (when present on the event) |
| `size` | number ≥ 0 | Size of the last-trade update (when present on the event) |
| `side` | enum `"BUY"` / `"SELL"` | Aggressor side of the last trade, in uppercase |

The feed mixes several event subtypes (`price_change`, `best_bid_ask`, `last_trade_price`,
`book`), and **not every field updates on every event** — `best_bid_ask` updates `bid`/`ask`
only, while `last_trade_price` updates `price`/`size`/`side` only. Design a condition around
the specific field you need rather than assuming all fields move together.

**Operators by method** (restricted per method):

| Method(s) | Allowed operators |
|---|---|
| `price`, `bid`, `ask` | `>` `<` `>=` `<=` `==` `!=` `crosses_above` `crosses_below` |
| `size` | `>` `<` `>=` `<=` `==` `!=` |
| `side` | `==` `!=` |

`value` must be a **literal** matching the method's type (`0`–`1` for `price`/`bid`/`ask`,
≥ 0 for `size`, uppercase `"BUY"` / `"SELL"` for `side`). Polymarket conditions **do not
support dynamic (field-vs-field) values** — dynamic Polymarket targets are rejected at
validation.

```json
{
  "source": "polymarket",
  "method": "price",
  "args": { "ticker": "115556263888245616435851357148058235707004733438163639091106356867234218207169" },
  "operator": "crosses_below",
  "value": 0.4
}
```

Standard EQL limits apply to both prediction-market sources: combinable with other sources
inside `AND`/`OR` groups, up to depth 3 and 10 leaf conditions. Full method tables and
example automations:
[Prediction Markets → Polymarket](https://docs.elfa.ai/auto/prediction-markets#polymarket).

**Market-structure source (`funding`) — perp funding rate:**

Trigger on a perp's funding rate — an overheated long bias, a flip to negative, or a
cross-venue divergence. Funding and liquidation flow often lead the spot price reaction.

**Ticker = composite `SYMBOL:EXCHANGE`** (not `symbol` + `exchange` args). `SYMBOL` is the
base asset (`BTC`, not `BTCUSDT`); the venue rides in the ticker. Venues: `binance`,
`hyperliquid`. Examples: `BTC:BINANCE`, `ETH:HYPERLIQUID`.

| Method | Args | Returns | Operators | Description |
|---|---|---|---|---|
| `annualized_rate` | `ticker` | number | all 8 | **Canonical.** Funding as annualized percent (APR): `32.85` = 32.85% APR. Positive = longs pay shorts. |
| `interval_rate` | `ticker` | number | all 8 | Percent per settlement interval. |
| `interval_hours` | `ticker` | number | level only | Settlement interval in hours: `8` (Binance) or `1` (Hyperliquid). Venue metadata. |
| `exchange` | `ticker` | enum | `==` / `!=` | The venue: `"binance"` or `"hyperliquid"`. |

- **Prefer `annualized_rate`** — Binance settles every 8h and Hyperliquid every 1h, so the
  same `interval_rate` threshold means different things per venue; annualizing removes that
  trap. "Funding flips negative" is exactly `annualized_rate crosses_below 0`.
- "level only" = `>` `<` `>=` `<=` `==` `!=` (no `crosses_*`).
- HIP-3 dex-prefixed symbols (`xyz:TSLA`) are **rejected** here (`EQL_INVALID_ARG_VALUE`,
  `details.hip3: true`) — the funding feed never publishes keys for them.

```json
{ "source": "funding", "method": "annualized_rate", "args": { "ticker": "BTC:BINANCE" }, "operator": "crosses_below", "value": 0 }
```

**Market-structure source (`liquidation`) — liquidation flow:**

Trigger on liquidation flow in a trailing window — a cascade crossing a USD threshold, a
one-sided flush, or liquidations as a share of open interest. Same composite
`SYMBOL:EXCHANGE` ticker as `funding`. Venues: `binance`, `bybit`, `hyperliquid`.

| Method | Args | Returns | Operators | Description |
|---|---|---|---|---|
| `total_usd_1m` / `total_usd_5m` / `total_usd_1h` | `ticker` | number | all 8 | Total USD liquidated in the trailing window. |
| `long_usd_1m` / `long_usd_5m` / `long_usd_1h` | `ticker` | number | all 8 | Longs liquidated (forced selling). |
| `short_usd_1m` / `short_usd_5m` / `short_usd_1h` | `ticker` | number | all 8 | Shorts liquidated (forced buying). |
| `largest_order_usd_1h` | `ticker` | number | all 8 | Single biggest liquidation order in the trailing hour, USD. |
| `count_1h` | `ticker` | number | level only | Number of liquidation orders in the trailing hour. |
| `total_pct_oi_1m` / `total_pct_oi_5m` / `total_pct_oi_1h` | `ticker` | number | all 8 | Window total as a **percent of open interest** (compares across symbols). |
| `exchange` | `ticker` | enum | `==` / `!=` | The venue: `"binance"` / `"bybit"` / `"hyperliquid"`. |

- **Feed quality differs by venue.** Binance is **sampled** (≤1 liquidation/symbol/second) so
  its values are a **lower bound** and undercount most during the cascades you care about;
  Bybit and Hyperliquid are **complete** (exact totals). Set a lower threshold on Binance for
  the same real-world event.
- **Windows decay to zero** once a cascade subsides, which re-arms the condition — so a
  `repeat` plan fires **once per cascade**, not once ever.
- `total_pct_oi_*` magnitudes are **small**: ~0.1%/hr is already heavy for a major; start
  around `0.5`–`1` (percent), not raw fractions. HIP-3 symbols are **rejected** here too.

```json
{ "source": "liquidation", "method": "total_usd_5m", "args": { "ticker": "ETH:BYBIT" }, "operator": "crosses_above", "value": 500000 }
```

Full method tables, feed-quality table, and examples:
[Funding and Liquidations](https://docs.elfa.ai/auto/funding-and-liquidations).

**Market-sentiment source (`fear_greed`) — Crypto Fear & Greed Index:**

Trigger on the market-wide Crypto Fear & Greed Index. This is a **keyless** source — one
global reading, no per-market identity — so its methods take **no ticker**. Pass
`args: {}`.

| Method | Args | Returns | Operators | Description |
|---|---|---|---|---|
| `value` | _(none)_ | number | all 8 | Index score, integer `0`–`100` (0 = extreme fear, 100 = extreme greed). |
| `classification` | _(none)_ | enum | `==` / `!=` | Bucket label (see below). |

- `classification` value ∈ `"Extreme fear"` (`0–19`), `"Fear"` (`20–39`), `"Neutral"`
  (`40–59`), `"Greed"` (`60–79`), `"Extreme greed"` (`80–100`). Bands map to fixed `value`
  ranges — **prefer `value`** for a precise threshold.
- Updates ~every 15 min. A `crosses_*` leaf needs a prior reading, so it can only fire on the
  **second** reading after activation. No dynamic values.

```json
{ "source": "fear_greed", "method": "value", "args": {}, "operator": "crosses_below", "value": 20 }
```

**Supported operators:** `>`, `<`, `>=`, `<=`, `==`, `!=`, `crosses_above`, `crosses_below`

**Dynamic comparisons:** `value` can reference another live data source instead of a literal:

```json
{
  "source": "price",
  "method": "current",
  "args": { "symbol": "ETH", "exchange": "hyperliquid" },
  "operator": "crosses_above",
  "value": {
    "source": "ta",
    "method": "bbands_upper",
    "args": { "symbol": "ETH", "timeframe": "4h", "exchange": "hyperliquid" }
  }
}
```

#### Copy-paste query templates

**1) Breakout alert (webhook):**

```json
{
  "title": "BTC breakout above 100k",
  "description": "Notify runner when BTC spot trades above the 100k level.",
  "conditions": { "AND": [{ "source": "price", "method": "current", "args": { "symbol": "BTC", "exchange": "hyperliquid" }, "operator": ">", "value": 100000 }] },
  "actions": [{ "stepId": "step_1", "type": "webhook", "params": { "url": "https://your-endpoint.example/events" } }],
  "expiresIn": "24h"
}
```

**2) Downside guardrail (telegram_bot):**

```json
{
  "title": "ETH downside guardrail (< 2500)",
  "description": "Risk-off alert: flag if ETH breaks below 2500. The notification body is auto-composed from title + description + trigger context.",
  "conditions": { "AND": [{ "source": "price", "method": "current", "args": { "symbol": "ETH", "exchange": "hyperliquid" }, "operator": "<", "value": 2500 }] },
  "actions": [{ "stepId": "step_1", "type": "telegram_bot", "params": { "botToken": "<TELEGRAM_BOT_TOKEN>", "chatId": "<TELEGRAM_CHAT_ID>" } }],
  "expiresIn": "24h"
}
```

**3) Triggered LLM analysis:**

```json
{
  "title": "BTC > 100k — LLM review",
  "description": "On BTC breakout, run LLM to decide next trading action.",
  "conditions": { "AND": [{ "source": "price", "method": "current", "args": { "symbol": "BTC", "exchange": "hyperliquid" }, "operator": ">", "value": 100000 }] },
  "actions": [{
    "stepId": "step_1",
    "type": "llm",
    "params": { "objective": "Analyze trigger context and return next action" }
  }],
  "expiresIn": "24h"
}
```

**4) Multi-symbol confirmation:**

```json
{
  "title": "BTC + ETH joint breakout",
  "description": "Confirm majors moving together before acting.",
  "conditions": {
    "AND": [
      { "source": "price", "method": "current", "args": { "symbol": "BTC", "exchange": "hyperliquid" }, "operator": ">", "value": 100000 },
      { "source": "price", "method": "current", "args": { "symbol": "ETH", "exchange": "hyperliquid" }, "operator": ">", "value": 3500 }
    ]
  },
  "actions": [{ "stepId": "step_1", "type": "notify", "params": { "message": "BTC and ETH confirmation fired" } }],
  "expiresIn": "24h"
}
```

**5) Dynamic comparison (price vs Bollinger Band):**

```json
{
  "title": "ETH breakout above 4h upper BBand",
  "description": "Dynamic: fire when ETH price crosses above its own 4h upper Bollinger Band.",
  "conditions": {
    "AND": [{
      "source": "price", "method": "current", "args": { "symbol": "ETH", "exchange": "hyperliquid" },
      "operator": "crosses_above",
      "value": { "source": "ta", "method": "bbands_upper", "args": { "symbol": "ETH", "timeframe": "4h", "exchange": "hyperliquid" } }
    }]
  },
  "actions": [{ "stepId": "step_1", "type": "webhook", "params": { "url": "https://your-endpoint.example/events" } }],
  "expiresIn": "2d"
}
```

**6) Scheduled cron check:**

```json
{
  "title": "Every 4h: portfolio sweep",
  "description": "Recurring LLM pass every 4h.",
  "conditions": { "AND": [{ "source": "cron", "method": "every", "args": { "period": "4h" }, "operator": "==", "value": true }] },
  "actions": [{
    "stepId": "step_1",
    "type": "llm",
    "params": { "objective": "Summarize BTC/ETH/SOL context and flag any risk shifts" }
  }],
  "expiresIn": "3d"
}
```

**7) LLM-evaluated narrative condition:**

```json
{
  "title": "AI narrative shift watcher",
  "description": "Fire when dominant AI-token narrative shifts based on news + X sentiment.",
  "conditions": {
    "AND": [{
      "source": "llm", "method": "athena_condition",
      "args": { "query": "Has the dominant narrative around AI-sector tokens shifted materially in the last 6 hours?", "period": "1h" },
      "operator": "==", "value": true
    }]
  },
  "actions": [{ "stepId": "step_1", "type": "telegram_bot", "params": { "botToken": "<TELEGRAM_BOT_TOKEN>", "chatId": "<TELEGRAM_CHAT_ID>" } }],
  "expiresIn": "2d"
}
```

**8) Signal — X/Twitter Post (account-anchored):**

```json
{
  "title": "Binance Alpha listing post watcher",
  "description": "Fire when cz_binance posts that Binance Alpha is listing a new token so the runner can review follow-through.",
  "conditions": {
    "AND": [{
      "source": "tweet",
      "args": {
        "username": "cz_binance",
        "text": "Binance Alpha is listing a new token",
        "minConfidence": 80
      }
    }]
  },
  "actions": [{ "stepId": "step_1", "type": "webhook", "params": { "url": "https://your-runner.example/auto/events" } }],
  "expiresIn": "24h"
}
```

**9) Signal — Event (news-driven catalyst):**

```json
{
  "title": "ETH ETF approval event watcher",
  "description": "Fire when event feeds indicate a spot ETH ETF approval so I can kick off a post-event playbook.",
  "conditions": {
    "AND": [{
      "source": "news",
      "args": {
        "text": "SEC approves a spot ETH ETF",
        "minConfidence": 80
      }
    }]
  },
  "actions": [{ "stepId": "step_1", "type": "notify", "params": { "message": "Event trigger fired: spot ETH ETF approval signal" } }],
  "expiresIn": "24h"
}
```

**10) Prediction Market — Kalshi (YES probability crossing):**

```json
{
  "title": "Kalshi YES crosses 60%",
  "description": "Fire when the market's implied YES probability crosses up through 60%, signalling the market now expects this outcome.",
  "conditions": { "AND": [{ "source": "kalshi", "method": "yes_price", "args": { "ticker": "KXBTC-26APR0803-T77799.99" }, "operator": "crosses_above", "value": 0.6 }] },
  "actions": [{ "stepId": "step_1", "type": "webhook", "params": { "url": "https://your-runner.example/auto/events" } }],
  "expiresIn": "48h"
}
```

**11) Prediction Market — Kalshi (settlement recap via LLM):**

```json
{
  "title": "Kalshi market resolved YES — recap",
  "description": "When the market settles with a YES result, generate a concise recap of what happened and why.",
  "conditions": { "AND": [{ "source": "kalshi", "method": "result", "args": { "ticker": "KXBTC-26APR0803-T77799.99" }, "operator": "==", "value": "yes" }] },
  "actions": [{ "stepId": "step_1", "type": "llm", "params": { "objective": "This Kalshi market just resolved YES. Write a concise recap explaining what resolved and what to watch next." } }],
  "expiresIn": "48h"
}
```

**12) Prediction Market — Polymarket (outcome-token price crossing):**

```json
{
  "title": "Polymarket outcome crosses 60%",
  "description": "Fire when the outcome token's last traded price crosses up through 0.60, signalling the market now expects this outcome.",
  "conditions": { "AND": [{ "source": "polymarket", "method": "price", "args": { "ticker": "115556263888245616435851357148058235707004733438163639091106356867234218207169" }, "operator": "crosses_above", "value": 0.6 }] },
  "actions": [{ "stepId": "step_1", "type": "webhook", "params": { "url": "https://your-runner.example/auto/events" } }],
  "expiresIn": "48h"
}
```

**13) Recurring trigger (`repeat`):**

Re-fire on the plan's own condition instead of a fixed cron cadence — notify every time BTC
crosses down through 60k, rate-limited to once per hour, capped at 10 fires. Note the
safer-pattern choices: `crosses_below` (reacts to the crossing edge, not a value sitting
below the line) plus a `1h` cooldown and a low `maxTriggers` ceiling.

```json
{
  "title": "Notify when BTC crosses below 60k",
  "description": "Recurring risk alert: fire each time BTC price crosses down through 60000, no more than once per hour, up to 10 times.",
  "conditions": { "AND": [{ "source": "price", "method": "current", "args": { "symbol": "BTC", "exchange": "hyperliquid" }, "operator": "crosses_below", "value": 60000 }] },
  "actions": [{ "stepId": "step_1", "type": "notify", "params": { "message": "BTC dipped below 60k again" } }],
  "expiresIn": "7d",
  "repeat": { "cooldown": "1h", "maxTriggers": 10 }
}
```

**14) Calendar schedule (`cron.schedule`):**

Run on a wall-clock schedule — every weekday at 09:00 New York time. Direct EQL/API path
only (Builder Chat support pending).

```json
{
  "title": "Weekday 9am NY: market open recap",
  "description": "Every weekday at 09:00 America/New_York, run an LLM market-open recap.",
  "conditions": { "AND": [{ "source": "cron", "method": "schedule", "args": { "expression": "0 9 * * 1-5", "timezone": "America/New_York" }, "operator": "==", "value": true }] },
  "actions": [{ "stepId": "step_1", "type": "llm", "params": { "objective": "Give a concise market-open recap for BTC/ETH/SOL and flag overnight risk shifts" } }],
  "expiresIn": "7d"
}
```

**15) Funding flip (`funding`):**

Fire when Binance BTC funding turns negative — shorts start paying longs (crowded-short
signal). Note the composite `SYMBOL:EXCHANGE` ticker and venue-comparable `annualized_rate`.

```json
{
  "title": "BTC funding flips negative",
  "description": "Shorts are now paying longs on Binance BTC — a crowded-short signal worth reviewing.",
  "conditions": { "AND": [{ "source": "funding", "method": "annualized_rate", "args": { "ticker": "BTC:BINANCE" }, "operator": "crosses_below", "value": 0 }] },
  "actions": [{ "stepId": "step_1", "type": "notify", "params": { "message": "BTC funding on Binance flipped negative" } }],
  "expiresIn": "7d"
}
```

**16) Liquidation cascade (`liquidation` + `repeat`):**

Fire each time ETH liquidations cross $500k in a 5-minute window. Windows decay to zero once
a cascade subsides, so with `repeat` this fires **once per cascade**.

```json
{
  "title": "ETH liquidation cascade (5m > $500k)",
  "description": "Alert on each distinct ETH liquidation cascade on Bybit, capped at 10 alerts.",
  "conditions": { "AND": [{ "source": "liquidation", "method": "total_usd_5m", "args": { "ticker": "ETH:BYBIT" }, "operator": "crosses_above", "value": 500000 }] },
  "actions": [{ "stepId": "step_1", "type": "webhook", "params": { "url": "https://your-runner.example/auto/events" } }],
  "expiresIn": "7d",
  "repeat": { "cooldown": "1h", "maxTriggers": 10 }
}
```

**17) Catalyst → equity/index trade (HIP-3):**

The prediction-market-to-perp bridge: when a Fed-decision market reprices, take a position in
the S&P perp — including overnight and at weekends, when cash equities are closed. `xyz:SP500`
is a HIP-3 market on Hyperliquid; each `repeat` fire opens a **new** position, so `maxTriggers`
is a position count. Resolve a real open Kalshi ticker first — don't guess.

```json
{
  "title": "Fed cut odds → long S&P",
  "description": "When the market prices a cut as more likely than not, go long the S&P perp.",
  "conditions": { "AND": [{ "source": "kalshi", "method": "yes_price", "args": { "ticker": "<an open Kalshi Fed-decision market ticker>" }, "operator": "crosses_above", "value": 0.6 }] },
  "actions": [{ "stepId": "step_1", "type": "market_order", "params": { "exchange": "hyperliquid", "symbol": "xyz:SP500", "side": "buy", "amount": "250" } }],
  "expiresIn": "168h",
  "repeat": { "cooldown": "4h", "maxTriggers": 3 }
}
```

#### Poll response shape

`GET /v2/auto/queries/{queryId}` (and the x402 `POST` equivalent) returns:

```json
{
  "queryId": "q_123",
  "status": "active",
  "latestEvaluation": {
    "evaluatedAt": "2026-04-01T12:00:00.000Z",
    "wouldTriggerNow": false
  },
  "executions": [
    {
      "id": "exec_123",
      "queryId": "q_123",
      "type": "llm",
      "status": "failed",
      "error": {
        "code": "LLM_ACTION_UPSTREAM_ERROR",
        "message": "Failed to execute llm action"
      },
      "createdAt": "2026-04-01T12:00:01.000Z"
    }
  ]
}
```

Use polling for debugging or backfills. For production delivery, prefer webhook or SSE
notifications. Store `sessionId` values from executions so you can fetch full LLM analysis
only when needed via `GET /v2/auto/queries/:queryId/sessions/:sessionId`.

#### Notifications — delivery channels

After a query triggers, Auto delivers events via one of three channels:

| Channel | Best for | Setup |
|---|---|---|
| **Webhook** | Production agent automation | `action.type = "webhook"` with signature verification + queue/worker |
| **Telegram** | Fast human-readable alerts | `action.type = "telegram_bot"` with `params.botToken` + `params.chatId` (direct), or webhook→bot relay for custom formatting |
| **SSE Stream** | Real-time event consumers; **always available regardless of the chosen action** | `GET /v2/auto/queries/{queryId}/stream` using the **same auth as query creation** (`x-elfa-api-key` for API-key queries, the x402 secret for x402 queries) |

**Query `title` and `description` in notifications:** both fields are embedded in every
outbound notification (Telegram, webhook, SSE). Recipients often see an alert hours or days
after the query was set up — these fields are what make it clear **what** fired and **why
it was set up**. Always set them.

#### Notification payload (what Auto actually sends)

Auto's outbound notification object (webhook body, SSE `data`) has this shape:

```json
{
  "id": 12345,
  "type": "athena_query_notify_only",
  "category": "alerts",
  "title": "BTC breakout above 100k",
  "body": "price > threshold",
  "data": { "queryId": "q_123" },
  "priority": "high",
  "createdAt": "2026-04-01T12:00:00.000Z"
}
```

`id` is the numeric notification ID; correlate back to a query via `data.queryId`. `title`
and `body` come from the query's `title` / `description` plus trigger context.

#### Canonical event payload contract (internal normalization)

It's useful to normalize incoming events (webhook, Telegram relay, SSE) to a single internal
shape so downstream processing is channel-agnostic. This is a **recommended runner-side
convention**, not the wire format Auto sends (see the payload above):

```json
{
  "version": "1.0",
  "eventType": "query.triggered",
  "eventId": "evt_01J...",
  "timestamp": "2026-04-01T12:00:00.000Z",
  "queryId": "q_123",
  "channel": "webhook",
  "trigger": {
    "symbol": "BTC",
    "reason": "price > threshold"
  },
  "evaluation": { "triggered": true },
  "action": { "type": "webhook" }
}
```

**Webhook request headers** (what your receiver must read):

| Header | Purpose |
|---|---|
| `X-Auto-Event-Id` | Unique event ID for deduplication |
| `X-Auto-Signature-Timestamp` | Unix seconds for replay-window check |
| `X-Auto-Signature` | `v1=<hex_hmac_sha256>` — verify against raw body |

**SSE frame format** (the stream uses the **same auth used to create the query** —
`x-elfa-api-key` for API-key queries, or the x402 secret for x402 queries; it is *not*
limited to `x-elfa-api-key`. For minimal setup, attach a `notify` action with a `message` —
those notifications are retrievable only via SSE or poll):

```
id: 12345
event: notification:new
data: {"id":12345,"type":"athena_query_notify_only","category":"alerts","title":"...","body":"...","data":{"queryId":"q_123"},"priority":"high","createdAt":"2026-04-01T12:00:00.000Z"}
```

The SSE `id:` line is the **numeric notification ID** (not the query ID); the query UUID
lives in `data.queryId`.

**Telegram relay job format** (when transforming webhook → Telegram Bot API):

```json
{
  "eventId": "evt_01J...",
  "queryId": "q_123",
  "channel": "telegram",
  "chatId": "<CHAT_ID>",
  "text": "BTC trigger fired: price > threshold",
  "priority": "high"
}
```

#### Webhook signature verification

Signing inputs:

```
signing_key = SHA256(your_secret)
expected    = HMAC_SHA256(signing_key, timestamp + "." + eventId + "." + rawBody)
```

**Node.js verification:**

```typescript
import crypto from "crypto";

export function verifyAutoWebhook(
  secret: string,
  rawBody: string,
  signatureHeader: string,
  timestamp: string,
  eventId: string,
): boolean {
  if (!signatureHeader?.startsWith("v1=")) return false;
  const given = signatureHeader.slice(3);
  const signingKey = crypto.createHash("sha256").update(secret).digest();
  const payload = `${timestamp}.${eventId}.${rawBody}`;
  const expected = crypto.createHmac("sha256", signingKey).update(payload).digest("hex");
  if (given.length !== expected.length) return false;
  return crypto.timingSafeEqual(Buffer.from(given), Buffer.from(expected));
}
```

Operational checklist:
- Enforce a bounded replay window on `X-Auto-Signature-Timestamp` (reject drift >30s).
- Deduplicate by `X-Auto-Event-Id` in durable storage.
- Return `2xx` fast, then process asynchronously (queue + worker).

#### Telegram bot setup (for `action.type: "telegram_bot"` or relay)

1. Open `@BotFather` in Telegram → `/newbot` → save bot token (treat as secret).
2. Send any message to the bot (or in a group where the bot is present).
3. `curl "https://api.telegram.org/bot<BOT_TOKEN>/getUpdates"` → read `message.chat.id`.
4. Send messages via:

```bash
curl -X POST "https://api.telegram.org/bot<BOT_TOKEN>/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{"chat_id": "<CHAT_ID>", "text": "Auto trigger fired for BTC RSI"}'
```

**Direct chats, groups, and supergroups:** `telegram_bot` delivers to private chats, groups,
and supergroups. **Channels are not supported** and are rejected at create time. Two gotchas
for groups: (1) **group chat IDs are negative** (`-1001234567890`) — copy verbatim from
`getUpdates`, including the leading `-`; (2) **the bot must be able to post** — at create time
Auto checks the bot's membership/permissions, and if it can't post, create fails with
`Telegram bot cannot send messages in this chat (check its permissions)`. If a group is later
upgraded to a supergroup (new chat ID), Auto detects the migration, updates the stored ID, and
retries — no action needed.

#### Agent runner — reference architecture

Auto handles query evaluation + event emission. Your runner handles event ingestion,
verification, deduplication, strategy continuation, and audit logging.

```
Auto Query
  → Auto Event Ingress (Webhook / SSE)
  → Signature Verification + Idempotency
  → Job Queue
  → Agent Decision Worker
  → Action Adapter (Telegram / Internal API / Order Router)
  → Logs + Metrics + Alerts
```

**Core processing loop:**

1. Receive event (webhook or SSE frame).
2. Verify signature (webhook only).
3. Check idempotency — is `eventId` already processed?
4. Enqueue job and ACK `2xx` fast.
5. Worker resolves extra context (poll query, fetch LLM session).
6. Apply policy, decide next step.
7. Execute downstream action.
8. Record result for replay/debug.

**Instruction envelope** — structured contract passed from ingress to worker:

```json
{
  "eventId": "evt_123",
  "queryId": "q_123",
  "objective": "Handle trigger and decide next action",
  "allowedActions": ["notify", "fetch_session", "execute_adapter"],
  "constraints": {
    "maxExecutionSeconds": 30,
    "riskMode": "conservative"
  }
}
```

**Minimal TypeScript worker skeleton:**

```typescript
type AutoJob = { eventId: string; queryId: string; raw: unknown };
const queue: AutoJob[] = [];
const processed = new Set<string>();

function onWebhook(eventId: string, queryId: string, raw: unknown) {
  if (processed.has(eventId)) return; // idempotent
  queue.push({ eventId, queryId, raw });
}

async function workerLoop() {
  while (true) {
    const job = queue.shift();
    if (!job) { await new Promise((r) => setTimeout(r, 250)); continue; }
    // 1) Pull latest query/execution state if needed
    // 2) Fetch session details for llm actions
    // 3) Decide next action (policy + agent logic)
    // 4) Execute action (notify, relay, order adapter)
    processed.add(job.eventId);
  }
}
```

**Deployment patterns:**

| Pattern | Best for |
|---|---|
| Single process (API + worker) | Early-stage prototypes |
| API + queue + workers | Production reliability at scale |
| Serverless consumer + queue worker | Spiky workloads with managed ops |

**Local (Docker Compose) stack:**

```yaml
version: "3.9"
services:
  redis: { image: redis:7-alpine, ports: ["6379:6379"] }
  ingress:
    build: ./ingress
    environment:
      AUTO_SECRET: ${AUTO_SECRET}
      REDIS_URL: redis://redis:6379
    depends_on: [redis]
    ports: ["3000:3000"]
  worker:
    build: ./worker
    environment:
      AUTO_SECRET: ${AUTO_SECRET}
      REDIS_URL: redis://redis:6379
      ELFA_BASE_URL: https://api.elfa.ai/v2/auto
    depends_on: [redis]
```

**Minimal environment contract** (same keys local + cloud):

```
AUTO_SECRET=<event-signing secret>
ELFA_BASE_URL=https://api.elfa.ai/v2/auto
QUEUE_URL=<redis/sqs/pubsub endpoint>
RUNNER_MODE=local|cloud
```

**Reliability checklist:**

- Store dedupe keys by `eventId` in durable storage
- Retry policy with dead-letter queue
- Keep webhook handler fast and non-blocking
- Log decision input/output for every run
- Health checks + alerting on worker lag

**Recommended setup by stage:**

| Stage | Pattern |
|---|---|
| Prototype | Auto Telegram + local worker |
| Production | Auto webhook + queue + worker |
| Real-time operations | Auto SSE + worker service |

Full detail: [Notifications](https://docs.elfa.ai/auto/notifications) |
[Agent Runner](https://docs.elfa.ai/auto/agent-runner)

#### Notification troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `400` / `401` when polling or streaming | Missing/invalid API key or auth headers | Send `x-elfa-api-key`; include HMAC headers where required |
| Webhook signature mismatch | Signing wrong payload (not raw body) or wrong secret | Verify with `timestamp + "." + eventId + "." + rawBody` and `SHA256(secret)` key |
| Duplicate downstream actions | No idempotency on event processing | Dedupe by `eventId` before enqueue/execute |
| Event received but agent does nothing | Ingress processes inline and times out | ACK fast, push to queue, process in worker |
| SSE disconnect/reconnect loops | No retry/backoff or unstable consumer | Add reconnect backoff + heartbeat monitoring |
| Missing triggers after some time | Query expired or was cancelled | Poll status; check `expiresIn`, `status`, `latestEvaluation` |
| Signature timestamp rejected | Runner clock skew | Sync clock (NTP); enforce bounded replay window |
| `Telegram bot cannot send messages in this chat` at create | Bot isn't in the group, or the group revokes `can_send_messages` for it | Add the bot to the chat and grant send permission (or make it an admin), then retry |
| Telegram create fails for a group | `chatId` missing the leading `-`, or the target is a channel | Group IDs are negative (`-1001234567890`); channels are not supported |

#### Validation errors — next action table

When `/v2/auto/queries/validate` (or Create) rejects, the error is almost always a phrasing
issue, not a capability gap. Iterate on Validate instead of abandoning the query.

| Error signal | What it means | Next action |
|---|---|---|
| `EQL_MISSING_ARG` | A required arg is absent (e.g. `period` on `ema`/`sma`, or `exchange` on any `price`/`ta` condition) | Add the missing arg from the TA Args Contract, re-validate |
| Missing/invalid `exchange` on `price`/`ta` | Every `price`/`ta` condition needs `exchange` | Add `exchange` (`hyperliquid` or `gmx`) to the condition `args`, re-validate |
| `EQL_INVALID_ARG` / type errors | Wrong type (`"14"` instead of `14`) or unrecognized key (`length` vs `period`) | Use exact key names + JSON numeric types |
| Unknown `method` | Indicator name not supported | Pick nearest supported method; ask Builder Chat to substitute |
| Unsupported `timeframe` / `period` | Value outside enum | Snap to nearest allowed value |
| Unsupported `symbol` / source | Asset not indexed or DEX pair unsupported | Skip symbol and report it; proceed with supported subset |
| Depth / leaf-count exceeded | More than depth 3 or 10 leaves | Split into two queries joined by your runner |
| `cron` / `llm` period too short | Below 1h minimum | Raise to `1h` or higher |
| Unmonitored `tweet` username | `tweet.semantic` `args.username` not in monitored active accounts | Replace with a monitored active handle (without `@`) and re-validate |
| Invalid `minConfidence` (`tweet` / `news`) | Non-integer or outside `0..100` | Use a JSON integer between `0` and `100` (start with `80`) |
| `kalshi` ticker not open (`EQL_INVALID_ARG_VALUE` on `args.ticker`) | Ticker is not a currently-open Kalshi market (closed/settled/unknown) | Resolve a currently-open full ticker and re-validate; don't guess tickers |
| `kalshi` invalid enum / operator | Enum `value` outside its set, or operator not in the method's allowlist (e.g. `crosses_above` on `trade_size`) | Use the per-method operator allowlists and enum sets from the `kalshi` source reference |
| `kalshi` `is_block_trade` type error | `value` passed as a string instead of a JSON boolean | Use JSON `true` / `false`, not `"true"` / `"false"` |
| `polymarket` ticker not found / not active | `args.ticker` is not a live Polymarket outcome token (`asset_id`) — unknown or inactive | Resolve a currently-active outcome-token `asset_id` and re-validate; don't guess ids |
| `polymarket` invalid operator / dynamic value | Operator not in the method's allowlist (e.g. `crosses_above` on `size`, `>` on `side`), or a dynamic (field-vs-field) `value` was used | Use the per-method operator allowlists; use a literal `value` (dynamic values are unsupported for `polymarket`) |
| `cron.schedule` cadence too fast | Minute field isn't a single fixed value (e.g. `*/15 * * * *`), or a sub-hour cadence | Use a single fixed minute — see the `cron.schedule` allowed/not-allowed examples |
| `EQL_INVALID_REPEAT` | `repeat` was combined with a recurring cron condition (`cron.every` / `cron.schedule`) — both provide recurrence. `repeat` **is** allowed on trade actions | Remove `repeat` for recurring cron (cron already recurs), or drop the cron condition |
| `EQL_INVALID_ARG_VALUE` with `details.hip3: true` | A HIP-3 (dex-prefixed) symbol was used on a `funding` / `liquidation` condition — those feeds don't publish HIP-3 keys | Use a plain base symbol (`BTC:BINANCE`). HIP-3 stays valid on `price`/`ta` and trade actions |
| Unknown symbol in a composite ticker | Symbol not listed on that venue's perp catalog (often a naming mismatch) | Check the venue's own base-symbol convention (`1000PEPE` on Binance/Bybit vs `KPEPE` on Hyperliquid) |
| `SYMBOL_CATALOG_UNAVAILABLE` (HTTP `503`) | Market catalog was momentarily unreachable, so the symbol couldn't be checked — validation fails closed | Retry after the interval in the `Retry-After` header; this is transient — do not reshape the query |
| Dynamic value in action params | Dynamic values only allowed in condition `value` | Move dynamic reference into condition; keep action params literal |

Cross-operator semantics: `crosses_above` = previous `<` threshold AND current `>=` threshold.
`crosses_below` = previous `>` threshold AND current `<=` threshold. Both require previous-state
tracking server-side.

#### Substitution ladder — if Auto doesn't fit

Before concluding a use case is out of scope, walk this ladder. Most intents resolve at
rung 1 or 2.

1. **Rephrase through Builder Chat** — append `"If anything is unsupported, return the closest supported query and list substitutions"` to your chat prompt.
2. **Iterate on Validate Query** — loop: validate → reshape → re-validate. Do NOT jump to "this isn't possible" after one rejection.
3. **Split into multiple queries** joined by your runner (for depth 3 / 10-leaf limits).
4. **Use `source: "llm"`** with `athena_condition` for fuzzy/narrative predicates.
5. **Pre-compute in your own service, use Auto as control plane** — only after rungs 1–4 fail.

**Worked example — "alert on descending trendline break":**

- **Rung 1:** Rephrase as a supported proxy — _"alert when BTC price crosses above 4h upper Bollinger Band AND 1h RSI > 55"_.
- **Rung 4:** If the proxy isn't acceptable, use `source: "llm"` with a scheduled natural-language predicate — _"has BTC broken its recent descending trendline on the 4h chart?"_.
- **Rung 5:** Only if both fail: compute trendline-break externally, feed a boolean into an Auto `cron` + `llm` query as the condition trigger.

Do not build your own monitoring/evaluation/trigger stack before walking rungs 1–4.

#### Query drafts

Drafts let you stage an Auto query without activating it (and without spending credits).
Useful for human-in-the-loop approval workflows, dashboards where users edit before
committing, or batch authoring flows.

**Draft lifecycle:**

1. `POST /v2/auto/queries/drafts` — create or update a draft (idempotent upsert).
2. `GET /v2/auto/queries/drafts` — list editable drafts.
3. `POST /v2/auto/queries/drafts/:draftId/validate` — validate stored draft.
4. `POST /v2/auto/queries/drafts/:draftId/convert` — promote draft → active query (**HMAC conditional**: required only when the stored draft uses a trade action type).
5. `DELETE /v2/auto/queries/drafts/:draftId` — discard draft.

> `GET /v2/auto/queries/drafts/:draftId` still works but is legacy — prefer
> `GET /v2/auto/queries/{queryId}` which resolves both active queries and drafts.

Drafts are API-key-mode only. Not available via x402.

#### Symbols (tracking vs execution)

Auto is **not crypto-only.** Crypto majors and on-chain tokens are plain uppercase tickers
(`BTC`, `ETH`, `SOL`, `HYPE`, long-tail tokens). **HIP-3 assets** on Hyperliquid — tokenized
equities, indices, commodities, FX, and pre-IPO names — use a **DEX-prefixed** form
`<dex>:<SYMBOL>` and trade **24/7**, even when the underlying cash market is closed.

**Two DEX prefixes matter in practice:** `xyz` lists nearly everything and carries almost all
the volume; `mkts` lists a smaller overlapping set. Hyperliquid hosts other HIP-3 DEXs whose
markets are **dormant** (listed but not trading) — Auto **rejects** them exactly like a typo
(`EQL_INVALID_SYMBOL`). A symbol being listed on Hyperliquid is **not** enough; only the
liquid listing is usable (`GOLD` appears on six DEXs). A **bare** HIP-3 symbol is rejected —
`{"symbol": "GOLD"}` fails with `EQL_INVALID_SYMBOL`. Only plain crypto tickers work without a
prefix (they live on Hyperliquid's main DEX).

| Class | Examples |
|---|---|
| Crypto majors | `BTC`, `ETH`, `SOL`, `HYPE` (no prefix — main DEX) |
| On-chain / long-tail tokens | `RAVE`, `TAO`, niche memes |
| Indices (HIP-3) | `xyz:SP500`, `xyz:XYZ100` (Nasdaq 100), `xyz:JP225`, `mkts:US500`, `mkts:USTECH` |
| Sector / country baskets (HIP-3) | `xyz:SMH` (semis), `xyz:XLE` (energy), `xyz:EWY`, `xyz:EWJ` |
| Equities — mega-cap (HIP-3) | `xyz:NVDA`, `xyz:TSLA`, `xyz:AAPL`, `xyz:MSFT`, `xyz:GOOGL`, `xyz:META` |
| Equities — semis / high-beta (HIP-3) | `xyz:AMD`, `xyz:TSM`, `xyz:ARM`, `xyz:COIN`, `xyz:MSTR`, `xyz:PLTR` |
| Pre-IPO / private (HIP-3) | `xyz:SPCX` (SpaceX), `xyz:ZHIPU`, `xyz:MINIMAX` |
| Commodities (HIP-3) | `xyz:CL` (WTI crude), `xyz:BRENTOIL`, `xyz:NATGAS`, `xyz:GOLD`, `xyz:SILVER`, `xyz:COPPER` |
| FX (HIP-3) | `xyz:EUR`, `xyz:JPY`, `xyz:GBP` |

**Illustrative, not exhaustive — and listings change.** Markets are added and go dormant.
Never hardcode this list: confirm any HIP-3 symbol with
`GET /v2/auto/validate-symbol/{exchange}/{symbol}` before building on it, and read a rejection
as "that market is dead", not "Auto is missing the asset". HIP-3 markets are tradable on
**`hyperliquid` only** — a HIP-3 symbol on `gmx` is rejected with `EQL_INVALID_SYMBOL`.

**Composite tickers (`funding` / `liquidation` only):** those two sources do **not** take a
`symbol` + `exchange` arg — they take a single `SYMBOL:EXCHANGE` ticker (e.g. `BTC:BINANCE`,
`ETH:HYPERLIQUID`, `SOL:BYBIT`). Use each venue's own base-symbol convention: `1000PEPE` on
Binance/Bybit vs `KPEPE` on Hyperliquid. HIP-3 symbols are rejected for these two sources.

**Tracking vs execution differ:**
- **Tracking** (conditions, alerts, webhooks) covers DEX/on-chain assets — effectively
  unbounded (long-tail tokens, pre-CEX-listing assets, niche memes).
- **Execution** (`market_order` / `limit_order`) is limited to symbols tradable as perps on
  the target venue. Tradability varies by exchange — a symbol may be tradable on
  `hyperliquid`, `gmx`, both, or neither. Pre-flight with
  `GET /v2/auto/validate-symbol/{exchange}/{symbol}` (`exchange` = `hyperliquid` or `gmx`).
  The same check also validates symbols for `price`/`ta` data sources, not just execution.
  Non-tradable symbols still work for tracking.

Full reference: [Symbols](https://docs.elfa.ai/auto/symbols) and
[Catalyst Triggers](https://docs.elfa.ai/auto/catalyst-triggers).

#### Trade execution (`market_order` / `limit_order`)

Live trade actions execute on a connected perp venue. **Two venues are supported:
`hyperliquid` and `gmx`.** (The `exchange` arg on a `price`/`ta` *condition* is separate —
it only selects market-data source, not where orders execute.)

**Order params:**

| Param | Required | Notes |
|---|---|---|
| `exchange` | yes | `hyperliquid` or `gmx` (no default) |
| `symbol` | yes | e.g. `BTC`, `ETH`, `SOL` — must be tradable on the venue |
| `side` | yes | `buy` or `sell` |
| `amount` / `size` / `positionSizePercent` | yes (exactly one) | `amount` = USD/USDC notional; `size` = contracts/units; `positionSizePercent` = % of account value, range `(0, 100]` |
| `price` | limit only | absolute limit price (string) |
| `reduceOnly` | no | default `false`; **Hyperliquid only** (rejected on GMX) |
| `leverage` | no | integer ≥ 1 |
| `marginType` | no | `cross` or `isolated`; **Hyperliquid only** (rejected on GMX); when omitted, the asset's current margin mode is preserved |
| `tp` | no | take-profit, `"5%"` or absolute `"50000"` |
| `sl` | no | stop-loss, `"2%"` or absolute `"48000"` |

`positionSizePercent` resolves at execution as
`accountValue × (positionSizePercent / 100) × effectiveLeverage`, converted to size via the
order's reference price — mark price for `market_order`, limit price for `limit_order`.

**Venue differences:**

| Feature | Hyperliquid | GMX |
|---|---|---|
| Minimum `amount` | 10 USDC | none |
| `reduceOnly` | supported | rejected |
| `marginType` | supported | rejected |
| HIP-3 markets (equities, indices, commodities, FX) | supported | not listed (rejected) |

**Trading HIP-3 markets:** order actions are not limited to crypto. Any HIP-3 market
(`xyz:SP500`, `xyz:NVDA`, `xyz:GOLD`, `xyz:CL`, `xyz:SPCX`) is tradable through the same
`market_order` / `limit_order` schema using its DEX-prefixed symbol — **`hyperliquid` only**
(the same order with `"exchange": "gmx"` is rejected `EQL_INVALID_SYMBOL`). They trade 24/7,
including when the underlying cash market is halted; max leverage is per-market and the `10`
USDC minimum notional still applies.

**Catalyst pattern (prediction market → asset it moves):** a prediction-market condition
doesn't have to end the plan — it can be the trigger for a position in the asset that catalyst
moves. A Kalshi Fed-decision leaf (`yes_price crosses_above 0.6`) can fire a `market_order` on
`xyz:SP500` at 3am on a Sunday, while cash equities are shut. Bridge on **asset class** (rates
→ indices/mega-cap/metals/FX; earnings → mega-cap/semis; a named commodity → that commodity),
and use `maxTriggers` as a hard circuit breaker. Full guide:
[Catalyst Triggers](https://docs.elfa.ai/auto/catalyst-triggers).

Trade fees: Elfa charges **0.05% per trade**; the venue's own fees also apply (e.g.
Hyperliquid base fee scales with 14-day volume).

**Reading account state:** Auto executes trades but does **not** proxy account-state reads
(balance, leverage, positions, unrealized PnL) — read those from the venue directly. On
**Hyperliquid**, use its [Info endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)
(a `POST /info` REST API) with the **master account address** (the address that owns the
funds), not the agent wallet address. On **GMX**, read on-chain via the GMX Reader contract
or the GMX subgraph — there is no REST `info` endpoint as on Hyperliquid.

#### Exchange connections

Required only for **live trade-execution actions** (beyond `webhook`, `notify`,
`telegram_bot`, `llm`). Connects your venue account to Auto so triggered queries can place
orders on your behalf.

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| `/v2/auto/exchanges` | POST | HMAC | Connect an exchange |
| `/v2/auto/exchanges` | GET | API key | List connected exchanges |
| `/v2/auto/exchanges/:exchange` | DELETE | HMAC | Disconnect |

**Trade-ready onboarding** (one-time): enable Auto in the dev portal (Privy link + HMAC
secret) → complete venue onboarding (Hyperliquid and/or GMX) in the Elfa app → return to the
portal and click **Verify connection**. Then `GET /v2/auto/exchanges` must show the target
venue active, or trade actions fail at execution time with `AGENT_WALLET_REQUIRED`.

Exchange connections are API-key-mode only. Not available via x402. Trade execution is not
available via x402 at all. Full reference:
[Trading Execution](https://docs.elfa.ai/auto/trading-execution).

#### Executions

Every trigger fire produces an **execution record** — use these endpoints to audit trigger
history, debug failed actions, or reconcile with your runner's audit log.

| Endpoint | Method | Description |
|---|---|---|
| `/v2/auto/executions` | GET | List execution records (filterable) |
| `/v2/auto/executions/:executionId` | GET | Get a single execution record |

Execution records are also embedded in the poll response (`GET /v2/auto/queries/:queryId`)
under the `executions` array, but the dedicated endpoints are useful for cross-query audits
and pagination.

Executions are API-key-mode only. Not available via x402.

### Step 3b: Trade — Direct Execution

Trade is a **direct, synchronous order API** on `/v2/trade/*`. You call an endpoint, it
executes against the venue immediately, and the response carries the fill. No condition
engine, no query, no trigger — one request, one order.

Full Trade docs: [docs.elfa.ai/trade/overview](https://docs.elfa.ai/trade/overview)

#### Trade vs Auto — which to use

Both place orders for the **same linked account** with the **same API key + HMAC** auth and
the **same venues** (`hyperliquid`, `gmx`). They differ only in _when_ the order fires:

| | **Trade** (`/v2/trade/*`) | **Auto** (`/v2/auto/*`) |
|---|---|---|
| Execution | Synchronous — fires on the request | Conditional — fires when a trigger resolves true |
| You send | An order to execute now | A query (conditions + actions) to evaluate over time |
| State created | None (proxied straight to the venue) | A persistent query you poll/stream |
| Best for | "Place this order now", bots that decide off-platform | "Watch for X, then trade", alerting + automation |

Use **Trade** when the agent has already decided and wants to act now. Use **Auto** when you
want Elfa to watch the market and act for you.

#### Access model

- `x-elfa-api-key` on **every** request (including previews).
- The key must be **Privy-linked** (enable Auto in the [Developer Portal](https://dev.elfa.ai/)).
  Unlinked keys get `403`. Same prerequisite as Auto — there is no separate Trade enablement.
- An **active exchange connection** for the target venue must exist, or the write fails at
  execution. Verify with `GET /v2/auto/exchanges` before placing orders.
- **HMAC required on every write** (place / cancel / modify / close / tpsl); previews are
  unsigned. Unlike Auto, there is **no notification-only bypass** — every Trade write is signed.
- Trade is **not** available in x402 keyless mode.

#### HMAC signing (Trade mount)

Identical scheme to Auto, with **one critical difference: the signed `mounted_path` is
relative to the `/v2/trade` mount**, not `/v2/auto` and not the full URL path.

```
timestamp + method + mounted_path + body
```

- Request URL: `/v2/trade/orders` → signed path: `/orders`
- Request URL: `/v2/trade/orders/cancel` → signed path: `/orders/cancel`
- Request URL: `/v2/trade/positions/close` → signed path: `/positions/close`
- Request URL: `/v2/trade/positions/tpsl` → signed path: `/positions/tpsl`

Signing `/v2/trade/orders` instead of `/orders` fails verification. Replay window: ±30s.
Send a per-request UUID in `x-correlation-id` (optional but recommended — used for tracing;
the backend does **not** de-duplicate, so pair it with a client-side guard to avoid double
submissions).

#### Sizing an order

Order and close payloads accept three **mutually-exclusive** ways to size — provide exactly one:

| Field | Type | Meaning |
|---|---|---|
| `size` | `string` | Base units (contracts), e.g. `"0.1"` BTC |
| `amount` | `string` | Quote/USD notional, e.g. `"2500"` |
| `positionSizePercent` | `number` | Percent of available balance, `(0, 100]` |

All sizes and prices are **decimal strings**; only `leverage`, `positionSizePercent`, and
`closePercent` are numbers. Venue notes: `reduceOnly` / `marginType` are **Hyperliquid-only**
(rejected for GMX); Hyperliquid has a `10` USDC minimum notional, GMX has none.

#### Place an order (preview → sign → place)

Always preview unfamiliar payloads first (free, unsigned), then place (1 credit, signed):

```bash
# 1. Preview (free, no HMAC)
curl -sS -X POST https://api.elfa.ai/v2/trade/orders/preview \
  -H "x-elfa-api-key: ${ELFA_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"exchange":"hyperliquid","symbol":"BTC","side":"buy","orderType":"market","amount":"25"}'
# -> { "success": true, "wouldExecute": true }

# 2. Place (1 credit, HMAC required — sign the MOUNTED path "/orders")
TIMESTAMP=$(date +%s)
BODY='{"exchange":"hyperliquid","symbol":"BTC","side":"buy","orderType":"market","amount":"25"}'
SIGNATURE=$(echo -n "${TIMESTAMP}POST/orders${BODY}" | \
  openssl dgst -sha256 -hmac "${ELFA_HMAC_SECRET}" -hex | awk '{print $2}')

curl -sS -X POST https://api.elfa.ai/v2/trade/orders \
  -H "x-elfa-api-key: ${ELFA_API_KEY}" \
  -H "x-elfa-signature: ${SIGNATURE}" \
  -H "x-elfa-timestamp: ${TIMESTAMP}" \
  -H "x-correlation-id: $(uuidgen)" \
  -H "Content-Type: application/json" \
  -d "${BODY}"
# -> { "success": true, "orderId": "123456789", "filledSize": "0.0004", "avgFillPrice": "62500" }
```

With the bundled helper (handles `/v2/trade` signing automatically when `ELFA_HMAC_SECRET` is set):

```bash
./scripts/elfa_call.sh /v2/trade/orders/preview -d '{"exchange":"hyperliquid","symbol":"BTC","side":"buy","orderType":"market","amount":"25"}'
./scripts/elfa_call.sh /v2/trade/orders -d '{"exchange":"hyperliquid","symbol":"BTC","side":"buy","orderType":"market","amount":"25"}' --hmac-secret "$ELFA_HMAC_SECRET"
```

#### Manage the position

All write routes sign the same way — just change `mounted_path` and `body`:

- **Attach TP/SL** — `POST /v2/trade/positions/tpsl` (`{ "exchange": "...", "symbol": "BTC", "tp": "72000", "sl": "60000" }`)
- **Close (full or partial)** — `POST /v2/trade/positions/close` (`{ ..., "orderType": "market", "closePercent": 100 }`)
- **Cancel a resting order** — `POST /v2/trade/orders/cancel` (`{ ..., "orderId": "123456789" }`)
- **Modify a resting order** — `POST /v2/trade/orders/modify` (`{ ..., "orderId": "123456789", "price": "61000" }`)

#### Errors and reconciliation

Failures carry `success: false` and a structured `error` `{ code, message }` (e.g.
`INSUFFICIENT_MARGIN`, `TRADE_SERVICE_UNAVAILABLE`).

| Status | Meaning | Billed? |
|---|---|---|
| `200` | Success — order executed / action accepted | Yes (writes that cost credits) |
| `400` | Missing or invalid parameters | No |
| `401` | Missing/invalid API key, signature, timestamp, or clock skew | No |
| `403` | API key not linked for trading | No |
| `422` | Order rejected by the venue (e.g. insufficient margin) | No |
| `502` | Transport / trade-service failure (`TRADE_SERVICE_UNAVAILABLE`), incl. timeout | No |

> **Reconcile before retrying a `502`.** A write blocks up to the trade service's 60-second
> timeout. On timeout the order **may still have landed** at the venue, and there is no
> server-side idempotency lock — a blind retry can double-fill. Read your open
> orders/positions from the venue first and only resubmit if the order is genuinely absent.

Trade executes orders but does **not** proxy balances, positions, or PnL — read those from the
venue directly (see [Trading Execution](https://docs.elfa.ai/auto/trading-execution)).

### Step 4: Generating code snippets

When the user wants integration help, generate correct, production-ready code.
See the [Elfa API documentation](https://docs.elfa.ai) for the full parameter specs.

**Principles for code generation:**
- Always mention both access modes (API key and x402) so developers know their options
- Include the signup link `https://go.elfa.ai/claude-skills` as a comment near the
  API key placeholder, and link to `https://docs.elfa.ai/x402-payments` for x402
- Always include proper error handling
- For API key mode: show the `x-elfa-api-key` header (use a placeholder like `YOUR_API_KEY`)
- For x402 mode: show the `/x402/v2/` prefix and recommend `@x402/fetch` or `@x402/axios`
- For Auto trade mutations and exchange linking: include HMAC signing code (notification-only mutations skip HMAC); for x402 use the agent-secret header
- Include TypeScript types when generating TS code
- Add comments explaining each parameter
- For pagination endpoints, show how to paginate through results
- For time-windowed endpoints, explain the `timeWindow` vs `from`/`to` pattern

**Language priorities** (use unless the user specifies otherwise):
1. TypeScript/JavaScript (fetch) — most Elfa integrators are web/Node devs
2. Python (requests)
3. curl

**The Chat endpoint deserves special attention** — it's the most complex:
- It supports multiple `analysisType` values: `chat`, `macro`, `summary`, `tokenIntro`,
  `tokenAnalysis`, `accountAnalysis`
- Session management via `sessionId` for multi-turn conversations
- Different `assetMetadata` requirements per analysis type
- Two speed modes: `fast` and `expert`

**Auto code generation guidance:**
- Always include the validate → create flow (never create without validating first)
- For API key mode: include HMAC signing helper for trade-action and exchange-linking calls (notification-only mutations can be made with just `x-elfa-api-key`)
- For x402 mode: include `x-elfa-agent-secret` header on all query lifecycle calls
- Include Builder Chat examples when the user wants natural-language query building
- Show how to poll or stream for results after query creation

### Common patterns

**Time window parameters:**
Many endpoints accept either `timeWindow` (e.g., "30m", "1h", "4h", "24h", "7d", "30d")
OR `from`/`to` unix timestamps. If both are provided, `from`/`to` takes priority.

**Pagination:**
Aggregation endpoints (trending-tokens, trending-cas, top-mentions, token-news) use
`page` + `pageSize`. The keyword-mentions endpoint uses cursor-based pagination instead
(`cursor` + `limit`).

Defaults and maximums:

| Parameter | Default | Max |
|---|---|---|
| `pageSize` | `20` (data) / `50` (aggregations) | `100` |
| `limit` (keyword-mentions cursor) | `20` | `30` |
| `page` | `1` | — |
| `timeWindow` | `24h` | — |

**Per-endpoint parameter notes:**
- **`keyword-mentions`** — accepts `keywords`, `accountName`, `searchType` (`or`), `from`/`to`,
  `limit`, `cursor`. Provide either `keywords` OR `accountName` (or both); `accountName`
  filters mentions by a specific account (e.g. `accountName=elonmusk`).
- **`token-news`** — accepts `coinIds`, `from`/`to`, `page`, `pageSize` (default `20`). V2
  always returns news mentions (no `isNews` parameter).
- **`top-mentions`** — accepts `ticker`, `timeWindow`, `page`, `pageSize`. Account details are
  always included (no `includeAccountDetails` parameter).

**Ticker format (top-mentions):**
The `ticker` parameter behavior changes based on whether you include the `$` prefix:
- **With `$` prefix** (e.g., `ticker=$SOL` or URL-encoded `ticker=%24SOL`): Exact cashtag matching only. Searches the `cashtags` field for exact matches.
- **Without `$` prefix** (e.g., `ticker=SOL`): Broader search across both cashtags (boosted 2x) and general token references.

Use `$` when you want only cashtag-specific mentions. Omit `$` for a more inclusive search.

**Credit costs (data endpoints — both modes):**
- Most endpoints: 1 credit per call ($0.009 via x402)
- Event summary: 5 credits ($0.045 via x402)
- Trending narratives: 5 credits ($0.045 via x402)
- Chat: fast = 5 credits ($0.045), expert = 18 credits ($0.162) via x402

**Auto query lifecycle:**
- **Validate before create (recommended):** Call `POST /v2/auto/queries/validate` first to preview
  estimated credits and catch validation errors before committing. The server validates internally
  during create anyway, but pre-validation lets you iterate on errors without side effects.
- Prefer webhook or SSE for real-time delivery
- Deduplicate events by `eventId`
- Use shorter expiries (`24h`–`3d`) for fresh signals
- Include `title` and `description` in queries — they appear in notifications

## Important notes

- The Elfa API domain (`api.elfa.ai`) must be accessible from the network. If blocked,
  inform the user and provide the code snippet instead.
- Always use the v2 endpoints (paths starting with `/v2/` or `/x402/v2/`).
- For experimental endpoints (trending-tokens, smart-stats), mention that behavior may
  change without notice.
- When the user asks about pricing or API key tiers, direct them to
  https://go.elfa.ai/claude-skills for full details on plans and pricing.
- API-key request rate limits are per tier: Free / Chill / PAYG = **60 requests/min**,
  Grow = **120 requests/min** (Enterprise custom). These are independent of credit balances.
- x402 is currently in beta. Rate limits: 1,000 requests per 60s window (per client IP).
- x402 and API key credits are independent — they do not overlap or share balances.
- For x402 documentation and setup, refer users to https://docs.elfa.ai/x402-payments.
- For Auto documentation, refer users to https://docs.elfa.ai/auto/overview.
- Auto HMAC signing uses the **mounted path** (e.g., `/queries`), NOT the full URL path
  (`/v2/auto/queries`). Using the full path will fail signature verification.
- Auto x402 agent secret must be persistent — do not rotate per request.
- For the full list of Auto capabilities, triggers, and query templates, see
  https://docs.elfa.ai/auto/capabilities and https://docs.elfa.ai/auto/query-model.
