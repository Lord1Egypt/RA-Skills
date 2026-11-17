#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""置信度与交付闸门 —— 来源四档标注 + 分项置信度 + 是否允许交付。

借鉴高分 Skill 的可核验设计：每个数字必须带来源档位，交付末尾附分项置信度，
低于闸门阈值则拒绝交付（而不是硬着头皮出一份看着像样的报告）。

输入 JSON：
{
  "items": [                      # 关键数据/结论清单
    {"name": "客单价", "source": "S1", "note": "生意参谋导出"},
    {"name": "类目均价", "source": "S3", "note": "公开榜单"},
    {"name": "目标毛利", "source": "S4", "note": "无数据时推算"}
  ],
  "checks": {                      # 可选，各项校验结果 true/false
    "data_complete": true,
    "caliber_consistent": true,
    "recomputable": true,
    "conclusion_robust": false
  },
  "gate_min": 60                   # 可选，默认 60
}

来源四档（S1–S4）：
  S1 平台后台 / 用户导出原始数据（可核验）
  S2 单方可信来源（如客户口述、单一第三方工具）
  S3 公开可检索来源（榜单/公开数据，需注明出处与日期）
  S4 模型推算 / 行业经验值（未经核验，必须显式标注）

用法：
  python confidence.py --data c.json            # 人类可读
  python confidence.py --data c.json --json     # 机器可读
  python confidence.py --demo
  python confidence.py --self-test
