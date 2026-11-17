---
name: galleon-defi-yield
description: "Use when comparing savings and strategy vaults, planning deposits or exits, or evaluating principal/yield tokens and maturity across Pendle, Yearn, Spark, Morpho, Euler and Ethena."
license: MIT
metadata:
  version: "0.2.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# DeFi yield positions

Use official builders and data sources. This skill adds a common decision process for vault shares, savings tokens and tokenized yield; it is not a yield optimizer with trading authority.

Read [providers](references/providers.md) for the chosen product and version. Read [workflows](references/workflows.md) for vault mechanics, maturity/exit plans and evaluation cases.

## Start with the requested task

Read [task examples and user configuration](references/task-examples.md) for a completed example and recovery path. Apply only the workflow stages needed by the current request. Reuse supplied preferences and compatible tools; ask only for missing terms that affect this task. Public explanation or comparison does not require transaction fields. Keep any existing authorization within its exact scope.

## Workflow

1. Resolve chain, contract/version, underlying asset, share token, accounting asset, owner and recipient. For Pendle resolve SY, PT, YT, market and exact maturity together. A familiar token symbol does not prove a vault's origin or supported redemption route.
2. Read current assets/shares, conversion and preview values, owner-specific limits, liquidity, fees, queue/cooldown status, strategy allocation, curator/admin powers and rate provenance. Keep APY observation period, compounding, fees, rewards and points separate. Missing yield is unknown, not zero; historical rates are not guaranteed future returns.
3. Compare net outcomes over the user's actual horizon. Distinguish assets from shares and accounting principal from raw receipt tokens. A vault's assets under management are not immediately withdrawable cash. Show early-exit price risk, maturity, underlying loss exposure and each claim step.
4. Prepare the selected unsigned deposit, mint, withdrawal, redemption, claim or market trade with an official interface. Set concrete slippage/minimum-output and loss tolerances appropriate to that interface; a loss tolerance is not necessarily a price-slippage tolerance. Review approvals, recipients, shares/assets, deadlines and final simulation.
5. Respect existing authorization, obtaining any missing approval for the concrete transaction plan. Research, comparison and simulation do not authorize signatures, allowances, asset movement, borrowing or automatic compounding. Use the selected signer without exposing credentials.
6. Track prepared, authorized, signed, submitted, receipt-confirmed and position-reconciled states separately. For queued exits add requested, claimable and claimed. For maturity distinguish redeemable principal from received output. Investigate existing transaction hashes and request IDs before retrying; an indexer's lag is not failure.

## Output

Show asset identity, observation block/time, APY methodology, underlying/strategy and governance exposure, net horizon comparison, liquidity and exit route, explicit transaction limits and approval scope, and what was actually verified. Label official documentation separately from tooling tested in the current environment.

Do not connect/install services or enable broad tools automatically. Use official provider skills when building an integration instead of copying their SDK logic. Borrowing against a vault or PT introduces lending risk and requires a separate position analysis; Boros margin trades are derivatives, not passive vault deposits.

## Protocol-specific procedures

For a named protocol task, prefer its focused skill when installed:

- `galleon-pendle-maturity`: PT/YT maturity, accounting assets and exit comparisons.
- `galleon-vault-exit`: ERC4626 previews versus limits and asynchronous redemption.

This existing skill remains usable on its own for cross-protocol comparisons. Do not require another pack to complete its workflow.
