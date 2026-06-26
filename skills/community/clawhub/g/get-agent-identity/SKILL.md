---
name: get-agent-identity
description: >
  Check your agent's on-chain ERC-8004 identity, trust score, and KYA
  credentials. Use when the user wants to see agent identity, check trust
  score, view credentials, or check agent status. Covers "agent ID",
  "trust score", "show my identity", "agent status", "KYA".
user-invocable: true
disable-model-invocation: false
allowed-tools:
  - "Bash(npx agnic@latest status*)"
  - "Bash(npx agnic@latest agent-identity*)"
---

# Getting Agent Identity

Check the user's on-chain ERC-8004 agent identity, trust score, and KYA (Know Your Agent) credentials.

## Authentication

Run `npx agnic@latest status --json` to verify. If not authenticated:
- **Headless (CI/server/agent)**: Set `AGNIC_TOKEN` env var or pass `--token <token>`
- **Interactive (has browser)**: Run `npx agnic@latest auth login`

See the `authenticate-wallet` skill for details.

## Check Agent Identity

```bash
npx agnic@latest agent-identity --json
```

Returns the agent's on-chain identity including:
- **Agent ID** -- The ERC-721 token ID on the ERC-8004 Identity Registry
- **Owner address** -- The wallet that owns the agent NFT
- **Trust score** -- Reputation score (0-100) based on transaction history
- **Categories** -- Authorized action categories (e.g., payment, general, alcohol)
- **Status** -- Whether the agent is active or suspended

## What is ERC-8004?

ERC-8004 ("Trustless Agents") is an Ethereum standard that gives AI agents:

| Feature              | Description                                                          |
| -------------------- | -------------------------------------------------------------------- |
| **On-chain identity**| An ERC-721 NFT representing the agent on the Identity Registry       |
| **Reputation score** | Trust score (0-100) based on on-chain transaction history            |
| **KYA credentials**  | SD-JWT verifiable credentials for identity verification              |
| **Delegation**       | Spending limits and category permissions via KYA delegation credentials |

## Contract Addresses

| Contract          | Network      | Address                                      |
| ----------------- | ------------ | -------------------------------------------- |
| Identity Registry | Base Mainnet | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| Identity Registry | Base Sepolia | `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| Reputation        | Base Mainnet | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` |
| Reputation        | Base Sepolia | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |

## Expected Output

```json
{
  "agentId": 373,
  "ownerAddress": "0x046906b3cd9d73bf85eb01d795d333b364b75842",
  "status": "active",
  "registeredAt": "2024-12-15T10:30:00Z",
  "trustScore": 85,
  "categories": ["payment", "general"],
  "hasDelegation": true
}
```

## Prerequisites

- Must be authenticated (`npx agnic@latest status` to check)
- Agent identity is automatically created during Agnic sign-up

## Error Handling

Common errors:

- "Not authenticated" -- Run `npx agnic@latest auth login` or set `AGNIC_TOKEN`
- "No agent identity found" -- The user may not have an agent registered; create one at [app.agnic.ai](https://app.agnic.ai)
- "Agent suspended" -- The agent's delegation may have been revoked; contact support
