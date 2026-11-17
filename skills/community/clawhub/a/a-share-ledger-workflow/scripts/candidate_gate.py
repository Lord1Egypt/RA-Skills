#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
candidate_gate.py — 候选池门槛复查（A1/A2 必过 + B1-B5 任一触发）

判定规则（本工作流 确认，不得偏离）
────────────────────────────────────────────────
必过（排除项，达不到坚决不推荐）：
 A1  扣非净利同比 > 0  且  经营现金流 > 0  且  现金流同比 > 0
 A2  无 B 层失效证据（价格波动/跌破均线不算失效）

B1-B5 任一满足即提醒（由用户决定是否进第6步）：
  B1  距60日最高价回撤 ≥ 25%
  B2  已跌破 MA60
  B3  PB分位<75%（剔上市首年）｜或 PE分位(近3年)≤50% 且 扣非占归母≥90%
  B4  相对方向中位差值 ≥ 0（不再跑输）
  B5  站上 MA20 且 MACD 金叉
B1 与 B2 是「或」关系，不是同时满足。

用法：
  python3 candidate_gate.py                    # 全部候选
  python3 candidate_gate.py --codes 600000,600001
  python3 candidate_gate.py --json-out /tmp/gate.json
输出：人类可读表格 + JSON（供 cron prompt 读取）
"""
import pathlib
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
# ── 数据根目录（环境变量；未设置即报错，不回落任何具体路径）──────────────
_D = os.environ.get("STOCK_DATA_DIR", "").rstrip("/")
if not _D:
    raise SystemExit(
        "🔴 未设置环境变量 STOCK_DATA_DIR（你的股票数据根目录）。\n"
        '   例：export STOCK_DATA_DIR="$HOME/stock_data"\n'
        "   目录结构见 README「数据目录约定」。"
    )



LEDGER = _D + "/股票台账/候选"
UA = {"User-Agent": "Mozilla/5.0"}

# ── 门槛常量（默认值；可在 bench.json 的 constants 块按需覆盖）──────────
RETRACE_MIN = 0.25      # B1 回撤 ≥25%
PB_PCTL_MAX = 75.0      # B3 PB分位 <75%
PE_PCTL_3Y_MAX = 50.0   # B3 替代口径：PE分位(近3年) ≤50%
KF_RATIO_MIN = 90.0     #   且 扣非占归母 ≥90%（防 PE 低来自一次性收益）
ATR_PERIOD = 20
ATR_MULT = 2.0

# ── 门槛数据：**不在本文件里** ─────────────────────────────────────────
#   🔴 各标的的 BENCH(方向内相对中位) / PB分位 / PE分位 / 扣非占比 /
#      A1 基线 / A1 备注 / A2 硬信号，都是**使用者的私有研究数据**，
#      不进代码、不进仓库。统一放 $STOCK_DATA_DIR/bench.json。
#   首次使用：cp templates/bench.example.json $STOCK_DATA_DIR/bench.json
#             再按你自己的标的逐条填写（字段说明见该文件与 README）。
#   为什么要外抽：硬编码在本文件里时——① 换人使用必须改代码，等于没法分享；
#      ② 数据与代码混在一起，改个数值要动代码、review 看不出改了什么。
BENCH_FILE = _D + "/bench.json"


def load_bench(path=None):
    """读 bench.json → 各字典。缺文件 / 字段缺失 / 空字典 → 明确报错。

    🔴 三种失败都**不静默**：静默退化会让所有台账报 NEED_DATA，
       表面上「没风险提醒」，实际是监控失效。
    """
    path = path or BENCH_FILE
    f = pathlib.Path(path)
    if not f.is_file():
        sys.exit(f"🔴 缺少门槛数据文件：{path}\n"
                 f"   本脚本**不含内置标的明细**（那是使用者的私有研究数据）。\n"
                 f"   做法：cp <仓库>/templates/bench.example.json {path}，"
                 f"再按你的标的填写。\n"
                 f"   字段说明见 templates/bench.example.json 顶部注释与 README。")
    data = json.loads(f.read_text(encoding="utf-8"))
    stock = data.get("stock") or {}
    if not stock:
        sys.exit(f"🔴 bench.json 的 stock 为空：{path}\n"
                 f"   至少填 1 只标的，否则所有台账都会报 NEED_DATA（等于监控失效）。")

    c = data.get("constants") or {}
    g = globals()
    for key, var in (("retrace_min", "RETRACE_MIN"), ("pb_pctl_max", "PB_PCTL_MAX"),
                     ("pe_pctl_3y_max", "PE_PCTL_3Y_MAX"), ("kf_ratio_min", "KF_RATIO_MIN"),
                     ("atr_period", "ATR_PERIOD"), ("atr_mult", "ATR_MULT")):
        if c.get(key) is not None:
            g[var] = c[key]
    if c.get("a1_base_date") is not None:
        g["A1_BASE_DATE"] = c["a1_base_date"]

    need = ("direction", "bench_pt", "pb_pctl", "pe_pctl_3y", "kf_ratio", "a1", "a1_note")
    miss = [(code, k) for code, v in stock.items() for k in need if k not in v]
    if miss:
        sys.exit("🔴 bench.json 字段缺失（代码.字段）："
                 + ", ".join(f"{c_}.{k}" for c_, k in miss)
                 + f"\n   必填字段：{', '.join(need)}")

    return {
        "BENCH":      {c_: (v["direction"], v["bench_pt"]) for c_, v in stock.items()},
        "PB_PCTL":    {c_: v["pb_pctl"] for c_, v in stock.items()},
        "PE_PCTL_3Y": {c_: v["pe_pctl_3y"] for c_, v in stock.items()},
        "KF_RATIO":   {c_: v["kf_ratio"] for c_, v in stock.items()},
        "A1_BASE":    {c_: tuple(v["a1"]) for c_, v in stock.items()},
        "A1_NOTE":    {c_: v["a1_note"] for c_, v in stock.items()},
        # A2：B层失效硬信号。历史实现一律 None（未见硬失效），bench.json 可逐股写
        "A2_HARD":    {c_: v.get("a2_hard") for c_, v in stock.items()},
    }


_B = load_bench()
BENCH = _B["BENCH"]
PB_PCTL = _B["PB_PCTL"]
PE_PCTL_3Y = _B["PE_PCTL_3Y"]
KF_RATIO = _B["KF_RATIO"]
A1_BASE = _B["A1_BASE"]
A1_NOTE = _B["A1_NOTE"]
A2_HARD = _B["A2_HARD"]

# ── 数据完整性：建台账即纳入，bench.json 缺字段报 NEED_DATA ──
# 用途：新标的只建台账、忘补 bench.json 数据时，必须**报出来**，不能静默跳过。
# （DICTS 是下面内存字典名；数据源头是 bench.json，见 load_bench。）
DICTS = ("BENCH", "PB_PCTL", "PE_PCTL_3Y", "KF_RATIO", "A1_BASE", "A1_NOTE")


def missing_dicts(code):
    """返回该标的缺失的字典名列表（空 = 齐全）。"""
    tbl = {"BENCH": BENCH, "PB_PCTL": PB_PCTL, "PE_PCTL_3Y": PE_PCTL_3Y,
           "KF_RATIO": KF_RATIO, "A1_BASE": A1_BASE, "A1_NOTE": A1_NOTE}
    return [n for n in DICTS if code not in tbl[n]]

# ── 公告检测：抓自基准日以来的财报类公告 ──────────
# 基准日 = 当前 A1 基线/估值分位的数据日（bench.json → constants.a1_base_date，
# 如 "2026-09-30"）；晚于它的财报公告说明基线已过期。
# 未配置时为 None → 公告检测整段跳过（不误报"无新财报"）。
A1_BASE_DATE = None
REPORT_KEYS = ("季度报告", "三季度", "三季报", "半年度报告", "半年报",
               "年度报告", "年报", "业绩快报", "业绩预告", "主要经营数据")
ANN_API = ("https://np-anotice-stock.eastmoney.com/api/security/ann"
           "?page_size=50&page_index={pg}&ann_type=A&client_source=web&stock_list={code}")


def _get(url, timeout=25):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=timeout).read()


# 🔴 取数失败原因留存（原来 except 里 pass，错误信息全丢）
KLINE_ERR = {}     # code → K线取数失败原因
ANN_ERR = {}       # code → 公告取数失败原因


def fetch_kline(code, n=120, tries=3):
    """腾讯前复权日K，必须带市场前缀。返回 list 或 None。

    🔴 None = 取数失败（下游报 DATA_FAIL）。绝不与「K线不足」混为一谈：
    前者是接口问题，后者是新股问题，处置动作完全不同。
    """
    pre = "sh" if code[0] in "69" else "sz"
    p = pre + code
    url = (f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get"
           f"?param={p},day,,,{n},qfq")
    last = ""
    for i in range(tries):
        try:
            k = json.loads(_get(url).decode("utf-8", errors="ignore"))
            d = k["data"][p]
            kl = d.get("qfqday") or d.get("day") or []
            if kl:
                return kl
            last = "接口可达但 K线列表为空"
        except Exception as exc:
            last = f"{type(exc).__name__}: {exc}"
        time.sleep(1.0 * (i + 1))
    KLINE_ERR[code] = last
    return None


def fetch_reports(code, tries=2):
    """查公告，返回 (财报类公告list, ok)。ok=False 表示取数失败，须与'无公告'区分。"""
    arts, ok = [], False
    for pg in (1, 2):
        d = None
        err = ""
        for _ in range(tries):
            try:
                raw = _get(ANN_API.format(pg=pg, code=code))
                d = json.loads(raw.decode("utf-8"))
                ok = True
                break
            except Exception as exc:
                # 🔴 原来 except: pass —— 报错原因全丢，
                # 用户只看到「取数失败」，无法判断是网络问题还是接口改版
                err = f"{type(exc).__name__}: {exc}"
                time.sleep(0.5)
        if d is None:
            ANN_ERR[code] = err
            return arts, False if pg == 1 else ok
        lst = (d.get("data") or {}).get("list") or []
        if not lst:
            break
        arts += lst
    return arts, ok


def check_new_reports(code, since=None):
    """返回自 since 以来的财报类公告（最多3条，新的在前）。
    用途：A1 基线过期提醒——不改变门槛判定，只提示'取证基线需更新'。
    ⚠️ since 默认在**运行时**解析全局 A1_BASE_DATE，不要写成默认参数（定义时绑定，改全局不生效）。"""
    if since is None:
        since = A1_BASE_DATE
    arts, ok = fetch_reports(code)
    if not ok:
        return None, False            # None = 取数失败；[] = 确实没有
    out = []
    for a in arts:
        title = a.get("title") or ""
        nd = (a.get("notice_date") or "")[:10]
        if nd > since and any(k in title for k in REPORT_KEYS):
            out.append({"title": title, "date": nd,
                        "pdf_url": f"https://pdf.dfcfw.com/pdf/H2_{a.get('art_code')}_1.pdf"})
    out.sort(key=lambda x: x["date"], reverse=True)
    return out[:3], True


def ema(vals, n):
    k = 2.0 / (n + 1)
    e = vals[0]
    for x in vals[1:]:
        e = x * k + e * (1 - k)
    return e


def indicators(cl):
    """返回 MA20/MA60/回撤/RSI/MACD 状态。"""
    out = {}
    if len(cl) < 60:
        return None
    out["ma20"] = sum(cl[-20:]) / 20
    out["ma60"] = sum(cl[-60:]) / 60
    hi60 = max(cl[-60:])
    out["high60"] = hi60
    out["retrace"] = (cl[-1] / hi60 - 1) * 100      # 负数=回撤
    # RSI14 Wilder
    g = l = 0.0
    for i in range(-14, 0):
        ch = cl[i] - cl[i - 1]
        g += max(ch, 0.0)
        l += max(-ch, 0.0)
    out["rsi14"] = 100 - 100 / (1 + (g / 14) / ((l / 14) or 1e-9))
    # MACD
    dif = [ema(cl[:i + 1], 12) - ema(cl[:i + 1], 26) for i in range(25, len(cl))]
    dea = ema(dif, 9)
    out["dif"], out["dea"], out["macd_bar"] = dif[-1], dea, dif[-1] - dea
    out["above_ma20"] = cl[-1] > out["ma20"]
    out["above_ma60"] = cl[-1] > out["ma60"]
    out["macd_golden"] = out["macd_bar"] > 0
    return out


def evaluate(code, name, direction):
    rec = {"code": code, "name": name, "direction": direction}

    # ── 字典完整性（缺字典 → NEED_DATA 并列出，不静默跳过）────────
    miss = missing_dicts(code)
    rec["missing_dicts"] = miss

    # ── 公告检测：A1 基线是否已过期（与K线无关，最先执行）──────────
    if A1_BASE_DATE is None:
        # 未配置 a1_base_date → 无基准可比，不检测也不报"无新财报"
        rec["new_reports"] = []
        rec["report_fetch_ok"] = None
        rec["report_stale"] = False
    else:
        reps, rep_ok = check_new_reports(code)
        rec["new_reports"] = reps            # [] = 无新财报；None = 取数失败
        rec["report_fetch_ok"] = rep_ok
        rec["report_stale"] = bool(reps)     # True = 有晚于基准日的财报 → 基线需更新

    kl = fetch_kline(code)
    if not kl:
        rec["error"] = "kline_unavailable"
        rec["action"] = "DATA_FAIL"
        rec["gate_pass"] = False
        # 🔴 带上真实原因，否则用户只能看到「K线不可用」，无从排查
        rec["reason"] = ("K线不可用，无法计算技术面指标"
                         + (f"｜原因：{KLINE_ERR.get(code)}" if KLINE_ERR.get(code) else ""))
        return rec
    cl = [float(x[2]) for x in kl]
    ind = indicators(cl)
    if not ind:
        rec["error"] = "insufficient_klines"
        rec["action"] = "DATA_FAIL"
        rec["gate_pass"] = False
        rec["reason"] = (f"K线仅{len(kl)}根（需≥{60}），新股上市不足，"
                         f"MA60/回撤/MACD 暂无法判定 → 待累计满60个交易日")
        return rec

    rec.update({
        "close": round(cl[-1], 3),
        "kline_last_date": kl[-1][0],
        "ma20": round(ind["ma20"], 3),
        "ma60": round(ind["ma60"], 3),
        "retrace_pct": round(ind["retrace"], 2),
        "rsi14": round(ind["rsi14"], 1),
        "macd_golden": ind["macd_golden"],
        "above_ma20": ind["above_ma20"],
        "below_ma60": not ind["above_ma60"],
    })

# ── A1：扣非>0 且 现金流>0 且 现金流同比>0 ──────────────────────
    kf, cf, cf_yoy = A1_BASE.get(code, (None, None, None))
    rec["a1_kf_yoy"] = kf
    rec["a1_cashflow"] = cf
    rec["a1_cashflow_yoy"] = cf_yoy
    rec["a1_note"] = A1_NOTE.get(code, "")
    if kf is None or cf is None:
        rec["A1"] = None        # 数据缺失，不能判过
        rec["A1_reason"] = "扣非同比或现金流数值缺失，需补最新财报"
    else:
        # kf == "TURNAROUND"：上年为负、本年转正，同比百分比无意义，按扭亏处理
        if kf == "TURNAROUND":
            kf_ok = True
            kf_txt = "扣非扭亏✅"
        else:
            kf_ok = kf > 0
            kf_txt = f"扣非同比{kf:+.2f}%{'✅' if kf_ok else '❌'}"
        cf_ok = (cf > 0) and (cf_yoy is None or cf_yoy > 0)
        rec["A1"] = bool(kf_ok and cf_ok)
        rec["A1_reason"] = (kf_txt + "；"
                           f"现金流{cf:.2f}亿"
                           f"{f'({cf_yoy:+.2f}%)' if cf_yoy is not None else ''}"
                           f"{'✅' if cf_ok else '❌'}")

    # ── A2：无 B 层失效证据 ─────────────────────────────────────
    hard = A2_HARD.get(code)
    rec["A2"] = True if hard is None else False
    rec["A2_reason"] = ("未见公司端硬失效证据" if hard is None
                        else f"命中失效证据：{hard}")

    # ── B1-B5 任一命中 ──────────────────────────────────────────
    pb = PB_PCTL.get(code)
    b1v = BENCH.get(code, (None, None))[1]
    trig = {}
    trig["B1"] = bool(ind["retrace"] <= -RETRACE_MIN * 100)   # 回撤≥25%
    trig["B2"] = (not ind["above_ma60"])                    # 跌破MA60
    # B3 双口径：PB分位<75%  ｜  或 PE分位(近3年)≤50% 且 扣非占归母≥90%
    pb_ok = (pb is not None and pb < PB_PCTL_MAX)
    pe3 = PE_PCTL_3Y.get(code)
    kfr = KF_RATIO.get(code)
    pe_ok = (pe3 is not None and pe3 <= PE_PCTL_3Y_MAX
             and kfr is not None and kfr >= KF_RATIO_MIN)
    trig["B3"] = bool(pb_ok or pe_ok)
    b3_via = "PB+PE" if (pb_ok and pe_ok) else ("PB" if pb_ok else ("PE" if pe_ok else None))
    trig["B4"] = (b1v is not None and b1v >= 0)              # 不再跑输方向中位
    trig["B5"] = bool(ind["above_ma20"] and ind["macd_golden"])  # MA20+MACD金叉
    rec["triggers"] = trig
    rec["trigger_hits"] = [f"B3({b3_via})" if (k == "B3" and b3_via) else k
                           for k, v in trig.items() if v]
    rec["pb_pctl"] = pb
    rec["pe_pctl_3y"] = pe3
    rec["kf_ratio"] = kfr
    rec["b3_via"] = b3_via
    rec["b4_rel_pt"] = b1v

    # ── 合并判定 ────────────────────────────────────────────────
    if rec.get("missing_dicts"):
        rec["gate_pass"] = None
        rec["action"] = "NEED_DATA"
        rec["reason"] = (f"⚠️ 缺字典数据：{'、'.join(rec['missing_dicts'])}"
                         f" → 新标的已自动纳入，但需补齐字典才能算出真实门槛")
    elif rec["A1"] is None or rec["A2"] is None:
        rec["gate_pass"] = None
        rec["action"] = "NEED_DATA"
        rec["reason"] = "A1/A2 数据缺失，需补最新财报后判定"
    elif rec["A1"] and rec["A2"] and rec["trigger_hits"]:
        rec["gate_pass"] = True
        rec["action"] = "ALERT"
        rec["reason"] = (f"A1✅ A2✅ ＋ 触发 {len(rec['trigger_hits'])} 项："
                         + "、".join(rec["trigger_hits"])
                         + (f"｜{rec['a1_note']}" if rec.get("a1_note") else ""))
    elif rec["A1"] and rec["A2"]:
        rec["gate_pass"] = False
        rec["action"] = "SILENT"
        rec["reason"] = "A1✅ A2✅ 但 B1-B5 均未满足 → 按规则静默"
    else:
        rec["gate_pass"] = False
        rec["action"] = "EXCLUDE"
        why = []
        if rec["A1"] is False:
            why.append("A1未过")
        if rec["A2"] is False:
            why.append("A2未过")
        rec["reason"] = "、".join(why) + " → 排除项未达，坚决不推荐"
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--codes", default=None)
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    targets = []
    if args.codes:
        for c in args.codes.split(","):
            c = c.strip()
            targets.append((c, BENCH.get(c, ("?", None))[0]))
    else:
        # ⭐ 扫描台账目录决定标的：**建台账即纳入**（不再要求已在字典里）
        #    缺字典数据 → evaluate() 返回 NEED_DATA 并在 reason 里列出缺哪些
        for fn in sorted(os.listdir(LEDGER)):
            if not fn.endswith("_跟踪台账.md"):
                continue
            code = fn.split("_")[1]
            nm = fn.split("_")[0]
            targets.append((code, BENCH.get(code, ("?", None))[0]))

    results = []
    for i, (code, direction) in enumerate(targets):
        r = evaluate(code, "", direction)
        # 补名称
        for fn in os.listdir(LEDGER):
            if fn.endswith("_跟踪台账.md") and fn.split("_")[1] == code:
                r["name"] = fn.split("_")[0]
                break
        results.append(r)
        if i < len(targets) - 1:
            time.sleep(0.4)

    out = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "rule": "A1+A2必过；B1-B5任一满足即提醒（B3=PB<75% 或 PE近3年≤50%且扣非占归母≥90%）",
        "retrace_min_pct": RETRACE_MIN * 100,
        "pb_pctl_max": PB_PCTL_MAX,
        "pe_pctl_3y_max": PE_PCTL_3Y_MAX,
        "kf_ratio_min": KF_RATIO_MIN,
        "total": len(results),
        "alert": [r for r in results if r["action"] == "ALERT"],
        "report_alerts": [{"code": r["code"], "name": r.get("name", ""),
                           "reports": r.get("new_reports") or []}
                          for r in results if r.get("report_stale")],
        "report_fetch_failed": [r["code"] for r in results
                                if r.get("report_fetch_ok") is False],
        "a1_base_date": A1_BASE_DATE,
        "results": results,
    }

    if not args.quiet:
        W = 112
        print("=" * W)
        print("候选门槛复查｜规则：A1+A2 必过 ＋ (B1..B5) 任一")
        print("=" * W)
        hdr = (f"{'标的':<12}{'代码':<9}{'方向':<9}{'回撤%':>8}{'MA60':>9}"
               f"{'PB分位':>8}{'PE3y':>7}{'A1':>4}{'A2':>4}  触发项")
        print(hdr)
        print("-" * W)
        for r in results:
            a1 = {True: "✅", False: "❌", None: "—"}[r.get("A1")]
            a2 = {True: "✅", False: "❌", None: "—"}[r.get("A2")]
            tr = "、".join(r.get("trigger_hits", [])) or "—"
            ret = f"{r['retrace_pct']:+.1f}" if "retrace_pct" in r else "—"
            ma60 = f"{r['ma60']:.2f}" if "ma60" in r else "—"
            pb = f"{r['pb_pctl']:.1f}" if r.get("pb_pctl") is not None else "—"
            pe3s = f"{r['pe_pctl_3y']:.1f}" if r.get("pe_pctl_3y") is not None else "—"
            rep = "📄" if r.get("report_stale") else ""
            print(f"{r.get('name','?')[:10]:<12}{r['code']:<9}{r['direction']:<9}"
                  f"{ret:>8}{ma60:>9}{pb:>8}{pe3s:>7}{a1:>4}{a2:>4}  {tr}{rep}")
        print("-" * W)
        for r in results:
            mark = {"ALERT": "🔔", "SILENT": "🔴", "EXCLUDE": "⛔",
                    "NEED_DATA": "⚠️", "DATA_FAIL": "🔴"}[r["action"]]
            print(f"{mark} {r['name'][:10]:<12}{r.get('reason') or r.get('error') or '未知'}")
        ra = out["report_alerts"]
        if ra:
            print("-" * W)
            print(f"📄 有新财报（晚于基准日 {A1_BASE_DATE}）→ **A1 基线/估值分位需更新**：")
            for x in ra:
                for rp in x["reports"]:
                    print(f"   · {x['name']} {x['code']}｜{rp['date']}｜{rp['title'][:60]}")
                    print(f"     PDF: {rp['pdf_url']}")
        if out["report_fetch_failed"]:
            print(f"⚠️ 公告接口取数失败（须人工核验，不可当'无公告'）：{out['report_fetch_failed']}")
            for c in out["report_fetch_failed"]:
                if ANN_ERR.get(c):
                    print(f"   · {c}｜{ANN_ERR[c]}")
        print("=" * W)
        print(f"总计 {len(results)}｜🔔 提醒 {len(out['alert'])}｜"
              f"⛔ 排除 {sum(1 for r in results if r['action']=='EXCLUDE')}｜"
              f"⚠️ 需补数据 {sum(1 for r in results if r['action']=='NEED_DATA')}｜"
              f"📄 基线过期 {len(out['report_alerts'])}")

    js = args.json_out or os.path.join(tempfile.gettempdir(), f"candidate_gate_{time.strftime('%Y%m%d')}.json")
    try:
        with open(js, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2, default=str)
        print(f"\n[JSON] {js}")
    except Exception as e:
        print(f"[JSON] 写入失败：{e}", file=sys.stderr)


if __name__ == "__main__":
    main()