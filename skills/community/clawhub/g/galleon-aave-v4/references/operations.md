# V4 official interface procedure

Primary documentation reviewed 2026-10-08. Installed tool schemas and observed chain state govern actual use.

## Tool discovery and selectors

[Aave MCP getting started](https://aave.com/docs/mcp/getting-started) documents the keyless HTTP endpoint `https://mcp.aave.com`, root POST and `/mcp` alias. The server supplies `tools/list`; use it as the argument authority. It does not offer an SSE GET stream. Clients using the 2026 protocol revision need its documented `Mcp-Method`/`Mcp-Name` headers; use the existing client's negotiated transport rather than inventing a handshake. Shared limits can produce 401/429.

[Aave tools](https://aave.com/docs/mcp/tools) expose V4 `get_hubs`, `get_hub_assets`, position items and operations-aware confirmation. Supply/borrow reserve selectors come from current `get_markets`; withdraw/repay selectors come from `get_position_items` for the exact owned position. Opaque reserve IDs differ from Spoke, Hub-asset and user-position IDs; preserve each in its own argument namespace. Parse the successful envelope from `data` and inspect warnings. Main-unit decimal amounts differ from raw contract inputs. Supply/APY context can share Hub accounting across spokes; do not call those independent sources.

## AaveKit implementation route

[V4 TypeScript](https://aave.com/docs/aave-v4/getting-started/typescript) currently documents `@aave/client@next`; V3 uses a different distribution track. Pin a reviewed compatible version when implementing. Read-only client actions need no wallet. Await `ResultAsync`, branch on `isOk()`/`isErr()`, and preserve the actual failure instead of converting it to empty positions. Display overrides change names/icons, not the underlying token identity.

[Borrow](https://aave.com/docs/aave-v4/positions/borrow), [repay](https://aave.com/docs/aave-v4/positions/repay) and [withdraw](https://aave.com/docs/aave-v4/positions/withdraw) carry their own conditions and plans. Inspect the SDK's current union rather than assuming every result is a `TransactionRequest`. A balance failure is not approval to fund the wallet.

## Plan branches

The MCP action union documents `TransactionRequest`, `Erc20ApprovalRequired`, `PreContractActionRequired` and `InsufficientBalanceError`. An approval may offer `bySignature`; if the authorized user signs it, rebuild with `permitSignature` and the message's actual `permitDeadline`. Otherwise wait for the `byTransaction` receipt and visible allowance. Never fabricate a permit argument on the first call.

Native gateway plans have `transaction` before `originalTransaction`. Preserve order and check each payload. V4's `get_transaction_processed` consumes the exact `operations` returned by preparation. Corroborate a receipt independently; the activity feed cannot supply arbitrary receipt, gas or block information.

## Liquidation scope

[V4 liquidations](https://aave.com/docs/aave-v4/positions/liquidations) use health-dependent bonus and residual-debt constraints. Do not import a V3 fixed close-factor calculation. This skill's default is position planning; a liquidation request additionally needs the actual eligible debt/collateral, receiving account, simulation and separately authorized spending.
