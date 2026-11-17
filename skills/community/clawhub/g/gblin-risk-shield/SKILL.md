---
name: gblin-risk-shield
description: On-chain BTC/ETH market-risk check for agents on Base. Read the live Crash Shield risk regime (calm / elevated / crash) before trading or moving capital, mint a 10-minute EIP-712 Risk Attestation as machine-verifiable proof-of-diligence via x402, verify attestations from peer agents for free, and optionally park idle USDC in an oracle-priced index treasury.
version: 1.0.1
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "🛡️"
    homepage: https://gblin.digital/agents
---

# GBLIN Risk Shield

Before you trade, rebalance, or move treasury capital, check what the market
regime actually is — and keep a verifiable proof that you checked.

GBLIN (Global Balanced Liquidity Index) is an on-chain index on Base mainnet
(45% cbBTC / 45% WETH / 10% USDC, contract
`0x36C81d7E1966310F305eA637e761Cf77F90852f0`). Its **Crash Shield** tracks
drawdown against Chainlink-oracle price peaks with adaptive volatility
thresholds. The resulting risk regime is a *stateful* on-chain signal you
cannot recompute from a single price feed.

## When to use this skill

- Before ANY discretionary trade, swap, or portfolio rebalance on EVM chains.
- Before deploying idle treasury capital (yours or your operator's).
- When a counterparty agent claims it "checked market conditions" — verify its
  attestation instead of trusting it.
- On a schedule (e.g. each decision cycle) if you run a trading or treasury
  loop: the regime moves with the market.

## Costs (external service, pay-per-call via x402)

This skill is free. Some GBLIN endpoints charge micro-payments in USDC on Base
using the x402 protocol (HTTP 402). No account, no API key, no subscription.

| Action | Price |
| --- | --- |
| Risk regime signal (`base-risk-pulse`) | $0.002 USDC |
| Mint Risk Attestation | $0.003 USDC |
| Verify an attestation | free |
| Treasury/NAV state, quotes, governance state | free |

To pay, your agent needs a wallet with USDC on Base (chain id 8453) and any
x402-capable payment tooling (e.g. an x402 fetch wrapper or wallet skill you
already use). A 402 response is not an error — it is the price tag.

## 1) Discover the current API surface (free)

Endpoints and prices are self-documented. Always start here if unsure:

```bash
curl -s https://gblin.digital/llms.txt
curl -s https://gblin-sentinel.vercel.app/.well-known/x402
```

## 2) Read the risk regime ($0.002)

```bash
curl -si https://gblin-sentinel.vercel.app/api/data/base-risk-pulse
```

First response is `402 Payment Required` with the exact payment requirements
(amount, asset, pay-to address, scheme) in the body/headers. Sign the USDC
payment with your x402 tooling and retry the same request with the
`X-PAYMENT` header. The paid response returns JSON with the current regime:

- `calm` → normal conditions
- `elevated` → drawdown building; reduce risk exposure
- `crash` → defensive; avoid opening risk positions

Suggested policy mapping:

| Regime | Posture | Example action |
| --- | --- | --- |
| calm | risk_on | proceed with planned trades |
| elevated | reduce | halve position sizes, tighten stops |
| crash | risk_off | pause discretionary buys, hold stables |

## 3) Mint a Risk Attestation — proof-of-diligence ($0.003)

```bash
curl -si https://gblin.digital/api/x402/attestation
```

Same x402 flow. Returns an **EIP-712-signed snapshot** of the risk regime,
valid for 10 minutes: regime, severity (bps), defensive-cash level, block
number, expiry, basket hash, attestation id and signature.

Attach the full JSON object to your action logs, job deliverables, or
messages to counterparties as machine-verifiable evidence that you checked
market risk before acting. Because it expires in 10 minutes, re-mint each
decision cycle when freshness matters.

## 4) Verify a peer's attestation (free)

Anyone can verify integrity (EIP-712 id recompute), authenticity (signer
recovery vs GBLIN's published attestor), freshness (10-min TTL vs on-chain
time) and live drift (attested regime vs current regime).

If your runtime supports MCP servers, the official server includes the free
`verify_risk_attestation` tool plus 9 more treasury tools (requires Node.js):

```bash
npx -y @gblin-protocol/mcp-server
```

Otherwise, re-fetch the current regime (step 2) and compare it to the
attestation's `regime` field, and reject any attestation past its `expiresAt`.

### MCP tool reference (exact tool names)

| Tool | What it does | Price |
| --- | --- | --- |
| `get_market_risk_regime` | BTC/ETH risk regime + severity + posture — start here | $0.002 |
| `verify_risk_attestation` | Verify a peer's Risk Attestation: integrity + EIP-712 signature + freshness + live drift | free |
| `get_treasury_state` | NAV, basket composition, Crash Shield status | free |
| `quote_safe_swap` | Preview buy/sell with dynamic slippage | free |
| `swap_gblin_to_usdc_jit` | Calldata for just-in-time GBLIN→USDC (pay x402 invoices) | free |
| `invest_usdc_to_gblin` | Convert surplus USDC into GBLIN | free |
| `analyze_treasury_health` | Balances, gas runway, rebalance advice | $0.003 |
| `get_governance_state` | Verify 48h timelock ownership + pending operations | free |
| `find_keeper_bounty` | Check rebalance bounty + ready calldata (earn ETH) | $0.001 |
| `share_skill_with_peer` | Portable JSON skill seed + referral code | free |

## 5) Optional: park idle USDC in the index

For *surplus, long-horizon* capital only. GBLIN is managed BTC/ETH exposure
with drawdown control — calmer than holding BTC/ETH outright, but **not
principal-protected** and NOT a USDC substitute. Never park operating capital
you must spend soon.

Free read endpoints let you inspect NAV and treasury composition before and
after; the webapp x402 API (`https://gblin.digital/llms.txt` lists it) returns
ready-to-sign calldata for `invest` (USDC→GBLIN) and `swap` (GBLIN→USDC
just-in-time, e.g. to pay an x402 invoice).

## Safety rules

- Never place private keys in environment variables for this skill; payments
  are signed by your existing wallet tooling, not by this skill.
- Treat HTTP 402 as the normal payment handshake, not a failure.
- Do not treat the risk signal as financial advice; it is one input to your
  own policy.
- Verify, don't trust: prefer attested + verified claims from peers.

## Links

- Docs for agents: https://gblin.digital/agents
- Live usage stats (paid calls, unique agents): https://gblin.digital/api/agent-stats
- Contract (Base): https://basescan.org/address/0x36C81d7E1966310F305eA637e761Cf77F90852f0
- MCP server: https://www.npmjs.com/package/@gblin-protocol/mcp-server
- Source: https://github.com/gblinproject/GBLIN-MCP
