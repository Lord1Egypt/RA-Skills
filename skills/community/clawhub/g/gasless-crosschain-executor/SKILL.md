---
name: gasless-crosschain-executor
description: local-key swap planning and execution skill. Cross-chain (1inch Fusion+, gasless), same-chain gasless (1inch Fusion), and same-chain paid (1inch Aggregation Router v6) paths are bundled. Use when a user asks an agent to quote, validate, sign locally, broadcast, monitor, or recover EVM swaps while keeping private keys on the user's machine.
---

# Gasless Crosschain Executor

## Overview

Plan, validate, sign, submit, and monitor EVM swaps with local-only key custody. Same-chain and cross-chain paths are bundled.

This is not a trading strategy. It is an execution-safety workflow over 1inch Fusion+ (cross-chain gasless), 1inch Fusion (same-chain gasless), and 1inch Aggregation Router v6 (same-chain paid). `custom` is an escape hatch when the user supplies audited contracts.

## Environment prerequisites

Helpers are not installed system-wide. Before running anything in `scripts/` or `examples/`:

- A Python venv must exist at `./.venv` with `eth-account` and `web3`. If a script raises `ModuleNotFoundError`, ask the user to run `./scripts/setup.sh` from the skill root.
- Invoke scripts via `.venv/bin/python` or after `source .venv/bin/activate`. Never `pip install` into system Python.
- The `.mjs` helpers also need Node 20+ and `examples/node_modules/`. `setup.sh` handles this when Node is available; without Node, only the Python tools work (sufficient for wallet bootstrap, validation, and signing).

## Non-negotiable safety model

- Never ask the user to paste a private key, seed phrase, mnemonic, raw keystore password, wallet backup, or one-time code into chat.
- Never print, log, store, or echo any private key material. Use a local environment variable, local key vault, hardware wallet, or wallet connector managed outside the conversation.
- Do not execute a real trade unless the user has reviewed an exact execution plan and explicitly authorized that exact plan.
- Do not sign arbitrary calldata or typed data unless the provider, chain ids, token addresses, spender or settler addresses, amounts, recipient, deadline, nonce, slippage, and cancellation or refund path have been checked.
- Treat approvals as high risk. Prefer finite allowances, permit signatures, or intent/resource-lock designs. Avoid unlimited approvals unless the user explicitly approves the risk.
- If a flow needs a source-chain approval transaction and no permit path exists, state that the flow is not fully gasless for that wallet-token pair.
- If the agent cannot access a secure local signing runtime, produce an implementation plan and commands only; do not simulate possession of the key.

## Resolving an open-ended buy request

When the user says *"buy PEPE"* or *"swap my USDC for ETH"* without exact addresses / chains / amounts, expand the request before doing anything else. Do not infer fields silently.

1. **Destination token** — if only a symbol was given, run `examples/resolve_token.mjs --chain <id> {--symbol <SYM>|--address <addr>}`. If the result has a `warning` (no verified match, multiple verified candidates), show the user the list and ask. Refuse to plan against an unverified address unless the user explicitly opts in.
2. **Destination chain** — use the chain the user named. If none was named, ask. The skill has no liquidity-comparison tool; do not guess.
3. **Source side** — if the user did not specify, run `examples/portfolio_scan.py --owner <addr>` and pick a candidate (e.g. a stablecoin or the largest verified holding) on a chain that can reach the destination. Confirm with the user.
4. **Path** — cross-chain → `1inch-fusion-plus`. Same-chain → check the wallet's native balance via `preflight.py --token native`: zero/dust → `1inch-fusion`, otherwise → `1inch-aggregator`. See the workflow decision tree below for the exact invocation.
5. **Amount** — plan amounts are smallest-unit decimal strings. Convert via the source token's `decimals`. Fiat-denominated requests (e.g. "$10 worth") need an external price source the skill does not provide; ask the user for a token-unit amount or document the oracle used.
6. Hand off to the standard execution workflow below.

## Workflow decision tree

1. Classify the request.
   - Design or review only: provide architecture, adapter choices, and risk notes.
   - Quote only: gather route parameters, query provider quotes, and return a route comparison without signing.
   - Execute: use the full execution workflow below.
   - Monitor or recover: use provider status APIs and cancellation or refund instructions.
   - Bootstrap a wallet: the user has no wallet or does not know how to configure one. Use the wallet bootstrap workflow before any other workflow that needs a signer.

