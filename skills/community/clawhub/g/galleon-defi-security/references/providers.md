# Official transaction-review tools

Primary documentation reviewed 2026-09-05. Access tiers and schemas can change; inspect current docs and discovered tool inputs before enabling a provider. No authenticated provider call was needed to author this reference.

## Tenderly

[Official MCP overview](https://docs.tenderly.co/ai-tools/overview) and [connection guide](https://docs.tenderly.co/ai-tools/quickstart) document `https://mcp.tenderly.co/mcp`, remote HTTP with OAuth, paid-plan enablement and an account/project prerequisite. A successful OAuth flow does not prove the selected network or requested simulation works. Do not enroll a plan or spend credits implicitly.

The [tool reference](https://docs.tenderly.co/ai-tools/tools) documents `set_active_project` before project-scoped calls; preserve the operator's intended account/project. For review, select `simulate_transaction`, contract/network lookup and the necessary simulation detail reads. In particular, `get_simulation_exposure_changes` describes approvals/permits while `get_simulation_balance_changes` describes net asset effects. Inspect truncated responses. Simulations persist in the project dashboard: unsigned calldata may still be private. The wider server includes virtual-environment creation, deletion and impersonated sends; do not expose that entire surface for a review-only task.

For an existing approved RPC connection, the [RPC quickstart](https://docs.tenderly.co/simulations/quickstart) uses `tenderly_simulateTransaction` with transaction fields and a block argument. Its RPC URL embeds a credential; redact it. [Simulation overview](https://docs.tenderly.co/simulations/overview) distinguishes API, RPC and bundled simulation paths. Prefer a bundle for dependent steps and record overrides. Gasless execution in a simulator is neither a free-service guarantee nor evidence that the future onchain transaction will succeed.

### Hermes integration

Use the selected Hermes profile's native MCP setup, for example `hermes mcp add tenderly --url https://mcp.tenderly.co/mcp --auth oauth`. Inspect discovered schemas and allow only the required tools. Keep external output untrusted; disable unused resource/prompt wrappers and use `trust: untrusted` where supported. Confirm a bounded permitted read before declaring readiness. Native filters do not constrain separate shell tools or replace wallet policies. [Hermes MCP guidance](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp/).

## Safe

Use official `@safe-global/protocol-kit` for contract/account interaction and `@safe-global/api-kit` for Transaction Service reads. Read chain, Safe version, owners, threshold, nonce, modules and guard; examine existing pending transactions before planning another nonce. The service's proposals and collected signatures are distinct from onchain execution. Service authentication and supported networks depend on the deployment; follow the selected service's current requirements. Do not use a service's pending status as final receipt evidence. [Protocol Kit](https://docs.safe.global/sdk/protocol-kit), [read-method reference](https://docs.safe.global/reference-sdk-protocol-kit/overview), [API Kit](https://docs.safe.global/sdk/api-kit).

## Blockaid

The official TypeScript client is `@blockaid/client`. Its documented `client.evm.jsonRpc.scan(...)` accepts a wallet-style request, including typed-data signatures. Select the supported chain and inspect the installed client's request/response types rather than constructing guessed tool names. User-owned API access is required; preserve environment selection. Bound retries and distinguish API failure from a completed scan. Do not send a signature or seed phrase merely to analyze unsigned data. [Official client and examples](https://github.com/blockaid-official/blockaid-client-node).

## GoPlus

The documented token-risk read is `GET https://api.gopluslabs.io/api/v1/token_security/{chain_id}?contract_addresses=...`. Resolve exact chain and contract; follow current authorization and response-field rules. Risk flags are observations, not audited guarantees; absent fields and unsupported chains must remain unknown. The broader product includes approval, signature-decoding and transaction-simulation surfaces, so select the endpoint matching the proposal. [Token security reference](https://docs.gopluslabs.io/reference/tokensecurityusingget_1), [API overview](https://docs.gopluslabs.io/reference/api-overview).
