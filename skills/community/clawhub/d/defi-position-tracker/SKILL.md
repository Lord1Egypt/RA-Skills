---
name: defi-position-tracker
description: >
  Monitor and analyze DeFi positions across protocols and chains. Track LP (liquidity provider) positions,
  staking rewards, yield farming returns, impermanent loss calculations, and cost basis per position.
  Outputs structured data for portfolio reporting, tax handoff to crypto-tax-agent, and treasury dashboards.
  Supports Uniswap v2/v3, Curve, Aave, Compound, Balancer, Lido, and other major protocols.
  Use when: tracking active DeFi positions, calculating IL on LP pairs, monitoring yield across farms,
  preparing DeFi data for tax reporting, or building treasury dashboards for DAOs/funds.
  NOT for: executing DeFi transactions (buy/sell/stake), bridging assets, swapping tokens, or generating
  on-chain payroll (use on-chain-payroll). NOT for: real-time price alerts on spot holdings without
  active DeFi positions. NOT for: NFT portfolio tracking.
metadata:
  category: defi
  tags: [defi, lp, staking, yield, impermanent-loss, multi-chain, crypto, treasury]
  requires:
    optional_bins: [cast, python3, node]
    apis: [DeBank API, Zapper API, Zerion API, The Graph, Moralis, Alchemy, Infura]
---

# DeFi Position Tracker

Monitor LP positions, staking rewards, and yield farming across protocols. Calculate impermanent loss, track cost basis, and feed structured data to crypto-tax-agent for tax reporting.

---

## Supported Protocols

| Category | Protocols |
|----------|-----------|
| DEX LP | Uniswap v2/v3, Curve, Balancer, Velodrome, PancakeSwap |
| Lending | Aave v2/v3, Compound v2/v3, Euler, Morpho |
| Liquid Staking | Lido (stETH), Rocket Pool (rETH), Frax (sfrxETH) |
| Yield Farming | Convex, Yearn, Beefy, Pendle |
| Bridges/xChain | LayerZero positions, Stargate LPs |

## Supported Chains

Ethereum, Arbitrum, Optimism, Base, Polygon, BSC, Avalanche, Fantom, Solana (via Birdeye/Helius).

---

## Core Workflows

### 1. Full Portfolio Snapshot

Pull all active DeFi positions for a wallet address using DeBank Pro API (most comprehensive):

```bash
# DeBank Pro API — full protocol positions
curl -s "https://pro-openapi.debank.com/v1/user/all_complex_protocol_list?id=0xYOUR_WALLET&chain_ids=eth,arb,op,base,matic" \
  -H "AccessKey: YOUR_DEBANK_API_KEY" | jq '.[] | {protocol: .name, net_usd_value: .net_usd_value, positions: .portfolio_item_list}'
```

**Free alternative — Zapper API:**
```bash
curl -s "https://api.zapper.xyz/v2/balances?addresses[]=0xYOUR_WALLET&networks[]=ethereum&networks[]=arbitrum" \
  -H "Authorization: Basic $(echo -n ':YOUR_ZAPPER_KEY' | base64)"
```

### 2. Impermanent Loss Calculator

**Formula:**
```
IL% = 2 * sqrt(price_ratio) / (1 + price_ratio) - 1
```

Where `price_ratio = current_price / entry_price` for the volatile asset vs stable.

