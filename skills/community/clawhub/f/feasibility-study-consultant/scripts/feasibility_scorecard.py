#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""可行性门槛评分器（Feasibility Scorecard）

把"这个项目能不能做 / 值不值得做"从主观印象，变成**带权重、带门槛、带致命假设判定**的可复核结论。

用法：
    python3 feasibility_scorecard.py 立项评估.json
    python3 feasibility_scorecard.py 立项评估.json --json
    python3 feasibility_scorecard.py --demo          # 跑内置示例（可直接看输出长什么样）
    python3 feasibility_scorecard.py --print-schema  # 打印输入 JSON 的结构说明

退出码：
    0 = 可做（Go）或有条件可做（Conditional Go）
    1 = 不做（No-Go）—— 存在证伪的致命假设 / 关键维度大幅低于门槛 / 财务不达标
    2 = 用法或数据错误

依赖：仅 Python 3 标准库。

设计说明：
  · 评分只解决"多因素怎么比"，不能替代证据。每条打分都要挂证据等级（A/B/C/D）与来源。
  · 门槛（threshold）是**否决线**，不是加权项：一票不过就要在结论里说明。
  · 致命假设（must_be_true）优先于分数：任何一条被证伪，无论综合分多高都判 No-Go。
"""
import json
import sys

EVIDENCE_LEVELS = {
    "A": "A 官方/一手（政府文件、审计报告、企业台账、合同订单）",
    "B": "B 权威二手（行业年鉴、券商研报、协会统计、上市公司财报）",
    "C": "C 一般二手（媒体报道、第三方文章、公开访谈）",
    "D": "D 推断/假设（模型推算、类比估计，未验证）",
}


def _num(x, default=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def evaluate(cfg):
    dims = cfg.get("dimensions") or []
    if not dims:
        raise ValueError("dimensions 不能为空：至少给出一个评估维度")

    total_w = sum(_num(d.get("weight")) for d in dims) or 0.0
    rows, weighted, blockers, weak = [], 0.0, [], []

    for d in dims:
        name = d.get("name", "未命名维度")
        w = _num(d.get("weight"))
        wn = w / total_w if total_w else 0.0
        s = _num(d.get("score"))
        th = d.get("threshold")
        ev = (d.get("evidence") or "D").strip().upper()[:1]
        gap = (s - _num(th)) if th is not None else None
        passed = (gap is None) or (gap >= 0)
        weighted += wn * s
        rows.append({
            "维度": name, "权重": round(wn, 3), "得分": s,
            "门槛": None if th is None else _num(th),
            "是否过门槛": "—" if th is None else ("过" if passed else "不过"),
            "证据等级": ev, "证据": EVIDENCE_LEVELS.get(ev, ev),
            "备注": d.get("note", ""),
        })
        if th is not None and not passed:
            weak.append((name, wn, s, _num(th)))
            # 高权重维度不过门槛 = 硬阻塞
            if wn >= 0.15 or (_num(th) - s) >= 2:
                blockers.append(f"维度「{name}」{s:g} 分低于门槛 {_num(th):g}（权重 {wn:.0%}）")

    # 致命假设
    mbt = cfg.get("must_be_true") or []
    falsified = [a for a in mbt if (a.get("status") or "").lower() in ("falsified", "证伪", "已证伪", "否")]
    unverified = [a for a in mbt if (a.get("status") or "").lower() not in ("verified", "已验证", "已证", "是")]

    # 财务门槛
    fin = cfg.get("financial") or {}
    fin_issues = []
    if fin:
        if fin.get("irr") is not None and fin.get("benchmark") is not None:
            if _num(fin["irr"]) < _num(fin["benchmark"]):
                fin_issues.append(
                    f"全投资 IRR {_num(fin['irr']):.2%} < 基准 {_num(fin['benchmark']):.2%}")
        if fin.get("payback") is not None and fin.get("payback_max") is not None:
            if _num(fin["payback"]) > _num(fin["payback_max"]):
                fin_issues.append(
                    f"回收期 {_num(fin['payback']):g} 年 > 上限 {_num(fin['payback_max']):g} 年")
        if fin.get("unit_economics_positive") is False:
            fin_issues.append("单位经济模型为负（单个客户/单件产品越卖越亏）")
        if fin.get("npv") is not None and _num(fin["npv"]) <= 0:
            fin_issues.append(f"NPV {_num(fin['npv']):g} ≤ 0")
    blockers += fin_issues

    # 低证据等级提示
    low_ev = [r["维度"] for r in rows if r["证据等级"] in ("C", "D")]

    # 判定
    hard_block = bool(falsified) or bool(fin_issues)
    if hard_block:
        verdict, code = "No-Go（不做／需重大重构后再评）", 1
    elif blockers:
        verdict, code = "Conditional Go（有条件可做：先补齐阻塞项再决策）", 0
    elif weighted >= 7.0:
        verdict, code = "Go（可做）", 0
    elif weighted >= 5.5:
        verdict, code = "Conditional Go（有条件可做：可小步试、按验证计划推进）", 0
    else:
        verdict, code = "No-Go（综合评分不足）", 1

    return {
        "项目": cfg.get("project", "（未命名）"),
        "问题类型": cfg.get("question", "能不能做/值不值"),
        "维度明细": rows,
        "加权总分": round(weighted, 2),
        "阻塞项": blockers,
        "已证伪的致命假设": [a.get("assumption", "") for a in falsified],
        "尚未验证的致命假设": [a.get("assumption", "") for a in unverified if a not in falsified],
        "低证据等级维度": low_ev,
        "结论": verdict,
        "退出码": code,
    }


def render(res):
    L = []
    L.append("=" * 68)
    L.append(f"可行性门槛评分  {res['项目']}")
    L.append(f"待答问题：{res['问题类型']}")
    L.append("=" * 68)
    L.append("")
    L.append(f"{'维度':<14}{'权重':>7}{'得分':>7}{'门槛':>7}{'过门槛':>8}  证据")
    for r in res["维度明细"]:
        th = "-" if r["门槛"] is None else f"{r['门槛']:g}"
        L.append(f"{r['维度']:<14}{r['权重']:>6.0%}{r['得分']:>7g}{th:>7}{r['是否过门槛']:>9}  {r['证据等级']}")
    L.append("")
    L.append(f"加权总分：{res['加权总分']} / 10")
    if res["已证伪的致命假设"]:
        L.append("")
        L.append("❌ 已证伪的致命假设（优先于任何分数）：")
        for a in res["已证伪的致命假设"]:
            L.append(f"   · {a}")
    if res["阻塞项"]:
        L.append("")
        L.append("🚧 阻塞项（不补齐则不能判可做）：")
        for b in res["阻塞项"]:
            L.append(f"   · {b}")
    if res["尚未验证的致命假设"]:
        L.append("")
        L.append("❓ 尚未验证的致命假设（下一步必须验的就是这些）：")
        for a in res["尚未验证的致命假设"]:
            L.append(f"   · {a}")
    if res["低证据等级维度"]:
        L.append("")
        L.append("⚠️ 证据等级偏低（C/D）的维度，结论稳健性打折：" + "、".join(res["低证据等级维度"]))
    L.append("")
    L.append("-" * 68)
    L.append(f"结论：{res['结论']}")
    L.append("提示：本工具只做门槛与一致性检查，阈值是否合理、证据是否属实，仍需人来负责。")
    L.append("-" * 68)
    return "\n".join(L)


DEMO = {
    "project": "××片区冷链物流园（示例）",
    "question": "能不能做 + 值不值",
    "dimensions": [
        {"name": "市场容量", "weight": 0.20, "score": 7.5, "threshold": 6, "evidence": "B",
         "note": "自下而上：区域内生鲜产量×冷链流通率×第三方外包比例"},
        {"name": "竞争壁垒", "weight": 0.15, "score": 4.0, "threshold": 5, "evidence": "C",
         "note": "仅价格优势，无规模/网络效应"},
        {"name": "政策合规", "weight": 0.15, "score": 8.0, "threshold": 6, "evidence": "A",
         "note": "已列入省级物流规划；用地为物流仓储用地"},
        {"name": "单位经济", "weight": 0.20, "score": 6.5, "threshold": 6, "evidence": "C",
         "note": "单托毛利为正，但满库率假设 75% 未验证"},
        {"name": "执行能力", "weight": 0.10, "score": 6.0, "threshold": 5, "evidence": "B",
         "note": "团队有同类园区运营经验"},
        {"name": "财务回报", "weight": 0.20, "score": 6.8, "threshold": 6, "evidence": "D",
         "note": "三情景测算，基准情景 IRR 9.8%"}
    ],
    "must_be_true": [
        {"assumption": "3 家以上区域头部生鲜商签订入驻意向（锁定 60% 库容）", "status": "unverified"},
        {"assumption": "拿地成本不高于 45 万元/亩", "status": "verified"},
        {"assumption": "用电价格按工业电价执行", "status": "unverified"}
    ],
    "financial": {"irr": 0.098, "benchmark": 0.08, "npv": 4200, "payback": 8.5,
                  "payback_max": 9, "unit_economics_positive": True}
}

SCHEMA = """输入 JSON 结构（缺省字段会被宽容处理）：

