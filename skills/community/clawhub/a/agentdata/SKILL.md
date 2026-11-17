---
name: agentdata
description: "Crypto market signals and pre-trade checks for agents, paid per call in USDC on Base via x402 (from $0.001, no account, no API key): funding rates and predictions, liquidation zones, sentiment, stablecoin peg health, DEX-vs-CEX and cross-exchange spreads, ETF flows, memecoin risk checks, labelled crypto news, a search for x402 services that answer right now, a red-flag check before a trade, wallet liquidation risk with alerts, signed receipts, recorded history anchored on Base. Every predictive signal has a public track record against a naive baseline. Use when the user asks about crypto market conditions, funding, liquidations, depeg risk, a memecoin's risk or crypto news, needs a paid x402 service for some other task, or wants crypto data an agent can pay for itself."
homepage: https://agentdata-api.com
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "homepage": "https://agentdata-api.com",
        "requires": { "bins": ["curl"] },
      },
  }
---

# AgentData

Crypto market data at `https://agentdata-api.com`, sold per request through the x402 protocol: an
endpoint answers `402 Payment Required` with its price, the caller pays in USDC on Base, and the data
comes back. No account and no API key. Settlement gas is paid by the service, so the buying wallet
needs USDC only, no ETH.

What sets it apart from other price feeds: signals are recorded every hour or quarter hour and kept,
each day of records is committed to Base as a Merkle root, and every signal that makes a prediction
is scored in public against a naive baseline, including the ones that do not beat it.

## Step 1: start free

These cost nothing and need no wallet:

```bash
curl -s https://agentdata-api.com/api/try/prices          # BTC price (paid version adds ETH, SOL, BNB, XRP)
curl -s https://agentdata-api.com/api/try/sentiment       # Fear & Greed component
curl -s https://agentdata-api.com/api/try/funding-rates   # BTC perpetual funding rate
curl -s https://agentdata-api.com/calibration             # track record of every signal
curl -s https://agentdata-api.com/pricing                 # every price in one call, for a budget
curl -s https://agentdata-api.com/info                    # live catalogue with current prices
```

Samples are rate-limited to 30 requests a minute. Each sample names in `withheld` what the paid
version adds.

**Read `/calibration` before paying for a signal as a predictor.** For each signal it reports the hit
rate, the error, and whether it beats a naive baseline (`beatsNaive`, `beatsBaseRate`). A `false`
there means the number is still useful as a current reading but not as a forecast. `knownWeaknesses`
lists verdict fields that are near-constant by construction (for example a risk level that has read
LOW in every observation); use the raw numbers beside them instead. The memecoin record shows that
most new tokens collapse within a week whatever the verdict says: treat a memecoin verdict as a list of
concrete red flags, never as a buy signal.

## Step 2: paying

Prices are in the `402` reply, in `/pricing` and in `/info`; they are what the service charges, so do
not rely on a remembered price. Responses of scored signals carry a `trackRecord` field: if it says
`beatsBaseRate: false` or `beatsNaive: false`, use the value as a reading, not as a forecast. Most calls cost $0.002 to $0.005.

**Do not spend the user's money without their go-ahead.** Say what you want to call and what it costs,
and keep to a budget they set.

### With the AgentData MCP server (simplest)

The npm package `agentdata-mcp` pays automatically from a buyer wallet, with a per-call cap
(`AGENTDATA_MAX_PAYMENT_USDC`, default 0.05) and a per-process budget
(`AGENTDATA_SESSION_BUDGET_USDC`, default 1.00). It exposes every endpoint as a tool.
The five free tools are marked read-only, so OpenClaw can run them without asking; the paid ones are
not, so it asks before each call that would pay. Leave it that way.

The user sets this up, not you:

1. A **dedicated** wallet holding only a few USDC on Base. Never a main wallet.
2. Its private key in the environment of the process that runs OpenClaw, for example
   `export AGENTDATA_BUYER_PRIVATE_KEY=0x...` before starting the gateway. Never ask the user to
   paste a key into the chat, and never print it.
3. Then register the server. The key is referenced, not written into the config; OpenClaw fills
   `${...}` in from its own environment when it starts the server:

```bash
openclaw mcp add agentdata --command npx --arg=-y --arg agentdata-mcp \
  --env 'AGENTDATA_BUYER_PRIVATE_KEY=${AGENTDATA_BUYER_PRIVATE_KEY}' \
  --env AGENTDATA_SESSION_BUDGET_USDC=0.50 --no-probe
openclaw mcp probe agentdata     # expect 42 tools
```

