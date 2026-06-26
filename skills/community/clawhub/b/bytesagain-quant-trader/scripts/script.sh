#!/usr/bin/env bash
set -euo pipefail
DATA_DIR="${HOME}/.local/share/bytesagain-quant-trader"
mkdir -p "$DATA_DIR"
_log() { echo "[$(date '+%H:%M:%S')] $*" >&2; }
_err() { echo "ERROR: $*" >&2; exit 1; }

cmd_strategy() {
    local asset="BTC" timeframe="4h" style="momentum"
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --asset)     asset="$2";     shift 2 ;;
            --timeframe) timeframe="$2"; shift 2 ;;
            --style)     style="$2";     shift 2 ;;
            *) shift ;;
        esac
    done
    echo ""
    echo "═══════════════════════════════════════════════"
    echo "QUANT STRATEGY: $style | $asset | $timeframe"
    echo "Generated: $(date '+%Y-%m-%d %H:%M')"
    echo "═══════════════════════════════════════════════"
    echo ""
    case "${style,,}" in
        momentum)
            cat << EOF
MOMENTUM STRATEGY for $asset ($timeframe)

LOGIC:
  Entry: Price > EMA20 AND RSI crosses above 50 AND Volume > 1.5× avg
  Exit:  Price < EMA20 OR RSI < 40 OR Trailing stop -3%

INDICATORS:
  Trend filter:  EMA20, EMA50 (must be aligned bullish)
  Momentum:      RSI(14) > 50, MACD histogram positive
  Volume filter: Volume > 20-period average × 1.5

PARAMETERS (tune per asset):
  RSI period:     14
  EMA fast:       20
  EMA slow:       50
  Stop loss:      2–3% below entry
  Take profit:    1:2 or 1:3 risk/reward
  Max position:   2% of capital per trade

BACKTEST NOTES:
  Works best in trending markets
  Filter out: sideways/low-volatility periods (ADX < 20)
  Best timeframes: 4h, Daily
EOF
            ;;
        mean-reversion)
            cat << EOF
MEAN-REVERSION STRATEGY for $asset ($timeframe)

LOGIC:
  Entry Long:  RSI < 30 AND price > 2 STD below Bollinger lower band
  Entry Short: RSI > 70 AND price > 2 STD above Bollinger upper band
  Exit:        Price returns to middle Bollinger band (20 SMA)

INDICATORS:
  Bollinger Bands (20, 2)
  RSI(14) — oversold/overbought extremes
  Volume confirmation

PARAMETERS:
  BB period: 20, STD multiplier: 2
  RSI thresholds: 30 (long), 70 (short)
  Stop loss: Outside opposite Bollinger band
  Take profit: Middle band (20 SMA)

BACKTEST NOTES:
  Works best in ranging/sideways markets
  Avoid in strong trending conditions
  Reduce size in volatile regimes
EOF
            ;;
        breakout)
            cat << EOF
BREAKOUT STRATEGY for $asset ($timeframe)

LOGIC:
  Entry: Price closes above N-period high + Volume confirmation
  Exit:  Price closes below entry candle low OR -2% stop

INDICATORS:
  N-period High/Low: 20 bars
  Volume: Must be >2× average on breakout candle
  ATR: For dynamic stop placement

PARAMETERS:
  Lookback period: 20 bars
  Volume multiplier: 2×
  Stop loss: Low of breakout candle or 1 ATR below
  Trailing stop: 2 ATR

BACKTEST NOTES:
  High win rate in trending markets
  Many false breakouts in choppy conditions
  Add ADX > 25 filter to reduce noise
EOF
            ;;
        *)
            echo "TREND-FOLLOWING STRATEGY for $asset ($timeframe)"
            echo ""
            echo "LOGIC:"
            echo "  Entry: EMA9 crosses above EMA21 with MACD confirmation"
            echo "  Exit:  EMA9 crosses below EMA21 or ATR trailing stop"
            echo ""
            echo "PARAMETERS:"
            echo "  Fast EMA: 9 | Slow EMA: 21"
            echo "  MACD: 12/26/9"
            echo "  Stop: 1.5 ATR(14)"
            ;;
    esac
    echo ""
    echo "───────────────────────────────────────────────"
    echo "⚠️  Educational only. Not financial advice. Always backtest before trading."
    echo "Powered by BytesAgain | bytesagain.com"
}

cmd_signal() {
    local asset="" price="" ma20="" ma50="" rsi="" volume="avg"
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --asset)  asset="$2";  shift 2 ;;
            --price)  price="$2";  shift 2 ;;
            --ma20)   ma20="$2";   shift 2 ;;
            --ma50)   ma50="$2";   shift 2 ;;
            --rsi)    rsi="$2";    shift 2 ;;
            --volume) volume="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    [[ -z "$price" ]] && _err "Usage: signal --asset BTC --price 3200 --ma20 3050 --ma50 2900 --rsi 62 --volume above-avg"

    python3 - "$asset" "$price" "$ma20" "$ma50" "$rsi" "$volume" << 'PYEOF'
