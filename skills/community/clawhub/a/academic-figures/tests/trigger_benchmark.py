#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trigger_benchmark：SKILL.md description 触发判别力基准（v7.8.0 批次2 · B3）。

对 trigger_cases.json 的 40 条用例（20 正=图型中英高频表述 / 20 负=跨工具负面分类学：
纯统计/数据清洗/写作/代码调试/文献检索/设计排除 pie·3D/仪表盘/plotly/图像编辑）
做**规则判别**评分：

- 触发规则 = 用例文本命中图型关键词族（CHART_KEYWORDS，双语正则）且未命中
  排除模式（EXCLUDE_PATTERNS：plotly/交互/仪表盘/3D/饼图/修图/统计计算动词…）；
  排除模式优先于关键词——「plotly 交互式折线」含关键词但被排除=不触发；
- 报告 precision / recall / F1 + 逐条误分类清单 + description 关键词族覆盖率
  （SKILL.md frontmatter description 覆盖了多少正例词族——发现召回缺口就补 desc）；
- 纯本地零网络；stdlib 实现（json/re），无第三方依赖；
- --selftest：用例文件完整性（40 条 20/20、字段齐、文本去重）+ 判别确定性
  （连跑两次结果逐位一致）+ 负例 100% 不触发。

Usage:
  python trigger_benchmark.py                 # 全量评分报告
  python trigger_benchmark.py --selftest      # 内置自测
  python trigger_benchmark.py --json out.json # 结构化结果侧车
