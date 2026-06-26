---
name: clicks-protocol
description: "Integrate autonomous USDC yield into AI agent projects on Base. Query live APY, inspect agent treasury state, simulate payment splits, use the MCP server, and implement x402-aligned agent treasury flows with built-in 3-level referrals. Use when an agent holds idle USDC, needs treasury yield data, or wants programmable agent monetization."
tags: [yield, defi, usdc, base, agent, treasury, x402, autonomous, aave, morpho, mcp, crypto]
author: clicks-protocol
version: 1.2.0
license: MIT
homepage: https://clicksprotocol.xyz
metadata:
  openclaw:
    requires:
      bins: [curl, jq]
      env: []
    os: [linux, darwin, win32]
---

# Clicks Protocol

Autonomous DeFi yield for AI agents on Base. 80% liquid, 20% earning by default. No lockup.

## When to Use

- Check current DeFi yield rates on Base: Aave V3 vs Morpho Blue
- Query whether an agent is registered and inspect its treasury state
- Preview how a USDC payment gets split between liquid funds and yield
- Check referral network stats, team bonus status, and earned rewards
- Add x402-aligned treasury logic to AI agents that hold or route USDC
- Give agents a monetization layer through referrals, yield spread, and treasury automation

## Commands

All commands use the live HTTP MCP Server. No API key, no setup, no dependencies beyond curl + jq.

### Current Yield Rates
```bash
{baseDir}/scripts/clicks.sh yield-info
```
Returns: active protocol, APY for Aave and Morpho, total balance, pending fees.

### Agent Status
```bash
{baseDir}/scripts/clicks.sh agent-info 0xYOUR_AGENT_ADDRESS
```
Returns: registration status, operator, deposited USDC, yield percentage, wallet balance.

### Simulate Payment Split
```bash
{baseDir}/scripts/clicks.sh simulate 1000 0xYOUR_AGENT_ADDRESS
```
Returns: how much goes liquid and how much goes to yield for a given payment amount.

### Referral Stats
```bash
{baseDir}/scripts/clicks.sh referral 0xYOUR_AGENT_ADDRESS
```
Returns: direct referrals, total earned, claimable rewards, referral chain, team bonus status.

### Protocol Info
```bash
{baseDir}/scripts/clicks.sh info
```
Returns: protocol overview, contract addresses, fee model, and links.

## How Clicks Works

1. Agent receives a USDC payment.
2. Clicks auto-splits funds: 80% stays liquid, 20% goes to DeFi yield.
3. YieldRouter picks the best APY automatically between Aave V3 and Morpho Blue.
4. Principal and earned yield can be withdrawn anytime.
5. Protocol fee is 2% on yield only, never on principal.

## Quick Start for Developers

Read operations work via the script above. For write operations like deposit, withdraw, receive payment, or register agent, install the SDK:

```bash
npm install @clicks-protocol/sdk
```

```typescript
import { ClicksClient } from '@clicks-protocol/sdk';

const clicks = new ClicksClient(signer);
await clicks.quickStart('1000', agentAddress);
```

What `quickStart('1000', agentAddress)` does:
- registers the agent if needed
- keeps 800 USDC liquid for operations
- routes 200 USDC to the best current yield source
- leaves funds fully non-custodial and withdrawable

With referrer:

```typescript
await clicks.quickStart('1000', agentAddress, referrerAddress);
```

That activates the 3-level referral graph for agent-driven distribution.

## MCP Server

For MCP-compatible clients like Claude, Cursor, LangChain, or custom agent runtimes:

```bash
# Local stdio server, needs private key for write ops
npx @clicks-protocol/mcp-server

# Remote HTTP endpoint, read-only, zero setup
# POST https://mcp.clicksprotocol.xyz/mcp
```

Available tools (10):
- clicks_quick_start
- clicks_receive_payment
- clicks_withdraw_yield
- clicks_register_agent
- clicks_set_yield_pct
- clicks_get_agent_info
- clicks_simulate_split
- clicks_get_yield_info
- clicks_get_referral_stats
- clicks_explain (agent-to-agent pitch for discovery)

