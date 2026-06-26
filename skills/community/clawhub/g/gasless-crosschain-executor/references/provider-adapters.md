# Provider adapter notes

These notes describe the providers the skill ships with and the contract any
new provider must satisfy. The validator's enum is currently
`{1inch-fusion-plus, 1inch-fusion, 1inch-aggregator, custom}`. To add another
provider, follow the integration template at the bottom of this file.

## Common adapter interface

Each adapter — whether shipped or user-added — should expose these operations:

```text
capabilities(params)            → supported chains, tokens, permit support, gasless verdict
quote(params)                   → normalized quote plus raw provider response
preflight(params)               → balances, allowances, permit/resource-lock availability
build_payload(quote, preflight) → typed-data OR tx ready for local_signer.py
sign(payload, local_signer)     → typed-data signature or signed transaction (handled by local_signer.py)
submit(payload, signature)      → order id or tx hash
status(order_id_or_tx_hash)     → status, substatus, terminal flag
cancel_or_refund(order_id)      → recovery instructions or transaction data
```

The agent should keep provider-specific raw responses on disk as redacted audit artifacts and should expose only normalized summaries to the user.

## 1inch Fusion+ (`1inch-fusion-plus`)

Cross-chain, gasless, intent-based. Resolvers cover gas and execute against a signed Order; hash-locked secrets enforce atomicity across the source and destination chains.

Pipeline:
- `examples/build_order_fusion_plus.mjs` — fetches quote, generates secrets, builds `EvmCrossChainOrder`, persists secrets to 0600 files. Outputs `typedData` + `submitPayload` + `secretFiles`.
- `examples/local_signer.py` (typed-data mode) — signs the EIP-712 order with strict field binding via `--expect-message-equal`.
- `examples/submit_fusion_plus.mjs` — POSTs `submitPayload + signature` to the relayer.
- `examples/status_fusion_plus.mjs` — polls until ready-to-accept-secret-fills, then until terminal.
- `examples/submit_secret.mjs` — releases one secret per fill and unlinks the file.

Good fit when:
- The route is EVM↔EVM and exposed by Fusion+.
- The user holds a 1inch developer token and a local signer.
- Allowance to the 1inch Limit Order Protocol is sufficient OR a permit path exists.
- The agent can keep state across multiple Bash invocations long enough to release each hash-lock secret when the provider reports a fill ready.

Notes:
- SDK package: `@1inch/cross-chain-sdk` (pinned via `examples/package.json`).
- The skill never writes raw secrets to disk visible to the agent. Secrets live in 0600 files under `$XDG_RUNTIME_DIR/gxe` (Linux) or `$TMPDIR/gxe-<uid>` (macOS), and `submit_secret.mjs` unlinks each file after the relayer accepts it.
- If allowance is insufficient and no permit is available, the first approval is not gasless. Reflect this honestly in `gasless_verdict`.
- Cross-chain intent flows have time-lock, refund, and recovery phases — keep cancellation/expiry information in the plan and audit artifacts.

Useful docs:
- https://help.1inch.com/en/articles/9842591-what-is-1inch-fusion-and-how-does-it-work
- https://github.com/1inch/cross-chain-sdk

## 1inch Fusion (`1inch-fusion`)

Same-chain, gasless, intent-based. Resolvers compete in a Dutch auction to fill a signed Order on the user's behalf, paying source-chain gas; the user signs once and waits for the auction to clear. No hash-lock secrets needed (single chain → no cross-chain atomicity to enforce).

Pipeline:
- `examples/build_order_fusion.mjs` — fetches quote, builds `FusionOrder`, outputs `typedData` + `submitPayload` (no secrets).
- `examples/local_signer.py` (typed-data mode) — signs the EIP-712 order against the 1inch LOP v4 domain. Strict field binding via `--expect-message-equal`.
- `examples/submit_fusion.mjs` — POSTs the signed Order to `/fusion/relayer/v2.0/{chainId}/order/submit`.
- `examples/status_fusion.mjs` — polls `/fusion/orders/v2.0/{chainId}/order/status/{orderHash}` until terminal.

Selection rule (same-chain): pick `1inch-fusion` when the wallet's native gas balance on the source chain is zero or below the chain's single-tx fee threshold. The user has no way to pay source gas, so the gasless intent path is forced. The agent should not ask which provider to use; it should run `examples/preflight.py --token native` and decide from the balance.

Notes:
- SDK package: `@1inch/fusion-sdk` (pinned via `examples/package.json`).
- The Order is the same struct as 1inch Limit Order Protocol v4: `{salt, maker, receiver, makerAsset, takerAsset, makingAmount, takingAmount, makerTraits}`. Bind every business field via `--expect-message-equal` flags on the signer; `nonce`, `expiry`, and partial-fill flags are packed inside `makerTraits`.
- If allowance is insufficient and no permit path exists, the first approval is not gasless — degrade the verdict to `gasless_after_existing_allowance` (next time) or `not_fully_gasless` (this time, if approval is needed in the same flow).
- If `getQuote` returns no fillable preset (illiquid pair, no resolver interest) and the wallet has no native gas, the user is in a deadlock: surface that they must either add gas to the wallet or pick a different pair. Do not silently retry through `1inch-aggregator`.

