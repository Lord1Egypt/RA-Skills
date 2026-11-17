#!/usr/bin/env python3
"""DRT Self-Improving Agent — analyze.py
Analysér trades.json og udskriv konkrete læringer (agenten bliver bedre pr. trade).
Eksempel:
  python3 analyze.py              # fuld analyse
  python3 analyze.py --symbol BTC # kun BTC
"""
import argparse, json, os, sys
from collections import defaultdict

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB = os.path.join(DATA_DIR, "trades.json")

def load():
    if not os.path.exists(DB):
        print("📭 Ingen trades endnu — journalisér med scripts/journal.py")
        sys.exit(0)
    with open(DB) as f:
        return json.load(f)

def wr(trades, pred=lambda t: True):
    sel = [t for t in trades if pred(t)]
    if not sel:
        return None
    wins = sum(1 for t in sel if t.get("result") == "win")
    return wins / len(sel), len(sel)

def fmt(wr_res):
    if not wr_res:
        return "n/a"
    w, n = wr_res
    return f"{w*100:.0f}% ({n} trades)"

def main():
    p = argparse.ArgumentParser(description="Analysér DRT-trade-hukommelse")
    p.add_argument("--symbol", default=None)
    p.add_argument("--min-trades", type=int, default=3)
    a = p.parse_args()

    trades = load()
    if a.symbol:
        trades = [t for t in trades if t["symbol"] == a.symbol.upper()]
    if not trades:
        print("📭 Ingen trades matcher filteret")
        sys.exit(0)

    total = len(trades)
    wins = sum(1 for t in trades if t.get("result") == "win")
    print(f"📊 HUKOMMELSE: {total} trades · {wins} wins · {total-wins} losses · WR {wins/total*100:.0f}%")
    print("=" * 56)

    # Per DRT-type
    for t in (1, 2, 3):
        r = wr(trades, lambda x, t=t: x.get("type") == t)
        if r and r[1] >= a.min_trades:
            w, n = r
            advice = "KØR PÅ! 💪" if w >= 0.8 else ("Vær selektiv" if w >= 0.6 else "UNDGÅ ⛔")
            print(f"Type {t}: {fmt(r)} → {advice}")

    # Per bias
    for b in ("LONG", "SHORT"):
        r = wr(trades, lambda x, b=b: x.get("bias") == b)
        if r and r[1] >= a.min_trades:
            print(f"{b}: {fmt(r)}")

    # Per killzone
    kz = defaultdict(list)
    for t in trades:
        kz[t.get("killzone") or "?"].append(t)
    for zone, zt in sorted(kz.items(), key=lambda kv: -len(kv[1])):
        if len(zt) >= a.min_trades:
            print(f"Killzone {zone}: {fmt(wr(zt))}")

    # R:R-opdeling
    low_rr = [t for t in trades if (t.get("rr") or 0) < 1.5]
    high_rr = [t for t in trades if (t.get("rr") or 0) >= 2.0]
    if len(low_rr) >= a.min_trades:
        print(f"R:R < 1.5: {fmt(wr(low_rr))} → (lav R:R giver ofte lav WR)")
    if len(high_rr) >= a.min_trades:
        print(f"R:R >= 2.0: {fmt(wr(high_rr))}")

    # Top 3 læringer
    print("\n🧠 LÆRINGER:")
    lessons = []
    for t in (1, 2, 3):
        r = wr(trades, lambda x, t=t: x.get("type") == t)
        if r and r[1] >= a.min_trades and r[0] >= 0.8:
            lessons.append(f"Type {t} vinder {r[0]*100:.0f}% — fortsæt med disse setups")
        elif r and r[1] >= a.min_trades and r[0] < 0.5:
            lessons.append(f"Type {t} vinder kun {r[0]*100:.0f}% — skærp filter eller spring over")
    for zone, zt in sorted(kz.items(), key=lambda kv: -(wr(kv[1])[0] if wr(kv[1]) else 0)):
        r = wr(zt)
        if r and r[1] >= a.min_trades and r[0] < 0.5:
            lessons.append(f"{zone}-trades taber ({r[0]*100:.0f}%) — undgå dette vindue")
    if len(low_rr) >= a.min_trades and wr(low_rr)[0] < 0.6:
        lessons.append("R:R < 1.5 giver lav WR — vent på 2R+ setups")
    if not lessons:
        lessons.append("For lidt data endnu — journalisér flere trades, så lærer agenten")
    for i, l in enumerate(lessons[:5], 1):
        print(f"  {i}. {l}")

    print("\n💡 Næste skridt: journalisér hver trade med scripts/journal.py")

if __name__ == "__main__":
    main()
