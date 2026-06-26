---
name: erc20-tokenomics-builder
description: ERC20 token launch readiness toolkit. Use when designing or auditing tokenomics for a new token project — includes VestingWallet setup (OpenZeppelin), allocation table generation, cliff/vesting schedule modeling, investor documentation, Uniswap v2/v3 liquidity math, and token distribution analysis. Triggers on: token launch, tokenomics design, vesting schedule, token allocation, SAFT/token sale docs, liquidity bootstrapping, Uniswap pool setup, token supply modeling. NOT for: already-deployed token audits (use solidity-audit-precheck), DeFi position tracking (use defi-position-tracker), or general smart contract upgrades.
---

# ERC20 Tokenomics Builder

End-to-end token launch readiness: allocation design → vesting contracts → liquidity math → investor docs.

## Workflow

1. **Gather inputs** — total supply, allocations, unlock schedules, raise target, listing price
2. **Build allocation table** — categories, amounts, percentages, unlock logic
3. **Generate vesting schedules** — cliff + linear using OpenZeppelin VestingWallet
4. **Model Uniswap liquidity** — initial price, pool depth, slippage targets
5. **Draft investor documentation** — token sale summary, SAFT context, vesting proof

---

## 1. Allocation Table

Standard allocation buckets (adjust to project):

| Category         | % Supply | Cliff  | Vesting  | TGE Unlock |
|-----------------|----------|--------|----------|------------|
| Team            | 15–20%   | 12 mo  | 36 mo    | 0%         |
| Investors (seed)| 10–15%   | 6 mo   | 24 mo    | 0–5%       |
| Investors (priv)| 8–12%    | 3 mo   | 18 mo    | 5–10%      |
| Ecosystem/DAO   | 20–30%   | 0      | 48 mo    | 5%         |
| Community/Airdrop| 10–15%  | 0      | 0–12 mo  | 100%       |
| Liquidity       | 5–10%    | 0      | 0        | 100%       |
| Reserve/Treasury| 10–20%   | 0      | Governance| 0–5%      |

**Output format:** Markdown table + CSV for investor decks.

---

## 2. OpenZeppelin VestingWallet

OZ `VestingWallet` handles cliff + linear release natively.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/finance/VestingWallet.sol";

// Deploy one per beneficiary (or use a factory)
// constructor(address beneficiary, uint64 startTimestamp, uint64 durationSeconds)

// Example: 12mo cliff + 24mo linear for team member
// start = TGE timestamp + 12 months (cliff built in by setting start = cliff end)
// duration = 24 months (linear release after start)

VestingWallet teamVest = new VestingWallet(
    teamMemberAddress,
    uint64(tgeTimestamp + 365 days),   // start after 12mo cliff
    uint64(730 days)                    // 24mo linear vesting
);
```

**Key methods:**
- `release(token)` — beneficiary calls to claim vested tokens
- `vestedAmount(token, timestamp)` — query how much is unlockable
- `releasable(token)` — current claimable balance

**Cliff pattern:** Set `startTimestamp = TGE + cliffDuration`. Vesting begins linearly after cliff with no special code needed.

**Multi-beneficiary factory pattern:** See `references/vesting-factory.md`

---

## 3. Vesting Schedule Modeling

Calculate monthly unlock amounts for each category:

```
Monthly unlock (post-cliff) = (allocation_tokens / vesting_months)
TGE unlock = allocation_tokens × tge_pct
Remaining = allocation_tokens × (1 - tge_pct)
Linear_per_month = Remaining / vesting_months_after_cliff
```

**Circulating supply projection formula:**
```
CS(t) = Σ [tge_i + max(0, (t - cliff_i) / vest_i) × (1 - tge_pct_i)] × supply_i
```
Where `t` = months since TGE, `i` = each allocation bucket.

Model month-by-month in a table through month 48. Flag any month where unlock > 5% of circulating supply (selling pressure risk).

---

## 4. Uniswap Liquidity Math

### v2 Pool Setup (constant product: x * y = k)

```
Initial price = ETH_amount / TOKEN_amount
k = ETH_amount × TOKEN_amount

Slippage for trade size S:
  price_impact = S / (ETH_reserve + S)
  tokens_out = TOKEN_reserve × S / (ETH_reserve + S)

Recommended: price impact < 1% for typical retail trade size
→ Pool depth = trade_size / 0.01
```

**Example:** Target $10k retail trade at <1% impact
→ Need $1M TVL in the pool

### v3 Concentrated Liquidity

- Define price range: `[P_low, P_high]` where P = token price in ETH/USDC
- Recommended initial range: ±20–30% from listing price
- Concentrated liquidity = ~10x capital efficiency vs v2 in-range
- Use `tickLower` / `tickUpper` = `log(price) / log(1.0001)`

**Listing price discovery:**
```
FDV_target = total_supply × listing_price
Implied_MC = circulating_supply × listing_price
Liquidity_ratio = pool_TVL / MC  → target 5–15% for healthy launch
```

See `references/uniswap-math.md` for deeper tick/range calculations.

---

## 5. Investor Documentation Templates

### Token Sale Summary (SAFT context)

```markdown
## Token: [NAME] ($TICKER)
- Total Supply: X,000,000,000
- TGE Date: [DATE]
- Network: Ethereum / [L2]
- Contract: [0x...]

## This Round
- Round: Seed / Private / Strategic
- Raise: $X at $Y/token → $Z FDV
- Allocation: X% of supply
- Vesting: X mo cliff, X mo linear, X% TGE
- VestingWallet: [contract address or "to be deployed"]

## Token Release Schedule
[Month-by-month unlock table for this tranche]

## Use of Funds
[breakdown]
```

### Vesting Proof for Investor

After deploying VestingWallet, provide:
- Contract address
- Etherscan link
- `vestedAmount(tokenAddress, block.timestamp)` call
- Next release milestone date

---

## 6. Common Pitfalls

- **Too much TGE unlock for team** → dump signal; keep 0% until cliff
- **Liquidity < 5% of MC** → vulnerable to price manipulation
- **No vesting cliff for advisors** → cheap paper hands
- **FDV too high at listing** → suppresses price for years
- **Missing `release()` automation** → beneficiaries forget; use a keeper script
- **Single VestingWallet per team** → use individual wallets per person for clean cap table

---

## References

- `references/vesting-factory.md` — Solidity VestingWallet factory + batch deployment
- `references/uniswap-math.md` — Detailed Uniswap v2/v3 tick math and liquidity formulas
- `references/allocation-templates.md` — Pre-built allocation tables for DeFi, GameFi, DAO, Infrastructure

## NOT This Skill

- **Already-deployed contract audit** → use `solidity-audit-precheck`
- **LP position monitoring / IL tracking** → use `defi-position-tracker`
- **Safe/multisig treasury management** → use `multi-sig-treasury`
- **General ERC20 contract upgrades** → use `upgrade-solidity-contracts`
