# Arbitrum Morpho deployment pack

Use this pack for Arbitrum first-canary Morpho market work.

## Required live inputs
- Arbitrum RPC URL that returns chain id `42161`
- deployer/signer address and private key supplied only via runtime/local secret handling
- exact collateral and borrow token addresses
- Morpho core address for Arbitrum
- enabled IRM address and LLTV value
- feed funding mode and send/broadcast intent

## Command order
1. `agentic-lending-morpho preflight-morpho-market --input-file ./request.json --format json`
2. Stop unless `safeToRun === true`.
3. `agentic-lending-morpho ensure-feeds-and-deploy-morpho-market --input-file ./request.json --format json`
4. If blocked or waiting, run `agentic-lending-morpho explain-next --run-dir <run-dir> --format json`.
5. Before final success reporting, run `agentic-lending-morpho verify-feed-to-market-handoff --run-dir <run-dir> --format json`.

## Reporting rule
Only report live market success when the wrapper completed, `agent-decision.json.successClaimAllowed === true`, and handoff verification passes.
