# Aave read recipe and worked decision

## Read-only calls

With Foundry already installed, set `RPC_URL`, `PROVIDER`, `POOL`, `ACCOUNT` and numeric `BLOCK` from verified deployment inputs. These are read calls, not a wallet setup.

```sh
cast call "$PROVIDER" 'getPool()(address)' --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$POOL" 'getUserAccountData(address)(uint256,uint256,uint256,uint256,uint256,uint256)' "$ACCOUNT" --rpc-url "$RPC_URL" --block "$BLOCK"
cast call "$POOL" 'getUserEMode(address)(uint256)' "$ACCOUNT" --rpc-url "$RPC_URL" --block "$BLOCK"
```

Use the deployed ABI for further reserve reads; V3 minor versions differ. If only an Aave MCP is available, inspect its advertised tool schemas and version coverage first. Do not invent a method from a UI label or call V4 tools against V3.

## Synthetic worked record

At synthetic block 100, eligible collateral is 10,000 common-base units, applicable liquidation threshold is 80%, and debt is 4,000. Current HF is 2. A proposed extra 1,000 debt gives HF 1.6. A 20% collateral shock and 5% debt-value shock give 6,400 / 5,250 = 1.2190476. With a user floor of 1.3, that proposal fails the stress budget despite passing the current HF test. Under those assumptions total debt budget is 6,400 / (1.3 × 1.05) = 4,688.64; extra debt budget is approximately 688.64 before interest, rounding, liquidity and reserve restrictions. This is an illustrative budget, not transaction readiness.

Missing read example: the indexer shows HF 1.03 but has no block. Return `risk-unverified`; read the pool at a known fresh block and reprice each reserve. Do not claim liquidation has happened or borrow more to repair it.

The bundled [stress calculator](../scripts/stress.ts) accepts already-normalized common-base integers and outputs fixed-point HF and a conservative debt budget. It does not fetch prices, interpret eMode, or validate borrowing permission. From the installed skill directory, run `bun scripts/stress.ts scripts/scenario.example.json`; verify its arithmetic with `bun test scripts/stress.test.ts`. Inputs are nonnegative integer strings, with common-base precision chosen consistently.

## Primary sources checked 2026-09-27

- [Pool interface](https://aave.com/docs/aave-v3/smart-contracts/pool): call signatures and units.
- [Health factor](https://aave.com/help/borrowing/liquidations): liquidation mechanics.
- [Address book](https://github.com/bgd-labs/aave-address-book): select deployment and version at runtime.
- [Positions](https://www.aave.com/docs/aave-v3/markets/positions): maintained SDK read surface.

