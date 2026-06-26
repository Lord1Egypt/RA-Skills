---
name: uniswap-ai
description: Use Uniswap AI as the intent planner for swaps and liquidity actions, then pipe its output into Elytro smart accounts.
user-invocable: true
disable-model-invocation: false
required-skills: ["defi/elytro"]
allowed-tools: []
related-skills: ["defi", "elytro"]
metadata:
  upstream: https://github.com/Uniswap/uniswap-ai
---

# Use Uniswap AI as Your DeFi Planner

This skill explains how to collaborate with the Uniswap AI agent to design swaps, limit orders, or liquidity instructions before executing them with Elytro.

## Prerequisites

1. **Execution stack ready** – Follow `defi/elytro` so you know how to simulate/send transactions through Elytro smart accounts.
2. **Wallet context** – Gather balances and chain IDs using `elytro query ...` commands. You will feed these facts into Uniswap AI so it can size trades correctly.
3. **Market data** – If the user needs quotes, clarify slippage tolerance and deadlines up front; Uniswap AI can incorporate them into calldata/UserOps.

## Workflow

### 1. Provide Context to Uniswap AI

When invoking Uniswap AI, pass a concise brief that contains:

- Elytro account alias + address
- Chain / network (e.g., Arbitrum 42161)
- Token balances relevant to the trade
- Desired action (swap, add/remove liquidity, set range, etc.)
- Constraints (slippage, minimum received, deadline)

**Prompt template:**

```text
You control the Elytro smart account demo-arb at 0x1234... on Arbitrum (42161).
Balances: 500 USDC, 1.2 WETH.
Goal: swap 250 USDC into WETH with max 0.5% slippage. Provide calldata + ETH value for the Uniswap v3 router or build an ERC-4337 UserOperation that Elytro can sign.
Return JSON with fields {chainId, target, calldata, valueEth} OR {userOperation}.
```

### 2. Validate the Planner Output

Ensure Uniswap AI responds with one of:

- **Calldata bundle** – Router address, calldata hex, ETH value, chain ID, intent summary.
- **UserOperation** – A full ERC-4337 structure referencing your Elytro account as `sender` and optionally embedding a paymaster.

Checklist:

- Target contract is known (Uniswap v3 router, Universal Router, Permit2, etc.).
- Token addresses/amounts match the user request.
- Slippage settings align with requirements (`amountOutMinimum`, deadlines).

If anything is ambiguous, ask Uniswap AI for clarification before executing.

### 3. Hand Off to Elytro

Feed the validated artifact into the `defi/elytro` workflow:

- For calldata: set `ACCOUNT`, `CHAIN`, `ROUTER`, `CALLDATA`, `VALUE_ETH` environment variables and run `elytro tx simulate/send` as documented there.
- For UserOp: save the JSON (e.g., `swap-userop.json`), run `elytro tx simulate <alias> --userop "$(cat swap-userop.json)"`, then `elytro tx send ...`.

### 4. Report Back

After Elytro returns a bundler or transaction hash:

1. Share the hash + explorer link with the user.
2. Optionally re-run `elytro query balance` to confirm final balances and include them in the response.

## Safety & Validation

- Reject Uniswap AI outputs that reference unknown contracts or arbitrary delegatecalls.
- Require calldata to be hex with `0x` prefix and even length before passing it to Elytro.
- If the planner suggests `permit2` approvals, ensure the approving token is held and confirm allowances post-trade.
- For liquidity operations, double-check that NFT position IDs or pool fees match user input.

## Example Interaction

1. User: “Swap 100 USDC to ETH on Arbitrum with Elytro.”
2. Agent loads `defi` → selects `defi/uniswap`.
3. Agent prompts Uniswap AI with wallet info; receives router calldata.
4. Agent follows `defi/elytro` to simulate and send the transaction.
5. Agent reports back: “Swap submitted via Elytro, bundler hash 0x..., tx hash 0x..., final balance 0.12 WETH.”

Keep this skill handy for any Uniswap-centered workflow; for other protocols, add additional skills and link them through `defi`.
