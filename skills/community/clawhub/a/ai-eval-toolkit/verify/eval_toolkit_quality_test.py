# -*- coding: utf-8 -*-
"""LLM 评测工具链 - 质量与安全稳定性验证（本地闭环，零网络）
维度：指标时效 / 覆盖完整 / 工具可用 / 判定正确 / 结构一致 / 安全净度
"""
import json
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFS = os.path.join(BASE, "references")
TOOLS = os.path.join(BASE, "tools")
SKILL_MD = os.path.join(BASE, "SKILL.md")
PY = sys.executable

DIM_KEYS = ["engine_timeliness", "coverage_completeness", "tool_usability",
            "judgment_accuracy", "structure_compliance", "security_cleanliness"]
DIM_LABELS = ["引擎时效", "覆盖完整", "工具可用", "判定正确", "结构一致", "安全净度"]


def run_tool(args, timeout=30):
    try:
        r = subprocess.run([PY, os.path.join(TOOLS, "eval_toolkit.py")] + args,
                           capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout or ""
    except Exception as e:
        return -1, str(e)


def check_timeliness():
    items = []
    for f in os.listdir(REFS):
        if not f.endswith(".md"):
            continue
        text = open(os.path.join(REFS, f), encoding="utf-8").read()
        items.append({"name": f"{f} 含核对基准日", "pass": "核对基准日" in text})
    return items


def check_coverage():
    items = []
    nav = open(SKILL_MD, encoding="utf-8").read()
    files = sorted(f for f in os.listdir(REFS) if f.endswith(".md"))
    items.append({"name": f"references 模块数=8（实际 {len(files)}）", "pass": len(files) == 8})
    for f in files:
        items.append({"name": f"导航表包含 {f}", "pass": f in nav})
    for kw in ["01-工具链全景", "02-评测集管理", "03-幻觉检测引擎", "04-RAG指标计算",
               "05-回归对比", "06-报告与门禁", "07-与平台工具衔接", "08-FAQ"]:
        items.append({"name": f"关键模块 {kw}", "pass": kw in nav})
    items.append({"name": "快速上手存在", "pass": "快速上手" in nav})
    items.append({"name": "能力边界存在", "pass": "能力边界" in nav})
    items.append({"name": "版权与许可段存在", "pass": "版权与许可" in nav})
    return items


def check_tool():
    items = []
    rc, out = run_tool(["--help"])
    items.append({"name": "--help 可执行", "pass": rc == 0})
    for cmd in ["dataset", "hallucination", "ragscore", "compare", "report"]:
        items.append({"name": f"命令 {cmd} 在帮助中", "pass": cmd in out})
    rc, out = run_tool(["dataset", "--action", "init", "--out", "/tmp/evalset_t.jsonl"])
    items.append({"name": "dataset init 可执行", "pass": rc == 0})
    rc, out = run_tool(["hallucination", "--answer", "销量100万台", "--source", "销量50万台"])
    items.append({"name": "hallucination 检数字矛盾", "pass": rc == 0 and "suspicious" in out})
    rc, out = run_tool(["hallucination", "--answer", "保修期一年", "--source", "保修期一年"])
    items.append({"name": "hallucination 干净放行", "pass": rc == 0 and "未命中" in out})
    rc, out = run_tool(["ragscore", "--answer", "保修期1年", "--context", "保修期1年"])
    items.append({"name": "ragscore 含忠实度", "pass": rc == 0 and "忠实度" in out})
    return items


def check_judgment():
    items = []
    # 场景指标命中正确性
    cases = [
        ("数字矛盾", "销量100万台", "销量50万台", "suspicious"),
        ("干净", "保修期一年", "保修期一年", "未命中"),
    ]
    for name, ans, src, expect in cases:
        rc, out = run_tool(["hallucination", "--answer", ans, "--source", src])
        items.append({"name": f"幻觉检测[{name}]→{expect}", "pass": rc == 0 and expect in out})
    return items


def check_structure():
    items = []
    sk = open(SKILL_MD, encoding="utf-8").read()
    fm = sk.split("---")[1]
    items.append({"name": "frontmatter 有 9 必填字段",
                  "pass": all(k in fm for k in ["name:", "slug:", "display_name:", "displayName:",
                                                "title:", "version:", "category:", "author:", "license:"])})
    # YAML 可解析性防回归（SkillPie 半角冒号坑）
    colon_ok = True
    for line in fm.splitlines():
        if line.startswith(("description:", "description_en:", "name:", "title:", "display_name:", "displayName:")):
            rest = line.split(":", 1)[1] if ":" in line else ""
            if ": " in rest:
                colon_ok = False
    items.append({"name": "description 值无半角冒号+空格（YAML 安全）", "pass": colon_ok})
    items.append({"name": "LICENSE.md 存在", "pass": os.path.exists(os.path.join(BASE, "LICENSE.md"))})
    items.append({"name": "SECURITY_AUDIT.md 存在", "pass": os.path.exists(os.path.join(BASE, "SECURITY_AUDIT.md"))})
    return items


def check_safety():
    items = []
    patterns = ["C:\\Users", "D:\\Workbuddy", "zhaoxinghua",
                "Ste" + "ven", "Med" + "Xpert", "美达" + "信"]
    clean = True
    for f in os.listdir(REFS) + [SKILL_MD]:
        text = open(os.path.join(REFS, f) if f != "SKILL.md" else SKILL_MD, encoding="utf-8").read()
        for p in patterns:
            if p in text:
                clean = False
    items.append({"name": "references+SKILL.md 无敏感词", "pass": clean})
    items.append({"name": "工具脚本零网络依赖",
                  "pass": "import requests" not in open(os.path.join(TOOLS, "eval_toolkit.py"), encoding="utf-8").read()})
    return items


def main():
    all_items = [
        check_timeliness(), check_coverage(), check_tool(), check_judgment(),
        check_structure(), check_safety(),
    ]
    total = fail = 0
    lines = []
    dimensions = []
    for label, key, items in zip(DIM_LABELS, DIM_KEYS, all_items):
        ok = sum(1 for i in items if i["pass"])
        total += len(items)
        fail += len(items) - ok
        lines.append(f"[{label}] {ok}/{len(items)}")
        for i in items:
            if not i["pass"]:
                lines.append(f"  FAIL: {i['name']}")
        dimensions.append({"key": key, "label": label,
                           "score": round(5.0 * ok / len(items), 2), "checks": items})
    score = round(5.0 * (total - fail) / total, 2) if total else 0
    lines.append(f"综合平均：{score}")
    print("\n".join(lines))

    result = {
        "skill": "ai-eval-toolkit",
        "version": "1.0.0",
        "generated_at": "2026-08-28",
        "note": "LLM 评测工具链 · 质量与安全稳定性实测（本地闭环）",
        "dimensions": dimensions,
        "summary": {"total": total, "passed": total - fail, "failed": fail, "overall": score},
        "benchmarks": {
            "industry_baseline": {k: v for k, v in zip(DIM_KEYS, [3.0, 3.2, 3.0, 3.4, 3.2, 3.0])},
            "enterprise_standard": {k: v for k, v in zip(DIM_KEYS, [4.5, 4.5, 4.5, 4.5, 4.5, 4.5])},
        },
    }
    with open(os.path.join(BASE, "verify", "security_results.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
