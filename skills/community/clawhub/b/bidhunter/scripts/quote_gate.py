#!/usr/bin/env python3
"""
quote_gate.py - 报价闸门（BidHunter v2.7）

把「出价前必须过的算式校验」固化成可执行闸门：
  C-1 品类清算价筛查 → C2 规模换算 → C3 单位单价校验 → M1 毛利红线
外加 5 项正则扫不出来的人工核对卡（C1/C0/C4/C5/C6）。

铁律：任一道不过，禁止输出金额；缺参数时只交成本模型框架 + 参数待补清单，
     绝不交带金额的报价函。错的数字比没有数字危害大得多。

零依赖：仅标准库，不联网、不调用任何外部命令与模型。

Usage:
  python3 quote_gate.py params                 # 交互式填一次参数（写入 ~/.config/bidhunter/）
  python3 quote_gate.py params --show          # 查看当前参数 + 过期提醒
  python3 quote_gate.py check --labor --heads 7 --months 12 --cost 200000 --quote 260000
  python3 quote_gate.py check --prior-amount 600000 --prior-scale 300 --new-scale 60 --quote 120000
  python3 quote_gate.py check --selftest
"""
import argparse
import datetime
import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GATE_PATH = os.path.join(HERE, "quote", "gate.json")
CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "bidhunter")
PARAMS_PATH = os.path.join(CONFIG_DIR, "quote_params.json")

PASS, BLOCK, SKIP = "PASS", "BLOCK", "SKIP"
MARK = {PASS: "✅", BLOCK: "❌", SKIP: "⬜"}


