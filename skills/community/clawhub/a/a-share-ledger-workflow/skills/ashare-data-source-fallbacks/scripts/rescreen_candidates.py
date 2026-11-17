#!/usr/bin/env python3
"""按现行 B3 双口径 + A1 批量复筛 A 股候选标的。

用法：
    python3 rescreen_candidates.py 600000 600001 600002
    python3 rescreen_candidates.py --file codes.txt          # 每行一个代码，# 开头为注释
    python3 rescreen_candidates.py --json-out out.json 600000

输出：每只标的 PB 全样本分位 / PE 近 3 年分位 / PE 全史分位 / 扣非占归母 / A1 / B3，
末尾列出硬门槛双通过者。

口径（与 ashare-step-5 门槛合同一致）：
    A1 = 扣非>0 且 扣非同比>0 且 经营现金流>0 且 现金流同比>0
    B3 = PB 分位<75%  或  (PE 近 3 年分位<=50% 且 扣非占归母>=90%)

🔴 现金流同比必须由 NETCASH_OPERATE_PK 同期金额自行计算 —— 响应里的 MGJYXJJETZ
   名字像「经营现金流同比」但不是，用它会成批误判 A1。
"""

import json
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta

UA = {"User-Agent": "Mozilla/5.0", "Referer": "https://data.eastmoney.com/"}
VAL_URL = ("https://datacenter-web.eastmoney.com/api/data/v1/get?"
           "reportName=RPT_VALUEANALYSIS_DET&columns=ALL&filter={f}"
           "&pageSize=500&pageNumber={p}&sortColumns=TRADE_DATE&sortTypes=1")
FIN_URL = ("https://datacenter-web.eastmoney.com/api/data/v1/get?"
           "reportName=RPT_F10_FINANCE_MAINFINADATA&columns=ALL&filter={f}"
           "&pageSize=20&sortColumns=REPORT_DATE&sortTypes=-1")

# 现行报告期（财报季更新时必须同步改这两行）
CUR_PERIOD = "2026-06-30"
PREV_PERIOD = "2025-06-30"
PE_WINDOW_DAYS = 1095  # 近 3 年
PB_MAX = 75.0          # B3 PB 分支阈值
PE_MAX = 50.0          # B3 PE 分支阈值
KC_RATIO_MIN = 90.0    # B3 PE 分支的扣非占归母下限


def secucode(code):
    """F10 系接口要带市场后缀；估值系接口要纯代码（传错会静默返空）。"""
    if code.startswith("6"):
        return code + ".SH"
    if code.startswith(("0", "3")):
        return code + ".SZ"
    if code.startswith(("4", "8", "9")):
        return code + ".BJ"
    return code + ".SZ"


def _get(url):
    req = urllib.request.Request(url, headers=UA)
    return json.loads(urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "ignore"))


def valuation(code, max_pages=30):
    """日度 PE_TTM / PB_MRQ 全序列（数据起点约 2018-01-02）。"""
    rows = []
    for p in range(1, max_pages + 1):
        try:
            j = _get(VAL_URL.format(f=urllib.parse.quote(f'(SECURITY_CODE="{code}")'), p=p))
        except Exception:
            break
        d = (j.get("result") or {}).get("data") or []
        if not d:
            break
        rows += d
        if len(d) < 500:
            break
        time.sleep(0.15)
    return rows


def financials(code):
    """返回 (本期, 去年同期) 两条记录；缺失为 None。"""
    try:
        j = _get(FIN_URL.format(f=urllib.parse.quote(f'(SECUCODE="{secucode(code)}")')))
    except Exception:
        return None, None
    cur = prv = None
    for r in (j.get("result") or {}).get("data") or []:
        rd = (r.get("REPORT_DATE") or "")[:10]
        if rd == CUR_PERIOD:
            cur = r
        elif rd == PREV_PERIOD:
            prv = r
    return cur, prv


def pctl(vals, cur):
    """cur 在 vals 中的分位（%）：小于等于 cur 的占比。负值/空值剔除。"""
    v = [x for x in vals if x is not None and x > 0]
    if not v or cur is None or cur <= 0:
        return None
    return round(sum(1 for x in v if x <= cur) / len(v) * 100, 1)


