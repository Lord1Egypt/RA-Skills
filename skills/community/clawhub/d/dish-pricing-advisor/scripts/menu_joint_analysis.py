#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Menu Joint Analysis Engine（销量×利润联合看板）
=============================================
同一份数据，既出「销量排名 / 畅销滞销」，又出「BCG 利润分类」，
并叠加「销量×利润联合洞察」——专门解决「仅凭销量误杀高毛利慢销菜（金牛）」
以及「把高销低利的问题菜（Puzzle）当英雄菜」这两类坑。

输入（两种模式）：
  A. 统一 JSON（推荐）：每道菜同时含定价字段 + sales 时序数组
     {
       "period": "2026-07",
       "store_info": {...},
       "format": "正餐",                 # 可选：快餐 / 正餐 / 茶饮
       "dishes": [
         {
           "name": "秘制炖蹄花",
           "category": "主菜",
           "raw_cost": 10, "seasoning_cost": 1, "labor_apportionment": 2,
           "price": 38, "return_rate": 0, "is_signature": false,
           "sales": [                       # 销量时序（驱动销量维度 + 利润销量）
             {"date": "2026-07-01", "period": "午市", "quantity": 5, "revenue": 190},
             {"date": "2026-07-01", "period": "晚市", "quantity": 8, "revenue": 304},
             ...
           ]
         }
       ]
     }
  B. 双文件：--sales sales.csv --pricing pricing.json
     sales.csv   ：日期,菜品,品类,时段,销量[,销售额]（菜单销量分析口径）
     pricing.json：标准 Menu Engineering JSON（含 dishes[] 定价字段）

输出：
  - 第一部分：利润 / BCG 诊断报告（复用 menu_engineering）
  - 第二部分：销量分析报告（复用 menu_sales_analysis）
  - 第三部分：销量×利润联合洞察（交叉矩阵 + 金牛勿误杀预警 + 高销低利预警）

依赖：复用同目录 menu_engineering.py / menu_sales_analysis.py（仅标准库）。
用法：
  python menu_joint_analysis.py --input joint.json
  python menu_joint_analysis.py --sales sales.csv --pricing pricing.json --format 正餐
  cat joint.json | python menu_joint_analysis.py
