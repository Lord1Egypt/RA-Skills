# ENS Registration Costs

**Last updated:** 2026-03-12  
**Current gas price:** 0.22 gwei (very low)  
**ETH price:** ~$2,500

---

## ENS Name Pricing Tiers

These are **annual rental costs** set by the ENS protocol:

| Name Length | Annual Cost (ETH) | Annual Cost (USD) | Example |
|-------------|-------------------|-------------------|---------|
| 3 characters | 0.309 ETH | ~$773/year | `abc.eth` |
| 4 characters | 0.077 ETH | ~$193/year | `cool.eth` |
| 5+ characters | 0.002 ETH | ~$6/year | `hello.eth` |

**Note:** These are **name rental prices only**, not including gas costs.

---

## Gas Costs by Network Conditions

Gas costs vary dramatically based on network congestion. Here's what to expect:

### Current (0.22 gwei) - Very Low 🟢
| Operation | Gas Used | ETH Cost | USD Cost |
|-----------|----------|----------|----------|
| Commitment | 45,000 | 0.000010 | $0.02 |
| Registration | 265,000 | 0.000058 | $0.15 |
| **Total Gas** | **310,000** | **0.000068** | **$0.17** |

### Typical (10 gwei) - Normal 🟡
| Operation | Gas Used | ETH Cost | USD Cost |
|-----------|----------|----------|----------|
| Commitment | 45,000 | 0.000450 | $1.13 |
| Registration | 265,000 | 0.002650 | $6.63 |
| **Total Gas** | **310,000** | **0.003100** | **$7.75** |

### High (50 gwei) - Congested 🔴
| Operation | Gas Used | ETH Cost | USD Cost |
|-----------|----------|----------|----------|
| Commitment | 45,000 | 0.002250 | $5.63 |
| Registration | 265,000 | 0.013250 | $33.13 |
| **Total Gas** | **310,000** | **0.015500** | **$38.75** |

---

## Complete Registration Cost Examples

### 5-Letter Name (Most Common)

**Current conditions (0.22 gwei):**
- Name cost: ~$6/year
- Gas cost: ~$0.17
- **Total: ~$6.17**

**Typical conditions (10 gwei):**
- Name cost: ~$6/year
- Gas cost: ~$7.75
- **Total: ~$13.75**

**High congestion (50 gwei):**
- Name cost: ~$6/year
- Gas cost: ~$38.75
- **Total: ~$44.75**

---

### 4-Letter Name (Premium)

**Current conditions (0.22 gwei):**
- Name cost: ~$193/year
- Gas cost: ~$0.17
- **Total: ~$193.17**

**Typical conditions (10 gwei):**
- Name cost: ~$193/year
- Gas cost: ~$7.75
- **Total: ~$200.75**

---

### 3-Letter Name (Ultra Premium)

**Current conditions (0.22 gwei):**
- Name cost: ~$773/year
- Gas cost: ~$0.17
- **Total: ~$773.17**

**Typical conditions (10 gwei):**
- Name cost: ~$773/year
- Gas cost: ~$7.75
- **Total: ~$780.75**

---

## Subdomain & Content Costs

These operations are much cheaper (single transaction):

### Current Conditions (0.22 gwei) 🟢
| Operation | Gas Used | ETH Cost | USD Cost |
|-----------|----------|----------|----------|
| Create subdomain (wrapped) | 150,000 | 0.000033 | $0.08 |
| Create subdomain (unwrapped) | 200,000 | 0.000044 | $0.11 |
| Set content hash | 100,000 | 0.000022 | $0.06 |

### Typical Conditions (10 gwei) 🟡
| Operation | Gas Used | ETH Cost | USD Cost |
|-----------|----------|----------|----------|
| Create subdomain (wrapped) | 150,000 | 0.001500 | $3.75 |
| Create subdomain (unwrapped) | 200,000 | 0.002000 | $5.00 |
| Set content hash | 100,000 | 0.001000 | $2.50 |

---

## Cost Optimization Tips

### 1. Check Gas Price Before Registration

```bash
# Check current gas price
cast gas-price --rpc-url https://mainnet.rpc.buidlguidl.com

# Wait for low gas (< 20 gwei is good)
```

### 2. Use Dry Run Mode

```bash
# Check cost before committing
node register-ens-name.js mynewname --dry-run
```

Shows current name price (updates in real-time).

### 3. Register During Off-Peak Hours

- **Lowest gas:** Weekends, late night UTC
- **Highest gas:** Weekdays, afternoon US/EU time
- **Monitor:** https://etherscan.io/gastracker

### 4. Longer Names Are Cheaper

- 5 chars: ~$6/year
- 10 chars: ~$6/year (same price!)
- Only 3-4 char names have premium pricing

---

## Historical Context

**Why gas is so low now (0.22 gwei)?**

Ethereum network is currently very quiet. This won't last forever. Typical gas prices:

- **2021 bull market:** 100-500 gwei (insane)
- **2022-2023 bear:** 10-50 gwei (typical)
- **2024-2026:** 0.5-20 gwei (current era)
- **Right now:** 0.22 gwei (lucky timing!)

**Recommendation:** If you're reading this and gas is < 5 gwei, **register your names now**!

---

## Gas Price Alerts

Set up alerts for low gas:

```bash
# Monitor gas price
while true; do
  GAS=$(cast gas-price --rpc-url https://mainnet.rpc.buidlguidl.com | cut -d' ' -f1)
  if [ "$GAS" -lt 5000000000 ]; then  # 5 gwei
    echo "🔔 Low gas alert: $GAS wei"
  fi
  sleep 300  # Check every 5 minutes
done
```

---

## Refunds & Failures

### Failed Transactions

You **lose the gas cost** even if the transaction fails. Common causes:

- Insufficient balance
- Name already taken (check availability first!)
- Commitment expired (> 24 hours old)

**Always use `--dry-run` first!**

### No Refunds on Name Rentals

Once you register, there are no refunds. Names are non-transferable rentals.

---

## Renewal Costs

Renewals are **cheaper** than initial registration (no commitment needed):

| Condition | Gas Used | ETH Cost | USD Cost |
|-----------|----------|----------|----------|
| Current (0.22 gwei) | 100,000 | 0.000022 | $0.06 |
| Typical (10 gwei) | 100,000 | 0.001000 | $2.50 |
| High (50 gwei) | 100,000 | 0.005000 | $12.50 |

Plus name rental cost (same as original registration).

---

## Summary

**For a 5-letter name right now:**
- ✅ **Total: ~$6.17** (name + gas)
- ⏱️  **Time: 2-3 minutes**
- 🎯 **Best time to register!**

**At typical gas (10 gwei):**
- ✅ **Total: ~$13.75** (name + gas)
- ⏱️  **Time: 2-3 minutes**

**Avoid registering when gas > 50 gwei** unless you really need the name immediately.
