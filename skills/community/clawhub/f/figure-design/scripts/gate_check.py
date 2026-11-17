#!/usr/bin/env python3
"""Validate figure design parameters against the manufacturing rule table.

Usage
-----
    python gate_check.py params.json [--json-out report.json]
    python gate_check.py --ratio 1/7 --height 240 --price 899 --wall 3.0 --gap 0.28
    python gate_check.py --demo

Prints PASS / WARN / FAIL per item, then a G0-G3 gate verdict.
Exit code: 0 if no FAIL, 1 if any FAIL, 2 on bad input.
"""

import argparse
import json
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ---------------------------------------------------------------- rule tables
HEIGHT_RANGE = {
    12: (12, 15), 10: (16, 18), 8: (20, 24), 7: (22, 26),
    6: (28, 32), 4: (40, 45), 3: (50, 60),
}
PRICE_BAND = {
    12: (59, 199), 10: (99, 299), 8: (399, 999), 7: (600, 1500),
    6: (1200, 3000), 4: (2000, 5000), 3: (5000, 99999),
}
DETAIL_BUDGET = {12: 3, 10: 5, 8: 7, 7: 8, 6: 10, 4: 12, 3: 99}
MOQ = {"silicone": 100, "steel": 1000}

DEFAULTS = {
    "ratio": None, "height_mm": None, "price_cny": None, "quantity": None,
    "mold": "silicone", "material": "pvc", "wall_mm": None, "draft_deg": 2.0,
    "gap_mm": None, "colors": None, "points": None, "head_body": "1:1.5",
    "eye_offset_pct": None, "seam_on_face": False, "dfm_signed": False,
    "golden_sample": False, "margin_x": None,
}

RESULTS = []  # (stage, item, status, message)


def add(stage, item, status, msg):
    RESULTS.append({"stage": stage, "item": item, "status": status, "message": msg})


def parse_ratio(value):
    """Accept '1/7', '1:7', '7' -> 7."""
    if value is None:
        return None
    s = str(value).replace(":", "/").strip()
    try:
        if "/" in s:
            a, b = s.split("/", 1)
            return int(float(b) / float(a))
        return int(float(s))
    except (ValueError, ZeroDivisionError):
        return None


