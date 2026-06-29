#!/usr/bin/env python3
"""
scan_packages.py —— archunit-architecture-guard 技能的结构扫描器（阶段一）。

解析 Java/Kotlin 源文件，产出：
  1. 基础（根）包及其顶层子包。
  2. 内部"包 -> 包"依赖图（来自 import 语句）。
  3. 角色关键字频率表（controller/service/repository/domain/...）。
  4. 包级依赖循环（不依赖 ArchUnit 也能先把循环标出来）。

仅使用标准库，无第三方依赖。

用法：
    python scan_packages.py <源码根> [--base com.acme.shop] [--json]

省略 --base 时，使用最长公共包前缀作为基础包。
默认输出为人类可读格式；加 --json 输出机器可读格式。
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict, Counter

PACKAGE_RE = re.compile(r'^\s*package\s+([\w.]+)\s*;?', re.MULTILINE)
IMPORT_RE = re.compile(r'^\s*import\s+(?:static\s+)?([\w.]+)\s*;?', re.MULTILINE)

ROLE_KEYWORDS = [
    "controller", "web", "api", "resource", "endpoint", "rest",
    "service", "usecase", "application", "interactor",
    "domain", "model", "entity", "aggregate", "vo", "valueobject", "event",
    "repository", "dao", "persistence", "mapper",
    "infrastructure", "infra", "adapter", "port", "gateway", "client",
    "config", "dto", "viewmodel", "view", "ui", "shared", "common", "util",
]


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def collect_files(root):
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            if name.endswith((".java", ".kt")):
                yield os.path.join(dirpath, name)


def longest_common_prefix(packages):
    if not packages:
        return ""
    split = [p.split(".") for p in packages]
    prefix = []
    for parts in zip(*split):
        if len(set(parts)) == 1:
            prefix.append(parts[0])
        else:
            break
    return ".".join(prefix)


def find_cycles(graph):
    """用 DFS 返回所有循环（每个循环是一组包节点）。"""
    cycles = []
    seen_cycle_keys = set()
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(lambda: WHITE)
    stack = []

    def dfs(node):
        color[node] = GRAY
        stack.append(node)
        for nxt in sorted(graph.get(node, ())):
            if color[nxt] == GRAY:
                idx = stack.index(nxt)
                cyc = stack[idx:] + [nxt]
                key = tuple(sorted(set(cyc)))
                if key not in seen_cycle_keys:
                    seen_cycle_keys.add(key)
                    cycles.append(cyc)
            elif color[nxt] == WHITE:
                dfs(nxt)
        stack.pop()
        color[node] = BLACK

    for n in sorted(graph):
        if color[n] == WHITE:
            dfs(n)
    return cycles


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src_root", help="源码根目录，例如 src/main/java")
    ap.add_argument("--base", default=None, help="基础包；省略时取最长公共前缀")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    file_packages = {}     # 路径 -> 包名
    all_imports = defaultdict(set)  # 包名 -> 导入的全限定名集合
    for path in collect_files(args.src_root):
        text = read(path)
        m = PACKAGE_RE.search(text)
        if not m:
            continue
        pkg = m.group(1)
        file_packages[path] = pkg
        for imp in IMPORT_RE.findall(text):
            all_imports[pkg].add(imp)

    packages = sorted(set(file_packages.values()))
    base = args.base or longest_common_prefix(packages)

    # 内部包依赖图：只保留基础包之下的 import，约简为"导入方包 -> 被导入包"（去掉类名）。
    dep_map = defaultdict(set)
    for pkg, imports in all_imports.items():
        for fqn in imports:
            if base and not fqn.startswith(base + "."):
                continue
            target_pkg = fqn.rsplit(".", 1)[0]
            if target_pkg and target_pkg != pkg:
                dep_map[pkg].add(target_pkg)

    # 基础包下的顶层子包。
    top = Counter()
    for pkg in packages:
        if base and pkg.startswith(base + "."):
            top[pkg[len(base) + 1:].split(".")[0]] += 1
        elif pkg == base:
            top["(base)"] += 1

    # 所有包名分段里的角色关键字频率。
    roles = Counter()
    for pkg in packages:
        segs = set(pkg.lower().split("."))
        for kw in ROLE_KEYWORDS:
            if kw in segs:
                roles[kw] += 1

    cycles = find_cycles({k: v for k, v in dep_map.items()})

    result = {
        "src_root": args.src_root,
        "base_package": base,
        "package_count": len(packages),
        "file_count": len(file_packages),
        "top_level_packages": dict(top.most_common()),
        "role_keyword_counts": dict(roles.most_common()),
        "dependency_map": {k: sorted(v) for k, v in sorted(dep_map.items())},
        "cycles": cycles,
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    print(f"基础包          ：{base or '（未探测到）'}")
    print(f"包数 / 文件数    ：{len(packages)} / {len(file_packages)}")
    print("\n基础包下的顶层子包（按包数）：")
    for name, n in top.most_common():
        print(f"  {name:<20} {n}")
    print("\n角色关键字频率（用于模式识别的证据）：")
    for kw, n in roles.most_common():
        print(f"  {kw:<16} {n}")
    print(f"\n发现的包依赖循环：{len(cycles)} 个")
    for cyc in cycles:
        print("  循环：" + " -> ".join(c[len(base) + 1:] if base and c.startswith(base + '.') else c for c in cyc))
    if not cycles:
        print("  （无）")
    print("\n内部包依赖（导入方 -> 被导入方）：")
    for pkg in sorted(dep_map):
        short = pkg[len(base) + 1:] if base and pkg.startswith(base + ".") else pkg
        for tgt in sorted(dep_map[pkg]):
            tshort = tgt[len(base) + 1:] if base and tgt.startswith(base + ".") else tgt
            print(f"  {short}  ->  {tshort}")


if __name__ == "__main__":
    sys.exit(main())