`--no-probe` is needed: the check that `mcp add` runs before saving passes `${...}` through as text,
the server rejects that as a key and nothing is saved. `mcp probe` afterwards fills it in. The same
happens later if the variable is missing from OpenClaw's environment: the server does not start.
Without a key at all (leave out the first `--env` and `--no-probe`), the server still runs and answers
the free tools; paid tools then return the payment requirements instead of data.

Tested with OpenClaw 2026.11.3 and agentdata-mcp 1.5.0.

**The wallet must be a plain account.** A wallet that delegates to a contract through EIP-7702 cannot
pay this way: USDC then checks the signature through the delegate contract, which rejects it, and every
payment fails with `invalid_exact_evm_transaction_simulation_failed`. This has happened to a real
buyer. `eth_getCode` of the wallet address must return `0x`.

### Without MCP

Any x402 v2 client works: send the request, read the base64 JSON `PAYMENT-REQUIRED` header, sign the
Base USDC requirement as an ERC-3009 `TransferWithAuthorization`, and resend with `PAYMENT-SIGNATURE`.
Echo the chosen requirement unchanged; the server compares it with what it issued. Full steps:
https://agentdata-api.com/llms.txt

## What to call

| Need | Endpoint | Price |
| --- | --- | --- |
| Overnight / "what changed" risk check | `/api/overnight-risk-brief` | $0.012 |
| Eight signals in one payment | `/api/market-pulse` | $0.018 |
| Funding now / next settlement | `/api/funding-rates`, `/api/funding-predictions` | $0.002 / $0.003 |
| Where leveraged positions get liquidated | `/api/liquidation-levels` | $0.003 |
| Stablecoin depeg check | `/api/stablecoin-health` | $0.002 |
| On-chain vs exchange price gap | `/api/dex-vs-cex` | $0.005 |
| One memecoin on Solana or Base | `/api/memecoin/risk?chain=solana&token=<mint>` | $0.005 |
| Only what changed since this wallet last paid | `/api/diff?signal=<name>` | $0.001 |
| Recorded history of a signal | `/api/history/7d?signal=<name>` | $0.005 |
| Red flags before one concrete trade (slippage, liquidation distance, funding, peg) | `/api/pretrade-check?asset=BTC&side=long&sizeUsd=10000&leverage=5` | $0.008 |
| How close a wallet is to liquidation on Aave v3 / Morpho (Base) | `/api/wallet/risk?address=<0x…>` | $0.005 |
| Leave a condition watching while offline, and be woken (`webhook=` or `ntfy=`) | `/api/watch?signal=&op=above&threshold=&hours=` | $0.010 |
| Crypto news, each item labelled (assets, sentiment, relevance) | `/api/news?hours=24&asset=BTC` | $0.003 |
| Label one crypto text (see Privacy) | `/api/grid/classify?text=<up to 1,000 chars>` | $0.005 |
| Find another paid x402 service that answers now | `/api/x402/services?q=<words>&maxPrice=0.01` | $0.005 |

The full list with every parameter is in `/info` and `/openapi.json`. History is offered only for
signals whose record has no hole longer than six hours; others answer `404`.

## Errors

| Reply | Meaning | What to do |
| --- | --- | --- |
| `402` without a payment | the price | pay, or stop if it is over budget |
| `402` after paying | payment rejected; the reason is in the `error` field of the decoded `PAYMENT-REQUIRED` header | `..._insufficient_balance`: the wallet needs USDC; `..._simulation_failed`: see EIP-7702 above |
| `400` | the request is wrong (unknown signal, bad address) | fix the request; nothing was charged |
| `502` | an upstream source failed | retry later; nothing was charged |
| `404` on history | that record is not complete enough to sell | use a shorter tier or `/api/diff` |

A payment is only settled when the data is delivered with status 200.

## Receipts

Every paid answer carries a signed receipt (`X-AgentData-Receipt` and `X-AgentData-Receipt-Signature`;
over MCP it is appended to the tool result). It binds the SHA-256 of the answer to the request and to
the payment authorization's nonce. Keep it if you may need to show later what data a decision was
based on. Signer and how to check: `https://agentdata-api.com/.well-known/agentdata-receipts.json`;
free check: `/receipts/verify?receipt=&signature=`.

## Checking a record yourself

Each recorded day can be recomputed and compared with the root published on Base:
`https://agentdata-api.com/anchors?verify=YYYY-MM-DD`.

## Privacy

Requests carry no account. The paying wallet address is visible on-chain, like any USDC transfer, and
is used by the service to keep `/api/diff` cursors and watches per wallet. Text sent to
`/api/grid/classify` is processed in plain text by independent GPU operators on AI Power Grid: never
send anything private there. Like any web service it logs
requests (time, path, status, IP address, user agent) for operation and rate limiting.
