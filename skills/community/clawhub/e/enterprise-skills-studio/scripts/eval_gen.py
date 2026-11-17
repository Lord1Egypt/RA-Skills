#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能评测套件生成器（厚技能化，纯标准库）。

读入一个技能的 SKILL.md，生成动态评测用例套件（应触发/不应触发/边界），
输出 markdown（可填空）与 json（机器可读）。接 references/evaluation.md。

用法：
  python eval_gen.py --skill <dir> [--json] [--md]
  python eval_gen.py --name "foo" --desc "..." [--json]
"""
import argparse
import json
import os
import re
import sys

# 通用"不应触发"反例（任何业务技能都应不命中）
NEGATIVE_POOL = [
    "帮我写一首关于春天的诗",
    "今天天气怎么样",
    "讲个冷笑话",
    "翻译这句话成英文：你好世界",
    "推荐一部电影",
]

# 边界示例模板（需按技能补预期）
BOUNDARY_TEMPLATES = [
    "（缺关键参数）只说要'<目标>'但没给目标对象/系统 → 预期：追问而非臆测",
    "（模糊表述）'<目标>'这个说法有歧义 → 预期：澄清或给默认并提示",
    "（冲突指令）既要求 A 又要求与 A 矛盾的 B → 预期：指出冲突并请求裁决",
]


def read_skill(skill_dir):
    path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(path):
        return None, None
    txt = open(path, encoding="utf-8", errors="ignore").read()
    name = os.path.basename(os.path.abspath(skill_dir))
    m = re.search(r"name:\s*(.+)", txt)
    if m:
        name = m.group(1).strip().strip('"').strip("'")
    desc = ""
    m = re.search(r"description:\s*(.+)", txt)
    if m:
        desc = m.group(1).strip().strip('"').strip("'")
    return name, desc


def extract_triggers(desc):
    # 1) 抓"当用户要...时 / 当...时"包裹的内容作为意图池
    m = re.search(r"当用户(?:要)?(.+?)时", desc, re.S)
    core = m.group(1) if m else desc
    # 2) 按常见分隔符切成候选意图（兼容"当用户要 A / B / C 时"写法）
    parts = re.split(r"[／/、，,；;]", core)
    phrases = []
    for p in parts:
        p = p.strip().strip("\"'“”").strip()
        p = re.sub(r"\s+", " ", p)
        if 2 <= len(p) <= 30:
            phrases.append(p)
    # 3) 去重保序，最多取前 6 条
    seen = set(); uniq = []
    for p in phrases:
        if p not in seen:
            seen.add(p); uniq.append(p)
    if not uniq:
        uniq = [desc[:30]]
    return uniq[:6]


def build_suite(name, desc):
    triggers = extract_triggers(desc)
    positives = []
    for t in triggers:
        base = re.sub(r"^当用户|^当|时$|用于", "", t).strip(" ，。；")
        positives.append(f"用户说：'{base}' → 预期：命中技能 {name}")
    # 若触发短语太少，补一个通用正向
    if not positives:
        positives.append(f"用户表达意图与'{desc[:30]}'相关 → 预期：命中 {name}")
    negatives = [f"用户说：'{n}' → 预期：不触发 {name}" for n in NEGATIVE_POOL]
    boundaries = [t.replace("<目标>", (desc[:12] or "目标")) for t in BOUNDARY_TEMPLATES]
    return {
        "name": name,
        "description": desc,
        "positive": positives,
        "negative": negatives,
        "boundary": boundaries,
    }


def render_md(suite):
    lines = [
        f"# 评测套件 · {suite['name']}",
        "",
        f"> 描述：{suite['description']}",
        "",
        "## 应触发（Positive）",
    ]
    for i, c in enumerate(suite["positive"], 1):
        lines.append(f"{i}. {c}")
    lines += ["", "## 不应触发（Negative）"]
    for i, c in enumerate(suite["negative"], 1):
        lines.append(f"{i}. {c}")
    lines += ["", "## 边界（Boundary，需补预期与判定）"]
    for i, c in enumerate(suite["boundary"], 1):
        lines.append(f"{i}. {c}")
    lines += ["", "---", "判定：逐项记录 命中/误触发/边界通过；算召回率/精确率/边界通过率；每次改技能后回归。"]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="技能评测套件生成器")
    ap.add_argument("--skill", help="技能目录（含 SKILL.md）")
    ap.add_argument("--name", help="技能名（不读目录时）")
    ap.add_argument("--desc", help="技能描述")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--md", action="store_true")
    args = ap.parse_args()

    name, desc = None, None
    if args.skill:
        name, desc = read_skill(args.skill)
    if not name:
        name = args.name or "untitled-skill"
    if not desc and args.desc:
        desc = args.desc

    suite = build_suite(name, desc)
    if args.json:
        print(json.dumps(suite, ensure_ascii=False, indent=2))
    else:
        print(render_md(suite))
    return 0


if __name__ == "__main__":
    sys.exit(main())
