#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨平台适配检查器（厚技能化，纯标准库）。

按 references/cross-platform.md 规则，检查一个技能目录对多桌面 Agent 的适配度：
  - agentskills.io 结构合规（SKILL.md/前导元数据/三级加载）
  - name 规则（≤64 字符、小写连字符）
  - description 规则（≤1024、含"何时调用"触发语）
  - 依赖预置检查（API/容器部署不能运行时装包）
  - 是否过度特化单一平台

输出每平台适配要点 + 总体可移植性评级。

用法：
  python cross_platform_check.py --skill <dir> [--json] [--md]
  python cross_platform_check.py --skill <dir> --platform claude-code   # 仅某平台
"""
import argparse
import json
import os
import re
import sys

PLATFORMS = ["workbuddy", "claude-code", "codex", "cursor", "loong", "hermes"]


def load_skill(skill_dir):
    path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(path):
        return None
    txt = open(path, encoding="utf-8", errors="ignore").read()
    meta = {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", txt, re.S)
    if m:
        for line in m.group(1).splitlines():
            kv = re.match(r"(\w+):\s*(.+)", line)
            if kv:
                meta[kv.group(1)] = kv.group(2).strip().strip('"').strip("'")
    return {"text": txt, "meta": meta, "has_frontmatter": bool(m)}


def check(skill):
    txt = skill["text"]
    meta = skill["meta"]
    issues = []
    # name
    name = meta.get("name", "")
    if not name:
        issues.append(("FAIL", "缺 name 字段"))
    elif len(name) > 64:
        issues.append(("FAIL", f"name 超 64 字符（{len(name)}）"))
    elif not re.match(r"^[a-z0-9][a-z0-9\-]*$", name):
        issues.append(("WARN", "name 应全小写连字符（建议符合 agentskills.io）"))
    # description
    desc = meta.get("description", "")
    if not desc:
        issues.append(("FAIL", "缺 description 字段"))
    elif len(desc) > 1024:
        issues.append(("FAIL", f"description 超 1024（{len(desc)}）"))
    else:
        if not re.search(r"当|用于|如果|需要|要|时", desc):
            issues.append(("WARN", "description 建议含'何时调用'触发语（跨平台召回一致）"))
    # frontmatter
    if not skill["has_frontmatter"]:
        issues.append(("FAIL", "缺 YAML 前导元数据（agentskills.io 必需）"))
    # 三级加载：至少含指令段
    if not re.search(r"^#", txt, re.M):
        issues.append(("WARN", "未见标题/指令段，确认三级加载可用"))
    # 依赖预置：扫描 scripts 里 import（启发式）
    has_runtime_install_risk = False
    for root, _, files in os.walk(os.path.join(skill.get("_dir", ""), "scripts")) if skill.get("_dir") else []:
        for f in files:
            if f.endswith(".py"):
                # 跳过检查器自身（其源码含 pip install 正则字面量，会自匹配）
                if f == "cross_platform_check.py":
                    continue
                fp = os.path.join(root, f)
                if os.path.isfile(fp):
                    c = open(fp, encoding="utf-8", errors="ignore").read()
                    if re.search(r"pip install|npm install|apt-get|requirements\.txt", c):
                        has_runtime_install_risk = True
    if has_runtime_install_risk:
        issues.append(("WARN", "scripts 含运行时装包指令；API/容器部署须预置依赖（跨 surface 不自动同步）"))
    # 过度特化：description 含具体平台专有名词
    for kw in ["claude", "cursor", "codex", "workbuddy", "龙虾", "hermes", "loong"]:
        if kw.lower() in (name + desc).lower():
            issues.append(("WARN", f"出现平台专有词'{kw}'，避免过度特化以保持可移植"))
            break
    return issues


def per_platform(issues):
    # 推导各平台要点
    out = {}
    for p in PLATFORMS:
        notes = []
        for sev, msg in issues:
            if sev == "FAIL":
                notes.append(f"需修复后再上 {p}：{msg}")
            elif "依赖" in msg and p in ("claude-code", "codex", "loong", "hermes", "workbuddy"):
                notes.append(f"部署到 {p} 前预置依赖（{msg}）")
        out[p] = notes
    return out


def render(skill_dir, issues, per_plat, md=False):
    fails = [m for s, m in issues if s == "FAIL"]
    warns = [m for s, m in issues if s == "WARN"]
    rating = "可移植(PASS)" if not fails else "需修复(BLOCK)"
    if md:
        lines = ["# 跨平台适配检查", "", f"**评级**：{rating}", "", "## 结构/字段问题", ""]
        for s, m in issues:
            lines.append(f"- [{s}] {m}")
        lines += ["", "## 各平台适配要点", ""]
        for p, notes in per_plat.items():
            lines.append(f"### {p}")
            lines.append("\n".join(f"- {n}" for n in notes) if notes else "- 无额外适配项")
            lines.append("")
        return "\n".join(lines)
    lines = [f"跨平台适配检查：{skill_dir}", "=" * 50, f"评级：{rating}", "-" * 50]
    lines.append(f"FAIL：{len(fails)}  WARN：{len(warns)}")
    for s, m in issues:
        lines.append(f"  [{s}] {m}")
    lines.append("-" * 50)
    lines.append("各平台要点：")
    for p, notes in per_plat.items():
        lines.append(f"  · {p}: " + ("无额外适配项" if not notes else "; ".join(notes)))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", required=True, help="技能目录（含 SKILL.md）")
    ap.add_argument("--platform", help="仅检查某平台：" + "/".join(PLATFORMS))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--md", action="store_true")
    args = ap.parse_args()

    if not os.path.isdir(args.skill):
        print(f"错误：目录不存在 {args.skill}", file=sys.stderr)
        return 1
    skill = load_skill(args.skill)
    if not skill:
        print("错误：目录内无 SKILL.md", file=sys.stderr)
        return 1
    skill["_dir"] = args.skill
    issues = check(skill)
    per_plat = per_platform(issues)
    if args.platform:
        per_plat = {args.platform: per_plat.get(args.platform, [])}

    if args.json:
        print(json.dumps({"issues": issues, "per_platform": per_plat,
                          "rating": "PASS" if not any(s == "FAIL" for s, _ in issues) else "BLOCK"},
                         ensure_ascii=False, indent=2))
    else:
        print(render(args.skill, issues, per_plat, md=args.md))
    return 2 if any(s == "FAIL" for s, _ in issues) else 0


if __name__ == "__main__":
    sys.exit(main())
