---
name: galleon-defi-lending
description: "Use when researching lending markets, planning supply, borrow, repay or withdrawals, or monitoring liquidation risk across Aave, Morpho, Compound, Euler and Spark."
license: MIT
metadata:
  version: "0.3.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# DeFi lending

Use the provider's maintained SDK, API, contracts or documented MCP for the selected deployment. This skill supplies operational judgment; it does not supply a wallet, signer, runtime adapter or authority to transact.

Read [providers](references/providers.md) for the chosen protocol and version. Read [workflows](references/workflows.md) for position planning, monitoring and evaluation cases. Keep unrelated provider manuals out of context.

## Start with the requested task

Read [task examples and user configuration](references/task-examples.md) for a completed example and recovery path. Apply only the workflow stages needed by the current request. Reuse supplied preferences and compatible tools; ask only for missing terms that affect this task. Public explanation or comparison does not require transaction fields. Keep any existing authorization within its exact scope.

## Workflow

1. Identify the requested operation, chain ID, protocol version, market/pool/spoke or vault, collateral and debt token addresses, account/subaccount, amount and recipient. Resolve deployments from official sources. A token ticker or familiar frontend name is insufficient.
2. Read current balances, accrued debt, oracle values and units, collateral configuration, liquidity, caps, rates, fees and pause state. Record block/time and data provenance. Distinguish indexed discovery from fresh transaction state; missing or stale risk data is a blocker for execution planning.
3. Explain the proposed post-state: supplied assets, debt, withdrawable liquidity, interest exposure and distance to liquidation. Stress collateral and debt prices separately. Compare variable rates, fixed-term quotes, reward assumptions and rollover costs on a common basis. A maximum borrow amount is not a recommended amount.
4. For a requested transaction, use the official builder to prepare the complete unsigned sequence, including approvals/permits and any batch or flash-loan legs. Decode spender, amounts, recipients, chain, expiry and authority. Simulate the final sequence against current state. An error warning or unknown permission must be resolved before presenting it for signing.
5. Preserve the user's existing authorization scope. Research or preparation alone does not authorize signatures, debt, token allowances, delegation or transfers. Obtain any missing authorization for the concrete plan, then use the user's chosen signer; never request seed phrases or expose keys in prompts or logs.
6. Track separately: prepared, authorized, signed, submitted, confirmed, and reconciled. A signature, transaction hash, successful approval, or indexed position alone is not proof that all intended legs completed. Verify receipt and onchain balances/debt, then wait for indexer reconciliation. On timeout, inspect the known hash/nonce before considering a retry.

## Decision record

Return the target identity and block/time, tool/version actually used, rate basis and costs, pre/post-position risk, approvals and signer scope, simulation result, transaction state, and unresolved questions. Label documentation-only guidance or untested tooling honestly. Do not install/connect an MCP, enable broad tools, or open a leveraged position merely because a skill lists it.

Prefer adding collateral or repaying within authorized limits over assuming an unapproved refinance, bridge or asset sale. Monitoring alerts must state what changed and what action is proposed; scheduling and automated execution require their own explicit scope.

## Protocol-specific procedures

For a named protocol task, prefer its focused skill when installed:

- `galleon-aave-position`: Aave V3 health factor, eMode, isolation and stress sizing.
- `galleon-morpho-market`: Morpho market identity, oracle and vault exit diligence.
- `galleon-compound-borrow`: Comet base borrowing, minimum debt and dual collateral factors.

This existing skill remains usable on its own for cross-protocol comparisons. Do not require another pack to complete its workflow.

For an identified Aave V4 Hub/Spoke operation, prefer `galleon-aave-v4` when installed. V3 Pool operations continue to use `galleon-aave-position`. Each remains independently usable.
