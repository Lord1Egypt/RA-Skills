#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""agentskills.io 规范自检（v1.7 F3）：SKILL.md frontmatter 兼容矩阵。

校验规则（跨注册表通用）：
  1. frontmatter 存在且可解析（--- 围栏）
  2. name 存在、kebab-case、与目录名一致（可选 --dir 校验）
  3. description 存在且 ≤1024 字符（超长会被静默丢弃——ZCode 实测铁律）
  4. 必备键齐全（name/description）；license 建议存在
  5. 未知顶层键仅提示（各平台兼容度不同，不算错误）
用法：python3 agentskills_check.py <SKILL.md 路径> [--dir <技能目录名>]
"""
import argparse
import re
import sys


def frontmatter(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else ""


def parse_keys(fm: str) -> dict:
    out = {}
    for line in fm.splitlines():
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):", line)
        if m:
            out[m.group(1)] = line
    return out


def scalar_value(fm: str, key: str) -> str:
    m = re.search(rf"^{key}:\s*(.+?)$", fm, re.M)
    return m.group(1).strip().strip("\"'") if m else ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill_md")
    ap.add_argument("--dir", help="技能目录名（校验 name 一致性）")
    ap.add_argument("--distro", action="store_true",
                    help="输出 skills.sh / agentskills.io 分发准备清单（v1.11）")
    args = ap.parse_args()
    text = open(args.skill_md, encoding="utf-8").read()
    fm = frontmatter(text)
    fails, notes = [], []

    if not fm:
        print("FAIL: frontmatter 缺失或格式错误")
        return 1
    keys = parse_keys(fm)

    name = scalar_value(fm, "name")
    if not name:
        fails.append("name 缺失")
    elif not re.match(r"^[a-z0-9][a-z0-9-]*$", name):
        fails.append(f"name 非 kebab-case: {name}")
    if args.dir and name and name != args.dir:
        fails.append(f"name ({name}) 与目录名 ({args.dir}) 不一致")

    desc = scalar_value(fm, "description")
    if not desc and "description:" not in fm:
        fails.append("description 缺失")
    else:
        # 折叠标量（>-）取正文块长度——遇下一 top-level 键即止(贪婪版会把
        # when_to_use 一并计入致误报超长,09-24 修复)
        m = re.search(r"description:\s*>-?\n((?:[ \t]+(?!\w+:).*\n?)+)", fm)
        # v4.5.0：量折叠后的值（平台 YAML 折叠实收）——注意 desc 不能用作长度：
        # scalar_value 对 >- 折叠标量返回 ">-"（审计 P1 实证 dlen 恒 2 守卫已死）
        dlen = len(" ".join(l.strip() for l in m.group(1).splitlines())) if m \
            else len(desc)
        if dlen > 1024:
            fails.append(f"description 超长（{dlen} > 1024，会被静默丢弃）")
        else:
            notes.append(f"description {dlen} 字符（≤1024 安全）")

    for k in ("name", "description"):
        if k not in keys:
            fails.append(f"必备键缺失: {k}")
    if "license" not in keys:
        notes.append("建议补 license 键（部分注册表展示用）")
    # v1.11：when_to_use 与 description 同为折叠标量，超长同样有被截断/丢弃风险
    if "when_to_use" in keys:
        m = re.search(r"when_to_use:\s*>-?\n((?:[ \t]+.*\n?)+)", fm)
        wlen = len(m.group(1)) if m else len(scalar_value(fm, "when_to_use"))
        if wlen > 1024:
            notes.append(f"when_to_use 超长（{wlen} > 1024，部分平台可能截断）")
        else:
            notes.append(f"when_to_use {wlen} 字符（≤1024 安全）")

    known = {"name", "license", "description", "when_to_use", "metadata",
             "version", "author", "homepage", "documentation", "icon"}
    unknown = [k for k in keys if k not in known]
    if unknown:
        notes.append("非通用键（各平台兼容度不同，仅提示）: " + ", ".join(unknown))

    if args.distro:
        # v1.11 分发扩面准备清单（skills.sh = vercel-labs repo 型目录，
        # npx skillsadd <owner/repo> 安装；agentskills.io 为开放标准规范）
        print("--- 分发准备（--distro）---")
        print("skills.sh: 需公开 GitHub repo；SKILL.md 于 repo 根 / skills/<name>/ /"
              " .claude/skills/<name>/ 均可被发现；安装 npx skillsadd <owner/repo>")
        print("agentskills.io: name(kebab-case)+description(≤1024) 必备——上方已校验")
        print("ClawHub/SkillHub: 现有发布链覆盖（ch_release_*_claw.sh），无需额外适配")

    for n in notes:
        print("NOTE:", n)
    for f in fails:
        print("FAIL:", f)
    print("AGENTSPEAK_CHECK:", "PASS" if not fails else "FAIL")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
