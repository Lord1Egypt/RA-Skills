# Official Aave V3 MCP procedure

Reviewed 2026-10-08 against [official safe-transactions skill](https://github.com/aave/skills/blob/main/plugins/mcp/skills/safe-transactions/SKILL.md), [confirmation skill](https://github.com/aave/skills/blob/main/plugins/mcp/skills/tx-confirmation/SKILL.md) and [live tool contract documentation](https://aave.com/docs/mcp/tools). Source procedures are linked, not copied.

Discover `get_markets` with `version: v3`, applicable `symbols` and actual `user`; preserve returned `market`, `token`, `chainId`. These selectors are not V4 opaque IDs or recalled Pool addresses. Read summary/reserve before previewing the exact action. Inspect `tools/list` as current argument authority.

MCP amounts are human-unit positive decimal strings: six-decimal token 100000 base units becomes `"0.1"`. Percent `Pct` fields differ from ratios. Do not transplant these units into raw Pool contract calls. `native` with `max` is not supported for V3 repay; use an explicit native amount or the documented wrapped-token mode.

Run `preview_action` before preparation. Error warnings stop the requested action; warnings reach the user. A health preview does not establish ERC20 allowance. Inspect V3 `ApprovalRequired`, permits, pre-contract gateway and transaction branches. Rebuild only after real approval state or an authorized permit with its actual deadline. Supply does not create borrowing power without collateral enablement.

V3 confirmation uses actual receipt plus updated positions/activity. `get_transaction_processed` is V4-only and requires builder operations; never use it as a V3 explorer. Activity supplies neither arbitrary receipt nor gas/block proof. An absent indexed row is unknown without chain corroboration.

For cross-chain V3 comparisons, preserve `chainsCovered`, `chainsNotCovered` and `chainsNotServed`; default unfiltered discovery can be narrower than symbol-filtered discovery. A displayed highest APY is not an enterable market: read available liquidity, caps, flags and user constraints. Refresh current schemas rather than promoting a documented default to a universal scope.
