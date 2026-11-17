#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu Sales Analysis Engine（菜单销量数据分析引擎）
=================================================
对菜单销量数据从五个维度统计：菜品畅销/滞销排名、销量趋势变化、品类占比、时段分布、关键发现，
并生成结构化优化报告（概览 / 关键发现 / 滞销优化建议 / 菜单结构调整建议）。

输入（CSV / JSON，字段可中英文、顺序不限）：
  日期 date, 菜品 dish, 品类 category, 时段 period, 销量 quantity [, 销售额 revenue]

输出：标准 Markdown 报告（stdout）+ 可选 JSON（--json 路径）。
依赖：仅 Python 标准库。Excel(.xlsx) 请先经 xlsx 工具转 CSV/JSON，或用配套 sales_entry.html 上传解析。
用法：
  python menu_sales_analysis.py --input sales.csv
  python menu_sales_analysis.py --input sales.json --json out.json
  cat sales.csv | python menu_sales_analysis.py
"""

import sys
import io
import os
import re
import json
import csv
import math
import argparse
from datetime import datetime

# 强制 UTF-8，避免 Windows 控制台乱码（幂等：已为 utf-8 则跳过，防止重复包装导致 buffer 关闭）
if getattr(sys.stdout, "encoding", None) != "utf-8":
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")
    except Exception:
        pass


# ---------------------------------------------------------------------------
# 解析
# ---------------------------------------------------------------------------
COL_ALIASES = {
    "date": ["日期", "时间", "date", "day", "交易日"],
    "dish": ["菜品", "菜名", "名称", "name", "dish", "item"],
    "category": ["品类", "类别", "分类", "category", "cat", "type"],
    "period": ["时段", "餐段", "period", "slot", "meal"],
    "quantity": ["销量", "份数", "数量", "qty", "quantity", "sales", "volume"],
    "revenue": ["销售额", "营收", "金额", "revenue", "amount", "income"],
}


def _norm_header(h):
    h = h.strip().lower()
    for key, aliases in COL_ALIASES.items():
        for a in aliases:
            if a in h:
                return key
    return None


def _clean_num(s):
    if s is None:
        return None
    s = str(s).strip()
    if s == "":
        return None
    s = re.sub(r"[^0-9.\-]", "", s)
    if s in ("", "-", ".", "-."):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _parse_date(s):
    if s is None:
        return None
    s = str(s).strip()
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M",
               "%m-%d", "%m/%d", "%Y%m%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    # 纯数字如 20260719
    m = re.search(r"\d{4}\d{2}\d{2}", s)
    if m:
        try:
            return datetime.strptime(m.group(0), "%Y%m%d")
        except ValueError:
            pass
    return None


def parse_input(text):
    """返回 (records, anomalies)。records: list[dict]。"""
    text = text.lstrip()
    records, anomalies = [], []

    # JSON
    if text.startswith("["):
        try:
            arr = json.loads(text)
            if isinstance(arr, list):
                records, anomalies = _from_rows(arr, is_json=True)
                return records, anomalies
        except Exception as e:
            return [], [f"JSON 解析失败：{e}"]
    elif text.startswith("{"):
        try:
            obj = json.loads(text)
            arr = obj.get("records") or obj.get("data") or obj.get("sales") or []
            if isinstance(arr, list):
                records, anomalies = _from_rows(arr, is_json=True)
                return records, anomalies
        except Exception as e:
            return [], [f"JSON 解析失败：{e}"]

    # CSV
    reader = csv.reader(io.StringIO(text))
    rows = [r for r in reader if any(c.strip() for c in r)]
    if not rows:
        return [], ["未检测到任何销量数据。"]
    header = rows[0]
    idx = {_norm_header(h): i for i, h in enumerate(header)}
    if "quantity" not in idx and "dish" not in idx:
        # 无表头，按默认顺序：日期,菜品,品类,时段,销量
        idx = {"date": 0, "dish": 1, "category": 2, "period": 3, "quantity": 4}
        data_rows = rows
    else:
        data_rows = rows[1:]
    for ln in data_rows:
        rec = _row_to_record(ln, idx, has_header=("quantity" in idx))
        if rec is None:
            anomalies.append(f"数据行无效（需含菜品名与正数销量）：{ln}")
            continue
        if rec:
            records.append(rec)
        else:
            anomalies.append(f"数据行缺少必填字段（菜品/销量）：{ln}")
    if not records:
        anomalies.append("没有可用的合法销量数据，请检查后重新提交。")
    return records, anomalies


def _from_rows(arr, is_json=True):
    records, anomalies = [], []
    for item in arr:
        if not isinstance(item, dict):
            anomalies.append(f"JSON 记录须为对象：{item}")
            continue
        rec = _dict_to_record(item)
        if rec:
            records.append(rec)
        else:
            anomalies.append(f"JSON 记录无效（需含菜品名 dish 与正数销量 quantity）：{item}")
    if not records:
        anomalies.append("没有可用的合法销量数据，请检查后重新提交。")
    return records, anomalies


def _dict_to_record(d):
    dish = d.get("dish") or d.get("name") or d.get("菜品")
    qty = d.get("quantity") or d.get("销量") or d.get("qty")
    if dish is None or qty is None:
        return None
    qty = _clean_num(qty)
    if qty is None or qty < 0:
        return None
    rev = d.get("revenue") or d.get("销售额")
    rev = _clean_num(rev) if rev is not None else None
    dt = _parse_date(d.get("date") or d.get("日期"))
    return {
        "date": dt,
        "date_raw": str(d.get("date") or d.get("日期") or ""),
        "dish": str(dish).strip(),
        "category": str(d.get("category") or d.get("品类") or "未分类").strip(),
        "period": str(d.get("period") or d.get("时段") or "全天").strip(),
        "quantity": qty,
        "revenue": rev,
    }


def _row_to_record(ln, idx, has_header):
    def get(key):
        i = idx.get(key)
        return ln[i].strip() if (i is not None and i < len(ln)) else ""
    dish = get("dish")
    qty_raw = get("quantity")
    qty = _clean_num(qty_raw)
    if not dish or qty is None or qty < 0:
        return None
    rev_raw = get("revenue")
    rev = _clean_num(rev_raw) if rev_raw else None
    dt = _parse_date(get("date"))
    return {
        "date": dt,
        "date_raw": get("date"),
        "dish": dish,
        "category": get("category") or "未分类",
        "period": get("period") or "全天",
        "quantity": qty,
        "revenue": rev,
    }


# ---------------------------------------------------------------------------
# 分析
# ---------------------------------------------------------------------------
def analyze(records):
    n = len(records)
    dates = sorted({r["date"] for r in records if r["date"]})
    date_min = dates[0] if dates else None
    date_max = dates[-1] if dates else None
    total_qty = sum(r["quantity"] for r in records)
    total_rev = sum(r["revenue"] for r in records if r["revenue"] is not None)
    dishes = sorted({r["dish"] for r in records})
    n_days = len(dates)
    avg_daily = (total_qty / n_days) if n_days else total_qty

    # 排名
    by_dish = {}
    for r in records:
        d = by_dish.setdefault(r["dish"], {"dish": r["dish"], "qty": 0.0, "rev": 0.0})
        d["qty"] += r["quantity"]
        if r["revenue"] is not None:
            d["rev"] += r["revenue"]
    ranked = sorted(by_dish.values(), key=lambda x: x["qty"], reverse=True)
    for d in ranked:
        d["share"] = d["qty"] / total_qty if total_qty else 0.0
        d["avg_day"] = d["qty"] / n_days if n_days else d["qty"]
    top = ranked[:5]
    # 滞销：销量低于平均日销的 50% 或排在末位（取末 5，或低于阈值）
    avg_dish_qty = total_qty / len(ranked) if ranked else 0
    slow = [d for d in ranked if d["qty"] < avg_dish_qty * 0.5]
    slow = sorted(slow, key=lambda x: x["qty"])[:5] if slow else ranked[-5:]

    # 趋势（整体日销量）
    daily = {}
    for r in records:
        if r["date"]:
            daily[r["date"]] = daily.get(r["date"], 0.0) + r["quantity"]
    daily_series = [(d, daily[d]) for d in sorted(daily)]
    trend_overall = None
    if len(daily_series) >= 2:
        first, last = daily_series[0][1], daily_series[-1][1]
        if first:
            trend_overall = (last - first) / first
    # 单品趋势：前半段 vs 后半段（按日期均分），或线性回归斜率
    dish_trend = []
    for d in dishes:
        dr = sorted([r for r in records if r["dish"] == d and r["date"]], key=lambda x: x["date"])
        if len(dr) >= 2:
            xs = [(r["date"] - dates[0]).days for r in dr]
            ys = [r["quantity"] for r in dr]
            slope = _linreg_slope(xs, ys)
            first_half = sum(r["quantity"] for r in dr[:len(dr)//2])
            second_half = sum(r["quantity"] for r in dr[len(dr)//2:])
            base = first_half if first_half else 1
            change = (second_half - first_half) / base
            dish_trend.append({"dish": d, "slope": slope, "change": change,
                               "first": first_half, "second": second_half})
    rising = sorted([t for t in dish_trend if t["change"] > 0.10], key=lambda x: x["change"], reverse=True)
    falling = sorted([t for t in dish_trend if t["change"] < -0.10], key=lambda x: x["change"])

    # 品类占比
    by_cat = {}
    for r in records:
        c = by_cat.setdefault(r["category"], {"category": r["category"], "qty": 0.0, "dishes": set()})
        c["qty"] += r["quantity"]
        c["dishes"].add(r["dish"])
    cat_list = []
    for c in by_cat.values():
        cat_list.append({"category": c["category"], "qty": c["qty"],
                         "share": c["qty"] / total_qty if total_qty else 0.0,
                         "n_dishes": len(c["dishes"]),
                         "avg_dish": c["qty"] / len(c["dishes"]) if c["dishes"] else 0,
                         "dishes": sorted(c["dishes"])})
    cat_list.sort(key=lambda x: x["qty"], reverse=True)

    # 时段分布
    by_period = {}
    for r in records:
        p = by_period.setdefault(r["period"], {"period": r["period"], "qty": 0.0})
        p["qty"] += r["quantity"]
    period_list = [{"period": p["period"], "qty": p["qty"],
                    "share": p["qty"] / total_qty if total_qty else 0.0}
                   for p in by_period.values()]
    period_list.sort(key=lambda x: x["qty"], reverse=True)
    peak_period = period_list[0]["period"] if period_list else "—"

    # 关键发现
    findings = []
    if top:
        findings.append(f"销量冠军为「{top[0]['dish']}」，累计 {top[0]['qty']:.0f} 份，"
                        f"占全菜单 {top[0]['share']*100:.1f}%，存在一定集中度。")
    if len(ranked) >= 2 and ranked[-1]["qty"] > 0:
        findings.append(f"滞销末端为「{ranked[-1]['dish']}」，仅 {ranked[-1]['qty']:.0f} 份，"
                        f"约为冠军的 {ranked[-1]['qty']/top[0]['qty']*100:.1f}%。")
    if trend_overall is not None:
        direction = "上升" if trend_overall >= 0 else "下滑"
        findings.append(f"整体日销量由 {daily_series[0][1]:.0f} 份升至 {daily_series[-1][1]:.0f} 份，"
                        f"区间{date_min.date() if date_min else ''}~{date_max.date() if date_max else ''}整体{direction} {abs(trend_overall)*100:.1f}%。")
    if len(cat_list) >= 1:
        findings.append(f"品类集中度：{cat_list[0]['category']} 占比 {cat_list[0]['share']*100:.1f}%（{cat_list[0]['n_dishes']} 道），"
                        f"{'品类结构偏单一，建议丰富其他品类' if cat_list[0]['share'] > 0.5 else '品类结构较均衡'}。")
    if peak_period and peak_period != "全天":
        findings.append(f"高峰时段为「{peak_period}」，贡献 {period_list[0]['share']*100:.1f}% 销量，"
                        f"建议在该时段强化备货与前厅主推。")
    if rising:
        findings.append(f"上升趋势菜品：{('、'.join(t['dish'] for t in rising[:3]))}，可重点培养为下一波招牌。")
    if falling:
        findings.append(f"下滑预警菜品：{('、'.join(t['dish'] for t in falling[:3]))}，需排查原因（季节/口味/竞品/陈列）。")

    diag = {
        "n": n,
        "n_dishes": len(dishes),
        "n_days": n_days,
        "date_min": date_min.strftime("%Y-%m-%d") if date_min else None,
        "date_max": date_max.strftime("%Y-%m-%d") if date_max else None,
        "total_qty": round(total_qty, 2),
        "total_revenue": round(total_rev, 2) if total_rev else None,
        "avg_daily_qty": round(avg_daily, 2),
        "ranked": ranked,
        "top": top,
        "slow": slow,
        "avg_dish_qty": round(avg_dish_qty, 2),
        "daily_series": [[d.strftime("%Y-%m-%d"), round(q, 2)] for d, q in daily_series],
        "trend_overall": round(trend_overall, 4) if trend_overall is not None else None,
        "rising": rising,
        "falling": falling,
        "cat_list": cat_list,
        "period_list": period_list,
        "peak_period": peak_period,
        "findings": findings,
    }
    return diag


def _linreg_slope(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den if den else 0.0


# ---------------------------------------------------------------------------
# 报告
# ---------------------------------------------------------------------------
def pct(x, d=1):
    return f"{x*100:.{d}f}%"


def build_report(diag):
    L = []
    L.append("# 菜单销量数据分析报告（Menu Sales Analytics）")
    L.append("")
    L.append("## 1. 销量数据概览")
    L.append("")
    rev_s = f"¥{diag['total_revenue']:,.2f}" if diag["total_revenue"] is not None else "未提供"
    L.append(f"- **记录数**：{diag['n']} 条　|　**菜品数**：{diag['n_dishes']} 道　|　**统计天数**：{diag['n_days']} 天")
    L.append(f"- **统计区间**：{diag['date_min']} ~ {diag['date_max']}")
    L.append(f"- **总销量**：{diag['total_qty']:,.0f} 份　|　**日均销量**：{diag['avg_daily_qty']:,.0f} 份/天　|　**总销售额**：{rev_s}")
    L.append("")

    L.append("## 2. 菜品畅销 / 滞销排名")
    L.append("")
    L.append("**畅销 Top 5**")
    L.append("")
    L.append("| 排名 | 菜品 | 累计销量(份) | 占比 | 日均(份) |")
    L.append("|------|------|------:|------:|------:|")
    for i, d in enumerate(diag["top"], 1):
        L.append(f"| {i} | {d['dish']} | {d['qty']:.0f} | {pct(d['share'])} | {d['avg_day']:.0f} |")
    L.append("")
    L.append("**滞销 Bottom（销量低于均值 50% 或末位）**")
    L.append("")
    L.append("| 菜品 | 累计销量(份) | 占比 | 日均(份) |")
    L.append("|------|------:|------:|------:|")
    for d in diag["slow"]:
        L.append(f"| {d['dish']} | {d['qty']:.0f} | {pct(d['share'])} | {d['avg_day']:.0f} |")
    L.append("")

    L.append("## 3. 销量趋势变化")
    L.append("")
    if diag["trend_overall"] is not None:
        direction = "上升" if diag["trend_overall"] >= 0 else "下滑"
        L.append(f"- **整体日销量趋势**：区间整体{direction} **{abs(diag['trend_overall'])*100:.1f}%**"
                 f"（{diag['daily_series'][0][1]:.0f} → {diag['daily_series'][-1][1]:.0f} 份/天）。")
    else:
        L.append("- 整体日销量趋势：数据不足（需 ≥2 个交易日）无法判定趋势。")
    L.append("")
    if diag["daily_series"]:
        L.append("**每日销量走势**：" + "、".join(f"{d}={q:.0f}" for d, q in diag["daily_series"]))
        L.append("")
    if diag["rising"]:
        L.append(f"- **上升趋势（后半段 vs 前半段）**：" +
                 "、".join(f"{t['dish']}(+{t['change']*100:.0f}%)" for t in diag["rising"][:5]))
    if diag["falling"]:
        L.append(f"- **下滑预警**：" +
                 "、".join(f"{t['dish']}({t['change']*100:.0f}%)" for t in diag["falling"][:5]))
    L.append("")

    L.append("## 4. 品类占比")
    L.append("")
    L.append("| 品类 | 销量(份) | 占比 | 菜品数 | 品类均销(份/道) |")
    L.append("|------|------:|------:|------:|------:|")
    for c in diag["cat_list"]:
        L.append(f"| {c['category']} | {c['qty']:.0f} | {pct(c['share'])} | {c['n_dishes']} | {c['avg_dish']:.0f} |")
    L.append("")

    L.append("## 5. 时段分布")
    L.append("")
    if len(diag["period_list"]) > 1 or diag["period_list"][0]["period"] != "全天":
        L.append("| 时段 | 销量(份) | 占比 |")
        L.append("|------|------:|------:|")
        for p in diag["period_list"]:
            L.append(f"| {p['period']} | {p['qty']:.0f} | {pct(p['share'])} |")
        L.append("")
        L.append(f"> 高峰时段：**{diag['peak_period']}**（{pct(diag['period_list'][0]['share'])}）。")
    else:
        L.append("> 数据未含时段字段，跳过时段分布分析。")
    L.append("")

    L.append("## 6. 关键发现（Key Findings）")
    L.append("")
    for f in diag["findings"]:
        L.append(f"- {f}")
    L.append("")

    L.append("## 7. 滞销菜品优化建议")
    L.append("")
    L.append("| 滞销菜品 | 累计销量 | 建议动作 | 说明 |")
    L.append("|----------|------:|------|------|")
    for d in diag["slow"]:
        action, note = _slow_advice(d, diag)
        L.append(f"| {d['dish']} | {d['qty']:.0f} | {action} | {note} |")
    L.append("")

    L.append("## 8. 菜单结构调整建议")
    L.append("")
    for s in _structure_advice(diag):
        L.append(f"- {s}")
    L.append("")

    L.append("---")
    L.append("")
    L.append("> **Disclaimer**：本报告基于所提供的历史销量数据，采用描述性统计（排名/趋势/占比/分布），"
             "不含成本与利润维度。若结合本 Skill 的「菜单工程定价模块」（补充食材成本/售价），可进一步输出"
             "波士顿矩阵分类与提价/下架的盈利级建议。决策前请结合门店实际经营情况。")
    L.append("")
    return "\n".join(L)


def _slow_advice(d, diag):
    share = d["share"]
    if share < 0.02:
        return ("下架 / 替换", "销量占比极低（<2%），长期占用菜单位与后厨产能，建议直接下架或以新菜替换。")
    if share < 0.05:
        return ("重做 or 重推", "销量偏低，先小批量测试改良（口味/份量/摆盘）或由服务员主推，观察 2 周无起色则下架。")
    return ("调位 / 组合", "销量中等偏下，建议调整至菜单黄金视线位或加入套餐组合，提升曝光与连带率。")


def _structure_advice(diag):
    out = []
    if diag["cat_list"] and diag["cat_list"][0]["share"] > 0.5:
        c = diag["cat_list"][0]
        out.append(f"**品类多元化**：{c['category']} 占比 {pct(c['share'])} 过高，结构偏单一；"
                   f"建议引入 1-2 道其他品类菜品分散风险并吸引更广客群。")
    if diag["rising"]:
        out.append(f"**培育上升款**：{('、'.join(t['dish'] for t in diag['rising'][:3]))} 呈上升趋势，"
                   f"建议加大曝光（菜单置顶/前厅主推/套餐绑定），转化为新招牌。")
    if diag["falling"]:
        out.append(f"**抢救下滑款**：{('、'.join(t['dish'] for t in diag['falling'][:3]))} 持续下滑，"
                   f"需排查季节/口味/竞品/陈列原因，必要时重做或下架回收产能。")
    if diag["peak_period"] and diag["peak_period"] != "全天":
        out.append(f"**时段运营**：高峰「{diag['peak_period']}」贡献 {pct(diag['period_list'][0]['share'])} 销量，"
                   f"建议在该时段强化备货、人员排班与前厅主推资源。")
    if diag["top"] and diag["top"][0]["share"] > 0.3:
        out.append(f"**降低依赖**：销量冠军「{diag['top'][0]['dish']}」占比 {pct(diag['top'][0]['share'])} 过高，"
                   f"存在单品依赖风险；可通过第二招牌分流，平滑业绩波动。")
    if not out:
        out.append("当前菜单销量结构较为均衡，无紧急结构性风险；维持现有节奏并持续监控趋势即可。")
    return out


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Menu Sales Analysis Engine")
    ap.add_argument("--input", help="CSV/JSON 文件路径；留空则从 stdin 读取")
    ap.add_argument("--json", help="将结构化结果写入该 JSON 路径")
    args = ap.parse_args()

    text = ""
    if args.input:
        if not os.path.exists(args.input):
            sys.stderr.write(f"输入文件不存在：{args.input}\n")
            sys.exit(2)
        with open(args.input, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    records, anomalies = parse_input(text)
    if anomalies:
        print("⚠️ 检测到异常数据，分析已终止，请先修正：\n")
        for a in anomalies:
            print(f"- {a}")
        print("\n提示：本引擎仅基于您提供的数据计算，不编造。必填字段：菜品、销量；"
              "可选：日期、品类、时段、销售额。")
        if args.json:
            with open(args.json, "w", encoding="utf-8") as f:
                json.dump({"ok": False, "anomalies": anomalies}, f, ensure_ascii=False, indent=2)
        sys.exit(0)

    diag = analyze(records)
    md = build_report(diag)
    print(md)

    if args.json:
        payload = {"ok": True, "diagnostics": diag}
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"\n[JSON 已写入: {args.json}]")


if __name__ == "__main__":
    main()
