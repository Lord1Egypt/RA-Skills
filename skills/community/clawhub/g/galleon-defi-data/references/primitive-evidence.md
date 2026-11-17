# Evidence across DeFi primitives

Sources accessed 2026-09-05. These are data interpretation procedures, not transaction adapters.

| Primitive | Preserve | Common misleading comparison |
|---|---|---|
| Lending | Deployment/version, collateral and debt assets, oracle units, variable/fixed term, caps, available liquidity, borrow and liquidation thresholds, accrued interest | A single APY or health-factor formula applied across Aave, Morpho, Compound and Euler |
| Vaults | Share and asset decimals, accounting ratio, fees, exit liquidity, queue state, user-specific limits, block/time | Share balance treated as underlying balance or `totalAssets` treated as immediately withdrawable cash |
| Yield tokens | PT/YT/SY identity, accounting asset, maturity, discount and accrued claimable yield | PT assumed redeemable for one raw underlying token, or YT assumed to retain future yield after maturity |
| Staking | Rebase or exchange-rate model, slashable exposure, queue request, eligibility/finality and claim owner | Queued stake counted as liquid wallet cash or a historical waiting period promised as fixed |
| Derivatives | Venue/subaccount, collateral, net/gross notional, funding/borrow costs, maintenance margin, order/fill state | Posted margin confused with full exposure, or an order accepted by an API called a fill |
| Tokenized assets | Exact issuer/product, eligibility, NAV timestamp, transfer restrictions, market hours, redemption terms | Secondary-market price treated as guaranteed issuer redemption or proof of onboarding |
| Payments | Asset, recipient, authorized cost, transaction/payment ID, settlement and delivery evidence | HTTP success treated as settled payment, or funded stream treated as fully received income |

## Standards and protocol evidence

[ERC-4626](https://eips.ethereum.org/EIPS/eip-4626) distinguishes shares from assets, idealized conversion from previews, and previews from user limits. Preserve rounding and operation direction. `convertToAssets` is not an executable withdrawal quote and a preview does not establish balance/allowance or capacity.

[ERC-7540](https://eips.ethereum.org/EIPS/eip-7540) adds asynchronous request, pending and claimable states. Discover supported interfaces and inspect the actual implementation. Do not assume synchronous preview methods work for an asynchronous flow, or aggregate pending and claimable amounts twice.

Use primary protocol state alongside aggregators: [Aave](https://aave.com/docs/llms.txt) distinguishes V3 and V4, [Morpho](https://docs.morpho.org/developers/agents/skills/) separates variable and fixed-term borrowing, and [Yearn data services](https://docs.yearn.fi/developers/data-services/yearn-data) supplies Kong. [yDaemon](https://github.com/yearn/ydaemon) identifies itself as legacy even where older docs still recommend it. Record contradictory source guidance and choose the current supported interface.

## Portfolio composition

Canonicalize chain, contract/mint, account, protocol deployment and position ID. Distinguish owned, staked, delegated and smart-wallet custody. A receipt token and its underlying claim represent one economic exposure; retain both identities but count value once. Separate debt and pending liabilities. Missing prices remain unknown; they are not zero. Mark estimates with timestamp and method, and disclose stale or shared upstream feeds.

Keep fee yield, token incentives, leverage, price changes and financing costs separate before annualizing. A quoted APY is neither a forecast nor an executable net return. Realized PnL requires cash-flow and cost-basis evidence; deposits, withdrawals and internal transfers are not trading performance. A portfolio report is not a tax determination.

## Review cases

- A vault has 100 shares worth 120 assets: report one 120-asset claim, not 220.
- A bridge source confirms but destination is unknown: retain an in-flight claim and unresolved chain risk, not a completed destination balance.
- Two aggregators use the same CoinGecko feed: label shared provenance, not independent corroboration.
- The protocol upgraded while an indexer still exposes old fields: stop mechanical comparisons until version and units match.
- A debt field is missing: report incomplete net worth; never silently set debt to zero.
