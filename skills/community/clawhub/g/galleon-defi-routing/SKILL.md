---
name: galleon-defi-routing
description: Compare token swaps and cross-chain routes, prepare reviewed transaction handoffs, and track destination delivery or refunds. Use when comparing DEX quotes, selecting bridges, preparing CCTP transfers, investigating stuck transfers, or recovering partial routes.
license: MIT
compatibility: Portable Agent Skills instructions. Live work needs the selected provider's HTTP, MCP or SDK tools; signing stays in the user's trusted wallet. No provider or runtime is installed by this skill.
metadata:
  author: Galleon Labs
  version: "0.3.1"
---

# DeFi routing

Move from an exact asset intent to a comparable quote and, when authorized, a reconciled outcome. A quote, signature, source receipt and destination delivery are different facts.


For Uniswap quote/Permit2/AMM/order tasks, prefer `uniswap-swap` when installed. For LI.FI quoting and transfer reconciliation, prefer `lifi-cross-chain`. Discover by exact skill name without assuming sibling files. Otherwise continue this standalone multi-provider procedure.

## Start with the requested task

Read [task examples and user configuration](references/task-examples.md) for a completed example and recovery path. Apply only the workflow stages needed by the current request. Reuse supplied preferences and compatible tools; ask only for missing terms that affect this task. Public explanation or comparison does not require transaction fields. Keep any existing authorization within its exact scope.

## Choose the task

Read [providers](references/providers.md) for official swaps, bridges and CCTP surfaces, access requirements and observed gaps. Read [workflows](references/workflows.md) for transaction sequencing, intent orders, asynchronous recovery and the output record. The [evaluation cases](references/evaluation.md) exercise decision boundaries with fixtures only.

Reuse a suitable connected official tool. Inspect actual schemas and version before relying on a skill or advertised tool list. Documentation MCP supplies reference material; unsigned builders supply proposed calls; signing or submission tools have a separate authority boundary. Do not automatically register a provider, install upstream skills, change accounts, pay for an API request or enable a signer.

## Establish exact intent

Resolve source and destination chain, network, token contract or mint, decimals, amount and exact-in/exact-out mode, sender and final recipient. Tickers and native-token sentinels differ by provider; bridged USDC, native USDC and wrapped assets are separate identities. Confirm the user's slippage, total fee budget, deadline and preferred execution route when those choices affect the result. Preserve already approved unchanged terms.

For comparisons, use the same amount, recipient, route constraints and near-contemporaneous observations. Compare conservative output and all-in costs: approvals, source/destination gas, bridge or solver fees, price impact, protocol/integrator fees and refund costs. An estimated duration is not a finality guarantee. State inaccessible routes instead of silently ranking an incomplete set as the entire market. Compare executable routes rather than preferred quote currencies: any supported quote asset can form a valid leg, including multihop, and an unavailable route is a concrete blocker where a quote symbol is not.

Capital location is not a route constraint. Holdings on another supported chain are deployable through a quoted bridge; count the quote's cost, delivery time and settlement risk as part of the economics instead of treating the holding chain as a blocker. When the destination action needs native gas, quote an owned source asset into the destination native currency delivered to the same account and make that delivery a separately verified prerequisite. A bridge cannot create gas from nothing: the source leg still needs source native gas, so an account with no native gas on any funded chain needs a supported gasless route or a small native deposit, not another quote.

## Prepare and hand off

Validate chain, balances, native gas reserve, token behavior, exact spender and finite allowance, permit domain/deadline, recipient, target, value and calldata. Use the official builder and simulate the exact proposed action when supported. Record unavailable simulation and material uncertainty. Source-chain simulation cannot prove future destination execution.

Separate approvals from swaps or bridge deposits. After approval receipts, obtain a fresh plan if the provider requires rebuilding or quote validity changed. A signature can be an executable off-chain intent even without a gas transaction. Present the final terms before handing the unchanged payload to an existing authorized wallet path. This skill never grants authority to sign, submit, create an account or change permissions. Never add affiliate, referral or builder fees without explicit consent.

## Reconcile before continuing

Persist request/order identity and transaction hashes. On a timeout or lost response, query the original operation before any new write. Continue bounded status reads; exhausted polling means pending or unknown, not failed. Never submit another source transfer to repair a delayed destination leg.

For swaps, require the provider's fill record and matching chain/account state. For bridges, require destination token, amount, recipient and receipt. Report partial output, refund pending, refund received and completion separately; inspect where and in which asset funds arrived. A follow-on swap, lending deposit or retry uses the actual received asset and newly reviewed terms.

## Deliver

Return the selected route or comparison with provider/version, exact identities, amounts, costs, quote expiry, evidence timestamps and unresolved gaps. For a submitted operation, add request ID, source and destination receipts, actual received asset/amount, state and next action. Redact credentials, signed payloads and private evidence. Use the user's installed LP, lending or other skill for the next primitive if available; otherwise return a self-contained handoff rather than silently installing dependencies.
