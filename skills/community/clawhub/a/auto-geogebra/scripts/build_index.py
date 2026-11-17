#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 GeoGebra manual（asciidoc）重建 data/commands-index.json（v1.3 新增）。

用法：
    python scripts/build_index.py                                  # 重建并输出到 data/commands-index.json（自动留 .bak）
    python scripts/build_index.py --out <文件>                     # 输出到指定文件（不覆盖现索引）
    python scripts/build_index.py --out <文件> --compare <现索引>  # 并输出与现有索引的字段级对照

默认探测本机手册目录（如 E:\\软件学习\\Geogebra资料\\manual-main\\en\\modules\\ROOT\\pages），
扫描 commands/*.adoc；可用 --manual 指定其他路径。
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys

DEFAULT_MANUAL = r"E:\软件学习\Geogebra资料\manual-main\en\modules\ROOT\pages"

SYNTAX_RE = re.compile(r"^(.+?\(.*\))\s*::\s*$")


def clean(s):
    s = s.replace("++", "").replace("_", "").replace("*", "")
    s = re.sub(r"`([^`]*)`", r"\1", s)
    s = re.sub(r"link:[^\s\[]*\[([^\]]*)\]", r"\1", s)
    s = re.sub(r"image:[^\s\[]*\[[^\]]*\]", "", s)
    return s.strip()


def parse_file(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    lines = raw.split("\n")
    title = ""
    for l in lines[:8]:
        m = re.match(r"^=\s+(.+?)\s+Command\s*$", l.strip())
        if m:
            title = m.group(1).strip()
            break
    name = os.path.splitext(os.path.basename(path))[0]
    syntax, descs = [], []
    i = 0
    while i < len(lines):
        l = lines[i]
        m = SYNTAX_RE.match(l)
        if m and re.match(r"^" + re.escape(name) + r"\s*\(", m.group(1).strip()):
            syntax.append(re.sub(r"[ \t\r\n]+", " ", m.group(1)).strip())
            j, buf = i + 1, []
            while j < len(lines) and lines[j].strip() and not SYNTAX_RE.match(lines[j]):
                if lines[j].lstrip().startswith(("[", "=")) or lines[j].strip() == "====":
                    break
                buf.append(lines[j].strip())
                j += 1
            descs.append(clean(" ".join(buf)))
            i = j
            continue
        i += 1
    examples = []
    for m in re.finditer(r"\[EXAMPLE\]\s*\n====\s*\n(.*?)\n====", raw, re.S):
        for line in m.group(1).split("\n"):
            line = line.strip()
            if line:
                examples.append(clean(line))
    return {
        "name": name,
        "title": title,
        "syntax": syntax,
        "description": " ".join(d for d in descs if d),
        "examples": examples,
        "source": path,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manual", default=DEFAULT_MANUAL)
    ap.add_argument("--out", default=None)
    ap.add_argument("--compare", default=None)
    args = ap.parse_args()

    cmds_dir = os.path.join(args.manual, "commands")
    if not os.path.isdir(cmds_dir):
        print("手册目录不存在：%s" % cmds_dir)
        sys.exit(1)

    files = sorted(f for f in os.listdir(cmds_dir) if f.endswith(".adoc"))
    commands, errors = [], []
    for f in files:
        path = os.path.join(cmds_dir, f)
        try:
            rec = parse_file(path)
            if not rec["syntax"]:
                errors.append({"name": rec["name"], "reason": "no syntax parsed（索引页/列表页，已跳过）"})
                continue
            commands.append(rec)
        except Exception as e:
            errors.append({"name": f, "reason": str(e)})
    commands.sort(key=lambda c: c["name"])

    out = {
        "commands": commands,
        "count": len(commands),
        "errors": errors,
        "generatedAt": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        "manualPagesDir": args.manual,
    }

    out_path = args.out or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "data", "commands-index.json")
    if args.out is None and os.path.exists(out_path):
        shutil.copy2(out_path, out_path + ".bak")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    print("已生成：%s（%d 条；errors %d）" % (out_path, len(commands), len(errors)))

    if args.compare:
        old = json.load(open(args.compare, encoding="utf-8"))
        old_map = {c["name"]: c for c in old.get("commands", [])}
        new_map = {c["name"]: c for c in commands}
        only_old = sorted(set(old_map) - set(new_map))
        only_new = sorted(set(new_map) - set(old_map))
        common = sorted(set(old_map) & set(new_map))
        syn_ok = sum(1 for n in common if old_map[n].get("syntax") == new_map[n].get("syntax"))
        desc_ok = sum(1 for n in common if old_map[n].get("description") == new_map[n].get("description"))
        print("对照：旧 %d 条 / 新 %d 条 / 共有 %d / 仅旧 %d / 仅新 %d" % (
            len(old_map), len(new_map), len(common), len(only_old), len(only_new)))
        print("syntax 完全一致：%d/%d；description 一致：%d/%d" % (
            syn_ok, len(common), desc_ok, len(common)))
        if only_old:
            print("仅旧（若替换将丢弃，需人工复核）：%s%s" % (
                only_old[:25], " …" if len(only_old) > 25 else ""))
        if only_new:
            print("仅新（新索引新增）：%s%s" % (
                only_new[:25], " …" if len(only_new) > 25 else ""))
        diffs = [n for n in common if old_map[n].get("syntax") != new_map[n].get("syntax")][:5]
        for n in diffs:
            print("syntax 差异示例 [%s]：\n  旧: %s\n  新: %s" % (
                n, old_map[n].get("syntax"), new_map[n].get("syntax")))
        ddiffs = [n for n in common if old_map[n].get("description") != new_map[n].get("description")][:4]
        for n in ddiffs:
            print("desc 差异示例 [%s]：\n  旧: %r\n  新: %r" % (
                n, old_map[n].get("description"), new_map[n].get("description")))


if __name__ == "__main__":
    main()