**Python implementation:**
```python
import math

def impermanent_loss(entry_price: float, current_price: float) -> float:
    """
    Calculate impermanent loss percentage for a 50/50 LP position.
    
    Args:
        entry_price: Price of volatile asset at LP entry (in terms of stable)
        current_price: Current price of volatile asset
    
    Returns:
        IL as a decimal (negative = loss). Multiply by 100 for percentage.
    
    Example:
        entry_price = 2000  # ETH at entry
        current_price = 3000  # ETH now
        il = impermanent_loss(2000, 3000)
        # Returns ~-0.0203 → -2.03% IL
    """
    price_ratio = current_price / entry_price
    il = (2 * math.sqrt(price_ratio)) / (1 + price_ratio) - 1
    return il

def lp_position_pnl(
    token0_qty: float, token1_qty: float,
    token0_entry: float, token1_entry: float,
    token0_current: float, token1_current: float,
    fees_earned_usd: float = 0.0
) -> dict:
    """
    Full P&L for an LP position including IL and fees.
    
    Returns:
        Dict with: hodl_value, lp_value, il_usd, fees_earned, net_pnl
    """
    hodl_value = (token0_qty * token0_current) + (token1_qty * token1_current)
    lp_value = _calculate_lp_value(
        token0_qty, token1_qty,
        token0_entry, token1_entry,
        token0_current, token1_current
    )
    il_usd = lp_value - hodl_value
    net_pnl = il_usd + fees_earned_usd
    
    return {
        "hodl_value_usd": hodl_value,
        "lp_value_usd": lp_value,
        "il_usd": il_usd,
        "il_pct": il_usd / hodl_value if hodl_value else 0,
        "fees_earned_usd": fees_earned_usd,
        "net_pnl_usd": net_pnl,
        "net_pnl_pct": net_pnl / hodl_value if hodl_value else 0,
    }

def _calculate_lp_value(t0_qty, t1_qty, t0_entry, t1_entry, t0_cur, t1_cur):
    """Compute constant-product AMM LP value at current prices."""
    k = t0_qty * t1_qty  # invariant
    # At current prices: t0_new = sqrt(k * t1_cur / t0_cur) — wait, recalc with entry ratio
    entry_value = (t0_qty * t0_entry) + (t1_qty * t1_entry)
    price_ratio = t0_cur / t0_entry
    # AMM rebalances: each side = sqrt(initial_product * price_ratio)
    t0_new = math.sqrt(k * t0_cur / t1_cur)
    t1_new = math.sqrt(k * t1_cur / t0_cur)
    return (t0_new * t0_cur) + (t1_new * t1_cur)
```

**Uniswap v3 LP (concentrated liquidity):**
Uniswap v3 IL is range-dependent. Use the official SDK or Revert Finance API:
```bash
# Revert Finance — v3 position analytics
curl "https://api.revert.finance/v1/position?position_id=YOUR_NFT_ID&chain_id=1"
```

### 3. Cost Basis Tracking Per Position

Track entry prices and quantities for accurate P&L and tax reporting:

```python
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class LPEntry:
    """Single LP entry event (add liquidity)."""
    timestamp: datetime
    protocol: str
    chain: str
    pool: str
    token0_symbol: str
    token0_qty: float
    token0_price_usd: float
    token1_symbol: str
    token1_qty: float
    token1_price_usd: float
    tx_hash: str
    gas_cost_usd: float = 0.0

    @property
    def cost_basis_usd(self) -> float:
        return (self.token0_qty * self.token0_price_usd +
                self.token1_qty * self.token1_price_usd +
                self.gas_cost_usd)

@dataclass
class LPExit:
    """LP exit event (remove liquidity)."""
    timestamp: datetime
    protocol: str
    chain: str
    pool: str
    token0_qty_returned: float
    token0_price_usd: float
    token1_qty_returned: float
    token1_price_usd: float
    fees_token0: float
    fees_token1: float
    tx_hash: str
    gas_cost_usd: float = 0.0

    @property
    def proceeds_usd(self) -> float:
        return (self.token0_qty_returned * self.token0_price_usd +
                self.token1_qty_returned * self.token1_price_usd +
                self.fees_token0 * self.token0_price_usd +
                self.fees_token1 * self.token1_price_usd -
                self.gas_cost_usd)
```

**IRS treatment (current guidance):**
- Adding liquidity: typically not a taxable event, but track cost basis
- LP fees earned: ordinary income at time of receipt (FMV)
- Removing liquidity: capital gain/loss (proceeds - cost basis)
- Staking rewards: ordinary income at FMV when received

### 4. Staking Rewards Tracker

```bash
# Pull staking reward history via The Graph (Lido example)
curl -X POST "https://api.thegraph.com/subgraphs/name/lidofinance/lido" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ totalRewards(where: {account: \"0xYOUR_WALLET\"}, orderBy: block, orderDirection: desc, first: 100) { id totalRewards totalFee block blockTime } }"
  }'
```

**Aave interest accrual:**
```bash
# aToken balance change = interest earned
# Use Aave subgraph to get historical balance snapshots
curl -X POST "https://api.thegraph.com/subgraphs/name/aave/protocol-v3" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ userReserves(where: {user: \"0xYOUR_WALLET\"}) { reserve { symbol } currentATokenBalance scaledATokenBalance } }"
  }'
```

