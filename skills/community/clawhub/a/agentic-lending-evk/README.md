# Agentic Lending EVK

Execution-capable EVK skill bundle for Api3-backed lending workflows.

## Install + first command

```bash
npm install <this-package>
part2-planner run-evk-workflow --input-file ./node_modules/agentic-lending-evk/references/example-request.json
```

If you want a top-level entrypoint instead:

```bash
agentic-lending-evk run-evk-workflow --input-file ./node_modules/agentic-lending-evk/references/example-request.json
```

This published skill now carries its own runnable EVK execution surface instead of depending on a separate repo checkout for the planner runtime and core planning artifacts.

## Bundled contents

- packaged skill instructions in `SKILL.md`
- bundled live borrow proof executor in `scripts/evk_live_borrow_proof.js`
- local CLI entrypoint in `scripts/bin/agentic-lending-evk.js`
- bundled EVK planner runtime in `scripts/lib/`
- bundled planning data under `data/part2/`
  - `evk-addresses.api3-supported-overlap.json`
  - `feed-status.json`
  - `market-registry.json`
  - required contract artifacts for the current EVK path

## Published CLI commands

After installing this package, the published executables are:

- `agentic-lending-evk`
- `api3-feed-manager`
- `part2-planner`

## Quick examples

Top-level EVK workflow planning:

```bash
agentic-lending-evk run-evk-workflow --input-file ./request.json
```

Feed discovery or readiness work:

```bash
api3-feed-manager resolve --dapi-name ETH/USD --chain arbitrum --rpc-url https://arb1.arbitrum.io/rpc
api3-feed-manager ensure-active --dapi-name ETH/USD --chain arbitrum --rpc-url https://arb1.arbitrum.io/rpc
```

Lower-level planner entrypoint:

```bash
part2-planner plan-market --input-file ./node_modules/agentic-lending-evk/references/example-request.json
part2-planner prepare-evk-market --input-file ./node_modules/agentic-lending-evk/references/example-request.json
```

## Cold-install expectations

- Node.js `>=20`
- start from `references/example-request.json` and replace placeholder values or planning inputs as needed
- provide a live RPC URL for on-chain checks or transaction-oriented flows
- provide signer material only for explicitly user-approved send paths
- treat bundled planner snapshots as local packaged fallback inputs, not fresh chain truth

## Runtime note

The bundled `feed-status.json` and `market-registry.json` are packaged snapshots for local planning fallback, not global truth.

When live RPC or fresher operator-managed data is available, prefer that newer state over the bundled snapshot.