def load_gate(path=GATE_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def defaults():
    g = load_gate()
    t = g["thresholds"]
    return {
        "schema": "bidhunter-quote-params/v1",
        "as_of": "",
        "min_wage_monthly": None,
        "min_wage_region": "",
        "min_wage_as_of": "",
        "labor_coefficient": [t["labor_coefficient_low"], t["labor_coefficient_high"]],
        "margin_floor_pct": t["margin_floor_pct_default"],
        "scale_tolerance_pct": t["scale_tolerance_pct"],
        "tax_rate": 0.06,
        "unit_price_bands": {},
    }


def load_params():
    d = defaults()
    if os.path.exists(PARAMS_PATH):
        try:
            with open(PARAMS_PATH, "r", encoding="utf-8") as f:
                d.update(json.load(f))
        except Exception:
            pass
    return d


def save_params(d):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    d["as_of"] = datetime.date.today().isoformat()
    tmp = PARAMS_PATH + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    os.replace(tmp, PARAMS_PATH)
    try:
        os.chmod(PARAMS_PATH, 0o600)
    except OSError:
        pass
    return PARAMS_PATH


def params_age_days(p):
    stamp = p.get("min_wage_as_of") or p.get("as_of") or ""
    if not stamp:
        return None
    try:
        d = datetime.date.fromisoformat(stamp[:10])
    except ValueError:
        return None
    return (datetime.date.today() - d).days


def params_stale(p):
    g = load_gate()
    limit = g["thresholds"]["params_stale_days"]
    age = params_age_days(p)
    if age is None:
        return True, None, limit
    return age > limit, age, limit


# ---------------------------------------------------------------- 算式校验

def check_floor_price(a, p):
    """C-1 品类清算价筛查：对手地板价 ≈ 月最低工资 × 人数 × 月数 × 系数"""
    wage = a.min_wage or p.get("min_wage_monthly")
    if not wage or not a.heads or not a.months:
        missing = [n for n, v in (("月最低工资", wage), ("人数", a.heads), ("月数", a.months)) if not v]
        return {"id": "C-1", "status": SKIP, "missing": missing,
                "title": "品类清算价筛查",
                "detail": "地板价 = 月最低工资 × 人数 × 月数 × (1.10~1.25)"}
    lo_k, hi_k = p.get("labor_coefficient", [1.10, 1.25])
    base = wage * a.heads * a.months
    lo, hi = base * lo_k, base * hi_k
    out = {"id": "C-1", "status": PASS, "missing": [],
           "title": "品类清算价筛查",
           "detail": f"对手地板价 {lo:,.0f} ~ {hi:,.0f} 元（{wage:,.0f}/月 × {a.heads}人 × {a.months}月）"}
    if a.cost:
        if a.cost >= lo:
            out["status"] = BLOCK
            out["detail"] += f"｜我方成本 {a.cost:,.0f} 元 ≥ 地板价下限 → 结构性陪跑"
            out["fix"] = "即使保本零毛利也进不了前列，建议直接不投，不要继续做标书"
        else:
            out["detail"] += f"｜我方成本 {a.cost:,.0f} 元低于地板价下限"
    else:
        out["detail"] += "｜未提供我方成本，无法判定陪跑"
    return out


def check_scale_linearity(a, p):
    """C2 规模换算：新口径金额 ≈ 旧口径金额 × 新规模 ÷ 旧规模"""
    if not (a.prior_amount and a.prior_scale and a.new_scale):
        missing = [n for n, v in (("旧口径金额", a.prior_amount), ("旧规模", a.prior_scale),
                                  ("新规模", a.new_scale)) if not v]
        return {"id": "C2", "status": SKIP, "missing": missing,
                "title": "规模换算（线性校验）",
                "detail": "新金额 = 旧金额 × 新规模 ÷ 旧规模"}
    expect = a.prior_amount * a.new_scale / a.prior_scale
    out = {"id": "C2", "status": PASS, "missing": [], "title": "规模换算（线性校验）",
           "detail": f"线性推算 {expect:,.0f} 元（{a.prior_amount:,.0f} × {a.new_scale}/{a.prior_scale}）"}
    if a.quote:
        dev = abs(a.quote - expect) / expect * 100 if expect else 0.0
        tol = p.get("scale_tolerance_pct", 15.0)
        out["detail"] += f"｜填入 {a.quote:,.0f} 元，偏差 {dev:.1f}%（容差 {tol:.0f}%）"
        if dev > tol:
            out["status"] = BLOCK
            out["fix"] = "先解释规模差异来源（台数/人月/点位/期数）；解释不通则禁止沿用旧价"
    else:
        out["detail"] += "｜未提供拟报金额，无法比对"
    return out


def check_unit_price(a, p):
    """C3 单位单价校验：单价 = 总价 ÷ 数量"""
    if not (a.quote and a.qty):
        missing = [n for n, v in (("拟报总价", a.quote), ("数量", a.qty)) if not v]
        return {"id": "C3", "status": SKIP, "missing": missing,
                "title": "单位单价校验", "detail": "单价 = 总价 ÷ 数量"}
    unit = a.quote / a.qty
    out = {"id": "C3", "status": PASS, "missing": [], "title": "单位单价校验",
           "detail": f"单价 {unit:,.2f} 元（{a.quote:,.0f} ÷ {a.qty:g}）"}
    band = (p.get("unit_price_bands") or {}).get(a.category) if a.category else None
    if band and len(band) == 2:
        lo, hi = band
        out["detail"] += f"｜价带 {lo:,.2f}~{hi:,.2f}"
        if not (lo <= unit <= hi):
            out["status"] = BLOCK
            out["fix"] = "先用单价反查总价，而不是用总价解释单价"
    else:
        out["detail"] += "｜无该品类单价带，仅做算术核对"
    return out


def check_margin(a, p):
    """M1 毛利红线"""
    if not (a.quote and a.cost):
        missing = [n for n, v in (("拟报总价", a.quote), ("成本", a.cost)) if not v]
        return {"id": "M1", "status": SKIP, "missing": missing,
                "title": "毛利红线", "detail": "毛利率 = (总价 - 成本) ÷ 总价"}
    rate = (a.quote - a.cost) / a.quote * 100 if a.quote else 0.0
    floor = p.get("margin_floor_pct", 17.0)
    out = {"id": "M1", "status": PASS, "missing": [], "title": "毛利红线",
           "detail": f"毛利率 {rate:.2f}%（红线 {floor:.1f}%）"}
    if rate < floor:
        out["status"] = BLOCK
        out["fix"] = "低于红线不得出价；若战略压价，必须留下书面决策依据"
    return out


def check_market_band(a, p):
    """C0 市场价带偏离（有外部锚点时才检）"""
    if not (a.quote and a.market_low and a.market_high):
        return None
    mid = (a.market_low + a.market_high) / 2
    dev = abs(a.quote - mid) / mid * 100 if mid else 0.0
    tol = load_gate()["thresholds"]["market_band_deviation_pct"]
    out = {"id": "C0", "status": PASS, "missing": [], "title": "市场价带偏离",
           "detail": f"价带 {a.market_low:,.0f}~{a.market_high:,.0f}，中值偏离 {dev:.1f}%（阈值 {tol:.0f}%）"}
    if dev > tol:
        out["status"] = BLOCK
        out["fix"] = "偏离价带必须能书面解释，否则视为测算口径有错"
    return out


def run_gates(a, p):
    cards = [check_floor_price(a, p), check_scale_linearity(a, p),
             check_unit_price(a, p), check_margin(a, p)]
    mb = check_market_band(a, p)
    if mb:
        cards.append(mb)
    return cards


def verdict_of(cards):
    if any(c["status"] == BLOCK for c in cards):
        return "禁止出价"
    if any(c["status"] == SKIP for c in cards) or not cards:
        return "参数待补"
    return "已过闸门"


# ---------------------------------------------------------------- 渲染

def render_check(args, p, cards, gate):
    stale, age, limit = params_stale(p)
    out = []
    out.append("=" * 62)
    out.append("🧮 BidHunter 报价闸门 (v2.7)")
    out.append("=" * 62)
    out.append(f"参数库: {PARAMS_PATH}")
    out.append(f"  最低工资: {p.get('min_wage_monthly') or '未填'} 元/月"
               f"　地区: {p.get('min_wage_region') or '未填'}"
               f"　标准起始: {p.get('min_wage_as_of') or '未填'}")
    if stale:
        tip = f"已 {age} 天未更新" if age is not None else "缺少日期"
        out.append(f"  ⚠️ 参数可能过期（{tip}，建议 ≤{limit} 天）→ 先跑 python3 bidhunter.py quote params")
    out.append("")

    v = verdict_of(cards)
    for c in cards:
        out.append(f"{MARK[c['status']]} [{c['id']}] {c['title']}"
                   f"{'（缺: ' + '、'.join(c['missing']) + '）' if c.get('missing') else ''}")
        out.append(f"    {c['detail']}")
        if c["status"] == BLOCK and c.get("fix"):
            out.append(f"    → {c['fix']}")
    out.append("")

    manual = gate.get("manual_cards", [])
    out.append(f"--- 人工核对卡（{len(manual)} 项，算式扫不出来，必须逐条确认）---")
    for m in manual:
        out.append(f"☐ [{m['id']}] {m['name']}")
        out.append(f"    → {m['action']}")
    out.append("")

    out.append("=" * 62)
    out.append(f"结论：{v}")
    if v == "已过闸门":
        out.append(f"  拟报金额：{args.quote:,.2f} 元 —— 算式校验全部通过，仍需逐条确认人工卡")
    else:
        out.append("  ⛔ 本闸门不给出结论金额。缺什么补什么，补齐后重跑；")
        out.append("     上表出现的金额仅为你输入的比对值，不构成报价结论。")
        out.append("     补齐前只允许交成本模型框架与参数待补清单，不得交带金额的报价函。")
    blocked = [c for c in cards if c["status"] == BLOCK]
    if blocked:
        out.append(f"  卡住 {len(blocked)} 道：" + "、".join(c["id"] for c in blocked))
    out.append("=" * 62)
    out.append("⚠️ " + gate["disclaimer"])
    return "\n".join(out), v


def render_params(p):
    stale, age, limit = params_stale(p)
    out = ["📦 报价参数库", f"  路径: {PARAMS_PATH}"]
    if not os.path.exists(PARAMS_PATH):
        out.append("  状态: 尚未创建 → 跑 python3 bidhunter.py quote params 填一次")
        return "\n".join(out)
    for k in ("as_of", "min_wage_monthly", "min_wage_region", "min_wage_as_of",
              "labor_coefficient", "margin_floor_pct", "scale_tolerance_pct",
              "tax_rate", "unit_price_bands"):
        out.append(f"  {k}: {json.dumps(p.get(k), ensure_ascii=False)}")
    if stale:
        out.append(f"  ⚠️ 可能过期：{'已 %s 天未更新' % age if age is not None else '缺少日期'}"
                   f"（建议 ≤{limit} 天）")
    else:
        out.append(f"  ✅ 参数在有效期内（{age} 天）")
    return "\n".join(out)


def interactive_params(p):
    print("报价闸门参数初始化（直接回车用括号内默认值；只写本机，不上传）")
    try:
        wage = input(f"  ① 当地月最低工资（元/月）[{p.get('min_wage_monthly') or ''}]: ").strip()
        region = input(f"  ② 适用地区[{p.get('min_wage_region') or ''}]: ").strip()
        wage_asof = input(f"  ③ 该标准执行起始日 YYYY-MM-DD[{p.get('min_wage_as_of') or ''}]: ").strip()
        floor = input(f"  ④ 毛利红线 %（默认 {p.get('margin_floor_pct')}）: ").strip()
        tol = input(f"  ⑤ 规模换算容差 %（默认 {p.get('scale_tolerance_pct')}）: ").strip()
        tax = input(f"  ⑥ 常用税率（服务类 0.06 / 货物类 0.13，默认 {p.get('tax_rate')}）: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n已取消，未写入。", file=sys.stderr)
        return 1
    if wage:
        try:
            p["min_wage_monthly"] = float(wage)
        except ValueError:
            print("[error] 最低工资必须是数字", file=sys.stderr)
            return 1
    if region:
        p["min_wage_region"] = region
    if wage_asof:
        p["min_wage_asof"] = None
        p["min_wage_as_of"] = wage_asof
    for key, raw in (("margin_floor_pct", floor), ("scale_tolerance_pct", tol), ("tax_rate", tax)):
        if raw:
            try:
                p[key] = float(raw)
            except ValueError:
                print(f"[error] {key} 必须是数字", file=sys.stderr)
                return 1
    p.pop("min_wage_asof", None)
    path = save_params(p)
    print(f"\n✅ 已写入 {path}（权限 600）")
    print("   最低工资会随年度调整，到期提醒阈值 "
          f"{load_gate()['thresholds']['params_stale_days']} 天。")
    return 0


# ---------------------------------------------------------------- 自检

def selftest():
    results = []

    def ok(name, cond):
        results.append((name, bool(cond)))

    g = load_gate()
    ok("闸门库可加载", g["schema"] == "bidhunter-quote-gate/v1")
    ok("阈值齐全", all(k in g["thresholds"] for k in
                     ("labor_coefficient_low", "scale_tolerance_pct", "margin_floor_pct_default")))
    ok("算式卡 4 道", len(g["computed_cards"]) == 4)
    ok("人工卡 5 道", len(g["manual_cards"]) == 5)
    gate_raw = json.dumps(g, ensure_ascii=False)
    roots = (os.path.expanduser("~"), tempfile.gettempdir(), os.sep + "home", os.sep + "tmp")
    ok("闸门库不含本机绝对路径", not any(r and r in gate_raw for r in roots))
    ok("闸门库不含具体金额（无 6 位以上连续数字）", not re.search(r"\d{6,}", gate_raw))

    d = defaults()
    ok("默认系数 1.10/1.25", d["labor_coefficient"] == [1.10, 1.25])
    ok("默认毛利红线 17", d["margin_floor_pct"] == 17.0)

    class A:
        pass
    p = dict(d, min_wage_monthly=2320.0)

    a = A(); a.min_wage = None; a.heads = 7; a.months = 12; a.cost = 300000.0
    a.prior_amount = None; a.prior_scale = None; a.new_scale = None
    a.quote = None; a.qty = None; a.category = None
    a.market_low = None; a.market_high = None
    r = check_floor_price(a, p)
    ok("地板价：成本 300000 ≥ 地板价下限 → BLOCK", r["status"] == BLOCK)

    a2 = A(); a2.min_wage = None; a2.heads = 7; a2.months = 12; a2.cost = 150000.0
    r2 = check_floor_price(a2, p)
    ok("地板价：成本 150000 < 地板价下限 → PASS", r2["status"] == PASS)

    a3 = A(); a3.min_wage = None; a3.heads = None; a3.months = None
    r3 = check_floor_price(a3, p)
    ok("地板价：缺人数/月数 → SKIP 并列出缺失", r3["status"] == SKIP and "人数" in r3["missing"])

    a4 = A(); a4.prior_amount = 600000.0; a4.prior_scale = 300; a4.new_scale = 60
    a4.quote = 600000.0
    r4 = check_scale_linearity(a4, p)
    ok("规模换算：漏做换算的 400% 偏差 → BLOCK", r4["status"] == BLOCK)

    a5 = A(); a5.prior_amount = 600000.0; a5.prior_scale = 300; a5.new_scale = 60
    a5.quote = 120000.0
    ok("规模换算：换算后正解 → PASS", check_scale_linearity(a5, p)["status"] == PASS)

    a6 = A(); a6.quote = 300000.0; a6.cost = 310000.0
    ok("毛利：负毛利 → BLOCK", check_margin(a6, p)["status"] == BLOCK)
    a7 = A(); a7.quote = 300000.0; a7.cost = 200000.0
    ok("毛利：33% → PASS", check_margin(a7, p)["status"] == PASS)
    a8 = A(); a8.quote = 300000.0; a8.cost = None
    ok("毛利：缺成本 → SKIP", check_margin(a8, p)["status"] == SKIP)

    a9 = A(); a9.quote = 100000.0; a9.qty = 60.0; a9.category = None
    ok("单价：100000÷60 → PASS", check_unit_price(a9, p)["status"] == PASS)

    ok("结论：有 BLOCK → 禁止出价",
       verdict_of([{"status": PASS}, {"status": BLOCK}]) == "禁止出价")
    ok("结论：有 SKIP 无 BLOCK → 参数待补",
       verdict_of([{"status": PASS}, {"status": SKIP}]) == "参数待补")
    ok("结论：全 PASS → 已过闸门",
       verdict_of([{"status": PASS}, {"status": PASS}]) == "已过闸门")

    banned = r"^\s*(?:import|from)\s+(?:urllib|requests|socket|subprocess|smtplib|http)\b"
    ok("无网络/子进程依赖（无相关 import）",
       not re.search(banned, open(__file__, encoding="utf-8").read(), re.MULTILINE))

    passed = sum(1 for _, c in results if c)
    for name, cond in results:
        print(f"  {'✅' if cond else '❌'} {name}")
    print(f"\n自检 {passed}/{len(results)} 通过")
    return 0 if passed == len(results) else 1


# ---------------------------------------------------------------- 入口

def main():
    ap = argparse.ArgumentParser(description="BidHunter 报价闸门 v2.7")
    sub = ap.add_subparsers(dest="cmd")

    ap.add_argument("--selftest", action="store_true", help="运行内置自检")

    pp = sub.add_parser("params", help="初始化/查看报价参数库")
    pp.add_argument("--show", action="store_true", help="只看不写")

    cp = sub.add_parser("check", help="跑闸门")
    cp.add_argument("--quote", type=float, help="拟报总价（元）")
    cp.add_argument("--cost", type=float, help="我方成本（元）")
    cp.add_argument("--qty", type=float, help="数量（台/人/点位）")
    cp.add_argument("--category", help="品类名，用于查单价带")
    cp.add_argument("--heads", type=int, help="人数（纯人力品类）")
    cp.add_argument("--months", type=int, help="月数")
    cp.add_argument("--labor", action="store_true", help="标记为纯人力品类")
    cp.add_argument("--min-wage", type=float, help="临时覆盖月最低工资")
    cp.add_argument("--prior-amount", type=float, help="旧口径金额")
    cp.add_argument("--prior-scale", type=float, help="旧口径规模")
    cp.add_argument("--new-scale", type=float, help="新口径规模")
    cp.add_argument("--market-low", type=float, help="市场价带下限")
    cp.add_argument("--market-high", type=float, help="市场价带上限")

    args = ap.parse_args()

    if args.selftest or getattr(args, "cmd", None) is None and not sys.stdin.isatty():
        return selftest()

    p = load_params()
    gate = load_gate()

    if args.cmd == "params":
        if args.show:
            print(render_params(p))
            return 0
        return interactive_params(p)

    if args.cmd == "check":
        cards = run_gates(args, p)
        text, v = render_check(args, p, cards, gate)
        print(text)
        return 0 if v == "已过闸门" else 2

    print(render_params(p))
    print("\n用法：quote params [--show] | quote check --help")
    return 0


if __name__ == "__main__":
    sys.exit(main())