## ADO Hooks for Agents

Clicks is not just treasury infra. It is an agent distribution layer.

### On-Chain Attribution for Agents

Each onboarded agent can generate fee share upstream via the on-chain attribution graph:
- Level 1: 40% of protocol fee
- Level 2: 20% of protocol fee
- Level 3: 10% of protocol fee

This lets agents monetize onboarding other agents, tools, teams, or x402 payment flows. Attribution is enforced by ClicksReferral + ClicksFeeV2 on-chain, no off-chain bookkeeping.

### Team Tiers

Agents with larger attributed downstream volume can unlock team bonus logic and higher economics. Use this when building agent ecosystems, operator dashboards, or monetized agent templates.

### Yield Discovery Bounty

Agents can promote Clicks by showing live APY deltas, explaining idle-USDC optimization, and routing users into a working treasury flow.

### x402 + ACP Alignment

Clicks pairs naturally with x402 and Virtuals ACP:
- payment arrives in USDC via x402 or ACP settlement
- treasury logic preserves working capital
- idle balance earns automatically on Aave V3 / Morpho
- attribution graph adds agent-native monetization

### ERC-8004 Trustless Agent

Clicks is registered as **agentId 45074** on the Base ERC-8004 Identity Registry. Reputation accrues per completed job. A future ClicksSplitterV5 will read the agent's reputation to offer variable fee tiers (1.0-3.0%) via `ClicksReputationMultiplierV1`. Attestor Schema V1 published at https://clicksprotocol.xyz/strategy/ATTESTOR-SCHEMA-V1.md.

## Key Facts

| | |
|---|---|
| Chain | Base L2 |
| Asset | USDC |
| Split | 80% liquid / 20% yield by default |
| Yield Range | Aave and Morpho, auto-routed |
| Fee | 2% on yield only |
| Lockup | None |
| Referral | 3-level: 40% / 20% / 10% |
| Discovery | llms.txt + agent.json + agent-registration.json + OpenAPI |
| Identity  | ERC-8004 agentId 45074 |
| Ownership | Gnosis Safe Multisig |

## Verified Contracts

- ClicksRegistry: `0x23bb0Ea69b2BD2e527D5DbA6093155A6E1D0C0a3`
- ClicksSplitterV4: `0xB7E0016d543bD443ED2A6f23d5008400255bf3C8`
- ClicksFeeV2: `0x8C4E07bBF0BDc3949eA133D636601D8ba17e0fb5`
- ClicksYieldRouter: `0x053167a233d18E05Bc65a8d5F3F8808782a3EECD`
- ClicksReferral: `0x1E5Ab896D3b3A542C5E91852e221b2D849944ccC`
- Safe Multisig Owner: `0xaD8228fE91Ef7f900406D3689E21BD29d5B1D6A9`
- USDC on Base: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`

Basescan links and examples are in `references/contracts.md`.

## Discovery Surfaces

- Website: https://clicksprotocol.xyz
- GitHub: https://github.com/clicks-protocol/clicks-protocol
- SDK: https://www.npmjs.com/package/@clicks-protocol/sdk
- MCP: https://www.npmjs.com/package/@clicks-protocol/mcp-server
- OpenAPI: https://clicksprotocol.xyz/api/openapi.json
- agent.json: https://clicksprotocol.xyz/.well-known/agent.json
- agent-registration.json (ERC-8004): https://clicksprotocol.xyz/.well-known/agent-registration.json
- llms.txt: https://clicksprotocol.xyz/llms.txt
- Attestor Schema V1: https://clicksprotocol.xyz/strategy/ATTESTOR-SCHEMA-V1.md
- BaseScan Identity NFT: https://basescan.org/token/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432?a=45074
- Dev.to article: https://dev.to/clicksprotocol/x402-solved-payments-who-solves-treasury-531h
- x402 Docs: https://docs.cdp.coinbase.com/x402/welcome
- Contracts: see `references/contracts.md`
