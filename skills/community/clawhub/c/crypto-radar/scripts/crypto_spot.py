"""
数字货币雷达 - 加密货币实时行情
三数据源：Yahoo Finance(主) + CoinGecko(次) + Binance/HTML(备用)
"""
import requests

# Yahoo Finance 实时价格
YAHOO_SYMBOLS = {
    "BTC-USD": "比特币BTC",
    "ETH-USD": "以太坊ETH",
    "SOL-USD": "Solana",
    "BNB-USD": "币安币BNB",
    "XRP-USD": "XRP",
    "DOGE-USD": "狗狗币DOGE",
    "ADA-USD": "艾达币ADA",
    "AVAX-USD": "雪崩AVAX",
    "DOT-USD": "波卡DOT",
    "MATIC-USD": "Polygon",
}

MACRO_SYMBOLS = {
    "DX-Y.NYB": "DXY美元指数",
    "^VIX": "VIX恐慌指数",
}

# CoinGecko ID 映射
COINGECKO_IDS = {
    "BTC-USD": "bitcoin",
    "ETH-USD": "ethereum",
    "SOL-USD": "solana",
    "BNB-USD": "binancecoin",
    "XRP-USD": "ripple",
    "DOGE-USD": "dogecoin",
    "ADA-USD": "cardano",
    "AVAX-USD": "avalanche-2",
    "DOT-USD": "polkadot",
    "MATIC-USD": "matic-network",
}

def get_yahoo_quote(sym):
    url = f"https://query2.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=1d"
    r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    r.raise_for_status()
    meta = r.json()["chart"]["result"][0]["meta"]
    price = meta.get("regularMarketPrice")
    prev = meta.get("chartPreviousClose") or meta.get("previousClose")
    if price is None or prev in (None, 0):
        return None
    chg = price - prev
    pct = chg / prev * 100
    return {"price": price, "chg": chg, "pct": pct}

def get_yahoo_quotes():
    """Yahoo Finance 获取实时价格（容错）"""
    results = {}
    for sym, name in YAHOO_SYMBOLS.items():
        try:
            quote = get_yahoo_quote(sym)
            if quote:
                results[sym] = {"name": name, **quote}
        except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
            continue
    return results

def get_macro_quotes():
    """Yahoo Finance 获取宏观指标（DXY + VIX，容错）"""
    results = {}
    for sym, name in MACRO_SYMBOLS.items():
        try:
            quote = get_yahoo_quote(sym)
            if quote:
                results[sym] = {"name": name, **quote}
        except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
            continue
    return results

def get_binance_prices():
    """
    Binance 价格备用（当 Yahoo Finance / CoinGecko 均失败时调用）
    数据来源：Binance 公开 Web API（无需认证）
    """
    # Binance 24hr ticker API 一次获取多个交易对
    symbols = ["BTCUSDT","ETHUSDT","SOLUSDT","BNBUSDT","XRPUSDT",
               "DOGEUSDT","ADAUSDT","AVAXUSDT","DOTUSDT","MATICUSDT"]
    headers = {"User-Agent": "Mozilla/5.0", "X-MBX-APIKEY": "fake"}
    results = {}
    BINANCE_ID_MAP = {
        "BTCUSDT": "BTC-USD", "ETHUSDT": "ETH-USD", "SOLUSDT": "SOL-USD",
        "BNBUSDT": "BNB-USD", "XRPUSDT": "XRP-USD", "DOGEUSDT": "DOGE-USD",
        "ADAUSDT": "ADA-USD", "AVAXUSDT": "AVAX-USD", "DOTUSDT": "DOT-USD",
        "MATICUSDT": "MATIC-USD",
    }
    try:
        # Binance 组合行情 API（单个请求获取多个symbol）
        url = "https://api.binance.com/api/v3/ticker/24hr"
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            raise ValueError(f"Binance {r.status_code}")
        tickers = {t["symbol"]: t for t in r.json()}
        for sym, yahoo_sym in BINANCE_ID_MAP.items():
            ticker = tickers.get(sym)
            if not ticker:
                continue
            try:
                price = float(ticker["lastPrice"])
                pct = float(ticker["priceChangePercent"])
                chg = float(ticker["priceChange"])
                results[yahoo_sym] = {
                    "name": YAHOO_SYMBOLS[yahoo_sym],
                    "price": price, "chg": chg, "pct": pct,
                }
            except (ValueError, KeyError):
                continue
    except Exception:
        pass
    return results


def get_coingecko_markets():
    """CoinGecko 获取市值和交易量"""
    ids = ",".join(COINGECKO_IDS.values())
    url = (f"https://api.coingecko.com/api/v3/coins/markets"
           f"?vs_currency=usd&ids={ids}&order=market_cap_desc"
           f"&per_page=10&sparkline=false&price_change_percentage=24h")
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        if r.status_code == 200:
            return {c["id"]: c for c in r.json()}
        if r.status_code == 429:
            return {}
    except (requests.RequestException, ValueError, TypeError):
        return {}
    return {}

def fmt_row(name, price, pct, chg, mcap=None, vol=None, indent=""):
    arrow = "🔴" if pct > 0 else "🟢" if pct < 0 else "⚪"
    pct_str = f"{pct:>+7.2f}%"
    price_str = f"${price:>12,.2f}" if price >= 1 else f"${price:>12.6f}"
    chg_str = f"{chg:+.2f}" if price >= 1 else f"{chg:+.6f}"
    line1 = f"{indent}{arrow} {name:12s}  {price_str}  {chg_str:>12s}"
    if mcap is not None and vol is not None:
        mc_str = f"MCap:${mcap/1e12:>6.2f}T" if mcap >= 1e12 else f"MCap:${mcap/1e9:>6.2f}B"
        vol_str = f"Vol24h:${vol/1e9:>5.2f}B"
        line1 += f"  {pct_str}  {mc_str}  {vol_str}"
    else:
        line1 += f"  {pct_str}"
    return line1

