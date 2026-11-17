---
name: aerodrome-slipstream
description: "Use when depositing, staking, claiming, withdrawing, or evaluating Aerodrome Slipstream concentrated-liquidity NFT positions on Base. Distinguishes gauge emissions from unstaked fees, checks gauge custody and deployed-version penalties, and prepares a concrete exit."
license: MIT
compatibility: "Read-only EVM RPC and official protocol APIs or UI. Optional Node.js 20 for offline helpers. No signer included."
metadata:
  author: "Galleon Labs"
  version: "0.6.1"
---

# Aerodrome Slipstream

Return the NFT's range, custodian, emissions eligibility, claim estimate, and exact next action. Aerodrome has both classic stable/volatile ERC-20 pools and Slipstream concentrated NFT pools. Identify the model before using any gauge ABI. This recipe covers Slipstream; an ERC-20 LP amount requires the classic pool's own router/gauge flow.

## Identify the real position

1. Pin Base chain ID and read block. Resolve deployment addresses through official Aerodrome sources, then verify on-chain code and ABI/version. An arbitrary link, token symbol or APR widget does not establish the correct pool.
2. Read manager `positions(tokenId)` and `ownerOf(tokenId)`. Slipstream's pool key uses **tickSpacing**, unlike Uniswap v3's fee field. Read factory `getPool(token0,token1,tickSpacing)` and compare the returned pool's token order, spacing and current price. Do not assume fee equals spacing or remains fixed.
3. Resolve the pool's gauge through the verified voter `gauges(pool)`. Verify gauge `pool()`, `nft()`, `voter()`, `token0()`, `token1()` and `tickSpacing()` against those reads. Read `isAlive(gauge)` on its voter. A dead gauge is not a deposit candidate even when the pool remains swappable.
4. If ownerOf is the wallet, the NFT is unstaked. If it is the gauge, read `stakedContains(wallet,tokenId)` or `stakedValues(wallet)`. A gauge-owned NFT with no matching depositor record is unresolved custody, not a lost NFT or wallet-owned position. Unknown vault/Sickle ownership requires its withdrawal procedure.

## Decide between fees and emissions

For the verified gauge model, staking receives emissions instead of the unstaked position's trading fees. Show these alternatives separately, using the user's range and active liquidity rather than adding both headline APRs. Read `rewardToken()`, token decimals, `periodFinish()`, `rewardRate()` and current range. Out-of-range capital does not earn in-range emissions merely because its NFT is staked.

Read `earned(wallet,tokenId)` only for a confirmed stake. Treat the result as block/version-specific; inspect whether that implementation requires a reward-growth update for an accurate simulation. Do not send a state-changing update solely to obtain a quote. Simulate the relevant claim path when available.

Current upstream includes `depositTimestamp(tokenId)` and gauge-factory `penaltyRate()`/`minStakeTimes(pool)`. These are version-dependent, not promises about every deployed gauge. Confirm deployed selectors/source first. Where supported, compute the earliest penalty-free time and simulate the actual claim/withdrawal. Do not subtract a penalty again if `earned` already returns net claimable reward. An older implementation without these methods needs its own verified semantics.

## Prepare the selected lifecycle

- **Stake:** verify ownership, matching pool, alive gauge and positive liquidity. Prepare NFT-specific `approve(gauge,tokenId)` if needed, then gauge `deposit(tokenId)`. Re-read custody and depositor membership. Do not substitute an ERC-20 approve or require blanket `setApprovalForAll`.
- **Claim:** use the owner's `getReward(uint256 tokenId)` overload. The `getReward(address account)` overload can be voter-restricted. Include reward token, expected net amount, penalty assumptions and gas cost.
- **Exit gauge:** gauge `withdraw(tokenId)` returns custody and may collect emissions/fees in the verified implementation. Confirm ownerOf and membership before any manager operation; do not assume a second claim remains necessary.
- **Remove liquidity:** after withdrawal, use the deployed manager's decrease and collect interface with minimums, recipient and deadline. Some newer versions support special staked-liquidity operations; use them only after verifying that implementation. A normal wallet-owned manager recipe cannot simply operate on a gauge-owned NFT.
- **Recenter:** withdraw, remove, collect, rebalance if requested, mint a new range, then optionally stake. Keep each dependent ID and amount unresolved until observed or atomically simulated.

The skill is independently usable through reads and an unsigned official UI/tool handoff. Installation does not authorize signing, approvals or transfers. For an explicitly requested action, use an existing authorized wallet tool, exact terms and simulation; never build a signer here. Do not resend an uncertain deposit or withdrawal. Read the original receipt and both custody records first.

## Worked output

Synthetic NFT 42: owner is verified gauge G; stakedContains(Alice,42)=true; current tick equals tickUpper. Report `staked, out of range`, not missing. Suppose this deployed version's earned read returns 90 AERO net of a 10% early-claim penalty and penalty-free time is in 1 hour. The present claim estimate is 90, not 81. Compare waiting against market and gas costs without guaranteeing a future 100. For a user-requested exit, prepare `withdraw(42)` first, then verify Alice owns it before decrease/collect.

## Sources and maintenance

Primary sources checked 2026-09-27. [Protocol recipes and sources](references/recipes.md) contain the concrete calls. Recheck deployments and API schemas before preparing financial actions; documentation access alone proves no live position or transaction.
