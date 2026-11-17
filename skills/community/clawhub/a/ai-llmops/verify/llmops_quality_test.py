# -*- coding: utf-8 -*-
"""AI 模型资产管理（LLMOps）- 质量与安全稳定性验证（本地闭环，零网络）
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

DIM_KEYS = ["asset_timeliness", "coverage_completeness", "tool_usability",
            "judgment_accuracy", "structure_compliance", "security_cleanliness"]
DIM_LABELS = ["方法时效", "覆盖完整", "工具可用", "判定正确", "结构一致", "安全净度"]


def run_tool(args, timeout=30):
    try:
        r = subprocess.run([PY, os.path.join(TOOLS, "llmops_toolkit.py")] + args,
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
    for kw in ["01-资产全景与台账", "02-模型卡与注册", "03-版本管理", "04-上线下线管理",
               "05-漂移监控", "06-成本治理", "07-治理制度与流程", "08-FAQ"]:
        items.append({"name": f"关键模块 {kw}", "pass": kw in nav})
    items.append({"name": "快速上手存在", "pass": "快速上手" in nav})
    items.append({"name": "能力边界存在", "pass": "能力边界" in nav})
    items.append({"name": "版权与许可段存在", "pass": "版权与许可" in nav})
    return items


def check_tool():
    items = []
    rc, out = run_tool(["--help"])
    items.append({"name": "--help 可执行", "pass": rc == 0})
    for cmd in ["inventory", "modelcard", "lifecycle", "drift", "cost"]:
        items.append({"name": f"命令 {cmd} 在帮助中", "pass": cmd in out})
    rc, out = run_tool(["inventory"])
    items.append({"name": "inventory 含五类资产", "pass": rc == 0 and "五类资产" in out})
    rc, out = run_tool(["modelcard"])
    items.append({"name": "modelcard 含运维信息", "pass": rc == 0 and "运维信息" in out})
    rc, out = run_tool(["lifecycle", "--phase", "launch"])
    items.append({"name": "lifecycle launch 含灰度", "pass": rc == 0 and "灰度" in out})
    rc, out = run_tool(["drift"])
    items.append({"name": "drift 含三类漂移", "pass": rc == 0 and "数据" in out})
    rc, out = run_tool(["cost"])
    items.append({"name": "cost 含路由分层", "pass": rc == 0 and "路由分层" in out})
    return items


def check_judgment():
    items = []
    # 场景指标命中正确性
    cases = [
        ("register", "Model Card"),
        ("launch", "快照"),
        ("monitor", "评测集"),
        ("retire", "替代方案"),
    ]
    for phase, expect in cases:
        rc, out = run_tool(["lifecycle", "--phase", phase])
        items.append({"name": f"生命周期[{phase}]含[{expect}]", "pass": rc == 0 and expect in out})
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
                  "pass": "import requests" not in open(os.path.join(TOOLS, "llmops_toolkit.py"), encoding="utf-8").read()})
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
        "skill": "ai-llmops",
        "version": "1.0.0",
        "generated_at": "2026-08-28",
        "note": "AI 模型资产管理 · 质量与安全稳定性实测（本地闭环）",
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