"""

import sys
import io
import os
import re
import json
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

# 复用同目录引擎
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import menu_engineering as me
import menu_sales_analysis as sa

CATEGORY_CN = {
    "star": "明星 Star",
    "puzzle": "问题 Puzzle",
    "cash_cow": "金牛 Cow",
    "dog": "瘦狗 Dog",
}


# ---------------------------------------------------------------------------
# 解析：统一 JSON
# ---------------------------------------------------------------------------
def parse_unified(text):
    """返回 (dishes_pricing, sales_records, meta, anomalies)。

    dishes_pricing：menu_engineering.analyze 所需的菜品列表（含 sales_volume / net_volume）。
    sales_records ：menu_sales_analysis.analyze 所需的销量记录。
    """
    try:
        obj = json.loads(text)
    except Exception as e:
        return [], [], {}, [f"JSON 解析失败：{e}。请检查括号/引号是否完整。"]

    dishes_raw = obj.get("dishes") if isinstance(obj, dict) else obj
    if not isinstance(dishes_raw, list) or not dishes_raw:
        return [], [], {}, ["dishes 字段缺失或为空，请提供至少一道菜的数组。"]

    meta = {
        "period": (obj.get("period") if isinstance(obj, dict) else None) or "未指定",
        "store_info": (obj.get("store_info") if isinstance(obj, dict) else None) or {},
        "format": None,
    }
    if isinstance(obj, dict):
        fmt = obj.get("format") or (obj.get("store_info") or {}).get("format")
        if isinstance(fmt, str) and fmt.strip():
            meta["format"] = fmt.strip()

    pricing, records, anomalies = [], [], []
    for i, d in enumerate(dishes_raw):
        name = d.get("name") or f"菜品{i+1}"
        raw = d.get("raw_cost")
        seasoning = d.get("seasoning_cost", 0) or 0
        labor = d.get("labor_apportionment", 0) or 0
        price = d.get("price")
        ret = d.get("return_rate", 0) or 0
        is_sig = bool(d.get("is_signature", False))
        cat = d.get("category", "")
        sales = d.get("sales") or []

        # 定价校验
        if raw is None or price is None:
            anomalies.append(f"「{name}」缺少必填定价字段（raw_cost / price），请补全。")
            continue
        try:
            raw = float(raw); seasoning = float(seasoning); labor = float(labor)
            price = float(price); ret = float(ret)
        except Exception:
            anomalies.append(f"「{name}」存在非数字定价字段，请检查 raw_cost/price/return_rate。")
            continue
        if price <= 0:
            anomalies.append(f"「{name}」售价须为正数（price={price}）。")
            continue
        if not (0 <= ret < 1):
            anomalies.append(f"「{name}」return_rate 须在 [0,1) 区间（当前 {ret}）。")
            continue
        total_cost = raw + seasoning + labor
        if total_cost >= price:
            anomalies.append(
                f"「{name}」合计成本({total_cost:.2f}) ≥ 售价({price:.2f})，"
                f"毛利为零或为负，请修正成本或售价后再分析。"
            )
            continue

        # 销量时序 → 总销量（驱动利润聚合）+ 销量记录（驱动销量维度）
        total_qty = 0.0
        if not isinstance(sales, list):
            anomalies.append(f"「{name}」的 sales 字段须为数组。")
            continue
        for s in sales:
            if not isinstance(s, dict):
                continue
            q_raw = s.get("quantity") or s.get("qty") or s.get("销量")
            q = me._clean_num(q_raw) if q_raw is not None else None
            if q is None or q < 0:
                continue
            total_qty += q
            rev_raw = s.get("revenue") or s.get("销售额")
            rev = me._clean_num(rev_raw) if rev_raw is not None else None
            dt = sa._parse_date(s.get("date") or s.get("日期"))
            records.append({
                "date": dt,
                "date_raw": str(s.get("date") or s.get("日期") or ""),
                "dish": str(name),
                "category": str(s.get("category") or cat or "未分类"),
                "period": str(s.get("period") or s.get("时段") or "全天"),
                "quantity": q,
                "revenue": rev,
            })

        pricing.append({
            "name": name,
            "category": cat,
            "raw_cost": round(raw, 2),
            "seasoning_cost": round(seasoning, 2),
            "labor_apportionment": round(labor, 2),
            "price": round(price, 2),
            "sales_volume": int(round(total_qty)),
            "return_rate": round(ret, 4),
            "is_signature": is_sig,
            "net_volume": int(round(total_qty * (1 - ret))),
        })

    if not pricing:
        anomalies.append("没有可用的合法菜品数据，请检查后重新提交。")
    return pricing, records, meta, anomalies


# ---------------------------------------------------------------------------
# 解析：双文件（sales.csv + pricing.json）
# ---------------------------------------------------------------------------
def parse_two_file(sales_text, pricing_text, fmt_override):
    pricing, meta_p, anomalies = me.parse_json(pricing_text)
    # parse_json 已做定价校验；其 sales_volume 取 JSON 自带值（可能与销量表不同期）
    records, sales_anom = sa.parse_input(sales_text)
    anomalies.extend(sales_anom)
    meta = {
        "period": meta_p.get("period", "未指定"),
        "store_info": meta_p.get("store_info", {}),
        "format": meta_p.get("format") or fmt_override,
    }
    return pricing, records, meta, anomalies


# ---------------------------------------------------------------------------
# 联合洞察
# ---------------------------------------------------------------------------
def build_joint_insight(dishes, diag, sdiag):
    """菜品销量排名 × BCG 利润象限交叉分析。"""
    # 销量排名映射：菜名 -> (rank, share, qty, avg_day)
    rank_map = {}
    for i, d in enumerate(sdiag.get("ranked", []), 1):
        rank_map[d["dish"]] = {
            "rank": i, "share": d["share"], "qty": d["qty"], "avg_day": d["avg_day"],
        }
    # 趋势映射
    trend_map = {}
    for t in sdiag.get("rising", []):
        trend_map[t["dish"]] = f"+{t['change']*100:.0f}% ↑"
    for t in sdiag.get("falling", []):
        trend_map[t["dish"]] = f"{t['change']*100:.0f}% ↓"

    rows = []
    for d in dishes:
        rk = rank_map.get(d["name"])
        rank = rk["rank"] if rk else "—"
        share = rk["share"] if rk else 0.0
        qty = rk["qty"] if rk else 0.0
        trend = trend_map.get(d["name"], "—")
        key = d["category_key"]
        # 联合判定
        if key == "star":
            verdict = "双优 · 放大"
            action = "金三角置顶 + 前厅主推，最大化利润捕获"
        elif key == "cash_cow":
            verdict = "金牛 · 勿误杀"
            action = "价值话术 + 黄金视线位主推；销量低≠该下架，它是利润引擎"
        elif key == "puzzle":
            verdict = "高销低利 · 提利"
            action = (d.get("recommend", {}).get("action", "Price +10% / 成本重构")
                      + "；勿仅看销量当英雄菜，悄悄漏利润")
        else:  # dog
            verdict = "双弱 · 裁剪"
            action = "下架 / 重做，回收菜单位与后厨产能"
        rows.append({
            "name": d["name"], "rank": rank, "share": share, "qty": qty,
            "trend": trend, "key": key, "category_cn": d["category_cn"],
            "cm": d["cm"], "cm_mix": d.get("cm_mix", 0.0), "sales_mix": d.get("sales_mix", 0.0),
            "verdict": verdict, "action": action,
        })

    # 预警分组
    cows = [r for r in rows if r["key"] == "cash_cow"]
    puzzles = [r for r in rows if r["key"] == "puzzle"]
    dogs = [r for r in rows if r["key"] == "dog"]
    stars = [r for r in rows if r["key"] == "star"]

    L = []
    L.append("## 第三部分：销量 × 利润联合洞察（Joint Insight）")
    L.append("")
    L.append("> 本部分将「销量维度」与「利润维度」叠加，避免两个经典误判：")
    L.append("> ① 仅凭销量低就下架高毛利慢销菜（金牛）——实为利润引擎；")
    L.append("> ② 仅凭销量高就把低利问题菜（Puzzle）当招牌——实为悄悄漏利润。")
    L.append("")

    # 交叉矩阵
    L.append("### 3.1 销量排名 × BCG 利润象限 交叉矩阵")
    L.append("")
    L.append("| 菜品 | 销量排名 | 销量占比 | 利润象限 | 联合判定 | 趋势 | 建议行动 |")
    L.append("|------|------:|------:|------|------|------|------|")
    for r in sorted(rows, key=lambda x: (x["key"] != "star", x["key"] != "cash_cow",
                                         x["key"] != "puzzle", x["key"] != "dog",
                                         -(x["share"] or 0))):
        share_s = f"{r['share']*100:.1f}%" if isinstance(r["share"], (int, float)) else "—"
        L.append(f"| {r['name']} | {r['rank']} | {share_s} | {r['category_cn']} "
                 f"| **{r['verdict']}** | {r['trend']} | {r['action']} |")
    L.append("")

    # 金牛勿误杀预警
    L.append("### 3.2 ⚠️ 金牛勿误杀预警（高毛利 · 低销量）")
    L.append("")
    if cows:
        L.append("以下菜品在「销量分析」口径下会被判为慢销/滞销，但若仅据此下架，"
                 "将直接砍掉菜单主要利润来源。它们盈利性高（CM 高于均值），只是曝光/点选不足——"
                 "正确动作是**价值推销 + 黄金位主推**，而非下架：")
        L.append("")
        L.append("| 菜品 | 销量排名 | 销量占比 | 单位CM(元) | 贡献毛利占比 | 处置建议 |")
        L.append("|------|------:|------:|------:|------:|------|")
        for r in cows:
            L.append(f"| {r['name']} | {r['rank']} | {r['share']*100:.1f}% | {r['cm']:.2f} "
                     f"| {r['cm_mix']*100:.1f}% | 保留 + 主推（价值话术/套餐绑定） |")
        L.append("")
    else:
        L.append("当前无金牛类菜品（低销量·高毛利）。")
        L.append("")

    # 高销低利预警
    L.append("### 3.3 ⚠️ 高销低利预警（高销量 · 低利润 = Puzzle）")
    L.append("")
    if puzzles:
        L.append("以下菜品在「销量分析」口径下会被捧为畅销英雄，但其贡献毛利偏低（CM 低于均值），"
                 "高销量反而放大了利润泄漏。正确动作是**提价测试或成本重构**，而非一味加推走量：")
        L.append("")
        L.append("| 菜品 | 销量排名 | 销量占比 | 利润象限 | 推荐动作 |")
        L.append("|------|------:|------:|------|------|")
        for r in puzzles:
            L.append(f"| {r['name']} | {r['rank']} | {r['share']*100:.1f}% | {r['category_cn']} "
                     f"| {r['action']} |")
        L.append("")
    else:
        L.append("当前无问题类菜品（高销量·低利润）。")
        L.append("")

    # 联合行动优先级
    L.append("### 3.4 联合行动优先级（Joint Action Priority）")
    L.append("")
    if stars:
        L.append(f"1. **放大明星**：{('、'.join(r['name'] for r in stars))} 双优，"
                 f"置于菜单金三角并前厅主推，巩固利润基本盘。")
    if puzzles:
        L.append(f"2. **抢救问题菜利润**：{('、'.join(r['name'] for r in puzzles))} 走量但漏利，"
                 f"按利润侧敏感度结论执行提价/成本重构，把‘引流款’转‘利润款’。")
    if cows:
        L.append(f"3. **激活金牛**：{('、'.join(r['name'] for r in cows))} 利润厚但曝光不足，"
                 f"上价值话术 + 黄金视线位，严禁因销量低而下架。")
    if dogs:
        L.append(f"4. **裁剪瘦狗**：{('、'.join(r['name'] for r in dogs))} 双弱，"
                 f"下架或重做，回收产能。")
    if not (stars or puzzles or cows or dogs):
        L.append("当前无显著联合风险项。")
    L.append("")

    L.append("---")
    L.append("")
    L.append("> **Disclaimer**：联合看板基于同一份历史数据同时计算销量维度（描述统计）与利润维度"
             f"（BCG / 菜单工程 / 价格弹性系数 {diag.get('bench', {}).get('elasticity', '-')}）。"
             "结论为诊断级建议，落地前请结合门店实际与财务总监（CMA/CFO）复核。")
    L.append("")
    return "\n".join(L), rows


def _downgrade(md, by=1):
    """将所有 Markdown 标题级别整体下调 by 级，便于嵌套进联合报告。"""
    out = []
    for line in md.splitlines():
        m = re.match(r"^(#{1,6})\s", line)
        if m:
            hashes = m.group(1)
            new = "#" * min(6, len(hashes) + by)
            line = new + line[len(hashes):]
        out.append(line)
    return "\n".join(out)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Menu Joint Analysis Engine（销量×利润联合看板）")
    ap.add_argument("--input", help="统一 JSON 文件路径（菜含 sales 时序）；留空则从 stdin 读取")
    ap.add_argument("--sales", help="销量数据文件（CSV/JSON），与 --pricing 配套使用")
    ap.add_argument("--pricing", help="定价 JSON 文件，与 --sales 配套使用")
    ap.add_argument("--format", help="业态基准：快餐 / 正餐 / 茶饮（覆盖输入中的 format 字段）")
    ap.add_argument("--json", help="将结构化结果写入该 JSON 路径")
    ap.add_argument("--md", help="将完整 Markdown 联合报告写入该文件路径")
    args = ap.parse_args()

    # 读取输入
    if args.sales and args.pricing:
        if not os.path.exists(args.sales) or not os.path.exists(args.pricing):
            sys.stderr.write("双文件模式下 --sales 与 --pricing 均须存在。\n")
            sys.exit(2)
        with open(args.sales, "r", encoding="utf-8") as f:
            sales_text = f.read()
        with open(args.pricing, "r", encoding="utf-8") as f:
            pricing_text = f.read()
        pricing, records, meta, anomalies = parse_two_file(sales_text, pricing_text, args.format)
    else:
        text = ""
        if args.input:
            if not os.path.exists(args.input):
                sys.stderr.write(f"输入文件不存在：{args.input}\n")
                sys.exit(2)
            with open(args.input, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            text = sys.stdin.read()
        if not text.strip():
            sys.stderr.write("未读取到任何输入数据。\n")
            sys.exit(2)
        pricing, records, meta, anomalies = parse_unified(text)

    # 业态基准（CLI > JSON format > 通用默认）
    eff_format = args.format or meta.get("format")
    bench = me.get_bench(eff_format)

    if anomalies:
        print("⚠️ 检测到异常数据，分析已终止，请先修正：\n")
        for a in anomalies:
            print(f"- {a}")
        print("\n提示：统一 JSON 模式下每道菜需含 raw_cost/price，并可附 sales[] 时序；"
              "成本(合计)须小于售价。")
        if args.json:
            with open(args.json, "w", encoding="utf-8") as f:
                json.dump({"ok": False, "anomalies": anomalies}, f, ensure_ascii=False, indent=2)
        sys.exit(0)

    # 利润维度
    dishes, diag = me.analyze(pricing, meta, bench)
    profit_md = _downgrade(me.build_report(dishes, diag, meta, bench), 1)

    # 销量维度
    has_sales = len(records) > 0
    if has_sales:
        sdiag = sa.analyze(records)
        sales_md = _downgrade(sa.build_report(sdiag), 1)
    else:
        sdiag = None
        sales_md = "_（未提供销量时序数据，跳过销量维度分析；可在统一 JSON 的 sales[] 中补充。）_"

    # 联合洞察
    if has_sales:
        joint_md, rows = build_joint_insight(dishes, diag, sdiag)
    else:
        joint_md = "_（无销量数据，无法生成联合洞察。）_"
        rows = []

    # 组装报告
    report = []
    report.append("# 菜单销量 × 利润联合诊断报告（Menu Joint Analysis）")
    report.append("")
    report.append(f"> 适用业态基准：**{bench['label']}**　|　分析周期：{meta.get('period','未指定')}　|　"
                 f"菜品数：{diag['n']} 道")
    report.append("")
    report.append("## 第一部分：利润 / BCG 诊断（菜单工程）")
    report.append("")
    report.append(profit_md)
    report.append("")
    report.append("## 第二部分：销量数据分析（菜单销量）")
    report.append("")
    report.append(sales_md)
    report.append("")
    report.append(joint_md)

    full = "\n".join(report)
    print(full)

    if args.md:
        with open(args.md, "w", encoding="utf-8") as f:
            f.write(full)
        print(f"\n[Markdown 已写入: {args.md}]")
    if args.json:
        payload = {
            "ok": True,
            "meta": meta,
            "benchmarks": {
                "format": bench["format"], "label": bench["label"],
                "gm_low": bench["gm_low"], "gm_high": bench["gm_high"],
                "ptr_target": bench["ptr_target"], "elasticity": bench["elasticity"],
                "rationale": bench["rationale"],
            },
            "dishes": dishes,
            "profit_diagnostics": diag,
            "sales_diagnostics": sdiag,
            "joint_rows": rows,
        }
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        print(f"[JSON 已写入: {args.json}]")


if __name__ == "__main__":
    main()
