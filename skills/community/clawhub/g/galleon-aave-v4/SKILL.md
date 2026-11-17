---
name: galleon-aave-v4
description: Use when inspecting an Aave V4 Hub/Spoke position, sizing supply or borrowing, preparing repay/withdraw calls, or reconciling a V4 execution plan through official Aave MCP or AaveKit. V3 Pools, eMode and Aptos require their own interfaces.
license: MIT
compatibility: Portable instructions for public official Aave MCP or version-compatible AaveKit and read-only EVM tools. No signer included.
metadata:
  author: Andrew Wilkinson and Galleon Labs
  version: "0.3.1"
---

# Aave V4 positions and execution plans

Produce a decision for an observed V4 deployment and, when requested, a complete unsigned sequence with health preview and confirmation prerequisites. Do not migrate a V3 recipe by renaming its Pool.

## Discover the live deployment

Inspect the current tool schema and selected version. Use `get_chains` and `get_markets` with `version: v4`, the relevant symbols and actual `user`. For supply/borrow, select the current `get_markets` reserve. For withdraw/repay, use the `reserveId` returned by `get_position_items` for the exact owned position being exited or repaid. A same-symbol market reserve on another Spoke is not that position. Keep the selected opaque ID unchanged. Resolve chain, Spoke, Hub, reserve, asset, decimals and position identity from those observations, never a remembered address or hand-built ID. API coverage is not the universe of Aave deployments: retain covered, omitted and unserved chains.

Read user summary/positions, selected reserve details, relevant Hub asset/liquidity and position items. V4 risk and collateral operate within the position/Spoke; a wallet aggregate can hide a constrained position. Preserve principal, accrued interest, collateral enablement, applicable borrowing/health conditions, caps and available liquidity at one recorded state. Indexed USD rounding cannot settle a dust debt question.

Load [official MCP and SDK procedure](references/operations.md) for exact selectors, input units, plan branches and evidence limits. Refresh chain state when an executable action needs a fresh balance or allowance observation. Do not infer production maturity or deployed chain coverage from SDK `next` naming alone.

## Preview the precise action

Establish action, exact main-unit amount, recipient/on-behalf-of account, selected reserve and user risk floor. Aave MCP amounts are ordinary positive decimal strings in human token units; base-unit integer strings belong to different interfaces. Keep the unit conversion explicit. Inspect optional `native`, `max` and collateral behavior using current schemas.

Call `preview_action` with the exact parameters intended for `prepare_action`. Read returned `data`, all warnings and the health factor/position changes. An error-level warning stops the requested action; a warning needs explanation, not concealment. A health preview does not check every allowance or prove EVM execution. Apply user risk limits and separate interest/oracle stress from current conditions. Plain supply does not provide borrowing collateral unless the chosen action enables it.

## Build and reconcile the sequence

Use `prepare_action` with unchanged selectors and parameters. Inspect `__typename`; return every approval, permit, pre-contract gateway transaction and economic action in provider order. A typed permit creates spend authority and must bind the actual spender, amount, chain/domain and deadline. Review returned `from`, `to`, `data`, `value`, `chainId` and `operations` before a wallet handoff. An unknown plan branch is unresolved.

For separately authorized signing/submission, preserve exact payload and valid existing limits. After onchain approval, wait for the receipt and observed allowance before rebuilding. For V4 operations, carry the builder's `operations` into `get_transaction_processed` with its transaction hash; poll within bounded limits before preparing a dependent next action. This tool is not an arbitrary hash explorer. A provider index flag is not chain finality.

Repay uses current principal/interest and actual spendable debt token. After repay, re-read residual debt and collateral conditions before withdrawal. `withdrawableIgnoringDebt` omits borrowing constraints. Do not automatically increase the repay amount, alter collateral settings or substitute assets beyond user limits.

## Deliver

Return chain/Spoke/Hub/reserve/account, recorded observation state, amounts and units, current/proposed/stressed position, complete unsigned plan, warnings, approval and indexing prerequisites, and next missing read. For completed authorized work, require successful chain receipt plus matching position and actual asset balances; compare the preview with the observed outcome and explain indexing/accrual gaps.

Read [worked records and recovery](references/examples.md). Research checked 2026-10-08; no real supply, borrow, repay or liquidation was performed by this package. This skill is independently installable.