退出码：0 允许交付 / 1 拒绝交付（低于闸门）/ 2 输入错误
"""
import argparse
import json
import os
import sys

SOURCE_TIERS = {
    "S1": ("平台原始数据", 100, "平台后台 / 用户导出原始数据，可核验"),
    "S2": ("单方来源", 70, "单一可信来源（口述/单方提供），需交叉验证"),
    "S3": ("公开来源", 55, "公开可检索来源，须注明出处与抓取日期"),
    "S4": ("推算值", 20, "模型推算 / 经验值，未经核验，必须显式标注"),
}

DIMENSIONS = [
    ("data_complete", "数据完整性", 30, "关键字段是否齐全，无空缺"),
    ("caliber_consistent", "口径一致性", 25, "同一指标是否同源同口径（ROAS/ROI 不得混用来源）"),
    ("recomputable", "计算可复现", 25, "数值是否由本 Skill 脚本产出、可被复算"),
    ("conclusion_robust", "结论稳健性", 20, "结论是否由 >=2 条独立证据支撑，非单点推测"),
]

DEFAULT_GATE = 60


def score_items(items):
    """统计来源分布，返回分布与加权来源分。"""
    dist = {k: 0 for k in SOURCE_TIERS}
    unknown = []
    for it in items:
        src = str(it.get("source", "")).upper().strip()
        if src in SOURCE_TIERS:
            dist[src] += 1
        else:
            unknown.append(it.get("name", "?"))
    total = len(items)
    # 不允许出现未分档的数据 -> 视为 S4 并计入 unknown 提示
    eff = dict(dist)
    if unknown:
        eff["S4"] = eff.get("S4", 0) + len(unknown)
    wsum = sum(eff[k] * SOURCE_TIERS[k][1] for k in eff)
    source_score = wsum / float(total) if total else 0.0
    return {"total": total, "distribution": dist, "ungraded": unknown,
            "source_score": round(source_score, 1)}


def score_dims(checks, item_sc):
    """分项置信度打分：四项独立维度 + 来源质量作为结论稳健性的修正。"""
    got = {}
    total = 0.0
    earned = 0.0
    for key, label, weight, desc in DIMENSIONS:
        w = float(weight)
        total += w
        v = checks.get(key)
        if v is None:
            got[key] = {"label": label, "weight": weight, "score": None,
                        "desc": desc, "note": "未校验"}
            continue
        s = 100.0 if v else 0.0
        got[key] = {"label": label, "weight": weight, "score": s,
                    "desc": desc, "note": "通过" if v else "未通过"}
        earned += w * (s / 100.0)
    base = round(earned / total * 100, 1) if total else 0.0
    return {"dimensions": got, "base_score": base}


def assess(data):
    items = data.get("items") or []
    checks = data.get("checks") or {}
    gate = data.get("gate_min", DEFAULT_GATE)
    try:
        gate = float(gate)
    except (TypeError, ValueError):
        gate = DEFAULT_GATE

    si = score_items(items)
    sd = score_dims(checks, si["source_score"])

    # 来源质量直接折损结论：S4 占比越高，整体置信度越低
    penalty = 0.0
    if si["total"]:
        s4_ratio = si["distribution"].get("S4", 0) / float(si["total"])
        penalty = round(s4_ratio * 30, 1)
    final = round(max(0.0, sd["base_score"] - penalty), 1)

    ungraded = si["ungraded"]
    passed = final >= gate and not ungraded
    reasons = []
    if final < gate:
        reasons.append("综合置信度 %.1f 低于闸门 %.1f" % (final, gate))
    if ungraded:
        reasons.append("存在未标来源档位的数据：%s" % "、".join(ungraded[:5]))

    return {
        "sources": si,
        "confidence": {
            "dimensions": sd["dimensions"],
            "base_score": sd["base_score"],
            "s4_penalty": penalty,
            "final_score": final,
        },
        "gate": {"min": gate, "passed": passed,
                 "reasons": reasons or ["满足交付闸门"],
                 "verdict": "允许交付" if passed else "拒绝交付（须补齐数据或降档说明）"},
    }


def render(r):
    o = []
    si = r["sources"]
    o.append("【数据来源分档】(S1 原始 > S2 单方 > S3 公开 > S4 推算)")
    o.append("  数据条数 = %d  加权来源分 = %.1f" % (si["total"], si["source_score"]))
    for k in ("S1", "S2", "S3", "S4"):
        if si["distribution"].get(k):
            o.append("  %s %s: %d 条" % (k, SOURCE_TIERS[k][0], si["distribution"][k]))
    if si["ungraded"]:
        o.append("  [S4-兜底] 未标档位 %d 条：%s" % (
            len(si["ungraded"]), "、".join(si["ungraded"][:5])))

    c = r["confidence"]
    o.append("")
    o.append("【分项置信度】")
    for key, label, weight, desc in DIMENSIONS:
        d = c["dimensions"][key]
        sv = "未校验" if d["score"] is None else "%.0f" % d["score"]
        o.append("  %-6s 权重%2d  得分 %-6s  %s" % (label, weight, sv, d["note"]))
    o.append("  基础分 = %.1f  -  S4折损 %.1f  =  综合置信度 %.1f"
             % (c["base_score"], c["s4_penalty"], c["final_score"]))

    g = r["gate"]
    o.append("")
    o.append("【交付闸门】阈值 %.1f -> %s" % (g["min"], g["verdict"]))
    for x in g["reasons"]:
        o.append("  - %s" % x)
    return "\n".join(o)


DEMO = {
    "items": [
        {"name": "支付金额", "source": "S1"},
        {"name": "退款金额", "source": "S1"},
        {"name": "广告花费", "source": "S1"},
        {"name": "竞品价格", "source": "S3"},
        {"name": "类目平均转化率", "source": "S4"},
    ],
    "checks": {"data_complete": True, "caliber_consistent": True,
               "recomputable": True, "conclusion_robust": False},
    "gate_min": 60,
}


def main():
    ap = argparse.ArgumentParser(description="来源四档标注 + 分项置信度 + 交付闸门")
    ap.add_argument("--data", help="输入 JSON 路径")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if a.demo:
        data = DEMO
    elif a.data:
        if not os.path.isfile(a.data):
            sys.stderr.write("输入文件不存在: %s\n" % a.data)
            return 2
        with open(a.data, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception as e:
                sys.stderr.write("JSON 解析失败: %s\n" % e)
                return 2
    else:
        sys.stderr.write("需要 --data / --demo / --self-test 之一\n")
        return 2

    r = assess(data)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(render(r))
    return 0 if r["gate"]["passed"] else 1


def self_test():
    ok = True

    def chk(name, got, exp, tol=1e-6):
        nonlocal ok
        good = (abs(got - exp) < tol) if isinstance(exp, float) else (got == exp)
        print("[%s] %s (got=%s exp=%s)" % ("PASS" if good else "FAIL", name, got, exp))
        if not good:
            ok = False

    # 全 S1 且四项校验通过 -> 100 分，放行
    r = assess({"items": [{"name": "a", "source": "S1"}, {"name": "b", "source": "S1"}],
                "checks": {k: True for k, _, _, _ in DIMENSIONS}})
    chk("全 S1 满分", r["confidence"]["final_score"], 100.0, 0.05)
    chk("全 S1 放行", r["gate"]["passed"], True)

    # 全 S4 且有未通过项 -> 低分，拒绝
    r2 = assess({"items": [{"name": "x", "source": "S4"}],
                 "checks": {"data_complete": False, "caliber_consistent": False,
                            "recomputable": False, "conclusion_robust": False}})
    chk("全 S4 低分", r2["confidence"]["final_score"] < 30, True)
    chk("全 S4 拒绝", r2["gate"]["passed"], False)

    # 未标档位 -> 计入 S4 兜底并拒绝交付
    r3 = assess({"items": [{"name": "y"}],
                 "checks": {k: True for k, _, _, _ in DIMENSIONS}})
    chk("未标档位计入 S4", r3["sources"]["distribution"]["S4"], 0)
    chk("未标档位被拦", r3["gate"]["passed"], False)
    chk("未标档位计数", len(r3["sources"]["ungraded"]), 1)

    # 来源分布与来源分
    r4 = assess({"items": [{"name": "a", "source": "S1"}, {"name": "b", "source": "S4"}],
                 "checks": {}})
    chk("S1 计数", r4["sources"]["distribution"]["S1"], 1)
    chk("S4 计数", r4["sources"]["distribution"]["S4"], 1)
    # (100 + 20) / 2 = 60
    chk("加权来源分", r4["sources"]["source_score"], 60.0, 0.05)
    chk("未校验时基础分为 0", r4["confidence"]["base_score"], 0.0, 0.05)

    print("\n自测：%s" % ("全部通过" if ok else "存在失败"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
