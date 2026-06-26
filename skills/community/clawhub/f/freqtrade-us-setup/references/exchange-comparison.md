# Exchange Comparison for US Traders

## Why This Matters

Freqtrade is legal in the US. The problem is **which exchange you use**. Many international exchanges explicitly block US users. Using them via VPN violates their ToS and can freeze your funds.

## The Options

### ✅ Kraken (RECOMMENDED)

**Status:** Fully legal in US, fully supported by Freqtrade

| Feature | Details |
|---------|---------|
| **Fees** | 0.16% maker / 0.26% taker (decreases with volume) |
| **Stake currencies** | USDT, USD, EUR, GBP, JPY |
| **API support** | Excellent — specifically tested with Freqtrade |
| **Withdrawal limits** | None for US users (KYC verified) |
| **Known issues** | Occasional API rate limits during high traffic |
| **Recommended for** | Beginners to advanced — most stable choice |

**Why Kraken?**
- Explicitly complies with US regulations
- No risk of account suspension for US traders
- Strong API documentation
- Mature platform (founded 2011)
- Widely used by Freqtrade community

---

### ⚠️ Binance.US (ALTERNATIVE)

**Status:** Legal in US, supported by Freqtrade, but more restrictions

| Feature | Details |
|---------|---------|
| **Fees** | 0.1% maker / 0.1% taker (better than Kraken) |
| **Stake currencies** | USDT, USD, BUSD (limited pairs) |
| **API support** | Good, but documented as less stable than Binance.com |
| **Withdrawal limits** | Strict daily limits for new accounts |
| **Known issues** | More rate limiting, occasional API downtime |
| **Recommended for** | Users who already have Binance.US account |

**Considerations:**
- Smaller order book than Binance.com (slippage risk)
- Less liquid on smaller trading pairs
- Historical friction between Binance.US and regulators
- If you're starting fresh, Kraken is safer

---

### ❌ Binance.com (DO NOT USE)

**Status:** BLOCKED for US users

- Explicitly restricts US IP addresses
- Using a VPN is a ToS violation
- Can result in funds being frozen indefinitely
- Not worth the risk
- Freqtrade support community will not help if you violate ToS

---

### ⏳ Coinbase Advanced Trade (NOT READY YET)

**Status:** Legal in US, but Freqtrade support is incomplete

| Feature | Details |
|---------|---------|
| **Fees** | 0.5-0.6% maker/taker (higher) |
| **API support** | Basic Freqtrade support, limited strategy options |
| **Maturity** | Newer, fewer community examples |
| **Recommended for** | Check latest Freqtrade docs — support is still maturing |

---

## Decision Tree

```text
Are you a US resident?
├─ Yes
│  ├─ Starting fresh?
│  │  └─ USE KRAKEN ✅ (most reliable)
│  │
│  └─ Already on Binance.US?
│     └─ Can stay there ⚠️ (works, but less stable)
│
└─ No (international)
   └─ Use Binance.com or your local exchange
```

---

## Important: What NOT to Do

### ❌ Never Use a VPN to Access Blocked Exchanges

- **Why not?** Violates exchange ToS explicitly
- **Consequence:** Funds can be frozen when they detect VPN usage
- **Recovery:** Nearly impossible — customer support won't help
- **Legal risk:** Potentially considered fraud or ToS circumvention

The exchanges have your KYC data (ID, address). They will notice if you access from a US IP, then a VPN, then back again.

**Just use Kraken. It's easier and safe.**

---

## Setup Comparison

### Kraken Setup Time: 15 minutes

1. Create account
2. Complete KYC (ID verification)
3. Enable API → generate keys with correct permissions
4. Paste keys into Freqtrade config
5. Done

### Binance.US Setup Time: 20 minutes

1. Same as above, but account approval takes longer
2. Higher complexity for API key permissions
3. More restrictive rate limits to work around

---

## Recommendation

**For US-based traders starting Freqtrade:**

1. **Kraken** if you're building from scratch (95% of cases)
2. **Binance.US** if you already have an account there
3. **Coinbase** if you specifically want self-custody (but wait for better Freqtrade support)
4. **Binance.com** — do not attempt. Not worth it.
