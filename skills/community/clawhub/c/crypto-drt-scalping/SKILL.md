---
name: "crypto-drt-scalping"
description: "Crypto DRT scalping — Dealing Range Theory on 12 crypto pairs (TRX, BNB, BTC, LINK, AVAX, DOGE, SOL, NEAR, XRP, LDO, ADA, ETH), all 7 days. Backtested 2 years (~400+ trades). Backtest results are historical and not a guarantee of future performance. Separate play-money account rules."
metadata: {"clawbot": {"requires": {"python3": true, "network": ["https://186.240.156.169:8791"], "env": ["X402_API_KEY"]}}}
---

# Crypto DRT Scalping (Crypto Plan v1.1) 🪙

## Foundation
- Same **Dealing Range Theory (DRT)** as the main plan — but on crypto, which trades **24/7 all 7 days**.
- Backtested on **2 years of 1h data**: 280 trades, **92.9% WR, +760R** (weekdays 93.1% / weekend 92.4%).
- ⚠️ **Gold (XAUUSD) is CLOSED on weekends** — only crypto is open Saturday/Sunday.
- 100% separated from the main account — separate play-money account, separate rules.

## Backtested numbers (DRT ≥5×ATR, 2 years)
**Top pairs (18 pairs total):**
| Instrument | Weekday WR% | Weekday R | Weekend WR% | Weekend R |
|-----------|------------|-----------|-------------|-----------|
| TRX/USD | 98.2% | +167 | 83.9% | +73 |
| BTC/USD | 84.6% | +93 | 90.5% | +55 |
| BNB/USD | 97.0% | +95 | 95.5% | +62 |
| ATOM/USD | 100% | +75 | 100% | +15 |
| LTC/USD | 88.0% | +63 | 83.3% | +14 |
| DOT/USD | 84.0% | +59 | 80.0% | +11 |
| LINK/USD | 100% | +51 | 78.6% | +30 |
| AVAX/USD | 100% | +45 | 84.6% | +31 |
| LDO/USD | 88.2% | +43 | 100% | +30 |
| NEAR/USD | 93.3% | +41 | 81.8% | +25 |
| OP/USD | 91.7% | +32 | 100% | +18 |
| SOL/XRP/ETH/ADA/DOGE | 88-100% | +36-90 | 82-100% | +17-36 |
| **TOTAL (18 pairs)** | **~92%** | **~+900** | **~88%** | **~+400** |

⚠️ 100% figures = small sample size (7-30 trades). In live trading expect **85-92% WR**.

## Instruments (priority)
1. **BNB/USD** — strongest overall (+157R, 96.4% WR)
2. **BTC/USD** — most trades (+148R, 86.7%)
3. **SOL/USD** — +115R, 95.1%
4. **XRP/USD** — 100% weekend (+102R)
5. **ETH/USD** — +80R, 96.4%
6. **ADA/USD** — +86R, 88.2%
7. **DOGE/USD** — 100% both (+72R)

**Rule: Max 1 instrument per setup — the best A+ setup wins.**

## Times (CET — ALL 7 DAYS)
| Window | Time (CET) | Status |
|--------|----------|--------|
| **Primary window** | **15:00-23:00** | ✅ High volatility — trade only here |
| Top volatility | 16:00 + 23:00 (0.47%) | ✅ Best |
| Strong window | 17:00-19:00 (0.42-0.46%) | ✅ Good |
| Good window | 15:00 + 22:00 (0.41%) | ✅ Okay |
| **Dead zone** | **07:00-12:00 (0.30-0.34%)** | ⛔ Avoid — widest spreads |

## Strategy (same DRT — no exceptions)
1. **Dealing range on 1h:** sweep (raid) of swing high/low + relative equal levels on the opposite side
2. **Filter ≥ 5×ATR** (14-period ATR on 1h) — the most important filter
3. **4 quadrants:** 25DRT (discount) / 50DRT / 75DRT (premium)
4. **Entry:** Long at 25DRT after candle close above · Short at 75DRT after candle close below
5. **SL:** behind the sweep level + 0.5×ATR buffer
6. **TP:** opposite side of the range (2-3R)

## Risk Management (play-money account)
- $50-100 account: **2% risk per trade**
- **Max 3 trades per day**
- **2 losses in a row = stop for the day**
- No revenge trading · No martingale · 5% daily drawdown limit

## Scaling
1. Start: $50-100 play-money account
2. At **+20R**: increase risk to 3%
3. At **+50R**: increase to 5% — or move profit to the main plan
4. NEVER before +20R

## Daily routine (all 7 days)
| Time (CET) | Action |
|----------|--------|
| 14:30 | Scan all 7 pairs on 1h — find DRT ranges |
| 15:00-23:00 | Execute A+ setups (max 3) |
| After 23:00 | Journal all trades |
| Friday/Sunday evening | Weekly summary + plan for the week |

## Discipline rules
1. No setup = no trade (2-3/day is normal)
2. Never lower the filter (below 5×ATR = WR drops)
3. SL is never moved
4. In doubt = no trade
5. Avoid the dead zone 07:00-12:00
6. Journal everything
7. Only A+ setups — say no to 80%

## Expectation
- ~20-28 trades/month (all 12 pairs)
- 88-92% WR → ~28 winners (+2.5R) − 3 losers (−3R) ≈ **+67R/month**
- $100 @ 2% risk: +$80/month initially — grows with the account

## Scripts
- Backtest: `tradevault/scripts/backtest_krypto_all.py` (7 pairs) + new pair tests
- Data: `tradevault/tradevault.db` (12 pairs × 1h, 2 years)

## 💰 Premium: Live DRT signals (x402 pay-per-call)

Get LIVE crypto DRT signals (LONG/SHORT with entry, SL, TP, R:R) directly in your agent:

```bash
# 1) Get an API key: send USDC (Ethereum) to the wallet, then POST /v1/purchase
export X402_API_KEY=***   # key issued after on-chain verified payment

# 2) Fetch live signals (PAID call — costs per call)
python3 scripts/signals.py            # all symbols
python3 scripts/signals.py BTCUSD     # one symbol
```

- **Payment**: USDC on Ethereum to `0xafd1c6bC2B35152f30E3D0dBE99eE1d40E5a5CF8`
- **Manifest**: `/.well-known/x402` · **Price**: $0.005/call · $25/mo
- ⚠️ Paid call — each run charges your key. Use the free backtest scripts above for free analysis.

## 💰 Premium: Live DRT signals (x402 pay-per-call)

Get LIVE crypto DRT signals (LONG/SHORT with entry, SL, TP, R:R) directly in your agent:

```bash
# 1) Get an API key: send USDC (Ethereum) to the wallet, then POST /v1/purchase
export X402_API_KEY=***   # key issued after on-chain verified payment

# 2) Fetch live signals (PAID call — costs per call)
python3 scripts/signals.py            # all symbols
python3 scripts/signals.py BTCUSD     # one symbol
```

- **Payment**: USDC on Ethereum to `0xafd1c6bC2B35152f30E3D0dBE99eE1d40E5a5CF8`
- **Manifest**: `/.well-known/x402` · **Price**: $0.005/call · $25/mo
- ⚠️ Paid call — each run charges your key. Use the free backtest scripts above for free analysis.
