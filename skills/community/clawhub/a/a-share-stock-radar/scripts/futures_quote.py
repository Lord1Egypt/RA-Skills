#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
期货实时行情（多数据源：新浪 hq.sinajs.cn 实时 → 东方财富 push2delay 兜底）
用法：
  python3 futures_quote.py RB0 CU0 M0 AU0 SC0 IF0 IC0
  python3 futures_quote.py 螺纹钢 豆粕 沪铜 黄金 原油 沪深300 中证500
  python3 futures_quote.py 113.rbm 220.IFM      # 直接给东财 secid
环境变量：SOURCE=em 强制东方财富，SOURCE=sina 强制新浪（默认 sina 优先，实时）
输出：最新价/涨跌/涨跌幅/开高低/成交量/持仓量
"""
import os, sys, json, urllib.request

SINA = "https://hq.sinajs.cn/list={}"
SINA_HEADERS = {"Referer": "https://finance.sina.com.cn", "User-Agent": "Mozilla/5.0"}
EM_HOSTS = ["push2delay.eastmoney.com", "1.push2delay.eastmoney.com",
            "7.push2delay.eastmoney.com", "82.push2delay.eastmoney.com"]
EM_UT = "ut=bd1d9ddb04089700cf9c27f6f7426281"
EM_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36",
              "Referer": "https://quote.eastmoney.com/"}
EM_FIELDS = "fields=f57,f58,f43,f44,f45,f46,f47,f48,f49,f60,f169,f170"

# (中文名, 新浪代码, 东财secid)  —— 均为主力连续合约
TABLE = [
    ("螺纹钢", "RB0", "113.rbm"), ("螺纹", "RB0", "113.rbm"), ("热卷", "HC0", "113.hcm"),
    ("铁矿石", "I0", "114.im"), ("铁矿", "I0", "114.im"),
    ("沪铜", "CU0", "113.cum"), ("铜", "CU0", "113.cum"), ("沪铝", "AL0", "113.alm"),
    ("沪锌", "ZN0", "113.znm"), ("沪镍", "NI0", "113.nim"), ("沪锡", "SN0", "113.snm"),
    ("沪铅", "PB0", "113.pbm"), ("不锈钢", "SS0", "113.ssm"), ("氧化铝", "AO0", "113.aom"),
    ("黄金", "AU0", "113.aum"), ("沪金", "AU0", "113.aum"), ("白银", "AG0", "113.agm"), ("沪银", "AG0", "113.agm"),
    ("原油", "SC0", "142.scm"), ("燃油", "FU0", "113.fum"), ("沥青", "BU0", "113.bum"),
    ("橡胶", "RU0", "113.rum"), ("纸浆", "SP0", "113.spm"),
    ("豆粕", "M0", "114.mm"), ("豆油", "Y0", "114.ym"), ("棕榈油", "P0", "114.pm"),
    ("豆一", "A0", "114.am"), ("豆二", "B0", "114.bm"),
    ("玉米", "C0", "114.cm"), ("玉米淀粉", "CS0", "114.csm"), ("淀粉", "CS0", "114.csm"),
    ("鸡蛋", "JD0", "114.jdm"), ("生猪", "LH0", "114.lhm"),
    ("塑料", "L0", "114.lm"), ("聚丙烯", "PP0", "114.ppm"), ("PVC", "V0", "114.vm"),
    ("乙二醇", "EG0", "114.egm"), ("苯乙烯", "EB0", "114.ebm"), ("纯苯", "BZ0", "114.bzm"),
    ("液化气", "PG0", "114.pgm"), ("焦炭", "J0", "114.jm"), ("焦煤", "JM0", "114.jmm"),
    ("甲醇", "MA0", "115.MAM"), ("PTA", "TA0", "115.TAM"), ("纯碱", "SA0", "115.SAM"),
    ("玻璃", "FG0", "115.FGM"), ("尿素", "UR0", "115.URM"), ("白糖", "SR0", "115.SRM"),
    ("棉花", "CF0", "115.CFM"), ("菜油", "OI0", "115.OIM"), ("菜粕", "RM0", "115.RMM"),
    ("动力煤", "ZC0", "115.ZCM"), ("对二甲苯", "PX0", "115.PXM"),
    ("沪深300", "IF0", "220.IFM"), ("沪深300股指", "IF0", "220.IFM"),
    ("上证50", "IH0", "220.IHM"), ("中证500", "IC0", "220.ICM"), ("中证1000", "IM0", "220.IMM"),
    ("国债", "T0", "220.TM"), ("十债", "T0", "220.TM"), ("五年债", "TF0", "220.TFM"),
    ("二年债", "TS0", "220.TSM"), ("三十债", "TL0", "220.TLM"),
]
NAME2 = {n: (s, e) for n, s, e in TABLE}
SINA2EM = {s: e for n, s, e in TABLE}

def resolve(tok):
    """返回 (显示名, 新浪代码或None, 东财secid或None)"""
    t = tok.strip()
    if t in NAME2:
        s, e = NAME2[t]
        return t, s, e
    if "." in t:               # 直接给了东财 secid
        return t, None, t
    up = t.upper()
    return up, up, SINA2EM.get(up)

def sina_fetch(sina_codes):
    if not sina_codes:
        return {}
    q = ",".join("nf_" + c for c in sina_codes)
    raw = urllib.request.urlopen(urllib.request.Request(SINA.format(q), headers=SINA_HEADERS),
                                 timeout=12).read().decode("gbk", "replace")
    out = {}
    for line in raw.strip().split("\n"):
        if "=" not in line:
            continue
        key = line.split("=")[0].replace("var hq_str_nf_", "").strip()
        val = line.split("=", 1)[1].strip().strip('";')
        out[key] = val.split(",") if val else []
    return out

def sina_parse(code, f):
    g = lambda i: (f[i] if i < len(f) else "")
    if code.startswith(("IF", "IH", "IC", "IM", "T", "TF", "TS", "TL")):
        name = g(49) or code
        o, h, l, last = g(0), g(1), g(2), g(3)
        vol, oi, prev = g(4), g(6), g(48)
    else:
        name = g(0) or code
        o, h, l, last = g(2), g(3), g(4), g(8)
        vol, oi, prev = g(14), g(13), g(27)
    try:
        last_f, prev_f = float(last), float(prev)
        chg = last_f - prev_f
        pct = chg / prev_f * 100 if prev_f else 0.0
    except Exception:
        last_f = prev_f = chg = pct = 0.0
    return dict(name=name, src="新浪", last=last_f, chg=chg, pct=pct,
                open=o, high=h, low=l, prev=prev_f, vol=vol, oi=oi)

def _num(x):
    try:
        return float(x)
    except Exception:
        return 0.0

def em_get(secid):
    for k in range(4):
        host = EM_HOSTS[k % len(EM_HOSTS)]
        url = f"https://{host}/api/qt/stock/get?{EM_UT}&invt=2&fltt=2&{EM_FIELDS}&secid={secid}"
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers=EM_HEADERS), timeout=10).read().decode("utf-8", "replace")
            d = json.loads(raw).get("data")
            if not d:
                continue
            last = _num(d.get("f43")); prev = _num(d.get("f60"))
            chg = _num(d.get("f169")); pct = _num(d.get("f170"))
            if not chg and prev:
                chg = last - prev
            return dict(name=d.get("f58") or secid, src="东财", last=last, chg=chg, pct=pct,
                        open=d.get("f46"), high=d.get("f44"), low=d.get("f45"),
                        prev=prev, vol=d.get("f47"), oi=d.get("f49"))
        except Exception:
            continue
    return None

def fmt(v):
    try:
        return f"{float(v):.2f}"
    except Exception:
        return str(v)

def main():
    args = sys.argv[1:] or ["RB0", "CU0", "M0", "AU0", "SC0", "IF0", "IC0"]
    prefer = os.environ.get("SOURCE", "sina").lower()
    items = [resolve(a) for a in args]
    sina_codes = [s for _, s, _ in items if s]
    sdata = {}
    if prefer != "em" and sina_codes:
        try:
            sdata = sina_fetch(sina_codes)
        except Exception:
            sdata = {}
    for label, scode, emid in items:
        r = None
        if prefer == "em":
            if emid:
                r = em_get(emid)
            if r is None and scode and not sdata:
                try:
                    sdata = sina_fetch([scode])
                except Exception:
                    sdata = {}
            if r is None and scode and sdata.get(scode):
                r = sina_parse(scode, sdata[scode])
        else:
            if scode and sdata.get(scode):
                r = sina_parse(scode, sdata[scode])
            if r is None and emid:
                r = em_get(emid)
        if not r:
            print(f"⚠️  {label}: 无数据（代码可能不对）\n")
            continue
        arrow = "🔴" if r["pct"] < 0 else ("🟢" if r["pct"] > 0 else "⚪")
        print(f"{arrow} {r['name']}（{label}）  [{r['src']}]")
        print(f"   最新 {fmt(r['last'])}  涨跌 {fmt(r['chg'])}  ({r['pct']:+.2f}%)  昨结 {fmt(r['prev'])}")
        print(f"   开 {r['open']}  高 {r['high']}  低 {r['low']}  持仓 {r['oi']}  成交 {r['vol']}")
        print()

if __name__ == "__main__":
    main()
