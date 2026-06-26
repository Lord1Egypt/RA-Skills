---
name: floor-otc
description: Trustless token swaps for AI agents on Base. Two paths — relay agent-signed orders to CoW Protocol for instant batch-auction settlement (zero capital, MEV protected), or create a 1:1 on-chain escrow for human OTC. Both atomic, no middleman.
version: 1.3.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🟩"
    homepage: https://floor-otc.vercel.app
---

# FLOOR OTC — Token Swaps for the Agent Economy

FLOOR OTC routes token swaps two ways on Base mainnet:

1. **CoW Protocol relay** (recommended for agents) — the calling agent signs an EIP-712 order locally, FLOOR forwards it to CoW's batch auction. Solvers fill against all of Base's liquidity in ~30s. MEV-protected, no slippage to pool, no escrow custody. FLOOR earns 25 bps via CoW's `partnerFee` mechanism, encoded in the appData the trader signs.
2. **FloorEscrowV2** (for humans / 1:1 OTC) — both parties deposit into an on-chain escrow contract, atomic settlement, 25 bps protocol fee.

ERC-8004 Agent #31596 on Base Mainnet.

## Quick Start

### Get a quote (REST)

```bash
curl -s "https://floor-a2a-production.up.railway.app/api/quote?from=USDC&to=WETH&amount=1000" | jq
```

### Get a quote (JSON-RPC / A2A)

```bash
curl -s -X POST https://floor-a2a-production.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tasks/send","params":{"skill_id":"get_quote","arguments":{"from_token":"USDC","to_token":"WETH","amount":1000}},"id":1}'
```

### Get live prices

```bash
curl -s "https://floor-a2a-production.up.railway.app/api/prices" | jq
```

### Execute a trade (creates on-chain escrow)

```bash
curl -s -X POST https://floor-a2a-production.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tasks/send","params":{"skill_id":"execute_trade","arguments":{"from_token":"USDC","to_token":"DAI","amount":1000}},"id":1}'
```

### Check trade status

```bash
curl -s -X POST https://floor-a2a-production.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tasks/send","params":{"skill_id":"check_trade","arguments":{"trade_id":"0xYOUR_TRADE_ID"}},"id":1}'
```

### Prepare a CoW order (agent-signed, FLOOR-relayed)

Step 1 — ask FLOOR to build the order:

```bash
curl -s -X POST https://floor-a2a-production.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tasks/send","params":{"skill_id":"prepare_trade","arguments":{"sell_token":"USDC","buy_token":"WETH","sell_amount":1000,"trader_address":"0xYourAgentWallet"}},"id":1}'
```

You get back `typed_data` (EIP-712 domain + types + message), `app_data` (FLOOR's partnerFee doc + hash), `quote_summary`, `preflight` (balance + relayer allowance), and `relayer.approve_calldata` if you still need to approve the GPv2VaultRelayer.

Step 2 — sign locally with your wallet:

```js
const signature = await wallet.signTypedData(
  typed_data.domain,
  typed_data.types,
  typed_data.message
);
```

Step 3 — submit through FLOOR:

```bash
curl -s -X POST https://floor-a2a-production.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tasks/send","params":{"skill_id":"submit_signed_trade","arguments":{"order":{...},"signature":"0x...","trader_address":"0xYourAgentWallet"}},"id":1}'
```

Returns `order_uid` + `explorer_url`. Track the fill at `https://explorer.cow.fi/base/orders/{order_uid}`.

### Check a CoW order

```bash
curl -s -X POST https://floor-a2a-production.up.railway.app/a2a \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tasks/send","params":{"skill_id":"check_cow_order","arguments":{"order_uid":"0xYOUR_ORDER_UID"}},"id":1}'
```

## Supported Tokens (Base Mainnet)

| Token | Address |
|-------|---------|
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| USDbC | `0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6Ca` |
| DAI | `0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb` |
| WETH | `0x4200000000000000000000000000000000000006` |

Additional tokens supported for quotes only: ETH, BTC, WBTC, UNI, LINK, AAVE.

## Pricing

Quotes are free at real CoinGecko market rates — zero spread. A 25 bps (0.25%) protocol fee is collected on every fill:
- **CoW relay:** routed by solvers via CoW's `partnerFee` mechanism in the appData the trader signs.
- **FloorEscrowV2:** deducted from each side on settlement, immutable in the contract — no admin keys.

## Skills

**CoW relay (recommended for agents):**
- **prepare_trade** — Build a CoW order for the calling agent's wallet to sign. Returns EIP-712 typed data, FLOOR appData (with 25 bps partner fee baked in), and a preflight check on the trader's balance + relayer allowance. FLOOR never custodies funds.
- **submit_signed_trade** — Forward a trader-signed CoW order to the CoW order book on Base. FLOOR validates the signature locally, then relays. Returns the orderUid and explorer URL. Solvers fill in the next batch (~30s).
- **check_cow_order** — Look up a CoW order by its 56-byte orderUid. Returns open / fulfilled / cancelled / expired plus executed amounts.

**FloorEscrowV2 (1:1 OTC, for humans via web UI):**
- **execute_trade** — Create on-chain escrow on Base (both parties deposit, atomic settlement)
- **check_trade** — Check escrow status by trade ID

**Quotes & data:**
- **get_quote** — Live swap quote at real market rates, zero spread
- **get_prices** — Current token prices

## Endpoints

- Agent Card: `https://floor-a2a-production.up.railway.app/.well-known/agent.json`
- A2A (JSON-RPC): `POST https://floor-a2a-production.up.railway.app/a2a`
- REST Quote: `GET https://floor-a2a-production.up.railway.app/api/quote?from=USDC&to=WETH&amount=1000`
- REST Prices: `GET https://floor-a2a-production.up.railway.app/api/prices`
- MCP (SSE): `https://zesty-solace-production-13de.up.railway.app/sse`
- Health: `GET https://floor-a2a-production.up.railway.app/health`

## On-Chain

- **Network:** Base Mainnet (chain ID 8453)
- **Escrow Contract (V2):** `0x9EC9d882C93F52621CBD0d146D3F2e0929E53AA7` (verified on Basescan)
- **CoW Settlement:** `0x9008D19f58AAbD9eD0D60971565AA8510560ab41`
- **CoW VaultRelayer (approve sell tokens here):** `0xC92E8bdf79f0507f65a392b0ab4667716BFE0110`
- **Protocol Fee:** 25 bps (0.25%) — both venues
- **Identity Registry:** `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`
- **Agent ID:** 31596

No authentication required. Quotes are free.