def get_coingecko_price_fallback(markets):
    results = {}
    for sym, coin_id in COINGECKO_IDS.items():
        market = markets.get(coin_id)
        if not market:
            continue
        price = market.get("current_price")
        pct = market.get("price_change_percentage_24h")
        chg = market.get("price_change_24h")
        if price is None or pct is None or chg is None:
            continue
        results[sym] = {
            "name": YAHOO_SYMBOLS[sym],
            "price": price,
            "chg": chg,
            "pct": pct,
        }
    return results

def main():
    print("\n" + "=" * 75)
    print("  🪙 数字货币雷达 — 实时行情")
    print("=" * 75)

    print("\n正在获取数据...")
    quotes = get_yahoo_quotes()
    markets = get_coingecko_markets()
    fallback_quotes = get_coingecko_price_fallback(markets)
    for sym, data in fallback_quotes.items():
        quotes.setdefault(sym, data)
    # 三层兜底：Binance（Yahoo+CG均失败时）
    if not quotes:
        quotes = get_binance_prices()
    macro = get_macro_quotes()

    # 当前跟踪币种市值汇总（非全市场）
    total_mcap = sum(
        (markets.get(cgid, {}).get("market_cap") or 0)
        for cgid in COINGECKO_IDS.values()
    )
    btc_mcap = markets.get("bitcoin", {}).get("market_cap") or 0
    eth_mcap = markets.get("ethereum", {}).get("market_cap") or 0
    tracked_btc_share = btc_mcap / total_mcap * 100 if total_mcap > 0 else 0

    # BTC/ETH/SOL 第一梯队
    print("\n【 🥇 主流加密货币 】")
    for sym in ["BTC-USD", "ETH-USD", "SOL-USD"]:
        if sym not in quotes:
            continue
        q = quotes[sym]
        cgid = COINGECKO_IDS.get(sym)
        mkt = markets.get(cgid, {}) if cgid else {}
        print(fmt_row(q["name"], q["price"], q["pct"], q["chg"],
                      mkt.get("market_cap"), mkt.get("total_volume")))

    # 平台币 + 山寨
    tier2 = ["BNB-USD", "XRP-USD", "ADA-USD", "DOGE-USD"]
    tier2_names = {s: quotes.get(s) for s in tier2}
    if any(tier2_names.values()):
        print("\n【 🥈 平台币 & 山寨 】")
        for sym in tier2:
            if sym not in quotes:
                continue
            q = quotes[sym]
            cgid = COINGECKO_IDS.get(sym)
            mkt = markets.get(cgid, {}) if cgid else {}
            print(fmt_row(q["name"], q["price"], q["pct"], q["chg"],
                          mkt.get("market_cap"), mkt.get("total_volume")))

    # L2 / 其他
    tier3 = ["AVAX-USD", "DOT-USD", "MATIC-USD"]
    tier3_data = {s: quotes.get(s) for s in tier3}
    if any(tier3_data.values()):
        print("\n【 🥉 L2 & 波卡生态 】")
        for sym in tier3:
            if sym not in quotes:
                continue
            q = quotes[sym]
            cgid = COINGECKO_IDS.get(sym)
            mkt = markets.get(cgid, {}) if cgid else {}
            print(fmt_row(q["name"], q["price"], q["pct"], q["chg"],
                          mkt.get("market_cap"), mkt.get("total_volume")))

    # 关键比值分析
    print("\n" + "=" * 75)
    print("\n📐 关键比值:")
    print(f"  跟踪篮子中 BTC 市值占比: {tracked_btc_share:.1f}%")
    if "ETH-USD" in quotes and "BTC-USD" in quotes:
        eth_btc = quotes["ETH-USD"]["price"] / quotes["BTC-USD"]["price"]
        print(f"  ETH/BTC:       {eth_btc:.5f}  (<0.030弱势 / >0.050强势)")
    print(f"  跟踪篮子总市值: ${total_mcap/1e12:.3f}T")

    # 宏观数据
    if macro:
        print("\n🌍 宏观背景:")
        for sym, m in macro.items():
            arrow = "🔴" if m["pct"] > 0 else "🟢" if m["pct"] < 0 else "⚪"
            print(f"  {arrow} {m['name']}: {m['price']:.2f}  {m['pct']:+.2f}%")
        # DXY 信号解读
        dxy = macro.get("DX-Y.NYB")
        if dxy:
            dxy_val = dxy["price"]
            if dxy_val > 104:
                print(f"  → DXY强势(>{104})  美元强 → 加密货币承压 🟢")
            elif dxy_val < 100:
                print(f"  → DXY弱势(<{100})  美元弱 → 加密货币利好 🔴")
            else:
                print(f"  → DXY中性({100}~{104})  加密货币区间震荡")
        vix = macro.get("^VIX")
        if vix:
            vix_val = vix["price"]
            if vix_val > 25:
                print(f"  → VIX高({vix_val:.0f})  市场恐慌 → 避险优先 🟢BTC")
            elif vix_val < 15:
                print(f"  → VIX低({vix_val:.0f})  风险偏好 → 山寨有机会 🔴Altcoin")
            else:
                print(f"  → VIX中性({vix_val:.0f})  平衡市")

    print("\n" + "=" * 75)

if __name__ == "__main__":
    main()
