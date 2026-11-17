---
name: galleon-defi-staking
description: "Use when planning liquid staking, wrapping, restaking, delegation or queued exit claims for Lido, Rocket Pool, EigenLayer and Symbiotic."
license: MIT
metadata:
  version: "0.2.1"
  author: "Andrew Wilkinson and Galleon Labs"
  source: "https://github.com/galleonlabs/crypto-defi-skills"
---

# DeFi staking and restaking

Use maintained official interfaces for the selected deployment. This skill guides liquid-staking and restaking positions, not validator installation or custody. It includes no signer or automatic transaction runner.

Read the selected protocol in [providers](references/providers.md); use [workflows](references/workflows.md) for exits, accounting and evaluation cases.

## Start with the requested task

Read [task examples and user configuration](references/task-examples.md) for a completed example and recovery path. Apply only the workflow stages needed by the current request. Reuse supplied preferences and compatible tools; ask only for missing terms that affect this task. Public explanation or comparison does not require transaction fields. Keep any existing authorization within its exact scope.

## Workflow

1. Identify chain, deployment/version, input token, receipt token, account, recipient and intended action. Separate buying an LST on a market, staking through its issuer, wrapping, restaking, and operating a validator. These create different claims and exit paths.
2. Read the exchange rate or rebasing shares, actual protocol liquidity, deposit limits, fees, pauses, current queue/epoch/cooldown state and pending request ownership. Restaking additionally requires the chosen vault/operator/network, allocation and slashing terms. A points campaign is not a promised monetary return.
3. Compare the complete lifecycle. Show principal denomination, expected receipts, yield methodology, underlying exposure, available exit routes, expected delay and loss/slashing exposure during that delay. Quote a secondary-market exit separately with price impact; never call it a protocol redemption at par.
4. Prepare the requested unsigned operation with official SDK/contracts and simulate it. Review token/spender/amount, recipient, permit deadlines, delegate/operator authority and any withdrawal credentials. Creating an EigenPod or changing validator withdrawal credentials is materially different from restaking an LST and needs specifically scoped authorization.
5. Use existing authorization only within its scope. Research or exit estimates do not authorize staking, token approvals, delegation, restaking or signing. Present the concrete plan for any missing authorization, and use the selected signer without ingesting secrets.
6. Reconcile each stage independently: preparation, authorization, signature, submission, receipt, resulting position, pending exit, claimable exit, final claim. Save request IDs, epoch or eligible block, current owner and claim recipient. A request receipt is not funds returned; an indexer's countdown is not proof of claimability. Check authoritative state before claiming or retrying an uncertain transaction.

## Report

Return chain/version and source time, underlying versus receipt units, available liquidity, current queue state and ownership, operator/curator/slashing exposure where relevant, unsigned plan and approval scope, and the verified lifecycle stage. Report a delay as an estimate unless a current contract condition proves eligibility.

Do not auto-install/connect tools, import wallet secrets, select an operator, extend authority, or schedule claims merely because these capabilities are documented. Use native harness scheduling only when monitoring is requested, with explicit targets and actionable alerts.

## Protocol-specific procedures

For a named protocol task, prefer its focused skill when installed:

- `galleon-lido-withdrawals`: Lido request IDs, NFT ownership, finalization and ETH claims.

This existing skill remains usable on its own for cross-protocol comparisons. Do not require another pack to complete its workflow.
