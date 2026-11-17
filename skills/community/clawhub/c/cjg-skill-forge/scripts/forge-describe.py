#!/usr/bin/env python3
"""forge-describe.py — 技能描述（description）SEO 生成助手。

按 references/trigger-keywords.md 第 2 节公式生成 ≤1024 字符的描述草稿：
  一句话定位 → 核心能力 2–4 条（每条嵌 1–2 个触发词）→ 使用场景 1 句 → 边界（可选）
并校验长度 + 触发词密度（writing_gate W3a/W3b 的生成侧助手）。

用法：
  python forge-describe.py --name "XX技能" --what "一句话定位" \
      --abilities "能力1|能力2|能力3" --triggers "触发词1,触发词2,..." [--english]
  python forge-describe.py --skill <技能目录>     # 从现有 SKILL.md 提取要点生成增强版
退出码：0=生成且 ≤1024；2=超长（已尽量精简仍超）
"""
import argparse
import json
import os
import re
import sys

MAX = 1024
CORE_HINT = ("创建", "制作", "升级", "生成", "整理", "合并", "审计", "打分",
             "review", "build", "forge", "skill", "create", "improve")


def _shorten(parts, budget):
    """按预算拼接：定位(必留) + 能力(可裁剪) + 场景 + 边界。"""
    anchor = parts[0]
    rest = [p for p in parts[1:] if p]
    out = anchor
    for p in rest:
        if len(out) + len(p) + 1 > budget:
            break
        out += p
    return out


def gen(name, what, abilities, triggers, english=False):
    """生成描述草稿。返回 (text, used_abilities, length)。"""
    t = "、".join([x for x in triggers if x]) or "（触发词未提供）"
    if english:
        head = f"{name} / {what} — "
        body = ""
        for i, a in enumerate(abilities, 1):
            body += f"({i}) {a.strip()}; "
        scene = f"Use when {t}."
        tail = ""
    else:
        head = f"{name} —— {what}："
        body = "".join(f"{a.strip()}；" for a in abilities)
        scene = f"当你想{t}时，用它。"
        tail = ""
    raw = head + body + scene + tail
    # 若超长，先裁能力，再裁场景
    if len(raw) > MAX:
        used = []
        cur = head
        for a in abilities:
            cand = cur + f"{a.strip()}；"
            if len(cand) + len(scene) + len(tail) > MAX - 20:
                break
            cur = cand
            used.append(a)
        body = cur[len(head):]
        raw = head + body + scene + tail
        used_ab = len(used)
    else:
        used_ab = len(abilities)
    return raw, used_ab, len(raw)


def check_report(text):
    hits = [w for w in CORE_HINT if w.lower() in text.lower()]
    return len(text) <= MAX, len(hits), hits


def from_skill(skill_dir):
    """从 SKILL.md 提取要点：displayName/description/何时使用表触发词。"""
    p = os.path.join(skill_dir, "SKILL.md")
    md = open(p, encoding="utf-8").read()
    fm = md.split("---", 2)[1] if md.startswith("---") else ""
    name = re.search(r"^displayName:\s*(.+)$", fm, re.M)
    name = name.group(1).strip().strip('"') if name else os.path.basename(skill_dir)
    desc = ""
    m = re.search(r"^description:[ \t]*\|\n((?:  .*\n?)+)", fm, re.M)
    if m:
        desc = re.sub(r"^  ", "", m.group(1), flags=re.M).strip()
    m2 = re.search(r"^description:[ \t]*([^|\n].*)$", fm, re.M)
    if not desc and m2:
        desc = m2.group(1).strip().strip('"')
    trigs = []
    mt = re.search(r"## 何时使用.*?\n((?:\|.*\n)+)", md, re.S)
    if mt:
        for row in mt.group(1).splitlines():
            cols = [c.strip() for c in row.strip().strip("|").split("|")]
            if len(cols) >= 3:
                for q in re.findall(r'“([^”]+)”|"([^"]+)"', cols[2]):
                    trigs += [x for x in q if x]
    return name, desc, list(dict.fromkeys([t for t in trigs if t]))[:10]


def main():
    ap = argparse.ArgumentParser(description="技能描述 SEO 生成助手")
    ap.add_argument("--name", help="技能名（如 技能锻造炉）")
    ap.add_argument("--what", help="一句话定位（如 从零打造/重铸全球最牛的 AI 技能）")
    ap.add_argument("--abilities", help="核心能力，| 分隔（如 锻造新技能|审计打分|合并重叠技能）")
    ap.add_argument("--triggers", help="触发词，逗号分隔（如 创建技能,升级技能,review this skill）")
    ap.add_argument("--skill", help="从现有技能目录提取要点生成增强版")
    ap.add_argument("--english", action="store_true", help="输出英文描述")
    args = ap.parse_args()

    if args.skill:
        name, desc, trigs = from_skill(args.skill)
        print(f"# 从技能目录提取：{name}")
        print(f"  现有 description {len(desc)} 字符；触发词 {len(trigs)} 个: {trigs[:6]}")
        what = args.what or (desc.split("——")[1].split("。")[0] if "——" in desc else desc[:40])
        abilities = [a for a in (args.abilities or "").split("|") if a] or \
                    [s.strip("；。 ") for s in re.split(r"[；。]", desc) if len(s.strip()) > 8][:4]
        triggers = args.triggers.split(",") if args.triggers else trigs
    else:
        if not (args.name and args.what and args.abilities):
            ap.error("需 --name/--what/--abilities（或 --skill 提取）")
        name, what = args.name, args.what
        abilities = [a for a in args.abilities.split("|") if a]
        triggers = [t for t in (args.triggers or "").split(",") if t]

    text, used, ln = gen(name, what, abilities, triggers, args.english)
    ok, n_hits, hit_list = check_report(text)
    print(f"\n# 生成描述（{ln}/{MAX} 字符，{'✅ ≤1024' if ok else '❌ 超长'}）：")
    print(text)
    print(f"\n# 触发词命中 {n_hits} 个: {hit_list}（目标 ≥3，不足可手动补充）")
    print(f"# 能力条目用了 {used}/{len(abilities)} 条（超长自动裁剪）")
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