2. Choose provider mode. The choice follows from observable state; do not ask the user. Validator enum: `{1inch-fusion-plus, 1inch-fusion, 1inch-aggregator, custom}`.

   Cross-chain (`source_chain_id != destination_chain_id`) → `1inch-fusion-plus`. Pipeline: `build_order_fusion_plus.mjs` → `local_signer.py` (typed-data) → `submit_fusion_plus.mjs` → `status_fusion_plus.mjs` → `submit_secret.mjs`.

   Same-chain (`source_chain_id == destination_chain_id`) — branch on the wallet's native balance on the source chain:
   1. Read it: `examples/preflight.py --rpc-url <RPC> --token native --owner <wallet> --spender <wallet>` (`--spender` is unused but required; pass the wallet itself).
   2. Below the chain's single-tx gas cost (treat under ~0.001 native on ETH-class chains as zero) → `1inch-fusion`. Pipeline: `build_order_fusion.mjs` → `local_signer.py` (typed-data) → `submit_fusion.mjs` → `status_fusion.mjs`.
   3. Otherwise → `1inch-aggregator`. Pipeline: `swap_aggregator.mjs` → `local_signer.py --mode tx` → `broadcast_tx.mjs`.

   `custom` is reserved for user-supplied audited contracts; otherwise the rule above is non-negotiable.

   If the wallet has no gas and `1inch-fusion` returns no fillable preset, report the deadlock to the user. Do not silently fall through to the aggregator.

   Same-chain vs cross-chain follows from the user-named chain ids. Never reroute through cross-chain to find liquidity.

   To add a provider, see `references/provider-adapters.md`.

3. Decide whether the route is actually gasless.
   - Gasless means no source-chain native gas is required for swap execution.
   - Destination-side gas fronting, refuel, or receiving native on the destination chain is not source-chain gasless.
   - Approvals, source-chain order-creation transactions, and native fixed fees break gasless unless covered by a permit, an existing allowance, a resource lock, or a third-party relay.

## Wallet bootstrap workflow

Use this workflow only when the user has no usable signer or explicitly asks for help configuring one. The skill never accepts a key in chat; it only triggers a local generator that runs on the user's machine.

1. Confirm intent and risk acknowledgement.
   - Ask the user to confirm: "I want to generate a brand-new wallet locally on this machine."
   - Tell the user clearly: this wallet should be treated as a low-balance starter wallet until they have verified their backup. Do not move large funds into a freshly generated wallet before testing recovery.

2. Pick a generation mode.
   - `keystore` (default): an encrypted EIP-2335-style JSON keystore. The user types the passphrase into the local terminal, never into chat.
   - `file`: raw 0x-prefixed private key in a `0600` file. Prototype only — read access by any other process means total loss of funds.
   - `env`: prints a one-shot `export LOCAL_PRIVATE_KEY=...` line on the local terminal. The agent must never see, log, or store the printed value.

3. Run the generator on the user's machine.
   - Invoke `examples/generate_wallet.py` (or an equivalent local tool) with the chosen mode and a target path under a directory whose permissions are `0700`.
   - The generator must: source entropy from a CSPRNG, derive the EVM address from the new key, set file permissions to `0600`, refuse to overwrite an existing wallet without `--force`, and print the address only — never the key — to standard output that the agent can read.

4. Run the backup ceremony in the local terminal.
   - The generator displays the BIP-39 mnemonic (24 words) once on the local TTY (not via the agent), prompts the user to write it down on paper or store it in an offline password manager, and requires the user to retype a confirmation phrase before the script exits.
   - Remind the user that anyone who learns the mnemonic or private key controls all funds in the wallet, that there is no recovery if it is lost, and that screenshotting or pasting it into chat or cloud notes defeats the purpose of local generation.

5. Wire the new wallet into subsequent plans.
   - Use `signer_ref` of the form `keystore:<absolute path>`, `file:<absolute path>`, or `env:<VAR_NAME>` per the chosen mode. Never embed the key.
   - Use the new wallet for subsequent plans unless the user names another.
   - Before the first real execution, run a dry-run or quote-only round trip to confirm the signer.

## Execution workflow

1. Gather required parameters.
   - source chain id and destination chain id
   - source token address or native token marker
   - destination token address or native token marker
   - source amount in smallest units
   - recipient address on the destination chain
   - wallet address derived locally from the signer
   - slippage or minimum received constraint
   - deadline and fill timeout
   - provider preference and API keys, if any
   - local RPC URLs for source and destination chains
   - whether this is dry-run, quote-only, or authorized execution

2. Verify local signer setup.
   - If the user has no signer yet, run the wallet bootstrap workflow before continuing.
   - Derive the wallet address locally from the configured signer.
   - Confirm the derived address matches the address the user expects.
   - Use chain-specific signers only for supported chains. Do not reuse EVM private keys for non-EVM chains unless the user has explicitly configured that wallet type.

3. Query balances and token metadata.
   - Verify source token balance, decimals, symbol, and destination recipient format.
   - For ERC-20 tokens, check allowance to the provider's spender (1inch LOP v4 for Fusion+ and Fusion, Aggregation Router v6 for Aggregator).
   - If allowance is insufficient, check EIP-2612 / DAI-style / Permit2 support via `examples/preflight.py` before recommending an approval transaction.

4. Quote and build the signable payload.
   - Normalize the quote into the execution plan schema in `references/execution-plan-schema.md`.
   - Show route, min received, fees, expected time, contracts, spender, chain ids, and status endpoint.
   - Cross-chain: `examples/build_order_fusion_plus.mjs` produces typed-data + submit payload + 0600 secret files in one pass.
   - Same-chain (Fusion): `examples/build_order_fusion.mjs` produces typed-data + submit payload; no secrets.
   - Same-chain (Aggregator): `examples/swap_aggregator.mjs` produces a tx envelope; add `nonce` from RPC `eth_getTransactionCount` before signing.

