---
name: hyperliquid-plan
description: "Build an exact unsigned Hyperliquid ticket for an entry, exit, reduction, cancel, modify, trigger order, TWAP, leverage change, or isolated-margin change. Use when the user has chosen an intent and asks for size, limits, order fields, risk checks, or a preflight plan. Planning only; not for market selection, live monitoring, signing, or submission."
license: MIT
compatibility: "Requires read-only market and account access for executable plans. The bundled risk script needs Node.js 20 or newer."
metadata:
  version: "0.4.0"
  protocol: "hyperliquid"
---

# Hyperliquid plan

Turn one user intent into an unsigned ticket that can be reviewed, expired, and reconciled.

If a skill rule blocks progress, cite its file and exact rule, explain the missing input or authority, and continue independent work within this skill's boundary. User instructions govern workflow and style defaults; they do not bypass tool or financial controls.

## Tool selection

When connecting or choosing tools, read [official tools](references/official-tools.md). Reuse a suitable maintained upstream capability before implementing new integration code; tool adoption stays optional and never supplies wallet authority.

## First task and connected workflow

Prepare an unsigned ticket for the selected action. For a hypothetical sizing example, state supplied inputs and missing live preflight fields. A cancel needs order identity, not an invented entry price. Read [agent integration and handoffs](references/agent-integration.md) on first use or when a tool or related skill is missing.

## Task handling

Reuse the user's stated intent and constraints across turns. Ask only for missing material inputs; never invent wallet identity, spend limits, or risk tolerance. Continue independent reads and show incomplete fields while awaiting answers. If prerequisite research is missing, complete the relevant read-only assessment when possible; keep the plan non-executable until its gates pass.

## Inputs

Start with network, public user account, target market/DEX and action. Use [intent and user preferences](references/intent-and-preferences.md) to require only the fields that action needs. An entry needs its loss and exposure limits; a cancel needs the exact existing order and protection impact, not a new entry thesis. Missing risk inputs stop an exposure-increasing plan, but do not prevent a clearly labeled hypothetical calculation or independent read-only preparation.

## Workflow

Apply each step to the selected action. Mark irrelevant fields not applicable with a reason; retain all identity, state, risk, recovery and expiry checks that can affect that action.

1. Rebind live identity and state: network, account, account abstraction mode, DEX, coin name, asset ID, `szDecimals`, price rules, margin table, mark, oracle, mid, depth, effective fees, positions, open orders, balances, available-to-trade, and current leverage.
2. Read [account modes](references/account-modes.md). Standard, unified, and portfolio-margin accounts expose balances and liquidation risk differently.
3. For exposure-increasing orders, size with [risk sizing](references/risk-sizing.md). For other actions, apply the action-specific checks in [intent and user preferences](references/intent-and-preferences.md); mark inapplicable entry-sizing fields as such with a reason. Use `node scripts/risk.mjs --help` for deterministic arithmetic. The stop fill must include adverse slippage and both entry and exit fees.
4. Construct the action with [order semantics](references/order-semantics.md). Resolve all IDs and precision from the target network now.
5. Model the full result set: rejection, resting, full fill, partial fill, trigger wait, margin cancel, unknown response, and account-state mismatch.
6. Assign one fresh 128-bit client order ID per order leg. Add `expiresAfter` when the signing scheme supports it. Record both before execution.
7. Check exchange constraints, user limits, rate-limit budget, current price tolerance, free margin, margin tier at post-trade notional, total open risk, correlated exposure, and protection for the resulting position.
8. Emit [the ticket contract](references/ticket-contract.md). Do not request a signature.

## Invariants

- A market-style order is an IOC limit with a worst acceptable price. There is no unbounded market order in the API.
- Size rounds down to current `szDecimals`. Price follows current tick and significant-figure rules. Never round size up to meet a minimum.
- Every exit, stop, and take-profit is reduce-only.
- TP/SL trigger on mark price. Their executable bound is separate from the trigger.
- A fixed-size trigger does not resize with the position.
- A partial IOC entry can leave the filled remainder unprotected. Plan the containment path.
- Changes to network, account, account mode, DEX, market, side, size, price, trigger, leverage, margin mode, slippage, fees, client IDs, expiry, or protection invalidate approval.

## Boundary

Do not construct a signature, expose a key, submit an action, or claim that a plan or simulation changed exchange state. Route explicit execution to `hyperliquid-execute` only after the ticket is complete.
