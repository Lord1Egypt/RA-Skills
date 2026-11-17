---
name: galleon-coinbase-agentkit-readiness
description: Inspect Coinbase CDP and AgentKit wallet configuration, verify an existing account with read-only tools, and inventory exposed actions before protocol use. Use when an agent cannot find its wallet, uses the wrong Base network, or needs a scoped Coinbase capability report without creating accounts or signing.
license: MIT
compatibility: Portable instructions; optional offline helper uses Bun. Live recipes require an existing official provider or public HTTPS access.
metadata:
  author: Galleon Labs
  version: "0.4.1"
---

# Coinbase AgentKit readiness

Find the exact missing capability between “AgentKit installed” and “this existing account can perform the requested task.” Return a usable capability report without invoking a transaction or provisioning a wallet.

## Procedure

1. Identify the user's product: CDP API Key Wallet, AgentKit wallet provider, or email-authenticated Agentic Wallet (`awal`). They have different authentication and lifecycle behavior. A Coinbase exchange API key is not automatically a CDP wallet credential.
2. Inspect installed package versions and the existing application's selected provider, network ID, account address and exposed action list. Use [the inspection recipe](references/inspection.md). Reuse its environment without displaying values. Public market research does not require a wallet.
3. Match the expected account to its owner and the requested network. Distinguish Base mainnet `base` / 8453 from `base-sepolia` / 84532. A smart account and its owner EOA are different identities; a funded owner does not prove the smart account can pay gas.
4. Test only the reads required for the task: public chain identity, head timestamp and existing account balance; optionally authenticated retrieval of the exact existing CDP account. Record what was actually tested. Missing signer credentials do not block a public balance read.
5. Inventory action providers. Separate reads, signing, transfers, swaps, approvals and paid x402 calls. Inspect schemas/source; never infer read-only behavior from a friendly action name. Expose only the operations needed by the current application. Keep broader financial authority behind the application's explicit policy and confirmation mechanism.
6. Return the report below. If the blocker is an absent key, wrong network, unsupported action or account mismatch, name that blocker and the smallest correction. Do not “repair” readiness by creating or funding an account.

## Evidence report

```text
Product / SDK versions:
Runtime / provider:
Expected network and account:
Observed network and account:
Credential presence: set / missing (never values)
Public read: chain, block number, head time, balance and observation time
Authenticated account lookup: passed / failed / untested
Exposed action names and classifications:
Signing authority: separately configured / unknown
Next task readiness: ready for [specific read] | blocked by [specific gap]
```

## Worked cases

- “My Base balance is zero in AgentKit.” Existing provider says `base-sepolia`, user means mainnet. Report the mismatch first; use an already configured mainnet read tool for the requested balance if available. Do not fund testnet or migrate assets.
- “Is CDP ready? Keys are set.” Presence establishes local configuration only. Retrieve the expected existing account and run the scoped public read before claiming authenticated readiness. If the wallet secret is missing, public reads can still work while signing remains unverified.
- “Audit what my agent can do.” An exposed transfer action plus a balance reader means the agent has a write surface. Report exact action names and gating; do not execute a transfer as a test.

The deliverable is the scoped readiness report and, for an engineering task, a reviewable configuration correction. A tool inventory is not financial authorization. See [dated official sources](references/sources.md).
