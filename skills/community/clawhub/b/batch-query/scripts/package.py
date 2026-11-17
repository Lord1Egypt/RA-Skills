#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把技能目录打包成可分发的 zip 包。

产出结构（zip 内顶层为一层目录，解压后即为完整技能包）：

    xdcc-batch-query/
    ├── SKILL.md
    ├── SECURITY_AUDIT.md
    ├── scripts/   (6 个 .py)
    └── references/ (2 个 .md)

默认排除 .git / .workbuddy / __pycache__ / .venv / node_modules，
这些是开发期目录，不该随技能分发。

用法：
    python scripts/package.py                      # 输出到 dist/
    python scripts/package.py -o ../release.zip    # 指定输出文件
    python scripts/package.py --quiet              # 只输出结果路径
"""

import argparse
import os
import re
import sys
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
PKG_ROOT_NAME = "xdcc-batch-query"

# 打包时排除的目录（开发期产物 / 本机私有数据）
SKIP_DIRS = {".git", ".workbuddy", "__pycache__", ".venv", "venv", "node_modules", "dist"}

# 只允许这些扩展名进包，杜绝意外混入二进制或隐私文件
ALLOW_EXT = {".md", ".py", ".txt", ".json", ".yaml", ".yml"}


def read_frontmatter(path):
    """读 SKILL.md 的 YAML frontmatter，返回 (name, version) 或 (None, None)。"""
    try:
        with open(path, encoding="utf-8") as f:
            head = f.read(4096)
    except OSError:
        return None, None
    m = re.match(r"^---\r?\n(.*?)\r?\n---", head, re.S)
    if not m:
        return None, None
    name = re.search(r"^name:\s*(.+)$", m.group(1), re.M)
    version = re.search(r"^version:\s*(.+)$", m.group(1), re.M)
    return (
        name.group(1).strip().strip('"\'') if name else None,
        version.group(1).strip().strip('"\'') if version else None,
    )


def collect_files():
    """遍历项目根目录，返回 [(绝对路径, 包内相对路径), ...]。"""
    out = []
    for dirpath, dirnames, filenames in os.walk(PROJECT_DIR):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for fn in sorted(filenames):
            if os.path.splitext(fn)[1].lower() not in ALLOW_EXT:
                continue
            abs_path = os.path.join(dirpath, fn)
            rel = os.path.relpath(abs_path, PROJECT_DIR).replace(os.sep, "/")
            out.append((abs_path, rel))
    return out


def build(out_path, pretty=True):
    name, version = read_frontmatter(os.path.join(PROJECT_DIR, "SKILL.md"))
    if not name:
        print("错误: SKILL.md 缺失或 frontmatter 无 name 字段", file=sys.stderr)
        return 2

    files = collect_files()
    if not files:
        print("错误: 未收集到任何待打包文件", file=sys.stderr)
        return 2

    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)

    skipped = set()
    total = 0
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for abs_path, rel in files:
            if rel.startswith(".workbuddy/") or "__pycache__" in rel:
                skipped.add(rel)
                continue
            arc = f"{PKG_ROOT_NAME}/{rel}"
            zf.write(abs_path, arc)
            total += os.path.getsize(abs_path)
            if pretty:
                print(f"  + {arc}")

    if pretty:
        if skipped:
            print(f"  - 已排除 {len(skipped)} 个开发期文件：{', '.join(sorted(skipped)[:5])}")
        print("-" * 56)
        print(f"技能名 {name}  版本 {version or '未声明'}")
        print(f"文件 {len(files)} 个 | 原始 {total / 1024:.1f} KB | "
              f"压缩包 {os.path.getsize(out_path) / 1024:.1f} KB")
        print(f"输出：{out_path}")

    return 0


def main():
    ap = argparse.ArgumentParser(description="打包 xdcc-batch-query 技能为 zip")
    ap.add_argument("-o", "--out", default=None, help="输出 zip 路径，默认 dist/xdcc-batch-query-<version>.zip")
    ap.add_argument("--quiet", action="store_true", help="静默模式，仅输出结果路径")
    args = ap.parse_args()

    _, version = read_frontmatter(os.path.join(PROJECT_DIR, "SKILL.md"))
    if not args.out:
        out_dir = os.path.join(PROJECT_DIR, "dist")
        os.makedirs(out_dir, exist_ok=True)
        args.out = os.path.join(out_dir, f"{PKG_ROOT_NAME}-{version or '0.0.0'}.zip")

    rc = build(args.out, pretty=not args.quiet)
    if rc == 0 and args.quiet:
        print(os.path.abspath(args.out))
    return rc


if __name__ == "__main__":
    sys.exit(main())
