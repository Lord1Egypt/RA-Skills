# Official Hyperliquid tools

Read this when connecting data, selecting an SDK, building an integration, or reviewing an action produced by another tool. Reviewed 2026-09-05; verify current upstream behavior before use.

## Reuse the maintained API and SDK

The [Hyperliquid Python SDK](https://github.com/hyperliquid-dex/hyperliquid-python-sdk) is maintained by `hyperliquid-dex`. Prefer its `Info`, `Exchange`, WebSocket support and signing implementation when they satisfy the feature. Do not reinvent signing, nonce domains, asset encoding, subscription handling or order payloads from examples. Pin the reviewed release in the consuming project's dependency lock; inspect current changelog and code before upgrading. SDK use is optional and installing this skill does not install it or grant an account permission.

Public data requires no API key. For a Python integration, install the reviewed release (0.24.0):

```sh
python3 -m pip install hyperliquid-python-sdk==0.24.0
```

Perform that installation only for a user-selected Python integration, preferably in its existing virtual environment. Resolve and pin its release in that project's lock. This read-only example uses official SDK methods and no signer:

```python
from hyperliquid.info import Info
from hyperliquid.utils import constants

info = Info(constants.MAINNET_API_URL, skip_ws=True)
print(info.meta())
```

Use `TESTNET_API_URL` for an explicitly chosen testnet environment. A returned market universe is metadata evidence only; record observation time and fetch current depth before sizing. Do not invoke the SDK's trading examples as installation tests: some instantiate an exchange and submit orders.

For HTTP-capable harnesses, use the official [Info endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint) directly for reads. The equivalent metadata request is:

```sh
curl --fail-with-body https://api.hyperliquid.xyz/info \
  -H 'Content-Type: application/json' \
  --data '{"type":"meta"}'
```

The local market snapshot helper is another optional diagnostic if bundled in the installed skill. It does not replace the full SDK or supply a signer. Existing TypeScript applications can use documented HTTP/WebSocket reads or an explicitly identified maintained community SDK, but must not label community packages or MCP servers official. Verify signing parity against the official SDK before adopting a separate signing implementation; do not create a Python service solely to wrap a trivial public read.

## Identity, access and costs

Account reads use the user's public account or subaccount address. An API wallet address is a signing identity and is not a substitute for the account being queried. Configure any separately authorized API wallet through the official [API wallet interface](https://app.hyperliquid.xyz/API) and the user's trusted wallet tooling. Setup never authorizes that registration and never handles private keys. Keep signer secrets outside repository files, examples, shell arguments, logs and agent context even where upstream examples demonstrate file-based configuration.

Check current [API limits](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/rate-limits-and-user-limits), account fees and selected market metadata. No-key data access is not a guarantee of unlimited throughput or fee-free trading. Disclose protocol fees and any optional builder fee; never insert referral or builder attribution silently. Keep the `builder` field absent unless the user explicitly approved its exact recipient and fee. Installing an SDK is not consent to pay a builder.

## Integration contract

1. Inventory actual HTTP, WebSocket, SDK, account-read and trusted signer capabilities. Choose the smallest path that serves the task and record its version, network, methods, evidence and missing coverage.
2. Use SDK metadata resolution for asset identities, precision, product class and DEX scope. Verify spot, HIP-3 and subaccount support separately; a successful validator-perp read does not prove them.
3. Keep read and unsigned intent generation outside the signer. Review the final normalized order terms, address, fees, expiry and reduce-only semantics before requesting exact authorization.
4. Use the SDK's signing implementation inside the existing trusted execution boundary. Persist client order identity before submission; serialize signer writes. Review [official nonce and API wallet rules](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets) for the selected setup.
5. Distinguish transport success, action acceptance, per-order errors, fills and reconciled account state. Reconcile unknown results by client order ID and exchange records before any retry. Test public reads or local fixtures during setup; testnet orders still require explicit authorization.
6. For streams, use the SDK's subscriptions where suitable and enforce snapshot, gap, reconnect and backfill contracts in the application. See [official WebSocket documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket). A library reconnect alone does not prove the local order/account view is current.

Return selected upstream, installed version (or unavailable), successful read evidence, account identity source, supported operations, fee policy and next action. Report missing SDK or network access honestly and retain the direct public HTTP fallback when suitable. Never invent an official Hyperliquid MCP or CLI when the required surface is not verified.

## Account modes, assets and nonce lifecycle

The official [account abstraction modes](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/account-abstraction-modes), [asset IDs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/asset-ids), [nonce rules](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/nonces-and-api-wallets) and [builder codes](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/builder-codes) are published by Hyperliquid and were accessed 2026-09-05. These documentation checks are not a live account or signer test.

Read the account mode before interpreting collateral. Standard, unified and portfolio modes change balance and margin semantics; unified/portfolio account balances rely on the documented spot clearinghouse view, and perp DEX balance fields need not be meaningful in those modes. Do not add fields from multiple views as if they were independent spendable collateral. Read the actual user's account or subaccount, not its API wallet address, and identify the selected DEX scope. A migration between account modes is a separate authorized account change.

Resolve assets from current metadata using upstream helpers. Validator perps, spot, HIP-3 markets and outcome products use distinct asset namespaces; never derive an ID from the ticker alone or carry one network's cached ID into another. Validate precision, market identity and product support against the chosen SDK version. Unrecognized or changed metadata blocks construction rather than defaulting to a similarly named market.

Nonce state belongs to the signing identity. Independent workers sharing an API wallet must coordinate that identity's nonces; assigning separate authorized agent wallets avoids accidental collisions but is not permission to create one during setup. Retain durable order/client identity and nonce records across restarts. Follow official validity windows and pruning behavior: do not reuse a removed or expired agent wallet after its nonce state may have been pruned, because previously signed actions can become replayable. Never repair an unknown result by merely generating a newer nonce.

Builder fees are optional and separately authorized. The documented fee field uses tenths of a basis point, so a human basis-point limit must be converted and checked explicitly. Verify the exact builder address, fee and current approval with the main account. Never add a builder field simply to provide attribution.

The [official builder-code guide](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/builder-codes), retrieved 2026-09-23, caps builder fees at 0.1% on perps and 1% on spot; verify the current limit before encoding an approved fee.
The [official builder-code guide](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/builder-codes), retrieved 2026-09-23, names the user-signed `ApproveBuilderFee` action; the user's main wallet, not an API wallet, must sign approval. Approval is a separate authorized action outside these skills' trading execution scope.
The [official builder-code guide](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/builder-codes), retrieved 2026-09-23, requires the builder to have at least 100 USDC in perps account value; check the current requirement before claiming fee readiness.
The [official builder-code guide](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/builder-codes), retrieved 2026-09-23, allows at most 10 active builder-code approvals per user; if a user is already at that limit, a new approval cannot proceed. Do not insert builder attribution into a ticket while approval is unresolved.
The [official account-mode guide](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/account-abstraction-modes), retrieved 2026-09-23, requires a builder address to be in Standard mode to accrue builder fees; check the observed mode and keep any mode change separate.

Evaluation checks: an API-wallet address returning empty positions does not prove the user's account is flat; a timeout followed by restart does not authorize a duplicate order; unified-mode balances must not be double-counted; a pruned agent wallet must not be silently reused; and an approved builder fee of one basis point must not be encoded as one percent. Return the reconciled identity/state or block the action with the exact unresolved field.
