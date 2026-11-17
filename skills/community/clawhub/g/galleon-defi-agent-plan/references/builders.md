# Official builders and capability boundaries

Reviewed 2026-10-08. Documentation research establishes advertised interfaces; it does not establish installed tool versions, provider access or successful execution.

## Nethermind deterministic playbooks

[Official source and README](https://github.com/NethermindEth/defi-skills) document the `defi-skills` Python CLI. `build` has no LLM, signer or broadcaster. Inspect the installed interface before using these read/build commands:

```bash
defi-skills actions --chain-id 8453 --json
defi-skills actions aave_supply --chain-id 8453 --json
defi-skills build --action aave_supply --args '{"asset":"USDC","amount":"100"}' --chain-id 8453 --json
```

Use an existing configured public wallet address or the documented `--wallet` argument; never add a private key. Check `success` before consuming `transactions`. Ordered entries carry `raw_tx` with `chain_id`, `to`, `value` and `data`; the signing wallet still needs sender, nonce and gas. Resolve approved token/spender from each approval. Token resets can add calls.

The published source describes manually maintained addresses and single-hop Uniswap/Balancer routes. Discover chain/action support and cross-check current deployments rather than treating the static resource file as chain proof. `build` and optional LLM-backed `chat` are different paths. Certain resolvers need provider credentials; report the missing variable name without collecting its value in chat.

## Aave official unsigned path

[Aave MCP](https://aave.com/docs/mcp/getting-started) supplies keyless reads and unsigned preparation. Use `tools/list` as the schema authority, then the topic-specific `get_aave_guide` for current IDs, amounts and signing branches. Discovery, health preview, preparation and confirmation are separate observations. A public connection is not a wallet signer.

For operation-specific V3/V4 details, use the dedicated installed lending skill when available. Do not encode a recalled market selector, transform an opaque V4 ID yourself, or mistake main-unit amounts for wei. A successful health preview can still leave an approval prerequisite. Carry builder-returned operation identifiers into the applicable confirmation call.

## Broad platform CLIs

[Alchemy CLI](https://www.alchemy.com/docs/alchemy-cli) combines public data, simulations, wallet signing and administration. Inspect version, JSON schemas and actual available flags. Limit a planning request to data/build/simulation operations; do not use a swap, bridge, send, wallet-creation or app-management command as a lookup. `alchemy evm contract call` is state-changing despite its name. Generic `evm rpc` also permits write methods; schema inspection and a method allowlist are required. CLI availability alone proves none of its permissions.

[WalletConnect Agent SDK](https://github.com/WalletConnect/agent-sdk) is marked beta. Its documented pipe/agent `send-transaction` route may automatically bridge when destination ETH is insufficient. A send-only budget does not authorize that extra transfer. Preflight gas and use a reviewed path with no implicit funding, or report the absent supported mode rather than inventing a disabling flag. Sessions persist; `whoami --json` is inspection, while connection and signing establish different rights.

## When no supported builder exists

Return the missing action/deployment and a concrete official integration route. Do not substitute a similarly named protocol, silently change chains or build calldata against an obsolete ABI. A developer implementing a new playbook must validate resolver inputs, deployment identity and fork behavior separately; this installed skill does not vendor those runtimes.