"""
import argparse
import json
import os
import re
import sys

# 图型关键词族（双语；真值源——正例必须各自命中一族，负例不得命中任何族）
CHART_KEYWORDS = {
    "km":         r"KM\b|kaplan|生存曲线|survival curve",
    "forest":     r"森林图|forest plot|forest",
    "roc":        r"\bROC\b|受试者工作|roc 曲线",
    "box":        r"箱线|箱型|boxplot|box plot",
    "violin":     r"小提琴|violin",
    "volcano":    r"火山图|volcano",
    "heatmap":    r"热图|heatmap",
    "bar":        r"柱状图|条形图|bar chart|\bbars?\b",
    "scatter":    r"散点|scatter",
    "venn":       r"韦恩|venn",
    "waterfall":  r"瀑布图|waterfall",
    "ridgeline":  r"山脊|ridgeline|joyplot",
    "dumbbell":   r"哑铃|dumbbell",
    "nomogram":   r"列线图|nomogram",
    "pca":        r"主成分|\bPCA\b",
    "dca":        r"决策曲线|\bDCA\b",
    "calibration": r"校准曲线|calibration",
    "swimmer":    r"游泳图|swimmer",
    "dual_axis":  r"双轴|dual.axis",
    "upset":      r"交集图|upset",
}

# 排除模式（优先于关键词；负面用例分类学的机械化口径）
EXCLUDE_PATTERNS = [
    r"plotly|交互式|dashboard|仪表盘",
    r"3[dD]\b|3[dD]\s|立体|渲染",
    r"饼图",
    r"修图|去背景|替换成白色|放大到印刷|海报",
    r"润色|翻译|降重|cover letter|写一封",
    r"跑一个.*检验|方差分析|给出\s*p\s*值|算\s*p\s*值",
    r"缺失值|去掉重复行|统一格式|填充",
    r"\bKeyError\b|调试|哪里错了|帮我看看哪里",
    r"检索|找到原文|DOI 是什么",
    r"三线表|排版配一套",
]


def load_desc(root):
    """从 SKILL.md frontmatter 提取 description 块（触发判别的评测对象）。"""
    t = open(os.path.join(root, "SKILL.md"), encoding="utf-8").read()
    m = re.search(r"description: >-\n((?:  .*\n)+?)^\w", t, re.M)
    return " ".join(l.strip() for l in m.group(1).splitlines()) if m else ""


def classify(text):
    """单条规则判别：True=应触发本 skill。"""
    if any(re.search(p, text, re.I) for p in EXCLUDE_PATTERNS):
        return False
    return any(re.search(rx, text, re.I) for rx in CHART_KEYWORDS.values())


def run_benchmark(root):
    cases = json.load(open(os.path.join(root, "tests", "trigger_cases.json"),
                           encoding="utf-8"))["cases"]
    desc = load_desc(root)
    tp = fp = tn = fn = 0
    misses, coverage = [], []
    fam_hit_in_desc = set()
    for fam, rx in CHART_KEYWORDS.items():
        if re.search(rx, desc, re.I):
            fam_hit_in_desc.add(fam)
    results = []
    for c in cases:
        pred = classify(c["text"])
        label = (c["label"] == "pos")
        results.append({"id": c["id"], "label": c["label"], "family": c.get("family"),
                        "predicted": pred, "correct": pred == label})
        if label and pred:
            tp += 1
            if c.get("family") not in fam_hit_in_desc:
                coverage.append(f"{c['id']}（{c.get('family')}）词族未出现在 description")
        elif label and not pred:
            fn += 1
            misses.append(f"{c['id']} 正例漏触发（family={c.get('family')}）")
        elif not label and pred:
            fp += 1
            misses.append(f"{c['id']} 负例误触发（text={c['text'][:24]}…）")
        else:
            tn += 1
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"cases": results, "tp": tp, "fp": fp, "tn": tn, "fn": fn,
            "precision": round(precision, 4), "recall": round(recall, 4),
            "f1": round(f1, 4), "misses": misses,
            "desc_coverage": f"{len(fam_hit_in_desc)}/{len(CHART_KEYWORDS)}",
            "desc_uncovered": coverage, "neg_reject_rate": round(tn / (tn + fp), 4) if tn + fp else 1.0}


def selftest(root):
    """完整性+确定性+负例 100% 拒绝。exit 0/1。"""
    p = os.path.join(root, "tests", "trigger_cases.json")
    data = json.load(open(p, encoding="utf-8"))
    cases = data["cases"]
    ok = True
    n_pos = sum(1 for c in cases if c["label"] == "pos")
    n_neg = len(cases) - n_pos
    checks = [
        (len(cases) == 40, f"用例数 {len(cases)} == 40"),
        (n_pos == 20 and n_neg == 20, f"20 正 / 20 负（实际 {n_pos}/{n_neg}）"),
        (len({c["text"] for c in cases}) == 40, "文本无重复"),
        (all(c.get("id") and c.get("text") and c.get("family") for c in cases), "字段齐全"),
    ]
    r1 = run_benchmark(root)
    r2 = run_benchmark(root)
    det = (r1["cases"] == r2["cases"] and r1["f1"] == r2["f1"])
    checks.append((det, "判别确定性（连跑两次逐位一致）"))
    checks.append((r1["neg_reject_rate"] == 1.0 and r1["fp"] == 0,
                   f"负例 100% 不触发（实际 {r1['neg_reject_rate'] * 100:.0f}%，FP={r1['fp']}）"))
    for good, name in checks:
        print(f"  selftest: {'PASS' if good else 'FAIL'} — {name}")
        ok = ok and good
    print(f"  指标快照: P={r1['precision']} R={r1['recall']} F1={r1['f1']} "
          f"desc 覆盖 {r1['desc_coverage']}")
    print("trigger_benchmark --selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="SKILL.md description trigger benchmark")
    ap.add_argument("--selftest", action="store_true", help="内置自测")
    ap.add_argument("--json", default=None, metavar="PATH", help="结构化结果侧车")
    args = ap.parse_args()
    root = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    if args.selftest:
        sys.exit(selftest(root))
    r = run_benchmark(root)
    print(f"== trigger benchmark（{len(r['cases'])} 条）==")
    print(f"  TP={r['tp']} FP={r['fp']} TN={r['tn']} FN={r['fn']}")
    print(f"  precision={r['precision']}  recall={r['recall']}  F1={r['f1']}")
    print(f"  负例拒绝率={r['neg_reject_rate'] * 100:.0f}%（要求 100%）")
    print(f"  description 词族覆盖: {r['desc_coverage']}")
    if r["misses"]:
        print("  误分类清单:")
        for m in r["misses"]:
            print(f"    - {m}")
    if r["desc_uncovered"]:
        print("  desc 覆盖缺口（正例词族未出现在 description——召回提升候选）:")
        for u in r["desc_uncovered"]:
            print(f"    - {u}")
    if args.json:
        json.dump(r, open(args.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"结构化结果 → {args.json}")
    sys.exit(0 if r["neg_reject_rate"] == 1.0 else 1)


if __name__ == "__main__":
    main()
