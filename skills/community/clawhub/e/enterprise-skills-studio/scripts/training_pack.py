#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
培训推广包生成器（厚技能化，纯标准库）。

读入一个技能的 SKILL.md（或 --name/--desc），生成"培训包四件套"markdown 骨架：
  场景卡 / 上手指南 / FAQ / 反馈单。
可作为业务人员培训材料起点。

用法：
  python training_pack.py --skill <skill_dir> [--md] [--json]
  python training_pack.py --name "foo" --desc "..." [--md]
"""
import argparse
import json
import os
import re
import sys


def read_skill(skill_dir):
    path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(path):
        return None, None
    txt = open(path, encoding="utf-8", errors="ignore").read()
    name = os.path.basename(os.path.abspath(skill_dir))
    m = re.search(r"name:\s*(.+)", txt)
    if m:
        name = m.group(1).strip().strip('"').strip("'")
    d = ""
    m = re.search(r"description:\s*(.+)", txt)
    if m:
        d = m.group(1).strip().strip('"').strip("'")
    return name, d


def build_pack(name, desc):
    desc = desc or "（待补充：该技能解决什么业务问题）"
    return {
        "name": name,
        "scenario_card": (
            f"## 场景卡 · {name}\n\n"
            f"- **解决什么**：{desc}\n"
            f"- **何时用**：用户/业务方发起明确的相关请求时\n"
            f"- **别用在哪**：跨系统敏感写操作前未确认 / 超出授权域 / 替代人工决策的合规场景\n"
        ),
        "quick_start": (
            "## 上手指南（3 步）\n\n"
            "1. 用一句话描述你要做的事（如：'把这批 CRM 线索同步到 ERP'）\n"
            "2. 看技能返回的结果与确认提示，按需补充信息\n"
            "3. 出现异常：技能会请求确认或给出回滚提示，按提示处理；仍卡住 → 提反馈单\n"
        ),
        "faq": (
            "## FAQ（业务最常问）\n\n"
            "1. **它会不会乱改我数据？** 涉及写操作默认走确认 + 最小权限 + 审计（见事务安全四件套）。\n"
            "2. **出错了怎么办？** 操作幂等可重跑；关键动作有回滚/不归点保护。\n"
            "3. **它比我自己做快多少？** 试点场景按 ROI 门槛筛选，通常单次节省 >30 分钟。\n"
            "4. **数据会出公司吗？** 不出；以 Git 为单一真源，不自动跨 surface 同步。\n"
            "5. **谁负责维护？** 每个技能有 owner/负责人（见技能头声明）。\n"
        ),
        "feedback_ticket": (
            "## 反馈单\n\n"
            "- **反馈人/角色**：_________\n"
            "- **场景**：_________\n"
            "- **期望**：_________\n"
            "- **实际**：_________\n"
            "- **频率**：偶发 / 经常\n"
            "- **回收**：每周反馈小会汇总 → 进入技能 Evolution Log（见 `references/evolution.md`）\n"
        ),
    }


def render_md(pack):
    return "\n\n---\n\n".join([
        pack["scenario_card"], pack["quick_start"], pack["faq"], pack["feedback_ticket"]
    ])


def main():
    ap = argparse.ArgumentParser()
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

    pack = build_pack(name, desc)
    if args.json:
        print(json.dumps(pack, ensure_ascii=False, indent=2))
    else:
        print(render_md(pack))
    return 0


if __name__ == "__main__":
    sys.exit(main())
