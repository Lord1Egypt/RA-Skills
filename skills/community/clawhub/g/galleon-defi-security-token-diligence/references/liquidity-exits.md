# Liquidity custody and executable exits

## Discover enough of the market to support the claim

Record every discovery source, factory/version, searched block interval, pagination and exclusions. Separate the advertised pool from other material pools. Indexer results are a candidate set; verify identities and state with supported onchain reads. If historical indexing is unavailable, narrow the conclusion to observed pools rather than declaring there are no others.

For each position, trace beneficial ownership, manager, token/NFT identifier, approvals, operator, locker and any contract capable of decreasing liquidity, transferring the position, rescuing assets or upgrading those paths. State what is locked, for whom, under which code and for how long. Locked principal does not establish locked fees, price support or in-range liquidity.

## Scanner labels versus verified custody

A scanner's `is_locked=0`, a blank field or a contract named as a locker is not evidence either way. For a concentrated-liquidity NFT, identify the position manager, NFT ID, pool, `ownerOf` at a recorded block, token pair, fee tier and active range. When the owner is a contract, inspect verified source or runtime for principal withdrawal paths, time-gated release, upgrade and emergency roles; fee collection is not principal withdrawal. Attribute custody to what the evidence shows and leave withdrawal rights unresolved until read: neither freely removable nor permanently locked follows from a label. A scanner's share of total LP is not the executable depth at the current tick, because concentrated positions provide depth only inside their ranges; read position bounds and obtain a trade-size quote.

## Uniswap version matters

For v3, verify factory/pool identity and token pair; read the manager's position, owner, approvals and tick range. Analyze principal and uncollected fees separately. Use [official position data](https://github.com/Uniswap/v3-periphery/blob/main/contracts/interfaces/INonfungiblePositionManager.sol) and the matching deployment ABI.

For v4, identify the complete PoolKey and derived PoolId, selected PoolManager, hook and PositionManager. Read the exact pool/position state through the supported [pool-state interface](https://developers.uniswap.org/docs/protocols/v4/guides/read-pool-state). The [singleton](https://developers.uniswap.org/docs/protocols/v4/concepts/poolmanager) holds state for multiple pools; its total token balance is not one pool's reserve. Hook permissions and custom accounting can affect removal and swap outcomes. Do not assume the manager implements ERC721Enumerable; use documented [position discovery](https://developers.uniswap.org/docs/sdks/v4/guides/managing-liquidity/position-fetching) and reconcile indexed history with chain state.

## Show an exit curve at the requested size

Choose a small diagnostic amount and the user's relevant holding sizes; record amounts in exact base units and display units. For each quote, preserve pool/route, caller assumptions, chain state, quote asset, expected output, fee treatment and failure reason. Report per-unit degradation with size. Distinguish market price impact from chosen slippage tolerance and transaction cost. Do not label a price API response an executable quote.

ETH or WETH pairs are valid venues; wrapping or a router's native-input path is an execution step, not a blocker, and a thin stablecoin pool does not veto a deeper WETH route. A pool fee tier is a quantifiable hurdle: two 1% legs lose about 1.99% to pool fees (1 minus 0.99 squared) before impact, gas or taxes. Measure that against the specific thesis rather than treating a fee tier, quote asset or protocol version as a categorical veto. Executable quote amounts already embed pool fees and impact; never subtract them again.

A receipt that shows part of one route leg's output diverted to another recipient is leg-specific evidence. Quantify it from the logs, identify the recipient and its controller, and do not promote it to a token-wide tax or apply it as a blanket haircut without the token's transfer logic or a second independent leg.

A past successful sell proves only the historical caller, route and state. Check current transfer restrictions, exemptions, approval prerequisites and available depth. Quotes from privileged or exempt callers do not establish an ordinary holder's exit. A fork test must record its synthetic accounts, state overrides, transaction receipt, actual payout delta and remaining conversion costs; logs alone can mislead.

If the quote asset is a wrapper, bridge asset or tokenized claim, show the next conversion or redemption constraints. A sale into an unredeemable claim does not satisfy a request to exit into a liquid underlying asset. No live sell or approval is needed for this review.

Primary sources reviewed 2026-09-06. Pool discovery and exit testing remain limited to the recorded universe and state.