def check(p):
    # ---- T0 ------------------------------------------------------------
    d = parse_ratio(p.get("ratio"))
    if d is None:
        add("T0", "比例", "SKIP", "未给出比例，跳过尺度相关校验")
    else:
        if d in HEIGHT_RANGE and p.get("height_mm"):
            lo, hi = HEIGHT_RANGE[d]
            h = float(p["height_mm"]) / 10.0  # table is in cm
            if lo <= h <= hi:
                add("T0", "高度", "PASS", f"{h:.1f}cm 在 1/{d} 的 {lo}-{hi}cm 区间内")
            else:
                add("T0", "高度", "WARN",
                    f"{h:.1f}cm 偏离 1/{d} 常规区间 {lo}-{hi}cm（头发/底座/姿势可造成偏差，请确认）")

        if d in PRICE_BAND and p.get("price_cny"):
            lo, hi = PRICE_BAND[d]
            price = float(p["price_cny"])
            if lo <= price <= hi:
                add("T0", "价格", "PASS", f"¥{price:.0f} 落在 1/{d} 的 ¥{lo}-{hi} 带内")
            elif price < lo:
                add("T0", "价格", "WARN",
                    f"¥{price:.0f} 低于 1/{d} 的 ¥{lo}-{hi} 带，需确认成本能压住")
            else:
                add("T0", "价格", "WARN",
                    f"¥{price:.0f} 高于 1/{d} 的 ¥{lo}-{hi} 带，需要稀缺性理由（限量/签名/材质）")

        if d in DETAIL_BUDGET and p.get("points") is not None:
            budget = DETAIL_BUDGET[d]
            pts = int(p["points"])
            if pts <= budget:
                add("T0", "细节预算", "PASS", f"{pts} 个记忆点 ≤ 1/{d} 的预算 {budget}")
            else:
                add("T0", "细节预算", "FAIL",
                    f"{pts} 个记忆点超过 1/{d} 的预算 {budget}——在这个尺寸上多出来的点会糊成一团")

    if p.get("quantity") and p.get("mold") in MOQ:
        need = MOQ[p["mold"]]
        q = int(p["quantity"])
        if q >= need:
            add("T0", "起订量", "PASS", f"{p['mold']} 模 {q} 件 ≥ 起订 {need}")
        else:
            add("T0", "起订量", "WARN",
                f"{p['mold']} 模通常 {need} 件起，{q} 件单价会偏高；或改用硅胶模")

    # ---- T1 ------------------------------------------------------------
    if p.get("colors") is not None:
        c = int(p["colors"])
        if c <= 4:
            add("T1", "色彩分区", "PASS", f"{c} 块 ≤ 4")
        else:
            add("T1", "色彩分区", "FAIL", f"{c} 块超过 4 块——每多一块多一道工序、多一次偏色风险")

    if p.get("head_body"):
        hb = str(p["head_body"]).replace("：", ":")
        if hb in ("1:1", "1:1.5", "1:2"):
            add("T1", "头身比", "PASS", f"{hb}（幼态/潮/成熟三档之一）")
        else:
            add("T1", "头身比", "WARN", f"{hb} 不在 1:1 / 1:1.5 / 1:2 三档内，请确认是有意为之")

    if p.get("eye_offset_pct") is not None:
        e = float(p["eye_offset_pct"])
        if 15 <= e <= 20:
            add("T1", "眼位", "PASS", f"中线偏下 {e:.0f}%，亲和力区间内")
        else:
            add("T1", "眼位", "WARN", f"中线偏下 {e:.0f}%，常规区间 15-20%（偏高显成熟，偏低显幼态）")

    # ---- T2 ------------------------------------------------------------
    mat = str(p.get("material", "pvc")).lower()
    if p.get("wall_mm") is not None:
        w = float(p["wall_mm"])
        lo, hi = (2.5, 4.0) if mat != "resin" else (1.5, 2.0)
        if lo <= w <= hi:
            add("T2", "壁厚", "PASS", f"{w:.2f}mm 落在 {mat} 的 {lo}-{hi}mm 区间")
        else:
            add("T2", "壁厚", "FAIL", f"{w:.2f}mm 超出 {mat} 的 {lo}-{hi}mm（厚了缩水，薄了注不满/易断）")

    if p.get("draft_deg") is not None:
        a = float(p["draft_deg"])
        if 1 <= a <= 3:
            add("T2", "拔模角", "PASS", f"{a:.1f}° 在 1-3° 内")
        else:
            add("T2", "拔模角", "FAIL", f"{a:.1f}° 超出 1-3°，零件会拉伤或脱不出来")

    if p.get("gap_mm") is not None:
        g = float(p["gap_mm"])
        if 0.25 <= g <= 0.30:
            add("T2", "配合间隙", "PASS", f"{g:.2f}mm 在静配合 0.25-0.30mm 内")
        elif 0.20 <= g <= 0.50:
            add("T2", "配合间隙", "WARN", f"{g:.2f}mm 只在活动件可接受（0.2-0.5mm），静配合请用 0.25-0.30")
        else:
            add("T2", "配合间隙", "FAIL", f"{g:.2f}mm 超出范围——小于 0.2 装不进，大于 0.5 会松垮")

    if p.get("seam_on_face"):
        add("T2", "分模线", "FAIL", "存在穿过面部的分模线——必须重新规划拆件")
    else:
        add("T2", "分模线", "PASS", "未标注面部接缝（请确认已逐条标注位置）")

    if p.get("dfm_signed"):
        add("T2", "DFM 回签", "PASS", "工厂已书面回签")
    else:
        add("T2", "DFM 回签", "FAIL", "工厂未书面回签——口头确认不算通过 G2")

    # ---- T3 ------------------------------------------------------------
    if p.get("margin_x") is not None:
        m = float(p["margin_x"])
        if m >= 3:
            add("T3", "毛利倍数", "PASS", f"{m:.1f}× ≥ 3×")
        else:
            add("T3", "毛利倍数", "FAIL", f"{m:.1f}× < 3×，回 T0 重定尺度（降比例/减配件），不要偷偷减配")

    if p.get("golden_sample"):
        add("T3", "上色样", "PASS", "Golden Sample 已批准并归档")
    else:
        add("T3", "上色样", "FAIL", "Golden Sample 未批准/未归档，不能放行量产")


def gates():
    out = {}
    for g, stages in (("G0", ("T0",)), ("G1", ("T0", "T1")),
                      ("G2", ("T2",)), ("G3", ("T3",))):
        fails = [r for r in RESULTS if r["stage"] in stages and r["status"] == "FAIL"]
        out[g] = {"passed": not fails, "blockers": [r["item"] for r in fails]}
    return out


