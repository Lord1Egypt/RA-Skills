---
title: Uniswap v2/v3 Liquidity Math
---

# Uniswap Liquidity Math Reference

## Uniswap v2: Constant Product AMM

### Core Formula
```
x * y = k
x = token0 reserve (e.g. ETH)
y = token1 reserve (e.g. TOKEN)
k = constant (invariant)
```

### Price & Impact
```
spot_price = x / y  (token1 per token0)

trade_size_in = Δx
tokens_out = y * Δx / (x + Δx)   [ignoring fees]
tokens_out_with_fee = y * Δx * 997 / (x * 1000 + Δx * 997)

price_impact = 1 - (tokens_out / (spot_price * Δx))
             ≈ Δx / (x + Δx)
```

### Initial Liquidity Sizing
```
Target: price_impact < 1% for typical retail order (Δx)

Required reserve x ≥ Δx / 0.01

Example: Δx = $10,000 retail buy
→ Need $1,000,000 in ETH/USDC side of pool

TVL = 2 * x_usd   (both sides equal at launch)
→ Need $2M TVL for <1% impact on $10k trade
```

### Impermanent Loss (v2)
```
price_ratio r = new_price / initial_price

IL = 2√r/(1+r) - 1

r=1.25 → IL ≈ -0.6%
r=1.5  → IL ≈ -2.0%
r=2.0  → IL ≈ -5.7%
r=4.0  → IL ≈ -20.0%
r=0.5  → IL ≈ -5.7%
```

---

## Uniswap v3: Concentrated Liquidity

### Tick System
```
price = 1.0001^tick
tick  = log(price) / log(1.0001) ≈ log(price) * 1.0001

tick spacing by fee tier:
  0.05% pool → tickSpacing = 10
  0.30% pool → tickSpacing = 60
  1.00% pool → tickSpacing = 200

Ticks must be multiples of tickSpacing
```

### Price Range → Ticks
```python
import math

def price_to_tick(price, tick_spacing=60):
    tick = math.log(price) / math.log(1.0001)
    # Round to nearest valid tick
    return round(tick / tick_spacing) * tick_spacing

# Example: TOKEN = $0.01, range ±30%
listing_price_usd = 0.01
p_low  = listing_price_usd * 0.70   # $0.007
p_high = listing_price_usd * 1.30   # $0.013

# If pool is TOKEN/USDC (USDC=token0, TOKEN=token1):
# price = USDC per TOKEN
tick_lower = price_to_tick(p_low)
tick_upper = price_to_tick(p_high)
print(f"tickLower={tick_lower}, tickUpper={tick_upper}")
```

### Capital Efficiency vs v2
```
Concentration factor = full_range_TVL / concentrated_TVL
                    ≈ √(P_upper/P_lower) / (√(P_upper/P_listing) - 1 + √(P_listing/P_lower) - 1 + ...)

Approximation for ±P% range:
  factor ≈ 1 / (2 * (√(1+P%) - 1))

±10% range → ~5x efficiency
±20% range → ~3x efficiency
±50% range → ~1.5x efficiency
```

### v3 Initial Liquidity Position
```
Given: listing_price P, token budget T_tokens, ETH budget T_eth

At price P within range [P_a, P_b]:
  L = T_eth / (1/√P - 1/√P_b)
  L = T_tokens / (√P - √P_a)

Required ETH = L * (1/√P_a - 1/√P_b)
Required TOKEN = L * (√P_b - √P_a)
```

### Fee Tier Selection
```
0.01% (1bp)  → Stable pairs (USDC/DAI)
0.05% (5bp)  → Major pairs (ETH/USDC, BTC/ETH)
0.30% (30bp) → Standard — best for new token launches
1.00% (100bp) → Exotic/volatile pairs
```

**Recommendation for new token:** 0.30% fee, ±20–30% initial range.

---

## FDV & Market Cap Analysis

```
FDV (Fully Diluted Valuation) = total_supply × listing_price
MC (Market Cap at launch)     = circulating_supply × listing_price
Float ratio                   = MC / FDV  → target >10% at launch

Liquidity ratio = pool_TVL / MC
  < 5%   → thin market, manipulation risk
  5–15%  → healthy for new token
  > 20%  → overcapitalized (opportunity cost)

Round valuation check:
  Seed_FDV ≥ 5x Listing_FDV → red flag (over-valued seed)
  Typical: Listing_FDV = 3–8x Seed FDV for venture-backed tokens
```

## Listing Price Discovery

```
Comparable tokens (comps) approach:
  1. Find 3–5 comparable tokens by sector + market cap stage
  2. Calculate average FDV at launch
  3. Apply discount/premium based on differentiation

Bottom-up approach:
  target_FDV = team_runway + 3x raise + protocol_value_estimate
  listing_price = target_FDV / total_supply

Investor return check:
  seed_price = raise / seed_allocation_tokens
  min_listing = seed_price × 2  (2x min for seed investors)
  recommended_listing = seed_price × 3–5
```

## Bonding Curve Alternative (no AMM)

For projects not using Uniswap immediately:
```
Linear bonding curve:
  price(s) = m * s + b
  where s = tokens sold, m = slope, b = initial price

Cost to buy n tokens starting at supply S:
  cost = m*n*S + m*n²/2 + b*n

Bancor-style reserve ratio:
  price = reserve_balance / (supply × reserve_ratio)
  reserve_ratio = 0.1–0.9 (higher = more stable price)
```
