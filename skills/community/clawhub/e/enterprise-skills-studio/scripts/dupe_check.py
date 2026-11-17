#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能发现/复用检测器（厚技能化，纯标准库）。

扫描一组技能（来自技能目录树或注册表 JSON），检测：
  - name 重名 / name 近似（编辑距离）
  - description 关键词 Jaccard 重叠
  - 触发词重叠（双方 description 共同含的"何时调用"关键词数量）

输出每对技能的关系与决策建议（复用/扩展/合并/新造/错开触发域）。

用法：
  python dupe_check.py --skills-dir <dir> [--json] [--md]
  python dupe_check.py --registry <reg.json> [--json] [--md]
  python dupe_check.py --name "foo" --desc "..." --skills-dir <dir>   # 单技能 vs 库

退出码：0 正常；发现 name 完全相同返回 2（视为发布门阻断信号）。
"""
import argparse
import json
import os
import re
import sys

# ---------- 文本工具 ----------
STOP = set("的 了 和 与 或 在 是 把 对 为 用于 一个 用户 当 时 进行 处理 生成 创建 管理 查询 同步 更新 删除 提交 写入 读取 调用 需要 可以 使用 以及 并 等 中 之 其 该 此 要 如果 想要 做 导出 导入 审批 将 把 被 由 从 向 给 让 使 请 即 也 都 还 就 而 则".split())

TRIGGER_HINTS = ["当用户", "用于", "当", "如果", "需要", "想要", "要", "做", "处理", "查询", "生成", "创建", "管理", "同步", "审批", "导出", "导入"]


def tokenize(text):
    if not text:
        return set()
    # 中文按字+英文按词混合；简单按非字母数字切，再拆中文单字
    toks = set()
    for m in re.findall(r"[a-zA-Z0-9_]+|[一-鿿]", text.lower()):
        if re.match(r"[a-zA-Z0-9_]+$", m):
            if len(m) > 1:
                toks.add(m)
        else:
            toks.add(m)  # 单汉字
    toks -= STOP
    return toks


def jaccard(a, b):
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def levenshtein(a, b):
    if a == b:
        return 0
    la, lb = len(a), len(b)
    if la == 0:
        return lb
    if lb == 0:
        return la
    prev = list(range(lb + 1))
    for i in range(1, la + 1):
        cur = [i] + [0] * lb
        for j in range(1, lb + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[lb]


def norm_name(n):
    return re.sub(r"[\s_\-]+", "-", (n or "").lower()).strip("-")


def extract_trigger_words(desc):
    # 取 description 中的核心名词短语过于复杂；用关键词 token 交集近似"触发域重叠"
    return tokenize(desc)


# ---------- 加载技能清单 ----------
def load_from_dir(d):
    skills = []
    if not os.path.isdir(d):
        return skills
    for entry in sorted(os.listdir(d)):
        sp = os.path.join(d, entry, "SKILL.md")
        if os.path.isfile(sp):
            txt = open(sp, encoding="utf-8", errors="ignore").read()
            fname = entry
            nm = re.search(r"name:\s*(.+)", txt)
            if nm:
                fname = nm.group(1).strip().strip('"').strip("'")
            desc = ""
            m = re.search(r"description:\s*(.+)", txt)
            if m:
                desc = m.group(1).strip().strip('"').strip("'")
            skills.append({"name": fname, "description": desc})
    return skills


def load_from_reg(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    out = []
    for it in data:
        out.append({"name": it.get("name", ""), "description": it.get("description", "")})
    return out


# ---------- 核心判定 ----------
def analyze(skills, new_one=None):
    # 归一化 name
    for s in skills:
        s["_n"] = norm_name(s["name"])
        s["_t"] = tokenize(s["description"])
    findings = []
    names = {}
    for s in skills:
        names.setdefault(s["_n"], []).append(s["name"])

    # name 重名
    for nn, originals in names.items():
        if len(originals) > 1:
            findings.append({
                "type": "NAME_DUP",
                "a": originals[0], "b": originals[1] if len(originals) > 1 else "",
                "others": originals[2:],
                "detail": f"name 完全归一重名: {originals}",
                "recommend": "禁止新造；复用或合并后重命名",
                "block": True,
            })

    # 两两比较
    n = len(skills)
    checked = set()
    for i in range(n):
        for j in range(i + 1, n):
            a, b = skills[i], skills[j]
            key = (a["name"], b["name"])
            if key in checked:
                continue
            checked.add(key)
            # name 近似
            dist = levenshtein(a["_n"], b["_n"])
            jac = jaccard(a["_t"], b["_t"])
            overlap_trig = len(a["_t"] & b["_t"])
            rec = None
            if dist <= 2 and a["_n"] != b["_n"]:
                rec = ("NAME_NEAR", f"name 编辑距离={dist}，易混淆", "重命名其一避免召回歧义", False)
            elif jac >= 0.7:
                rec = ("REUSE", f"description Jaccard={jac:.2f}", "直接复用已有技能，不新造", False)
            elif 0.5 <= jac < 0.7:
                rec = ("EXTEND", f"description Jaccard={jac:.2f}", "扩展已有技能而非另起炉灶", False)
            elif jac < 0.5 and overlap_trig >= 3:
                rec = ("NARROW", f"触发词重叠={overlap_trig}，Jaccard={jac:.2f}", "错开各自触发域，写清'不应触发'", False)
            if rec:
                findings.append({
                    "type": rec[0], "a": a["name"], "b": b["name"],
                    "detail": rec[1], "recommend": rec[2], "block": rec[3],
                })

    # 单技能 vs 库
    if new_one:
        new_one["_n"] = norm_name(new_one["name"])
        new_one["_t"] = tokenize(new_one["description"])
        for s in skills:
            dist = levenshtein(new_one["_n"], s["_n"])
            jac = jaccard(new_one["_t"], s["_t"])
            overlap_trig = len(new_one["_t"] & s["_t"])
            if new_one["_n"] == s["_n"]:
                findings.append({"type": "NAME_DUP", "a": new_one["name"], "b": s["name"],
                                 "detail": "与库中 name 完全归一重名", "recommend": "重命名或复用", "block": True})
            elif dist <= 2:
                findings.append({"type": "NAME_NEAR", "a": new_one["name"], "b": s["name"],
                                 "detail": f"name 编辑距离={dist}", "recommend": "重命名避免混淆", "block": False})
            elif jac >= 0.5:
                typ = "REUSE" if jac >= 0.7 else "EXTEND"
                findings.append({"type": typ, "a": new_one["name"], "b": s["name"],
                                 "detail": f"description Jaccard={jac:.2f}", "recommend": ("复用已有" if typ == "REUSE" else "扩展已有"), "block": False})
            elif overlap_trig >= 3:
                findings.append({"type": "NARROW", "a": new_one["name"], "b": s["name"],
                                 "detail": f"触发词重叠={overlap_trig}", "recommend": "错开触发域", "block": False})
    return findings


def render_text(findings, md=False):
    if md:
        if not findings:
            return "# 技能发现检测\n\n✅ 未检测到重名或功能重叠。"
        lines = ["# 技能发现检测", "", "| 类型 | A | B | 详情 | 建议 |", "|------|---|---|------|------|"]
        for f in findings:
            lines.append(f"| {f['type']} | {f['a']} | {f.get('b','')} | {f['detail']} | {f['recommend']} |")
        return "\n".join(lines)
    if not findings:
        return "技能发现检测：✅ 未检测到重名或功能重叠。"
    lines = ["技能发现检测", "=" * 50]
    for f in findings:
        lines.append(f"[{f['type']}] {f['a']} <-> {f.get('b','')}")
        lines.append(f"    详情: {f['detail']}")
        lines.append(f"    建议: {f['recommend']}{'  ⛔阻断' if f.get('block') else ''}")
        lines.append("-" * 50)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skills-dir", help="含多个技能子目录的目录（每个子目录有 SKILL.md）")
    ap.add_argument("--registry", help="注册表 JSON（[{name,description}]）")
    ap.add_argument("--name", help="单技能 name（配合 --skills-dir 做 vs 库检测）")
    ap.add_argument("--desc", help="单技能 description")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--md", action="store_true")
    args = ap.parse_args()

    if args.registry:
        skills = load_from_reg(args.registry)
    elif args.skills_dir:
        skills = load_from_dir(args.skills_dir)
    else:
        print("错误：需 --skills-dir 或 --registry", file=sys.stderr)
        return 1

    new_one = None
    if args.name:
        new_one = {"name": args.name, "description": args.desc or ""}

    findings = analyze(skills, new_one)
    block = any(f.get("block") for f in findings)

    if args.json:
        print(json.dumps({"findings": findings, "block": block}, ensure_ascii=False, indent=2))
    else:
        print(render_text(findings, md=args.md))
    return 2 if block else 0


if __name__ == "__main__":
    sys.exit(main())
