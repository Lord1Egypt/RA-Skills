#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_all.py —— Skill 全量自检入口（R1：不测不发）

用法：
  python tests/run_all.py
退出码：0 = 全部通过；1 = 有失败项。
"""

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
SCRIPTS = os.path.join(SKILL, "scripts")
PY = sys.executable

SELF_TESTS = [
    ("定价/利润/ROI 恒等式（含目标ROI反推）", os.path.join(SCRIPTS, "profit_roi.py")),
    ("选品评估与竞品分析", os.path.join(SCRIPTS, "selection_eval.py")),
    ("备货计划（安全库存/红线）", os.path.join(SCRIPTS, "stocking_plan.py")),
    ("平台结算单对账 9 类检测", os.path.join(SCRIPTS, "settlement_audit.py")),
    ("广告法违禁词检测", os.path.join(SCRIPTS, "copy_compliance.py")),
    ("漏斗诊断（不出单/转化下滑/ROI）", os.path.join(SCRIPTS, "funnel_diagnose.py")),
    ("数据验真关卡①", os.path.join(SCRIPTS, "data_verify.py")),
    ("来源分级与置信度闸门", os.path.join(SCRIPTS, "confidence.py")),
    ("多平台运营周报（环比/异常）", os.path.join(SCRIPTS, "weekly_report.py")),
    ("变化归因 Price-Volume-Mix + 毛利桥", os.path.join(SCRIPTS, "margin_bridge.py")),
    ("批量变更 dry-run 预演", os.path.join(SCRIPTS, "batch_plan.py")),
    ("跨境到岸成本/关税/VAT/汇率", os.path.join(SCRIPTS, "landed_cost.py")),
    ("图表化 PDF 报告生成", os.path.join(SCRIPTS, "report_pdf.py")),
    ("PDF 交付验真", os.path.join(SCRIPTS, "pdf_verify.py")),
]


def main():
    results = []
    for name, path in SELF_TESTS:
        p = subprocess.run([PY, path, "--self-test"], capture_output=True, text=True, encoding="utf-8")
        ok = p.returncode == 0
        results.append((name, ok, (p.stdout or "").strip().splitlines()[-1:] or [p.stderr.strip()]))
    print("=" * 68)
    print("电商运营决策台 · Skill 自检")
    print("=" * 68)
    for name, ok, tail in results:
        print("[%s] %-28s %s" % ("PASS" if ok else "FAIL", name, tail[0] if tail else ""))
    passed = sum(1 for _, ok, _ in results if ok)
    print("-" * 68)
    print("%d/%d 通过" % (passed, len(results)))
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
