#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日K线 + 均线（多数据源自动切换）
  A股/指数：新浪 openapi（首选，稳）→ 同花顺 d.10jqka（兜底，限流频低）
  期货：新浪 finance.sina（首选）→ 东财 push2his（兜底）
用法：
  python3 kline.py 600519              # 个股
  python3 kline.py 000001 上证指数 创业板指
  python3 kline.py 淀粉 螺纹钢          # 期货（中文名/Sina代码）
  python3 kline.py 600519 30 --q 0     # 30根K线；--q 0=不复权 1=前复权(默认，仅同花顺)
输出：最近 N 根 OHLCV + MA5/10/20 + 多空排列
"""
import sys, json, re, time, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
HDR_SINA = {"User-Agent": UA, "Referer": "https://finance.sina.com.cn/"}
HDR_THS = {"User-Agent": UA, "Referer": "https://stockpage.10jqka.com.cn/",
           "Accept": "*/*", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "keep-alive"}

# 指数：名称 → 新浪代码 / 同花顺代码
INDEX = {
    "上证指数": ("sh000001", "1A0001"), "上证": ("sh000001", "1A0001"), "大盘": ("sh000001", "1A0001"),
    "深证成指": ("sz399001", "399001"), "深成指": ("sz399001", "399001"), "深证": ("sz399001", "399001"),
    "创业板指": ("sz399006", "399006"), "创业板": ("sz399006", "399006"), "创指": ("sz399006", "399006"),
    "沪深300": ("sh000300", None), "中证500": ("sh000905", "399905"),
    "中证1000": ("sh000852", "399852"), "科创50": ("sh000688", "1B0688"),
}
FUT = {"螺纹钢": "RB0", "螺纹": "RB0", "热卷": "HC0", "铁矿石": "I0", "铁矿": "I0",
       "沪铜": "CU0", "铜": "CU0", "沪铝": "AL0", "沪锌": "ZN0", "沪镍": "NI0",
       "黄金": "AU0", "沪金": "AU0", "白银": "AG0", "沪银": "AG0", "原油": "SC0",
       "燃油": "FU0", "沥青": "BU0", "橡胶": "RU0",
       "豆粕": "M0", "豆油": "Y0", "棕榈油": "P0", "玉米": "C0", "淀粉": "CS0",
       "玉米淀粉": "CS0", "鸡蛋": "JD0", "生猪": "LH0", "塑料": "L0", "聚丙烯": "PP0",
       "PVC": "V0", "乙二醇": "EG0", "焦炭": "J0", "焦煤": "JM0",
       "甲醇": "MA0", "PTA": "TA0", "纯碱": "SA0", "玻璃": "FG0", "白糖": "SR0",
       "棉花": "CF0", "菜粕": "RM0",
       "沪深300股指": "IF0", "上证50": "IH0", "中证500股指": "IC0", "中证1000股指": "IM0"}

def _get(url, headers, gbk=False, retries=5):
    last = None
    for k in range(retries):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=15).read()
            return raw.decode("gbk", "replace") if gbk else raw.decode("utf-8", "replace")
        except Exception as e:  # 404/502/超时 → 退避重试（同花顺/新浪会瞬时限流）
            last = e
            time.sleep(3 * (k + 1))
    raise last

def _jsonp(txt):
    m = re.search(r"\((\{.*\}|\[.*\])\)\s*;?\s*$", txt, re.S)
    return json.loads(m.group(1)) if m else json.loads(txt)

# ---------- A股/指数 ----------
def sina_stock_kline(symbol, n):
    txt = _get("https://quotes.sina.cn/cn/api/openapi.php/CN_MarketDataService.getKLineData"
               f"?symbol={symbol}&scale=240&ma=no&datalen={n}", HDR_SINA)
    d = json.loads(txt)["result"]["data"]
    return [(x["day"], float(x["open"]), float(x["high"]), float(x["low"]),
             float(x["close"]), float(x["volume"]), 0.0, "") for x in d]

def ths_stock_kline(code, q, n):
    txt = _get(f"https://d.10jqka.com.cn/v6/line/hs_{code}/{q}/last.js", HDR_THS)
    d = _jsonp(txt)
    bars = []
    for row in d.get("data", "").split(";"):
        p = row.split(",")
        if len(p) < 6 or not p[0]:
            continue
        try:
            bars.append((p[0], float(p[1]), float(p[2]), float(p[3]), float(p[4]),
                         float(p[5]), float(p[6]) if len(p) > 6 and p[6] else 0.0, p[7] if len(p) > 7 else ""))
        except Exception:
            continue
    return d.get("name", code), bars

# ---------- 期货 ----------
def sina_futures_kline(symbol, n):
    txt = _get("https://stock2.finance.sina.com.cn/futures/api/jsonp_v2.php/var%20t=/"
               f"InnerFuturesNewService.getDailyKLine?symbol={symbol}", HDR_SINA)
    arr = _jsonp(txt)
    return [(x["d"], float(x["o"]), float(x["h"]), float(x["l"]),
             float(x["c"]), float(x.get("v", 0) or 0), 0.0, x.get("p", "")) for x in arr[-n:]]

# ---------- 输出 ----------
def ma(bars, k):
    cl = [b[4] for b in bars]
    return sum(cl[-k:]) / k if len(cl) >= k else None

def trend(bars):
    m5, m10, m20, c = ma(bars, 5), ma(bars, 10), ma(bars, 20), bars[-1][4]
    if not (m5 and m10 and m20):
        return "数据不足"
    if c > m5 > m10 > m20:
        return "多头排列(↑)"
    if c < m5 < m10 < m20:
        return "空头排列(↓)"
    return "震荡/纠缠(→)"

def show(code, n, q):
    src = ""
    if code in INDEX:
        s, t = INDEX[code]
        try:
            name, bars, src = code, sina_stock_kline(s, n + 25), "新浪"
        except Exception:
            name, bars = ths_stock_kline(t, q, n + 25); src = "同花顺"
    elif re.fullmatch(r"\d{6}", code):
        s = ("sh" if code[0] in "69" else "sz") + code
        try:
            name, bars, src = code, sina_stock_kline(s, n + 25), "新浪"
        except Exception:
            name, bars = ths_stock_kline(code, q, n + 25); src = "同花顺"
    elif code in FUT or code.upper() in FUT.values():
        sym = FUT.get(code, code.upper())
        try:
            name, bars, src = f"{sym}", sina_futures_kline(sym, n + 25), "新浪"
        except Exception as e:
            print(f"⚠️  {code}: {e}"); return
    else:
        print(f"⚠️  无法识别: {code}")
        return
    if not bars:
        print(f"⚠️  {code}: 无K线数据"); return
    print(f"===== {name}（{code}）[{src}] 最近 {min(n, len(bars))} 根日K =====")
    if ma(bars, 20):
        print(f"MA5={ma(bars,5):.2f}  MA10={ma(bars,10):.2f}  MA20={ma(bars,20):.2f}  "
              f"收盘={bars[-1][4]}  → {trend(bars)}")
    else:
        print(f"MA5={ma(bars,5) and round(ma(bars,5),2)}  MA10={ma(bars,10) and round(ma(bars,10),2)}  "
              f"收盘={bars[-1][4]}  → {trend(bars)}")
    print(f"{'日期':<12}{'开':>10}{'高':>10}{'低':>10}{'收':>10}{'涨跌%':>8}{'量':>13}")
    prev = None
    for b in bars[-n:]:
        c = b[4]
        chg = (c - prev) / prev * 100 if prev else 0
        print(f"{b[0]:<12}{b[1]:>10.2f}{b[2]:>10.2f}{b[3]:>10.2f}{c:>10.2f}{chg:>+8.2f}{b[5]:>13.0f}")
        prev = c
    print()

def main():
    q = 1
    if "--q" in sys.argv:
        try:
            q = int(sys.argv[sys.argv.index("--q") + 1])
        except Exception:
            q = 1
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    codes, n = [], 30
    for a in args:
        if a.isdigit() and len(a) <= 3:
            n = int(a)
        else:
            codes.append(a)
    if not codes:
        print("用法: kline.py 600519 [或 上证指数 / 淀粉] [根数] [--q 0|1]"); return
    for i, c in enumerate(codes):
        if i:
            time.sleep(1.2)
        try:
            show(c, n, q)
        except Exception as e:
            print(f"⚠️  {c}: 取数失败 {e}\n")

if __name__ == "__main__":
    main()
