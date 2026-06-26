# Api3 Feed Manager

An OpenClaw skill for discovering Api3 feeds, checking whether they are live, classifying the activation/funding path, and executing the currently supported funding flows when possible. Default to discovery, readiness checks, and dry-run planning first; only use signer-backed execution when the operator explicitly asks for it.

## What it helps with

- find supported Api3 chain aliases
- audit feed coverage across chains
- separate activatable feeds from retired or delisted ones
- inspect queue tiers and default activation choices
- prepare exact `buySubscription(...)` Market contract calls for the supported narrow family
- execute guarded funding in the supported exact path
  - `direct`
  - `wrapper` when exact wrapper calldata is derivable safely
  - `auto`
- deploy the deterministic communal Api3 reader proxy when runtime or downstream integration readiness depends on it
- treat signer material as local runtime input rather than committed skill data
- expose machine-usable funding states:
  - `not-needed`
  - `executable`
  - `browser-assisted`
  - `unsupported`
- prepare browser-assisted funding plans when exact execution is not yet available

## What it does not do

- provide universal pure-onchain automation for every funding case
- pretend retired feeds are still available
- replace `SKILL.md` as the agent-facing instruction file

## Main files

- `SKILL.md` - instructions for the agent
- `scripts/bin/api3-feed-manager.js` - local CLI entrypoint
- `scripts/api3-feed-manager.js` - bundled runtime

## Quick examples

```bash
node ./scripts/bin/api3-feed-manager.js supported-chains
node ./scripts/bin/api3-feed-manager.js coverage-audit --chain arbitrum --limit 20
node ./scripts/bin/api3-feed-manager.js queue-plan --dapi-name ETH/USD --rpc-url https://arb1.arbitrum.io/rpc --chain arbitrum
node ./scripts/bin/api3-feed-manager.js deploy-communal-proxy --dapi-name ETH/USD --rpc-url https://arb1.arbitrum.io/rpc --chain arbitrum --private-key <private-key-hex>
```
