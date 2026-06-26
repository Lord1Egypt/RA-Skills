"""Check prices for BTC and ETH - CoinEx API (China accessible)"""
import json, urllib.request

COINEX = "https://api.coinex.com/v1"

def get_price(symbol):
    try:
        r = urllib.request.urlopen(f"{COINEX}/market/ticker?market={symbol}USDT", timeout=10)
        d = json.loads(r.read())
        if d.get("code") == 0:
            t = d["data"]["ticker"]
            p = float(t["last"])
            o = float(t["open"])
            h = float(t["high"])
            l = float(t["low"])
            v = float(t["vol"])
            c = (p - o) / o * 100
            return {"price": p, "change": c, "high": h, "low": l, "vol": v}
    except:
        return None

def get_kline(symbol, period="1day", limit=30):
    try:
        r = urllib.request.urlopen(f"{COINEX}/market/kline?market={symbol}USDT&type={period}&limit={limit}", timeout=10)
        d = json.loads(r.read())
        if d.get("code") == 0:
            return [[float(x) for x in k] for k in d["data"]]
    except:
        return None
    return None

if __name__ == "__main__":
    for sym in ["BTC", "ETH"]:
        p = get_price(sym)
        if p:
            ic = "↑" if p["change"] >= 0 else "↓"
            print(f"{sym}: ${p['price']:,.2f} {ic} {abs(p['change']):.2f}%  (24h ${p['low']:,.0f}~${p['high']:,.0f})")
