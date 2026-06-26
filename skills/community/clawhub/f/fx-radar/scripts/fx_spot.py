"""
汇率雷达 - 全球主要货币对实时行情
数据源: Yahoo Finance forex (USDCNY=X, USDHKD=X 等)
备用: European Central Bank (frankfurter.app)
"""
import requests

# Yahoo Finance 汇率代码
FOREX_PAIRS = {
    # 亚洲
    "USDCNY=X":  ("USD/CNY",  "💴 美元/在岸人民币",  "🇨🇳 中国"),
    "USDHKD=X":  ("USD/HKD",  "💴 美元/港元",        "🇭🇰 香港"),
    "USDCNH=X":  ("USD/CNH",  "💴 美元/离岸人民币",  "🇭🇰 CNH"),
    "USDJPY=X":  ("USD/JPY",  "💴 美元/日元",        "🇯🇵 日本"),
    "USDKRW=X":  ("USD/KRW",  "💴 美元/韩元",        "🇰🇷 韩国"),
    "USDSGD=X":  ("USD/SGD",  "💴 美元/新加坡元",    "🇸🇬 新加坡"),
    "USDTHB=X":  ("USD/THB",  "💴 美元/泰铢",        "🇹🇭 泰国"),
    "USDTWD=X":  ("USD/TWD",  "💴 美元/台币",        "🇹🇼 台湾"),
    "USDVND=X":  ("USD/VND",  "💴 美元/越南盾",      "🇻🇳 越南"),
    # 发达市场
    "EURUSD=X":  ("EUR/USD",  "💶 欧元/美元",        "🇪🇺 欧元区"),
    "GBPUSD=X":  ("GBP/USD",  "💷 英镑/美元",        "🇬🇧 英国"),
    "AUDUSD=X":  ("AUD/USD",  "💳 澳元/美元",        "🇦🇺 澳大利亚"),
    "NZDUSD=X":  ("NZD/USD",  "🇳🇿 纽元/美元",      "🇳🇿 新西兰"),
    "USDCHF=X":  ("USD/CHF",  "💴 美元/瑞郎",        "🇨🇭 瑞士"),
    "USDCAD=X":  ("USD/CAD",  "💴 美元/加元",        "🇨🇦 加拿大"),
    # 黄金/商品货币
    "DX-Y.NYB":  ("DXY",      "📊 美元指数(DXY)",     "🌐 美元"),
}

# ECB 备用数据（frankfurter.app）
ECB_PAIRS = ["CNY", "HKD", "JPY", "EUR", "GBP", "AUD", "CHF", "CAD", "NZD", "KRW", "SGD", "THB"]
INVERTED_ECB_PAIRS = {"EUR", "GBP", "AUD", "NZD"}

def get_yahoo_forex():
    """Yahoo Finance 获取汇率（主数据源）"""
    results = {}
    import concurrent.futures
    def _fetch_one(sym):
        try:
            url = f"https://query2.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=1d"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
            r.raise_for_status()
            d = r.json()
            meta = d["chart"]["result"][0]["meta"]
            price = meta.get("regularMarketPrice")
            prev = meta.get("chartPreviousClose") or meta.get("previousClose")
            if price is None or prev is None or prev == 0:
                return None
            chg = price - prev
            pct = chg / prev * 100
            name, label, flag = FOREX_PAIRS[sym]
            return sym, {
                "name": name, "label": label, "flag": flag,
                "price": price, "chg": chg, "pct": pct
            }
        except Exception:
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(_fetch_one, sym): sym for sym in FOREX_PAIRS}
        for f in concurrent.futures.as_completed(futures, timeout=20):
            result = f.result()
            if result is not None:
                sym, data = result
                results[sym] = data

    return results

def get_ecb_forex():
    """欧洲央行汇率（备用数据源，不需要 key）"""
    results = {}
    try:
        url = f"https://api.frankfurter.app/latest?base=USD&symbols={','.join(ECB_PAIRS)}"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        r.raise_for_status()
        data = r.json().get("rates", {})
        for curr, rate in data.items():
            if curr in INVERTED_ECB_PAIRS:
                if not rate:
                    continue
                sym = f"{curr}USD=X"
                name = f"{curr}/USD"
                price = 1 / rate
            else:
                sym = f"USD{curr}=X"
                name = f"USD/{curr}"
                price = rate
            results[sym] = {
                "name": name, "label": name,
                "flag": "🌐", "price": price,
                "chg": 0, "pct": 0, "source": "ECB"
            }
    except (requests.RequestException, ValueError):
        pass
    return results

