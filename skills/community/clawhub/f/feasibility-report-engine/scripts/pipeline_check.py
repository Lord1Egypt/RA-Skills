#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""报告生产流水线自检器（Report Pipeline Checker）

对成品报告做流水线合规检查，拦住低级失误。
不替代人工判断，但能让"这份报告还没准备好"这件事被自动发现。

用法：
    python3 pipeline_check.py 报告.md
    python3 pipeline_check.py 报告.md --json
    python3 pipeline_check.py 报告.md --strict     # 更严格的阈值

退出码：
    0 = 通过（可能有提示项）
    1 = 有硬伤（不建议交付）
    2 = 用法错误

依赖：仅 Python 3 标准库。
"""
import argparse
import json
import re
import sys
from pathlib import Path

# ---------- 检查配置 ----------

SOURCE_PATTERNS = [
    r"来源[:：]", r"出处[:：]", r"参考[:：]", r"引用[:：]", r"数据来源",
    r"https?://", r"据[^，。；]{2,20}(报告|公告|文件|年报|通稿|白皮书|年报)",
    r"《[^》]{2,40}》", r"第\s*\d+\s*页", r"附件\s*\d+",
    r"(统计|年鉴|数据库|访谈|调研|座谈|会议纪要)",
]

UNCERTAIN_PATTERNS = [
    r"待核实", r"未核实", r"待确认", r"待补充", r"存疑",
    r"估计", r"约\s*\d", r"预计", r"初步判断", r"不完全统计",
    r"假设", r"口径", r"仅供参考", r"不确定",
]

COUNTER_PATTERNS = [
    r"风险", r"局限", r"不足", r"反方", r"反面", r"反对",
    r"挑战", r"不确定性", r"对冲", r"情景分析", r"敏感性",
]

CONCLUSION_PATTERNS = [
    r"结论", r"综上", r"小结", r"建议", r"判断", r"总结", r"落地(建议|路径)",
]

# 判断段落"数字密集"的阈值
NUMBER_RE = re.compile(r"\d+(?:\.\d+)?%?")
UNIT_HINT_RE = re.compile(r"(亿元|万元|元|%|个|家|人|吨|平方米|亩|万台|倍|天|月|年|百分点)")
SECTION_RE = re.compile(r"^#{1,6}\s+\S", re.MULTILINE)


def _scan(text, patterns):
    hits = []
    for p in patterns:
        for m in re.finditer(p, text):
            hits.append(m.group(0)[:40])
    return hits


def check(path: Path, strict: bool) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    chars = len(re.sub(r"\s", "", text))
    sections = SECTION_RE.findall(text)

    results = []

    def add(name, ok, level, detail):
        results.append({"check": name, "pass": bool(ok), "level": level, "detail": detail})

    # 1. 来源标注
    src = _scan(text, SOURCE_PATTERNS)
    src_need = 8 if strict else 4
    add("来源标注", len(src) >= src_need, "high",
        f"命中 {len(src)} 处出处线索" + (f"，示例：{src[:3]}" if src else "（几乎没有可追溯出处）"))

    # 2. 不确定性披露
    unc = _scan(text, UNCERTAIN_PATTERNS)
    add("不确定性披露", len(unc) >= 2, "medium",
        f"命中 {len(unc)} 处" + (f"，示例：{unc[:3]}" if unc else "（没有任何不确定性标注，可疑）"))

    # 3. 反方与局限
    ctr = _scan(text, COUNTER_PATTERNS)
    add("反方与局限", len(ctr) >= 3, "high",
        f"命中 {len(ctr)} 处" + (f"，示例：{ctr[:3]}" if ctr else "（没有风险/反方视角，报告不完整）"))

    # 4. 结论明确
    con = _scan(text, CONCLUSION_PATTERNS)
    add("结论明确", len(con) >= 2, "high",
        f"命中 {len(con)} 处" + (f"，示例：{con[:3]}" if con else "（找不到明确结论）"))

    # 5. 结构完整
    min_sections = 8 if strict else 4
    min_chars = 3000 if strict else 1200
    ok_struct = len(sections) >= min_sections and chars >= min_chars
    add("结构完整", ok_struct, "medium",
        f"{len(sections)} 个小节 / {chars} 字（阈值：{min_sections} 节、{min_chars} 字）")

    # 6. 数字口径
    dense, dense_with_unit, dense_total = 0, 0, 0
    for ln in lines:
        n = NUMBER_RE.findall(ln)
        if len(n) >= 6:
            dense_total += 1
            if UNIT_HINT_RE.search(ln) or re.search(r"[（(][^）)]{2,40}[）)]", ln):
                dense_with_unit += 1
    if dense_total:
        ratio = dense_with_unit / dense_total
        add("数字口径说明", ratio >= 0.5, "medium",
            f"数字密集行 {dense_total} 行，其中 {dense_with_unit} 行带单位或口径说明（{ratio:.0%}）")
    else:
        add("数字口径说明", True, "low", "未发现数字密集段落")

    high_fail = [r for r in results if not r["pass"] and r["level"] == "high"]
    any_fail = [r for r in results if not r["pass"]]
    passed = len(high_fail) == 0
    return {
        "file": str(path),
        "chars": chars,
        "sections": len(sections),
        "results": results,
        "high_failures": len(high_fail),
        "failures": len(any_fail),
        "passed": passed,
    }


def render(rep: dict) -> str:
    ICON = {True: "✅", False: "❌"}
    lines = [
        "=" * 68,
        f"报告流水线自检  {rep['file']}",
        f"篇幅 {rep['chars']} 字 / {rep['sections']} 个小节",
        "=" * 68,
    ]
    for r in rep["results"]:
        mark = ICON[r["pass"]] if r["level"] != "low" else ("✅" if r["pass"] else "⚠️")
        lines.append(f"{mark} [{r['level']:6}] {r['check']}：{r['detail']}")
    lines.append("-" * 68)
    if rep["passed"]:
        lines.append(f"结论：通过（提示项 {rep['failures']} 个，可交付前确认）")
    else:
        lines.append(f"结论：未通过 —— {rep['high_failures']} 项硬伤必须修复后再交付")
    lines.append("提示：本工具只做机械检查，结论是否站得住，仍需人工复核。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="报告生产流水线自检器")
    ap.add_argument("report", help="报告文件路径（.md/.txt）")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--strict", action="store_true", help="严格阈值")
    args = ap.parse_args()

    p = Path(args.report)
    if not p.exists():
        print(f"找不到文件：{p}", file=sys.stderr)
        return 2

    rep = check(p, args.strict)
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=1))
    else:
        print(render(rep))
    return 0 if rep["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