def render(p):
    icon = {"PASS": "[PASS]", "WARN": "[WARN]", "FAIL": "[FAIL]", "SKIP": "[SKIP]"}
    print("=" * 74)
    print("手办设计参数校验  |  ratio=%s  height=%s  price=%s  mold=%s" % (
        p.get("ratio", "-"), p.get("height_mm", "-"), p.get("price_cny", "-"), p.get("mold", "-")))
    print("=" * 74)
    for r in RESULTS:
        print(f"{icon[r['status']]:7s} {r['stage']}  {r['item']:8s}  {r['message']}")
    print("-" * 74)

    g = gates()
    for name in ("G0", "G1", "G2", "G3"):
        state = "通过" if g[name]["passed"] else "未通过"
        blockers = "" if g[name]["passed"] else "  <- " + ", ".join(g[name]["blockers"])
        print(f"{name}  {state}{blockers}")

    fails = [r for r in RESULTS if r["status"] == "FAIL"]
    warns = [r for r in RESULTS if r["status"] == "WARN"]
    print("-" * 74)
    if fails:
        passed = [n for n in ("G0", "G1", "G2", "G3") if g[n]["passed"]]
        last = passed[-1] if passed else "无"
        print(f"结论：{len(fails)} 项硬性不合格，{len(warns)} 项需确认。当前最高可达闸门：{last}")
        print("建议：优先回到最早失败的环节修，不要在后面的阶段补救。")
    else:
        print(f"结论：无硬性不合格，{len(warns)} 项需人工确认。数值层面可进入下一阶段。")
        print("注意：数值合格不等于设计合格——剪影测试、三视图一致性仍需人工判断。")
    print("=" * 74)
    return fails, g


def main():
    ap = argparse.ArgumentParser(description="手办设计参数校验（G0-G3）")
    ap.add_argument("params", nargs="?", help="JSON 参数文件")
    ap.add_argument("--ratio"); ap.add_argument("--height", dest="height_mm", type=float)
    ap.add_argument("--price", dest="price_cny", type=float)
    ap.add_argument("--qty", dest="quantity", type=int)
    ap.add_argument("--mold", choices=["silicone", "steel"])
    ap.add_argument("--material", choices=["pvc", "resin"])
    ap.add_argument("--wall", dest="wall_mm", type=float)
    ap.add_argument("--draft", dest="draft_deg", type=float)
    ap.add_argument("--gap", dest="gap_mm", type=float)
    ap.add_argument("--colors", type=int)
    ap.add_argument("--points", type=int)
    ap.add_argument("--head-body", dest="head_body")
    ap.add_argument("--eye", dest="eye_offset_pct", type=float)
    ap.add_argument("--seam-on-face", dest="seam_on_face", action="store_true")
    ap.add_argument("--dfm-signed", dest="dfm_signed", action="store_true")
    ap.add_argument("--golden-sample", dest="golden_sample", action="store_true")
    ap.add_argument("--margin", dest="margin_x", type=float)
    ap.add_argument("--json-out", help="把结果写成 JSON 报告")
    ap.add_argument("--demo", action="store_true", help="用一组示例参数演示")
    args = ap.parse_args()

    p = dict(DEFAULTS)

    if args.demo or (not args.params and not args.ratio):
        p.update({"ratio": "1/7", "height_mm": 240, "price_cny": 899, "quantity": 100,
                  "mold": "silicone", "wall_mm": 3.0, "draft_deg": 2.0, "gap_mm": 0.28,
                  "colors": 4, "points": 6, "head_body": "1:1.5", "eye_offset_pct": 17,
                  "seam_on_face": False, "dfm_signed": False, "golden_sample": False,
                  "margin_x": 3.6})
        print("（未提供参数，使用 --demo 示例：1/7 · 240mm · ¥899 · 硅胶模 100 件）\n")
    else:
        if args.params:
            try:
                with open(args.params, encoding="utf-8") as f:
                    p.update(json.load(f))
            except Exception as e:
                print(f"读取参数文件失败：{e}", file=sys.stderr)
                return 2
        for k in ("ratio", "height_mm", "price_cny", "quantity", "mold", "material",
                  "wall_mm", "draft_deg", "gap_mm", "colors", "points", "head_body",
                  "eye_offset_pct", "seam_on_face", "dfm_signed", "golden_sample", "margin_x"):
            v = getattr(args, k, None)
            if v is not None:
                p[k] = v

    check(p)
    fails, g = render(p)

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump({"params": p, "results": RESULTS, "gates": g},
                      f, ensure_ascii=False, indent=2)
        print(f"报告已写入 {args.json_out}")

    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