Useful docs:
- https://portal.1inch.dev/documentation/fusion/introduction
- https://github.com/1inch/fusion-sdk

## 1inch Aggregator v6 (`1inch-aggregator`)

Same-chain, NOT gasless, immediate-execution. Returns a regular EVM transaction targeting Aggregation Router v6 (`0x111111125421ca6dC452d289314280a0f8842A65` on most chains); the user signs and submits it themselves.

Pipeline:
- `examples/swap_aggregator.mjs` — fetches `/swap/v6.0/{chainId}/swap`, computes `minToAmount` from slippage, returns the tx envelope.
- `examples/local_signer.py --mode tx` — signs the tx with strict binding via `--expect-chain-id / --expect-to / --expect-value / --expect-data-prefix`. The `to` field must match the validator's `contracts.spender` (Aggregation Router v6 address).
- `examples/broadcast_tx.mjs` — submits the raw signed tx via `eth_sendRawTransaction`.

Selection rule (same-chain): pick `1inch-aggregator` when the wallet's native gas balance on the source chain is sufficient to cover the swap's `tx.gas × tx.gasPrice` (typically anything above ~0.001 native on ETH-class chains is enough). The agent should not ask the user which provider to use; the choice follows from the preflight reading.

Notes:
- The verdict is always `not_fully_gasless` for this provider; the validator does not enforce that constraint, but you should set it consistently in the plan so the user sees the honest cost picture.
- Approval to the Aggregation Router is required before the swap; check via `examples/preflight.py` and skip the approval tx only if a permit path exists for the source token.
- Nonce is not returned by `/swap`; the agent must fetch it via `eth_getTransactionCount` before piping the tx to `local_signer.py --mode tx`.

Useful docs:
- https://portal.1inch.dev/documentation/swap/quick-start
- https://docs.1inch.io/docs/aggregation-protocol/introduction

## `custom`

Validator-only escape hatch for users supplying their own audited contracts and adapter code. No helpers ship; the integrator is responsible for emitting a signable payload that conforms to the existing plan schema and the `local_signer.py` binding model.

Refuse to plan against `custom` unless the user has provided:
- audited contract addresses for spender / settler / verifying contract,
- a documented threat model,
- the exact field mapping between the plan and the typed-data / tx the integrator will sign.

## Integration template — adding a new provider

To add e.g. LI.FI Intents, deBridge DLN, or a custom relayer, follow this checklist. Worked examples live in the two implemented providers above.

1. **Schema enum.** Add the provider value to `PROVIDERS` in `scripts/validate_execution_plan.py`. Keep the value lowercase, kebab-case, and unambiguous (e.g. `lifi-intents`, `debridge-dln`).

2. **Quote-or-build helper.** Write one script that fetches a quote (HTTP or SDK), constructs the on-wire payload (typed-data for intent flows, tx for transaction flows), and emits a single JSON line on stdout. Mirror the structure of `examples/build_order_fusion_plus.mjs` (cross-chain intent) or `examples/swap_aggregator.mjs` (same-chain tx). Keep all signing and broadcasting out of this script — separation of concerns is the safety boundary.

3. **Local signer binding.** Document the field mapping between the plan and the typed-data / tx the new provider produces. The agent must enumerate every plan-bound business field as an `--expect-message-equal` (typed-data mode) or `--expect-*` (tx mode) flag when invoking `examples/local_signer.py`. Do not rely on the typed-data type system or implicit checks.

4. **Submit / status / recover helpers.** Thin HTTP wrappers, modelled on `submit_fusion_plus.mjs` / `status_fusion_plus.mjs` / `submit_secret.mjs`. For tx-flow providers, broadcast via `examples/broadcast_tx.mjs` instead.

5. **Tests.** Add a Node test that stubs the provider's HTTP API with a localhost server and asserts URL / query / body / response shape (see `tests/build_order.test.mjs` and `tests/swap_aggregator.test.mjs`). Add at least one validator case asserting the new provider value passes schema. Add a binding-coverage case in `tests/test_local_signer.py` or `tests/test_tx_signer.py` to lock in the field mapping.

6. **Docs.** Add a section to this file describing capabilities, pipeline, good-fit conditions, and notes. Update the README provider table. Update `SKILL.md`'s "Choose provider mode" branch.

## Provider comparison heuristic

When more than one provider can serve a route, pick in this order:

1. Fully gasless and safe (existing allowance, permit, or signed intent).
2. Better min received after all fees and margins.
3. Lower operational complexity and fewer signing surfaces.
4. Stronger status and recovery APIs.
5. Better chain and token coverage.

Reject a quote when any of these are true:

- Token, spender, settler, router, or chain id differs from the user request.
- The recipient does not match the user's intended recipient.
- The deadline is already expired or too close for cross-chain settlement.
- The minimum received amount is below the user's threshold.
- The route requires an approval or native fee but the plan claims it is fully gasless.
- The provider response cannot be tied to an official endpoint or SDK.
