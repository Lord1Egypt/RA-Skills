"""
Wave Scanner — Cedars Wave Method
Scans Binance Futures for high-probability wave entry setups
Usage: python3 wave_scanner.py [--alert] [--symbols BTC ETH SOL]
"""
import hmac, hashlib, json, subprocess, sys, argparse
from datetime import datetime

BASE = "https://testnet.binancefuture.com"
SYMBOLS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT", "AVAXUSDT", "LINKUSDT", "DOGEUSDT"]

def curl_get(path):
    r = subprocess.run(["curl.exe", "-s", BASE + path], capture_output=True)
    return json.loads(r.stdout.decode("utf-8"))

def ema(data, period):
    k = 2 / (period + 1)
    e = data[0]
    for v in data[1:]:
        e = v * k + e * (1 - k)
    return e

def rsi(closes, period=14):
    gains = losses = 0.0
    for i in range(1, period + 1):
        d = closes[i] - closes[i - 1]
        if d > 0: gains += d
        else: losses += abs(d)
    if losses == 0: return 100
    rs = (gains / period) / (losses / period)
    return round(100 - (100 / (1 + rs)), 1)

def avg_volume(klines, n=10):
    vols = [float(k[5]) for k in klines[-n-1:-1]]
    return sum(vols) / len(vols) if vols else 0

def scan_symbol(sym):
    try:
        klines_15m = curl_get(f"/fapi/v1/klines?symbol={sym}&interval=15m&limit=60")
        klines_1h  = curl_get(f"/fapi/v1/klines?symbol={sym}&interval=1h&limit=30")

        closes_15m = [float(k[4]) for k in klines_15m]
        closes_1h  = [float(k[4]) for k in klines_1h]

        price = closes_15m[-1]

        # EMAs on 15m
        e9  = ema(closes_15m[-20:], 9)
        e21 = ema(closes_15m[-30:], 21)
        e50 = ema(closes_15m[-60:], 50)

        # RSI on 15m (last 3 for trend)
        rsi_now  = rsi(closes_15m[-16:])
        rsi_prev = rsi(closes_15m[-17:-1])
        rsi_rising = rsi_now > rsi_prev

        # Volume
        last_vol = float(klines_15m[-1][5])
        avg_vol  = avg_volume(klines_15m, 10)
        vol_ratio = round(last_vol / avg_vol, 2) if avg_vol > 0 else 0

        # 1h trend
        e9_1h  = ema(closes_1h[-15:], 9)
        e21_1h = ema(closes_1h[-25:], 21)
        trend_1h = e9_1h > e21_1h

        # MACD (12/26/9) on 15m
        e12 = ema(closes_15m[-30:], 12)
        e26 = ema(closes_15m[-40:], 26)
        macd = e12 - e26
        macd_positive = macd > 0

        # Scoring — each = 1 point
        score = 0
        signals = []

        # Signal 1: EMA stack
        if e9 > e21 > e50:
            score += 1
            signals.append("EMA9>21>50 ✅")
        else:
            signals.append(f"EMA stack ❌ (9={round(e9,2)} 21={round(e21,2)} 50={round(e50,2)})")

        # Signal 2: RSI zone
        if 50 <= rsi_now <= 80:
            score += 1
            signals.append(f"RSI={rsi_now} ✅ (sweet zone)")
        elif rsi_now < 50:
            signals.append(f"RSI={rsi_now} ❌ (below 50, no momentum)")
        else:
            signals.append(f"RSI={rsi_now} ⚠️ (extended, reduce size)")

        # Signal 3: RSI rising
        if rsi_rising:
            score += 1
            signals.append(f"RSI rising ({rsi_prev}→{rsi_now}) ✅")
        else:
            signals.append(f"RSI falling ({rsi_prev}→{rsi_now}) ❌")

        # Signal 4: Volume
        if vol_ratio >= 1.3:
            score += 1
            signals.append(f"Volume {vol_ratio}x avg ✅")
        else:
            signals.append(f"Volume {vol_ratio}x avg ❌ (need >1.3x)")

        # Signal 5: 1h trend
        if trend_1h:
            score += 1
            signals.append("1h trend BULL ✅")
        else:
            signals.append("1h trend BEAR ❌")

        # Signal 6: MACD
        if macd_positive:
            score += 1
            signals.append(f"MACD positive ({round(macd,2)}) ✅")
        else:
            signals.append(f"MACD negative ({round(macd,2)}) ❌")

        # Entry suggestion
        entry_limit = round(e9, 4)  # limit order at EMA9
        tp_3pct = round(price * 1.03, 4)
        tp_5pct = round(price * 1.05, 4)
        stop = round(e21, 4)

        # Grade
        if score >= 5:   grade = "🔥 STRONG SETUP"
        elif score == 4: grade = "✅ VALID SETUP"
        elif score == 3: grade = "⚠️  WEAK SETUP"
        else:            grade = "❌ SKIP"

        return {
            "symbol": sym,
            "price": price,
            "score": score,
            "grade": grade,
            "rsi": rsi_now,
            "e9": round(e9, 4),
            "e21": round(e21, 4),
            "e50": round(e50, 4),
            "vol_ratio": vol_ratio,
            "macd": round(macd, 4),
            "signals": signals,
            "entry_limit": entry_limit,
            "tp_3pct": tp_3pct,
            "tp_5pct": tp_5pct,
            "stop": stop,
        }
    except Exception as ex:
        return {"symbol": sym, "error": str(ex), "score": 0, "grade": "❌ ERROR"}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbols", nargs="+", default=SYMBOLS)
    parser.add_argument("--min-score", type=int, default=3)
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  CEDARS WAVE SCANNER — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    results = []
    for sym in args.symbols:
        r = scan_symbol(sym)
        results.append(r)

    # Sort by score
    results.sort(key=lambda x: x.get("score", 0), reverse=True)

    for r in results:
        if r.get("score", 0) < args.min_score:
            continue
        print(f"{'─'*50}")
        print(f"  {r['symbol']} — {r['grade']} ({r['score']}/6)")
        print(f"  Price: {r.get('price')} | RSI: {r.get('rsi')} | Vol: {r.get('vol_ratio')}x")
        print(f"  EMA9={r.get('e9')} EMA21={r.get('e21')} EMA50={r.get('e50')}")
        print(f"  MACD: {r.get('macd')}")
        print(f"  📍 Entry limit: {r.get('entry_limit')}")
        print(f"  🎯 TP (3%): {r.get('tp_3pct')} | TP (5%): {r.get('tp_5pct')}")
        print(f"  🛑 Stop (EMA21): {r.get('stop')}")
        print()
        for sig in r.get("signals", []):
            print(f"     {sig}")
        print()

    # Summary
    hot = [r for r in results if r.get("score", 0) >= 5]
    valid = [r for r in results if r.get("score", 0) == 4]
    print(f"\n{'='*60}")
    print(f"  SUMMARY: {len(hot)} STRONG | {len(valid)} VALID | {len(results)-len(hot)-len(valid)} SKIP")
    if hot:
        print(f"  🔥 BEST: {hot[0]['symbol']} score={hot[0]['score']}/6 RSI={hot[0].get('rsi')}")
    elif valid:
        print(f"  ✅ BEST: {valid[0]['symbol']} score={valid[0]['score']}/6 RSI={valid[0].get('rsi')}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