### 5. Multi-Chain Aggregation

**Using Moralis Web3 Data API (no API key for public endpoints):**
```bash
# ETH mainnet DeFi positions
curl "https://deep-index.moralis.io/api/v2.2/0xYOUR_WALLET/defi/positions?chain=eth" \
  -H "X-API-Key: YOUR_MORALIS_KEY"

# Arbitrum positions  
curl "https://deep-index.moralis.io/api/v2.2/0xYOUR_WALLET/defi/positions?chain=arbitrum" \
  -H "X-API-Key: YOUR_MORALIS_KEY"
```

**Using cast (Foundry) for on-chain reads:**
```bash
# Check Uniswap v3 position NFT owner (verify position still active)
cast call 0xC36442b4a4522E871399CD717aBDD847Ab11FE88 \
  "ownerOf(uint256)(address)" YOUR_NFT_ID \
  --rpc-url https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY

# Get Aave v3 account health factor
cast call 0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2 \
  "getUserAccountData(address)(uint256,uint256,uint256,uint256,uint256,uint256)" \
  0xYOUR_WALLET --rpc-url YOUR_RPC
```

### 6. Portfolio Summary Output

Standard JSON schema for handoff to crypto-tax-agent and treasury dashboards:

```json
{
  "snapshot_date": "2026-03-15T18:00:00Z",
  "wallet": "0x...",
  "total_value_usd": 125430.00,
  "positions": [
    {
      "id": "uniswap-v3-eth-usdc-500-12345",
      "protocol": "Uniswap v3",
      "chain": "ethereum",
      "pool": "ETH/USDC 0.05%",
      "type": "lp",
      "nft_id": 12345,
      "token0": { "symbol": "ETH", "qty": 1.5, "price_usd": 3000, "value_usd": 4500 },
      "token1": { "symbol": "USDC", "qty": 4500, "price_usd": 1.0, "value_usd": 4500 },
      "total_value_usd": 9000,
      "cost_basis_usd": 8800,
      "unrealized_pnl_usd": 200,
      "fees_earned_usd": 145.50,
      "il_usd": -42.10,
      "il_pct": -0.0047,
      "entry_date": "2026-01-10T00:00:00Z",
      "in_range": true
    },
    {
      "id": "lido-steth-deposit-20240101",
      "protocol": "Lido",
      "chain": "ethereum",
      "type": "liquid_staking",
      "token": { "symbol": "stETH", "qty": 5.0, "price_usd": 3010, "value_usd": 15050 },
      "cost_basis_usd": 14500,
      "staking_rewards_usd": 380.00,
      "apy_current": 3.8,
      "entry_date": "2025-06-01T00:00:00Z"
    }
  ],
  "summary": {
    "total_cost_basis_usd": 89000,
    "total_unrealized_pnl_usd": 36430,
    "total_fees_earned_usd_ytd": 2140,
    "total_staking_rewards_usd_ytd": 890,
    "total_il_usd": -520,
    "net_yield_usd_ytd": 3030
  }
}
```

---

## Tax Handoff to crypto-tax-agent

Export in crypto-tax-agent's expected format:

