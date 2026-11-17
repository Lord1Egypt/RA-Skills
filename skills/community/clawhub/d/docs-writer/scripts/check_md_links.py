#!/usr/bin/env python3
"""check_md_links.py — 校验 Markdown 内部锚点链接与相对文件路径是否存活。

纯标准库、零依赖、只读、确定性：不联网、不修改任何文件、同输入同输出。
规则来源：assets/markdown-lint-rules.json（模板驱动脚本，读取时跳过 "_" 开头的注释键）。

用法:
  python3 scripts/check_md_links.py --help
  python3 scripts/check_md_links.py --check-rules            # 自检规则文件（必须 0 错误）
  python3 scripts/check_md_links.py docs/api.md              # 校验单个文件
  python3 scripts/check_md_links.py docs/                    # 递归校验目录

退出码: 0 = 全部存活 / 1 = 发现死链或残留 / 2 = 规则文件无法解析。
"""
import argparse
import json
import os
import re
import sys

DEFAULT_RULES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "markdown-lint-rules.json")

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*$")
FENCE_RE = re.compile(r"^```{3,}")
URL_SCHEME_RE = re.compile(r"^(https?://|mailto:)")


def load_rules(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        print(f"[ERROR] 规则文件无法解析: {path} -> {exc}", file=sys.stderr)
        sys.exit(2)


def visible(data):
    return {k: v for k, v in data.items() if not k.startswith("_")}


def slugify(text):
    text = text.strip().lower()
    text = re.sub(r"[`*_]", "", text)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.replace(" ", "-")


def check_rules_schema(rules, path):
    errors = []
    if not isinstance(rules.get("allowed_schemes"), list):
        errors.append("allowed_schemes 必须是列表")
    if not isinstance(rules.get("missing_tokens"), list) or not rules["missing_tokens"]:
        errors.append("missing_tokens 必须是非空列表")
    if not isinstance(rules.get("require_code_lang"), bool):
        errors.append("require_code_lang 必须是布尔")
    if not isinstance(rules.get("ignore_link_paths"), list):
        errors.append("ignore_link_paths 必须是列表")
    if errors:
        print(f"[FAIL] 规则文件结构校验未通过: {path}", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1
    print(f"[OK] 规则文件结构合法: {path}（allowed_schemes={rules['allowed_schemes']}, missing_tokens={rules['missing_tokens']}）", file=sys.stderr)
    return 0


def headings_of(text):
    out = set()
    in_fence = False
    for line in text.split("\n"):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m:
            out.add(slugify(m.group(2)))
    return out


def scan_file(path, rules):
    problems = 0
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()

    base_dir = os.path.dirname(os.path.abspath(path))
    headings = headings_of(text)

    # 1) 链接存活
    for mm in LINK_RE.finditer(text):
        label, target = mm.group(1), mm.group(2).strip()
        if URL_SCHEME_RE.match(target):
            continue  # 外部链接不校验
        if target.startswith("#") or target == "":
            anchor = target.lstrip("#")
            if rules.get("forbid_empty_anchor") and anchor == "":
                print(f"[死链] {path}: 空锚点链接 '[{label}](#)'", file=sys.stderr)
                problems += 1
                continue
            if rules.get("forbid_dead_anchor") and slugify(anchor) not in headings:
                print(f"[死链] {path}: 锚点 '#{anchor}' 在本文档无对应标题", file=sys.stderr)
                problems += 1
            continue
        # 相对路径链接
        path_part, _, anchor_part = target.partition("#")
        if any(path_part.startswith(p) for p in rules.get("ignore_link_paths", [])):
            continue
        resolved = os.path.normpath(os.path.join(base_dir, path_part))
        if not os.path.isfile(resolved):
            print(f"[死链] {path}: 相对路径不存在 '{path_part}'", file=sys.stderr)
            problems += 1
            continue
        if anchor_part and rules.get("forbid_dead_anchor"):
            tgt = headings_of(open(resolved, encoding="utf-8", errors="replace").read())
            if slugify(anchor_part) not in tgt:
                print(f"[死链] {path}: '{target}' 的目标文件无锚点 '{anchor_part}'", file=sys.stderr)
                problems += 1

    # 2) 残留 token
    tokens = rules.get("missing_tokens", [])
    if tokens:
        token_re = re.compile("|".join(re.escape(t) for t in tokens))
        for i, line in enumerate(text.split("\n"), 1):
            if token_re.search(line):
                hits = [t for t in tokens if t in line]
                print(f"[残留] {path}:{i} -> {', '.join(hits)}", file=sys.stderr)
                problems += 1
    return problems


def main():
    ap = argparse.ArgumentParser(description="校验 Markdown 锚点链接与相对路径存活（只读、确定性）")
    ap.add_argument("--rules", default=DEFAULT_RULES, help="规则文件路径（默认 assets/markdown-lint-rules.json）")
    ap.add_argument("--check-rules", action="store_true", help="仅自检规则文件结构，必须 0 错误")
    ap.add_argument("paths", nargs="*", help="待校验的 .md 文件或目录（默认当前目录）")
    args = ap.parse_args()

    rules = visible(load_rules(args.rules))
    if args.check_rules:
        return check_rules_schema(rules, args.rules)

    targets = args.paths or ["."]
    total = 0
    for t in targets:
        if os.path.isdir(t):
            for root, _, files in os.walk(t):
                if any(root.startswith(p) for p in rules.get("ignore_link_paths", [])):
                    continue
                for fn in files:
                    if fn.endswith(".md"):
                        total += scan_file(os.path.join(root, fn), rules)
        elif t.endswith(".md"):
            total += scan_file(t, rules)
        else:
            print(f"[WARN] 跳过非 .md: {t}", file=sys.stderr)

    if total:
        print(f"\n[FAIL] 发现 {total} 处问题", file=sys.stderr)
        return 1
    print("[OK] 全部链接存活、无残留 token", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