import sys
asset, price_s, ma20_s, ma50_s, rsi_s, volume = sys.argv[1:]
price = float(price_s)
ma20 = float(ma20_s) if ma20_s else 0
ma50 = float(ma50_s) if ma50_s else 0
rsi = float(rsi_s) if rsi_s else 50

signals = []
score = 0

print(f"\n{'═'*47}")
print(f"SIGNAL ANALYSIS: {asset or 'Asset'} @ {price}")
print(f"{'═'*47}\n")
print(f"  Price:  {price}")
print(f"  MA20:   {ma20}  {'✅ Price above' if price > ma20 else '❌ Price below'}")
print(f"  MA50:   {ma50}  {'✅ Price above' if price > ma50 else '❌ Price below'}")
print(f"  RSI:    {rsi}   {'⚠️ Overbought' if rsi > 70 else '⚠️ Oversold' if rsi < 30 else '✅ Neutral'}")
print(f"  Volume: {volume}")
print()

if price > ma20: score += 1
if price > ma50: score += 1
if ma20 > ma50: score += 1
if 40 < rsi < 65: score += 1
elif rsi > 70: score -= 1
elif rsi < 30: score += 1  # oversold bounce potential
if "above" in volume.lower(): score += 1

print("  SIGNAL SCORE: ", end="")
if score >= 4:
    print(f"🟢 BULLISH ({score}/5) — Consider long entry")
elif score >= 2:
    print(f"🟡 NEUTRAL ({score}/5) — Wait for confirmation")
else:
    print(f"🔴 BEARISH ({score}/5) — Caution / Consider short")

print()
print("  SUGGESTED ACTION:")
if score >= 4:
    print("  → Long entry on next pullback to MA20")
    print(f"  → Stop loss: below MA20 ({ma20})")
    print(f"  → Take profit: +5–8% from entry")
elif score <= 1:
    print("  → Avoid long. Wait for trend reversal confirmation.")
else:
    print("  → Sideways / unclear. Wait for breakout or RSI extremes.")

print()
print("─"*47)
print("⚠️  Not financial advice. Educational only.")
print("Powered by BytesAgain | bytesagain.com")
PYEOF
}

cmd_risk() {
    local capital=10000 risk_pct=1 entry="" stop=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --capital)  capital="$2";  shift 2 ;;
            --risk-pct) risk_pct="$2"; shift 2 ;;
            --entry)    entry="$2";    shift 2 ;;
            --stop)     stop="$2";     shift 2 ;;
            *) shift ;;
        esac
    done
    [[ -z "$entry" || -z "$stop" ]] && _err "Usage: risk --capital 10000 --risk-pct 1 --entry 3200 --stop 3050"

    python3 - "$capital" "$risk_pct" "$entry" "$stop" << 'PYEOF'
import sys
capital, risk_pct, entry, stop = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])

risk_amount = capital * (risk_pct / 100)
price_risk = abs(entry - stop)
risk_pct_per_unit = price_risk / entry * 100
position_size = risk_amount / price_risk
position_value = position_size * entry

tp1 = entry + price_risk * 2  # 1:2 R/R
tp2 = entry + price_risk * 3  # 1:3 R/R

kelly = (risk_pct / 100) / (price_risk / entry)

print(f"\n{'═'*47}")
print(f"POSITION SIZING & RISK METRICS")
print(f"{'═'*47}\n")
print(f"  Capital:          ${capital:,.2f}")
print(f"  Risk per trade:   {risk_pct}% = ${risk_amount:,.2f}")
print(f"  Entry price:      {entry}")
print(f"  Stop loss:        {stop}  ({price_risk:.2f} pts / {risk_pct_per_unit:.1f}%)")
print()
print(f"  POSITION SIZE:    {position_size:.4f} units")
print(f"  POSITION VALUE:   ${position_value:,.2f}")
print(f"  % of Capital:     {position_value/capital*100:.1f}%")
print()
print(f"  TAKE PROFIT TARGETS:")
print(f"    TP1 (1:2 R/R):  {tp1:.2f}  (+${risk_amount*2:,.2f})")
print(f"    TP2 (1:3 R/R):  {tp2:.2f}  (+${risk_amount*3:,.2f})")
print()
print(f"  RISK CHECK:")
if position_value / capital > 0.2:
    print(f"  ⚠️  Position is {position_value/capital*100:.0f}% of capital — consider reducing")
else:
    print(f"  ✅ Position sizing within safe limits")
print()
print("─"*47)
print("⚠️  Not financial advice. Educational only.")
print("Powered by BytesAgain | bytesagain.com")
PYEOF
}

