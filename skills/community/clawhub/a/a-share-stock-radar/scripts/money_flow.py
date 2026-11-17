#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
资金流分析（东方财富，净额口径）—— 专治「只看当日主力净额会滞后」

为什么有这个脚本：
  选股时单看「当日主力净额」是滞后指标，无法预判次日抛压。
  必须看「近3日趋势 → 是否连续流入 vs 单日脉冲」，并在次日开盘用「分时主力」复核。

用法：
  python3 money_flow.py trend   600707 [N=8] [--upto 2026-09-21]  # 近N日 + 趋势；--upto=只用到该日（回溯/复盘用）
  python3 money_flow.py intraday 600707        # 当日分时主力净额累计(万) + 近5分钟增量 + 现价
  python3 money_flow.py check    600707 [买价] # 昨日净额 + 今日分时 + 价格位置 → 留/减/走 参考

口径说明（务必与老板对齐）：
  东财/新浪只公布「净额 = 买入 − 卖出」，不单独给「总流入/总卖出」绝对值。
  主力 = 超大单 + 大单；散户 = 中单 + 小单。各净额之和 ≈ 0。
"""
import sys, json, time, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"}
EM_SNAP = ["push2.eastmoney.com", "1.push2.eastmoney.com", "push2delay.eastmoney.com"]
EM_HIS = ["push2his.eastmoney.com", "push2delay.eastmoney.com", "1.push2delay.eastmoney.com"]


def secid(code):
    code = str(code).strip()
    if "." in code:
        return code
    if code[0] in "69":
        return "1." + code
    if code[0] in "03":
        return "0." + code
    return "1." + code


def _get(url, hosts, referer="https://quote.eastmoney.com/", retries=4):
    """按 host 轮换重试（东财部分域名会空回复/限流）"""
    last = None
    for k in range(retries):
        host = hosts[k % len(hosts)]
        u = url.replace("{HOST}", host)
        try:
            req = urllib.request.Request(u, headers={**UA, "Referer": referer})
            return urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "replace")
        except Exception as e:
            last = e
            time.sleep(0.7 * (k + 1))
    raise last


def q_flow_daily(code, lmt=8):
    """近 N 日日线资金流；返回 [ {date, main, small, mid, big, huge} ] 单位:元"""
    u = ("https://{HOST}/api/qt/stock/fflow/daykline/get?lmt=%d&klt=101&secid=%s"
         "&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65"
         % (lmt, secid(code)))
    j = json.loads(_get(u, EM_HIS))
    kl = (j.get("data") or {}).get("klines") or []
    out = []
    for row in kl:
        t = row.split(",")
        out.append({"date": t[0], "main": float(t[1]), "small": float(t[2]),
                    "mid": float(t[3]), "big": float(t[4]), "huge": float(t[5])})
    return out


def q_flow_min(code):
    """当日分时资金流；返回 [ {time, main, small, mid, big, huge} ]"""
    u = ("https://{HOST}/api/qt/stock/fflow/kline/get?lmt=0&klt=1&secid=%s"
         "&fields1=f1,f2,f3,f7&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65"
         % secid(code))
    j = json.loads(_get(u, EM_SNAP))
    kl = (j.get("data") or {}).get("klines") or []
    out = []
    for row in kl:
        t = row.split(",")
        out.append({"time": t[0], "main": float(t[1]), "small": float(t[2]),
                    "mid": float(t[3]), "big": float(t[4]), "huge": float(t[5])})
    return out


def q_quote(code):
    """新浪实时快照"""
    code = str(code)
    sym = ("sh" if code[0] in "69" else "sz") + code
    req = urllib.request.Request("https://hq.sinajs.cn/list=" + sym,
                                 headers={"User-Agent": UA["User-Agent"], "Referer": "https://finance.sina.com.cn/"})
    raw = urllib.request.urlopen(req, timeout=10).read().decode("gbk", "replace")
    p = raw.split('"')[1].split(",")
    return {"name": p[0], "open": float(p[1]), "prev": float(p[2]), "price": float(p[3]),
            "high": float(p[4]), "low": float(p[5]), "vol": float(p[8]), "amount": float(p[9])}


def w(x):
    return x / 1e4  # 元 → 万元


def cmd_trend(code, n=8, upto=None):
    d = q_flow_daily(code, n + 40)
    if upto:
        d = [r for r in d if r["date"] <= upto]
    d = d[-n:]
    if not d:
        print("⚠️ 无日线资金流数据"); return
    tag = f"（≤{upto}）" if upto else ""
    print(f"===== {code} 近{len(d)}日 资金流(万元·净额){tag} =====")
    print(f"{'日期':<12}{'主力':>12}{'超大单':>12}{'大单':>12}{'中单':>12}{'小单':>12}")
    for r in d:
        print(f"{r['date']:<12}{w(r['main']):>12.0f}{w(r['huge']):>12.0f}{w(r['big']):>12.0f}"
              f"{w(r['mid']):>12.0f}{w(r['small']):>12.0f}")
    last3 = sum(r["main"] for r in d[-3:])
    pos3 = sum(1 for r in d[-3:] if r["main"] > 0)
    last = d[-1]["main"]
    # 判定
    if last3 > 0 and pos3 == 3:
        v = "🟢 连续流入(近3日全正) → 资金趋势强，可作前瞻参考"
    elif last3 > 0 and pos3 < 3:
        v = "🟡 单日脉冲为主(近3日仅部分为正) → 警惕次日获利抛压"
    elif last3 < 0 and pos3 == 0:
        v = "🔴 连续流出(近3日全负) → 资金撤离，谨慎"
    else:
        v = "⚪ 反复/无方向"
    print(f"\n近3日主力合计 {w(last3):.0f}万（{pos3}/3 日为正）；最新一日 {w(last):.0f}万")
    print("判定:", v)
    print("提示: 「当日净额」是滞后指标，只说明昨天谁在买；选股理由里须标注为『昨日(滞后)』。")


def cmd_intraday(code):
    m = q_flow_min(code)
    if not m:
        print("⚠️ 无分时资金流数据（可能非交易时段）"); return
    q = q_quote(code)
    last = m[-1]
    chg = (q["price"] - q["prev"]) / q["prev"] * 100
    print(f"===== {q['name']}({code}) 分时资金流 =====")
    print(f"现价 {q['price']} ({chg:+.2f}%)  今开 {q['open']}  高 {q['high']}  低 {q['low']}")
    print(f"最新时点 {last['time']}")
    print(f"  今日累计 主力 {w(last['main']):.0f}万 | 超大 {w(last['huge']):.0f}万 | 大 {w(last['big']):.0f}万"
          f" | 中 {w(last['mid']):.0f}万 | 小 {w(last['small']):.0f}万")
    if len(m) >= 6:
        inc = last["main"] - m[-6]["main"]
        print(f"  近5分钟 主力增量 {w(inc):.0f}万（{'流入' if inc > 0 else '流出'}）")
    print("  最近6个时点 主力累计(万): " + ", ".join(f"{r['time'][-5:]}={w(r['main']):.0f}" for r in m[-6:]))


def cmd_check(code, buy=None):
    daily = q_flow_daily(code, 6)
    q = q_quote(code)
    m = q_flow_min(code)
    print(f"===== {q['name']}({code}) 资金流复核 =====")
    if daily:
        y = daily[-1]
        print(f"昨日({y['date']}) 主力净额 {w(y['main']):.0f}万（超大 {w(y['huge']):.0f}万，大 {w(y['big']):.0f}万）"
              f" → {'昨日是净买入(滞后信号)' if y['main'] > 0 else '昨日已是净卖出'}")
    if m:
        t = m[-1]
        print(f"今日分时 主力净额 {w(t['main']):.0f}万（超大 {w(t['huge']):.0f}万）"
              f" → {'今日主力仍在流入' if t['main'] > 0 else '今日主力在流出'}")
    else:
        print("今日分时：无数据（非交易时段）")
    chg = (q["price"] - q["prev"]) / q["prev"] * 100
    print(f"价格 {q['price']} ({chg:+.2f}%)  高 {q['high']} 低 {q['low']}")
    if buy:
        buy = float(buy)
        pnl = (q["price"] - buy) / buy * 100
        print(f"成本 {buy} → 现浮动 {pnl:+.2f}%")
    # 简易结论
    verdict = []
    if daily and daily[-1]["main"] > 0 and (not m or m[-1]["main"] < 0):
        verdict.append("昨日主力进、今日主力出 → 冲高减仓迹象，偏谨慎")
    if m and m[-1]["main"] > 0:
        verdict.append("今日主力仍净流入 → 相对抗跌")
    if not verdict:
        verdict.append("信号中性，以价格防线为准")
    print("结论:", "；".join(verdict))
    print("动作建议: 反弹滞涨减半 / 跌破关键防线清仓 / 绝不补仓（具体防线以选股留档为准）")


def main():
    argv = sys.argv[1:]
    upto = None
    if "--upto" in argv:
        i = argv.index("--upto"); upto = argv[i + 1]; del argv[i:i + 2]
    if len(argv) < 2:
        print(__doc__); return
    cmd, code = argv[0], argv[1]
    if cmd == "trend":
        cmd_trend(code, int(argv[2]) if len(argv) > 2 else 8, upto)
    elif cmd == "intraday":
        cmd_intraday(code)
    elif cmd == "check":
        cmd_check(code, argv[2] if len(argv) > 2 else None)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