{
  "project": "项目名称",
  "question": "能不能做 | 值不值 | 怎么做",
  "dimensions": [
    {"name": "维度名", "weight": 0.2, "score": 7.5, "threshold": 6,
     "evidence": "A|B|C|D", "note": "依据/口径"}
  ],
  "must_be_true": [
    {"assumption": "必须成立才敢做的前提", "status": "verified|unverified|falsified"}
  ],
  "financial": {
    "irr": 0.098, "benchmark": 0.08, "npv": 4200,
    "payback": 8.5, "payback_max": 9, "unit_economics_positive": true
  }
}

维度建议（可按项目裁剪，权重合计会自动归一化）：
  市场容量 / 竞争壁垒 / 政策合规 / 单位经济 / 执行能力 / 财务回报 / 供应链与要素 / 风险可控性
"""


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    flags = {a for a in argv if a.startswith("--")}

    if "--print-schema" in flags:
        print(SCHEMA)
        return 0

    if "--demo" in flags or not args:
        cfg = DEMO
    else:
        try:
            with open(args[0], encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception as e:  # noqa: BLE001
            print(f"读取配置文件失败：{e}", file=sys.stderr)
            return 2

    try:
        res = evaluate(cfg)
    except Exception as e:  # noqa: BLE001
        print(f"评估失败：{e}", file=sys.stderr)
        return 2

    if "--json" in flags:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(render(res))
    return res["退出码"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