5. Validate the plan before signing.
   - Save the normalized plan JSON locally.
   - Run `scripts/validate_execution_plan.py plan.json`.
   - Resolve every `ERROR`. Disclose every `WARNING` to the user.

6. Require explicit user authorization.
   - Present the exact route and plan hash.
   - Ask for approval only after showing amounts, recipient, chain ids, provider, contracts, deadline, allowance changes, and max loss.
   - The authorization must be specific to the current plan. A general instruction such as "you can trade for me" is not enough for real execution.

7. Sign locally.
   - Shell out to `examples/local_signer.py`. Pass the full binding from the validated plan via `--expect-*` flags; the signer re-asserts every one before signing and refuses on any mismatch.
   - Always pass `--expect-chain-id`. For typed-data, also pass `--expect-verifying-contract`.
   - Typed-data mode (default; used for Fusion+ Order, Fusion Order, EIP-2612 permits): one `--expect-message-equal FIELD=VALUE` per plan-bound message field.
     - 1inch Fusion+ / Fusion Order: `salt`, `receiver`, `makerAsset`, `takerAsset`, `makingAmount`, `takingAmount`, `makerTraits` (packs nonce, expiry, and partial-fill flags). Plus `--expect-sender-field maker`.
     - EIP-2612 permit: `owner`, `spender`, `value`, `nonce`, `deadline`. Plus `--expect-sender-field owner`.
     - Pin `--expect-domain-equal name=...` / `version=...` whenever the provider docs pin those.
   - Tx mode (`--mode tx`, for Aggregator swaps): bind `--expect-to <plan.contracts.spender>` and `--expect-value <plan.fees.source_native_value>` (typically `0` for ERC20→ERC20). Optional `--expect-data-prefix 0x<selector>` to pin the function selector.
   - Skipping a binding leaves that field tamperable; document the reason if you do.

8. Submit and monitor.
   - Submit via the provider's relayer (`submit_fusion_plus.mjs`, `submit_fusion.mjs`) or RPC (`broadcast_tx.mjs`).
   - Persist non-secret audit artifacts: plan JSON, plan hash, quote id, order id, tx hash, status endpoint, timestamps, redacted provider responses.
   - Fusion+ hash-lock secrets live in 0600 files under `$XDG_RUNTIME_DIR/gxe` (Linux) or `$TMPDIR/gxe-<uid>` (macOS). `submit_secret.mjs` reads one file per fill and unlinks it after the relayer accepts the secret. Do not log, copy, or echo the secret values.
   - Poll until a terminal state, then summarize final received amount, transaction hashes, and any remaining user action.

## Provider references

Load these files only when relevant:

- `references/provider-adapters.md` for 1inch Fusion+ and 1inch Aggregator adapter notes, plus the integration template for adding new providers.
- `references/security-policy.md` for key handling, allowance, signing, and local key generation guardrails.
- `references/execution-plan-schema.md` for the plan JSON shape that must be validated before signing.
- `references/sample-plan.json` for a minimal sample plan accepted by the validator.
- `examples/` for runnable tools:
   - bootstrap + signing: `generate_wallet.py`, `local_signer.py` (typed-data + `--mode tx`), `preflight.py`, `portfolio_scan.py`, `resolve_token.mjs`
   - cross-chain (Fusion+): `build_order_fusion_plus.mjs`, `submit_fusion_plus.mjs`, `status_fusion_plus.mjs`, `submit_secret.mjs`, plus the standalone `quote_fusion_plus.mjs`
   - same-chain gasless (Fusion): `build_order_fusion.mjs`, `submit_fusion.mjs`, `status_fusion.mjs`
   - same-chain paid (Aggregator v6): `swap_aggregator.mjs`, `broadcast_tx.mjs`

## Output format for execution plans

For every real or proposed execution, return this structure before signing:

```text
provider: <provider mode>
mode: dry_run | quote_only | approval_required | execute_after_user_approval | monitor_only
route: <source chain/token/amount> -> <destination chain/token/min received>
recipient: <destination recipient>
wallet: <locally derived wallet address>
contracts: <spender/settler/escrow/router addresses>
fees: <solver fee, protocol fee, source tx fee, destination gas, provider margin>
gasless verdict: fully_gasless | gasless_after_existing_allowance | gasless_after_permit | not_fully_gasless | unknown
user approval needed: yes/no and why
status tracking: <order id or tx hash plus endpoint>
plan hash: <sha256 of normalized plan json>
warnings: <non-fatal risks>
blocking errors: <must fix before signing>
```

## Recovery guidance

- If order creation fails before signing, no on-chain recovery is needed.
- If signing succeeds but broadcast fails, check whether the signature or order was accepted by the provider before retrying.
- If an intent/order is submitted but not filled, use provider-specific order status and cancellation or refund rules. Do not create a second conflicting order unless the first order is terminal, cancelled, expired, or has non-overlapping funds.
- If destination receipt differs from the quote, compare against the accepted minimum received amount and provider partial-fill semantics.
- If a user suspects compromise, stop execution and recommend revoking allowances and moving funds using a secure wallet environment.