cmd_portfolio() {
    local assets="" weights=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --assets)  assets="$2";  shift 2 ;;
            --weights) weights="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    [[ -z "$assets" ]] && _err "Usage: portfolio --assets 'BTC,ETH,SOL' --weights '40,30,30'"

    python3 - "$assets" "$weights" << 'PYEOF'
import sys
assets_str, weights_str = sys.argv[1], sys.argv[2]
assets = [a.strip() for a in assets_str.split(",")]
weights = [float(w.strip()) for w in weights_str.split(",")]

total = sum(weights)
weights_pct = [w/total*100 for w in weights]

print(f"\n{'═'*47}")
print(f"PORTFOLIO ANALYSIS")
print(f"{'═'*47}\n")
print(f"  {'Asset':<12} {'Allocation':>12} {'Weight%':>10}")
print(f"  {'─'*36}")
for a, w in zip(assets, weights_pct):
    flag = " ⚠️ Overweight" if w > 40 else ""
    print(f"  {a:<12} {'█'*int(w/5):<12} {w:>8.1f}%{flag}")

print(f"\n  Total: {total_w:.0f}%" if (total_w := sum(weights_pct)) else "")
print()
print("  DIVERSIFICATION SCORE:")
max_w = max(weights_pct)
if max_w > 50:
    print(f"  🔴 Concentrated — top asset is {max_w:.0f}% of portfolio")
elif max_w > 35:
    print(f"  🟡 Moderate — consider rebalancing for better spread")
else:
    print(f"  🟢 Diversified — allocation looks balanced")
print()
print("  SUGGESTED REBALANCE TRIGGER: ±5% drift from target")
print("─"*47)
print("⚠️  Not financial advice. Educational only.")
print("Powered by BytesAgain | bytesagain.com")
PYEOF
}

cmd_screener() {
    local market="crypto" filter=""
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --market) market="$2"; shift 2 ;;
            --filter) filter="$2"; shift 2 ;;
            *) shift ;;
        esac
    done
    echo ""
    echo "═══════════════════════════════════════════════"
    echo "SCREENER CRITERIA: $market"
    echo "═══════════════════════════════════════════════"
    echo ""
    echo "  Applied filters: ${filter:-default}"
    echo ""
    echo "  SCREENING LOGIC:"
    echo "  ┌─────────────────────────────────────────┐"
    IFS=',' read -ra FILTERS <<< "$filter"
    for f in "${FILTERS[@]}"; do
        f=$(echo "$f" | xargs)
        case "${f,,}" in
            rsi\<*) echo "  │ RSI Filter:     $f — oversold zone" ;;
            above-ma*) echo "  │ Trend Filter:   $f — above moving average" ;;
            volume-spike) echo "  │ Volume Filter:  Spike >2× average — momentum signal" ;;
            *) echo "  │ Filter:         $f" ;;
        esac
    done
    echo "  └─────────────────────────────────────────┘"
    echo ""
    echo "  NOTE: Connect to market data API (Binance/CoinGecko/yfinance)"
    echo "  to apply live screening. This tool generates the filter logic."
    echo ""
    echo "  Sample API for crypto screening:"
    echo "  curl 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=volume_desc&per_page=50'"
    echo ""
    echo "───────────────────────────────────────────────"
    echo "⚠️  Not financial advice. Educational only."
    echo "Powered by BytesAgain | bytesagain.com"
}

cmd_help() {
    cat << 'EOF'
Quant Trader — Build and analyze quantitative trading strategies
Powered by BytesAgain | bytesagain.com

Commands:
  strategy   Generate a quant trading strategy
  signal     Analyze price action and generate entry/exit signals
  risk       Calculate position size and risk metrics
  portfolio  Analyze portfolio allocation and correlation
  screener   Screen assets by technical criteria
  help       Show this help

Usage:
  bash scripts/script.sh strategy --asset BTC --timeframe 4h --style momentum
  bash scripts/script.sh signal --asset ETH --price 3200 --ma20 3050 --ma50 2900 --rsi 62
  bash scripts/script.sh risk --capital 10000 --risk-pct 1 --entry 3200 --stop 3050
  bash scripts/script.sh portfolio --assets "BTC,ETH,SOL,BNB" --weights "40,30,20,10"
  bash scripts/script.sh screener --market crypto --filter "rsi<35,above-ma200,volume-spike"

Styles: momentum, mean-reversion, breakout, trend-following
⚠️  For educational purposes only. Not financial advice.
More: https://bytesagain.com/skills | Feedback: https://bytesagain.com/feedback/
EOF
}

case "${1:-help}" in
    strategy)  shift; cmd_strategy "$@" ;;
    signal)    shift; cmd_signal "$@" ;;
    risk)      shift; cmd_risk "$@" ;;
    portfolio) shift; cmd_portfolio "$@" ;;
    screener)  shift; cmd_screener "$@" ;;
    help|*)    cmd_help ;;
esac
