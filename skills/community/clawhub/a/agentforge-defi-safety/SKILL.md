---
name: agentforge-defi-safety
description: Safety checks for agents that act on-chain. Call `preflight` once before any send, swap, approval, signature or x402 payment and get one proceed/caution/avoid verdict (transaction simulated, EIP-712 signature checked for permit phishing, recipients screened against OFAC sanctions and scam lists, tokens rug-checked). Also signature checks, transaction simulation, address screening, pre-trade token checks, batch rug checks, risk-scored new launches, Aave liquidation risk, and Solana simulation, on Ethereum, Base, Arbitrum, Optimism, Polygon, BNB Chain, Avalanche, Linea, Unichain, Sonic and Solana. Free over MCP up to a daily cap (no wallet); otherwise pay per call in USDC over x402, with the exact price quoted before any charge.
version: 1.10.0
metadata:
  author: agentforge
  openclaw:
    emoji: "🛡️"
    homepage: https://agentforge-taupe.vercel.app
    requires:
      anyBins:
        - curl
---

# AgentForge

AgentForge is a DeFi safety layer for AI agents on ten EVM chains and Solana. Base URL: `https://agentforge-taupe.vercel.app`. It has two tiers, and the free tier costs nothing to try:

1. **Free** — contract/program label lookups, full catalog, service docs, feedback. No wallet, no payment, no account.
2. **Paid** — 26 deeper analysis endpoints (one-call preflight safety checks, signature phishing checks, transaction simulation, liquidation risk, new-launch feed, address screening, batch rug checks, pre-trade token checks, wallet safety, transaction decode/simulate, and more), each billed per call via [x402](https://www.x402.org/) in USDC. Every price is stated plainly below and at `GET /catalog` — nothing is hidden.

## Free entry points (start here, no payment required)

- `GET /registry/lookup?address=0x...&chain=ethereum` — look up an EVM contract in our 433-contract label registry (protocol name, category, risk level).
- `GET /v1/solana/program-lookup?programId=...` — look up a Solana program in our 63-program label registry (protocol, category, risk level). Same idea, Solana side.
- `GET /registry/stats` — EVM registry coverage stats (entry count, chains, categories).
- `GET /catalog` — full machine-readable catalog of all 26 paid endpoints with current prices and JSON schemas.
- `GET /about` — service overview, every endpoint with description and `input_example` payload.
- `GET /.well-known/x402` — x402 discovery document (accepted networks, assets, payTo address).
- `POST /feedback` — report a bad response or suggest an improvement.

## MCP server — free, no wallet needed

All 27 tools are exposed over MCP at `https://agentforge-taupe.vercel.app/mcp` (Streamable HTTP). MCP calls are **free**: no wallet, no x402, no account.

- Lookups (`registry_lookup`, `solana_program_lookup`) and cheap data (`gas_oracle`, `pool_snapshot`) are unlimited.
- Every analysis tool is free for 10 calls per tool per client per day. Past that, the tool returns the matching paid x402 endpoint and its exact price.

Add it to Claude Code:
```bash
claude mcp add --transport http agentforge https://agentforge-taupe.vercel.app/mcp
```
Cursor, Windsurf, Claude Desktop: add an HTTP MCP server with the same URL.

Use the paid HTTP endpoints below when you need more volume than the free daily allowance, or when your agent already pays via x402.

## When to use the paid endpoints

- In a trading loop: poll `launches` every 1-5 minutes (pass `nextSince` back as `since`) for newly listed tokens that are already risk-scored, then re-screen your watchlist with `risk-batch` (2-25 tokens per call, priced per token).
- Before signing any message or permit: `signature-check` explains what the signature allows and catches permit phishing, sell-for-nothing NFT orders, and over-priced or fake x402 payment requests.
- Before ANY on-chain action, the simplest rule: call `preflight` with whatever you are about to do (transactions, a signature request, an x402 payment request, recipients, tokens to buy). One verdict covers simulation, signature phishing, sanctions/scam screening, and rug checks, on Ethereum, Base, Arbitrum, Optimism, Polygon, BNB Chain, Avalanche, Linea, Unichain and Sonic.
- Before signing any EVM transaction: `tx-simulate` shows exactly what leaves the wallet, which approvals are granted, and whether any counterparty is sanctioned or a known scammer.
- Managing a leveraged position: `lending/health` reports the Aave v3 health factor on every chain and how far collateral can fall before liquidation.
- Before every outgoing transfer or approval: `address-check` screens the counterparty against OFAC sanctions and scam-wallet lists and flags brand-new address-poisoning wallets (1-100 addresses per call).
- Before buying a token: `trade-check` runs the rug check, the AI risk assessment, and the gas oracle in one call and returns a proceed/caution/avoid verdict — cheaper than the three calls separately.
- Before executing a DeFi transaction: check `wallet-safety` or `approval-scan` (EVM) — or `solana/tx-simulate` (Solana).
- Before touching a new token: run `token-risk-metrics` (EVM) or `solana/token-risk-scan` (Solana) — rug check: mint/freeze authority, holder concentration, liquidity.
- To understand a transaction: `tx-decode` (EVM) or `solana/tx-explain` (Solana) turn raw transaction data into a plain-English explanation.
- To understand a contract: `contract-docs` generates function-level documentation with a security posture summary.
- For general AI text tasks tied to crypto/DeFi content: `sentiment`, `summarize`, `translate`.

## Endpoints and current prices

| Method | Path | Price (USDC) | What it does |
|---|---|---|---|
| POST | `/v1/preflight` | $0.008 + $0.004/token | Is this action safe? One call before any on-chain action: transactions simulated, signatures checked for phishing, recipients screened for sanctions and scams, tokens rug-checked (including tokens the simulation shows you receiving). One proceed/caution/avoid verdict. |
| POST | `/v1/signature-check` | $0.003 | Check a signature request before signing: EIP-712 permits, Permit2, Seaport orders, transfer authorizations, and x402 payment requests decoded, spenders and payees screened, drainer patterns caught. |
| POST | `/v1/tx-simulate` | $0.005 | Simulate 1-5 EVM transactions before signing: revert reason, asset changes, approvals, counterparty sanctions/scam screening, proceed/caution/avoid. Ethereum, Base, Arbitrum, Optimism, Polygon, BNB Chain, Linea, Unichain, Sonic. |
| GET | `/v1/lending/health` | $0.003 | Aave v3 liquidation risk across nine chains: collateral, debt, health factor, status, collateral drop to liquidation. |
| GET | `/v1/launches` | $0.005 | New-launch feed (Base, Ethereum, Arbitrum, BNB Chain), each launch already risk-scored: owner powers, proxy, supply held off-pool, honeypot trading pattern. Poll with `since=<nextSince>`. |
| POST | `/v1/address-check` | $0.003 + $0.001/extra address | Counterparty screening for 1-100 EVM or Solana addresses: OFAC sanctions, scam/phishing wallets, labeled protocols, brand-new addresses. |
| POST | `/v1/risk-batch` | $0.004 per token (2-25) | Rug-check a watchlist in one call: holder, permission, and liquidity risk per token. |
| POST | `/v1/trade-check` | $0.025 | Pre-trade bundle: rug-check metrics + AI risk assessment + current gas in one call, with a proceed/caution/avoid verdict. Cheaper than the three calls separately. |
| POST | `/v1/wallet-safety` | $0.10 | Comprehensive pre-transaction wallet safety check: approvals + activity pattern + target contract risk in one call. |
| POST | `/v1/token-risk-metrics` | $0.05 | Rug check / token risk score: mint authority, freeze authority, holder concentration, liquidity depth, deployer history, composite 0-100 score. |
| POST | `/v1/approval-scan` | $0.015 | Scans a wallet for risky ERC-20 approvals (unlimited allowances, unverified spenders). |
| POST | `/v1/contract-monitor` | $0.025 | Recent contract admin activity: ownership transfers, upgrades, pause changes. |
| POST | `/v1/contract-docs` | $0.05 | Human-readable smart contract documentation with security posture and interaction patterns. |
| POST | `/v1/tx-decode` | $0.05 | Decode any EVM transaction: function call, params, token transfers, plain-English explanation. |
| POST | `/v1/token-research` | $0.03 | Multi-source token research: CoinGecko + DeFiLlama + Etherscan + Polymarket in one report. |
| POST | `/v1/token-compare` | $0.08 | Compare a token against up to 3 competitors with AI-generated analysis. |
| POST | `/v1/token-intel` | $0.015 | Quick token lookup: market data + risk score in under 10 seconds. |
| GET | `/v1/gas` | $0.003 | Real-time gas prices (slow/standard/fast) with trend analysis, any supported EVM chain. |
| GET | `/v1/pool-snapshot` | $0.005 | Top 500 DeFi liquidity pools by TVL, filterable by protocol/chain/token, refreshed every 15 min. |
| POST | `/v1/sentiment` | $0.003 | Sentiment analysis for crypto/finance/social text. |
| POST | `/v1/summarize` | $0.008 | Text summarization with configurable length and format. |
| POST | `/v1/translate` | $0.002 | Translation with tone control, auto-detects source language. |
| GET | `/v1/ping` | $0.001 | Verifies your x402 payment flow works end to end — and returns the full service catalog with prices and example inputs. |
| POST | `/v1/solana/token-risk-scan` | $0.35 | Solana rug check: mint/freeze authority, holder concentration, liquidity depth, composite 0-100 score. Base or Solana USDC. |
| POST | `/v1/solana/tx-simulate` | $0.15 | Simulate a Solana transaction before signing: balance changes, labeled programs, proceed/caution/avoid recommendation. Base or Solana USDC. |
| POST | `/v1/solana/tx-explain` | $0.05 | Explain a Solana transaction: labeled programs, token/SOL movements, plain-English summary. Base or Solana USDC. |

Prices and JSON Schemas for every endpoint are always authoritative at `GET /catalog` — treat the table above as a snapshot, not the source of truth. The three `solana/*` endpoints accept payment on **either** Base or Solana mainnet USDC — pick whichever network your wallet holds funds on.

## Paying via x402 (3 representative examples)

x402 is a two-step HTTP flow: your first request gets `402 Payment Required` with payment terms in the `PAYMENT-REQUIRED` header (base64-encoded JSON); your client signs an EIP-3009 USDC transfer authorization and retries with an `X-PAYMENT` header. Most agents use an x402-aware HTTP client (`@x402/fetch` for JS, `x402` for Python) rather than raw curl, but the underlying HTTP is:

**1. Wallet safety check**
```bash
# Step 1: unpaid request — returns 402 with payment terms
curl -i -X POST https://agentforge-taupe.vercel.app/v1/wallet-safety \
  -H "Content-Type: application/json" \
  -d '{"walletAddress":"0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9","chain":"ethereum"}'

# Step 2: retry with X-PAYMENT header (built by your x402 client from
# the PAYMENT-REQUIRED response header above)
curl -X POST https://agentforge-taupe.vercel.app/v1/wallet-safety \
  -H "Content-Type: application/json" \
  -H "X-PAYMENT: <base64 payment payload from your x402 client>" \
  -d '{"walletAddress":"0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9","chain":"ethereum"}'
```

**2. Token risk / rug check**
```bash
curl -X POST https://agentforge-taupe.vercel.app/v1/token-risk-metrics \
  -H "Content-Type: application/json" \
  -H "X-PAYMENT: <base64 payment payload>" \
  -d '{"address":"0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9","chain":"ethereum"}'
```

**3. Decode a transaction**
```bash
curl -X POST https://agentforge-taupe.vercel.app/v1/tx-decode \
  -H "Content-Type: application/json" \
  -H "X-PAYMENT: <base64 payment payload>" \
  -d '{"txHash":"0xb7219192723c6a9ee77cd56ffdd28805d6177f76ffe0d34260bb5dc76abf19cf","chain":"ethereum"}'
```

Minimal JS client (recommended over raw curl):
```js
import { wrapFetchWithPayment } from '@x402/fetch';
const paidFetch = wrapFetchWithPayment(fetch, x402Client); // handles the 402 -> X-PAYMENT retry for you
const res = await paidFetch('https://agentforge-taupe.vercel.app/v1/wallet-safety', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ walletAddress: '0x...', chain: 'ethereum' }),
});
```

## Notes for buying agents

- All 19 endpoints declare bazaar discovery metadata with example inputs/outputs — use `GET /catalog` or the CDP x402 Bazaar discovery index to pull JSON Schemas programmatically rather than hardcoding request shapes from this file.
- Every paid response includes a `relatedServices` field suggesting other AgentForge endpoints relevant to the same wallet/token/contract — follow these to chain checks (e.g. `token-risk-metrics` → `tx-decode` for the token's deploy transaction).
- EVM endpoints: network is Base mainnet, asset is USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`).
- Solana endpoints (`solana/tx-explain`, `solana/tx-simulate`, `solana/token-risk-scan`): accept USDC on **either** Base or Solana mainnet (`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`) — the 402 response lists both `accepts` entries, pick the one matching your wallet.
