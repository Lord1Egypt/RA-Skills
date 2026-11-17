# Yield providers and integration routes

Primary-source review: **2026-09-05**. Documented tools below are not automatically installed or connected and are not claimed to have been transaction-tested by this skill. Provider APIs, product versions and current deployment parameters must be checked when used.

| Provider | Preferred official route | Product boundary |
| --- | --- | --- |
| Pendle | Official `pendle-finance/pendle-ai`, V2 API/MCP | PT/YT/SY and maturity; Boros is separate margin trading |
| Yearn | Kong GraphQL, current vault contracts | V2 versus V3; strategy queues, fees and loss tolerances |
| Spark / Sky | Savings vault/PSM contracts and address registry | Mainnet sUSDS, cross-chain tokens and Savings V2 differ |
| Morpho | Official Earn skill, `@morpho-org/morpho-sdk` and API | Vault V2 preferred; V1 compatibility is explicit |
| Euler | Official `euler-earn` and V2 SDK | Earn strategy vault versus a lending EVK vault |
| Ethena | Official sUSDe contracts and issuer/RFQ docs | Staking USDe differs from direct mint/redeem or LP locking |

## Pendle

[pendle-ai - Pendle Finance](https://github.com/pendle-finance/pendle-ai/blob/main/README.md) is an official beta plugin/skill collection. V2 has hosted Streamable HTTP MCP `https://api-v2.pendle.finance/core/mcp`; use live discovery before relying on tool names. The [V2 API documentation - Pendle Finance](https://api-v2.pendle.finance/core/docs) is the official schema source for data and transaction preparation.

[PT mechanics - Pendle Finance](https://docs.pendle.finance/pendle-v2/ProtocolMechanics/YieldTokenization/PT): one PT at maturity is a claim measured in its accounting asset, not necessarily one raw yield-bearing token. An ETH-denominated PT may redeem to ETH-value in a receipt token. Verify the supported output route and any subsequent swap. Fixed yield applies to execution price and successful maturity settlement; an early sale is market-priced.

[YT mechanics - Pendle Finance](https://docs.pendle.finance/pendle-v2/ProtocolMechanics/YieldTokenization/YT): future yield ends and YT value reaches zero at maturity, while accrued rewards may remain claimable. Show purchase cost, remaining horizon, fee/reward assumptions and break-even yield; do not imply PT-like principal redemption.

[Boros plugin - Pendle Finance](https://github.com/pendle-finance/pendle-ai/blob/main/packages/plugins/pendle-boros/README.md) uses local `@pendle/boros-mcp` for delegated trading and browser-wallet sensitive flows. [Boros SDK - Pendle Finance](https://docs.pendle.finance/boros-dev/Backend/sdk) names `@pendle/boros-sdk-public`, replacing an internal package. These are derivatives tooling; do not enable trading or transfer agent keys for a passive yield comparison.

## Yearn

[Data Services - Yearn](https://docs.yearn.fi/developers/data-services/yearn-data) documents public Kong GraphQL at `https://kong.yearn.fi/api/gql`. [yDaemon source - Yearn](https://github.com/yearn/ydaemon) labels itself legacy and recommends Kong, although the docs retain conflicting language about current vault data. Prefer Kong for covered data, document any necessary compatibility fallback, and compare fresh contract state before a transaction.

[VaultV3 - Yearn](https://docs.yearn.fi/developers/smart-contracts/V3/VaultV3) distinguishes assets versus shares and documents a critical asymmetry: `withdraw` defaults to no loss, while `redeem` defaults to allowing realized losses. Specify `max_loss` in basis points explicitly for the requested risk tolerance. Check `apiVersion`, owner-specific limits and strategy queue order; a wrong queue can misstate maximum exits.

[Vault management - Yearn](https://docs.yearn.fi/developers/v3/vault_management) describes accountant fees, strategy debt, profit unlocking and limit modules. Compare share-price observations over an appropriate window, not an isolated harvest as a guaranteed annual rate. No official agent transaction MCP was established.

## Spark / Sky

[Spark Savings V2 - Spark](https://docs.spark.finance/dev/savings/spark-vaults-v2) accrues share value using per-second `vsr`. Accounting assets are not idle liquidity. `previewWithdraw` and `previewRedeem` can revert when liquidity is insufficient; `convertToAssets` plus actual liquidity/limits is the non-reverting estimate route. A permissioned taker deploys liquidity outside the vault.

[Savings Vault Intents - Spark](https://docs.spark.finance/dev/savings/savings-vault-intents) provides request-based large exits. The latest request replaces the prior one for that account/vault without a cancellation event; relayer fulfillment is all-or-nothing and depends on allowance, shares and deadline still being valid. Creation is not settlement.

[Current documentation index - Spark](https://docs.spark.finance/llms.txt) routes mainnet sUSDS and cross-chain token implementations separately. Spark/Sky PSM fees and limits should be read onchain even when documentation currently describes zero fees. Do not reuse mainnet ERC-4626 calls against a bridged representation.

## Morpho and Euler

[Official builder skills - Morpho](https://docs.morpho.org/developers/agents/skills/) provide `earn-integration`, current Vault V2 data, SDK flows and liquid/illiquid exits. Vault APY, rewards, curator configuration, allocation/liquidity and fees need separate fields. [Morpho MCP - Morpho](https://docs.morpho.org/developers/agents/mcp/) is explicitly experimental and not recommended for production yet; keep stable SDK/API paths primary and inspect preparation warnings.

[Agent skills - Euler](https://docs.euler.finance/llms/) include `euler-earn`; [Euler SDK - Euler](https://docs.euler.finance/build/sdk/) supplies current account/vault reads and transaction plans. Inspect strategy allocation, roles, fees, caps, queues and loss accounting. An Earn vault's ERC-4626 interface does not make every strategy liquid or equally risky.

## Ethena

[Staking Key Functions - Ethena](https://docs.ethena.fi/solution-design/staking-usde/staking-key-functions) documents sUSDe's configurable unstaking cooldown and freeze permissions. Read the live cooldown and request state instead of assuming seven days or confusing staking with separately locked campaign positions.

[sUSDe Rewards Mechanism - Ethena](https://docs.ethena.fi/protocol-overview/rewards-mechanism) explains weekly accounting/distribution; annualizing a recent payment can differ from the provider's stated APY. [Order validity - Ethena](https://docs.ethena.fi/solution-design/minting-usde/order-validity-checks) requires whitelisted KYC/KYB for direct mint/redeem and distinguishes RFQ, signed order, expiry, last-look and submission. Secondary-market acquisition does not confer issuer access. No official agent MCP was established.

## Interface standards

[ERC-4626 - Ethereum Improvement Proposals](https://eips.ethereum.org/EIPS/eip-4626) standardizes single-asset vault shares, conversion, preview and limits. [ERC-7540](https://eips.ethereum.org/EIPS/eip-7540) adds asynchronous request workflows; [ERC-7575](https://eips.ethereum.org/EIPS/eip-7575) addresses multi-asset vault interfaces. Detect the actual implementation and supported extensions. A standard name alone does not establish liquidity, authorization, loss limits or safety.
