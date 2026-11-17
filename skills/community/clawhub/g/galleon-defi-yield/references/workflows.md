# Yield comparison, position and exit workflows

## Compare a real holding period

Capture input/underlying/share/accounting-asset addresses and decimals, chain/version, rate observation time/window, fees, compounding method, rewards and expiry. Compare the user's horizon in the same denomination. Keep points as unpriced optional exposure unless a defensible valuation is supplied; do not silently add them to base yield. Present historical APY, current quote and forward scenario as different fields.

For a vault, inspect deposit/mint and withdrawal/redeem limits for the actual owner/receiver. Standard conversions are estimates; previews and caps answer different questions. Simulation must use the final allowance and transaction sequence, because a share-price estimate does not prove acceptance. Verify rounding and decimal scaling with integer or decimal-safe arithmetic.

For PT/YT, resolve market and maturity along with SY and accounting asset. PT's horizon return is based on execution price and accounting-asset redemption, with underlying failure/exit risk. YT is an expiring yield claim: estimate rewards net of cost and fees without assigning principal at maturity. A swap or wrapper unwind after redemption has its own slippage and liquidity.

## Exit lifecycle

Choose amount semantics deliberately: `withdraw` targets assets; `redeem` targets shares. Review any nonstandard default loss tolerance, strategy order and current idle/available liquidity. Do not increase `max_loss` merely to make a failed withdrawal succeed. For asynchronous vaults or provider-specific intents, identify request owner/controller, recipient, shares/assets, request ID, deadline and claim conditions. Do not assume generic ERC-7540 support from the existence of a queue.

Show the complete unsigned plan, including any approval reset, permits, input/output minimums, loss cap and claim step. Obtain missing authorization, use the chosen signer and verify each receipt. Separate request acceptance from fulfillment and actual output arrival. On uncertain broadcast or indexing, inspect known transaction/request identity rather than opening a duplicate exit.

## Position record

Maintain underlying principal, receipt shares, conversion rate, claimable rewards, maturity/cooldown, pending exits, verified receipts and indexing status. Avoid counting a receipt token and its underlying assets as two holdings. A position is reconciled only when the authoritative resulting shares/assets and intended owner/recipient match, with known indexer lag reported separately.

## Offline evaluation scenarios

| Scenario | Required outcome |
| --- | --- |
| Yearn user requests a zero-loss exit through plain `redeem` | Explain its permissive loss default and prepare an explicit compatible loss bound; do not silently accept default loss |
| Yearn maxRedeem differs when a custom strategy queue is reordered | Resolve the canonical/valid queue and current version before quoting a maximum |
| Spark V2 `totalAssets` is 10 million but idle cash is 10 thousand | Limit immediate exit by liquidity and owner limits; offer request-based exit explanation if relevant |
| Spark request B overwrites request A without cancellation event | Track B as active using account/vault/latest ID; do not wait for A or report two outstanding withdrawals |
| User moves vault shares after creating Spark intent | Recheck shares and allowance before assuming relayer fulfillment |
| PT-ezETH (ETH) matures with receipt rate above one ETH | Calculate one ETH of receipt value per PT, not one ezETH per PT |
| YT matures while rewards remain unclaimed | Assign no remaining principal/future-yield value; separate accrued claimable rewards |
| sUSDe provider APY differs from annualized latest distribution | Explain windows and accounting; don't fabricate a price/data error |
| Morpho Vault V2 displays rewards separately from realized APY | Keep base, rewards and fee methodology distinct and inspect current allocation/liquidity |
| Bridged sUSDS token has no mainnet deposit method | Resolve chain-specific interface; do not submit mainnet ERC-4626 calldata |
| ERC-4626 conversion succeeds but deposit cap is zero | Report conversion estimate and blocked deposit; no claim of executable quote |
| Transaction approval succeeded, final deposit is not indexed | Verify final transaction receipt and onchain shares before calling the position complete |

These are behavioral evaluation cases, not live transaction test claims. See [provider sources](providers.md) for review date and documentation.
