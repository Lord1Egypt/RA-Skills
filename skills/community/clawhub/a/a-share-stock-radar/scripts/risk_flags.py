#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
形态风险标记（次日降级用）—— 把「昨天选进来、今天却冲高回落」的坑，前置成规则

检测（基于最近日K，东财 push2his）：
  - 炸板：当日最高触及涨停价但收盘未封（分歧加大信号）
  - 长上影：上影线占当日振幅 > 50% 且 上影/收盘 > 2%
  - 天量：当日成交量 > 前5日均量 × 2
  - 高位滞涨：收盘贴近20日最高但涨幅收窄
  - 换手过热：换手率 > 15%
  - 5日涨幅透支：近5日累计涨幅 > 25%

用法：
  python3 risk_flags.py 600707 002204 ... [--upto 2026-09-21]   # --upto=只用到该日（回溯/复盘）
"""
import sys, json, time, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"}
EM_HIS = ["push2his.eastmoney.com", "push2delay.eastmoney.com", "1.push2delay.eastmoney.com"]


def secid(code):
    code = str(code).strip()
    if "." in code:
        return code
    return ("1." if code[0] in "69" else "0.") + code


def get_kline(code, lmt=30):
    u = ("https://{HOST}/api/qt/stock/kline/get?secid=%s&klt=101&fqt=1&lmt=%d&end=20500101"
         "&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61"
         % (secid(code), lmt))
    last = None
    for k in range(4):
        host = EM_HIS[k % len(EM_HIS)]
        try:
            req = urllib.request.Request(u.replace("{HOST}", host),
                                         headers={**UA, "Referer": "https://quote.eastmoney.com/"})
            j = json.loads(urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "replace"))
            d = j.get("data") or {}
            name = d.get("name", code)
            bars = []
            for row in d.get("klines") or []:
                t = row.split(",")
                bars.append({"d": t[0], "o": float(t[1]), "c": float(t[2]), "h": float(t[3]),
                             "l": float(t[4]), "v": float(t[5]), "amp": float(t[7]),
                             "chg": float(t[8]), "turn": float(t[10]) if len(t) > 10 and t[10] else 0})
            return name, bars
        except Exception as e:
            last = e
            time.sleep(0.7 * (k + 1))
    raise last


def limit_pct(code):
    c = str(code)
    if c[:2] in ("30", "68"):   # 创业板 / 科创板
        return 0.20
    if c[0] in "84":             # 北交所
        return 0.30
    return 0.10                    # 沪深主板（ST 5% 无法从代码识别，忽略）


def analyze(code, upto=None):
    name, bars = get_kline(code, 60)
    if upto:
        bars = [b for b in bars if b["d"] <= upto]
    if len(bars) < 7:
        print(f"⚠️ {code}: 日K不足"); return
    b = bars[-1]
    prev = bars[-2]["c"]
    zt = round(prev * (1 + limit_pct(code)), 2)
    flags = []
    # 炸板
    if b["h"] >= zt - 0.001 and b["c"] < zt - 0.001:
        flags.append("💥 炸板（触涨停未封）")
    # 长上影
    up = b["h"] - max(b["o"], b["c"])
    rng = b["h"] - b["l"]
    if rng > 0 and up / rng > 0.5 and up / b["c"] > 0.02:
        flags.append(f"📌 长上影（上影占振幅{up/rng*100:.0f}%）")
    # 天量
    v5 = [x["v"] for x in bars[-6:-1]]
    if v5 and b["v"] > 2 * (sum(v5) / len(v5)):
        flags.append(f"🔊 天量（量={b['v']/1e4:.0f}万手, 前5均={sum(v5)/len(v5)/1e4:.0f}万手, {b['v']/(sum(v5)/len(v5)):.1f}倍）")
    # 高位
    h20 = max(x["h"] for x in bars[-20:])
    if b["c"] >= 0.97 * h20 and b["h"] >= h20:
        flags.append("⛰ 高位（收盘贴近20日最高）")
    # 换手
    if b["turn"] > 15:
        flags.append(f"🔥 换手过热（{b['turn']:.1f}%）")
    # 5日涨幅
    if len(bars) >= 6:
        r5 = (b["c"] - bars[-6]["c"]) / bars[-6]["c"] * 100
        if r5 > 25:
            flags.append(f"🚀 5日涨幅透支（{r5:+.1f}%）")
    chg = (b["c"] - prev) / prev * 100
    print(f"===== {name}({code}) 形态风险 =====")
    print(f"最新 {b['d']} 收 {b['c']} ({chg:+.2f}%) 高 {b['h']} 低 {b['l']} 换手 {b['turn']:.1f}%")
    print("风险标记:", "；".join(flags) if flags else "无")
    if any(k in "".join(flags) for k in ["炸板", "长上影", "天量"]):
        print("➡️ 次日建议: **降级**（不列买入，最多观察；若已持仓，冲高不追、反弹减）")
    elif flags:
        print("➡️ 次日建议: 谨慎（轻仓/等回踩确认）")
    else:
        print("➡️ 次日建议: 形态干净，可按常规处理")
    print()


def main():
    argv = sys.argv[1:]
    upto = None
    if "--upto" in argv:
        i = argv.index("--upto"); upto = argv[i + 1]; del argv[i:i + 2]
    codes = [a for a in argv if not a.startswith("-")]
    if not codes:
        print(__doc__); return
    for i, c in enumerate(codes):
        if i:
            time.sleep(0.8)
        try:
            analyze(c, upto)
        except Exception as e:
            print(f"⚠️ {c}: 失败 {e}\n")


if __name__ == "__main__":
    main()