```python
def export_for_tax_agent(positions: list, year: int) -> dict:
    """
    Generate tax-ready export for crypto-tax-agent consumption.
    
    Produces:
    - Income events: staking rewards, LP fees (ordinary income)
    - Disposal events: LP exits (capital gains/losses)
    - Cost basis lots: FIFO/HIFO tracking per position
    """
    income_events = []
    disposal_events = []
    
    for pos in positions:
        # Fee income events (ordinary income when earned)
        for reward in pos.get("reward_events", []):
            income_events.append({
                "date": reward["timestamp"],
                "type": "defi_income",
                "subtype": reward["type"],  # "lp_fee" | "staking_reward" | "yield"
                "asset": reward["symbol"],
                "qty": reward["qty"],
                "fmv_usd": reward["price_usd"],
                "income_usd": reward["qty"] * reward["price_usd"],
                "protocol": pos["protocol"],
                "tx_hash": reward["tx_hash"]
            })
        
        # LP exits (capital events)
        for exit_event in pos.get("exit_events", []):
            disposal_events.append({
                "date": exit_event["timestamp"],
                "type": "lp_exit",
                "protocol": pos["protocol"],
                "cost_basis_usd": exit_event["cost_basis_usd"],
                "proceeds_usd": exit_event["proceeds_usd"],
                "gain_loss_usd": exit_event["proceeds_usd"] - exit_event["cost_basis_usd"],
                "holding_period_days": exit_event["holding_period_days"],
                "is_long_term": exit_event["holding_period_days"] >= 365,
                "tx_hash": exit_event["tx_hash"]
            })
    
    return {
        "tax_year": year,
        "generated_at": datetime.utcnow().isoformat(),
        "income_events": income_events,
        "disposal_events": disposal_events,
        "total_income_usd": sum(e["income_usd"] for e in income_events),
        "total_realized_gain_usd": sum(
            e["gain_loss_usd"] for e in disposal_events if e["gain_loss_usd"] > 0
        ),
        "total_realized_loss_usd": sum(
            e["gain_loss_usd"] for e in disposal_events if e["gain_loss_usd"] < 0
        ),
    }
```

---

## Monitoring & Alerts

### Aave Health Factor Monitoring
```python
HEALTH_FACTOR_THRESHOLDS = {
    "critical": 1.1,   # Alert immediately — liquidation imminent
    "warning": 1.3,    # Alert — add collateral or reduce debt
    "caution": 1.5,    # Notify — monitor closely
}

def check_health_factor(wallet: str, rpc_url: str) -> dict:
    """
    Check Aave v3 health factor for liquidation risk.
    Returns alert level and recommended action.
    """
    # Use cast or web3.py to call getUserAccountData
    # Returns: totalCollateralBase, totalDebtBase, availableBorrowsBase,
    #          currentLiquidationThreshold, ltv, healthFactor
    pass
```

### LP Out-of-Range Detection (Uniswap v3)
```bash
# Check if v3 position is still in range (earning fees)
# currentTick within [tickLower, tickUpper] = in range
cast call 0xC36442b4a4522E871399CD717aBDD847Ab11FE88 \
  "positions(uint256)(uint96,address,address,address,uint24,int24,int24,uint128,uint256,uint256,uint128,uint128)" \
  YOUR_NFT_ID --rpc-url YOUR_RPC
```

---

## Data Sources Reference

| Tool | Best For | Cost |
|------|----------|------|
| DeBank Pro API | Most comprehensive, all protocols | $99/mo |
| Zapper API | Good free tier, Ethereum + L2 | Free tier available |
| Zerion API | Clean data, portfolio-focused | Freemium |
| Moralis | Multi-chain, developer-friendly | Freemium |
| The Graph | Protocol-specific subgraphs | Free |
| Revert Finance | Uniswap v3 concentrated LP analytics | Free |
| Alchemy/Infura | Raw RPC calls | Freemium |

---

## Common Workflows

**Monthly portfolio review:**
1. Pull snapshot via DeBank/Zapper
2. Run IL calculator on all LP positions
3. Flag any Aave/Compound positions below HF 1.5
4. Flag any v3 positions out of range
5. Export income events (fees, staking rewards) to crypto-tax-agent
6. Generate markdown summary for treasury dashboard

**Pre-tax-season export (Q1):**
1. Pull all 2025 transactions for tracked wallets
2. Classify: income events vs capital events
3. Calculate cost basis (FIFO default, HIFO optional)
4. Reconcile staking rewards (ordinary income)
5. Hand off structured JSON to crypto-tax-agent for 8949/Schedule D

**New position entry:**
1. Record entry tx_hash, block, prices at entry
2. Calculate cost basis (token values + gas)
3. Store in position ledger
4. Set monitoring thresholds (IL%, HF, range status)

---

## Not For This Skill

- **Executing trades or transactions** — use a wallet/trading skill
- **on-chain-payroll** — PTIN-backed Moltlaunch service, not ClawHub
- **NFT portfolio tracking** — different data model and APIs
- **CEX holdings** (Coinbase, Kraken) — use a CEX API skill or crypto-tax-agent directly
- **Real-time price ticker** — use a price feed skill
- **Bridging or swapping assets** — use a transaction execution skill
