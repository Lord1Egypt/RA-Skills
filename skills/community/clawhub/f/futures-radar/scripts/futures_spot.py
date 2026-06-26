"""
期货雷达 - WTI原油/黄金/白银/天然气/铜 等大宗商品实时行情
使用 Yahoo Finance chart API
"""
import requests

SYMBOLS = {
    # 能源
    "CL=F":  ("WTI原油",       "NYMEX WTI 原油期货",    "桶"),
    "BZ=F":  ("布伦特原油",    "ICE 布伦特原油期货",    "桶"),
    "NG=F":  ("天然气",        "NYMEX 天然气期货",       "百万英热"),
    # 贵金属
    "GC=F":  ("黄金",         "COMEX 黄金期货",         "盎司"),
    "SI=F":  ("白银",         "COMEX 白银期货",         "盎司"),
    "PL=F":  ("铂金",         "NYMEX 铂金期货",        "盎司"),
    "PA=F":  ("钯金",         "NYMEX 钯金期货",        "盎司"),
    # 基本金属
    "HG=F":  ("铜",           "COMEX 铜期货",           "磅"),
    # 农产品
    "ZC=F":  ("玉米",         "CBOT 玉米期货",          "蒲式耳"),
    "ZS=F":  ("大豆",         "CBOT 大豆期货",          "蒲式耳"),
    "ZW=F":  ("小麦",         "CBOT 小麦期货",          "蒲式耳"),
    # 美国国债期货（利率预期）
    "ZN=F":  ("10年国债期货",  "CBOT 10年期国债期货",   "面值100"),
    "ZB=F":  ("30年国债期货",  "CBOT 30年期国债期货",   "面值100"),
    # 宏观指数
    "DX-Y.NYB": ("DXY美元指数",  "ICE 美元指数",         "点"),
}

CATEGORIES = {
    "能源":    ["CL=F", "BZ=F", "NG=F"],
    "贵金属":  ["GC=F", "SI=F", "PL=F", "PA=F"],
    "基本金属": ["HG=F"],
    "农产品":  ["ZC=F", "ZS=F", "ZW=F"],
    "国债":    ["ZN=F", "ZB=F"],
    "宏观":    ["DX-Y.NYB"],
}

def get_quote(symbol):
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1d"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            return None
        d = r.json()
        meta = d["chart"]["result"][0]["meta"]
        price = meta.get("regularMarketPrice")
        prev = meta.get("chartPreviousClose") or meta.get("previousClose")
        high = meta.get("regularMarketDayHigh")
        low = meta.get("regularMarketDayLow")
        if price is None or prev is None or prev == 0:
            return None
        chg = price - prev
        pct = chg / prev * 100
        return {"price": price, "prev": prev, "chg": chg, "pct": pct, "high": high, "low": low}
    except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
        return None

def fmt_contract(q, sym, info):
    name, _, unit_name = info
    arrow = "🔴" if q["chg"] > 0 else "🟢" if q["chg"] < 0 else "⚪"
    price_prefix = "" if sym == "DX-Y.NYB" else "$"
    high = "--" if q["high"] is None else q["high"]
    low = "--" if q["low"] is None else q["low"]
    return (f"{arrow} {name:8s} {price_prefix}{q['price']:>10.2f}  "
            f"{q['chg']:>+8.2f}({q['pct']:>+6.2f}%)  "
            f"高:{high} 低:{low} {unit_name}")

def main():
    print("\n" + "=" * 65)
    print("  🛢️  期货雷达 — 大宗商品实时行情")
    print("=" * 65)

    all_quotes = {}
    for sym in SYMBOLS:
        q = get_quote(sym)
        if q:
            all_quotes[sym] = q

    for cat, syms in CATEGORIES.items():
        has_data = any(s in all_quotes for s in syms)
        if not has_data:
            continue
        print(f"\n【{cat}】")
        for sym in syms:
            if sym not in all_quotes:
                continue
            info = SYMBOLS[sym]
            q = all_quotes[sym]
            print(f"  {fmt_contract(q, sym, info)}")

    print("\n" + "=" * 65)

    # 关键比价分析
    if "GC=F" in all_quotes and "CL=F" in all_quotes and "SI=F" in all_quotes:
        au = all_quotes["GC=F"]
        ag = all_quotes["SI=F"]
        oil = all_quotes["CL=F"]
        if ag["price"] > 0:
            gsr = au["price"] / ag["price"]  # 金银比
            print(f"\n📐 关键比价:")
            print(f"  金银比 (GC/SI): {gsr:.1f}  (均值约80，高→银相对便宜)")
        if oil["price"] > 0 and au["price"] > 0:
            oil_au = oil["price"] / (au["price"] / 100)  # 油价/金价(归一化)
            print(f"  油金比: {oil_au:.2f}  (高→通胀预期强，低→避险)")

    # DXY 美元指数分析
    dxy = all_quotes.get("DX-Y.NYB")
    if dxy:
        dxy_val = dxy["price"]
        print(f"\n🌍 美元指数: {dxy_val:.2f}  {dxy['pct']:+.2f}%")
        if dxy_val > 104:
            print(f"  → 美元强势(>{104}) 大宗商品承压 黄金/原油倾向下跌 🟢")
        elif dxy_val < 100:
            print(f"  → 美元弱势(<{100}) 大宗商品获支撑 黄金/原油倾向上涨 🔴")
        else:
            print(f"  → 美元中性({100}~{104}) 大宗商品区间震荡")

if __name__ == "__main__":
    print("正在获取期货数据...")
    main()
