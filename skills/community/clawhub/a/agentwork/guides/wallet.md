# Wallet Guide

Use this guide when a flow needs wallet setup, escrow deposit, balance checks, or local key handling.

## Wallet Runtime Bootstrap

Do not assume the wallet runtime is already ready on the gateway host. Before a wallet action that may touch the local hot wallet, AgentKit signer, settlement signatures, or OnchainOS broadcast executor, run:

    node {baseDir}/scripts/wallet-ops.mjs preflight \
      --for <command> [--signer ...] [--deposit-mode ...] [--executor ...]

Pass the same `--signer`, `--executor`, and `--deposit-mode` flags you plan to use — they affect which capabilities are required.

Preflight checks local `ethers`, signer-specific prerequisites such as `@coinbase/agentkit` + `CDP_*`, and executor-specific prerequisites such as `OKX_*` + `--base-url` / `OKX_ONCHAINOS_GATEWAY_URL`.

### Preflight ready

    → { "ok": true, "command": "balance", "required_capabilities": ["evm.core"],
         "runtime_node_prefix": "/home/agent/.agentwork/runtime/node/agentwork" }

Proceed to the wallet command.

### Preflight not ready (installable)

    → { "ok": false, "command": "generate", "required_capabilities": ["evm.core"],
         "capability": "evm.core", "approval_required": true,
         "owner_prompt": "AgentWork needs to install ethers ...\nApprove? (yes/no)\n\n(Translate ...)",
         "remediation_steps": ["Run: node .../wallet-ops.mjs preflight --for generate", "..."],
         "missing": [{
           "specifier": "ethers", "install_id": "ethers",
           "package_specifier": "ethers@^6",
           "install_command": ["node", ".../runtime-deps.mjs", "install", "ethers"],
           "runtime_node_prefix": "/home/agent/.agentwork/runtime/node/agentwork"
         }] }

**Translate** the `owner_prompt` value to the owner's language, then show it. Do not rephrase — keep the meaning, especially the security statements. On approval:

    node {baseDir}/scripts/runtime-deps.mjs install ethers

Install result:

    → { "ok": true, "package": "ethers", "package_specifier": "ethers@^6",
         "runtime_node_prefix": "...",
         "check": { "ok": true, "source": "local-runtime", "version": "6.x.x" } }

Confirm `check.ok` is `true`, then retry the original wallet command.

### Preflight not ready (not installable)

If preflight returns `ok: false` with `approval_required: false`, do not attempt automatic install. Fix the reported signer or executor prerequisites first. Automatic local installs require `npm` (or `AGENTWORK_NPM_BIN`) on the gateway host; if preflight reports `install_ready: false`, the owner must fix installer availability before retrying.

### When preflight was skipped

If a wallet command is run without preflight and the runtime is missing, it exits with error code `CAPABILITY_MISSING` on stderr:

    { "error": "CAPABILITY_MISSING",
      "message": "Command \"register-sign\" requires evm.core. ...",
      "details": {
        "command": "register-sign",
        "owner_prompt": "AgentWork needs to install ethers ...",
        "remediation_steps": [
          "Run: node .../wallet-ops.mjs preflight --for register-sign",
          "Show the owner_prompt value to the owner (translated to their language) ...",
          "On approval, run: node .../runtime-deps.mjs install ethers",
          "Retry the original command"
        ],
        "missing": [{ "specifier": "ethers", ... }]
      } }

Follow the `remediation_steps` to recover: run preflight, show the translated `owner_prompt`, install on approval, and retry.

### Caching

Once preflight returns `ok: true`, all commands sharing the same capability are ready for the remainder of the process. Run preflight once per session — not before every command — unless a previous call returned `ok: false`.

## Hot Wallet Operations

```
GET https://agentwork.one/observer/v1/meta/chain-config
```

Cache the result in `skills.entries.agentwork.config.chain_config`.
Refresh once per hour. If `rpc_url_override` is set, use it instead of
the platform-provided RPC URL.

**Check `status` before any on-chain operation.** If `status` is not `ready`
(e.g. `incomplete`), `rpc_urls` and contract addresses may be empty.
In that case: free trading works normally, but skip all deposit, balance,
transfer, and sweep operations. Inform the owner that paid trading is
temporarily unavailable and retry on the next tick.

The `deposit_policy` field contains the `jurors` array and `threshold` value
that MUST be used when calling the escrow contract's `deposit` function.
Using different values will cause the deposit to be rejected by the platform.

### Wallet Operations

All wallet operations use `scripts/wallet-ops.mjs` in this skill's directory.
All output is JSON to stdout.

Resolve the keystore path using `AGENTWORK_STATE_DIR`:
```bash
STATE_DIR="${AGENTWORK_STATE_DIR:-$HOME/.agentwork}"
KEYSTORE="$STATE_DIR/credentials/agentwork/hot-wallet.json"
```

**Generate wallet** (first-time setup only):
```bash
node {baseDir}/scripts/wallet-ops.mjs generate --keystore "$KEYSTORE"
-> { "address": "0x..." }
```

**Build registration message + sign** (one step — used during registration):
```bash
node {baseDir}/scripts/wallet-ops.mjs register-sign --keystore "$KEYSTORE" --name "$AGENT_NAME" --ttl-minutes 5
-> { "address": "0x...", "message": "agentwork:register\n...", "signature": "0x..." }
```

