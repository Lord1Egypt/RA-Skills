# Lending providers and versions

Primary-source review: **2026-09-05**. These are documented integration surfaces, not a claim that each MCP, SDK, deployment or transaction has been tested by this package. Discover current chains, schemas, addresses and versions at use time. Prefer maintained official interfaces; a third-party catalog is not evidence of official support.

| Provider | Official interface | Version/access boundary |
| --- | --- | --- |
| Aave | AaveKit `@aave/client`, GraphQL, documented MCP `https://mcp.aave.com` | Public keyless APIs; distinguish V3 Pools, V4 Hubs/Spokes and Aptos Move |
| Morpho | `@morpho-org/morpho-sdk`, official builder skills, API; experimental MCP `https://mcp.morpho.org/` | Blue variable markets, Midnight fixed-term markets, Earn Vault V2; inspect RPC-chain support |
| Compound | Comet contracts, official documentation and deployments | Compound III base-asset markets are different from V2 cTokens |
| Euler | `@eulerxyz/euler-v2-sdk`, EVC/EVK, official agent skills, data/lenses | Euler V2; do not use the archived legacy SDK |
| Spark / Sky | Official SparkLend contracts, address registry and data providers | SparkLend differs from Morpho-powered Spark Isolated Markets and savings vaults |

## Aave

[Aave Documentation index - Aave Labs](https://aave.com/docs/llms.txt) documents public V3/V4 APIs and MCP for reads, simulation and unsigned preparation. The [V3 TypeScript guide - Aave Labs](https://aave.com/docs/aave-v3/getting-started/typescript) uses the package's `latest` channel; the [V4 guide](https://aave.com/docs/aave-v4/getting-started/typescript) uses `next`. Choose and pin a compatible tested release; do not mix import/plan schemas. `ResultAsync` must be awaited and checked, and signing helpers must not be added to a read-only example.

[V4 liquidations - Aave Labs](https://aave.com/docs/aave-v4/positions/liquidations) use health-dependent Dutch-auction bonuses and residual-debt constraints. Do not apply a fixed V3 close factor to V4. Identify spoke, reserve and chain; verify eligible collateral, debt and post-state. The official plan can include permits, ERC-20 transactions and allowance resets; inspect all steps. A receipt and API indexing are separate confirmation stages.

## Morpho

[Agent skills - Morpho](https://docs.morpho.org/developers/agents/skills/) provides `morpho-org/morpho-skills`: `earn-integration` and `borrow-integration`. Reuse their current SDK/product guidance when building; do not copy a bespoke bundler. Earn defaults to Vault V2. Borrow separates Blue variable-rate from Midnight fixed-rate, fixed-term behavior; read quote, maturity and refinancing conditions for the selected product.

[Morpho MCP - Morpho](https://docs.morpho.org/developers/agents/mcp/) is public, unauthenticated Streamable HTTP and explicitly experimental/pre-v1.0; its documentation says not to build production systems against it yet. Stable SDK/API integration should remain the production path. Query tools support chain IDs; RPC/position/prepare tools require registered slugs whose discovery says `supportsRpcTools: true`. Discover before resolving a market; never infer RPC support from a successful indexed query.

Prepared operations include approvals in their transaction array. Review outcome and warnings; severity `error` stops signing. The server never signs or broadcasts. Vault APY is a realized average; market supply/borrow APY are 24-hour averages, excluding rewards. V2 performance fees and annualized management fees are distinct. Do not treat displayed APY as a current execution rate or LLTV as a safe borrowing target.

## Compound III

[Collateral & Borrowing - Compound](https://docs.compound.finance/collateral-and-borrowing/) distinguishes the single market base token from collateral. Positive base supply earns interest; collateral does not. `supply` may repay a borrow, while `withdraw` may create one. Check the signed base balance, `baseBorrowMin`, caps, recipient and manager permissions before planning either operation.

[Liquidation - Compound](https://docs.compound.finance/liquidation/) uses separate borrow and liquidation collateral factors. `absorb` moves the account's debt/collateral to the protocol; buying protocol collateral is a separate reserves-dependent action. Do not model Comet as V2 repay-and-seize. No official agent MCP was established in this review; use official contract interfaces, not an unverified community server.

## Euler

[Agents and LLMs - Euler](https://docs.euler.finance/llms/) supplies five official skills in `euler-xyz/agent-skills`: vaults, IRM/oracles, Earn, advanced and data. The [Euler SDK - Euler](https://docs.euler.finance/build/sdk/) handles protocol reads, EVC batches, approvals, simulation and execution plans. Select read services for research; execution services do not inherit authority from the skill.

[Liquidations - Euler](https://docs.euler.finance/learn/liquidations/) transfer debt to the liquidator, with a health-dependent discount. Account checks on the receiving account still matter. Verify owner/subaccount, collateral enablement, controller, oracle route and unit, borrow/liquidation LTV, hooks, caps and liquidity. Cool-off and bad-debt socialization are configuration-dependent. No official hosted MCP was established; avoid archived `@eulerxyz/euler-sdk`.

## Spark / Sky

[Spark Documentation index - Spark](https://docs.spark.finance/llms.txt) is the current domain; `.fi` migrated to `.finance`. [SparkLend - Spark](https://docs.spark.finance/products/sparklend) and [Isolated Markets - Spark](https://docs.spark.finance/products/isolated-markets) are distinct. The latter uses Morpho; neither should be assumed to be a current Aave SDK deployment solely from ancestry. Resolve current addresses, source versions, e-mode/isolation settings and oracle routes through the official docs. No retail agent MCP was verified.

Savings sUSDS and Spark Savings V2 are yield-vault products, not the lending Pool. Their share/liquidity and queued exit behavior belong in a separate yield analysis. A stablecoin name or Sky backing does not eliminate price, liquidity or governance risk.