def fmt_row(item):
    """格式化一行汇率数据"""
    label = item["label"]
    price = item["price"]
    pct = item.get("pct", 0)
    if pct == 0:
        pct_str = "  --"
    else:
        pct_str = f"{pct:>+6.2f}%"
    arrow = "🔴" if pct > 0 else "🟢" if pct < 0 else "⚪"
    # 特殊处理：汇率小于1的显示更多小数位
    if price and price < 0.01:
        price_str = f"{price:.6f}"
    elif price and price < 1:
        price_str = f"{price:.4f}"
    elif price and price < 100:
        price_str = f"{price:.4f}"
    else:
        price_str = f"{price:.2f}"
    return f"  {arrow} {label:30s} {price_str:>12s}  {pct_str}"

def main():
    print("\n" + "=" * 70)
    print("  💱 汇率雷达 — 全球主要货币对")
    print("=" * 70)
    print("\n正在获取数据...")

    yahoo_data = get_yahoo_forex()
    ecb_data = get_ecb_forex()

    # 合并：优先 Yahoo，备用 ECB
    all_data = {**ecb_data, **yahoo_data}

    if not all_data:
        print("❌ 所有数据源均获取失败，请检查网络后重试")
        return

    # 分类显示
    asia = ["USDCNY=X", "USDHKD=X", "USDCNH=X", "USDJPY=X", "USDKRW=X",
            "USDSGD=X", "USDTHB=X", "USDTWD=X", "USDVND=X"]
    majors = ["EURUSD=X", "GBPUSD=X", "AUDUSD=X", "NZDUSD=X", "USDCHF=X", "USDCAD=X"]

    print("\n【 💴 亚洲货币 】")
    for sym in asia:
        if sym in all_data:
            print(fmt_row(all_data[sym]))

    print("\n【 💶 发达市场货币 】")
    for sym in majors:
        if sym in all_data:
            print(fmt_row(all_data[sym]))

    if "DX-Y.NYB" in all_data:
        print("\n【 📊 美元指数 】")
        print(fmt_row(all_data["DX-Y.NYB"]))

    # 关键汇率解读
    print("\n" + "=" * 70)
    print("\n📐 关键汇率解读:")

    signals = []

    if "USDCNY=X" in all_data:
        cny = all_data["USDCNY=X"]["price"]
        if cny > 7.30:
            signals.append(f"USD/CNY={cny:.4f} → 人民币偏弱，贬值压力 ⚠️")
        elif cny < 7.10:
            signals.append(f"USD/CNY={cny:.4f} → 人民币偏强 🟢")
        else:
            signals.append(f"USD/CNY={cny:.4f} → 人民币区间震荡")

    if "USDJPY=X" in all_data:
        jpy = all_data["USDJPY=X"]["price"]
        if jpy > 150:
            signals.append(f"USD/JPY={jpy:.2f} → 日本干预风险！⚠️")
        elif jpy < 145:
            signals.append(f"USD/JPY={jpy:.2f} → 日央行容忍区间")
        else:
            signals.append(f"USD/JPY={jpy:.2f} → 正常区间")

    if "EURUSD=X" in all_data:
        eur = all_data["EURUSD=X"]["price"]
        if eur > 1.10:
            signals.append(f"EUR/USD={eur:.4f} → 欧元强势 🔴")
        elif eur < 1.05:
            signals.append(f"EUR/USD={eur:.4f} → 欧元弱势 🟢")
        else:
            signals.append(f"EUR/USD={eur:.4f} → 欧元中性")

    if "USDCNH=X" in all_data and "USDCNY=X" in all_data:
        cnh = all_data["USDCNH=X"]["price"]
        cny = all_data["USDCNY=X"]["price"]
        diff = (cnh - cny) * 10000  # 转为pip
        if diff > 50:
            signals.append(f"CNH-CNY利差={diff:+.0f}pips → 离岸人民币弱于在岸，外流压力偏大 ⚠️")
        elif diff < -50:
            signals.append(f"CNH-CNY利差={diff:+.0f}pips → 离岸人民币强于在岸，离岸情绪偏稳 🟢")

    for s in signals:
        print(f"  {s}")

    if not signals:
        print("  (数据不足，无法生成解读)")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
