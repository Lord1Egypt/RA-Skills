# Official simulation providers

Reviewed 2026-10-08; provider documentation, entitlement and observed execution are distinct.

## Tenderly

[Quickstart](https://docs.tenderly.co/ai-tools/quickstart) documents remote MCP at `https://mcp.tenderly.co/mcp`, OAuth and selected project context. A 403 may mean the plan excludes MCP access; authentication success does not remove that restriction. Inspect current tool schemas and project/network before simulation. The server also offers infrastructure changes, so expose only selected operations for this task.

[Simulation documentation](https://docs.tenderly.co/simulations-and-forks) distinguishes simulated execution from virtual environments and forks. Preserve the actual chain/block, sender, full payload and overrides. Resolve an active virtual environment explicitly instead of accepting whichever context a previous session left selected. Trace/event truncation means missing evidence: request targeted detail or report the omitted coverage.

## Alchemy: deprecated API and unverified CLI capability

[Transaction Simulation notice](https://www.alchemy.com/docs/reference/simulation) says the APIs were deprecated on **2026-09-30**, before this review. The [asset-changes endpoint](https://www.alchemy.com/docs/data/simulation-apis/transaction-simulation-endpoints/alchemy-simulate-asset-changes) repeats that notice. Treat these API recipes as historical; do not recommend them as a supported live service or silently retry a deprecated route.

[CLI documentation](https://www.alchemy.com/docs/alchemy-cli) still advertises simulation alongside wallet and administration commands. That disagrees with the API lifecycle notice and does not establish a replacement backend. Inspect the installed version, exact non-signing command/schema, backend, chain support and current provider statement before a bounded read-only test within existing access. Until those agree and a suitable operation is observed, report the simulation capability unverified and use another user-approved supported provider. Do not invent flags or assume `--json` makes a command non-writing.

Any independently verified replacement still needs single-versus-stateful-bundle semantics and explicit asset, allowance, gas and smart-account coverage. Documentation discovery alone proves neither current access nor simulation success.

## Portals Foresight

[API reference](https://foresight.portals.fi/docs/) documents `/v1/simulate`, sequential `/v1/simulate/batch` and transaction trace/replay. Inspect response `bypassedChecks`, token/native asset changes and complete batch results. Foresight injects balances/allowances/gas and can bypass Safe, permit or ERC-4337 signature checks. HTTP 200 also wraps reverted execution; inspect `success`. These results cannot establish real funding or signer readiness. For batches, the top-level sender executes; `steps[].tx.from` is validated but ignored, and `account` tracks output only. A request with a different intended executor needs a different simulation.

[Official skill surface](https://foresight.portals.fi/docs/skill/) is reference material for the API, not an installed signer. A plan can use key-backed access or paid x402 requests. A keyless paid request remains a purchase; use existing approved budget/rails and never run an automatically paying fetch merely to discover documentation.

## Existing RPC and forks

[`eth_call` and chain reads](https://ethereum.org/en/developers/docs/apis/json-rpc/) can establish bounded execution at a chosen block but do not supply all decoded state changes. An omitted field or empty result is not proof that no authority changed. Record provider limitations explicitly. A local or hosted fork shares neither the real chain's future block production nor a bridge solver's destination execution.

No integration runtime is bundled here. Recheck schemas and supported networks; link documentation when access is missing instead of silently substituting a differently scoped service.