def screen(code):
    r = valuation(code)
    cur, prv = financials(code)
    s = {"code": code, "pb_pctl": None, "pe3_pctl": None, "pe_all_pctl": None,
         "kc": None, "kc_yoy": None, "cf": None, "cf_yoy": None,
         "kc_ratio": None, "a1": False, "b3": False, "b3_via": None, "note": None}

    if len(r) < 200:
        s["note"] = f"估值样本不足（{len(r)} 条）"
        return s

    pb = [x.get("PB_MRQ") for x in r]
    pe = [x.get("PE_TTM") for x in r]
    last = datetime.strptime(r[-1]["TRADE_DATE"][:10], "%Y-%m-%d")
    cut = last - timedelta(days=PE_WINDOW_DAYS)
    idx = [i for i, x in enumerate(r)
           if datetime.strptime(x["TRADE_DATE"][:10], "%Y-%m-%d") >= cut]
    s.update(asof=r[-1]["TRADE_DATE"][:10], pe3_n=len(idx),
             pb_pctl=pctl(pb, r[-1].get("PB_MRQ")),
             pe3_pctl=pctl([pe[i] for i in idx], r[-1].get("PE_TTM")),
             pe_all_pctl=pctl(pe, r[-1].get("PE_TTM")))

    if not cur:
        s["note"] = f"无 {CUR_PERIOD} 财报记录"
        return s

    kc = cur.get("KCFJCXSYJLR")
    kc_yoy = cur.get("KCFJCXSYJLRTZ")
    cf = cur.get("NETCASH_OPERATE_PK")
    par = cur.get("PARENTNETPROFIT")
    cfp = prv.get("NETCASH_OPERATE_PK") if prv else None
    cf_yoy = ((cf - cfp) / abs(cfp) * 100) if (cf is not None and cfp not in (None, 0)) else None
    ratio = (kc / par * 100) if (kc and par and par > 0) else None
    s.update(kc=kc, kc_yoy=kc_yoy, cf=cf, cf_yoy=cf_yoy, kc_ratio=ratio)

    # A1：扣非为负不等于「同比转正」——四项都必须 >0
    s["a1"] = all(v is not None and v > 0 for v in (kc, kc_yoy, cf, cf_yoy))

    b3_pb = s["pb_pctl"] is not None and s["pb_pctl"] < PB_MAX
    b3_pe = (s["pe3_pctl"] is not None and s["pe3_pctl"] <= PE_MAX
             and ratio is not None and ratio >= KC_RATIO_MIN)
    s["b3"] = b3_pb or b3_pe
    s["b3_via"] = "+".join(n for n, ok in (("PB", b3_pb), ("PE", b3_pe)) if ok) or None
    return s


def main(argv):
    codes, json_out = [], None
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--json-out" and i + 1 < len(argv):
            i += 1
            json_out = argv[i]
        elif a == "--file" and i + 1 < len(argv):
            i += 1
            with open(argv[i], encoding="utf-8") as fh:
                codes += [l.strip() for l in fh if l.strip() and not l.startswith("#")]
        elif a.isdigit() and len(a) == 6:
            codes.append(a)
        i += 1

    if not codes:
        print(__doc__)
        return 1

    res = []
    print(f"报告期基准 {CUR_PERIOD}（同比对 {PREV_PERIOD}）")
    print(f"{'代码':<8}{'PB全样本':>10}{'PE近3年':>9}{'PE全史':>8}{'扣非/归母':>10}{'A1':>4}{'B3':>4}  备注")
    print("-" * 78)
    for c in codes:
        s = screen(c)
        res.append(s)

        def fmt(k):
            return f"{s[k]}%" if s.get(k) is not None else "—"

        note = s.get("b3_via") or ""
        if s.get("note"):
            note += " " + s["note"]
        print(f"{s['code']:<8}{fmt('pb_pctl'):>10}{fmt('pe3_pctl'):>9}{fmt('pe_all_pctl'):>8}"
              f"{fmt('kc_ratio'):>10}{'✅' if s['a1'] else '❌':>4}{'✅' if s['b3'] else '❌':>4}  {note}")

    both = [s for s in res if s["a1"] and s["b3"]]
    print(f"\n硬门槛双通过（A1 ✅ 且 B3 ✅）：{len(both)} 只")
    for s in both:
        print(f"  {s['code']}  B3路径={s['b3_via']}  PB={s['pb_pctl']}%  "
              f"PE近3年={s['pe3_pctl']}%  扣非/归母={s['kc_ratio']}%")
    print("\n⚠️ 双通过≠可买入：仍需 A2（无失效证据）与业务逻辑确认；"
          "低 PB 若源于净资产被减值，不是便宜。")

    if json_out:
        with open(json_out, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=1)
        print(f"→ {json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
