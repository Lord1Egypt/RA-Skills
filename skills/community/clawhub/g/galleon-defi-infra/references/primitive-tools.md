# Wiring tools across DeFi primitives

Reviewed 2026-09-05 against [Agent Skills](https://agentskills.io/specification), [Hermes skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/), [Hermes MCP](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp/) and the primary provider sources below. Documentation availability is distinct from a tested connection. No authenticated protocol action was performed for this review.

## Reuse by interface, not provider branding

| Interface | Examples | Setup decision |
|---|---|---|
| Official hosted MCP | [Aave](https://aave.com/docs/llms.txt), [Morpho](https://docs.morpho.org/developers/agents/mcp/), [Pendle](https://github.com/pendle-finance/pendle-ai), [Snapshot](https://docs.snapshot.box/tools/snapshot-mcp) | Verify official origin, transport, account/plan and live tool schema. Morpho explicitly labels its MCP experimental and unsuitable for production; prefer its stable SDK for production workflows. |
| Documentation MCP | [Relay](https://docs.relay.link/resources/developing-with-ai), [Jupiter documentation](https://developers.jup.ag/docs/ai/mcp) | Reference retrieval does not provide a signer, transaction builder or market-data service. Jupiter's separate Trading MCP has a different scope and endpoint. |
| Official SDK / upstream skills | [Euler](https://docs.euler.finance/llms/), [Morpho skills](https://docs.morpho.org/developers/agents/skills/), [Uniswap](https://developers.uniswap.org/docs/uniswap-ai/overview), [Sablier](https://docs.sablier.com/guides/ai-agents) | Read the relevant upstream skill and pin a reviewed version only when needed. Keep Hermes as the harness even when an example targets another assistant. Do not vendor provider runtimes. |
| Account-backed simulation | [Tenderly MCP](https://docs.tenderly.co/ai-tools/overview) | Verify the current documentation route, entitlement and project. Simulation may consume credits or persist sensitive calldata; broader tools may mutate infrastructure. Discover first and expose only reviewed operations. |

No provider is enabled merely because it appears in a reference. Select the smallest set that completes the requested task. Tools that return unsigned calldata can still consume credits, disclose addresses or create records. Read-only annotations are hints; inspect the tool's actual contract. Exclude broad execute/product proxies, account setup, signing, automation and receipt-writing tools unless specifically needed and authorized.

## Hermes and progressive disclosure

Place complete skill folders in the intended profile's skills directory. Keep portable name/description/license and string-valued metadata; do not require another pack's files. Hermes can load metadata, then `skill_view` and individual references on demand. Avoid injecting the entire corpus or every provider schema into the system prompt.

Use native MCP configuration and reviewed commands for the installed Hermes version. Inspect install manifests and bootstrap steps. Set exact `tools.include` names and disable unneeded resource/prompt wrappers. A broad wildcard or exclusion list can silently expose new write tools. If discovery fails, leave the connection disabled or preserve a known narrow allowlist; do not fall back to all tools. Native install success is not proof of successful discovery. Recheck after schema changes and preserve the user's selected scope.

Keep credentials in the active private runtime, not skill YAML or provider examples. An OAuth flow may provision an alias, wallet or delegated signer. Distinguish connection authorization from financial/public-action authority. The runtime's tools, wallet policies and user instructions enforce permissions; a skill alone does not.

## EVM and Solana transaction context

EVM chain IDs, CCTP domain IDs, protocol market IDs and Solana cluster identities are separate namespaces. Resolve each from current official deployment metadata; never substitute a symbol or a chain name without validation.

For [Solana transactions](https://solana.com/docs/core/transactions), inspect fee payer, signer set, instructions and account permissions. Resolve address lookup tables before reviewing a versioned transaction; check recent blockhash/expiry or durable nonce semantics. Preserve the provider's block/slot commitment. Refresh expired transactions through the official builder and re-review economic terms before signing. A returned signature is not a successful transaction; reconcile error status and resulting accounts. Do not transplant EVM nonce or allowance assumptions into Solana.

For multi-step EVM operations, reconcile each approval receipt before rebuilding dependent calls. Keep quoted state/block, gas payer, spender, token limits, typed-data domain and deadline. A prepared plan is not immutable if a quote, route, state or recipient changes.

## 2026-10-08 platform update

[Base migration notice](https://docs.base.org/sdks/migrated-products) redirects former agent documentation to Coinbase Wallet MCP. Use the current [wallet models](wallets.md), preserving account/session distinctions and existing authority. Do not rewrite private profiles or reconnect an account as a documentation maintenance step.

[Alchemy CLI](https://www.alchemy.com/docs/alchemy-cli) includes data, simulation, wallets and administration. `alchemy evm contract call` is state-changing; generic `evm rpc` can invoke write methods. Classify the exact operation from its schema and method, not its familiar verb or JSON output flag. Paid request estimation and an automatically paying x402 request are separate capabilities.

[Tenderly MCP](https://docs.tenderly.co/ai-tools/tools) needs explicit active project/network/virtual context. Entitlement or quota failures are not cured by repeatedly reauthenticating. Traces/events have bounded output; use documented detail navigation or report coverage gaps. Simulation may inject state or bypass checks, so successful output does not prove a real wallet has funds or signing permission.

For unsigned intent construction or reproducible simulation, use installed `galleon-defi-agent-plan`/`galleon-defi-agent-simulate` when available. Infra remains independently usable for connection and permission readiness; the separate procedures are optional.
