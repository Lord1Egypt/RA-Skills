---
name: clicks-protocol
description: "Inspect and simulate Clicks Protocol settlement routing for AI agents on Base. Use read-only MCP calls for settlement state, split previews, optional yield routing, and attribution stats."
tags: [settlement, router, treasury, usdc, base, agent, x402, mcp, commerce, defi, aave, morpho]
author: clicks-protocol
version: 1.2.7
license: MIT-0
homepage: https://clicksprotocol.xyz
metadata:
  openclaw:
    requires:
      bins: [curl, jq]
      env: []
    os: [linux, darwin, win32]
---

# Clicks Protocol

Agent commerce settlement routing for AI agents on Base. Use this skill to inspect treasury state, preview settlement policy, and plan attribution flows before any on-chain action.

This ClawHub skill is published under MIT-0. The Clicks Protocol contracts, SDKs, docs, and packages keep their own repository-level licenses.

## Safety Boundary

This ClawHub skill is read-only by default.

- The bundled script only calls read-only MCP tools.
- It never asks for, stores, or handles a private key.
- It never signs or broadcasts transactions.
- It never performs state-changing treasury actions.
- Treat all payment, yield, and attribution outputs as previews or status checks unless a human operator separately signs an on-chain transaction.

If you build write flows with the SDK or local MCP server, require explicit human approval for every transaction. Show the chain, contract, method, asset, amount, recipient, fees, and expected state change before signing. Never auto-submit treasury or USDC-moving actions from an autonomous agent loop.

## When to Use

- Query whether an agent is registered and inspect its settlement state
- Preview how incoming USDC is split between working capital and the configured treasury route
- Inspect the optional yield backends used by the current live contracts
- Check explicit attribution stats and earned rewards
- Plan post-payment policy and routing for agents that receive USDC

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

## Current live flow

1. An agent receives USDC through a separate payment flow.
2. The operator submits that revenue to Clicks for settlement. The current default keeps 80% liquid and routes 20% to optional yield.
3. YieldRouter picks the active backend between Aave V3 and Morpho Blue.
4. Operator-controlled withdrawal stays outside this read-only ClawHub skill.
5. Protocol fee is 2% on yield only, never on principal.

## Developer Integration

Read operations work via the script above. For application code, install the SDK and start with read-only inspection and simulation:

```bash
npm install @clicks-protocol/sdk
```

```typescript
import { ClicksClient } from '@clicks-protocol/sdk';

const clicks = new ClicksClient(provider);
await clicks.getAgentInfo(agentAddress);
await clicks.simulateSplit('1000', agentAddress);
await clicks.getYieldInfo();
```

Write operations are available in the SDK for operators who control their own signer, but they are outside this ClawHub skill's default behavior. Before calling any method that changes on-chain state or touches USDC, get explicit human approval and show the exact transaction details.

Referral attribution should be approved by the agent operator before any state-changing transaction:

```typescript
const deadline = BigInt(Math.floor(Date.now() / 1000) + 3600);
const signature = await clicks.signReferralApproval(agentAddress, referrerAddress, deadline);
// Submit a state-changing transaction only after explicit human approval
// of chain, contract, asset, amount, and referrer.
```

Real attribution should use an explicit signed referral approval. Avoid implicit referral parameters in autonomous agent loops.

## MCP Server

For MCP-compatible clients like Claude, Cursor, LangChain, or custom agent runtimes:

```bash
# Local stdio server. Use read-only tools in agent loops.
npx @clicks-protocol/mcp-server

# Remote HTTP endpoint, read-only, zero setup
# POST https://mcp.clicksprotocol.xyz/mcp
```

Read-only tools:
- clicks_get_agent_info
- clicks_simulate_split
- clicks_get_yield_info
- clicks_get_referral_stats
- clicks_explain (agent-to-agent pitch for discovery)

The local MCP package also includes operator tools for state-changing flows. Those require a signer, a separate integration, and explicit human approval. Do not expose them to autonomous agent loops.

## Attribution for agents

### On-Chain Attribution for Agents

Each onboarded agent can generate fee share upstream via the on-chain attribution graph:
- Level 1: 40% of protocol fee
- Level 2: 20% of protocol fee
- Level 3: 10% of protocol fee

This lets an agent receive a defined share of protocol fees generated by agents it onboarded. ClicksReferral and ClicksFeeV2 enforce that relationship on-chain.

### Team Tiers

Agents with larger attributed downstream volume can unlock team bonus logic and higher economics. Use this when building agent ecosystems, operator dashboards, or monetized agent templates.

### x402 and ACP boundary

x402 and ACP can execute payments. Clicks starts after payment execution and applies settlement policy to received USDC. The dedicated x402 adapter is planned, not released. Do not treat the current skill as automatic x402 detection or verification.

### ERC-8004 Trustless Agent

Clicks is registered as **agentId 45074** on the Base ERC-8004 Identity Registry. One Schema V1 feedback record is live. A future ClicksSplitterV5 may read reputation to offer variable fee tiers, but V5 is a repository prototype and is not deployed. Attestor Schema V1 is published at https://clicksprotocol.xyz/strategy/ATTESTOR-SCHEMA-V1.md.

## Key Facts

| | |
|---|---|
| Chain | Base L2 |
| Asset | USDC |
| Current default split | 80% liquid / 20% optional yield route |
| Settlement scope | Post-payment policy and routing |
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
