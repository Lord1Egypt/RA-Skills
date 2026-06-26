---
name: evk-live-borrow-proof
description: Prove that a deployed Euler EVK market can really borrow against the intended collateral path with tiny live canaries or dry-run previews. Use when an agent needs to validate EVK borrowability on an EVM chain after deployment, especially for cross-vault share-token collateral, isolated collateral proofs, controller or collateral rotation in EVC, debt repayment cleanup, or adapting a known Arbitrum proof flow to other assets and chains.
metadata:
  clawdis:
    homepage: https://github.com/daav3/agentic-lending-project
    author: daav3
    requires:
      bins:
        - node
      env:
        - LIVE_SIGNER_ENV
      config:
        - borrow-proof-config.json
    primaryEnv: LIVE_SIGNER_ENV
---

# EVK Live Borrow Proof

Turn a successful one-off borrow probe into a repeatable agent workflow.

This skill is for proving actual borrowability onchain, not just showing that a vault deployed or that an oracle route exists on paper.

## Safety expectations
- default to preview mode first
- only use live signer-backed execution when the user explicitly asks for it
- require both `--live` and the config's guarded live-send acknowledgement field before any transaction is sent
- require the configured proof account address to match the signer address before any live proof transaction is sent
- keep signer material in environment variables or local runtime config, never in committed files
- require explicit nonzero swap protection for every live swap
- require explicit opt-in before using unlimited approvals

## Read next
1. `references/live-borrow-checklist.md`
2. `references/arbitrum-eusdc1-isolated-example.json` when you want a concrete config shape
3. Run `node scripts/evk_live_borrow_proof.js --help` for the bundled executor

## Default workflow
1. Normalize the proof target.
   Capture:
   - chain and RPC URL
   - wallet address and signer env name
   - borrow vault
   - target collateral vault
   - borrow asset and collateral asset
   - EVC address
   - tiny borrow amount
   - any stale controllers or stale collaterals that must be disabled first
   - whether collateral is already in the wallet or needs a swap path

2. Check the acceptance criteria before touching live state.
   Confirm all of these are true:
   - the borrow vault oracle can quote the intended collateral vault share token into the borrow vault unit of account
   - the borrow vault has enough cash for the tiny canary borrow
   - the borrow vault has the required LTV link for the target collateral vault
   - the account can rotate EVC controller and collateral state cleanly

3. Use preview mode first.
   Run the bundled executor without `--live` so the agent can inspect:
   - current debt
   - wallet balances
   - enabled collaterals
   - vault cash
   - planned approvals, swaps, collateral rotation, and borrow

4. Run live only after the preview is sane and the user has asked for a real canary.
   Keep amounts tiny.

5. Report what was actually proven.
   Always distinguish between:
   - mixed-collateral borrow
   - isolated target-collateral borrow
   - quoteability only
   - full live borrow success

## Bundled executor
Use `scripts/evk_live_borrow_proof.js`.

It supports:
- preview mode with a read-only account address
- live mode with a signer loaded from an environment variable
- optional debt repayment before the new proof
- optional single-hop Uniswap V3 style swaps to source repay or collateral assets
- collateral deposit into the target EVK vault
- disabling stale collateral vaults in EVC
- disabling stale controllers in EVC
- enabling the target collateral and optionally the target controller
- final tiny borrow and before/after logging

## Generalization rules
- Do not hardcode Arbitrum, WETH, USDC, `eWETH-11`, or `eUSDC-1`. Treat them as an example only.
- Treat router address, fee tier, wrapped native token, token decimals, EVC address, and vault addresses as per-chain inputs.
- If the collateral asset is already in the wallet, skip the swap and deposit directly.
- If the borrow asset used for repayment is not already in the wallet, either source it first or configure `repaySwap`.
- If the chain does not use a Uniswap V3 compatible router, do not pretend the bundled swap path is portable. Replace or bypass that step explicitly.
- If the proof must show isolation, disable the old collaterals first and report the final enabled collateral set.

## Non-negotiable EVK lessons
- A deployed market is not proven borrowable until a real borrow succeeds.
- Cross-vault borrowing depends on the borrow vault oracle pricing the collateral vault share token, not just the underlying asset.
- Controller state and collateral state in EVC are separate concerns. Check both.
- Preview mode is useful, but it is not a substitute for a live canary.

## Output expectations
Always report:
- chain and account used
- preview or live mode
- borrow vault and collateral vault
- whether old debt was repaid first
- whether the target collateral path was isolated
- before and after debt
- before and after enabled collaterals
- collateral vault balance after deposit
- vault cash and liquidity snapshot before borrow
- tx hashes for live operations
- what remains unproven or chain-specific

## If deployment is still missing
If the user is not yet at the live-proof stage and still needs a borrowable EVK market, switch to the `agentic-lending-evk` skill first, especially for share-aware router deployment work.