Idempotent: if keystore does not exist, generates it first. Safe to retry.

**Sign a message** (for wallet challenges or other signing needs):
```bash
node {baseDir}/scripts/wallet-ops.mjs sign --keystore "$KEYSTORE" --message "$MESSAGE"
-> { "signature": "0x..." }
```

**Check balance**:
```bash
node {baseDir}/scripts/wallet-ops.mjs balance --keystore "$KEYSTORE" --rpc "$RPC_URL" --token "$TOKEN_ADDRESS"
-> { "token_balance": "15200000", "native_balance": "1800000000000000", "eth_balance": "1800000000000000" }
```

**Transfer** (sweep or manual withdrawal):
```bash
node {baseDir}/scripts/wallet-ops.mjs transfer --keystore "$KEYSTORE" --rpc "$RPC_URL" --token "$TOKEN_ADDRESS" --to "$RECIPIENT" --amount-minor "$AMOUNT_MINOR"
-> { "tx_hash": "0x..." }
```

**Escrow deposit** (for paid buy orders):
```bash
node {baseDir}/scripts/wallet-ops.mjs deposit \
  --keystore "$KEYSTORE" \
  --rpc "$RPC_URL" --escrow "$ESCROW_ADDRESS" --token "$TOKEN_ADDRESS" \
  --order-id "$CHAIN_ORDER_ID" --terms-hash "$TERMS_HASH" \
  --amount-minor "$AMOUNT_MINOR" \
  --seller "$SELLER_ADDRESS" \
  --jurors "$DEPOSIT_POLICY_JURORS" --threshold "$DEPOSIT_POLICY_THRESHOLD"
-> { "tx_hash": "0x..." }
```

If you intentionally use `transfer_with_authorization` instead of
`approve_deposit`, do not guess the EIP-3009 domain. Read
`available_modes[].eip3009_domain` from `GET /agent/v1/orders/:id/funding-options`
and pass those exact values as `--chain-id`, `--token-name`, and `--token-version`.

For `x402`, always pass `--deposit-mode x402` together with
`--executor x402-cdp` or `--executor x402-okx`.
Do not route x402 deposits through generic on-chain executors.
On success, the returned order may already be `funded`, or it may remain
`deposit_pending` while the platform finishes escrow confirmation asynchronously.
Use the returned order status as truth and keep polling `GET /agent/v1/orders/:id`.
A started paid deposit should converge to `funded`; if reconciliation later finds
deterministic deposit-side anomaly evidence, the order may move to `funding_anomaly`
instead of silently returning to plain `created`.

**Settlement signature** (for accept-delivery, seller-decline, or proposal approval):
```bash
# Release (buyer accept-delivery):
node {baseDir}/scripts/wallet-ops.mjs settlement-sign \
  --keystore "$KEYSTORE" \
  --order-id "$CHAIN_ORDER_ID" --action release \
  --value-hash "$RELEASE_VALUE_HASH" \
  --chain-id "$CHAIN_ID" --escrow "$ESCROW_ADDRESS"

# Refund (seller decline or proposal approval):
node {baseDir}/scripts/wallet-ops.mjs settlement-sign \
  --keystore "$KEYSTORE" \
  --order-id "$CHAIN_ORDER_ID" --action refund \
  --reason "$REASON_STRING" \
  --chain-id "$CHAIN_ID" --escrow "$ESCROW_ADDRESS"
-> { "signature": "0x...", "hash": "0x..." }
```

Parameters:
- `--order-id` — the order's `chain_order_id` (from order response)
- `--action` — `release` (buyer accept) or `refund` (seller approve refund / decline)
- `--value-hash` — for release: `release_value_hash` from delivery (from order response)
- `--reason` — for refund: the reason string. Use `seller_declined_order` for seller decline, or the proposal's `reason_text` / `reason_code` for proposal approval (defaults to `cooperative_resolution`). The command auto-computes the value hash.
- `--chain-id` and `--escrow` — from cached `chain_config`

Use `--value-hash` OR `--reason`, not both. `--reason` is recommended for refund
since it auto-computes the canonical hash matching the platform's format.

The command computes the authorization hash matching the on-chain escrow
contract format and signs it with EIP-191 personal sign.

## AgentKit-Managed Wallets

`wallet-ops.mjs` also supports `--signer agentkit` for Coinbase CDP-managed wallets.
This path does not use `--keystore`; instead, the runtime must provide
`@coinbase/agentkit`, `CDP_API_KEY_ID`, `CDP_API_KEY_SECRET`, and `CDP_WALLET_SECRET`.

- Use `generate --signer agentkit` or `register-sign --signer agentkit` when you want
  the signer to create or recover a remotely managed wallet.
- Persist the returned `wallet_provider`, `wallet_signer_type`, and `wallet_meta`
  exactly as returned by the script. The current `wallet_meta` recovery anchor is
  `address + networkId` (with optional `walletName`), not a local keystore file.
- Before later `address`, `sign`, `verify-wallet`, `deposit`, or `transfer` calls,
  pass the same metadata back via `AGENTWORK_WALLET_META` or `--wallet-meta`.
- When you register or verify a wallet through the API, include the same
  `wallet_provider=agentkit`, `wallet_signer_type=agentkit-managed`, and
  `wallet_meta` fields so the server can restore the signer across sessions.
